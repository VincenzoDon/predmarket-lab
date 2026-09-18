"""
A5 — SIGNAL ENGINE (SHADOW MODE) 🧠

Il primo strato di "intelligenza che studia": ipotesi di trading esplicite, generate
da regole sui dati live e VERIFICATE automaticamente sui dati successivi — senza
toccare un centesimo (shadow = ombra: zero capitale, zero ordini).

Perche' shadow e non esecuzione: una regola che sembra sensata vale zero finche'
non misuri su dati reali quante volte avrebbe vinto. Ogni segnale viene valutato
dopo il suo orizzonte temporale e il sistema accumula un hit-rate per strategia.
Solo strategie con edge misurato e stabile passeranno mai al conto paper.

Le 4 ipotesi v0 (da affinare/sostituire coi dati):
  ENDGAME_FAVORITE  +1  favorito >=0.75 che chiude oggi con spread stretto: il mercato
                          converge sul vero negli ultimi istanti?
  MEAN_REVERT       ±1  mossa >=10 punti in 1h su mercato non in chiusura: eccesso che
                          rientra, o inizio di trend? (fade della mossa)
  LONGSHOT_FADE     -1  prezzo <=0.05 con volume: i longshot sono storicamente
                          sopravvalutati (documentato in letteratura)
  MAKER_SPREAD       0  spread >=8 punti con volume: quanto spesso lo spread si
                          comprime (cioe' quanto avrebbe raccolto un maker)?
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timedelta, timezone


def _iso_plus_hours(ts: str, hours: float) -> str:
    base = datetime.fromisoformat(ts)
    return (base + timedelta(hours=hours)).isoformat(timespec="seconds")


def generate(conn: sqlite3.Connection, rows, ts: str) -> int:
    """Genera nuovi segnali shadow dalle ultime righe di snapshot (deduplicati)."""
    open_sig = {(k, s) for k, s in
                conn.execute("SELECT kind, slug FROM signals WHERE status='pending'")}
    today = ts[:10]
    new = []

    def add(kind, slug, question, direction, price, rationale, horizon_h, entry_spread=None):
        if (kind, slug) in open_sig:
            return
        new.append((ts, kind, slug, (question or "")[:110], direction, price,
                    entry_spread, _iso_plus_hours(ts, horizon_h), rationale))
        open_sig.add((kind, slug))

    for (ts_, slug, q, bid, ask, spread, last, yes, vol, liq, ends, fee, hchg, dchg, rw) in rows:
        if not slug or yes is None:
            continue
        ends_today = bool(ends and ends[:10] == today)
        if (ends_today and 0.75 <= yes <= 0.97 and spread is not None
                and spread <= 0.03 and (vol or 0) >= 50_000):
            add("ENDGAME_FAVORITE", slug, q, +1, yes,
                f"favorito {yes:.2f} a fine giornata, spread {spread*100:.0f}p, vol {vol/1000:.0f}k", 8)
        if (abs(hchg or 0) >= 0.10 and (vol or 0) >= 30_000 and (liq or 0) >= 10_000
                and not ends_today):
            add("MEAN_REVERT", slug, q, -1 if hchg > 0 else +1, yes,
                f"mossa {hchg*100:+.0f}p in 1h — ipotesi rientro eccesso", 3)
        if yes <= 0.05 and (vol or 0) >= 20_000:
            add("LONGSHOT_FADE", slug, q, -1, yes,
                f"longshot a {yes:.3f} — ipotesi sopravvalutazione", 24)
        if (spread is not None and spread >= 0.08 and (vol or 0) >= 20_000
                and (liq or 0) >= 5_000):
            add("MAKER_SPREAD", slug, q, 0, yes,
                f"spread {spread*100:.0f}p — ipotesi cattura maker", 6, entry_spread=spread)

    if new:
        conn.executemany(
            "INSERT INTO signals (ts, kind, slug, question, direction, entry_price, "
            "entry_spread, eval_after_ts, rationale) VALUES (?,?,?,?,?,?,?,?,?)", new)
    return len(new)


def evaluate(conn: sqlite3.Connection, ts_now: str) -> int:
    """Valuta i segnali maturati: cerca il prezzo successivo all'orizzonte e chiude il conto."""
    matured = conn.execute(
        "SELECT id, kind, slug, direction, entry_price, entry_spread, eval_after_ts "
        "FROM signals WHERE status='pending' AND eval_after_ts <= ?", (ts_now,)
    ).fetchall()
    closed = 0
    for s in matured:
        snap = conn.execute(
            "SELECT yes_price, spread FROM snapshots WHERE slug=? AND ts>=? "
            "ORDER BY ts LIMIT 1", (s["slug"], s["eval_after_ts"])
        ).fetchone()
        if not snap or snap["yes_price"] is None:
            continue  # nessun dato successivo: resta pending
        if s["kind"] == "MAKER_SPREAD":
            res = ((s["entry_spread"] or 0) - (snap["spread"] or 0)) * 100
        else:
            ep = s["entry_price"] or 0
            if ep <= 0 or not s["direction"]:
                continue
            res = _pnl_pct_live(s["direction"], ep, snap["yes_price"])
        conn.execute(
            "UPDATE signals SET status='done', eval_price=?, eval_spread=?, result_pct=? WHERE id=?",
            (snap["yes_price"], snap["spread"], round(res, 2), s["id"]))
        closed += 1
    return closed


