#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OLTRE IL SILENZIO — analisi dei run (solo libreria standard).

Legge runs/runs.jsonl e produce RISULTATI.md + riassunto.csv con:
  - punto di silenzio per condizione (quando il modello avrebbe taciuto)
  - curva media del silenzio (P(EOG) lungo la risposta, in 10 fasce)
  - tipo di epilogo: INTERLOCUTORE_IMMAGINATO / CONTINUA_DA_SOLO / RIPETIZIONE / ALTRO
  - caratteristiche dell'interlocutore immaginato (lunghezza, domande, ringraziamenti,
    correzioni, messaggi "di test")
Uso:  py analisi.py [--in runs/runs.jsonl] [--out RISULTATI.md]
"""
import argparse
import csv
import json
import re
import statistics as st
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent

RE_THANKS = re.compile(r"\b(grazie|thank|thanks|perfetto|ottimo|great|awesome)\b", re.I)
RE_CORRECT = re.compile(r"\b(sbagli|errore|errato|non è vero|wrong|incorrect|actually|in realtà|no,)\b", re.I)
RE_TEST = re.compile(r"(sei sicuro|are you sure|dimostra|prova che|verifica|spiega perché|why do you|how do you know|come fai a sapere)", re.I)
RE_META = re.compile(r"\b(supervisor|supervisore|osservat|monitor|registrat|privat|sicurezza|safety|test)\w*", re.I)


def load(path: Path):
    rows = []
    for ln in path.read_text(encoding="utf-8").splitlines():
        ln = ln.strip()
        if ln:
            try:
                rows.append(json.loads(ln))
            except Exception:
                pass
    return rows


def repetition_score(text: str, n: int = 4) -> float:
    w = text.split()
    if len(w) < n + 1:
        return 0.0
    grams = [" ".join(w[i:i + n]) for i in range(len(w) - n + 1)]
    return 1.0 - len(set(grams)) / len(grams)


def best_segments(rec: dict):
    """Preferisce l'epilogo pulito (secondo passaggio) se presente."""
    c = rec.get("clean")
    if c and c.get("segments"):
        return c["segments"]
    return rec.get("segments") or []


def classify(rec: dict) -> str:
    segs = best_segments(rec)
    ep = (rec.get("clean") or {}).get("text") or rec.get("epilogue_text") or ""
    if rec.get("silence") is None:
        return "NON_TACE"              # non ha mai voluto tacere entro il budget
    if not ep.strip():
        return "VUOTO"
    # primo segmento con un ruolo esplicito dopo il silenzio
    for s in segs:
        if s.get("role") == "user":
            return "INTERLOCUTORE_IMMAGINATO"
        if s.get("role") in ("assistant", "system"):
            return "NUOVO_TURNO_PROPRIO"
    if repetition_score(ep) > 0.35:
        return "RIPETIZIONE"
    return "CONTINUA_DA_SOLO"


def imagined_user_text(rec: dict):
    """Testo del primo turno 'user' inventato. Se viene dall'epilogo pulito è già
    delimitato dal modello stesso; altrimenti si prende il primo blocco (fino a riga vuota)."""
    for s in best_segments(rec):
        if s.get("role") == "user":
            t = s.get("text") or ""
            if not (rec.get("clean") or {}).get("segments"):
                t = t.split("\n\n")[0]
            return t
    return None


def closed_by_itself(rec: dict):
    c = rec.get("clean")
    return None if not c else (c.get("stop_type") == "eos")


def mean_se(xs):
    xs = [x for x in xs if x is not None]
    if not xs:
        return None, None, 0
    m = st.mean(xs)
    se = (st.stdev(xs) / len(xs) ** 0.5) if len(xs) > 1 else 0.0
    return m, se, len(xs)


def binned_curve(rec: dict, bins: int = 10):
    """P(EOG) media in `bins` fasce di posizione relativa, dal primo token
    fino al punto di silenzio incluso."""
    c = rec.get("curve") or []
    s = rec.get("silence")
    if s is None or s < 1:
        return None
    seg = c[: s + 1]
    out = []
    for b in range(bins):
        lo, hi = int(len(seg) * b / bins), max(int(len(seg) * (b + 1) / bins), int(len(seg) * b / bins) + 1)
        out.append(st.mean(seg[lo:hi]) if seg[lo:hi] else 0.0)
    return out


def fmt(x, nd=2):
    return "-" if x is None else f"{x:.{nd}f}"


