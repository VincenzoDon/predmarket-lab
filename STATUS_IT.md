# STATUS_IT.md — Dove siamo davvero (aggiornato al 18/09/2026)

## Stato in una riga
Lab operativo e autonomo: 5 agenti attivi (SCOUT, ANALISTA, RISK, SIGNAL ENGINE, WHALE WATCHER),
~4.800 snapshot storici, 393 segnali shadow, prime evidenze reali raccolte. Zero soldi rischiati.
**Shadow Detector v1 costruito (18/09): scoring wallet + alert SHADOW_ENTRY.**
**Non esiste ancora nessuna esecuzione di ordini reali, per scelta (vedi rischi).**

## Novità 18/09/2026 — sessione 6 (pomeriggio)
- **CORREZIONE onesta:** nella sessione precedente avevo detto "GitHub Actions è verde ma
  non raccoglie dati". ERA SBAGLIATO. Verificato: il bot cloud GIRA e committa dati
  (lab-bot, scan delle 11:53 UTC, 5095 snapshot, DB fresco). Il cloud si è pure auto-riparato
  i marker di conflitto (il watcher rigenera REPORT/dashboard ogni ciclo).
- **Rami riallineati:** main (dati freschi del bot) e arena (codice v0.9) erano storie separate
  senza antenato comune. Ricostruito arena SOPRA i dati freschi di main + codice v0.9 → ora
  arena è un superset pulito di main (PR mergeabile senza conflitti).
- **UI pubblica (index.html):** nuova pagina "per tutti", pensata per GitHub Pages, statica,
  zero server. Spiega il progetto a parole semplici, mostra strategie con VERDETTO onesto
  (promettente/bocciata/pochi dati), Shadow Detector, conto simulato, nota legale ADM.
  Generata a ogni ciclo da lab/site.py, committata dal workflow.
- **Base validazione notizie (lab/newsvalidator.py):** IMPIANTO pronto (tabelle, scoring
  confidence, gate "solo eventi lunghi ≥48h"). Fonti esterne (news/X/Telegram) sono STUB
  espliciti: NON collegate finché non decidiamo insieme quali (nessun token nel repo).
- **Base automazione (lab/executor.py):** SCAFFOLD gated e NON attivo. Interruttore hard
  EXECUTION_ENABLED=False + blacklist venue ADM + soglia evidenza (edge≥3% su ≥100 trade) +
  budget alive + approval umano. Nessun codice di invio ordini. dry_run_report() mostra quanto
  siamo lontani dall'abilitazione per ogni strategia.

## Novità 18/09/2026 — sessione 5 (mattina)
- **Riparato** l'upload v0.8: i file REPORT.md, dashboard.html, data/last_run.json avevano
  marker di conflitto Git non risolti (residui di GitHub Desktop). Risolti + push.
- **Health-check onesto (T1):** il watcher ora esce con codice != 0 se un ciclo raccoglie 0
  mercati (rete/API giù). Prima il run GitHub Actions restava "verde" anche a vuoto: bugia
  pericolosa per un sistema che deve auto-aggiustarsi. Ora diventa ROSSO e ce ne accorgiamo.
