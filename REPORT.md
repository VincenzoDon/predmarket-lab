# Report predmarket-lab — 18/09/2026 15:08:17

🟡 **Salute dati:** dati un po' vecchi: ultimo scan 1.3 ore fa

Ultimo scan: `2026-09-18T11:49:43+00:00` UTC · ciclo n.19 · 934 mercati tracciati · 5095 snapshot · 1265 alert

## Conto paper

- **Equity:** 201.24 USDC (**ROI +0.62%**)
- Cash 201.24 · posizioni aperte 0 · trade 1 (W 1 / L 0)
- Realized +1.30 · drawdown dal picco -0.6%

## Ultimi alert

- `11:49` **CHIUDE_OGGI** — chiude oggi, vol 24h 1346k — finestra informativa finale
- `11:49` **MOVER_1H** — mossa -42 punti in 1h (prezzo 0.001) su 1280k vol
- `11:49` **CHIUDE_OGGI** — chiude oggi, vol 24h 1280k — finestra informativa finale
- `11:49` **MOVER_1H** — mossa -22 punti in 1h (prezzo 0.19) su 939k vol
- `11:49` **CHIUDE_OGGI** — chiude oggi, vol 24h 939k — finestra informativa finale
- `11:49` **MOVER_1H** — mossa -10 punti in 1h (prezzo 0.32) su 906k vol
- `11:49` **CHIUDE_OGGI** — chiude oggi, vol 24h 906k — finestra informativa finale
- `11:49` **CHIUDE_OGGI** — chiude oggi, vol 24h 899k — finestra informativa finale
- `11:49` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 678k: candidate yield maker
- `11:49` **CHIUDE_OGGI** — chiude oggi, vol 24h 637k — finestra informativa finale
- `11:49` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 538k: candidate yield maker
- `11:49` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 460k: candidate yield maker

## Indice di inefficienza (v0)

- **7/100** — 0% dei top-50 mercati ha spread >=4 punti, 18% ha mosso >=8 punti in 1h

## Shadow signals (l'AI studia, zero capitale)

- **ENDGAME_FAVORITE** — 26 valutati · 92.3% hit · risultato medio +7.71%
- **LONGSHOT_FADE** — 185 valutati · 87.6% hit · risultato medio +24.05%
- **MAKER_SPREAD** — 2 valutati · 100.0% hit · risultato medio +9.00%
- **MEAN_REVERT** — 37 valutati · 13.5% hit · risultato medio -53.39%

segnali aperti ora:

- `LONGSHOT_FADE` LoL: Team WE vs JD Gaming - Game 3 Winner — longshot a 0.001 — ipotesi sopravvalutazione
- `LONGSHOT_FADE` LoL: Team WE vs JD Gaming - Game 2 Winner — longshot a 0.001 — ipotesi sopravvalutazione
- `MEAN_REVERT` Guangzhou: Elias Ymer vs Marat Sharipov — mossa -14p in 1h — ipotesi rientro eccesso
- `LONGSHOT_FADE` Guangzhou: Elias Ymer vs Marat Sharipov — longshot a 0.001 — ipotesi sopravvalutazione
- `MEAN_REVERT` Ljubljana: Samira De Stefano vs Alice Tubello — mossa +46p in 1h — ipotesi rientro eccesso
- `LONGSHOT_FADE` Map Handicap: MOUZ (-1.5) vs Natus Vincere (+1.5) — longshot a 0.001 — ipotesi sopravvalutazione

## Whale watch 🐋

- JnStrtPrdctnMrkts: Will Ethereum dip to $1,500 by December 31, 2026? @ 0.88 ($881,593, P&L +258,812$)
- JnStrtPrdctnMrkts: Will Bitcoin dip to $55,000 by December 31, 2026? @ 0.83 ($592,308, P&L +212,887$)
- JnStrtPrdctnMrkts: Will Bitcoin dip to $50,000 by December 31, 2026? @ 0.91 ($564,267, P&L +147,041$)
- JnStrtPrdctnMrkts: Will Ethereum dip to $1,250 by December 31, 2026? @ 0.92 ($362,494, P&L +60,920$)
- kindar: Will United Russia (ER) gain the most seats in the next Russ @ 0.78 ($328,912, P&L +14,523$)

## Shadow Detector v1 🕵️ (scoring wallet — shadow, zero ordini)

Punteggio "insider-simiglianza" dallo storico on-chain (win-rate, profitto, convinzione, nicchia). Radar da validare nel tempo, non un invito a copiare.

- **JnStrtPrdctnMrkts** — score 88/100 · win 72% · 75 osservazioni su 15 mercati
- **Sassy-Bucket** — score 80/100 · win 88% · 17 osservazioni su 15 mercati
- **Donkey14** — score 76/100 · win 80% · 5 osservazioni su 5 mercati
- **HMLSF** — score 75/100 · win 76% · 17 osservazioni su 9 mercati
- **BrotherObama** — score 72/100 · win 71% · 7 osservazioni su 6 mercati
- **kindar** — score 70/100 · win 33% · 18 osservazioni su 4 mercati
- **halvanicus** — score 69/100 · win 40% · 5 osservazioni su 3 mercati
- **0xdc3E831cad** — score 68/100 · win 56% · 90 osservazioni su 15 mercati

## Watchlist normativa

- Blocco ADM attivo dal 27/07/2026 (Polymarket e Kalshi in lista nera, oscurati dagli ISP)
- TAR Lazio: urgenza rigettata il 05/08/2026; camera di consiglio del 25/08/2026 — esito non ancora reso pubblico alla data di questo report (verificare a ogni run)
- Betfair Italia: unico betting exchange con licenza ADM; automazione consentita via software certificato ADM (accesso API custom da verificare caso per caso)
- Fonti: ADM, Il Sole 24 Ore, Agipro, Sky TG24, Corriere della Sera

## Prossime azioni

1. Lasciare girare il watcher (GitHub Actions / VPS) per costruire lo storico
2. Ogni trade idea → prima in paper (`lab/paper.py`), mai diretto
3. Backtest delle strategie S3/S4/S5 quando il DB ha >= 2 settimane di dati
