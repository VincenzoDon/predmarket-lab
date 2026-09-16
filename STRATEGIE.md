# STRATEGIE.md — Playbook dei vantaggi competitivi

Ranking in base a: **fattibilità con ~€200, connessione domestica, e un italiano che parla
italiano e segue lo sport italiano**. Aggiornato a settembre 2026 sui dati reali del lab.

---

## S1 — Arb strutturale su panieri negRisk ⚙️ *Fattibilità: BASSA (con 200€)*

**Idea.** Un evento multi-esito mutuamente esclusivo (es. "Fed Decision": 5 esiti, uno solo
verrà pagato $1). Se la somma degli ask di TUTTI gli esiti + fee < $1, compri tutto il
paniere e incassi $1 garantito. Simmetrico sul lato NO (comprare NO ovunque paga n-1 dollari).

**Realtà 2026.** Lo scanner (`--mode arb`) conferma sui 150 eventi più liquidi che i panieri
costano oggi 1,014-1,07: le finestre positive durano in media **2,7 secondi** e sono già
presidiate da bot HFT con server co-locati (hanno estratto $40M in 12 mesi, IMDEA Networks).
Con €200 e una linea domestica non vinci quella corsa.

**Quando ritenta.** Il nostro scanner li logga comunque: se un varco >0,5% netto resta aperto
per decine di secondi (mercato di nicchia, orario notturno, evento appena creato), è il
segnale che lì NON ci sono bot. Quello è il tuo terreno di caccia.

---

## S2 — Cross-venue (Polymarket vs Kalshi vs bookmaker) ⚙️ *Fattibilità: BASSA-MEDIA + blocco legale*

**Idea.** Lo stesso evento quotato su piattaforme diverse a prezzi diversi: compra il lato
economico su una, il contrario sull'altra. Spread tipici pre-costi 1,5-4,5%.

**Problemi.** (1) Kalshi è nella blacklist ADM italiana insieme a Polymarket dal 27/07/2026;
(2) le fee taker su entrambe le piattaforme (~1% + ~3%) mangiano spread sotto ~6 punti;
(3) i contratti spesso NON sono identici: stesse domande con soglie o regole di risoluzione
diverse → quelli che sembrano arb sono a volte solo scommesse diverse;
(4) servono capitali pre-posizionati su entrambe le venue.

**Come sfruttarlo DA SUBITO senza tradare:** il confronto prezzi tra venue è un *segnale*:
se Betfair/bookmaker legali italiani quotano un evento del campionato italiano e Polymarket
lo quotato in modo diverso, la divergenza ti dice dove il mercato predittivo è meno efficiente
(= dove andare a caccia con S4/S5).

---

## S3 — Market making su spread larghi 💰 *Fattibilità: MEDIA-ALTA — la nostra arma n.1*

