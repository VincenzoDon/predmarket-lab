# Report predmarket-lab — 17/09/2026 20:27:21

Ultimo scan: `2026-09-17T18:27:15+00:00` UTC · ciclo n.14 · 648 mercati tracciati · 3597 snapshot · 558 alert

## Conto paper

- **Equity:** 201.24 USDC (**ROI +0.62%**)
- Cash 201.24 · posizioni aperte 0 · trade 1 (W 1 / L 0)
- Realized +1.30 · drawdown dal picco -0.6%

## Ultimi alert

- `18:27` **MOVER_1H** — mossa +21 punti in 1h (prezzo 0.85) su 5497k vol
- `18:27` **CHIUDE_OGGI** — chiude oggi, vol 24h 5497k — finestra informativa finale
- `18:27` **CHIUDE_OGGI** — chiude oggi, vol 24h 1230k — finestra informativa finale
- `18:27` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 1061k: candidate yield maker
- `18:27` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 734k: candidate yield maker
- `18:27` **CHIUDE_OGGI** — chiude oggi, vol 24h 706k — finestra informativa finale
- `18:27` **MOVER_1H** — mossa -10 punti in 1h (prezzo 0.023) su 624k vol
- `18:27` **CHIUDE_OGGI** — chiude oggi, vol 24h 624k — finestra informativa finale
- `18:27` **MOVER_1H** — mossa -19 punti in 1h (prezzo 0.46) su 602k vol
- `18:27` **CHIUDE_OGGI** — chiude oggi, vol 24h 602k — finestra informativa finale
- `18:27` **CHIUDE_OGGI** — chiude oggi, vol 24h 553k — finestra informativa finale
- `18:27` **MOVER_1H** — mossa +12 punti in 1h (prezzo 0.71) su 492k vol

## Indice di inefficienza (v0)

- **13/100** — 4% dei top-50 mercati ha spread >=4 punti, 26% ha mosso >=8 punti in 1h

## Shadow signals (l'AI studia, zero capitale)

- **ENDGAME_FAVORITE** — 7 valutati · 85.7% hit · risultato medio +10.62%
- **LONGSHOT_FADE** — 73 valutati · 84.9% hit · risultato medio +59.63%
- **MAKER_SPREAD** — 1 valutati · 100.0% hit · risultato medio +8.00%
- **MEAN_REVERT** — 7 valutati · 28.6% hit · risultato medio -41.14%

segnali aperti ora:

- `ENDGAME_FAVORITE` Will Real Betis Balompié win on 2026-09-17? — favorito 0.84 a fine giornata, spread 1p, vol 5497k
- `LONGSHOT_FADE` Will Getafe CF win on 2026-09-17? — longshot a 0.024 — ipotesi sopravvalutazione
- `LONGSHOT_FADE` Putin out as President of Russia by December 31, 2026? — longshot a 0.045 — ipotesi sopravvalutazione
- `LONGSHOT_FADE` Will Shakhtar Donetsk win the 2026-27 UEFA Champions League Championsh — longshot a 0.002 — ipotesi sopravvalutazione
- `MEAN_REVERT` Rennes: Adrian Mannarino vs Matisse Bobichon — mossa -56p in 1h — ipotesi rientro eccesso
- `LONGSHOT_FADE` Rennes: Adrian Mannarino vs Matisse Bobichon — longshot a 0.001 — ipotesi sopravvalutazione

## Whale watch 🐋

- **Consenso**: 2 balene (Sassy-Bucket,BrotherObama) su 'Los Angeles Dodgers vs. Cincinnati Reds: O/U 9.5' — $53,879
- **Consenso**: 2 balene (BrotherObama,lllllllIlll) su 'Counter-Strike: B8 vs M80 (BO1) - Logitech G Play Connect Gr' — $51,002
- **Consenso**: 2 balene (Sassy-Bucket,BrotherObama) su 'San Diego Padres vs. Colorado Rockies: O/U 10.5' — $49,913
- halvanicus: Will Real Betis Balompié win on 2026-09-17? @ 0.84 ($2,763,883, P&L +633,053$)
- JnStrtPrdctnMrkts: Will Ethereum dip to $1,500 by December 31, 2026? @ 0.86 ($865,555, P&L +242,774$)
- JnStrtPrdctnMrkts: Will Bitcoin dip to $55,000 by December 31, 2026? @ 0.81 ($578,121, P&L +198,700$)
- JnStrtPrdctnMrkts: Will Bitcoin dip to $50,000 by December 31, 2026? @ 0.88 ($545,562, P&L +128,336$)
- JnStrtPrdctnMrkts: Will Ethereum dip to $1,250 by December 31, 2026? @ 0.92 ($362,494, P&L +60,920$)

## Watchlist normativa

- Blocco ADM attivo dal 27/07/2026 (Polymarket e Kalshi in lista nera, oscurati dagli ISP)
- TAR Lazio: urgenza rigettata il 05/08/2026; camera di consiglio del 25/08/2026 — esito non ancora reso pubblico alla data di questo report (verificare a ogni run)
- Betfair Italia: unico betting exchange con licenza ADM; automazione consentita via software certificato ADM (accesso API custom da verificare caso per caso)
- Fonti: ADM, Il Sole 24 Ore, Agipro, Sky TG24, Corriere della Sera

## Prossime azioni

1. Lasciare girare il watcher (GitHub Actions / VPS) per costruire lo storico
2. Ogni trade idea → prima in paper (`lab/paper.py`), mai diretto
3. Backtest delle strategie S3/S4/S5 quando il DB ha >= 2 settimane di dati
