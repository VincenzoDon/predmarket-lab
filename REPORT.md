# Report predmarket-lab — 17/09/2026 16:27:38

Ultimo scan: `2026-09-17T14:27:33+00:00` UTC · ciclo n.13 · 573 mercati tracciati · 3297 snapshot · 395 alert

## Conto paper

- **Equity:** 201.24 USDC (**ROI +0.62%**)
- Cash 201.24 · posizioni aperte 0 · trade 1 (W 1 / L 0)
- Realized +1.30 · drawdown dal picco -0.6%

## Ultimi alert

- `14:27` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 1159k: candidate yield maker
- `14:27` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 843k: candidate yield maker
- `14:27` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 672k: candidate yield maker
- `14:27` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 656k: candidate yield maker
- `14:27` **CHIUDE_OGGI** — chiude oggi, vol 24h 379k — finestra informativa finale
- `14:27` **CHIUDE_OGGI** — chiude oggi, vol 24h 366k — finestra informativa finale
- `14:27` **CHIUDE_OGGI** — chiude oggi, vol 24h 311k — finestra informativa finale
- `14:27` **CHIUDE_OGGI** — chiude oggi, vol 24h 284k — finestra informativa finale
- `14:27` **MOVER_1H** — mossa +58 punti in 1h (prezzo 0.999) su 281k vol
- `14:27` **CHIUDE_OGGI** — chiude oggi, vol 24h 275k — finestra informativa finale
- `14:27` **CHIUDE_OGGI** — chiude oggi, vol 24h 274k — finestra informativa finale
- `14:27` **MOVER_1H** — mossa +39 punti in 1h (prezzo 0.999) su 228k vol

## Indice di inefficienza (v0)

- **7/100** — 2% dei top-50 mercati ha spread >=4 punti, 14% ha mosso >=8 punti in 1h

## Shadow signals (l'AI studia, zero capitale)

- **ENDGAME_FAVORITE** — 6 valutati · 100.0% hit · risultato medio +13.32%
- **LONGSHOT_FADE** — 71 valutati · 85.9% hit · risultato medio +60.70%
- **MAKER_SPREAD** — 1 valutati · 100.0% hit · risultato medio +8.00%
- **MEAN_REVERT** — 7 valutati · 28.6% hit · risultato medio -41.14%

segnali aperti ora:

- `MEAN_REVERT` Szczecin: Marco Cecchinato vs Marvin Moeller — mossa +58p in 1h — ipotesi rientro eccesso
- `MEAN_REVERT` Caldas da Rainha: Jeline Vandromme vs Elena Malygina — mossa +39p in 1h — ipotesi rientro eccesso
- `LONGSHOT_FADE` Will the price of Bitcoin be above $78,000 on September 17? — longshot a 0.049 — ipotesi sopravvalutazione
- `MEAN_REVERT` Rennes: Francesco Maestrelli vs Yanis Durand — mossa +11p in 1h — ipotesi rientro eccesso
- `MEAN_REVERT` Caldas da Rainha: Noma Noha Akugue vs Malaika Rapolu — mossa -55p in 1h — ipotesi rientro eccesso
- `LONGSHOT_FADE` Caldas da Rainha: Noma Noha Akugue vs Malaika Rapolu — longshot a 0.001 — ipotesi sopravvalutazione

## Whale watch 🐋

- JnStrtPrdctnMrkts: Will Ethereum dip to $1,500 by December 31, 2026? @ 0.86 ($865,555, P&L +242,774$)
- JnStrtPrdctnMrkts: Will Bitcoin dip to $55,000 by December 31, 2026? @ 0.83 ($588,761, P&L +209,340$)
- JnStrtPrdctnMrkts: Will Bitcoin dip to $50,000 by December 31, 2026? @ 0.88 ($545,562, P&L +128,336$)
- JnStrtPrdctnMrkts: Will Ethereum dip to $1,250 by December 31, 2026? @ 0.92 ($362,494, P&L +60,920$)
- JnStrtPrdctnMrkts: Will Ethereum dip to $1,750 by December 31, 2026? @ 0.84 ($322,899, P&L +30,362$)

## Watchlist normativa

- Blocco ADM attivo dal 27/07/2026 (Polymarket e Kalshi in lista nera, oscurati dagli ISP)
- TAR Lazio: urgenza rigettata il 05/08/2026; camera di consiglio del 25/08/2026 — esito non ancora reso pubblico alla data di questo report (verificare a ogni run)
- Betfair Italia: unico betting exchange con licenza ADM; automazione consentita via software certificato ADM (accesso API custom da verificare caso per caso)
- Fonti: ADM, Il Sole 24 Ore, Agipro, Sky TG24, Corriere della Sera

## Prossime azioni

1. Lasciare girare il watcher (GitHub Actions / VPS) per costruire lo storico
2. Ogni trade idea → prima in paper (`lab/paper.py`), mai diretto
3. Backtest delle strategie S3/S4/S5 quando il DB ha >= 2 settimane di dati
