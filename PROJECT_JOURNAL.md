# PROJECT_JOURNAL.md — cosa è successo e perché

## 2026-09-16 (sessione 1-3) — nascita del lab
- Founder chiede sistema per battere Polymarket partendo da 200€, obiettivo 10k/settimana.
- Ricerca: blocco ADM Italia (27/07/2026), fee V2 2026, volumi $25B/mese, arb già presidiati da HFT (2,7s).
- Costruiti: scanner 4 mode, modello fee, Kelly+Monte Carlo (puntando 30%: 56% prob. rovina),
  paper engine, STRATEGIE.md, README con piano a fasi.
- Decisione: nessuna esecuzione ordini; dati pubblici + paper trading (legale).
- Costruito watcher autonomo + SQLite + alert + dashboard self-contained + workflow GitHub Actions.
- Aggiunti agenti: SIGNAL ENGINE shadow (4 ipotesi) e WHALE WATCHER (leaderboard+posizioni).
- Ricerca posizionamento: spazio EN saturo, IT vuoto → "Osservatorio Italiano dei Mercati Predittivi",
  Indice di Inefficienza v0, piano virale 90 giorni (POSIZIONAMENTO.md).
- Founder preme per VPN "a bassi livelli": risposta no (fondi congelabili, quadro illecito);
  alternativa legale = radar→fucile (Betfair IT per sport, venue predittive quando legali).
- Ricerca "dove sono i soldi": <1% wallet = 50% profitti; $143M insider; bias longshot per categoria
  (crypto/politica sì, sport no); liquidity rewards $1M/mese → EDGE-STACK.md (Strati A/B/C).
- Decisione open-core: si pubblica infrastruttura+dati, restano privati i parametri d'alpha.
- v0.5: tracking rewards (97/300 mercati), alert REWARDS_MARKET.

## 2026-09-17 (sessione 4) — prima validazione
- Fix: row_factory DB, query mercati chiusi (closed=true), unpack 15 colonne.
- **Prima evidenza reale (46 mercati risolti):** ENDGAME_FAVORITE 6/6 (+13,3% medio);
  LONGSHOT_FADE 34/34 ma metrica fuorviante (P&L reale fade = +0,1…4,5%, loss = -100%);
  MEAN_REVERT 1/6 (-51,5%) → strategia bocciata v0. Esattamente ciò che il shadow mode serve a fare.
- Ricerca LLM per agente 24/7: GPT-5-nano $0,05/M token, DeepSeek V4-Flash $0,14/M,
  Gemini Flash-Lite ~$0,10/M → il "cervello" costerà frazioni di centesimo al giorno.
- Creato kit di continuità (STATUS_IT / PROJECT_JOURNAL / PROJECT_HANDOFF) adattando il kit
  personale del founder (uploads/01-03) a questo progetto.
- Da fare (prossimo passo unico): fix metrica fade → Shadow Detector v1.

