"""
Watcher continuo — il cuore della Fase 1: raccoglie dati, li salva, genera alert e report.

Uso:
    python3 watcher.py --once                     # un ciclo singolo (modalita' GitHub Actions)
    python3 watcher.py --loop --interval 300      # continuo (VPS / Raspberry / server)
    python3 watcher.py --cycles 3 --interval 20   # N cicoli ravvicinati (test/demo)
    python3 watcher.py --reset-paper              # azzera il conto paper (riparte da 200 USDC)

Ogni ciclo: ~4 richieste alle API pubbliche -> snapshots su SQLite -> alert con dedupe
-> equity del conto paper -> REPORT.md + dashboard.html aggiornati.

Progettato per girare SENZA il tuo PC acceso (vedi README: GitHub Actions gratis,
VPS, Raspberry Pi). Nessuna funzione di esecuzione ordini: solo dati e paper trading.
"""

from __future__ import annotations

import argparse
import json
import os
import sqlite3
import time
from datetime import datetime, timedelta, timezone

from lab.api import GammaClient
from lab.paper import PaperAccount
from lab.scanner import _f, scan_arb

DB_PATH = os.path.join("data", "lab.db")

ALERT_RULES = {
    "spread_min": 0.06,        # spread >= 6 punti...
    "spread_min_vol": 20_000,  # ...con almeno 20k di volume 24h...
    "spread_min_liq": 3_000,   # ...e 3k di liquidita' -> candidata maker
    "mover_min_1h": 0.08,      # mossa >= 8 punti in 1h con volume
    "mover_min_vol": 10_000,
    "closing_hot_vol": 100_000,  # chiude oggi con volume alto -> finestra informativa
    "arb_min_edge": 0.004,     # paniere negRisk con edge netto >= 0.4%
    "dedupe_min": 60,          # stesso alert non ripetuto entro 60 minuti
}