def stats(conn: sqlite3.Connection) -> list[dict]:
    """Hit-rate e risultato medio per strategia (solo segnali valutati)."""
    out = []
    for r in conn.execute(
        """SELECT kind, COUNT(*) n, SUM(CASE WHEN result_pct>0 THEN 1 ELSE 0 END) hits,
                  AVG(result_pct) avg_res FROM signals WHERE status='done' GROUP BY kind"""
    ):
        out.append({"kind": r["kind"], "n": r["n"],
                    "hit_pct": round(100.0 * r["hits"] / r["n"], 1) if r["n"] else 0.0,
                    "avg_res": round(r["avg_res"] or 0, 2)})
    return out


# ---------------- P&L reale per lato (stake-based) ----------------
def _pnl_pct_live(direction: int, ep: float, price: float) -> float:
    """P&L % sull'uscita a prezzo `price` (positio ancora aperta)."""
    if direction == 1:                      # comprato YES a ep
        return (price - ep) / ep * 100.0
    return (ep - price) / (1.0 - ep) * 100.0  # comprato NO a (1-ep)


def _pnl_settled(direction: int, ep: float, final_yes: float) -> float:
    """P&L % a risoluzione (final_yes in {0,1}). Loss = -100% della posizione."""
    if direction == 1:
        return ((1.0 - ep) / ep * 100.0) if final_yes == 1 else -100.0
    return (ep / (1.0 - ep) * 100.0) if final_yes == 0 else -100.0


def settle_resolved(conn: sqlite3.Connection, gamma, active_slugs: set | None = None) -> int:
    """Chiude i segnali il cui mercato si e' risolto (0/1), con P&L reale.

    `active_slugs` = slug visti nell'ultimo ciclo: se un mercato e' ancora attivo
    non serve interrogare Gamma (risparmio di richieste)."""
    active = active_slugs or set()
    pend = conn.execute(
        "SELECT id, kind, slug, direction, entry_price FROM signals WHERE status='pending'"
    ).fetchall()
    closed: dict[str, dict | None] = {}
    for s in pend:
        sl = s["slug"]
        if sl in active or sl in closed:
            continue
        try:
            r = gamma.markets(slug=sl, closed="true")
        except RuntimeError:
            closed[sl] = None
            continue
        closed[sl] = r[0] if r else None
    n = 0
    for s in pend:
        m = closed.get(s["slug"])
        if not m:
            continue
        try:
            p = float(json.loads(m["outcomePrices"])[0])
        except (ValueError, TypeError):
            continue
        if p not in (0.0, 1.0):
            continue
        ep = s["entry_price"] or 0
        if ep <= 0 or not s["direction"]:
            continue
        res = _pnl_settled(s["direction"], ep, p)
        conn.execute(
            "UPDATE signals SET status='done', eval_price=?, eval_spread=NULL, result_pct=? WHERE id=?",
            (p, round(res, 2), s["id"]))
        n += 1
    return n
