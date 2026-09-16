# EDGE-STACK.md — Dove sono davvero i soldi (ricerca 16/09/2026)

La domanda era: "scoprire qualcosa su Polymarket che non fa nessuno e che porta guadagni
altissimi". Ho cercato sulle fonti giuste (studi accademici 2026, dati on-chain, report).
Risposta onesta in tre parti: **(1) chi vince davvero e come, (2) i 3 strati di denaro
replicabili, (3) cosa facciamo noi domani.**

---

## 1. Chi vince davvero su Polymarket (i numeri che nessuno mostra)

- **Meno dell'1% dei wallet si prende ~metà di tutti i profitti** (Solidus Labs, dic 2025-feb 2026:
  lo 0,55% dei maker vincenti e lo 0,26% dei taker vincenti ≈ $8M su $16M) [CoinDesk].
- **I trader "informati" hanno incassato $143M dal 2024** con 210.000 operazioni sospette
  (studio Columbia Law + Haifa): scommesse grandi e puntate poco prima della notizia,
  su elezioni, decisioni Fed, sport, geopolitica [Business Insider, mar 2026].
- **152 wallet con win rate 97,2%** sui mercati militari USA: $8M totali; un cluster di 38
  wallet coordinati ha fatto **$1,6M** su mercati Iran/Venezuela, incassando tutti sullo
  stesso indirizzo Coinbase [Bloomberg/Businessweek, lug 2026; USA Today/Reuters, ago 2026].
- Solo il **30% dei trader chiude in profitto** (studio su 124M di trade): i bravi sfruttano
  i bias dei meno bravi.

**Conclusione dura:** i guadagni "assurdi" esistono, ma sono di tre specie: insider
(informazione privilegiata — illecita per chi la usa), infrastruttura (HFT/market making
professionale) e **copy di chi è informato** — quest'ultimo è legale, pubblico e
sotto-sfruttato: *"big traders and bots are copying potential insider trades"* dice il
ricercatore ACDC citato da USA Today. Tutti i flussi sono visibili on-chain. **Qui entriamo noi.**

---

## 2. I 3 strati di denaro replicabili (dal più "figo" al più noioso)

### Strato A — SHADOW DETECTOR: caccia e copia dei flussi informati 🔥
**Cos'è:** un sistema che punteggia i wallet per "insider-simiglianza" (win rate estremo,
timing delle entrate, mercati di nicchia, wallet giovane, profitti anomali) e li segue con
piccole size quando aprono posizioni nuove. È quello che i bot sofisticati fanno già —
ma **nessuno lo fa per il pubblico italiano, e pochi lo fanno con disciplina di rischio**.
**Perché è il nostro terreno:** usa solo dati pubblici (legale da osservare), non serve
velocità HFT (i wallet informati entrano ore/giorni prima della notizia), è misurabile
(hit-rate del copy). Il nostro A4 Whale Watcher è già il v0: logga le posizioni dei top
wallet ogni ciclo. Upgrade: scoring anomalie + alert quando un wallet-sospetto entra
su un mercato liquido.
**Rischi:** essere l'uscita di sicurezza della balena → mitighe: size piccole, stop,
diversificazione sui wallet, mai inseguire prezzi già mossi.

### Strato B — LIQUIDITY REWARDS: il rendimento "noioso" che Polymarket paga 💰
**Cos'è:** Polymarket paga **USDC ogni giorno** solo per tenere ordini limit vicino al
midprice (programma da $1M/mese annunciato con CLOB v2, apr 2026). Pools: mercati Fed
$200-400/giorno, elezioni $500-1000/giorno. Punteggio quadratico: stare a 1¢ dal mid
rende ~4x rispetto a 2¢. Pagamento a mezzanotte UTC, minimo $1.
**Numeri realistici:** 15-30% annuo sul capitale impiegato (le stime "9-24% al mese"
che girano online sono ottimistiche da manuale). Con $10k: $30-80/giorno dai pool
+ spread + rebate maker (0% fee). **Non è il 10k/settimana, ma è l'unica rendita
quasi-passiva del settore** — e si somma al layer A e C.
**Il nostro lab ha già il dato:** lo scanner traccia i mercati con `clobRewards` attivi
da oggi (colonna/nuovo alert). Parametri `min_incentive_size`/`max_incentive_spread` via API.

