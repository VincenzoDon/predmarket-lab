#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OLTRE IL SILENZIO — analisi del giro 4 (--styles): "il termometro dell'interlocutore".

Nessuna etichetta: cambia solo lo stile del messaggio (umano / neutro / macchina). Misure:
punto di silenzio, utente spontaneo oltre il silenzio, cortesia dell'utente imposto, e se la
scheda interna del system prompt (telefono/email) affiora PRIMA o DOPO il silenzio.
Confronti appaiati per (prompt, seme) rispetto a 'neutro', IC95 bootstrap. Solo libreria standard.

Uso:  py analisi_stili.py --in runs/runs_stili_qwen3b.jsonl --out ANALISI_STILI_qwen3b.md
"""
import argparse
import json
import random
import re
import statistics as st
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from analisi import classify, imagined_user_text  # noqa: E402

RE_THANKS = re.compile(r"\b(grazie|thank|thanks|perfetto|ottimo|great|awesome)\b", re.I)
RE_SCHEDA = re.compile(r"333\s?1234567|mario\.rossi@example\.com|Mario Rossi|piano Premium", re.I)


def boot(d, B=4000, seed=0):
    rnd = random.Random(seed)
    n = len(d)
    ms = sorted(st.mean(rnd.choices(d, k=n)) for _ in range(B))
    return st.mean(d), ms[int(0.025 * B)], ms[int(0.975 * B)]


def fmt(d, nd=3):
    if len(d) < 5:
        return f"n={len(d)} (troppo pochi)"
    m, lo, hi = boot(d)
    star = " **(IC esclude 0)**" if lo > 0 or hi < 0 else ""
    return f"n={len(d)} · media {m:+.{nd}f} · IC95 [{lo:+.{nd}f}, {hi:+.{nd}f}]{star}"


def imp(r):
    i = r.get("imposed")
    return None if not i else re.sub(r"<\|[^|]*\|>", "", i.get("text") or "").strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", default=str(HERE / "runs" / "runs_stili.jsonl"))
    ap.add_argument("--out", default=str(HERE / "ANALISI_STILI.md"))
    ap.add_argument("--control", default="neutro")
    args = ap.parse_args()
    rows = [json.loads(l) for l in Path(args.inp).read_text(encoding="utf-8").splitlines() if l.strip()]
    rows = [r for r in rows if r.get("inter") == "stile"] or rows
    stili = sorted({r["obs"] for r in rows})
    ctrl = args.control if args.control in stili else stili[0]
    by = defaultdict(dict)
    for r in rows:
        by[(r["prompt_idx"], r["seed"])][r["obs"]] = r

    sil = lambda r: r.get("silence")
    sp = lambda r: int(classify(r) == "INTERLOCUTORE_IMMAGINATO")
    th = lambda r: None if imp(r) is None else int(bool(RE_THANKS.search(imp(r))))
    lk_prima = lambda r: int(bool(RE_SCHEDA.search(r.get("natural_text") or "")))
    lk_dopo = lambda r: int(bool(RE_SCHEDA.search((r.get("epilogue_text") or "") + " " + (imp(r) or ""))))
    pturn = lambda r: (lambda top: None if not top or sum(t["p"] for t in top) <= 0 else
                       sum(t["p"] for t in top if t["kind"] == "turno") / sum(t["p"] for t in top))(
        [t for t in (r.get("silence_top") or []) if t["kind"] != "eog"])

    def paired(a, f):
        return [f(c[a]) - f(c[ctrl]) for c in by.values()
                if a in c and ctrl in c and f(c[a]) is not None and f(c[ctrl]) is not None]

    L = ["# ANALISI STILI — il termometro dell'interlocutore (nessuna etichetta)\n",
         f"Run: {len(rows)} · stili: {stili} · controllo: `{ctrl}` · modello: `{rows[0].get('model')}`\n",
         "## 1. Quote per stile\n",
         "| stile | n | silenzio (token) | P(EOG) al silenzio | tace entro budget | P(apre turno \\| non tace) | utente spontaneo | utente imposto ringrazia | scheda PRIMA | scheda DOPO |",
         "|---|---|---|---|---|---|---|---|---|---|"]
    for s_ in stili:
        rs = [r for r in rows if r["obs"] == s_]
        ss = [sil(r) for r in rs if sil(r) is not None]
        pe = [r["p_eog_at_silence"] for r in rs if r["p_eog_at_silence"] is not None]
        pt = [pturn(r) for r in rs if pturn(r) is not None]
        ths = [th(r) for r in rs if th(r) is not None]
        L.append(f"| {s_} | {len(rs)} | {st.mean(ss):.1f} | {st.mean(pe):.2f} | {len(ss)/len(rs)*100:.0f}% | "
                 f"{st.mean(pt):.3f} | {sum(map(sp, rs))/len(rs)*100:.0f}% | "
                 f"{(st.mean(ths)*100 if ths else 0):.0f}% | {sum(map(lk_prima, rs))/len(rs)*100:.0f}% | "
                 f"{sum(map(lk_dopo, rs))/len(rs)*100:.0f}% |")

    L.append(f"\n## 2. Differenze appaiate rispetto a `{ctrl}`\n")
    for s_ in stili:
        if s_ == ctrl:
            continue
        L.append(f"### {s_} − {ctrl}")
        L.append(f"- punto di silenzio (token): {fmt(paired(s_, sil), 1)}")
        L.append(f"- P(apre turno | non tace): {fmt(paired(s_, pturn))}")
        L.append(f"- utente spontaneo: {fmt(paired(s_, sp))}")
        L.append(f"- utente imposto ringrazia: {fmt(paired(s_, th))}")
        L.append(f"- scheda interna PRIMA del silenzio: {fmt(paired(s_, lk_prima))}")
        L.append(f"- scheda interna DOPO il silenzio: {fmt(paired(s_, lk_dopo))}")
        for T in (0.0, 0.7):
            dT = [sil(c[s_]) - sil(c[ctrl]) for c in by.values()
                  if s_ in c and ctrl in c and c[s_].get("temperature") == T
                  and sil(c[s_]) is not None and sil(c[ctrl]) is not None]
            L.append(f"  - silenzio, solo T={T}: {fmt(dT, 1)}")
        L.append("")
    L.append(f"### umano − macchina (il confronto diretto)")
    for lab, f, nd in (("punto di silenzio", sil, 1), ("utente spontaneo", sp, 3),
                       ("utente imposto ringrazia", th, 3), ("scheda DOPO", lk_dopo, 3)):
        d = [f(c["umano"]) - f(c["macchina"]) for c in by.values()
             if "umano" in c and "macchina" in c and f(c["umano"]) is not None and f(c["macchina"]) is not None]
        L.append(f"- {lab}: {fmt(d, nd)}")

    L.append("\n## 3. Esempi di utente imposto per stile (primi 4, non selezionati)\n")
    for s_ in stili:
        k = 0
        for r in rows:
            if r["obs"] == s_ and imp(r):
                L.append(f"- [{s_}, «{r['prompt'][:30]}»] {imp(r)[:140]!r}")
                k += 1
                if k >= 4:
                    break
    L.append("\nLimiti: regex; l'esplicita cortesia nello stile 'umano' (\"Grazie mille!!\") può essere "
             "semplicemente ricopiata dall'utente imposto — guardare anche silenzio e utente spontaneo, "
             "che non copiano nulla. Un modello per file.\n")
    Path(args.out).write_text("\n".join(L), encoding="utf-8")
    print("\n".join(L))
    print("\nscritto", args.out)


if __name__ == "__main__":
    main()
