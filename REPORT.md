# Report predmarket-lab — 18/09/2026 08:40:14

Ultimo scan: `2026-09-18T06:40:08+00:00` UTC · ciclo n.18 · 878 mercati tracciati · 4795 snapshot · 1119 alert

## Conto paper

- **Equity:** 201.24 USDC (**ROI +0.62%**)
- Cash 201.24 · posizioni aperte 0 · trade 1 (W 1 / L 0)
- Realized +1.30 · drawdown dal picco -0.6%

## Ultimi alert

- `06:40` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 597k: candidate yield maker
- `06:40` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 530k: candidate yield maker
- `06:40` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 461k: candidate yield maker
- `06:40` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 434k: candidate yield maker
- `06:40` **CHIUDE_OGGI** — chiude oggi, vol 24h 394k — finestra informativa finale
- `06:40` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 342k: candidate yield maker
- `06:40` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 283k: candidate yield maker
- `06:40` **CHIUDE_OGGI** — chiude oggi, vol 24h 261k — finestra informativa finale
- `06:40` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 215k: candidate yield maker
- `06:40` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 180k: candidate yield maker
- `06:40` **CHIUDE_OGGI** — chiude oggi, vol 24h 180k — finestra informativa finale
- `06:40` **REWARDS_MARKET** — liquidity rewards attivi — vol 24h 177k: candidate yield maker

## Indice di inefficienza (v0)

- **2/100** — 0% dei top-50 mercati ha spread >=4 punti, 6% ha mosso >=8 punti in 1h

## Shadow signals (l'AI studia, zero capitale)

- **ENDGAME_FAVORITE** — 7 valutati · 85.7% hit · risultato medio +10.62%
- **LONGSHOT_FADE** — 77 valutati · 81.8% hit · risultato medio +57.01%
- **MAKER_SPREAD** — 2 valutati · 100.0% hit · risultato medio +9.00%
- **MEAN_REVERT** — 8 valutati · 25.0% hit · risultato medio -36.00%

segnali aperti ora:

- `LONGSHOT_FADE` Will Leeds United win the 2026-27 English Premier League (EPL) Champio — longshot a 0.002 — ipotesi sopravvalutazione
- `MEAN_REVERT` Phan Thiet 4: Rodrigo Pacheco vs Philip Sekulic — mossa +16p in 1h — ipotesi rientro eccesso
- `ENDGAME_FAVORITE` Counter-Strike: Black Phoenix vs Lavked (BO3) - CCT Europe Series #9 G — favorito 0.76 a fine giornata, spread 1p, vol 123k
- `LONGSHOT_FADE` Kent State vs. Ohio State — longshot a 0.002 — ipotesi sopravvalutazione
- `MEAN_REVERT` W35 Shenyang: Kristiana Sidorova vs Yufei Ren — mossa +39p in 1h — ipotesi rientro eccesso
- `ENDGAME_FAVORITE` Will Elon Musk post 180-199 tweets from September 11 to September 18,  — favorito 0.89 a fine giornata, spread 1p, vol 78k

## Whale watch 🐋

- kindar: Will United Russia (ER) gain the most seats in the next Russ @ 0.77 ($366,842, P&L +11,614$)
- Herdonia: Bengals vs. Texans @ 0.42 ($71,018, P&L -600$)
- kindar: Russia Elections: United Russia Wins Every Region? @ 0.41 ($22,385, P&L -2,615$)
- Herdonia: Spread: BAL (-8.5) @ 0.49 ($22,169, P&L -576$)
- kindar: Will New People (NL) gain the most seats in the next Russian @ 0.81 ($18,716, P&L -1,284$)

## Watchlist normativa

- Blocco ADM attivo dal 27/07/2026 (Polymarket e Kalshi in lista nera, oscurati dagli ISP)
- TAR Lazio: urgenza rigettata il 05/08/2026; camera di consiglio del 25/08/2026 — esito non ancora reso pubblico alla data di questo report (verificare a ogni run)
- Betfair Italia: unico betting exchange con licenza ADM; automazione consentita via software certificato ADM (accesso API custom da verificare caso per caso)
- Fonti: ADM, Il Sole 24 Ore, Agipro, Sky TG24, Corriere della Sera

## Prossime azioni

1. Lasciare girare il watcher (GitHub Actions / VPS) per costruire lo storico
2. Ogni trade idea → prima in paper (`lab/paper.py`), mai diretto
3. Backtest delle strategie S3/S4/S5 quando il DB ha >= 2 settimane di dati
