"""
Money management: Kelly frazionato e limiti di rischio.

Un contratto binario comprato a prezzo `c` che paga 1 se l'evento avviene:
se stimi la probabilita' reale `q`, il Kelly ottimo (frazione del bankroll
da impegnare) e':

    f* = (q - c) / (1 - c)

Regole d'oro:
- MAI Kelly pieno: usa 1/4 di Kelly (le stime q sono rumorose).
- Cap duro per posizione (es. 5% del bankroll).
- Stop-loss giornaliero (es. -10%) e bankroll "ricaricabile" max 2 volte.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RiskConfig:
    bankroll: float = 200.0
    kelly_fraction: float = 0.25   # 1/4 di Kelly
    max_stake_pct: float = 0.05    # mai piu' del 5% del bankroll per trade
    min_edge: float = 0.02         # segni il trade solo se q - c >= 2 punti
    daily_stop_loss_pct: float = 0.10


def kelly_fraction(q: float, price: float) -> float:
    """Kelly pieno. >0 -> compra, <0 -> (se possibile) vendi/short."""
    if price <= 0.0 or price >= 1.0:
        return 0.0
    return (q - price) / (1.0 - price)


def suggested_stake(
    q: float,
    price: float,
    cfg: RiskConfig,
    bankroll: float | None = None,
) -> float:
    """Stake consigliato in valuta (0 se non c'e' edge sufficiente)."""
    bank = bankroll if bankroll is not None else cfg.bankroll
    if q - price < cfg.min_edge:
        return 0.0
    f = kelly_fraction(q, price) * cfg.kelly_fraction
    f = min(f, cfg.max_stake_pct)
    if f <= 0:
        return 0.0
    return round(bank * f, 2)


def risk_of_ruin_simulation(
    n_bets: int = 100,
    win_prob: float = 0.55,
    payout_ratio: float = 1.0,
    stake_pct: float = 0.05,
    runs: int = 20000,
    seed: int = 42,
) -> dict:
    """Monte Carlo veloce: probabilita' di dimezzarsi/distruggersi con sizing dato."""
    import random

    rng = random.Random(seed)
    ruined = halved = 0
    finals = []
    for _ in range(runs):
        bank = 1.0
        for _ in range(n_bets):
            stake = bank * stake_pct
            if rng.random() < win_prob:
                bank += stake * payout_ratio
            else:
                bank -= stake
            if bank <= 0.05:
                ruined += 1
                break
        finals.append(bank)
        if bank <= 0.5:
            halved += 1
    finals.sort()
    return {
        "bets": n_bets,
        "win_prob": win_prob,
        "p_ruin": ruined / runs,
        "p_halved": halved / runs,
        "median_bankroll": finals[len(finals) // 2],
    }
