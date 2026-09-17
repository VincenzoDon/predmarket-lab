# Report predmarket-lab — 17/09/2026 10:01:34

Ultimo scan: `2026-09-17T08:01:28+00:00` UTC · ciclo n.12 · 493 mercati tracciati · 2997 snapshot · 269 alert

## Conto paper

- **Equity:** 201.24 USDC (**ROI +0.62%**)
- Cash 201.24 · posizioni aperte 0 · trade 1 (W 1 / L 0)
- Realized +1.30 · drawdown dal picco -0.6%

## Ultimi alert

- `08:01` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 968k: candidate yield maker
- `08:01` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 829k: candidate yield maker
- `08:01` **CHIUDE_OGGI** — chiude oggi, vol 24h 820k — finestra informativa finale
- `08:01` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 672k: candidate yield maker
- `08:01` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 664k: candidate yield maker
- `08:01` **SPREAD_LARGO** — bid 0.47/ask 0.58 = 11 punti su 337k vol 24h — candidata maker
- `08:01` **MOVER_1H** — mossa -10 punti in 1h (prezzo 0.47) su 337k vol
- `08:01` **CHIUDE_OGGI** — chiude oggi, vol 24h 231k — finestra informativa finale
- `08:01` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 156k: candidate yield maker
- `08:01` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 154k: candidate yield maker
- `08:01` **CHIUDE_OGGI** — chiude oggi, vol 24h 154k — finestra informativa finale
- `08:01` **CHIUDE_OGGI** — chiude oggi, vol 24h 137k — finestra informativa finale

## Indice di inefficienza (v0)

- **3/100** — 4% dei top-50 mercati ha spread >=4 punti, 2% ha mosso >=8 punti in 1h

## Shadow signals (l'AI studia, zero capitale)

- nessun segnale ancora valutato: servono cicli del watcher

segnali aperti ora:

- `MEAN_REVERT` Valencia: Guiomar Maristany vs Marina Bassols Ribera — mossa -10p in 1h — ipotesi rientro eccesso
- `MAKER_SPREAD` Valencia: Guiomar Maristany vs Marina Bassols Ribera — spread 11p — ipotesi cattura maker
- `LONGSHOT_FADE` Will Ruben Gallego win the 2028 Democratic presidential nomination? — longshot a 0.001 — ipotesi sopravvalutazione
- `LONGSHOT_FADE` Will Erling Haaland win the 2026 Ballon d'Or? — longshot a 0.003 — ipotesi sopravvalutazione
- `LONGSHOT_FADE` Will Elissa Slotkin win the 2028 Democratic presidential nomination? — longshot a 0.002 — ipotesi sopravvalutazione
- `LONGSHOT_FADE` Will 1 Fed rate cut happen in 2026? — longshot a 0.017 — ipotesi sopravvalutazione

## Whale watch 🐋

- **Consenso**: 2 balene (HMLSF,RN1) su 'Valencia: Guiomar Maristany vs Marina Bassols Ribera' — $40,931
- Sassy-Bucket: Kansas City Royals vs. Houston Astros @ 1.00 ($166,695, P&L +101,684$)
- Sassy-Bucket: San Francisco Giants vs. St. Louis Cardinals: O/U 8.5 @ 1.00 ($86,945, P&L +45,217$)
- Sassy-Bucket: Athletics vs. Tampa Bay Rays @ 1.00 ($75,951, P&L +28,861$)
- Sassy-Bucket: Milwaukee Brewers vs. Pittsburgh Pirates @ 1.00 ($75,400, P&L +33,932$)
- Sassy-Bucket: Philadelphia Phillies vs. Washington Nationals: O/U 8.5 @ 1.00 ($52,279, P&L +28,231$)

## Watchlist normativa

- Blocco ADM attivo dal 27/07/2026 (Polymarket e Kalshi in lista nera, oscurati dagli ISP)
- TAR Lazio: urgenza rigettata il 05/08/2026; camera di consiglio del 25/08/2026 — esito non ancora reso pubblico alla data di questo report (verificare a ogni run)
- Betfair Italia: unico betting exchange con licenza ADM; automazione consentita via software certificato ADM (accesso API custom da verificare caso per caso)
- Fonti: ADM, Il Sole 24 Ore, Agipro, Sky TG24, Corriere della Sera

## Prossime azioni

1. Lasciare girare il watcher (GitHub Actions / VPS) per costruire lo storico
2. Ogni trade idea → prima in paper (`lab/paper.py`), mai diretto
3. Backtest delle strategie S3/S4/S5 quando il DB ha >= 2 settimane di dati
