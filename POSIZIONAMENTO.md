# POSIZIONAMENTO.md — Come diventiamo i maestri di una cosa che non esiste ancora

Ricerca di mercato svolta il 16/09/2026 (fonti in fondo). Conclusione in una riga:
**lo spazio è affollatissimo in inglese e completamente vuoto in italiano. Noi occupiamo il vuoto.**

---

## 1. La mappa di ciò che ESISTE già (per non illudersi)

| Segmento | Giocatori già attivi | Saturazione |
|---|---|---|
| Whale tracking | PolyInsider, PolyMonit, PolyWhaleTracker, HashDive, PrediEdge, PolyAlertHub | 🔴 altissima |
| Arb scanner cross-venue | ArbBets, Predictions Terminal, Arbitrage Agent, Claw Arbs | 🔴 alta |
| Framework bot/agenti | PolyBot (MCP, multi-venue), CloddsBot, Polymarket/agents (ufficiale), CLI varie | 🟠 media-alta |
| Dashboard analytics | Polymarket Analytics, PredictFolio, Stand.trade, Polyfactual | 🔴 alta |
| Paper trading game | **FantasyPoly** (play money, anche agenti AI, con "Agent Trust Score") | 🟠 media |
| Benchmark AI su mercati | Metaculus FutureEval, ForecastBench, "Prediction Arena" (arXiv), PolyBench (arXiv) | 🟠 accademica |
| Contenuti in italiano | Solo guide affiliazione scommesse ("cos'è Polymarket") | 🟢 **VUOTO** |
| Osservatorio dati in italiano | **NESSUNO** | 🟢 **VUOTO TOTALE** |

## 2. La lezione scomoda che la ricerca ci regala (da tenere davanti agli occhi)

I benchmark 2026 su agenti AI che operano nei mercati predittivi dicono una cosa chiarissima:

- **Prediction Arena** (paper trading di GPT-5.4, Claude Opus 4.6, GLM-5, Gemini 3.1 su Kalshi/Polymarket):
  la maggior parte dei modelli chiusa **piatta o in perdita** in settimane di trading (Claude -10% in 3 giorni,
  Gemini +6% nel miglior caso).
- **PolyBench** (38.666 mercati): su 7 modelli solo **2 in utile** (MiMo-V2 +17,6%, Gemini-3-Flash +6,2%), gli altri
  tutti negativi nonostante la fiducia dichiarata dell'85%.
- **Metaculus**: i superforecaster umani battono ancora i bot nei tornei (finora, ogni trimestre).

**Traduzione strategica:** "AI che scommette da sola" NON è l'edge — lo dicono i numeri di chi l'ha già provato
in pubblico. L'edge è **il metodo misurato** (hit-rate veri, disciplina, nicchie, velocità informativa).
Questo è il nostro差异atore dichiarabile e onesto: noi pubblichiamo i numeri, anche quando sono brutti.
La trasparenza totale È il prodotto.

## 3. Il posizionamento scelto: 🇮🇹 L'Osservatorio Italiano dei Mercati Predittivi

**Nessuno in Italia guarda ai mercati predittivi come fonte di informazione e dato.** Il mondo anglosassone
ha Bloomberg-of-prediction-markets, whale tracker, arena di agenti. L'italiano medio (giornalisti inclusi)
scopre le probabilità di Sanremo/Serie A/elezioni dai titoli tradotti, settimane dopo.

Cosa costruiamo, in ordine:

### 3a. Il numero: "Indice di Inefficienza" (già implementato nel lab, v0)
Un solo numero 0-100, aggiornato a ogni ciclo: **quanto è inefficiente il mercato predittivo adesso?**
(spread larghi sui top mercati + mosse violente in 1h). Il "Fear & Greed index" dei mercati predittivi.
Non esiste nessun indicatore pubblico equivalente. Da quotare ogni giorno sui social: diventa il nostro hook.

### 3b. Il contenuto: "Cosa dicono i mercati sull'Italia"
Settimanalmente: le probabilità di Serie A, mercato, elezioni, Sanremo, economia italiana — spiegate in
italiano, con i dati del nostro lab, prima che li riportino i giornali. Formato virale nativo.

