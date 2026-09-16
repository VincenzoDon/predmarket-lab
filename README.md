# predmarket-lab 🎯

**Laboratorio per battere i mercati predittivi (stile Polymarket) con dati live, agenti e money management rigoroso.**

Qui dentro c'è: uno scanner live sulle API pubbliche di Polymarket, il modello esatto delle
commissioni, il motore di paper trading e il framework di risk management (Kelly frazionato).
Si parte da €200 e si costruisce un sistema — non una scommessa.

---

## ⚠️ I tre fatti duri, prima di tutto

### 1. La matematica di "10k settimanali partendo da 200€"

€10.000/settimana con un bankroll di €200 significa **+4.900% a settimana**. Per darti
l'ordine di grandezza: i migliori fondi quantistici del mondo fanno **30-40% ALL'ANNO**.
Per arrivare a 10k€/settimana in modo *sostenibile* ti serve:

| Rendimento/settimana | Bankroll necessario per 10k€/sett. | Realtà |
|---|---|---|
| 1% | 1.000.000 € | Obiettivoragionevole di lungo periodo |
| 2% | 500.000 € | Ottimo già sosterlo per 1 anno |
| 5% | 200.000 € | Elite mondiale se sostenuto |
| 10% | 100.000 € | Nessuno lo sostiene a lungo |

L'unica via da 200€ a 10.000€ in breve è la **lotteria**: 6 raddoppi consecutivi (200→400→…→12.800).
Anche vincendo ogni singola puntata con probabilità 60% (un edge enorme), la probabilità di
fare 6 di fila è **4,7%** → il 95% delle volte azzeri il bankroll.

**Il piano vero** (questo lab): edge verificabile → paper trading → capitale piccolo →
compounding → scale. Non è un limite, è l'unica strada che esista.

