"""
A4 — WHALE WATCHER 🐋

Studia i wallet che storicamente vincono, usando il Data API pubblico di Polymarket:
  - /v1/leaderboard   -> top trader per finestra (1m/1w/all) con PnL
  - /positions        -> posizioni aperte correnti di un wallet

Ogni ciclo del watcher: scarica i top trader, logga le loro posizioni significative
su SQLite (tabella whale_positions) e segnala quando >=2 balene sono sullo stesso
mercato (WHALE_CONSENSUS) — l'ipotesi da validare e' che il consenso dei vincenti
sia un segnale informativo, NON un invito a copiare alla cieca (rischio: essere
l'uscita di sicurezza della balena).

Tutto in sola lettura, dati pubblici on-chain.
"""

from __future__ import annotations

import sqlite3

import requests

DATA_API = "https://data-api.polymarket.com"


def _get(path: str, params: dict):
    r = requests.get(f"{DATA_API}{path}", params=params, timeout=25)
    r.raise_for_status()
    return r.json()


def top_traders(window: str = "1m", limit: int = 10) -> list[dict]:
    return _get("/v1/leaderboard", {"window": window, "limit": limit})


def wallet_positions(wallet: str, limit: int = 15) -> list[dict]:
    return _get("/positions", {"user": wallet, "limit": limit,
                               "sortBy": "CURRENT", "sortDirection": "desc"})


def track(conn: sqlite3.Connection, ts: str, n_whales: int = 5,
          min_value: float = 300.0) -> list[tuple]:
    """Un ciclo di tracking. Ritorna gli alert WHALE_CONSENSUS (già pronti per il dedupe)."""
    leaders = top_traders("1m", n_whales)
    rows = []
    for l in leaders:
        wallet = l.get("proxyWallet")
        if not wallet:
            continue
        name = l.get("userName") or wallet[:10]
        try:
            positions = wallet_positions(wallet)
        except requests.RequestException:
            continue
        for p in positions:
            try:
                val = float(p.get("currentValue") or 0)
            except (TypeError, ValueError):
                continue
            if val < min_value:
                continue
            rows.append((
                ts, wallet, name, p.get("slug"), (p.get("title") or "")[:90],
                p.get("outcome"), _pf(p.get("size")), _pf(p.get("avgPrice")),
                _pf(p.get("curPrice")), val, _pf(p.get("cashPnl")),
            ))
    if rows:
        conn.executemany("INSERT INTO whale_positions VALUES (?,?,?,?,?,?,?,?,?,?,?)", rows)

    alerts: list[tuple] = []
    for c in conn.execute(
        """SELECT slug, COUNT(DISTINCT wallet) nw, SUM(current_value) tot,
                  GROUP_CONCAT(DISTINCT name) names, MAX(title) title
           FROM whale_positions WHERE ts=?
           GROUP BY slug HAVING nw>=2 ORDER BY tot DESC LIMIT 5""", (ts,)
    ):
        alerts.append((
            ts, "WHALE_CONSENSUS", c["slug"],
            f"{c['nw']} balene ({c['names']}) su '{(c['title'] or '')[:56]}' — valore tot ${c['tot']:,.0f}",
            round(c["tot"], 2),
        ))

    # ---- SHADOW DETECTOR v1: punteggia i wallet e alza SHADOW_ENTRY ----
    scores = score_wallets(conn)
    persist_scores(conn, ts, scores)
    alerts.extend(shadow_entry_alerts(conn, ts, rows, scores))
    return alerts