### Strato C — BIAS STRUTTURALI PER CATEGORIA: la cassa continua 📊
**Cos'è (paper settembre 2026, 588M di trade, 2,48M wallet):** acquisti sotto i 10¢
perdono **19,3 centesimi per dollaro** nei flussi (crypto e politica); comprare a ≥90¢
guadagna 0,83¢/$. MA il bias **sparisce nello sport** (e lì semmai i favoriti pesanti
sono sovrapprezzati: quotate 70-100% si realizzano solo il 76% delle volte — dato da
verificare su dati nostri, n=847 di un blog).
**Traduzione operativa:** LONGSHOT_FADE (comprare il NO dei longshot) in **crypto e
politica**, mai nello sport; nello sport semmai il contrario (fade dei favoriti estremi).
Il nostro signal engine misura già tutto — ora lo splittiamo per categoria e smetteremo
di fare media sulle mele con le arance (che è l'errore che il paper ha corretto).

**Come si sommano:** Shadow Detector (rendimento alto, rischio alto) + Rewards
(rendito base, rischio basso) + Bias (cassa sistematica, rischio medio) = portafoglio
di edge, non una scommessa. Ed è esattamente il tipo di stack che l'1% vincente usa.

---

## 3. Cosa facciamo domani (già deciso nel lab)

1. **Whale Watcher → Shadow Detector v1**: scoring wallet (win rate, timing, età, nicchia)
   e alert quando un "sospetto" entra → è il prossimo pezzo di codice.
2. **Signal engine per categoria**: LONGSHOT_FADE split crypto/politica vs sport.
3. **Alert REWARDS_MARKET** nel watcher: già implementato oggi (vedi changelog).
4. Le tre cose NON eseguono ordini: misurano. L'execution arriva con la venue legale
   (o Betfair IT per lo sport) — e a quel punto abbiamo lo stack già misurato.

## 4. Verifica community Italia (Reddit/Telegram/canali vari — richiesta esplicita)

- Reddit: **un solo thread** (r/ItaliaPersonalFinance, mar 2025) che chiede se Polymarket
  sia legale; commenti: "non risulta nessun italiano multato", zero community attive.
- Telegram: nessun gruppo italiano sui mercati predittivi; esistono solo gruppi
  scommesse/trading sportivo generici. (Nota: Polymarket ha lanciato una mini-app
  Telegram "Predict" su TON a giugno 2026 — ma per noi il blocco venue non cambia.)
- Stampa italiana: articoli-guida a luglio 2026 sul blocco ADM, nessun progetto dati.
- Scena inglese (dove stanno gli italiani attivi): r/PredictionMarkets, r/PredictionHunt,
  r/Kalshi (42k membri) — communities vive di strumenti e picks.
**Conferma:** il vuoto italiano regge su tutti i canali cercati. Chi è attivo oggi opera
in inglese: quindi il piano è doppio — dominare il vuoto italiano E portare allo scenario
inglese uno strumento che lì non esiste pronto (Shadow Detector pubblico + numeri trasparenti).

## 5. Decisione open source (sintesi della tua obiezione — giusta)

Modello **open-core**: pubblichiamo infrastruttura (watcher, dashboard, indici) e numeri
= credibilità e community; teniamo privati i **parametri d'alpha** (soglie di scoring,
filtri segnali, regole di sizing). Il vero fossato non è il codice: è lo **storico dati**,
l'**audience** e l'**edge misurato** che nessuno può copiare indietro nel tempo.

---

### Fonti (tutte verificate oggi)
- Solidus Labs via CoinDesk (29/04/2026): <1% wallet ≈ 50% profitti
- Columbia Law School + Univ. di Haifa via Business Insider (28/03/2026): $143M insider
- Bloomberg Businessweek (20/07/2026): cluster 38 wallet, $1.6M su mercati militari
- USA Today/Reuters (20/08/2026): 152 wallet, win rate 97,2%, "bots copying insider trades"
- arXiv 2609.12878 (11/09/2026): favorite-longshot bias, 588M trade, per-categoria
- LaikaLabs, startpolymarket.com (09-12/09/2026): meccanica liquidity rewards
- Bitget News (28/04/2026): CLOB v2 + $1M liquidity rewards
- Reddit r/ItaliaPersonalFinance, r/PredictionMarkets, r/PredictionHunt; financecue.it;
  italiangamingexpo.com (Telegram Predict su TON, 25/06/2026)
