# Report predmarket-lab — 18/09/2026 03:31:32

Ultimo scan: `2026-09-18T01:31:26+00:00` UTC · ciclo n.17 · 822 mercati tracciati · 4497 snapshot · 988 alert

## Conto paper

- **Equity:** 201.24 USDC (**ROI +0.62%**)
- Cash 201.24 · posizioni aperte 0 · trade 1 (W 1 / L 0)
- Realized +1.30 · drawdown dal picco -0.6%

## Ultimi alert

- `01:31` **MOVER_1H** — mossa -17 punti in 1h (prezzo 0.06) su 8051k vol
- `01:31` **CHIUDE_OGGI** — chiude oggi, vol 24h 8051k — finestra informativa finale
- `01:31` **MOVER_1H** — mossa +26 punti in 1h (prezzo 0.88) su 736k vol
- `01:31` **CHIUDE_OGGI** — chiude oggi, vol 24h 736k — finestra informativa finale
- `01:31` **MOVER_1H** — mossa +27 punti in 1h (prezzo 0.88) su 620k vol
- `01:31` **CHIUDE_OGGI** — chiude oggi, vol 24h 620k — finestra informativa finale
- `01:31` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 611k: candidate yield maker
- `01:31` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 560k: candidate yield maker
- `01:31` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 533k: candidate yield maker
- `01:31` **MOVER_1H** — mossa -30 punti in 1h (prezzo 0.113) su 504k vol
- `01:31` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 465k: candidate yield maker
- `01:31` **MOVER_1H** — mossa +34 punti in 1h (prezzo 0.94) su 376k vol

## Indice di inefficienza (v0)

- **12/100** — 2% dei top-50 mercati ha spread >=4 punti, 26% ha mosso >=8 punti in 1h

## Shadow signals (l'AI studia, zero capitale)

- **ENDGAME_FAVORITE** — 7 valutati · 85.7% hit · risultato medio +10.62%
- **LONGSHOT_FADE** — 75 valutati · 84.0% hit · risultato medio +58.72%
- **MAKER_SPREAD** — 1 valutati · 100.0% hit · risultato medio +8.00%
- **MEAN_REVERT** — 8 valutati · 25.0% hit · risultato medio -36.00%

segnali aperti ora:

- `ENDGAME_FAVORITE` Spread: Bills (-6.5) — favorito 0.85 a fine giornata, spread 2p, vol 736k
- `ENDGAME_FAVORITE` Spread: Bills (-5.5) — favorito 0.89 a fine giornata, spread 1p, vol 620k
- `MEAN_REVERT` Boston Red Sox vs. Texas Rangers — mossa -30p in 1h — ipotesi rientro eccesso
- `MEAN_REVERT` Philadelphia Phillies vs. New York Mets — mossa +34p in 1h — ipotesi rientro eccesso
- `LONGSHOT_FADE` Kansas City Royals vs. Houston Astros — longshot a 0.007 — ipotesi sopravvalutazione
- `MEAN_REVERT` Guadalajara Open Akron: Marta Kostyuk vs Liudmila Samsonova — mossa -12p in 1h — ipotesi rientro eccesso

## Whale watch 🐋

- **Consenso**: 3 balene (halvanicus,kindar,Donkey14) su 'Lions vs. Bills' — $5,624,683
- **Consenso**: 2 balene (Talvez10,Feromont) su 'Boston Red Sox vs. Texas Rangers' — $183,121
- **Consenso**: 2 balene (Feromont,Donkey14) su 'Philadelphia Phillies vs. New York Mets' — $42,422
- halvanicus: Lions vs. Bills @ 0.94 ($4,419,636, P&L +1,090,185$)
- kindar: Lions vs. Bills @ 0.94 ($1,114,563, P&L +280,132$)
- kindar: Will United Russia (ER) gain the most seats in the next Russ @ 0.77 ($374,754, P&L +11,865$)
- Talvez10: Boston Red Sox vs. Texas Rangers @ 0.87 ($165,771, P&L +74,990$)
- Feromont: Spread: Bills (-5.5) @ 0.89 ($123,900, P&L +53,902$)

## Watchlist normativa

- Blocco ADM attivo dal 27/07/2026 (Polymarket e Kalshi in lista nera, oscurati dagli ISP)
- TAR Lazio: urgenza rigettata il 05/08/2026; camera di consiglio del 25/08/2026 — esito non ancora reso pubblico alla data di questo report (verificare a ogni run)
- Betfair Italia: unico betting exchange con licenza ADM; automazione consentita via software certificato ADM (accesso API custom da verificare caso per caso)
- Fonti: ADM, Il Sole 24 Ore, Agipro, Sky TG24, Corriere della Sera

## Prossime azioni

1. Lasciare girare il watcher (GitHub Actions / VPS) per costruire lo storico
2. Ogni trade idea → prima in paper (`lab/paper.py`), mai diretto
3. Backtest delle strategie S3/S4/S5 quando il DB ha >= 2 settimane di dati