def _pf(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


# =====================================================================
# SHADOW DETECTOR v1 — scoring "insider-simiglianza" dei wallet
# =====================================================================
# EDGE-STACK.md Strato A. Idea: NON copiare alla cieca le balene, ma
# punteggiare quali wallet SEMBRANO informati (win-rate alto, convinzione,
# nicchia, profitto anomalo) e ALZARE UN ALERT — shadow, zero ordini —
# quando uno di loro entra su un mercato nuovo. L'alert va poi verificato
# come gli altri segnali (hit-rate misurato nel tempo) prima di valere un euro.
#
# Tutto calcolato dallo STORICO gia' in tabella whale_positions: nessuna
# nuova chiamata di rete, funziona anche offline. I pesi sono parametri
# d'alpha (open-core): stanno qui e sono facili da ritarare sui dati.
# =====================================================================

# pesi del punteggio (somma = 1.0) — v1, da ritarare quando cresce lo storico
SCORE_WEIGHTS = {
    "win_rate": 0.40,      # % posizioni in profitto: la firma piu' forte di "sa quello che fa"
    "profit": 0.25,        # P&L medio per posizione (normalizzato, log-scala)
    "conviction": 0.20,    # size media impegnata (capitale a rischio = convinzione)
    "focus": 0.15,         # concentrazione su pochi mercati (nicchia vs spray & pray)
}
SHADOW_MIN_SCORE = 65.0    # soglia di punteggio per generare un alert SHADOW_ENTRY
SHADOW_MIN_POS = 4         # servono almeno N osservazioni per fidarsi del punteggio
SHADOW_MIN_WINRATE = 0.55  # gate di rischio: sotto questo win-rate NON si alza l'alert
                           # (evita di seguire un wallet che potrebbe usarci come
                           #  liquidita' d'uscita — vedi rischi in EDGE-STACK.md Strato A)


def init_score_table(conn: sqlite3.Connection) -> None:
    conn.execute(
        "CREATE TABLE IF NOT EXISTS wallet_scores("
        " ts TEXT NOT NULL, wallet TEXT NOT NULL, name TEXT,"
        " score REAL, win_rate REAL, avg_pnl REAL, n_pos INTEGER,"
        " n_markets INTEGER, breakdown TEXT)"
    )
    conn.execute("CREATE INDEX IF NOT EXISTS idx_ws_wallet ON wallet_scores(wallet)")
    conn.commit()


def _norm_log(x: float, full: float) -> float:
    """Normalizza x in [0,1] con scala log: raggiunge ~1 attorno a `full`."""
    import math
    if x <= 0:
        return 0.0
    return min(1.0, math.log10(1.0 + x) / math.log10(1.0 + full))


def score_wallets(conn: sqlite3.Connection) -> list[dict]:
    """Punteggia OGNI wallet visto finora, dallo storico di whale_positions.

    Ritorna una lista di dict ordinata per punteggio decrescente. Nessuna rete.
    """
    rows = conn.execute(
        """SELECT wallet, name,
                  COUNT(*)                                    n_pos,
                  COUNT(DISTINCT slug)                        n_markets,
                  AVG(CASE WHEN cash_pnl>0 THEN 1.0 ELSE 0.0 END) win_rate,
                  AVG(cash_pnl)                               avg_pnl,
                  AVG(current_value)                          avg_val
           FROM whale_positions
           WHERE wallet IS NOT NULL
           GROUP BY wallet"""
    ).fetchall()

    out = []
    for r in rows:
        n_pos = r["n_pos"] or 0
        win = float(r["win_rate"] or 0.0)                    # 0..1
        avg_pnl = float(r["avg_pnl"] or 0.0)
        avg_val = float(r["avg_val"] or 0.0)
        n_markets = r["n_markets"] or 1

        c_win = win
        c_profit = _norm_log(max(avg_pnl, 0.0), full=50_000)     # $50k P&L medio ~ top
        c_conv = _norm_log(avg_val, full=500_000)               # $500k size media ~ top
        # focus: pochi mercati con molte osservazioni = concentrato/nicchia
        c_focus = min(1.0, n_pos / (n_markets * 3.0)) if n_markets else 0.0

        score = 100.0 * (
            SCORE_WEIGHTS["win_rate"] * c_win
            + SCORE_WEIGHTS["profit"] * c_profit
            + SCORE_WEIGHTS["conviction"] * c_conv
            + SCORE_WEIGHTS["focus"] * c_focus
        )
        # penalita' di fiducia se abbiamo pochissime osservazioni
        if n_pos < SHADOW_MIN_POS:
            score *= 0.6

        out.append({
            "wallet": r["wallet"], "name": r["name"] or (r["wallet"] or "")[:10],
            "score": round(score, 1), "win_rate": round(win, 3),
            "avg_pnl": round(avg_pnl, 0), "n_pos": n_pos, "n_markets": n_markets,
            "breakdown": {"win": round(c_win, 2), "profit": round(c_profit, 2),
                          "conviction": round(c_conv, 2), "focus": round(c_focus, 2)},
        })
    out.sort(key=lambda d: d["score"], reverse=True)
    return out


def persist_scores(conn: sqlite3.Connection, ts: str, scores: list[dict]) -> None:
    import json as _json
    init_score_table(conn)
    conn.executemany(
        "INSERT INTO wallet_scores VALUES (?,?,?,?,?,?,?,?,?)",
        [(ts, s["wallet"], s["name"], s["score"], s["win_rate"], s["avg_pnl"],
          s["n_pos"], s["n_markets"], _json.dumps(s["breakdown"])) for s in scores],
    )
    conn.commit()


def top_scores(conn: sqlite3.Connection, limit: int = 8) -> list[dict]:
    """Ultimo punteggio noto per wallet (per dashboard/report). Nessuna rete."""
    init_score_table(conn)
    last = conn.execute("SELECT MAX(ts) FROM wallet_scores").fetchone()[0]
    if not last:
        return []
    rows = conn.execute(
        "SELECT wallet, name, score, win_rate, avg_pnl, n_pos, n_markets "
        "FROM wallet_scores WHERE ts=? ORDER BY score DESC LIMIT ?", (last, limit)
    ).fetchall()
    return [dict(r) for r in rows]


def shadow_entry_alerts(conn: sqlite3.Connection, ts: str, this_cycle_rows: list[tuple],
                        scores: list[dict]) -> list[tuple]:
    """Alza SHADOW_ENTRY quando un wallet ad alto punteggio compare su un mercato
    su cui NON lo avevamo mai visto prima (ingresso nuovo). Shadow, zero ordini.

    `this_cycle_rows` = le righe (ts,wallet,name,slug,...) inserite in questo ciclo.
    """
    score_by_wallet = {s["wallet"]: s for s in scores}
    alerts: list[tuple] = []
    seen = set()
    for row in this_cycle_rows:
        _ts, wallet, name, slug, title = row[0], row[1], row[2], row[3], row[4]
        s = score_by_wallet.get(wallet)
        if (not s or s["score"] < SHADOW_MIN_SCORE or s["n_pos"] < SHADOW_MIN_POS
                or s["win_rate"] < SHADOW_MIN_WINRATE):
            continue
        if (wallet, slug) in seen:
            continue
        # e' un mercato NUOVO per questo wallet? (mai visto in cicli precedenti)
        prior = conn.execute(
            "SELECT 1 FROM whale_positions WHERE wallet=? AND slug=? AND ts<? LIMIT 1",
            (wallet, slug, ts)
        ).fetchone()
        if prior:
            continue
        seen.add((wallet, slug))
        alerts.append((
            ts, "SHADOW_ENTRY", slug,
            f"wallet informato-simile {s['name']} (score {s['score']:.0f}/100, "
            f"win {s['win_rate']*100:.0f}%) ENTRA su '{(title or slug or '')[:50]}' — "
            f"da osservare (shadow, zero ordini)",
            round(s["score"], 1),
        ))
    return alerts
