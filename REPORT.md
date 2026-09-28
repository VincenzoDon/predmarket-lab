# Report predmarket-lab — 28/09/2026 04:07:22

🟢 **Salute dati:** dati freschi: ultimo scan 9 min fa

Ultimo scan: `2026-09-28T01:58:51+00:00` UTC · ciclo n.81 · 4968 mercati tracciati · 23629 snapshot · 12047 alert

## Conto paper

- **Equity:** 201.24 USDC (**ROI +0.62%**)
- Cash 201.24 · posizioni aperte 0 · trade 1 (W 1 / L 0)
- Realized +1.30 · drawdown dal picco -0.6%

## Ultimi alert

- `01:58` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 5648k: candidate yield maker
- `01:58` **MOVER_1H** — mossa +23 punti in 1h (prezzo 0.89) su 5648k vol
- `01:58` **CHIUDE_OGGI** — chiude oggi, vol 24h 5648k — finestra informativa finale
- `01:58` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 1496k: candidate yield maker
- `01:58` **MOVER_1H** — mossa +26 punti in 1h (prezzo 0.82) su 1496k vol
- `01:58` **CHIUDE_OGGI** — chiude oggi, vol 24h 1496k — finestra informativa finale
- `01:58` **MOVER_1H** — mossa -24 punti in 1h (prezzo 0.2) su 971k vol
- `01:58` **CHIUDE_OGGI** — chiude oggi, vol 24h 971k — finestra informativa finale
- `01:58` **MOVER_1H** — mossa +23 punti in 1h (prezzo 0.85) su 888k vol
- `01:58` **CHIUDE_OGGI** — chiude oggi, vol 24h 888k — finestra informativa finale
- `01:58` **MOVER_1H** — mossa -26 punti in 1h (prezzo 0.19) su 397k vol
- `01:58` **CHIUDE_OGGI** — chiude oggi, vol 24h 397k — finestra informativa finale

## Indice di inefficienza (v0)

- **18/100** — 10% dei top-50 mercati ha spread >=4 punti, 30% ha mosso >=8 punti in 1h

## Shadow signals (l'AI studia, zero capitale)

- **ENDGAME_FAVORITE** — 163 valutati · 83.4% hit · risultato medio +0.29%
- **LONGSHOT_FADE** — 1959 valutati · 83.3% hit · risultato medio +2.37%
- **MAKER_SPREAD** — 16 valutati · 81.2% hit · risultato medio +10.51%
- **MEAN_REVERT** — 482 valutati · 18.7% hit · risultato medio -15.80%

segnali aperti ora:

- `ENDGAME_FAVORITE` Rams vs. Broncos — favorito 0.89 a fine giornata, spread 1p, vol 5648k
- `ENDGAME_FAVORITE` Spread: Rams (-1.5) — favorito 0.87 a fine giornata, spread 2p, vol 1496k
- `ENDGAME_FAVORITE` Spread: Rams (-2.5) — favorito 0.84 a fine giornata, spread 1p, vol 888k
- `LONGSHOT_FADE` Spread: Broncos (-3.5) — longshot a 0.050 — ipotesi sopravvalutazione
- `ENDGAME_FAVORITE` Spread: Rams (-3.5) — favorito 0.81 a fine giornata, spread 1p, vol 317k
- `MAKER_SPREAD` Rams vs. Broncos: O/U 50.5 — spread 51p — ipotesi cattura maker

## Whale watch 🐋

- **Consenso**: 5 balene (0x2c335066FE58fe9237c3d3Dc7b275C2a034a0563-1759935795465,HomeRunHazard,surfandturf,RN1,wr0ngw4yb3tt0r) su 'Rams vs. Broncos' — $1,773,544
- **Consenso**: 3 balene (HomeRunHazard,RN1,wr0ngw4yb3tt0r) su 'Spread: Rams (-1.5)' — $323,427
- **Consenso**: 2 balene (HomeRunHazard,RN1) su 'Spread: Broncos (-3.5)' — $156,958
- **Consenso**: 4 balene (HomeRunHazard,surfandturf,RN1,wr0ngw4yb3tt0r) su 'Rams vs. Broncos: O/U 44.5' — $142,871
- surfandturf: Rams vs. Broncos @ 0.89 ($907,125, P&L +391,407$)
- 0x2c335066FE58fe9237c3d3Dc7b275C2a034a0563-1759935795465: Rams vs. Broncos @ 0.89 ($370,704, P&L +149,921$)
- wr0ngw4yb3tt0r: Spread: Rams (-1.5) @ 0.86 ($243,013, P&L +108,591$)
- wr0ngw4yb3tt0r: Rams vs. Broncos @ 0.89 ($238,873, P&L +74,310$)
- HomeRunHazard: Spread: Broncos (-3.5) @ 0.95 ($151,279, P&L +44,414$)

