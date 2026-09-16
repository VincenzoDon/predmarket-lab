# Report predmarket-lab — 16/09/2026 15:14:41

Ultimo scan: `2026-09-16T13:14:35+00:00` UTC · ciclo n.8 · 312 mercati tracciati · 1797 snapshot · 48 alert

## Conto paper

- **Equity:** 201.24 USDC (**ROI +0.62%**)
- Cash 201.24 · posizioni aperte 0 · trade 1 (W 1 / L 0)
- Realized +1.30 · drawdown dal picco -0.6%

## Ultimi alert

- `13:14` **SPREAD_LARGO** — bid 0.35/ask 0.47 = 12 punti su 54k vol 24h — candidata maker
- `13:12` **CHIUDE_OGGI** — chiude oggi, vol 24h 103k — finestra informativa finale
- `13:12` **MOVER_1H** — mossa +11 punti in 1h (prezzo 0.81) su 76k vol
- `13:12` **SPREAD_LARGO** — bid 0.11/ask 0.18 = 7 punti su 74k vol 24h — candidata maker
- `13:12` **MOVER_1H** — mossa -64 punti in 1h (prezzo 0.18) su 74k vol
- `13:12` **MOVER_1H** — mossa -12 punti in 1h (prezzo 0.2) su 64k vol
- `13:12` **MOVER_1H** — mossa +14 punti in 1h (prezzo 0.54) su 36k vol
- `13:12` **MOVER_1H** — mossa +10 punti in 1h (prezzo 0.53) su 25k vol
- `13:12` **MOVER_1H** — mossa -45 punti in 1h (prezzo 0.01) su 22k vol
- `13:12` **MOVER_1H** — mossa -22 punti in 1h (prezzo 0.34) su 20k vol
- `12:47` **MOVER_1H** — mossa -10 punti in 1h (prezzo 0.29) su 95k vol
- `12:47` **MOVER_1H** — mossa -12 punti in 1h (prezzo 0.49) su 89k vol

## Shadow signals (l'AI studia, zero capitale)

- nessun segnale ancora valutato: servono cicli del watcher

segnali aperti ora:

- `MAKER_SPREAD` KBO: KT Wiz vs. Hanwha Eagles — spread 12p — ipotesi cattura maker
- `MAKER_SPREAD` Will the price of Ethereum be above $2,400 on September 16? — spread 11p — ipotesi cattura maker
- `LONGSHOT_FADE` Will the Fed increase interest rates by 50+ bps after the September 20 — longshot a 0.007 — ipotesi sopravvalutazione
- `LONGSHOT_FADE` Will the Fed decrease interest rates by 25 bps after the September 202 — longshot a 0.002 — ipotesi sopravvalutazione
- `ENDGAME_FAVORITE` Will the Fed increase interest rates by 25 bps after the September 202 — favorito 0.89 a fine giornata, spread 1p, vol 4825k
- `LONGSHOT_FADE` Will the Fed decrease interest rates by 50+ bps after the September 20 — longshot a 0.001 — ipotesi sopravvalutazione

## Whale watch 🐋

- 0xdc3E831cad: Will the U.S. invade Iran before 2027? @ 0.82 ($79,418, P&L +19,579$)
- 0xdc3E831cad: Will the Iranian regime fall before 2027? @ 0.92 ($9,150, P&L +1,943$)
- 0xdc3E831cad: Lee Jae-myung arrested before 2027? @ 0.93 ($7,478, P&L +1,009$)
- 0xdc3E831cad: Billionaire one-time wealth tax passes in California electio @ 0.68 ($5,588, P&L +621$)
- 0xdc3E831cad: Will AI solve 0 more Millennium Prize Problems in 2026? @ 0.51 ($3,233, P&L +1,707$)

## Watchlist normativa

- Blocco ADM attivo dal 27/07/2026 (Polymarket e Kalshi in lista nera, oscurati dagli ISP)
- TAR Lazio: urgenza rigettata il 05/08/2026; camera di consiglio del 25/08/2026 — esito non ancora reso pubblico alla data di questo report (verificare a ogni run)
- Betfair Italia: unico betting exchange con licenza ADM; automazione consentita via software certificato ADM (accesso API custom da verificare caso per caso)
- Fonti: ADM, Il Sole 24 Ore, Agipro, Sky TG24, Corriere della Sera

## Prossime azioni

1. Lasciare girare il watcher (GitHub Actions / VPS) per costruire lo storico
2. Ogni trade idea → prima in paper (`lab/paper.py`), mai diretto
3. Backtest delle strategie S3/S4/S5 quando il DB ha >= 2 settimane di dati
