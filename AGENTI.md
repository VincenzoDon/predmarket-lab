# AGENTI.md — La flotta di agenti (chi fa cosa, e quando)

L'obiettivo è chiaro: **tu pensi alla tua vita, il sistema osserva, misura, decide e
riporta**. Questa è la mappa dei componenti ("agenti") con lo stato reale a oggi.
Nessun agente esegue ordini reali: l'esecutore esiste come design ma resta
**gated** finché non esiste una venue legale per l'Italia (vedi watchlist normativa).

| # | Agente | Ruolo | Stato | Input → Output |
|---|---|---|---|---|
| A0 | **SCOUT** | raccoglie i dati di mercato | ✅ costruito (`watcher.py`, `lab/scanner.py`, `lab/api.py`) | API pubbliche → SQLite (`data/lab.db`) ogni ciclo |
| A1 | **ANALISTA** | trasforma i dati in report/dashboard | ✅ costruito (`lab/report.py`) | DB → `dashboard.html` + `REPORT.md` |
| A2 | **RISK MANAGER** | decide quanto puntare e quando fermarsi | ✅ costruito (`lab/kelly.py`, limiti in `config.json`) | edge stimato → stake (Kelly ¼, cap 5%, stop giornaliero 10%) |
| A3 | **SENTINELLA / NEWS VALIDATOR** | notizie/fonti → confidence sui segnali lunghi | 🟡 base costruita (`lab/newsvalidator.py`): tabelle + scoring; fonti esterne = stub da collegare | news/X/Telegram → confidence [-1,+1] per segnale (regola: 2 fonti indipendenti) |
| A4 | **WHALE WATCHER / SHADOW DETECTOR** | studia i wallet vincenti on-chain e ne punteggia l'"insider-simiglianza" | ✅ v1 costruito (`lab/whales.py`): leaderboard + posizioni + consenso multi-balena + **scoring wallet (win-rate/profitto/convinzione/nicchia) e alert `SHADOW_ENTRY`** con gate di rischio sul win-rate | Data API pubblica → `whale_positions` + `wallet_scores` + alert `WHALE_CONSENSUS`/`SHADOW_ENTRY` |
| A5 | **SIGNAL ENGINE** | genera ipotesi e le verifica sui dati (shadow, zero capitale) | ✅ v0 costruito (`lab/signals.py`): ENDGAME_FAVORITE / MEAN_REVERT / LONGSHOT_FADE / MAKER_SPREAD con hit-rate automatico | snapshot → tabella `signals` → statistiche per strategia in dashboard |
| A6 | **ESECUTORE** | firma e invia ordini reali | 🔒 scaffold gated NON attivo (`lab/executor.py`): 5 cancelli + interruttore hard, zero invio | segnali + 5 gate + autorizzazione → ordini (solo su venue legale, oggi inesistente in IT) |
| A7 | **NORMATIVE WATCH** | monitora ADM/TAR/licenze | 🟡 oggi manuale (watchlist in REPORT.md) | news → attivazione di A6 quando la via è legale |

## Come scala l'autonomia (lettere di livello)

- **L0 — Osserva** (ora): SCOUT+ANALISTA girano da soli, costruiscono lo storico. Zero rischio.
- **L1 — Consiglia** (Fase 1-2): il sistema produce trade idea motivate (entry, size, motivo) su carta.
- **L2 — Esegue su carta** (Fase 0-2): paper trading automatico delle idee, curva P&L tracciata.
- **L3 — Esegue davvero** (solo se: edge ≥3% su ≥100 trade paper E venue legale): micro-capitale,
  umano approva ogni ordine per le prime settimane (come fa PolyBot col suo approval-gate).
- **L4 — Autonomo** : l'umano approva solo i limiti (max giornaliero, max esposizione),
  l'agente opera dentro i binari. Obiettivo di fine percorso.

## Regole della flotta (non negoziabili)

1. Nessun agente supera i limiti di A2 (Risk Manager), nemmeno a comando.
2. Ogni decisione è loggata (audit trail): `data/paper_trades.csv` oggi, DB domani.
3. Prima di ogni salto di livello serve evidenza numerica, non entusiasmo.
4. Se la watchlist normativa peggiora → si scende di livello, non si aggira.
5. Budget AI = formula, non promessa (lab/budget.py): il budget giornaliero dell'AI e'
   clamp(FLOOR, 20% x guadagni_netti_30g / 30, HARD_CAP), dove i guadagni paper contano
   al 10% e quelli reali al 100%. Zero guadagni -> spesa minima vitale; il progetto si
   autofinanzia e cresce solo se guadagna. Kill switch automatico a budget esaurito e
   tetto assoluto replicato SUL PROVIDER. Ogni spesa AI viene registrata in budget_events.
