"""
predmarket-lab — scanner live dei mercati predittivi (dati pubblici Polymarket).

Uso:
    python3 run_scan.py                  # scan completo
    python3 run_scan.py --mode closing   # solo mercati in chiusura
    python3 run_scan.py --mode arb       # solo arbitraggio strutturale
    python3 run_scan.py --mode spreads   # candidate maker
    python3 run_scan.py --mode movers    # movimenti notizia
    python3 run_scan.py --mode closing --days 3 --min-vol 2000
    python3 run_scan.py --mode fees      # tabella commissioni
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone

try:
    from zoneinfo import ZoneInfo
    ROME = ZoneInfo("Europe/Rome")
except Exception:  # noqa: BLE001
    ROME = timezone.utc

from lab.api import ClobReader, GammaClient
from lab.fees import example_fees, taker_fee_per_share
from lab.scanner import _fmt_vol, scan_arb, scan_closing, scan_movers, scan_spreads

LINE = "=" * 100


def hdr(title: str) -> None:
    now = datetime.now(ROME).strftime("%d/%m/%Y %H:%M:%S")
    print(f"\n{LINE}\n{title}\naggiornato al {now} (Europe/Rome) — dati: Gamma API pubblica\n{LINE}")


def mode_closing(gamma, args) -> None:
    hdr(f"MERCATI IN CHIUSURA ENTRO {args.days} GIORNI (volume 24h > {args.min_vol:.0f})")
    rows = scan_closing(gamma, days=args.days, min_vol24=args.min_vol)
    if not rows:
        print("Nessun mercato coi filtri correnti. Prova --days 14 o --min-vol 0.")
        return
    print(f"{'#':>2} {'CHIUSURA (CEST)':<16} {'ORE':>6} {'YES ask':>7} {'spr':>5} {'vol24h':>8} {'liq':>8} {'fee':>5}  mercato")
    for i, r in enumerate(rows, 1):
        end_local = r["end"].astimezone(ROME).strftime("%d/%m %H:%M")
        flag = " *** OGGI ***" if r["hours_left"] < 24 else ""
        print(f"{i:>2} {end_local:<16} {r['hours_left']:>6.1f} "
              f"{(r['yes_ask'] or 0):>7.3f} {r['spread']:>5.2f} "
              f"{_fmt_vol(r['vol24h']):>8} {_fmt_vol(r['liquidity']):>8} "
              f"{r['fee_rate']:>5.2f}  {r['question'][:52]}{flag}")


def mode_arb(gamma, args) -> None:
    hdr("ARBITRAGGIO STRUTTURALE SU EVENTI MULTI-ESITO (negRisk) — NETTO DELLE FEE")
    opps, top = scan_arb(gamma)
    if opps:
        print(f"*** TROVATE {len(opps)} OPPORTUNITA' >= 0.5% (verificare order book CLOB prima di agire!) ***")
        for b in opps[:10]:
            side = "COMPRA TUTTI GLI YES" if b["edge_yes"] >= b["edge_no"] else "COMPRA TUTTI I NO"
            edge = max(b["edge_yes"], b["edge_no"])
            print(f"  +{edge*100:.2f}% | {side} | {b['event']} ({b['n_outcomes']} esiti) -> {b['slug']}")
    else:
        print("Nessuna opportunita' netta >= 0.5% in questo istante (normale: i bot HFT le chiudono in ~3 secondi).")
    print("\nPaniere MULTI-ESITO piu' vicini al rounding (per monitoraggio):")
    print(f"{'evento':<50} {'esiti':>5} {'costo YES':>9} {'edge YES':>8} {'edge NO':>8}")
    for b in top:
        print(f"{b['event'][:48]:<50} {b['n_outcomes']:>5} {b['cost_yes_basket']:>9.3f} "
              f"{b['edge_yes']*100:>7.2f}% {b['edge_no']*100:>7.2f}%")


def mode_spreads(gamma, args) -> None:
    hdr("MERCATI CON ALTO VOLUME E SPREAD LARGO (candidate strategie MAKER — fee 0% + rebate)")
    rows = scan_spreads(gamma)
    if not rows:
        print("Nessun mercato coi filtri correnti.")
        return
    print(f"{'bid':>6} {'ask':>6} {'spr':>5} {'vol24h':>8} {'liq':>8} {'rw':>2}  mercato")
    for r in rows:
        print(f"{(r['bid'] or 0):>6.2f} {(r['ask'] or 0):>6.2f} {r['spread']:>5.2f} "
              f"{_fmt_vol(r['vol24h']):>8} {_fmt_vol(r['liquidity']):>8} "
              f"{'Y' if r['has_clob_rewards'] else '-':>2}  {r['question'][:56]}")


def mode_movers(gamma, args) -> None:
    hdr("I 20 MERCATI CHE SI STANNO MUOVENDO DI PIU' (ultime 24h) — zona notizia")
    rows = scan_movers(gamma)
    if not rows:
        print("Nessun movimento rilevante.")
        return
    print(f"{'prezzo':>7} {'1h':>7} {'24h':>7} {'vol24h':>8}  mercato")
    for r in rows:
        print(f"{(r['price'] or 0):>7.3f} {r['chg_1h']*100:>6.1f}% {r['chg_24h']*100:>6.1f}% "
              f"{_fmt_vol(r['vol24h']):>8}  {r['question'][:58]}")


def mode_fees(_gamma, _args) -> None:
    hdr("TABELLA COMMISSIONI TAKER POLYMARKET (V2, 30/03/2026) — fee = rate*p*(1-p)")
    print(f"{'categoria':<28} {'rate':>5} {'fee su 100 share @ 50c':>24} {'@ 20c':>9}")
    for name, rate, at50, at20 in example_fees():
        print(f"{name:<28} {rate:>5.2f} {'$' + format(at50, '.2f'):>24} {'$' + format(at20, '.2f'):>9}")
    print("\nRegola pratica: spread + fee taker = costo round-trip. Sotto ~2 punti di edge NETTO non entri.")


def mode_book(gamma, args) -> None:
    """Deep-dive order book di un mercato (via slug)."""
    hdr(f"ORDER BOOK CLOB — {args.slug}")
    markets = gamma.markets(slug=args.slug)
    if not markets:
        # prova come evento: usa il primo mercato del gruppo
        events = gamma.events(slug=args.slug)
        if events and events[0].get("markets"):
            markets = events[0]["markets"]
    if not markets:
        print("Slug non trovato (ne' come mercato ne' come evento).")
        return
    m = markets[0]
    import json as _json
    tids = _json.loads(m["clobTokenIds"]) if isinstance(m.get("clobTokenIds"), str) else m.get("clobTokenIds", [])
    clob = ClobReader()
    for i, (tid, out) in enumerate(zip(tids, _json.loads(m["outcomes"]) if isinstance(m.get("outcomes"), str) else m.get("outcomes", []))):
        book = clob.book(tid)
        bids = sorted(book.get("bids", []), key=lambda b: -float(b["price"]))[:5]
        asks = sorted(book.get("asks", []), key=lambda a: float(a["price"]))[:5]
        print(f"\nEsito: {out}")
        print("  top bids:", ", ".join(f"{b['price']}x{float(b['size']):,.0f}" for b in bids))
        print("  top asks:", ", ".join(f"{a['price']}x{float(a['size']):,.0f}" for a in asks))


def main() -> int:
    ap = argparse.ArgumentParser(description="Scanner live mercati predittivi (sola lettura)")
    ap.add_argument("--mode", default="all",
                    choices=["all", "closing", "arb", "spreads", "movers", "fees", "book"])
    ap.add_argument("--days", type=int, default=7, help="orizzonte chiusura (default 7)")
    ap.add_argument("--min-vol", type=float, default=500.0, help="volume 24h minimo (default 500)")
    ap.add_argument("--slug", default=None, help="slug mercato per --mode book")
    args = ap.parse_args()

    if args.mode == "book" and not args.slug:
        print("Serve --slug con --mode book")
        return 2

    gamma = GammaClient()
    if args.mode in ("all", "closing"):
        mode_closing(gamma, args)
    if args.mode in ("all", "arb"):
        mode_arb(gamma, args)
    if args.mode in ("all", "spreads"):
        mode_spreads(gamma, args)
    if args.mode in ("all", "movers"):
        mode_movers(gamma, args)
    if args.mode == "fees":
        mode_fees(gamma, args)
    if args.mode == "book":
        mode_book(gamma, args)
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