**Idea.** I maker pagano **fee 0%** e prendono rebate. Quando uno spread è largo, posti un
limit order dentro lo spread (compri al bid+1tick, vendi all'ask-1tick) e incassi lo spread
ripetutamente. Esempio REALE visto oggi: "Ethereum $2.600 a settembre?" bid 0,48 / ask 0,69
su 70k$ di volume 24h → chi sta dentro quello spread sta raccogliendo.

**Perché è alla nostra portata.** Non serve velocità HFT: serve capitale paziente e
selezione. I bot grandi fanno market making sui mercati grossi (spread 1-2 centesimi);
sui mercati medi di nicchia gli spread larghi restano aperti perché non vale il loro tempo.
In più Polymarket paga **clobRewards** (incentivi liquidity mining) su alcuni mercati:
lo scanner li segnala con la colonna `rw`.

**Rischi.** Adverse selection: ti riempiono gli ordini solo quando hai torto (la notizia
esce mentre hai il lato sbagliato). Mitigazioni: (a) solo mercati con regole che conosci,
(b) ritira gli ordini quando vedi volatilità impazzita (`--mode movers`), (c) size piccole.

**Requisiti:** capitale a riposo (non serve velocità, serve presenza), bot che quotano
due lati e aggiorna — fattibile con API + py-clob-client (archiviato a maggio 2026, ora
esiste il client V2: da verificare al momento dell'eventuale esecuzione).

---

## S4 — Latenza informativa su mercati in chiusura ⚡ *Fattibilità: MEDIA (alta se scegli la tua nicchia)*

**Idea.** Il tuo punto: "cose che chiudono da un momento all'altro". Nei minuti finali di
un mercato, il prezzo è stabilito da chi ha l'informazione più fresca. Chi reagisce per
primo all'annuncio FOMC, al risultato live della partita, alla rettifica ufficiale, compra
a 0,80 ciò che vale 0,98.

**Esempio di OGGI (16/09/2026):** i 5 mercati "Fed Decision September" ($2-7M di volume
24h ciascuno) chiudono con l'annuncio FOMC di stasera. Chi ha un feed veloce sulla
comunicata (il testo, non solo il numero) si prende i secondi decisivi.

**Dove un piccolo player VINCE davvero:** gli eventi live minori — tennis Challenger
(lo scanner oggi mostra match di Biella e Guangzhou che si muovono del 40-90% in un'ora),
esports (CCT di Counter-Strike tra i top mover), campionati di calcio minori. I bot
generali non seguono il feed live di un Challenger: tu puoi. Serve: fonte live veloce
(score API ufficiale / streaming), script che confronta stato reale vs prezzo, esecuzione
subito. Edge tipico: 5-20 punti nelle finestre live. Occhio a fee taker (0,03 sports) e
al rischio che il mercato "sappia" qualcosa che tu non sai (infortunio, ritiro).

---

## S5 — Vantaggio conoscitivo locale 🇮🇹 *Fattibilità: ALTA — il nostro edge personale*

**Idea.** Sei italiano, a Torino: hai (a) lingua, (b) stampa locale, (c) fuso orario, (d)
passione calcistica. Polymarket quota Serie A, mercato italiani, eventi italiani con
liquidità media e Pricing fatto da trader USA che leggono Google Translate.

**Esempi concreti dove il prezzo spesso sbaglia:** conferme stampa di mercato ("tonnerà
l'allenatore X?" — le prime uscite sono su GianlucaDiMarzio/Fabrizio Romano ore prima
che il mercato si muova), probabilità di ritiro/infortunio comunicate da radio locali,
elezioni amministrative e regionali (sondaggi italiani istitutivi poco letti all'estero),
eventi culturali italiani (Festival di Sanremo ecc.).

**Come si costruisce:** lista di 10-15 fonti italiane verificabili (feed RSS/Telegram),
watcher su mercati correlati (lo scanner mostra quelli con volume sufficiente), regola:
si entra SOLO quando la fonte è ufficiale o 2 fonti indipendenti convergono.

---

## S6 — Bias sistematici (longshot bias) 📊 *Fattibilità: MEDIA, orizzonte lungo*

Nei mercati predittivi e nelle scommesse è documentato che i **longshot** (prezzi 0,01-0,10)
sono sistematicamente sopravvalutati e i favoriti (0,85-0,95) leggermente sottovalutati.
Strategia: vendere longshot di schifo (comprare NO a 0,92-0,97) su molti eventi indipendenti,
con sizing piccolo e capitolato. Vincere poco ma spesso, spread su centinaia di eventi.
Rischio massimo: quel longshot che si realizza e il tail risk non diversificato.
Da validare col dataset storico della Fase 2 PRIMA di credere al backtest.

## S7 — Flusso whale / copy trading 🐋 *Fattibilità: SPERIMENTALE*

Tutto on-chain: si vedono i wallet che storicamente vincono (leaderboard pubbliche).
Ipotesi: seguirli entro pochi minuti sui mercati poco liquidi amplifica il loro segnale.
Da studiare col Data API; rischio: sei tu l'uscita di sicurezza della balena.

## S8 — Resolution edge 📜 *Fattibilità: MEDIA-ALTA, sottovalutata da tutti*

Le regole di risoluzione sono testi legali. Chi le legge meglio del mercato vince senza
scommettere sulla notizia: mercati la cui definizione ("by September 15", "effectively
closed", "major offensive") rende un esito più probabile di quanto il prezzo implichi.
Richiede pazienza e letture fini, zero velocità. Perfetto per iniziare in paper.

---

## Checklist pre-trade (NON negoziabile, ogni volta)

1. ✅ **Edge netto ≥ 2 punti** dopo fee taker (o ordine maker a fee 0)
2. ✅ **Liquidità** sufficiente al tuo size (guarda `--mode book`: quanto c'è ai primi livelli?)
3. ✅ **Regole di risoluzione** lette per intero, fonte primaria identificata
4. ✅ **Sizing Kelly ¼ con cap 5%** (`lab/kelly.py`)
5. ✅ **Stato diario**: se -10% stop della giornata; 2 ricariche massime, poi si torna in paper
6. ✅ **Log** ogni trade nel registro (il paper engine lo fa già in automatico)

## Cosa automatizzare per primo (Fase 1 del piano)

1. **Watcher continuo** (cron/container): ogni 60s → scan closing+movers+arb, salva snapshot
   in `data/` → nasce il dataset storico per i backtest
2. **Alert** su regole: spread > 10 punti con volume > 20k (maker), paniere negRisk < 0,995
   (arb), mover 1h > 15 punti su mercato in chiusura (latency play)
3. **Agente notizie** per S5: monitor delle fonti italiane → confronto col prezzo → alert
4. Solo DOPO, quando c'è un edge misurato: pensare all'esecuzione, e solo su base legale
