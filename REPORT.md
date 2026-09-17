# Report predmarket-lab — 17/09/2026 23:37:23

Ultimo scan: `2026-09-17T21:37:17+00:00` UTC · ciclo n.15 · 717 mercati tracciati · 3897 snapshot · 700 alert

## Conto paper

- **Equity:** 201.24 USDC (**ROI +0.62%**)
- Cash 201.24 · posizioni aperte 0 · trade 1 (W 1 / L 0)
- Realized +1.30 · drawdown dal picco -0.6%

## Ultimi alert

- `21:37` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 6642k: candidate yield maker
- `21:37` **CHIUDE_OGGI** — chiude oggi, vol 24h 1980k — finestra informativa finale
- `21:37` **MOVER_1H** — mossa +22 punti in 1h (prezzo 0.999) su 1568k vol
- `21:37` **CHIUDE_OGGI** — chiude oggi, vol 24h 1568k — finestra informativa finale
- `21:37` **MOVER_1H** — mossa +21 punti in 1h (prezzo 0.999) su 881k vol
- `21:37` **CHIUDE_OGGI** — chiude oggi, vol 24h 881k — finestra informativa finale
- `21:37` **CHIUDE_OGGI** — chiude oggi, vol 24h 845k — finestra informativa finale
- `21:37` **CHIUDE_OGGI** — chiude oggi, vol 24h 627k — finestra informativa finale
- `21:37` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 583k: candidate yield maker
- `21:37` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 582k: candidate yield maker
- `21:37` **CHIUDE_OGGI** — chiude oggi, vol 24h 527k — finestra informativa finale
- `21:37` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 465k: candidate yield maker

## Indice di inefficienza (v0)

- **6/100** — 0% dei top-50 mercati ha spread >=4 punti, 16% ha mosso >=8 punti in 1h

## Shadow signals (l'AI studia, zero capitale)

- **ENDGAME_FAVORITE** — 7 valutati · 85.7% hit · risultato medio +10.62%
- **LONGSHOT_FADE** — 73 valutati · 84.9% hit · risultato medio +59.63%
- **MAKER_SPREAD** — 1 valutati · 100.0% hit · risultato medio +8.00%
- **MEAN_REVERT** — 8 valutati · 25.0% hit · risultato medio -36.00%

segnali aperti ora:

- `LONGSHOT_FADE` Will Real Sociedad de Fútbol win on 2026-09-17? — longshot a 0.001 — ipotesi sopravvalutazione
- `MEAN_REVERT` Rennes: Daniel Rincon vs Titouan Droguet — mossa -22p in 1h — ipotesi rientro eccesso
- `LONGSHOT_FADE` Rennes: Daniel Rincon vs Titouan Droguet — longshot a 0.001 — ipotesi sopravvalutazione
- `LONGSHOT_FADE` Will Málaga CF win on 2026-09-17? — longshot a 0.001 — ipotesi sopravvalutazione
- `MEAN_REVERT` Tiburon: Timo Legout vs Bryce Nakashima — mossa -46p in 1h — ipotesi rientro eccesso
- `LONGSHOT_FADE` Tiburon: Timo Legout vs Bryce Nakashima — longshot a 0.001 — ipotesi sopravvalutazione

## Whale watch 🐋

- **Consenso**: 3 balene (halvanicus,kindar,mooseborzoi) su 'Lions vs. Bills' — $4,139,761
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
