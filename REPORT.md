# Report predmarket-lab — 27/09/2026 03:55:36

🟢 **Salute dati:** dati freschi: ultimo scan 7 min fa

Ultimo scan: `2026-09-27T01:48:29+00:00` UTC · ciclo n.75 · 4469 mercati tracciati · 21830 snapshot · 10676 alert

## Conto paper

- **Equity:** 201.24 USDC (**ROI +0.62%**)
- Cash 201.24 · posizioni aperte 0 · trade 1 (W 1 / L 0)
- Realized +1.30 · drawdown dal picco -0.6%

## Ultimi alert

- `01:48` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 1134k: candidate yield maker
- `01:48` **MOVER_1H** — mossa +26 punti in 1h (prezzo 0.79) su 1134k vol
- `01:48` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 667k: candidate yield maker
- `01:48` **MOVER_1H** — mossa -20 punti in 1h (prezzo 0.09) su 667k vol
- `01:48` **MOVER_1H** — mossa +73 punti in 1h (prezzo 0.999) su 570k vol
- `01:48` **CHIUDE_OGGI** — chiude oggi, vol 24h 570k — finestra informativa finale
- `01:48` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 542k: candidate yield maker
- `01:48` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 454k: candidate yield maker
- `01:48` **MOVER_1H** — mossa +19 punti in 1h (prezzo 0.32) su 454k vol
- `01:48` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 377k: candidate yield maker
- `01:48` **SPREAD_LARGO** — bid 0.77/ask 0.86 = 9 punti su 377k vol 24h — candidata maker
- `01:48` **MOVER_1H** — mossa +34 punti in 1h (prezzo 0.6) su 377k vol

## Indice di inefficienza (v0)

- **25/100** — 12% dei top-50 mercati ha spread >=4 punti, 44% ha mosso >=8 punti in 1h

## Shadow signals (l'AI studia, zero capitale)

- **ENDGAME_FAVORITE** — 138 valutati · 84.1% hit · risultato medio +0.89%
- **LONGSHOT_FADE** — 1686 valutati · 82.6% hit · risultato medio +2.67%
- **MAKER_SPREAD** — 16 valutati · 81.2% hit · risultato medio +10.51%
- **MEAN_REVERT** — 409 valutati · 20.3% hit · risultato medio -5.75%

segnali aperti ora:

- `MEAN_REVERT` Oregon vs. USC — mossa +26p in 1h — ipotesi rientro eccesso
- `MEAN_REVERT` Texas A&M vs. LSU — mossa -20p in 1h — ipotesi rientro eccesso
- `LONGSHOT_FADE` Texas A&M vs. LSU — longshot a 0.045 — ipotesi sopravvalutazione
- `MEAN_REVERT` Missouri vs. Mississippi State — mossa +19p in 1h — ipotesi rientro eccesso
- `MEAN_REVERT` Spread: LSU (-8.5) — mossa +34p in 1h — ipotesi rientro eccesso
- `MAKER_SPREAD` Spread: LSU (-8.5) — spread 9p — ipotesi cattura maker

## Whale watch 🐋

- **Consenso**: 2 balene (HomeRunHazard,nigiri99) su 'Oregon vs. USC' — $137,587
- **Consenso**: 2 balene (HomeRunHazard,nigiri99) su 'Spread: Chiefs (-3.5)' — $84,230
- **Consenso**: 2 balene (nigiri99,0x3DFb153c197D4C19D3B31c1ecD2c7B6860eeabAf-1722957908185) su 'Oregon vs. USC: O/U 60.5' — $64,711
- **Consenso**: 2 balene (HomeRunHazard,0x3DFb153c197D4C19D3B31c1ecD2c7B6860eeabAf-1722957908185) su 'Oklahoma State vs. West Virginia: O/U 59.5' — $62,491
- matanovik: UFC Fight Night: Ilimbek Akylbek Uulu vs. Mehemmedeli Osmanl @ 1.00 ($106,587, P&L +76,683$)
- HomeRunHazard: Spread: Cowboys (-3.5) @ 0.74 ($94,756, P&L -507$)
- HomeRunHazard: Oregon vs. USC @ 0.62 ($85,093, P&L -1,952$)
- HomeRunHazard: Spread: Steelers (-3.5) @ 0.72 ($63,898, P&L -209$)
- nigiri99: James Madison vs. Old Dominion @ 1.00 ($62,896, P&L +19,493$)

