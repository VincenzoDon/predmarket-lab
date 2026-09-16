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
    return alerts


def _pf(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0
