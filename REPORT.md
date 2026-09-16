# Report predmarket-lab — 16/09/2026 15:44:35

Ultimo scan: `2026-09-16T13:44:29+00:00` UTC · ciclo n.11 · 326 mercati tracciati · 2697 snapshot · 155 alert

## Conto paper

- **Equity:** 201.24 USDC (**ROI +0.62%**)
- Cash 201.24 · posizioni aperte 0 · trade 1 (W 1 / L 0)
- Realized +1.30 · drawdown dal picco -0.6%

## Ultimi alert

- `13:44` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 6225k: candidate yield maker
- `13:44` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 4612k: candidate yield maker
- `13:44` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 3369k: candidate yield maker
- `13:44` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 718k: candidate yield maker
- `13:44` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 337k: candidate yield maker
- `13:44` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 337k: candidate yield maker
- `13:44` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 297k: candidate yield maker
- `13:44` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 292k: candidate yield maker
- `13:44` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 193k: candidate yield maker
- `13:44` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 190k: candidate yield maker
- `13:44` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 166k: candidate yield maker
- `13:44` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 166k: candidate yield maker

## Indice di inefficienza (v0)

- **3/100** — 2% dei top-50 mercati ha spread >=4 punti, 4% ha mosso >=8 punti in 1h

## Shadow signals (l'AI studia, zero capitale)

- nessun segnale ancora valutato: servono cicli del watcher

segnali aperti ora:

- `MEAN_REVERT` Guangzhou: Marat Sharipov vs Lloyd Harris — mossa +31p in 1h — ipotesi rientro eccesso
- `LONGSHOT_FADE` Counter-Strike: Just Players vs NAVI Junior - Map 2 Winner — longshot a 0.001 — ipotesi sopravvalutazione
- `ENDGAME_FAVORITE` Will Vissel Kobe win on 2026-09-16? — favorito 0.83 a fine giornata, spread 1p, vol 80k
- `MEAN_REVERT` Sao Paulo Open: Whitney Osuigwe vs Kaitlin Quevedo — mossa +16p in 1h — ipotesi rientro eccesso
- `LONGSHOT_FADE` Counter-Strike: OldMix vs EAC Extra (BO3) - United21 Playoffs — longshot a 0.001 — ipotesi sopravvalutazione
- `LONGSHOT_FADE` Will Port FC win on 2026-09-16? — longshot a 0.020 — ipotesi sopravvalutazione

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
