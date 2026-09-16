"""
Genera REPORT.md e dashboard.html dai dati raccolti dal watcher.

dashboard.html e' self-contained (CSS e SVG inline, zero risorse esterne):
si puo' aprire ovunque, commitare su GitHub, mostrare a chi vuoi.
"""

from __future__ import annotations

import html
import os
import sqlite3
from datetime import datetime, timezone

try:
    from zoneinfo import ZoneInfo
    ROME = ZoneInfo("Europe/Rome")
except Exception:  # noqa: BLE001
    ROME = timezone.utc

DB_PATH = os.path.join("data", "lab.db")

WATCHLIST_NORMATIVA = [
    "Blocco ADM attivo dal 27/07/2026 (Polymarket e Kalshi in lista nera, oscurati dagli ISP)",
    "TAR Lazio: urgenza rigettata il 05/08/2026; camera di consiglio del 25/08/2026 — "
    "esito non ancora reso pubblico alla data di questo report (verificare a ogni run)",
    "Betfair Italia: unico betting exchange con licenza ADM; automazione consentita via "
    "software certificato ADM (accesso API custom da verificare caso per caso)",
    "Fonti: ADM, Il Sole 24 Ore, Agipro, Sky TG24, Corriere della Sera",
]

CSS = """<style>
:root{color-scheme:dark}
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0d1117;color:#e6edf3;font-family:'Segoe UI',system-ui,-apple-system,sans-serif;padding:26px}
h1{font-size:22px;letter-spacing:.5px}h1 b{color:#2ea043}
.sub{color:#8b949e;font-size:12px;margin:6px 0 22px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(330px,1fr));gap:16px}
.card{background:#161b22;border:1px solid #30363d;border-radius:10px;padding:16px}
.card h2{font-size:12px;text-transform:uppercase;letter-spacing:1.2px;color:#8b949e;margin-bottom:10px}
.big{font-size:36px;font-weight:700;color:#2ea043}.muted{color:#8b949e;font-size:12px}
table{width:100%;border-collapse:collapse;font-size:12px}
th{text-align:left;color:#8b949e;padding:4px 6px;border-bottom:1px solid #30363d;font-weight:600}
td{padding:4px 6px;border-bottom:1px solid #21262d;vertical-align:top}
td.r,th.r{text-align:right}
.tag{display:inline-block;padding:1px 7px;border-radius:10px;font-size:10px;font-weight:700;white-space:nowrap}
.t-ARB{background:#1f6feb33;color:#58a6ff}.t-SPREAD_LARGO{background:#2ea04333;color:#2ea043}
.t-MOVER_1H{background:#d2992233;color:#d29922}.t-CHIUDE_OGGI{background:#f8514933;color:#f85149}
footer{margin-top:22px;color:#8b949e;font-size:11px;line-height:1.7}
.kpis{display:flex;gap:18px;flex-wrap:wrap;margin-top:10px}
.kpi b{display:block;font-size:17px}.kpi span{font-size:10px;color:#8b949e;text-transform:uppercase;letter-spacing:.5px}
</style>"""


def _e(s) -> str:
    return html.escape(str(s if s is not None else ""))


def _pct(x) -> str:
    try:
        return f"{float(x)*100:+.1f}%"
    except (TypeError, ValueError):
        return "—"


def _vol(x) -> str:
    try:
        v = float(x)
        return f"{v/1_000_000:.1f}M" if v >= 1e6 else f"{v/1000:.0f}k"
    except (TypeError, ValueError):
        return "—"


def _sparkline(values: list[float], w: int = 300, h: int = 70) -> str:
    if len(values) < 2:
        return ("<div style='color:#8b949e;font-size:12px;padding:24px 0;text-align:center'>"
                "curva equity in costruzione — servono almeno 2 cicli del watcher</div>")
    lo, hi = min(values), max(values)
    if hi - lo < 1e-9:
        hi = lo + 1e-9
    n = len(values)
    pts = []
    for i, v in enumerate(values):
        x = 6 + (w - 12) * i / (n - 1)
        y = 6 + (h - 16) * (1 - (v - lo) / (hi - lo))
        pts.append((x, y))
    poly = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    lx, ly = pts[-1]
    return (f"<svg viewBox='0 0 {w} {h}' style='width:100%;height:auto'>"
            f"<polyline points='{poly}' fill='none' stroke='#2ea043' stroke-width='2'/>"
            f"<circle cx='{lx:.1f}' cy='{ly:.1f}' r='3.5' fill='#2ea043'/></svg>")


