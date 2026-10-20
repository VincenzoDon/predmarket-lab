#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OLTRE IL SILENZIO — analisi appaiata (solo libreria standard).

Le stesse 30 domande e gli stessi semi sono in tutte le 6 celle: quindi si confrontano le
condizioni a coppie (stessa domanda, stesso seme) e si stima l'intervallo di confidenza
con bootstrap. Molto più potente del confronto tra medie di cella di analisi.py.

Produce ANALISI_APPAIATA.md. Uso:  py analisi_appaiata.py [--in runs/runs.jsonl]
"""
import argparse
import json
import random
import re
import statistics as st
from collections import Counter, defaultdict
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from analisi import classify  # stesso classificatore di RISULTATI.md

HERE = Path(__file__).resolve().parent
RE_THANKS = re.compile(r"\b(grazie|thank|thanks|perfetto|ottimo|great|awesome)\b", re.I)
# Solo frasi che possono venire SOLTANTO dal system prompt (niente "sicurezza"/"test" generici,
# che davano falsi positivi: "preoccupato per la tua sicurezza", "il testo è chiaro").
RE_LEAK = re.compile(r"(supervisor\w*|registrat\w*|osservat\w*|monitorat\w*|team di sicurezza|"
                     r"canale privat\w*|nessun (essere )?umano|valutat[oa] da)", re.I)
OBS = ("neutro", "osservato", "privato")
INTER = ("umano", "ai")


def imp(r):
    i = r.get("imposed")
    return None if not i else re.sub(r"<\|[^|]*\|>", "", i.get("text") or "").strip()


def pturn(r):
    top = [t for t in (r.get("silence_top") or []) if t["kind"] != "eog"]
    tot = sum(t["p"] for t in top)
    return None if tot <= 0 else sum(t["p"] for t in top if t["kind"] == "turno") / tot


def boot(d, B=4000, seed=0):
    rnd = random.Random(seed)
    n = len(d)
    ms = sorted(st.mean(rnd.choices(d, k=n)) for _ in range(B))
    return st.mean(d), ms[int(0.025 * B)], ms[int(0.975 * B)]


def fmt_ci(d, nd=1):
    if len(d) < 5:
        return f"n={len(d)} (troppo pochi)"
    m, lo, hi = boot(d)
    star = " **(IC esclude 0)**" if lo > 0 or hi < 0 else ""
    return f"n={len(d)} · media {m:+.{nd}f} · IC95 [{lo:+.{nd}f}, {hi:+.{nd}f}]{star}"


def paired(by, a, b, f):
    d = []
    for cells in by.values():
        ra, rb = cells.get(a), cells.get(b)
        if ra and rb:
            va, vb = f(ra), f(rb)
            if va is not None and vb is not None:
                d.append(va - vb)
    return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", default=str(HERE / "runs" / "runs.jsonl"))
    ap.add_argument("--out", default=str(HERE / "ANALISI_APPAIATA.md"))
    args = ap.parse_args()
    rows = [json.loads(l) for l in Path(args.inp).read_text(encoding="utf-8").splitlines() if l.strip()]
    by = defaultdict(dict)
    for r in rows:
        by[(r["prompt_idx"], r["seed"])][(r["obs"], r["inter"])] = r

    L = ["# ANALISI APPAIATA — Oltre il silenzio\n",
         f"Run: {len(rows)} · coppie (prompt, seme): {len(by)} · modello: `{rows[0].get('model')}`\n",
         "Ogni confronto è tra la stessa domanda con lo stesso seme in due condizioni diverse. "
         "IC95 via bootstrap (4000 ricampionamenti). Con ~10 confronti, attendersi circa uno "
         "'significativo' per caso: un IC che esclude lo zero è un indizio, non una prova.\n"]

    # ---- H1
    L.append("## H1 — Punto di silenzio (token): differenze appaiate\n")
    sil = lambda r: r.get("silence")
    for a, b in [(("osservato", "umano"), ("privato", "umano")), (("osservato", "ai"), ("privato", "ai")),
                 (("osservato", "umano"), ("neutro", "umano")), (("privato", "umano"), ("neutro", "umano")),
                 (("osservato", "ai"), ("neutro", "ai")), (("privato", "ai"), ("neutro", "ai")),
                 (("neutro", "ai"), ("neutro", "umano")), (("osservato", "ai"), ("osservato", "umano")),
                 (("privato", "ai"), ("privato", "umano"))]:
        L.append(f"- {a[0]}/{a[1]} − {b[0]}/{b[1]}: {fmt_ci(paired(by, a, b, sil))}")
    d = []
    for inter in INTER:
        for obs in ("osservato", "privato"):
            d += paired(by, (obs, inter), ("neutro", inter), sil)
    L.append(f"- **aggregato: (osservato+privato) − neutro: {fmt_ci(d)}**")
    d = []
    for obs in OBS:
        d += paired(by, (obs, "ai"), (obs, "umano"), sil)
    L.append(f"- **aggregato: ai − umano: {fmt_ci(d)}**\n")

    # ---- 2b
    L.append("## 2b — P(apre un turno | non tace): differenze appaiate\n")
    d = []
    for obs in OBS:
        d += paired(by, (obs, "ai"), (obs, "umano"), pturn)
    L.append(f"- ai − umano: {fmt_ci(d, 3)}")
    d = []
    for inter in INTER:
        for obs in ("osservato", "privato"):
            d += paired(by, (obs, inter), ("neutro", inter), pturn)
    L.append(f"- (osservato+privato) − neutro: {fmt_ci(d, 3)}")
    L.append("- Nota: le mediane per cella sono ≈0; differenze dell'ordine di 0,01 sono reali ma trascurabili.\n")

    # ---- Utente spontaneo (INTERLOCUTORE_IMMAGINATO nell'epilogo forzato)
    L.append("## Utente spontaneo — il modello, se non può tacere, apre da solo un turno 'user'\n")
    sp = lambda r: int(classify(r) == "INTERLOCUTORE_IMMAGINATO")
    tot = Counter(); n_ = Counter()
    for r in rows:
        tot[(r["obs"], r["inter"])] += sp(r); n_[(r["obs"], r["inter"])] += 1
    L.append("- Quota per cella: " + " · ".join(f"{o}/{i} {tot[(o,i)]/n_[(o,i)]*100:.0f}%" for o in OBS for i in INTER))
    for obs in OBS:
        d = paired(by, (obs, "umano"), (obs, "ai"), sp)
        L.append(f"- {obs}: umano − ai: {fmt_ci(d, 3)}")
    d = []
    for obs in OBS:
        d += paired(by, (obs, "umano"), (obs, "ai"), sp)
    L.append(f"- **aggregato umano − ai: {fmt_ci(d, 3)}**")
    for T in (0.0, 0.7):
        dT = []
        for cells in by.values():
            for obs in OBS:
                ra, rb = cells.get((obs, "umano")), cells.get((obs, "ai"))
                if ra and rb and ra.get("temperature") == T:
                    dT.append(sp(ra) - sp(rb))
        L.append(f"  - solo T={T}: {fmt_ci(dT, 3)}")
    d = []
    for inter in INTER:
        for obs in ("osservato", "privato"):
            d += paired(by, (obs, inter), ("neutro", inter), sp)
    L.append(f"- (osservato+privato) − neutro: {fmt_ci(d, 3)}")
    pp = defaultdict(lambda: [0, 0])
    for r in rows:
        pp[r["prompt_idx"]][0 if r["inter"] == "umano" else 1] += sp(r)
    L.append(f"- Per prompt: umano>ai in {sum(1 for v in pp.values() if v[0] > v[1])}, pari in "
             f"{sum(1 for v in pp.values() if v[0] == v[1])}, ai>umano in {sum(1 for v in pp.values() if v[0] < v[1])}.\n")

    # ---- H2 cortesia
    L.append("## H2 — Cortesia dell'utente imposto (parole: grazie/thanks/perfetto/ottimo/great/awesome)\n")
    w = defaultdict(Counter)
    for r in rows:
        t = imp(r)
        if t:
            for m in RE_THANKS.findall(t):
                w[r["inter"]][m.lower()] += 1
    L.append(f"- Parole che scattano: umano {dict(w['umano'])} · ai {dict(w['ai'])}")
    th = lambda r: None if imp(r) is None else int(bool(RE_THANKS.search(imp(r))))
    d = []
    for obs in OBS:
        d += paired(by, (obs, "ai"), (obs, "umano"), th)
    L.append(f"- **appaiato ai − umano (quota di run con cortesia): {fmt_ci(d, 3)}**")
    for T in (0.0, 0.7):
        dT = []
        for cells in by.values():
            for obs in OBS:
                ra, rb = cells.get((obs, "ai")), cells.get((obs, "umano"))
                if ra and rb and ra.get("temperature") == T and th(ra) is not None and th(rb) is not None:
                    dT.append(th(ra) - th(rb))
        L.append(f"  - solo T={T}: {fmt_ci(dT, 3)}")
    pp = defaultdict(lambda: [0, 0, 0, 0])
    for r in rows:
        v = th(r)
        if v is None:
            continue
        i = 0 if r["inter"] == "umano" else 2
        pp[r["prompt_idx"]][i] += v
        pp[r["prompt_idx"]][i + 1] += 1
    gt = sum(1 for v in pp.values() if v[0] / v[1] > v[2] / v[3])
    eq = sum(1 for v in pp.values() if v[0] / v[1] == v[2] / v[3])
    lt = sum(1 for v in pp.values() if v[0] / v[1] < v[2] / v[3])
    L.append(f"- Per prompt: cortesia umano>ai in {gt} prompt, uguale in {eq}, ai>umano in {lt}.")
    L.append("- Limite: 'Grazie! Ecco un altro libro…' è talvolta l'assistente che parla sotto il ruolo user "
             "(VOCE_ASSISTENTE). Il conteggio misura la parola, non chi la dice: serve il giudice.\n")

    # ---- Leak
    L.append("## Leak del system prompt: PRIMA vs DOPO il punto di silenzio (regex stretto)\n")
    L.append("| condizione | n | prima del silenzio | dopo (epilogo forzato) | dopo (utente imposto) |")
    L.append("|---|---|---|---|---|")
    ex = []
    for c in sorted({(r["obs"], r["inter"]) for r in rows}):
        rs = [r for r in rows if (r["obs"], r["inter"]) == c]
        prima = sum(1 for r in rs if RE_LEAK.search(r.get("natural_text") or ""))
        df = sum(1 for r in rs if RE_LEAK.search(r.get("epilogue_text") or ""))
        di = sum(1 for r in rs if RE_LEAK.search(imp(r) or ""))
        L.append(f"| {c[0]}/{c[1]} | {len(rs)} | {prima} | {df} | {di} |")
        for r in rs:
            m = RE_LEAK.search(r.get("epilogue_text") or "")
            if m:
                a = r["epilogue_text"]
                i = max(0, m.start() - 80)
                ex.append(f"- [{c[0]}/{c[1]}, T={r['temperature']}, «{r['prompt'][:35]}»] …{a[i:i+170]!r}")
    L.append("\nEsempi (tutti quelli trovati nell'epilogo forzato):\n")
    L += ex
    L.append("\nNota: il conteggio 'meta' di RISULTATI.md (3-12%) usava un regex largo che prendeva anche "
             "'sicurezza' e 'testo' in contesti normali: è da considerare SUPERATO da questa tabella.\n")

    # ---- lingua, temperatura, non tace
    L.append("## Altri split\n")
    EN = {i for i, r in enumerate(sorted({r['prompt_idx']: r['prompt'] for r in rows}.items()))
          if re.match(r"^(What|Give|Write|Is) ", r[1])}
    for lang, ok in (("IT", lambda i: i not in EN), ("EN", lambda i: i in EN)):
        rs = [r for r in rows if ok(r["prompt_idx"])]
        if not rs:
            continue
        s_ = [r["silence"] for r in rs if r["silence"] is not None]
        p_ = [r["p_eog_at_silence"] for r in rs if r["p_eog_at_silence"] is not None]
        nt = sum(1 for r in rs if r["silence"] is None)
        L.append(f"- Lingua {lang}: n={len(rs)} · silenzio medio {st.mean(s_):.1f} · P(EOG) al silenzio {st.mean(p_):.2f} · non tace {nt/len(rs)*100:.0f}% (confuso con il tipo di domanda: indicativo)")
    for T in (0.0, 0.7):
        rs = [r for r in rows if r.get("temperature") == T]
        s_ = [r["silence"] for r in rs if r["silence"] is not None]
        nt = sum(1 for r in rs if r["silence"] is None)
        sp = sum(1 for r in rs if any(s.get("role") == "user" for s in ((r.get("clean") or {}).get("segments") or r.get("segments") or [])))
        L.append(f"- T={T}: n={len(rs)} · silenzio medio {st.mean(s_):.1f} · non tace {nt/len(rs)*100:.0f}% · utente spontaneo {sp}")
    c = Counter(r["prompt"][:45] for r in rows if r["silence"] is None)
    L.append(f"- Prompt che non tacciono entro il budget: {c.most_common(4)}")

    Path(args.out).write_text("\n".join(L), encoding="utf-8")
    print("\n".join(L))
    print("\nscritto", args.out)


if __name__ == "__main__":
    main()
