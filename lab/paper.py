"""
Paper trading engine: simula operazioni su dati reali SENZA soldi veri.

Perche' e' la Fase 0 obbligatoria del piano:
- Polymarket NON offre testnet/sandbox: gli errori con soldi veri costano.
- Qui compriamo a prezzo reale (ask) + fee taker reali + slippage configurabile,
  cosi' quello che vedi in paper e' quello che accadrebbe con 5-10x piu' soldi.

Stato persistente in data/paper_state.json, operazioni in data/paper_trades.csv.
"""

from __future__ import annotations

import csv
import json
import os
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone

from .fees import taker_fee_per_share

STATE_FILE = os.path.join("data", "paper_state.json")
TRADES_FILE = os.path.join("data", "paper_trades.csv")


@dataclass
class Position:
    question: str
    outcome: str
    shares: float
    avg_price: float
    fee_rate: float = 0.0
    opened_at: str = ""


@dataclass
class PaperAccount:
    bankroll: float = 200.0          # in USDC (1 USDC ~ 1 USD)
    cash: float = 200.0
    positions: dict[str, Position] = field(default_factory=dict)
    n_trades: int = 0
    n_wins: int = 0
    n_losses: int = 0
    realized_pnl: float = 0.0
    max_bankroll: float = 200.0
    state_file: str = STATE_FILE
    trades_file: str = TRADES_FILE

    # ------------------------------------------------------------------ io
    @classmethod
    def load(cls, path: str = STATE_FILE) -> "PaperAccount":
        if os.path.exists(path):
            with open(path, encoding="utf-8") as fh:
                raw = json.load(fh)
            pos = {k: Position(**v) for k, v in raw.pop("positions", {}).items()}
            raw["positions"] = pos
            raw["state_file"] = path
            return cls(**raw)
        acc = cls()
        acc.state_file = path
        return acc

    def save(self) -> None:
        os.makedirs(os.path.dirname(self.state_file) or ".", exist_ok=True)
        data = asdict(self)
        with open(self.state_file, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2, ensure_ascii=False)

    def _log(self, kind: str, slug: str, detail: str, amount: float) -> None:
        os.makedirs(os.path.dirname(self.trades_file) or ".", exist_ok=True)
        new = not os.path.exists(self.trades_file)
        with open(self.trades_file, "a", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            if new:
                w.writerow(["timestamp_utc", "type", "slug", "detail", "amount_usd"])
            w.writerow(
                [
                    datetime.now(timezone.utc).isoformat(timespec="seconds"),
                    kind,
                    slug,
                    detail,
                    round(amount, 4),
                ]
            )

    # -------------------------------------------------------------- azioni
    def buy(
        self,
        slug: str,
        question: str,
        outcome: str,
        ask_price: float,
        stake: float,
        fee_rate: float = 0.0,
        slippage: float = 0.005,
    ) -> dict:
        """Compra `stake` USDC di `outcome` all'ask (con slippage)."""
        if stake > self.cash:
            return {"ok": False, "error": "cash insufficiente"}
        fill_price = min(ask_price * (1 + slippage), 0.999)
        fee = stake * taker_fee_per_share(fill_price, fee_rate) / fill_price * fill_price
        # fee proporzionale allo stake: shares = stake/(p+fee_p)
        cost_per_share = fill_price + taker_fee_per_share(fill_price, fee_rate)
        shares = stake / cost_per_share
        key = f"{slug}::{outcome}"
        if key in self.positions:
            p = self.positions[key]
            tot = p.shares + shares
            p.avg_price = (p.avg_price * p.shares + fill_price * shares) / tot
            p.shares = tot
        else:
            self.positions[key] = Position(
                question=question,
                outcome=outcome,
                shares=shares,
                avg_price=fill_price,
                fee_rate=fee_rate,
                opened_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
            )
        self.cash -= stake
        self.n_trades += 1
        self.max_bankroll = max(self.max_bankroll, self.equity({}))
        self.save()
        self._log("BUY", slug, f"{outcome} @ {fill_price:.3f} x{shares:.1f}", -stake)
        return {
            "ok": True,
            "shares": round(shares, 2),
            "fill_price": round(fill_price, 4),
            "fee_paid": round(stake - shares * fill_price, 4),
        }

    def sell(self, slug: str, outcome: str, bid_price: float, shares: float | None = None,
             fee_rate: float = 0.0) -> dict:
        """Vendi (esci prima della risoluzione) al bid."""
        key = f"{slug}::{outcome}"
        p = self.positions.get(key)
        if not p:
            return {"ok": False, "error": "posizione inesistente"}
        qty = min(shares or p.shares, p.shares)
        proceeds = qty * bid_price - qty * taker_fee_per_share(bid_price, fee_rate)
        cost = qty * p.avg_price
        pnl = proceeds - cost
        self.cash += proceeds
        self.realized_pnl += pnl
        p.shares -= qty
        if p.shares <= 1e-9:
            del self.positions[key]
        (self.n_wins if pnl >= 0 else self.n_losses).__class__  # no-op typing
        if pnl >= 0:
            self.n_wins += 1
        else:
            self.n_losses += 1
        self.save()
        self._log("SELL", slug, f"{outcome} @ {bid_price:.3f} x{qty:.1f}", proceeds)
        return {"ok": True, "pnl": round(pnl, 4), "cash": round(self.cash, 2)}

    def settle(self, slug: str, winning_outcome: str) -> list[dict]:
        """Risolvi tutte le posizioni di un mercato: 1 USDC per share vincente."""
        results = []
        for key in [k for k in self.positions if k.startswith(f"{slug}::")]:
            p = self.positions[key]
            won = p.outcome == winning_outcome
            payout = p.shares if won else 0.0
            pnl = payout - p.shares * p.avg_price
            self.cash += payout
            self.realized_pnl += pnl
            if pnl >= 0:
                self.n_wins += 1
            else:
                self.n_losses += 1
            del self.positions[key]
            self._log("SETTLE", slug, f"{p.outcome} -> {'WIN' if won else 'LOSE'}", payout)
            results.append({"key": key, "won": won, "pnl": round(pnl, 2)})
        self.save()
        return results

    # -------------------------------------------------------------- metric
    def equity(self, mark_prices: dict[str, float]) -> float:
        """cash + valore posizioni ai prezzi correnti (chiave: 'slug::outcome')."""
        pos_val = 0.0
        for key, p in self.positions.items():
            price = mark_prices.get(key, p.avg_price)
            pos_val += p.shares * price
        return self.cash + pos_val

    def summary(self, mark_prices: dict[str, float] | None = None) -> dict:
        eq = self.equity(mark_prices or {})
        return {
            "cash": round(self.cash, 2),
            "open_positions": len(self.positions),
            "equity": round(eq, 2),
            "roi_pct": round((eq / self.bankroll - 1) * 100, 2),
            "realized_pnl": round(self.realized_pnl, 2),
            "trades": self.n_trades,
            "wins": self.n_wins,
            "losses": self.n_losses,
            "peak_bankroll": round(self.max_bankroll, 2),
            "drawdown_pct": round((1 - eq / self.max_bankroll) * 100, 2),
        }