## Shadow Detector v1 🕵️ (scoring wallet — shadow, zero ordini)

Punteggio "insider-simiglianza" dallo storico on-chain (win-rate, profitto, convinzione, nicchia). Radar da validare nel tempo, non un invito a copiare.

- **JnStrtPrdctnMrkts** — score 91/100 · win 79% · 150 osservazioni su 15 mercati
- **0x361b16e3ddfe1d415d41008daac2631d94ab74fe** — score 88/100 · win 100% · 19 osservazioni su 19 mercati
- **Kch-Temp** — score 86/100 · win 94% · 33 osservazioni su 28 mercati
- **0x2c335066FE58fe9237c3d3Dc7b275C2a034a0563-1759935795465** — score 84/100 · win 76% · 246 osservazioni su 63 mercati
- **Tiger200** — score 81/100 · win 75% · 4 osservazioni su 3 mercati
- **UpTheBlues** — score 80/100 · win 92% · 105 osservazioni su 79 mercati
- **surfandturf** — score 79/100 · win 63% · 41 osservazioni su 11 mercati
- **BreakTheBank** — score 77/100 · win 59% · 165 osservazioni su 27 mercati

ingressi sospetti recenti (SHADOW_ENTRY):

- `09-28T01:58` wallet informato-simile 0x2c335066FE58fe9237c3d3Dc7b275C2a034a0563-1759935795465 (score 84/100, win 76%) ENTRA su 'Japan Open Tennis Championships, Qualification: Ri' — da osservare (shadow, zero ordini)
- `09-28T01:58` wallet informato-simile 0x2c335066FE58fe9237c3d3Dc7b275C2a034a0563-1759935795465 (score 84/100, win 76%) ENTRA su 'Will Club León FC win on 2026-09-27?' — da osservare (shadow, zero ordini)
- `09-28T01:58` wallet informato-simile 0x2c335066FE58fe9237c3d3Dc7b275C2a034a0563-1759935795465 (score 84/100, win 76%) ENTRA su 'Rams vs. Broncos' — da osservare (shadow, zero ordini)
- `09-28T01:58` wallet informato-simile surfandturf (score 79/100, win 63%) ENTRA su 'Rams vs. Broncos' — da osservare (shadow, zero ordini)
- `09-28T01:58` wallet informato-simile RN1 (score 72/100, win 83%) ENTRA su 'Rams vs. Broncos' — da osservare (shadow, zero ordini)
- `09-28T01:58` wallet informato-simile wr0ngw4yb3tt0r (score 73/100, win 70%) ENTRA su 'Rams vs. Broncos: 1H Moneyline' — da osservare (shadow, zero ordini)

## Watchlist normativa

- Blocco ADM attivo dal 27/07/2026 (Polymarket e Kalshi in lista nera, oscurati dagli ISP)
- TAR Lazio: urgenza rigettata il 05/08/2026; camera di consiglio del 25/08/2026 — esito non ancora reso pubblico alla data di questo report (verificare a ogni run)
- Betfair Italia: unico betting exchange con licenza ADM; automazione consentita via software certificato ADM (accesso API custom da verificare caso per caso)
- Fonti: ADM, Il Sole 24 Ore, Agipro, Sky TG24, Corriere della Sera

## Prossime azioni

1. Lasciare girare il watcher (GitHub Actions / VPS) per costruire lo storico
2. Ogni trade idea → prima in paper (`lab/paper.py`), mai diretto
3. Backtest delle strategie S3/S4/S5 quando il DB ha >= 2 settimane di dati