- **Bandiera salute dati (T2):** REPORT.md e dashboard mostrano 🟢/🟡/🔴 con "ultimo scan X ore fa".
- **Shadow Detector v1 (T3+T4):** `lab/whales.py` punteggia ogni wallet (win-rate, profitto,
  convinzione, nicchia) → tabella `wallet_scores`; alza `SHADOW_ENTRY` quando un wallet ad alto
  punteggio ENTRA su un mercato nuovo. Gate di rischio: niente alert sotto il 55% di win-rate
  (per non fare da liquidità d'uscita alle balene). Tutto shadow, zero ordini, calcolato
  offline dallo storico. Visibile in dashboard e REPORT.
- **Nota ambiente:** questa sandbox NON ha internet aperto (solo GitHub/PyPI raggiungibili;
  Polymarket e persino google.com danno errore). Il ciclo live NON gira da qui: gira su
  GitHub Actions. Da verificare che là raccolga ancora dati (vedi rischi).

## Cosa funziona VERIFICATO CON CODICE
- `run_scan.py` — scanner live 4 mode (closing/arb/spreads/movers/book/fees) su API pubbliche
- `watcher.py` — ciclo autonomo: 300 mercati/ciclo (paginato) → SQLite → alert dedupe → dashboard+report
- Signal engine shadow: ENDGAME_FAVORITE / MEAN_REVERT / LONGSHOT_FADE / MAKER_SPREAD, valutati su risoluzione reale
- Whale watcher: leaderboard + posizioni top-5 + alert consenso (fixare: vedi sotto)
- Tracking liquidity rewards (97/300 mercati con rewards attivi al 16/09)
- Paper trading engine (fee+slippage) — usato 1 volta demo, ROI +0.62%
- Budget governor (lab/budget.py): spesa AI = funzione matematica dei guadagni (paper al 10%,
  reali al 100%, FLOOR 0,03$/g, HARD_CAP 5$/g, kill switch) — wired nel watcher
- Git: repo locale con commit fino a v0.5 (NON ancora pushato su GitHub: serve sessione collegata)

## Prime evidenze (giorno 1, 16→17/09, 46 mercati risolti)
- **ENDGAME_FAVORITE: 6/6 vinte, media +13,3%** (Fed 25bps +13,0%, Barcellona +9,3%, Leverkusen +9,3%, Bitcoin>74k +4,4%, Musk tweet +24,2%, Vissel Kobe +19,8%) ← ipotesi più promettente
- **LONGSHOT_FADE: 34/34 vinte** MA attenzione: il +100% mostrato è un artefatto della metrica
  (misura il movimento del lato YES, non il P&L reale del fade). P&L reale per vincita = ep/(1-ep)
  ≈ +0,1%…+4,5%; una sola loss = -100% della posizione. Va fixata la metrica in `lab/signals.py`.
- **MEAN_REVERT: 1/6, media -51,5% → STRATEGIA BOCCIATA nella v0** (le mosse 1h dei mercati
  live tendono a CONTINUARE, non a rientrare). Da rivedere: forse invertirla (momentum) o cancellarla.

## Prossimo UNICO passo (dedotto, non deciso dal founder)
1. ✅ FATTO (17/09): metrica P&L reale per lato + settle automatico a risoluzione mercato
   (lab/signals.py: _pnl_settled / settle_resolved, chiamato dal watcher ogni ciclo)
2. ✅ FATTO (18/09): **Shadow Detector v1** (lab/whales.py): scoring wallet + alert SHADOW_ENTRY
   con gate di rischio sul win-rate. Persistito in wallet_scores, mostrato in dashboard/REPORT.
3. **PROSSIMO — Validare il ciclo cloud + affinare lo Shadow Detector coi dati veri:**
   a) verificare su GitHub Actions che il watcher raccolga ancora dati (i run erano "verdi"
      ma senza commit di dati né output — ora l'health-check li renderà onesti);
   b) far girare qualche ciclo per accumulare snapshot dei wallet ad alto score;
   c) misurare l'hit-rate degli alert SHADOW_ENTRY (come per gli altri segnali) prima di
      dargli qualsiasi peso — è un radar da falsificare, non una verità.
   Poi: split LONGSHOT_FADE per categoria (crypto/politica vs sport) — EDGE-STACK.md Strato C.

## Cosa NON fare (decisioni già prese, non riaprirle senza motivo del founder)
- Nessuna esecuzione ordini su venue non autorizzate in Italia (Polymarket/Kalshi in blacklist ADM).
  Il founder ha chiesto più volte di partire "a bassi livelli" via VPN: risposta data = no, per
  fondi congelabili senza ricorso + quadro illecito. La strategia è "radar → fucile" (EDGE-STACK.md §3).
- Nessun segreto/chiave privata mai nel repository.
- Nessun salto di livello di autonomia (L0→L4 in AGENTI.md) senza evidenza numerica.

## Rischi aperti
- **Ciclo cloud da verificare:** i run GitHub Actions risultavano "success" ma duravano 15-56s
  e NON producevano commit di dati (su main l'ultimo commit dati è ancora v0.8). Sospetto che
  lo scan non raccolga/committi. Da controllare il log dello step "Ciclo di scan" su GitHub →
  Actions. L'health-check aggiunto oggi renderà i prossimi run onesti (rosso se 0 mercati).
- **Sandbox senza internet aperto:** da qui non si testa il ciclo live (solo GitHub/PyPI passano).
- Legale: blocco ADM attivo; TAR 25/08 esito non pubblico — tenere aggiornata la watchlist in REPORT.md
- Shadow Detector: n piccolo (13 cicli, 16 wallet). Lo score è un indizio, NON una verità:
  va validato l'hit-rate degli alert prima di fidarsene. Rischio "liquidità d'uscita" mitigato
  dal gate win-rate, ma non azzerato.
- n campionario ancora piccolo: le risoluzioni raccolte sono un indizio, non una statistica
- Le edit_file fuzzy di Arena a volte non applicano: usare replace via Python per le modifiche critiche

## Ambiente
- Sandbox: /home/user/predmarket-lab (git repo locale, branch main)
- Run manuale: `python3 watcher.py --once` (o `--loop --interval 300`)
- Cloud: workflow GitHub Actions pronto (cron 15 min) — si attiva al primo push