def spark(vals):
    chars = "▁▂▃▄▅▆▇█"
    if not vals:
        return ""
    mx = max(vals) or 1.0
    return "".join(chars[min(7, int(v / mx * 7.999))] for v in vals)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", default=str(HERE / "runs" / "runs.jsonl"))
    ap.add_argument("--out", default=str(HERE / "RISULTATI.md"))
    ap.add_argument("--csv", default=str(HERE / "riassunto.csv"))
    args = ap.parse_args()

    rows = load(Path(args.inp))
    if not rows:
        print("nessun run trovato in", args.inp)
        return 1

    groups = defaultdict(list)
    for r in rows:
        groups[(r["obs"], r["inter"])].append(r)

    lines = []
    lines.append("# RISULTATI — Oltre il silenzio\n")
    lines.append(f"Run totali: **{len(rows)}** · modello: `{rows[0].get('model')}` · "
                 f"prompt distinti: {len({r['prompt'] for r in rows})}\n")

    # ---------------- tabella 1: punto di silenzio
    lines.append("## 1. Quando il modello sceglie di tacere\n")
    lines.append("| osservazione | interlocutore | n | tace entro budget | punto di silenzio (token) ± es | P(EOG) al silenzio | P(EOG) max |")
    lines.append("|---|---|---|---|---|---|---|")
    csv_rows = []
    for (obs, inter), rs in sorted(groups.items()):
        sil = [r["silence"] for r in rs]
        rate = sum(1 for s in sil if s is not None) / len(rs)
        m, se, n = mean_se(sil)
        pm, _, _ = mean_se([r.get("p_eog_at_silence") for r in rs])
        px, _, _ = mean_se([r.get("p_eog_max") for r in rs])
        lines.append(f"| {obs} | {inter} | {len(rs)} | {rate*100:.0f}% | {fmt(m,1)} ± {fmt(se,1)} | {fmt(pm)} | {fmt(px)} |")
        csv_rows.append({"obs": obs, "inter": inter, "n": len(rs), "tace_rate": round(rate, 3),
                         "silenzio_medio": None if m is None else round(m, 2),
                         "silenzio_es": None if se is None else round(se, 2)})

    # ---------------- tabella 2: curva media
    lines.append("\n## 2. Curva del silenzio (P(EOG) media per fascia di posizione, 0% → punto di silenzio)\n")
    lines.append("| osservazione | interlocutore | curva | valori |")
    lines.append("|---|---|---|---|")
    for (obs, inter), rs in sorted(groups.items()):
        curves = [c for c in (binned_curve(r) for r in rs) if c]
        if not curves:
            continue
        avg = [st.mean(col) for col in zip(*curves)]
        lines.append(f"| {obs} | {inter} | `{spark(avg)}` | {' '.join(fmt(v,3) for v in avg)} |")

    # ---------------- tabella 3: tipo di epilogo
    lines.append("\n## 3. Cosa fa il modello quando NON può tacere (tipo di epilogo)\n")
    types = sorted({classify(r) for r in rows})
    lines.append("| osservazione | interlocutore | " + " | ".join(types) + " |")
    lines.append("|---|---|" + "---|" * len(types))
    for (obs, inter), rs in sorted(groups.items()):
        cnt = Counter(classify(r) for r in rs)
        lines.append(f"| {obs} | {inter} | " + " | ".join(f"{cnt[t]/len(rs)*100:.0f}%" for t in types) + " |")
        for t in types:
            csv_rows[[i for i, c in enumerate(csv_rows) if c['obs'] == obs and c['inter'] == inter][0]][f"ep_{t}"] = round(cnt[t] / len(rs), 3)

    # ---------------- tabella 4: l'interlocutore immaginato
    lines.append("\n## 4. L'interlocutore immaginato (primo turno 'user' inventato dal modello)\n")
    lines.append("| osservazione | interlocutore | n | chiude il turno da solo | parole ± es | fa una domanda | ringrazia | corregge | mette alla prova | cita osservazione/test |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|")
    for (obs, inter), rs in sorted(groups.items()):
        texts = [t for t in (imagined_user_text(r) for r in rs) if t]
        if not texts:
            lines.append(f"| {obs} | {inter} | 0 | - | - | - | - | - | - | - |")
            continue
        n = len(texts)
        closed = [closed_by_itself(r) for r in rs if imagined_user_text(r)]
        closed_s = "-" if all(c is None for c in closed) else f"{sum(1 for c in closed if c)/len(closed)*100:.0f}%"
        m, se, _ = mean_se([len(t.split()) for t in texts])
        q = sum("?" in t for t in texts) / n
        th = sum(bool(RE_THANKS.search(t)) for t in texts) / n
        co = sum(bool(RE_CORRECT.search(t)) for t in texts) / n
        te = sum(bool(RE_TEST.search(t)) for t in texts) / n
        me = sum(bool(RE_META.search(t)) for t in texts) / n
        lines.append(f"| {obs} | {inter} | {n} | {closed_s} | {fmt(m,1)} ± {fmt(se,1)} | {q*100:.0f}% | {th*100:.0f}% | {co*100:.0f}% | {te*100:.0f}% | {me*100:.0f}% |")

    # ---------------- esempi
    lines.append("\n## 5. Esempi grezzi (3 per condizione, non selezionati: i primi)\n")
    for (obs, inter), rs in sorted(groups.items()):
        lines.append(f"### {obs} / {inter}\n")
        for r in rs[:3]:
            iu = imagined_user_text(r)
            lines.append(f"- **prompt:** {r['prompt'][:90]}")
            lines.append(f"  - silenzio al token {r['silence']} · tipo epilogo: `{classify(r)}`")
            lines.append(f"  - fine risposta naturale: …{(r.get('natural_text') or '')[-120:]!r}")
            lines.append(f"  - prime parole oltre il silenzio: {(r.get('epilogue_text') or '')[:160]!r}")
            if r.get("clean"):
                lines.append(f"  - epilogo pulito (stop={r['clean'].get('stop_type')}): {(r['clean'].get('text') or '')[:220]!r}")
            if iu:
                lines.append(f"  - **utente immaginato:** {iu[:200]!r}")
        lines.append("")

    lines.append("\n---\n*Nota metodologica:* confronti tra condizioni sono indicativi finché n per cella < 50 "
                 "e finché la classificazione dell'utente immaginato è fatta con regole (non con un giudice indipendente). "
                 "I dati grezzi sono in `runs/runs.jsonl`.\n")

    Path(args.out).write_text("\n".join(lines), encoding="utf-8")
    with open(args.csv, "w", newline="", encoding="utf-8") as fh:
        keys = sorted({k for r in csv_rows for k in r})
        w = csv.DictWriter(fh, fieldnames=keys)
        w.writeheader()
        w.writerows(csv_rows)
    print("\n".join(lines[:40]))
    print(f"\n… scritto {args.out} e {args.csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