## 2026-09-18 (sessione 6) — allineamento cloud, UI pubblica, basi validazione+automazione
- **Autocorrezione:** verificato che GitHub Actions RACCOGLIE dati (avevo detto il contrario:
  errore mio, mi ero fidato di git log prima del fetch). Il bot lab-bot committa scan su main.
  Il cloud si autoripara i conflitti (watcher rigenera i file d'output ogni ciclo).
- Scoperto che main (bot) e arena (mio codice v0.9) erano storie git SENZA antenato comune.
  Ricostruito arena su main fresco + codice v0.9 → superset pulito, PR mergeabile.
- **UI pubblica index.html** (lab/site.py): vetrina "per tutti" per GitHub Pages. Strategie con
  verdetto onesto, Shadow Detector, conto simulato, indice inefficienza, nota legale. La
  trasparenza come prodotto, anche per non-esperti → passo verso il "rivendibile".
- **lab/newsvalidator.py (base):** impianto per confermare i segnali su eventi LUNGHI (≥48h)
  con fonti esterne. Scoring confidence [-1,+1] pesato per fonte già funzionante; raccolta
  news/X/Telegram = STUB (NotImplementedError) finché non scegliamo le fonti. Nessun segreto.
- **lab/executor.py (base):** scaffold A6 gated e OFF. 5 cancelli di sicurezza (interruttore
  hard, blacklist ADM, evidenza numerica L3, budget alive, approval umano). Zero invio ordini.
  dry_run_report() dice quanto manca. Coerente con "radar → fucile" e con AGENTI.md.
- Decisione (col founder): per ora SOLO la struttura di validazione-notizie; le fonti X/Telegram
  si valutano dopo (API/costi/ToS), senza mettere chiavi nel repo.

## 2026-09-18 (sessione 5) — riparazione + Shadow Detector v1
- Nuovo agente collegato via ACCENSIONE_NUOVO_AGENTE.txt. Verifica repo: MANIFEST completo,
  commit v0.8 presente, DB storico intatto (4795 snapshot, 393 segnali, 308 posizioni whale).
- **Guasto trovato e riparato:** l'upload v0.8 via GitHub Desktop aveva lasciato marker di
  conflitto Git NON risolti dentro REPORT.md, dashboard.html, data/last_run.json. Risolti
  tenendo la versione più recente (ciclo 18, coerente col DB) + commit a1cfe8a + push.
- **Ambiente:** questa sandbox Arena non ha internet aperto (Polymarket e persino google.com
  irraggiungibili; solo GitHub/PyPI passano). Quindi il watcher live NON gira da qui — gira su
  GitHub Actions. Le sessioni precedenti giravano su sandbox aperte: è solo un ambiente diverso.
- **Osservazione preoccupante:** i run GitHub Actions risultano "success" ma durano 15-56s e non
  hanno prodotto NESSUN commit di dati (main fermo a v0.8). Probabile che lo scan non
  raccolga/committi, mascherato da `|| echo "nulla da committare"` e dal watcher che non falliva mai.
- **T1 — health-check onesto:** watcher.py ora esce con codice 2 se un ciclo raccoglie 0 mercati
  (in --once/--cycles) → i run cloud diventano ROSSI invece di verdi silenziosi. Workflow reso
  onesto (commit condizionale, niente più mascheramento).
- **T2 — bandiera salute dati:** report.py::_freshness → 🟢/🟡/🔴 "ultimo scan X ore fa" in
  dashboard e REPORT. Il sistema si accorge da solo quando è fermo (auto-aggiustante).
- **T3+T4 — SHADOW DETECTOR v1** (EDGE-STACK.md Strato A): lab/whales.py::score_wallets punteggia
  ogni wallet su win-rate (40%), profitto (25%), convinzione/size (20%), nicchia/focus (15%);
  penalità se poche osservazioni. Tabella wallet_scores. Alert SHADOW_ENTRY quando un wallet ad
  alto score entra su un mercato NUOVO. Gate di rischio: niente alert sotto 55% win-rate (per non
  fare da liquidità d'uscita alle balene). Calcolato offline dallo storico, zero ordini, zero rete.
  Ranking v1 sui dati reali: JnStrtPrdctnMrkts 87, Sassy-Bucket 80, Donkey14 76, HMLSF 75...
  I pesi/soglie sono parametri d'alpha (open-core), facili da ritarare.
- Prossimo passo: validare il ciclo cloud e misurare l'hit-rate degli alert SHADOW_ENTRY prima
  di dargli peso; poi split LONGSHOT_FADE per categoria (Strato C).

## Decisioni chiave (log)
| Data | Decisione | Motivo |
|---|---|---|
| 16/09 | Niente esecuzione su venue bloccate | rischi giuridici + fondi senza tutela; si lavora sui dati |
| 16/09 | Shadow mode prima del paper, paper prima del live | falsificare le strategie a costo zero |
| 16/09 | Open-core (infrastruttura pubblica, alpha privato) | credibilità/community senza regalare l'edge |
| 16/09 | Posizionamento IT + strumento EN | vuoto italiano verificato su Reddit/Telegram/stampa |
| 17/09 | MEAN_REVERT segnalata come bocciata | evidenza 1/6, media -51,5% |
- 17/09 (seguito): metrica P&L reale per lato implementata (_pnl_settled/_pnl_pct_live) +
  settle automatico a risoluzione mercato dentro il ciclo watcher. Ricalcolo onesto dei 46 segnali:
  ENDGAME 6/6 +13,3% · FADE 34/34 +0,61%/trade · MEAN_REVERT 1/7 -49,9% (confermata bocciatura).
  SIMULAZIONE CHIAVE (cap 5%/trade): tutte le strategie insieme = 200→175 (-12%);
  solo le valide (ENDGAME+FADE) = ~200→210. Lezione: il valore del lab è SEPARARE le strategie,
  non tradarle tutte. MEAN_REVERT resta attiva solo come esperimento (zero costi, più dati).
  Budget AI: regola n.5 in AGENTI.md (tetti di spesa lato provider, kill switch).
  Creato predmarket-lab-export.zip + MANUALE_GITHUB.md per il trasferimento.
- 17/09 (chiusura): BUDGET GOVERNOR (lab/budget.py): budget AI giornaliero = funzione
  matematica dei guadagni netti 30g (paper 10%, reali 100%, floor/cap, kill switch),
  wired nel watcher (registra gain_paper ogni ciclo). Preparati ACCENSIONE_NUOVO_AGENTE.txt
  + patch v0.8 per il trasferimento GitHub (via GitHub Desktop andata parzialmente bene:
  il nuovo agente deve verificare il MANIFEST e completare coi file del patch zip).
