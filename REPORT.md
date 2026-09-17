# Report predmarket-lab — 18/09/2026 01:41:13

Ultimo scan: `2026-09-17T23:41:07+00:00` UTC · ciclo n.16 · 783 mercati tracciati · 4197 snapshot · 818 alert

## Conto paper

- **Equity:** 201.24 USDC (**ROI +0.62%**)
- Cash 201.24 · posizioni aperte 0 · trade 1 (W 1 / L 0)
- Realized +1.30 · drawdown dal picco -0.6%

## Ultimi alert

- `23:41` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 7058k: candidate yield maker
- `23:41` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 600k: candidate yield maker
- `23:41` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 588k: candidate yield maker
- `23:41` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 487k: candidate yield maker
- `23:41` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 465k: candidate yield maker
- `23:41` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 365k: candidate yield maker
- `23:41` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 301k: candidate yield maker
- `23:41` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 203k: candidate yield maker
- `23:41` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 194k: candidate yield maker
- `23:41` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 191k: candidate yield maker
- `23:41` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 174k: candidate yield maker
- `23:41` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 161k: candidate yield maker

## Indice di inefficienza (v0)

- **0/100** — 0% dei top-50 mercati ha spread >=4 punti, 0% ha mosso >=8 punti in 1h

## Shadow signals (l'AI studia, zero capitale)

- **ENDGAME_FAVORITE** — 7 valutati · 85.7% hit · risultato medio +10.62%
- **LONGSHOT_FADE** — 74 valutati · 85.1% hit · risultato medio +59.52%
- **MAKER_SPREAD** — 1 valutati · 100.0% hit · risultato medio +8.00%
- **MEAN_REVERT** — 8 valutati · 25.0% hit · risultato medio -36.00%

segnali aperti ora:

- `MEAN_REVERT` Dota 2: Kalmychata vs uralan (BO3) - European Pro League Group B — mossa +28p in 1h — ipotesi rientro eccesso
- `LONGSHOT_FADE` Will Roy Cooper win the 2028 Democratic presidential nomination? — longshot a 0.001 — ipotesi sopravvalutazione
- `LONGSHOT_FADE` Will the price of Bitcoin be above $78,000 on September 18? — longshot a 0.045 — ipotesi sopravvalutazione
- `LONGSHOT_FADE` Will the next diplomatic US-Iran meeting be in the United States by Se — longshot a 0.043 — ipotesi sopravvalutazione
- `LONGSHOT_FADE` Will CD Real Tomayapo win on 2026-09-17? — longshot a 0.006 — ipotesi sopravvalutazione
- `LONGSHOT_FADE` Will the price of Bitcoin be above $88,000 on September 19? — longshot a 0.001 — ipotesi sopravvalutazione

## Whale watch 🐋

- **Consenso**: 2 balene (halvanicus,kindar) su 'Lions vs. Bills' — $4,113,656
- halvanicus: Lions vs. Bills @ 0.69 ($3,285,184, P&L -44,267$)
- JnStrtPrdctnMrkts: Will Ethereum dip to $1,500 by December 31, 2026? @ 0.86 ($865,555, P&L +242,774$)
- kindar: Lions vs. Bills @ 0.69 ($828,472, P&L -5,959$)
- JnStrtPrdctnMrkts: Will Bitcoin dip to $55,000 by December 31, 2026? @ 0.82 ($585,214, P&L +205,793$)
- JnStrtPrdctnMrkts: Will Bitcoin dip to $50,000 by December 31, 2026? @ 0.88 ($545,562, P&L +128,336$)

## Watchlist normativa

- Blocco ADM attivo dal 27/07/2026 (Polymarket e Kalshi in lista nera, oscurati dagli ISP)
- TAR Lazio: urgenza rigettata il 05/08/2026; camera di consiglio del 25/08/2026 — esito non ancora reso pubblico alla data di questo report (verificare a ogni run)
- Betfair Italia: unico betting exchange con licenza ADM; automazione consentita via software certificato ADM (accesso API custom da verificare caso per caso)
- Fonti: ADM, Il Sole 24 Ore, Agipro, Sky TG24, Corriere della Sera

## Prossime azioni

1. Lasciare girare il watcher (GitHub Actions / VPS) per costruire lo storico
2. Ogni trade idea → prima in paper (`lab/paper.py`), mai diretto
3. Backtest delle strategie S3/S4/S5 quando il DB ha >= 2 settimane di dati