### 3c. L'architettura trasparente: "radar → fucile"
- **Radar (legale, ora):** i dati pubblici di Polymarket/Kalshi come strumento di analisi.già in funzione.
- **Fucile (legale, quando c'è edge):** esecuzione sui mercati **legali** italiani — Betfair Exchange
  opera in Italia con licenza ADM dal 2014 (commissione 4,5% sulle vincite nette): exchange sportivo
  dove le nostre letture cross-venue diventano esecuzione reale.
- **Passaggio L3:** quando e se una venue predittiva diventa legale in Italia (licenza ADM o esito TAR),
  l'Esecutore già progettato si collega in giorni, con edge già misurato.

### 3d. La community: open source come moat
Codice aperto (GitHub) + dashboard pubblica (Cloudflare Pages) + numeri veri = credibilità che nessun
"guru" può comprare. Il progetto diventa il punto di riferimento italiano prima che il mercato si apra.

## 4. Setup 2026 (ricerca indipendente, non influenzata dal nome "GitHub")

| Bisogno | Scelta 2026 | Perche' | Costo |
|---|---|---|---|
| Codice + community + CI | **GitHub** (Actions incluso) | resta il centro di gravita' open source 2026; Actions gratis su repo pubblico | 0€ |
| Sito/dashboard pubblica | **Cloudflare Pages** | bandwidth illimitata gratis, CDN globale, dominio custom, 500 build/mese | 0€ |
| Compute periodico | **GitHub Actions** (cron 15 min) | già pronto | 0€ |
| Compute continuo (futuro) | **Oracle Cloud Always Free** → poi VPS ~5€/mese | quando servira' reazione in secondi | 0€ → 5€ |
| Dominio (quando serve) | .it o .com | ~10-12€/anno | 10€/anno |
| Social | X/Threads + LinkedIn (build in public) | dove vive l'audience finanza/tech italiana | 0€ |

Totale oggi: **0€/mese**. Verdetto onesto: "GitHub" non era un nome a caso — nel 2026 resta la scelta
razionale per un progetto open source. Ma la parte pubblica (il prodotto che la gente vede) va su
Cloudflare Pages, che per banda e prestazioni gratis è superiore a GitHub Pages.

## 5. Piano virale a 90 giorni

| Settimana | Azione | Metrica di successo |
|---|---|---|
| 1-2 | Repo pubblico + dashboard online + primo post "sto costruendo l'Osservatorio italiano dei mercati predittivi, open source" | repo online, 1 post |
| 3-4 | Indice di Inefficienza quotidiano + thread "cosa dicono i mercati sull'Italia" | prima 1.000 impression |
| 5-8 | Report settimanale automatico (generato dal lab) pubblicato come articolo | 100 follower, primi contributi/issues |
| 9-12 | "Arena degli agenti": classifica pubblica delle nostre strategie shadow (hit-rate reali) + invito a contribuire strategie | la community propone la prima strategia esterna |

## 6. Perché questo posizionamento CI FA anche guadagnare (quando sarà il momento)

1. Audience = distribuzione: quando una via legale si apre, siamo già i known-issue italiani del settore.
2. Il metodo misurato (hit-rate storici per strategia) è un asset che vale sia per trading che come prodotto.
3. Canali di monetizzazione compatibili: sponsor/donazioni, dataset premium, consulenza per piattaforme
   che vorranno entrare in Italia (pagheranno per capire il mercato italiano), e — se tutto converge —
   gestione del capitale quando lecito.

---

## Fonti principali (16/09/2026)

- Landscape analytics: CoinCodeCap "Top 10 Polymarket Analytics Tools 2026"; PolyInsider; PolyMonit; PolyWhaleTracker
- Paper trading: FantasyPoly (fantasypoly.com)
- Benchmark AI: arXiv "Prediction Arena" (2604.07355); arXiv "PolyBench" (2604.14199); LessWrong/EA Forum "AI Forecasting in 2026"
- Hosting 2026: klymentiev.com "Free Website Hosting in 2026"; snapdeploy.dev "Free Cloud Deploy Platforms 2026 — Ranked"
- Legale: ADM (list nera >12.000 domini, ago 2026 — statoquotidiano.it); Betfair Exchange Italia licenza ADM dal 2014, commissione 4,5% (bettingexchange.net)
- Italia/contenuti: scommessepro.it, criptovaluta.it (solo guide affiliazione: conferma del vuoto)