## Shadow Detector v1 🕵️ (scoring wallet — shadow, zero ordini)

Punteggio "insider-simiglianza" dallo storico on-chain (win-rate, profitto, convinzione, nicchia). Radar da validare nel tempo, non un invito a copiare.

- **JnStrtPrdctnMrkts** — score 91/100 · win 79% · 150 osservazioni su 15 mercati
- **0x361b16e3ddfe1d415d41008daac2631d94ab74fe** — score 88/100 · win 100% · 19 osservazioni su 19 mercati
- **Kch-Temp** — score 85/100 · win 91% · 23 osservazioni su 18 mercati
- **0x2c335066FE58fe9237c3d3Dc7b275C2a034a0563-1759935795465** — score 83/100 · win 75% · 231 osservazioni su 55 mercati
- **Tiger200** — score 81/100 · win 75% · 4 osservazioni su 3 mercati
- **UpTheBlues** — score 80/100 · win 92% · 105 osservazioni su 79 mercati
- **BreakTheBank** — score 77/100 · win 59% · 165 osservazioni su 27 mercati
- **surfandturf** — score 76/100 · win 63% · 35 osservazioni su 9 mercati

ingressi sospetti recenti (SHADOW_ENTRY):

- `09-27T01:48` wallet informato-simile 0x3DFb153c197D4C19D3B31c1ecD2c7B6860eeabAf-1722957908185 (score 72/100, win 68%) ENTRA su 'Spread: Florida Atlantic (-11.5)' — da osservare (shadow, zero ordini)
- `09-27T01:48` wallet informato-simile HomeRunHazard (score 68/100, win 56%) ENTRA su 'Kansas State vs. Cincinnati: O/U 55.5' — da osservare (shadow, zero ordini)
- `09-27T01:48` wallet informato-simile HomeRunHazard (score 68/100, win 56%) ENTRA su 'Oklahoma State vs. West Virginia' — da osservare (shadow, zero ordini)
- `09-27T01:48` wallet informato-simile matanovik (score 75/100, win 80%) ENTRA su 'Oregon vs. USC: O/U 58.5' — da osservare (shadow, zero ordini)
- `09-27T01:48` wallet informato-simile HomeRunHazard (score 68/100, win 56%) ENTRA su 'Spread: Fresno State (-12.5)' — da osservare (shadow, zero ordini)
- `09-27T01:48` wallet informato-simile matanovik (score 75/100, win 80%) ENTRA su 'Spread: Alabama (-14.5)' — da osservare (shadow, zero ordini)

## Watchlist normativa

- Blocco ADM attivo dal 27/07/2026 (Polymarket e Kalshi in lista nera, oscurati dagli ISP)
- TAR Lazio: urgenza rigettata il 05/08/2026; camera di consiglio del 25/08/2026 — esito non ancora reso pubblico alla data di questo report (verificare a ogni run)
- Betfair Italia: unico betting exchange con licenza ADM; automazione consentita via software certificato ADM (accesso API custom da verificare caso per caso)
- Fonti: ADM, Il Sole 24 Ore, Agipro, Sky TG24, Corriere della Sera

## Prossime azioni

1. Lasciare girare il watcher (GitHub Actions / VPS) per costruire lo storico
2. Ogni trade idea → prima in paper (`lab/paper.py`), mai diretto
3. Backtest delle strategie S3/S4/S5 quando il DB ha >= 2 settimane di dati
