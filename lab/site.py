"""
SITO PUBBLICO — genera index.html, la pagina "per tutti".

Diversa dalla dashboard (dashboard.html = cockpit tecnico e denso). Questa e'
la vetrina: spiega in parole semplici COSA fa il progetto, mostra i numeri
onesti (anche quelli brutti) e le strategie validate vs bocciate. Pensata per
essere pubblicata su GitHub Pages (statica, zero server, zero risorse esterne)
e per essere comprensibile da chi non sa nulla di mercati predittivi.

Filosofia: la trasparenza E' il prodotto. Qui non si vende un sogno, si mostra
un metodo misurato — comprese le strategie che abbiamo bocciato.
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

# soglie di "promozione" di una strategia (allineate ad AGENTI.md L3)
PROMO_MIN_TRADES = 30      # sotto questo n = "ancora pochi dati"
PROMO_MIN_EDGE = 3.0       # edge medio % minimo per considerarla "promettente"
PROMO_MIN_HIT = 55.0       # hit-rate % minimo


def _e(s) -> str:
    return html.escape(str(s if s is not None else ""))


def _verdict(n: int, hit: float, avg: float) -> tuple[str, str]:
    """Ritorna (etichetta, classe css) — onesto: valida / promettente / bocciata / pochi dati."""
    if n < PROMO_MIN_TRADES:
        return ("pochi dati", "v-wait")
    if avg <= 0 or hit < 50:
        return ("bocciata", "v-bad")
    if avg >= PROMO_MIN_EDGE and hit >= PROMO_MIN_HIT:
        return ("promettente", "v-good")
    return ("in osservazione", "v-mid")


CSS = """<style>
:root{color-scheme:dark}
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0b0f16;color:#e6edf3;font-family:'Segoe UI',system-ui,-apple-system,sans-serif;line-height:1.6}
.wrap{max-width:980px;margin:0 auto;padding:0 20px}
header{background:linear-gradient(160deg,#0d1117,#131b2e);border-bottom:1px solid #21324f;padding:54px 0 46px}
.badge{display:inline-block;background:#a371f722;color:#c9a9ff;border:1px solid #a371f755;border-radius:20px;padding:3px 13px;font-size:12px;font-weight:600;letter-spacing:.5px;margin-bottom:16px}
h1{font-size:40px;line-height:1.15;letter-spacing:-.5px}h1 b{color:#3fb950}
.lead{color:#9fb0c3;font-size:18px;margin-top:14px;max-width:680px}
.health{display:inline-flex;gap:8px;align-items:center;margin-top:22px;padding:8px 14px;border-radius:8px;font-size:13px;font-weight:600}
.h-ok{background:#2ea04322;border:1px solid #2ea04366;color:#3fb950}
.h-giallo{background:#d2992222;border:1px solid #d2992266;color:#d29922}
.h-rosso{background:#f8514922;border:1px solid #f8514966;color:#f85149}
section{padding:40px 0;border-bottom:1px solid #161d29}
h2{font-size:24px;margin-bottom:8px;letter-spacing:-.3px}
.sub{color:#8b98a9;margin-bottom:22px;max-width:720px}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:14px}
.stat{background:#111826;border:1px solid #1f2b3d;border-radius:12px;padding:18px}
.stat b{display:block;font-size:30px;color:#3fb950;font-weight:700}
.stat span{font-size:12px;color:#8b98a9;text-transform:uppercase;letter-spacing:.6px}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px}
.card{background:#111826;border:1px solid #1f2b3d;border-radius:12px;padding:18px}
.card h3{font-size:16px;margin-bottom:6px}
.card p{color:#9fb0c3;font-size:14px}
table{width:100%;border-collapse:collapse;font-size:14px;margin-top:8px}
th{text-align:left;color:#8b98a9;padding:9px 8px;border-bottom:1px solid #1f2b3d;font-size:12px;text-transform:uppercase;letter-spacing:.5px}
td{padding:10px 8px;border-bottom:1px solid #161d29;vertical-align:middle}
td.r,th.r{text-align:right}
.pill{display:inline-block;padding:2px 11px;border-radius:20px;font-size:12px;font-weight:700}
.v-good{background:#2ea04322;color:#3fb950}.v-bad{background:#f8514922;color:#f85149}
.v-mid{background:#d2992222;color:#d29922}.v-wait{background:#8b98a922;color:#9fb0c3}
.score-bar{height:7px;background:#1f2b3d;border-radius:4px;overflow:hidden;margin-top:5px;min-width:80px}
.score-fill{height:100%;background:linear-gradient(90deg,#d29922,#a371f7)}
.note{background:#0e1420;border-left:3px solid #a371f7;padding:14px 18px;border-radius:0 8px 8px 0;color:#9fb0c3;font-size:14px;margin-top:18px}
.legal{background:#160f0f;border-left:3px solid #f85149}
footer{padding:36px 0;color:#6b7787;font-size:13px;line-height:1.8}
a{color:#58a6ff;text-decoration:none}
.tabs{display:flex;gap:8px;margin-bottom:16px;flex-wrap:wrap}
.cta{display:inline-block;margin-top:8px;background:#3fb95022;border:1px solid #3fb95055;color:#3fb950;padding:9px 18px;border-radius:8px;font-weight:600;font-size:14px}
</style>"""


def generate(conn: sqlite3.Connection, paper, outdir: str = ".") -> None:
    from lab import signals as signals_mod
    from lab import whales as whales_mod
    from lab.report import _freshness  # riuso la logica di freschezza

    conn.row_factory = sqlite3.Row
    now = datetime.now(ROME).strftime("%d/%m/%Y %H:%M")
    latest = conn.execute("SELECT MAX(ts) FROM snapshots").fetchone()[0] or "n.d."
    fresh = _freshness(latest)
    dot = {"ok": "\U0001F7E2", "giallo": "\U0001F7E1", "rosso": "\U0001F534"}.get(fresh["level"], "")

    n_snap = conn.execute("SELECT COUNT(*) FROM snapshots").fetchone()[0]
    n_mkt = conn.execute("SELECT COUNT(DISTINCT slug) FROM snapshots").fetchone()[0]
    n_sig = conn.execute("SELECT COUNT(*) FROM signals").fetchone()[0]
    n_done = conn.execute("SELECT COUNT(*) FROM signals WHERE status='done'").fetchone()[0]
    n_wallet = conn.execute("SELECT COUNT(DISTINCT wallet) FROM whale_positions").fetchone()[0]
    ps = paper.summary()

    # ---- strategie: numeri onesti + verdetto ----
    stats = signals_mod.stats(conn)
    strat_rows = ""
    for s in sorted(stats, key=lambda x: x["avg_res"], reverse=True):
        label, cls = _verdict(s["n"], s["hit_pct"], s["avg_res"])
        color = "#3fb950" if s["avg_res"] >= 0 else "#f85149"
        strat_rows += (
            f"<tr><td><b>{_e(s['kind'])}</b></td>"
            f"<td class='r'>{s['n']}</td>"
            f"<td class='r'>{s['hit_pct']:.0f}%</td>"
            f"<td class='r' style='color:{color}'>{s['avg_res']:+.1f}%</td>"
            f"<td class='r'><span class='pill {cls}'>{label}</span></td></tr>"
        )
    if not strat_rows:
        strat_rows = "<tr><td class='muted'>nessun segnale ancora valutato</td></tr>"

    # ---- shadow detector: top wallet ----
    scores = whales_mod.top_scores(conn, limit=6)
    wallet_rows = ""
    for s in scores:
        wallet_rows += (
            f"<tr><td><b>{_e(s['name'])}</b></td>"
            f"<td class='r'>{(s['win_rate'] or 0)*100:.0f}%</td>"
            f"<td class='r' style='color:#8b98a9'>{s['n_pos']}</td>"
            f"<td class='r'><b>{s['score']:.0f}</b>"
            f"<div class='score-bar'><div class='score-fill' style='width:{max(0,min(100,s['score'])):.0f}%'></div></div></td></tr>"
        )
    if not wallet_rows:
        wallet_rows = "<tr><td class='muted'>scoring in costruzione</td></tr>"

    # ---- indice di inefficienza ----
    top50 = conn.execute("SELECT spread, hour_chg FROM snapshots WHERE ts=? "
                         "ORDER BY vol24h DESC LIMIT 50", (latest,)).fetchall()
    if top50:
        fs = sum(1 for r in top50 if (r["spread"] or 0) >= 0.04) / len(top50)
        fm = sum(1 for r in top50 if abs(r["hour_chg"] or 0) >= 0.08) / len(top50)
        inef = round(100 * (0.6 * fs + 0.4 * fm))
    else:
        inef = "—"

    page = f"""<!DOCTYPE html>
<html lang="it"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Osservatorio Italiano dei Mercati Predittivi</title>
<meta name="description" content="Il primo osservatorio italiano sui mercati predittivi: dati pubblici, strategie misurate con trasparenza totale, numeri veri anche quando sono brutti.">
{CSS}</head>
<body>
<header><div class="wrap">
  <span class="badge">\U0001F1EE\U0001F1F9 OSSERVATORIO ITALIANO DEI MERCATI PREDITTIVI</span>
  <h1>Capiamo i mercati predittivi<br>con <b>numeri veri</b>, non promesse.</h1>
  <p class="lead">Osserviamo i mercati predittivi (come Polymarket) usando solo dati pubblici.
  Misuriamo quali strategie funzionano davvero e quali no — e pubblichiamo tutto, anche
  i risultati brutti. Nessun ordine reale: qui si studia, non si scommette.</p>
  <div class="health h-{fresh['level']}">{dot} {_e(fresh['txt'])}</div>
</div></header>

<section><div class="wrap">
  <h2>Il progetto in numeri</h2>
  <p class="sub">Aggiornato automaticamente a ogni ciclo del sistema. Ultimo aggiornamento: {now} (ora italiana).</p>
  <div class="stats">
    <div class="stat"><b>{n_mkt:,}</b><span>mercati osservati</span></div>
    <div class="stat"><b>{n_snap:,}</b><span>rilevazioni storiche</span></div>
    <div class="stat"><b>{n_done:,}</b><span>previsioni verificate</span></div>
    <div class="stat"><b>{n_wallet}</b><span>wallet studiati</span></div>
    <div class="stat"><b>{inef}<span style="font-size:15px;color:#8b98a9">/100</span></b><span>indice inefficienza</span></div>
  </div>
</div></section>

<section><div class="wrap">
  <h2>Le strategie, senza trucchi</h2>
  <p class="sub">Ogni ipotesi viene provata "in ombra" (shadow): zero capitale, zero ordini.
  Il sistema misura da solo quante volte avrebbe avuto ragione. Una strategia diventa
  "promettente" solo con edge medio ≥{PROMO_MIN_EDGE:.0f}% e almeno {PROMO_MIN_TRADES} verifiche.
  Le bocciate restano qui in mostra: è il punto.</p>
  <table>
    <tr><th>strategia</th><th class="r">verifiche</th><th class="r">successo</th><th class="r">risultato medio</th><th class="r">verdetto</th></tr>
    {strat_rows}
  </table>
  <div class="note">Perché mostriamo anche le strategie bocciate? Perché il valore del progetto
  è <b>separare</b> ciò che funziona da ciò che no, <b>prima</b> di rischiare un euro.
  Un risultato negativo onesto vale più di un numero gonfiato.</div>
</div></section>

<section><div class="wrap">
  <h2>Shadow Detector \U0001F575\uFE0F — chi sembra "informato"</h2>
  <p class="sub">Diamo un punteggio ai wallet in base a quanto spesso vincono, quanto capitale
  rischiano e quanto sono specializzati. Quando uno con punteggio alto entra su un mercato nuovo,
  alziamo un segnale — <b>da osservare, non da copiare alla cieca</b>.</p>
  <table>
    <tr><th>wallet</th><th class="r">% vittorie</th><th class="r">osservazioni</th><th class="r">punteggio</th></tr>
    {wallet_rows}
  </table>
</div></section>

<section><div class="wrap">
  <h2>Come funziona (in 3 passi)</h2>
  <div class="cards">
    <div class="card"><h3>1. Osserva</h3><p>Ogni pochi minuti raccogliamo prezzi, volumi e
    movimenti di centinaia di mercati, più le mosse dei grandi wallet. Solo dati pubblici.</p></div>
    <div class="card"><h3>2. Misura</h3><p>Trasformiamo le intuizioni in ipotesi precise e le
    verifichiamo sui dati reali. Teniamo il conteggio: quante volte funziona, quanto rende.</p></div>
    <div class="card"><h3>3. Mostra</h3><p>Pubblichiamo tutto qui e in una dashboard tecnica.
    Numeri veri, aggiornati da soli, comprensibili anche a chi parte da zero.</p></div>
  </div>
  <a class="cta" href="dashboard.html">Apri la dashboard tecnica \u2192</a>
</div></section>

<section><div class="wrap">
  <h2>Il conto simulato</h2>
  <p class="sub">Per capire se le idee reggerebbero, teniamo un conto "di carta" con fee e
  slippage realistici. Nessun soldo vero è coinvolto.</p>
  <div class="stats">
    <div class="stat"><b>{ps['equity']:.0f}</b><span>USDC simulati</span></div>
    <div class="stat"><b style="color:{'#3fb950' if ps['roi_pct']>=0 else '#f85149'}">{ps['roi_pct']:+.2f}%</b><span>rendimento</span></div>
    <div class="stat"><b>{ps['trades']}</b><span>operazioni</span></div>
    <div class="stat"><b>{ps['wins']}/{ps['losses']}</b><span>vinte/perse</span></div>
  </div>
</div></section>

<section><div class="wrap">
  <h2>Onestà e regole</h2>
  <div class="note legal">
  \u26A0\uFE0F I mercati predittivi come Polymarket e Kalshi sono <b>oscurati in Italia</b> per
  provvedimento ADM (27/07/2026). Questo progetto <b>non esegue ordini</b> e non aiuta ad aggirare
  il blocco: legge solo dati pubblici per analisi e ricerca. Nessuna consulenza finanziaria.
  Il conto è simulato. Nessun segreto o chiave privata è mai contenuto qui.</div>
</div></section>

<footer><div class="wrap">
  Osservatorio Italiano dei Mercati Predittivi · dati pubblici in sola lettura ·
  pagina generata automaticamente il {now} · <a href="dashboard.html">dashboard tecnica</a> ·
  <a href="REPORT.md">report testuale</a><br>
  Trasparenza totale: pubblichiamo i numeri anche quando sono brutti.
</div></footer>
</body></html>"""

    with open(os.path.join(outdir, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(page)
