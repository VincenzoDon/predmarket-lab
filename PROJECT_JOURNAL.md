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
