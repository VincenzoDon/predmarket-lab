"""
BUDGET GOVERNOR — l'autosufficienza economica del progetto, in formule.

Regola matematica (nessuna discrezionalita'):
    base_netti_30g = guadagni_reali_30g + PAPER_WEIGHT x guadagni_paper_30g - spese_AI_30g
    budget_giornaliero = clamp( FLOOR, SHARE x base_netti_30g / 30, HARD_CAP )

- FLOOR   = spesa minima vitale (i loop essenziali non muoiono mai)
- SHARE   = quota dei guadagni netti reinvestita nell'AI (default 20%)
- HARD_CAP = tetto assoluto giornaliero, replicato come limite LATO PROVIDER
- PAPER_WEIGHT = i guadagni paper contano solo al 10%: il sistema non spende
  soldi veri sulla base di sogni paper. Quando arrivano guadagni reali,
  contano al 100%.

Con zero guadagni: si sta al FLOOR (frazioni di centesimo). Con 100 EUR reali
netti in 30 giorni: ~0,67 EUR/giorno di AI. Il progetto si paga da solo e
cresce solo se guadagna. kill() = spendibili a zero: l'agente si spegne da solo.

Tabella DB: budget_events(ts, kind, amount_usd) — kind in
('spend_ai','gain_paper','gain_real'). Il watcher registra gain_paper a ogni
ciclo (delta equity) e spend_ai quando (e se) chiama un LLM.
"""

from __future__ import annotations

import sqlite3
from datetime import datetime, timedelta, timezone

FLOOR_USD = 0.03          # spesa vitale minima/giorno
SHARE = 0.20              # 20% dei guadagni netti → budget AI
HARD_CAP_USD = 5.00       # tetto assoluto/giorno (da impostare ANCHE sul provider)
PAPER_WEIGHT = 0.10       # i guadagni paper valgono 1/10
WINDOW_DAYS = 30


def init_table(conn: sqlite3.Connection) -> None:
    conn.execute(
        "CREATE TABLE IF NOT EXISTS budget_events("
        " ts TEXT NOT NULL, kind TEXT NOT NULL, amount_usd REAL NOT NULL)"
    )
    conn.commit()


def record(conn: sqlite3.Connection, kind: str, amount_usd: float, ts: str | None = None) -> None:
    ts = ts or datetime.now(timezone.utc).isoformat(timespec="seconds")
    conn.execute("INSERT INTO budget_events VALUES (?,?,?)", (ts, kind, round(amount_usd, 4)))
    conn.commit()


def _sum(conn: sqlite3.Connection, kind: str, since: str) -> float:
    r = conn.execute(
        "SELECT COALESCE(SUM(amount_usd),0) FROM budget_events WHERE kind=? AND ts>=?",
        (kind, since)).fetchone()
    return float(r[0])


def state(conn: sqlite3.Connection) -> dict:
    """Stato del governor: base netti, budget di oggi, speso oggi, residuo."""
    now = datetime.now(timezone.utc)
    since = (now - timedelta(days=WINDOW_DAYS)).isoformat(timespec="seconds")
    today = now.date().isoformat()

    gains_real = _sum(conn, "gain_real", since)
    gains_paper = _sum(conn, "gain_paper", since)
    spent_30d = _sum(conn, "spend_ai", since)
    spent_today = _sum(conn, "spend_ai", today)

    base = gains_real + PAPER_WEIGHT * max(gains_paper, 0.0) - spent_30d
    daily = min(HARD_CAP_USD, max(FLOOR_USD, SHARE * base / WINDOW_DAYS))
    available = max(0.0, daily - spent_today)
    return {
        "gains_real_30d": round(gains_real, 2),
        "gains_paper_30d": round(gains_paper, 2),
        "spent_ai_30d": round(spent_30d, 4),
        "base_netta": round(base, 2),
        "daily_cap": round(daily, 4),
        "spent_today": round(spent_today, 4),
        "available_today": round(available, 4),
        "alive": available > 0,
    }


def can_spend(conn: sqlite3.Connection, amount_usd: float) -> tuple[bool, str]:
    s = state(conn)
    if amount_usd <= s["available_today"]:
        return True, f"ok: disponibile {s['available_today']}$ (cap {s['daily_cap']}$)"
    return False, (f"negato: servono {amount_usd}$, disponibile {s['available_today']}$ "
                   f"(cap giornaliero {s['daily_cap']}$ — kill switch attivo)")


def demo() -> None:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    init_table(conn)
    print("=== BUDGET GOVERNOR — scenari (formula: clamp(FLOOR, 20% x netti/30, HARD_CAP)) ===")
    scenari = [
        ("zero guadagni (oggi, giorno 1)", []),
        ("solo paper: +50$ paper in 30g", [("gain_paper", 50)]),
        ("paper + reali: +80$ paper, +100$ reali", [("gain_paper", 80), ("gain_real", 100)]),
        ("buon mese reale: +600$ reali netti", [("gain_real", 600)]),
        ("netto negativo: -30$ reali", [("gain_real", -30)]),
    ]
    for nome, eventi in scenari:
        for k, v in eventi:
            record(conn, k, v)
        s = state(conn)
        print(f"  {nome:<38} -> budget/giorno: {s['daily_cap']:>6.3f}$  (base netta {s['base_netta']:>7.2f}$)")
        conn.execute("DELETE FROM budget_events")
        conn.commit()
