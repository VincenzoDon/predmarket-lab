# STATUS_IT.md — Dove siamo davvero (aggiornato al 17/09/2026)

## Stato in una riga
Lab operativo e autonomo: 5 agenti attivi (SCOUT, ANALISTA, RISK, SIGNAL ENGINE, WHALE WATCHER),
~1.500 snapshot storici, 117+ segnali shadow, prime evidenze reali raccolte. Zero soldi rischiati.
**Non esiste ancora nessuna esecuzione di ordini reali, per scelta (vedi rischi).**

## Cosa funziona VERIFICATO CON CODICE
- `run_scan.py` — scanner live 4 mode (closing/arb/spreads/movers/book/fees) su API pubbliche
- `watcher.py` — ciclo autonomo: 300 mercati/ciclo (paginato) → SQLite → alert dedupe → dashboard+report
- Signal engine shadow: ENDGAME_FAVORITE / MEAN_REVERT / LONGSHOT_FADE / MAKER_SPREAD, valutati su risoluzione reale
- Whale watcher: leaderboard + posizioni top-5 + alert consenso (fixare: vedi sotto)
- Tracking liquidity rewards (97/300 mercati con rewards attivi al 16/09)
- Paper trading engine (fee+slippage) — usato 1 volta demo, ROI +0.62%
- Git: repo locale con commit fino a v0.5 (NON ancora pushato su GitHub: serve sessione collegata)

## Prime evidenze (giorno 1, 16→17/09, 46 mercati risolti)
- **ENDGAME_FAVORITE: 6/6 vinte, media +13,3%** (Fed 25bps +13,0%, Barcellona +9,3%, Leverkusen +9,3%, Bitcoin>74k +4,4%, Musk tweet +24,2%, Vissel Kobe +19,8%) ← ipotesi più promettente
- **LONGSHOT_FADE: 34/34 vinte** MA attenzione: il +100% mostrato è un artefatto della metrica
  (misura il movimento del lato YES, non il P&L reale del fade). P&L reale per vincita = ep/(1-ep)
  ≈ +0,1%…+4,5%; una sola loss = -100% della posizione. Va fixata la metrica in `lab/signals.py`.
- **MEAN_REVERT: 1/6, media -51,5% → STRATEGIA BOCCIATA nella v0** (le mosse 1h dei mercati
  live tendono a CONTINUARE, non a rientrare). Da rivedere: forse invertirla (momentum) o cancellarla.

## Prossimo UNICO passo (dedotto, non deciso dal founder)
1. Fix metrica LONGSHOT_FADE (P&L reale del lato NO) in `lab/signals.py::evaluate`
2. Poi: **Shadow Detector v1** (upgrade di whale watcher): scoring wallet per win-rate/timing/nicchia
   e alert quando un wallet "informato-simile" entra su un mercato liquido (vedi EDGE-STACK.md Strato A)

## Cosa NON fare (decisioni già prese, non riaprirle senza motivo del founder)
- Nessuna esecuzione ordini su venue non autorizzate in Italia (Polymarket/Kalshi in blacklist ADM).
  Il founder ha chiesto più volte di partire "a bassi livelli" via VPN: risposta data = no, per
  fondi congelabili senza ricorso + quadro illecito. La strategia è "radar → fucile" (EDGE-STACK.md §3).
- Nessun segreto/chiave privata mai nel repository.
- Nessun salto di livello di autonomia (L0→L4 in AGENTI.md) senza evidenza numerica.

## Rischi aperti
- Legale: blocco ADM attivo; TAR 25/08 esito non pubblico — tenere aggiornata la watchlist in REPORT.md
- Metrica LONGSHOT_FADE fuorviante (da fixare, vedi sopra)
- n campionario ancora piccolo: 46 risoluzioni non sono una statistica, sono un indizio
- Le edit_file fuzzy di Arena a volte non applicano: usare replace via Python per le modifiche critiche

## Ambiente
- Sandbox: /home/user/predmarket-lab (git repo locale, branch main)
- Run manuale: `python3 watcher.py --once` (o `--loop --interval 300`)
- Cloud: workflow GitHub Actions pronto (cron 15 min) — si attiva al primo push
