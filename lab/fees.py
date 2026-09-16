"""
Modello delle commissioni Polymarket (Fee Structure V2, dal 30/03/2026).

Formula (per share, lato TAKER):
    fee = rate * price * (1 - price)

dove `rate` dipende dalla categoria ed e' esposta nel campo `feeSchedule`
di ogni mercato via Gamma API:
    crypto   ~0.07 | sports ~0.03 | finance/politics/tech ~0.04
    economics/culture/weather ~0.05 | geopolitics/world = 0 (fee-free)

I MAKER pagano 0 e ricevono rebate (rebateRate ~ 0.25 dei taker fees).

Riferimento: campo `feeSchedule: {exponent, rate, takerOnly, rebateRate}`
nelle risposte Gamma. `feesEnabled: false` -> nessuna commissione.
"""

from __future__ import annotations


def market_fee_rate(market: dict) -> float:
    """Estrae il taker fee rate di un mercato Gamma (0 se fee disabilitate)."""
    if not market.get("feesEnabled"):
        return 0.0
    schedule = market.get("feeSchedule") or {}
    try:
        return float(schedule.get("rate") or 0.0)
    except (TypeError, ValueError):
        return 0.0


def taker_fee_per_share(price: float, rate: float) -> float:
    """Commissione taker per singola share acquistata a `price`."""
    if rate <= 0:
        return 0.0
    p = min(max(price, 0.0), 1.0)
    return rate * p * (1.0 - p)


def buy_cost_per_share(price: float, rate: float) -> float:
    """Costo effettivo per share acquistata come taker (prezzo + fee)."""
    return price + taker_fee_per_share(price, rate)


def max_taker_fee_on_stake(stake: float, rate: float) -> float:
    """Fee massima possibile su uno stake `stake` (picco a price=0.5)."""
    return stake * rate * 0.25


def example_fees() -> list[tuple[str, float, float, float]]:
    """Tabella esemplificativa: (categoria, rate, fee su 100 share a 50c, a 20c)."""
    out = []
    for name, rate in [
        ("geopolitics (free)", 0.0),
        ("sports", 0.03),
        ("finance/politics/tech", 0.04),
        ("economics/culture/weather", 0.05),
        ("crypto", 0.07),
    ]:
        at_50 = 100 * taker_fee_per_share(0.5, rate)
        at_20 = 100 * taker_fee_per_share(0.2, rate)
        out.append((name, rate, at_50, at_20))
    return out
