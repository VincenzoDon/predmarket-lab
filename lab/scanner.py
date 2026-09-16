"""
Scanner dei mercati Polymarket su DATI LIVE (Gamma API pubblica).

Quattro scansioni, una per tipo di vantaggio:

1. closing  -> mercati che chiudono entro N giorni con liquidita'/volume
               (i "final sprint": dove le informazioni tardive pagano di piu')
2. arb      -> arbitraggio strutturale su eventi multi-esito (negRisk):
               se la somma degli ask di TUTTI gli esiti < 1 USDC - fee,
               comprare tutto il paniere = profitto garantito
3. spreads  -> mercati con volume alto e spread largo = candidate per
               strategie MAKER (fee 0% + rebate)
4. movers   -> piu' grandi movimenti di prezzo 24h/1h = volatilita' da notizia

Tutto e' calcolato NETTO delle fee taker reali (campo feeSchedule).
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone


def _f(x, default=None):
    try:
        return float(x)
    except (TypeError, ValueError):
        return default


def _fmt_vol(v: float) -> str:
    if v >= 1_000_000:
        return f"{v/1_000_000:.1f}M"
    if v >= 1_000:
        return f"{v/1_000:.0f}k"
    return f"{v:.0f}"


# --------------------------------------------------------------------- 1. closing
def scan_closing(gamma, days: int = 7, min_liquidity: float = 2000.0,
                 min_vol24: float = 500.0, limit: int = 60) -> list[dict]:
    """Mercati attivi che scadono entro `days`, ordinati per chiusura imminente."""
    now = datetime.now(timezone.utc)
    markets = gamma.markets(
        active="true", closed="false", archived="false",
        end_date_min=now.strftime("%Y-%m-%d"),
        end_date_max=(now + timedelta(days=days)).strftime("%Y-%m-%d"),
        order="endDate", ascending="true", limit=500,
    )
    rows = []
    for m in markets:
        end = m.get("endDate")
        if not end:
            continue
        try:
            end_dt = datetime.fromisoformat(end.replace("Z", "+00:00"))
        except ValueError:
            continue
        # NB: endDate e' mezzanotte UTC del giorno di chiusura: il mercato resta
        # vivo fino alla risoluzione effettiva (es. annuncio FOMC serale).
        if end_dt.date() < now.date():
            continue
        liq = _f(m.get("liquidityNum"), 0) or 0
        vol = _f(m.get("volume24hr"), 0) or 0
        if liq < min_liquidity or vol < min_vol24:
            continue
        ask = _f(m.get("bestAsk"))
        bid = _f(m.get("bestBid"))
        rows.append({
            "question": m.get("question", "")[:78],
            "slug": m.get("slug"),
            "end": end_dt,
            "hours_left": max(0.0, (end_dt - now).total_seconds() / 3600),
            "ends_today": end_dt.date() == now.date(),
            "yes_ask": ask,
            "spread": _f(m.get("spread"), 0) or 0,
            "vol24h": vol,
            "liquidity": liq,
            "fee_rate": _f((m.get("feeSchedule") or {}).get("rate"), 0) if m.get("feesEnabled") else 0.0,
            "clob_token_ids": m.get("clobTokenIds"),
        })
        if len(rows) >= limit:
            break
    rows.sort(key=lambda r: r["hours_left"])
    return rows


# --------------------------------------------------------------------- 2. arb
def scan_arb(gamma, limit_events: int = 150, min_edge: float = 0.005) -> tuple[list[dict], list[dict]]:
    """Arbitraggio strutturale su eventi negRisk (esiti mutuamente esclusivi).

    Comprare 1 share YES di OGNI esito costa sum(ask_i + fee_i).
    Esattamente un esito paghera' 1 USDC -> se il costo < 1, edge garantito.
    Simmetricamente: comprare NO ovunque costa sum((1-bid_i) + fee_no_i).

    Ritorna (opportunita_nette_positive, top_baskets_per_riferimento).
    """
    from .fees import taker_fee_per_share

    events = gamma.events(
        active="true", closed="false", archived="false",
        order="volume24hr", ascending="false", limit=limit_events,
    )
    baskets = []
    for ev in events:
        groups: dict[str, list[dict]] = {}
        for m in ev.get("markets") or []:
            if not m.get("negRisk"):
                continue
            gid = m.get("negRiskMarketID") or f"ev-{ev.get('id')}"
            groups.setdefault(gid, []).append(m)
        for gid, ms in groups.items():
            if len(ms) < 3:  # con 2 esiti e' un binario normale
                continue
            legs, ok = [], True
            for m in ms:
                ask = _f(m.get("bestAsk"))
                bid = _f(m.get("bestBid"))
                if ask is None or bid is None or ask <= 0 or ask >= 1:
                    ok = False
                    break
                rate = _f((m.get("feeSchedule") or {}).get("rate"), 0) if m.get("feesEnabled") else 0.0
                legs.append({"title": m.get("groupItemTitle") or m.get("question", "")[:40],
                             "ask": ask, "bid": bid, "fee_rate": rate or 0.0})
            if not ok or not legs:
                continue
            n = len(legs)
            cost_yes = sum(l["ask"] + taker_fee_per_share(l["ask"], l["fee_rate"]) for l in legs)
            # comprare YES di ogni esito -> esattamente 1 paga 1 USDC
            # comprare NO di ogni esito  -> gli altri (n-1) pagano 1 USDC ciascuno
            cost_no = sum((1 - l["bid"]) + taker_fee_per_share(1 - l["bid"], l["fee_rate"]) for l in legs)
            baskets.append({
                "event": ev.get("title", "?")[:70],
                "slug": ev.get("slug"),
                "n_outcomes": n,
                "cost_yes_basket": cost_yes,
                "edge_yes": 1.0 - cost_yes,            # >0 = comprare tutti gli YES
                "edge_no": (n - 1) - cost_no,          # >0 = comprare tutti i NO
                "legs": legs,
            })
    baskets.sort(key=lambda b: max(b["edge_yes"], b["edge_no"]), reverse=True)
    opps = [b for b in baskets if max(b["edge_yes"], b["edge_no"]) >= min_edge]
    return opps, baskets[:10]


# --------------------------------------------------------------------- 3. spreads
def scan_spreads(gamma, min_vol24: float = 10_000.0, min_spread: float = 0.03,
                 limit: int = 25) -> list[dict]:
    """Mercati molto scambiati con spread largo: nicchie per strategie maker."""
    markets = gamma.markets(
        active="true", closed="false", archived="false",
        order="volume24hr", ascending="false", limit=300,
    )
    rows = []
    for m in markets:
        vol = _f(m.get("volume24hr"), 0) or 0
        spread = _f(m.get("spread"), 0) or 0
        liq = _f(m.get("liquidityNum"), 0) or 0
        if vol < min_vol24 or spread < min_spread:
            continue
        ask = _f(m.get("bestAsk"))
        bid = _f(m.get("bestBid"))
        rows.append({
            "question": m.get("question", "")[:70],
            "slug": m.get("slug"),
            "bid": bid, "ask": ask, "spread": spread,
            "vol24h": vol, "liquidity": liq,
            "has_clob_rewards": bool(m.get("clobRewards")),
        })
        if len(rows) >= limit:
            break
    rows.sort(key=lambda r: (r["vol24h"] * r["spread"]), reverse=True)
    return rows


# --------------------------------------------------------------------- 4. movers
def scan_movers(gamma, min_vol24: float = 50_000.0, top: int = 20) -> list[dict]:
    """I piu' grandi movimenti di prezzo (1h / 24h): dove sta girando la notizia."""
    markets = gamma.markets(
        active="true", closed="false", archived="false",
        order="volume24hr", ascending="false", limit=300,
    )
    rows = []
    for m in markets:
        vol = _f(m.get("volume24hr"), 0) or 0
        if vol < min_vol24:
            continue
        ch1h = _f(m.get("oneHourPriceChange"), 0) or 0
        ch24h = _f(m.get("oneDayPriceChange"), 0) or 0
        price = _f(m.get("lastTradePrice"))
        rows.append({
            "question": m.get("question", "")[:70],
            "slug": m.get("slug"),
            "price": price, "chg_1h": ch1h, "chg_24h": ch24h,
            "vol24h": vol,
        })
    rows.sort(key=lambda r: abs(r["chg_24h"]), reverse=True)
    return rows[:top]