Monte Carlo fatto col modulo `lab/kelly.py` (100 scommesse con edge REALE dell'8% ciascuna):

| Sizing | P(distruzione) | P(dimezzamento) | Bankroll mediano |
|---|---|---|---|
| 2%/trade | 0,0% | 0,0% | ×1,15 |
| 5%/trade (Kelly ¼) | 0,0% | 2,9% | ×1,32 |
| 15%/trade | 4,2% | 30,8% | ×1,07 |
| 30%/trade | 56,5% | 71,9% | ×0,05 |

→ **Anche con un edge vero, il sizing sbagliato ti ammazza.** Per questo il lab parte dal risk management.

### 2. Situazione legale in Italia (aggiornata al 16/09/2026)

- **22/10/2025** — ADM (Dogane e Monopoli) iscrive Polymarket nella blacklist dei siti di
  gioco non autorizzati → oscuramento ISP.
- **Dicembre 2025** — ricorso al TAR Lazio: sito riaperto ma **trading disabilitato** per IP italiani.
- **10/07/2026** — ADM reiscrive Polymarket (e **anche Kalshi**) tra i 293 nuovi siti da oscurare.
- **27/07/2026** — blocco effettivo.
- **05/08/2026** — TAR Lazio rigetta l'urgenza; il merito va in camera di consiglio il 25/08/2026
  (nessuna notizia di revoca trovata: **il blocco resta in piedi**).
- I ToS di Polymarket vietano esplicitamente l'uso da VPN per aggirare i blocchi; giocare su
  piattaforme non autorizzate = zero tutela legale in caso di problemi.

**Conseguenza pratica per noi:** questo lab lavora su **dati pubblici** (Gamma/CLOB API in
lettura: perfettamente accessibili e legali da analizzare) e su **paper trading**. Il modulo
di esecuzione ordini NON esiste qui, volutamente. Se il quadro cambia (licenza ADM, esito TAR,
o piattaforme legali), il lab è già pronto a collegarvisi.

**Tasse (anche se giochi all'estero, i guadagni sono tuoi):** dal 01/01/2026 le plusvalenze
cripto sono tassate al **33%** (L. 207/2024 e L. 199/2025), la franchigia dei 2.000€ è
abolita dal 2025 e c'è l'imposta dello 0,2% sul valore delle cripto-attività a fine anno,
con obbligo di monitoraggio nel quadro RW/W. Parlane con un commercialista prima di prelevare cifre serie.

### 3. Le fee hanno cambiato il gioco (2026)

Polymarket non è più "gratis": dal 30/03/2026 (Fee Structure V2) i **taker** pagano
`fee = rate × p × (1-p)` per share, dove rate dipende dalla categoria
(crypto 0,07 | sports 0,03 | finanza/politica 0,04 | economia/cultura 0,05 | geopolitica **0**).
I **maker pagano 0 e ricevono rebate**. Con spread incluso, un round-trip taker costa ~2-4%.
→ Regola: **sotto ~2 punti di edge NETTO non si entra. Mai.**

---

## Perché questo mercato sì (il tuo intuito è giusto)

I numeri che rendono il settore interessante oggi:

- Volumi Polymarket: **$25,7 miliardi solo a marzo 2026**, 1,29M wallet attivi nel Q1,
  sport a $10,1B nel Q1. Record giornaliero $425M (28/02/2026).
- I bot di arbitraggio hanno estratto **$40M in 12 mesi** (studio IMDEA Networks) —
  ma le finestre strutturali ora durano **~2,7 secondi**: quel gioco è dei robot HFT.
- Restano margini veri dove i bot grandi non guardano: spread larghi su mercati di nicchia,
  latenza informativa su eventi in chiusura, knowledge locale (calcio italiano!), bias
  sistematici (longshot bias), lettura fine delle regole di risoluzione.

Dettaglio strategie: **[STRATEGIE.md](STRATEGIE.md)** — playbook completo con ranking di fattibilità.

---

## Struttura del lab

```
predmarket-lab/
├── run_scan.py          # scanner live (CLI): closing | arb | spreads | movers | fees | book
├── watcher.py           # ⭐ ciclo continuo: scan -> SQLite -> alert -> report (autonomo)
├── dashboard.html       # cockpit self-contained generato dal watcher (apribile ovunque)
├── REPORT.md            # report sintetico generato dal watcher (markdown)
├── lab/
│   ├── api.py           # client Gamma + CLOB (SOLO LETTURA, dati pubblici)
│   ├── fees.py          # modello commissioni V2 esatto (dal campo feeSchedule)
│   ├── scanner.py       # 4 scansioni: chiusure, arb negRisk, spread maker, mover notizia
│   ├── kelly.py         # Kelly frazionato + Monte Carlo rischio di rovina
│   ├── paper.py         # motore paper trading (fill a ask reale + fee + slippage)
│   └── report.py        # generatore dashboard + report
├── .github/workflows/   # GitHub Actions: il watcher gira nel cloud ogni 30 min (gratis)
├── config.json          # bankroll, limiti rischio, parametri scan
├── data/                # lab.db (storico SQLite) + stato paper + registro CSV
├── AGENTI.md            # mappa della flotta di agenti e livelli di autonomia
└── STRATEGIE.md         # playbook dei vantaggi competitivi
```

## Uso rapido

```bash
pip install -r requirements.txt

python3 run_scan.py                        # scan completo
python3 run_scan.py --mode closing --days 3     # cosa chiude entro 3 giorni
python3 run_scan.py --mode arb                  # arbitraggi strutturali (netti fee)
python3 run_scan.py --mode spreads              # spread larghi -> candidate maker
python3 run_scan.py --mode movers               # dove sta girando la notizia
python3 run_scan.py --mode book --slug <slug>   # order book CLOB di un mercato
python3 run_scan.py --mode fees                 # tabella commissioni
```

Esempio reale dal primo scan (16/09/2026, 11:30 CEST):
- **Fed Decision di oggi**: 5 mercati da $2-7M di volume 24h che chiudono stasera con l'annuncio FOMC
- **"Ethereum $2.600 a settembre?"**: bid 0,48 / ask 0,69 → **21 punti di spread** su 70k di volume:
  classica situazione dove fare il maker (postare limit dentro lo spread, fee 0, rebate) cattura valore
- Panieri multi-esito (Fed ottobre: 5 esiti) con costo YES 1,069 → l'arb "gratis" non c'è (già mangiato
  dai bot), ma il monitoraggio dice quando si apre un varco

## ▶️ Far girare il watcher senza il tuo PC acceso

Il watcher è progettato per vivere nel cloud. Opzioni (dalla più semplice):

| Opzione | Costo | Adatta a | Limiti |
|---|---|---|---|
| **GitHub Actions** (workflow già pronto in `.github/workflows/`) | 0€ | scan ogni 30 min, storico, report, dashboard | ritardi anche di 5-15 min; non per reazioni in secondi |
| **Oracle Cloud Always Free** | 0€ | watcher continuo + agenti 24/7 | setup più tecnico; istanze ferme vengono recuperate se CPU <20% per 7 giorni (serve un keep-alive) |
| **VPS (es. Hetzner)** | ~4-6€/mese | il passo professionale: loop continuo, futuro live | costo mensile |
| **Raspberry Pi a casa** | ~70-90€ una tantum | tutto in casa, consuma ~5W | legato a casa/rete tua |

### Quickstart GitHub (10 minuti, una volta sola)

```bash
# sul tuo PC, dentro la cartella del progetto:
git init && git add -A && git commit -m "predmarket-lab v0.2"
# crea un repo VUOTO su github.com (account gratuito, SENZA readme), poi:
git remote add origin https://github.com/TUO-UTENTE/predmarket-lab.git
git branch -M main && git push -u origin main
```

Poi su GitHub: scheda **Actions** → workflow `watcher` già presente → parte da solo ogni
30 minuti e committa dati + dashboard nel repo (la dashboard si apre direttamente da GitHub).

Note: su repo **pubblico** i minuti sono illimitati (e il repo pubblico è in linea col
profilo "build in public"); su repo privato il piano free dà 2.000 min/mese — in quel caso
porta il cron a `0 * * * *` (orario). **Mai** committare chiavi private o seed phrase:
questo progetto non ne ha bisogno.

## Il piano in fasi

| Fase | Cosa | Durata | Obiettivo misurabile |
|---|---|---|---|
| **0 — Ora** | Scanner live + paper trading su dati reali | 2-4 settimane | ≥100 trade paper registrati, curva P&L positiva, edge medio ≥3% netto |
| **1** | Automazione: watcher continuo + alert (Telegram/discord) + dataset storico prezzi | 2-3 settimane | Agenti che loggano ogni finestra di vantaggio senza uomo al pc |
| **2** | Backtest strategie su dataset raccolto + scegli 1-2 armi | 3-4 settimane | Edge confermato out-of-sample |
| **3** | Capitale piccolo SOLO su venue legale per te (o se quadro ADM cambia) | — | Regole: max 5%/trade, stop-loss giornaliero 10%, max 2 ricariche |
| **4** | Scale: il bankroll cresce per compounding, si aggiunge capitale solo su edge provato | mesi/anni | Da 200€ il punto di partenza, non il limite |

**Regola non negoziabile:** nessuna fase salta la precedente. Il 90% di chi perde soldi qui
non è chi non ha edge — è chi non ha (in quest'ordine) sizing, pazienza e dati.

---

## Fonti principali

- Blocco ADM/TAR: Il Sole 24 Ore, Sky TG24, La Stampa, open.online, Punto Informatico, Agipro (lug-ago 2026)
- Fee structure V2 e API: docs Polymarket, sacra.com, crypticorn.com (2026), campi `feeSchedule` verificati live
- Volumi: Bitget Wallet report Q1 2026, tradetheoutcome.com, blockchainreporter.net
- Arb bot e finestre 2,7s: studio IMDEA Networks (arXiv 2508.03474), turbinefi.com, ahasignals.com (2026)
- Tasse: L. 207/2024, L. 199/2025, guide fiscali 2026 (tassetrading, centrofiscale, nevist)
