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
| A3 | **SENTINELLA** | notizie/fonti → alert informativi | ⬜ Fase 1 | RSS/Telegram/siti → alert nel DB (regola: 2 fonti indipendenti) |
| A4 | **WHALE WATCHER** | studia i wallet vincenti on-chain | ✅ v0 costruito (`lab/whales.py`): leaderboard live + posizioni + alert consenso multi-balena | Data API pubblica → tabella `whale_positions` + alert `WHALE_CONSENSUS` |
| A5 | **SIGNAL ENGINE** | genera ipotesi e le verifica sui dati (shadow, zero capitale) | ✅ v0 costruito (`lab/signals.py`): ENDGAME_FAVORITE / MEAN_REVERT / LONGSHOT_FADE / MAKER_SPREAD con hit-rate automatico | snapshot → tabella `signals` → statistiche per strategia in dashboard |
| A6 | **ESECUTORE** | firma e invia ordini reali | 🔒 disegnato, NON attivo | segnali + autorizzazione → ordini (solo su venue legale) |
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