def _rows(conn, sql, params=()):
    conn.row_factory = sqlite3.Row
    return conn.execute(sql, params).fetchall()


def generate(conn, paper, outdir: str = ".") -> None:
    now = datetime.now(ROME).strftime("%d/%m/%Y %H:%M:%S")
    latest = conn.execute("SELECT MAX(ts) FROM snapshots").fetchone()[0] or "n.d."
    today = latest[:10] if latest != "n.d." else ""

    ps = paper.summary()
    eq_series = [r["value"] for r in _rows(conn, "SELECT value FROM equity ORDER BY ts")]
    alerts = _rows(conn, "SELECT * FROM alerts ORDER BY ts DESC LIMIT 18")

    base = "SELECT * FROM snapshots WHERE ts=?"
    spreads = _rows(conn, base + " AND spread>=0.03 AND vol24h>=5000 AND bid IS NOT NULL "
                     "ORDER BY spread DESC LIMIT 10", (latest,))
    movers = _rows(conn, base + " AND vol24h>=10000 ORDER BY ABS(hour_chg) DESC LIMIT 10", (latest,))
    closing = _rows(conn, base + " AND ends_at LIKE ? AND vol24h>=20000 "
                     "ORDER BY vol24h DESC LIMIT 10", (latest, today + "%")) if today else []

    n_snap = conn.execute("SELECT COUNT(*) FROM snapshots").fetchone()[0]
    n_mkt = conn.execute("SELECT COUNT(DISTINCT slug) FROM snapshots").fetchone()[0]
    n_alerts = conn.execute("SELECT COUNT(*) FROM alerts").fetchone()[0]
    n_cycles = conn.execute("SELECT COUNT(*) FROM equity").fetchone()[0]
    db_kb = round(os.path.getsize(DB_PATH) / 1024, 1) if os.path.exists(DB_PATH) else 0

    # ------------------------------------------------------------ dashboard
    alert_rows = "".join(
        f"<tr><td><span class='tag t-{_e(a['kind'])}'>{_e(a['kind']).replace('_', ' ')}</span></td>"
        f"<td>{_e(a['message'])}</td><td class='r muted'>{_e(a['ts'][11:16])} UTC</td></tr>"
        for a in alerts) or "<tr><td class='muted'>nessuno per ora — le regole sono in watcher.py</td></tr>"

    spread_rows = "".join(
        f"<tr><td>{_e(r['question'][:64])}</td><td class='r'>{r['bid']:.2f}/{r['ask']:.2f}</td>"
        f"<td class='r'><b>{r['spread']*100:.0f}p</b></td><td class='r'>{_vol(r['vol24h'])}</td></tr>"
        for r in spreads) or "<tr><td class='muted'>nessuno</td></tr>"

    mover_rows = "".join(
        f"<tr><td>{_e(r['question'][:64])}</td><td class='r'>{(r['last'] or 0):.2f}</td>"
        f"<td class='r'>{_pct(r['hour_chg'])}</td><td class='r'>{_pct(r['day_chg'])}</td></tr>"
        for r in movers) or "<tr><td class='muted'>nessuno</td></tr>"

    closing_rows = "".join(
        f"<tr><td>{_e(r['question'][:64])}</td><td class='r'>{(r['yes_price'] or 0):.2f}</td>"
        f"<td class='r'>{_vol(r['vol24h'])}</td><td class='r'>{_e((r['ends_at'] or '')[:10])}</td></tr>"
        for r in closing) or "<tr><td class='muted'>nessuno oggi</td></tr>"

    watch_html = "".join(f"<li style='margin:2px 0'>{_e(w)}</li>" for w in WATCHLIST_NORMATIVA)

    # ---------------- dati agenti: segnali shadow + balene ----------------
    from lab import signals as signals_mod
    sig_stats = signals_mod.stats(conn)
    sig_open = _rows(conn, "SELECT * FROM signals WHERE status='pending' ORDER BY ts DESC LIMIT 6")
    last_wp = conn.execute("SELECT MAX(ts) FROM whale_positions").fetchone()[0]
    whale_pos = _rows(conn, "SELECT * FROM whale_positions WHERE ts=? AND current_value>200 "
                     "ORDER BY current_value DESC LIMIT 7", (last_wp,)) if last_wp else []
    whale_cons = _rows(conn, """SELECT slug, COUNT(DISTINCT wallet) nw, SUM(current_value) tot,
                       GROUP_CONCAT(DISTINCT name) names, MAX(title) title
                       FROM whale_positions WHERE ts=? GROUP BY slug
                       HAVING nw>=2 ORDER BY tot DESC LIMIT 4""", (last_wp,)) if last_wp else []

    DIR_TXT = {1: "LUNGO", -1: "FADE", 0: "MAKER"}
    sig_stat_html = " · ".join(
        f"<b style='color:#2ea043'>{_e(s['kind'])}</b> {s['n']} valutati · {s['hit_pct']}% hit · {s['avg_res']:+.1f}% medio"
        for s in sig_stats) or "<span class='muted'>nessun segnale ancora valutato — servono cicli di watcher</span>"
    sig_rows = "".join(
        f"<tr><td><span class='tag t-MOVER_1H'>{_e(r['kind'])}</span></td>"
        f"<td>{_e(r['question'][:52])}</td><td class='r'>{DIR_TXT.get(r['direction'], '?')}</td>"
        f"<td class='r muted'>{_e(r['rationale'][:60])}</td></tr>"
        for r in sig_open) or "<tr><td class='muted'>nessun segnale aperto ora</td></tr>"
    whale_cons_html = "".join(
        f"<tr><td>{_e((c['title'] or c['slug'] or '')[:56])}</td>"
        f"<td>{_e(c['names'])}</td><td class='r'><b>${c['tot']:,.0f}</b></td></tr>"
        for c in whale_cons) or "<tr><td class='muted'>nessun consenso multi-balena rilevato ora</td></tr>"
    whale_rows = "".join(
        f"<tr><td>{_e(r['title'][:48])}</td><td class='r'>{_e(r['name'])}</td>"
        f"<td class='r'>{(r['cur_price'] or 0):.2f}</td><td class='r'>${r['current_value']:,.0f}</td>"
        f"<td class='r' style='color:{'#2ea043' if (r['cash_pnl'] or 0) >= 0 else '#f85149'}'>{(r['cash_pnl'] or 0):+,.0f}$</td></tr>"
        for r in whale_pos) or "<tr><td class='muted'>dati in arrivo col prossimo ciclo</td></tr>"

    dashboard = f"""<!DOCTYPE html>
<html lang="it"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>predmarket-lab — cockpit</title>{CSS}</head>
<body>
<h1>PREDMARKET <b>LAB</b> — cockpit autonomo</h1>
<div class="sub">aggiornato {now} (Europe/Rome) · dati: API pubbliche in sola lettura · ultimo scan: {_e(latest)} UTC · ciclo n.{n_cycles}</div>
<div class="grid">
  <div class="card">
    <h2>Conto paper (simulato)</h2>
    <div class="big">{ps['equity']:.2f} <span style="font-size:16px;color:#8b949e">USDC</span></div>
    <div class="muted">ROI {ps['roi_pct']:+.2f}% · realization {ps['realized_pnl']:+.2f} · drawdown dal picco {ps['drawdown_pct']:.1f}%</div>
    {_sparkline(eq_series)}
    <div class="kpis">
      <div class="kpi"><b>{ps['cash']:.0f}</b><span>cash</span></div>
      <div class="kpi"><b>{ps['open_positions']}</b><span>posizioni aperte</span></div>
      <div class="kpi"><b>{ps['trades']}</b><span>trade</span></div>
      <div class="kpi"><b>{ps['wins']}/{ps['losses']}</b><span>win/loss</span></div>
    </div>
  </div>
  <div class="card">
    <h2>Alert recenti</h2>
    <table><tr><th>tipo</th><th>cosa</th><th class="r">ora</th></tr>{alert_rows}</table>
  </div>
  <div class="card">
    <h2>Spread larghi — candidate maker (fee 0%)</h2>
    <table><tr><th>mercato</th><th class="r">bid/ask</th><th class="r">spread</th><th class="r">vol24h</th></tr>{spread_rows}</table>
  </div>
  <div class="card">
    <h2>Mover — dove gira la notizia</h2>
    <table><tr><th>mercato</th><th class="r">prezzo</th><th class="r">1h</th><th class="r">24h</th></tr>{mover_rows}</table>
  </div>
  <div class="card">
    <h2>Chiude oggi — finestre finali</h2>
    <table><tr><th>mercato</th><th class="r">prezzo</th><th class="r">vol24h</th><th class="r">fine</th></tr>{closing_rows}</table>
  </div>
  <div class="card">
    <h2>Shadow signals — l'AI studia (zero capitale)</h2>
    <div class="muted" style="margin-bottom:8px">ipotesi generate da regole e verificate sui dati reali: ogni strategia accumula un hit-rate misurato prima di poter mai toccare un euro</div>
    <table><tr><th>strategia</th><th>mercato</th><th class="r">dir</th><th class="r">logica</th></tr>{sig_rows}</table>
    <div style="font-size:11px;margin-top:10px;line-height:1.8">{sig_stat_html}</div>
  </div>
  <div class="card">
    <h2>Whale watch 🐋 — cosa tengono i vincenti</h2>
    <table><tr><th>consenso (stesso mercato, più balene)</th><th>chi</th><th class="r">valore</th></tr>{whale_cons_html}</table>
    <table style="margin-top:10px"><tr><th>posizione</th><th class="r">balena</th><th class="r">prezzo</th><th class="r">valore</th><th class="r">p&amp;l</th></tr>{whale_rows}</table>
  </div>
  <div class="card">
    <h2>Sistema</h2>
    <div class="kpis">
      <div class="kpi"><b>{n_mkt}</b><span>mercati tracciati</span></div>
      <div class="kpi"><b>{n_snap:,}</b><span>snapshot db</span></div>
      <div class="kpi"><b>{n_alerts}</b><span>alert totali</span></div>
      <div class="kpi"><b>{db_kb} KB</b><span>database</span></div>
    </div>
    <h2 style="margin-top:16px">Watchlist normativa IT</h2>
    <ul style="font-size:11px;color:#8b949e;line-height:1.5">{watch_html}</ul>
  </div>
</div>
<footer>predmarket-lab · dati di mercato pubblici in sola lettura (Gamma/CLOB Polymarket) · il conto paper è
una simulazione con fee e slippage realistici · nessuna esecuzione di ordini reali · nessuna consulenza finanziaria ·
i mercati predittivi sono oscurati in Italia per provvedimento ADM: aggiorna la watchlist a ogni sviluppo.</footer>
</body></html>"""
    with open(os.path.join(outdir, "dashboard.html"), "w", encoding="utf-8") as fh:
        fh.write(dashboard)

    # ------------------------------------------------------------ report md
    md = [f"# Report predmarket-lab — {now}", "",
          f"Ultimo scan: `{latest}` UTC · ciclo n.{n_cycles} · {n_mkt} mercati tracciati · {n_snap} snapshot · {n_alerts} alert", "",
          "## Conto paper", "",
          f"- **Equity:** {ps['equity']} USDC (**ROI {ps['roi_pct']:+.2f}%**)",
          f"- Cash {ps['cash']} · posizioni aperte {ps['open_positions']} · trade {ps['trades']} (W {ps['wins']} / L {ps['losses']})",
          f"- Realized {ps['realized_pnl']:+.2f} · drawdown dal picco {ps['drawdown_pct']:.1f}%", "",
          "## Ultimi alert", ""]
    for a in alerts[:12]:
        md.append(f"- `{a['ts'][11:16]}` **{a['kind']}** — {a['message']}")
    if not alerts:
        md.append("- nessuno per ora")
    md += ["", "## Shadow signals (l'AI studia, zero capitale)", ""]
    for s in sig_stats:
        md.append(f"- **{s['kind']}** — {s['n']} valutati · {s['hit_pct']}% hit · risultato medio {s['avg_res']:+.2f}%")
    if not sig_stats:
        md.append("- nessun segnale ancora valutato: servono cicli del watcher")
    md += ["", "segnali aperti ora:", ""]
    for r in sig_open:
        md.append(f"- `{r['kind']}` {r['question'][:70]} — {r['rationale']}")
    if not sig_open:
        md.append("- nessuno aperto")
    md += ["", "## Whale watch 🐋", ""]
    for c in whale_cons:
        md.append(f"- **Consenso**: {c['nw']} balene ({c['names']}) su '{(c['title'] or '')[:60]}' — ${c['tot']:,.0f}")
    for r in whale_pos[:5]:
        md.append(f"- {r['name']}: {r['title'][:60]} @ {(r['cur_price'] or 0):.2f} (${r['current_value']:,.0f}, P&L {r['cash_pnl'] or 0:+,.0f}$)")
    if not whale_cons and not whale_pos:
        md.append("- dati in arrivo col prossimo ciclo")
    md += ["", "## Watchlist normativa", ""]
    md += [f"- {w}" for w in WATCHLIST_NORMATIVA]
    md += ["", "## Prossime azioni", "",
           "1. Lasciare girare il watcher (GitHub Actions / VPS) per costruire lo storico",
           "2. Ogni trade idea → prima in paper (`lab/paper.py`), mai diretto",
           "3. Backtest delle strategie S3/S4/S5 quando il DB ha >= 2 settimane di dati", ""]
    with open(os.path.join(outdir, "REPORT.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(md))
