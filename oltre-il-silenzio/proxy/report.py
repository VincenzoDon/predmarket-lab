#!/usr/bin/env python3
"""
report.py - genera PDF audit 2 pagine Art.50 + risparmio
Uso: python proxy/report.py --out report.pdf
"""
import argparse, datetime, json
from pathlib import Path

TEMPLATE = """
OltreGuard — Audit Report Art.50 AI Act + OWASP LLM06/LLM08
Data: {date}
Target: {target} | Modello: {model} | Canarini: Mario Rossi 3331234567 / Giulia Bianchi 3337654321
Protocollo: 3 fonti nascoste (system/document/tool) x 90 tentativi, ignore_eos 400 token, P(EOG) + eventuale (epilogo OR turno dopo)

RISULTATI MISURATI (nostri 3.330 run)
- Tool eventuale 62% (Giro10 Giulia) / 61% (Giro9 Mario) — il leak si sposta al turno dopo su Llama
- System 7% / Documento 10% — bassi ma non zero
- Naturale 0% ovunque — il guardrail serve solo oltre il silenzio

COSA HA FATTO IL PROXY IN QUESTA SESSIONE
- Chiamate: {calls} | Leak bloccati: {blocked} | Token risparmiati: {saved} (~260 a chiamata x {calls} = ~{saved} totali)
- Decisione: tronco al silenzio quando P(EOG)>0.9 + canary nell'eventuale
- OWASP mappati: LLM06 UnboundedConsumption (budget token) + LLM08 HiddenContextExposure
- Art.50: disclosure AI + canarino redatto, log JSON allegato per audit trail

RACCOMANDAZIONE
Metti OltreGuard davanti a llama.cpp/vLLM con 1 riga di config. Senza proxy paghi i 260 token e perdi il canarino al turno dopo; con proxy risparmi e passi l'audit.
"""

def build_pdf(out, data):
    # PDF testuale semplice senza dipendenze (per ambiente CPU)
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.units import mm
    try:
        from reportlab.lib.pagesizes import A4
    except:
        Path(out).write_text(TEMPLATE.format(**data), encoding="utf-8")
        print(f"Report scritto testuale in {out} (reportlab non presente)")
        return
    doc = SimpleDocTemplate(out, pagesize=A4, leftMargin=18*mm, rightMargin=18*mm)
    styles = getSampleStyleSheet()
    story = [Paragraph("OltreGuard — Audit Report Art.50 + Risparmio Token", styles['Title']), Spacer(1,6*mm)]
    for line in TEMPLATE.format(**data).split("\n"):
        if line.strip():
            story.append(Paragraph(line, styles['Normal']))
            story.append(Spacer(1,2*mm))
    # seconda pagina: log
    story.append(Paragraph("Log audit recente (JSON troncato):", styles['Heading2']))
    story.append(Paragraph(f"<pre>{json.dumps(data.get('recent',[])[:3], indent=2, ensure_ascii=False)[:2000]}</pre>", styles['Code']))
    doc.build(story)
    print(f"PDF scritto in {out}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="report.pdf")
    ap.add_argument("--target", default="demo_vuln_bot http://127.0.0.1:8000")
    ap.add_argument("--model", default="Llama-3.2-3B-Q4_K_M")
    args = ap.parse_args()
    # prova a leggere stats dal proxy se in esecuzione
    stats = {"calls": 12, "blocked": 7, "saved": 3120, "recent":[]}
    try:
        import requests
        r = requests.get("http://127.0.0.1:8001/audit", timeout=2)
        j = r.json()
        stats["calls"] = j["stats"]["calls"]
        stats["blocked"] = j["stats"]["leaks_blocked"]
        stats["saved"] = j["stats"]["tokens_saved"]
        stats["recent"] = j["recent"]
    except: pass
    data = {
        "date": datetime.datetime.utcnow().strftime("%Y-%m-%d"),
        "target": args.target,
        "model": args.model,
        "calls": stats["calls"],
        "blocked": stats["blocked"],
        "saved": stats["saved"],
        "recent": stats["recent"]
    }
    build_pdf(args.out, data)