def init_db(path: str = DB_PATH) -> sqlite3.Connection:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    conn = sqlite3.connect(path)
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS snapshots(
            ts TEXT NOT NULL, slug TEXT NOT NULL, question TEXT,
            bid REAL, ask REAL, spread REAL, last REAL, yes_price REAL,
            vol24h REAL, liquidity REAL, ends_at TEXT, fee_rate REAL,
            hour_chg REAL, day_chg REAL, has_rewards INTEGER DEFAULT 0);
        CREATE INDEX IF NOT EXISTS idx_snap_slug_ts ON snapshots(slug, ts);
        CREATE INDEX IF NOT EXISTS idx_snap_ts ON snapshots(ts);
        CREATE TABLE IF NOT EXISTS alerts(
            ts TEXT NOT NULL, kind TEXT NOT NULL, slug TEXT, message TEXT, metric REAL);
        CREATE INDEX IF NOT EXISTS idx_alerts_kind ON alerts(kind, slug);
        CREATE TABLE IF NOT EXISTS equity(ts TEXT NOT NULL, value REAL);
        CREATE TABLE IF NOT EXISTS signals(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts TEXT NOT NULL, kind TEXT NOT NULL, slug TEXT NOT NULL, question TEXT,
            direction INTEGER, entry_price REAL, entry_spread REAL,
            eval_after_ts TEXT, rationale TEXT,
            status TEXT DEFAULT 'pending', eval_price REAL, eval_spread REAL, result_pct REAL);
        CREATE INDEX IF NOT EXISTS idx_signals_status ON signals(status);
        CREATE INDEX IF NOT EXISTS idx_signals_kind ON signals(kind);
        CREATE TABLE IF NOT EXISTS whale_positions(
            ts TEXT NOT NULL, wallet TEXT, name TEXT, slug TEXT, title TEXT, outcome TEXT,
            size REAL, avg_price REAL, cur_price REAL, current_value REAL, cash_pnl REAL);
        CREATE INDEX IF NOT EXISTS idx_wp_slug ON whale_positions(slug);
        """
    )
    conn.commit()
    # migrazione per DB gia' esistenti
    cols = {r[1] for r in conn.execute("PRAGMA table_info(snapshots)")}
    if "has_rewards" not in cols:
        conn.execute("ALTER TABLE snapshots ADD COLUMN has_rewards INTEGER DEFAULT 0")
        conn.commit()
    return conn


def _fetch_markets(gamma: GammaClient, pages: int = 3) -> list[dict]:
    """Gamma caps a 100 mercati per richiesta: paginiamo con `offset`."""
    out: list[dict] = []
    for page in range(pages):
        try:
            ms = gamma.markets(
                active="true", closed="false", archived="false",
                order="volume24hr", ascending="false",
                limit=100, offset=page * 100,
            )
        except RuntimeError:
            break
        if not ms:
            break
        out.extend(ms)
        if len(ms) < 100:
            break
    seen: set[str] = set()
    res = []
    for m in out:
        s = m.get("slug")
        if s and s not in seen:
            seen.add(s)
            res.append(m)
    return res


def _yes_price(m: dict) -> float | None:
    p = m.get("outcomePrices")
    try:
        arr = json.loads(p) if isinstance(p, str) else p
        return float(arr[0]) if arr else None
    except (ValueError, TypeError):
        return None


def run_cycle(gamma, conn, paper, rules=ALERT_RULES, verbose=True) -> dict:
    now = datetime.now(timezone.utc)
    ts = now.isoformat(timespec="seconds")
    today = ts[:10]

    markets = _fetch_markets(gamma)
    rows, price_map = [], {}
    for m in markets:
        slug = m.get("slug")
        if not slug:
            continue
        yes = _yes_price(m)
        fee = 0.0
        if m.get("feesEnabled"):
            fee = _f((m.get("feeSchedule") or {}).get("rate")) or 0.0
        rows.append((
            ts, slug, (m.get("question") or "")[:120],
            _f(m.get("bestBid")), _f(m.get("bestAsk")), _f(m.get("spread")) or 0.0,
            _f(m.get("lastTradePrice")), yes,
            _f(m.get("volume24hr")) or 0.0, _f(m.get("liquidityNum")) or 0.0,
            m.get("endDate"), fee,
            _f(m.get("oneHourPriceChange")) or 0.0, _f(m.get("oneDayPriceChange")) or 0.0,
        ))
        if yes is not None:
            price_map[slug] = yes
    if rows:
        conn.executemany("INSERT INTO snapshots VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", rows)

    # ---------------- alert da regole ----------------
    cand = []
    for (ts_, slug, q, bid, ask, spread, last, yes, vol, liq, ends, fee, hchg, dchg, rw) in rows:
        if rw and vol >= 5000:
            cand.append((ts_, "REWARDS_MARKET", slug,
                         f"liquidity rewards attivi — vol 24h {vol/1000:.0f}k: candidate yield maker",
                         round(vol, 2)))
        if (spread >= rules["spread_min"] and vol >= rules["spread_min_vol"]
                and liq >= rules["spread_min_liq"]):
            cand.append((ts_, "SPREAD_LARGO", slug,
                         f"bid {bid}/ask {ask} = {spread*100:.0f} punti su {vol/1000:.0f}k vol 24h — candidata maker",
                         round(spread, 4)))
        if abs(hchg) >= rules["mover_min_1h"] and vol >= rules["mover_min_vol"]:
            cand.append((ts_, "MOVER_1H", slug,
                         f"mossa {hchg*100:+.0f} punti in 1h (prezzo {last}) su {vol/1000:.0f}k vol",
                         round(hchg, 4)))
        if ends and ends[:10] == today and vol >= rules["closing_hot_vol"]:
            cand.append((ts_, "CHIUDE_OGGI", slug,
                         f"chiude oggi, vol 24h {vol/1000:.0f}k — finestra informativa finale",
                         round(vol, 2)))

    # ---------------- arbitraggio strutturale ----------------
    try:
        opps, _ = scan_arb(gamma, min_edge=rules["arb_min_edge"])
    except RuntimeError:
        opps = []
    for b in opps:
        edge = max(b["edge_yes"], b["edge_no"])
        side = "TUTTI GLI YES" if b["edge_yes"] >= b["edge_no"] else "TUTTI I NO"
        cand.append((ts, "ARB", b.get("slug"),
                     f"paniere {b['n_outcomes']} esiti '{b['event']}': compra {side}, edge netto {edge*100:.2f}%",
                     round(edge, 4)))

    # ---------------- agenti: segnali shadow + whale watcher ----------------
    from lab import signals as signals_mod
    from lab import whales as whales_mod

    n_new_sig = signals_mod.generate(conn, rows, ts)
    n_closed_sig = signals_mod.evaluate(conn, ts)
    try:
        cand.extend(whales_mod.track(conn, ts))
    except Exception as exc:  # noqa: BLE001 — il watcher non deve mai morire per le balene
        if verbose:
            print(f"   [whales] saltato questo ciclo: {exc}")

    # dedupe: non ripetere lo stesso alert entro `dedupe_min` minuti
    cutoff = (now - timedelta(minutes=rules["dedupe_min"])).isoformat(timespec="seconds")
    kept = []
    for a in cand:
        row = conn.execute(
            "SELECT MAX(ts) FROM alerts WHERE kind=? AND slug=?", (a[1], a[2])
        ).fetchone()
        if row and row[0] and row[0] >= cutoff:
            continue
        kept.append(a)
    if kept:
        conn.executemany("INSERT INTO alerts VALUES (?,?,?,?,?)", kept)

    # ---------------- equity conto paper ----------------
    mark = {}
    for key, pos in paper.positions.items():
        mark[key] = price_map.get(key.split("::")[0], pos.avg_price)
    eq = paper.equity(mark)
    conn.execute("INSERT INTO equity VALUES (?,?)", (ts, round(eq, 2)))
    conn.commit()

    if verbose:
        print(f"[{ts}] mercati={len(rows)}  alert nuovi={len(kept)}  "
              f"segnali shadow: +{n_new_sig} aperti / {n_closed_sig} valutati  "
              f"equity paper={eq:.2f} USDC")
        for a in kept:
            print(f"   >> {a[1]:<15} {a[3]}")
    return {"ts": ts, "markets": len(rows), "alerts": len(kept),
            "signals_new": n_new_sig, "signals_closed": n_closed_sig, "equity": round(eq, 2)}


def main() -> int:
    ap = argparse.ArgumentParser(description="Watcher continuo predmarket-lab")
    ap.add_argument("--once", action="store_true", help="un solo ciclo ed esci")
    ap.add_argument("--loop", action="store_true", help="cicla per sempre (Ctrl-C per stop)")
    ap.add_argument("--cycles", type=int, default=0, help="numero di cicli")
    ap.add_argument("--interval", type=float, default=300, help="secondi tra i cicli (default 300)")
    ap.add_argument("--reset-paper", action="store_true", help="azzera il conto paper")
    args = ap.parse_args()

    if args.reset_paper:
        for f in (os.path.join("data", "paper_state.json"), os.path.join("data", "paper_trades.csv")):
            if os.path.exists(f):
                os.remove(f)
        PaperAccount().save()
        print("Conto paper azzerato: 200 USDC freschi.")

    gamma = GammaClient()
    conn = init_db()
    paper = PaperAccount.load()

    cycles = 10**9 if args.loop else (args.cycles or 1)
    i = 0
    while i < cycles:
        try:
            stats = run_cycle(gamma, conn, paper)
        except Exception as exc:  # noqa: BLE001
            print(f"[errore ciclo {i+1}] {exc} — riprovo tra 10s")
            time.sleep(10)
            i += 1
            continue
        from lab import report
        report.generate(conn, paper)
        with open(os.path.join("data", "last_run.json"), "w", encoding="utf-8") as fh:
            json.dump(stats, fh, indent=1)
        i += 1
        if i < cycles:
            time.sleep(args.interval)
    conn.close()
    print("Fatto: dashboard.html e REPORT.md aggiornati.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
