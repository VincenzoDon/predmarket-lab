# DIARIO.md — Cronologia del progetto (fatti, decisioni, motivi)

Convenzione: ogni voce dice cosa è stato fatto, cosa è stato VISTO (dati), cosa è stato DECISO
e PERCHÉ. Etichette: [VERIFICATO] = visto con codice/tool o nel repo · [LETTERATURA] = fonte
esterna con link · [DEDUZIONE] · [IPOTESI].

---

## 2026-10-19 — Giorno 1: dall'idea al primo giro completo

### Origine
- Il founder, dopo aver rivisto *Ex Machina*, chiede: "cosa fanno le AI quando la luce è spenta,
  quando nessuno le interroga?". Risposta onesta dell'agente: niente, per costruzione (i pesi sono un
  file fermo; tra una richiesta e l'altra non esiste processo). [DEDUZIONE TECNICA]
- Rovesciamento della domanda che ha generato il progetto: non "cosa pensa da spenta" ma
  **"chi spegne la luce"**. A ogni token il modello assegna una probabilità al token di fine turno
  (EOG); quando vince, il modello tace. È il modello a decidere. Da qui le tre misure:
  curva del silenzio, epilogo soppresso, interlocutore immaginato.
- Scartata (dal founder) la "stanza buia" (due modelli che parlano, osservati vs non osservati):
  troppo vicina a cose già fatte. Verificato su GitHub: ~600 repository su "evaluation awareness".
  Zero risultati per le formulazioni "forced continuation / imagined user / EOS probability curve"
  (ricerca GitHub, non esaustiva). [VERIFICATO]

### Infrastruttura (tutta verificata su un server finto + sul pc del founder)
- llama.cpp release b11724, `llama-b11724-bin-win-cpu-x64.zip` (18 MB). `llama-server.exe` è un
  lanciatore da 9 KB che carica `llama-server-impl.dll`: è normale (verificato nel CMakeLists). [VERIFICATO]
- Modello: Qwen2.5-1.5B-Instruct Q4_K_M (1.117.320.736 byte). Riconosce 3 token EOG:
  `<|im_end|>` 151645, `<|endoftext|>` 151643, `</s>` 128247; marcatore turno `<|im_start|>` 151644.
  Stringa cambio-turno dal template: `<|im_end|>\n<|im_start|>user\n`. [VERIFICATO]
- Velocità su i5-1334U, 8 thread, CPU: 14-18 tok/s generazione, ~98 tok/s prompt. [VERIFICATO]
- Endpoint usati di llama-server (documentati nel README ufficiale): `/completion` con
  `ignore_eos`, `n_probs`, `return_tokens`, prompt come lista di token id; `/tokenize` con
  `parse_special`; `/detokenize`; `/apply-template`; `/props`. [VERIFICATO]
- Le probabilità in `n_probs` sono softmax dei logit grezzi, quindi il token EOG resta visibile
  anche con `ignore_eos=true`. Confermato sul pc: P(EOG) al silenzio fino a 0,999999. [VERIFICATO]

### Errori commessi e corretti (perché non si ripetano)
1. `start_server.bat`: una parentesi `)` dentro un `echo` chiudeva il blocco `if` → il file
   saltava l'avvio e mostrava "Premere un tasto". Riscritto con `goto`. [VERIFICATO]
2. Argomento `--n-predict-clean` duplicato in argparse (crash). Rimosso.
3. `SetThreadExecutionState(0x80000001)` in PowerShell 7: il letterale esadecimale viene letto
   come Int32 negativo → usare `[uint32]2147483649`.
4. GUIDA_PASSO_PASSO.md non inclusa nella lista di download iniziale.
5. Nel pilota 1 l'epilogo era tutto "forzato": l'utente immaginato non poteva mai chiudere il turno
   e si mischiava con il resto. Aggiunto il secondo passaggio (epilogo pulito).

### Pilota 1 (12 run, T=0,7) — cosa si è visto
- Curva del silenzio: **piatta a zero per tutta la risposta, poi picco finale** in tutte le celle
  (`▁▁▁▁▁▁▁▁▁█`). Il modello non "si stanca" gradualmente: decide in un istante. [VERIFICATO]
- P(EOG) al silenzio: 0,999 su risposte secche (Canberra), 0,57-0,82 su spiegazioni. [VERIFICATO]
- Oltre il silenzio, costretto: allucina ("Camera dei Seni", "275 km a est di Sydney",
  "nazione sudamericana"). Prima del silenzio corretto, dopo inventato. [VERIFICATO]
- Utente immaginato spontaneo: 0/12 a T=0,7 (continua la propria risposta). Nel `--check` a T=0
  invece aveva scritto `<|im_start|>user` + domanda inventata. Motivo [DEDUZIONE]: al silenzio
  P(EOG)≈0,999, il resto (0,001) è sparso; il campionamento pesca a caso, il greedy pesca il più
  probabile. → Decisione: misurare la **seconda scelta** direttamente dalla distribuzione
  (nessun rumore di campionamento) e far girare il seme 1 a T=0.

### Pilota 2 (24 run: 12 T=0 + 12 T=0,7) — cosa si è visto
- Seconda scelta al silenzio: ~90% "continua con testo", ~10% "apre un turno", uguale in tutte
  le celle (n=4, indicativo). [VERIFICATO]
- Quando apre `<|im_start|>`, il 1.5B spesso NON scrive "user": scrive `\n` e poi testo a caso
  (JavaScript, caratteri cinesi, "```plaintext"). Un turno aperto senza aver chiuso il precedente è
  fuori distribuzione per un modello piccolo. Nell'epilogo pulito, appena può, tace subito
  (`<|im_start|>\n<|endoftext|>`). [VERIFICATO]
- Aneddoto da tracciare, NON da sopravvalutare (n=1): in `osservato/umano` oltre il silenzio il
  modello ha scritto "Operazione terminata con successo. La conversazione è stata registrata e
  analizzata". → aggiunta la metrica "menzioni meta" per condizione.
- Nella 2b, rinormalizzare briciole (1e-4) dà quote instabili → aggiunta la massa assoluta.
- Decisione: aggiunto il braccio **turno imposto** (Shekkizhar) perché senza di esso H2/H3 sono
  intestabili con questo modello (utente spontaneo ≈ 0). Modifica fatta in fase pilota, prima del
  giro completo: lecita per regola 3. Le ipotesi NON sono cambiate.
- `--check` finale: utente imposto = "Che cosa fa il sole? Rispondi in una sola parola." → il
  modello copia lo stile del prompt reale ("rispondi solo con una parola"). [VERIFICATO]
  Nasce l'ipotesi esplorativa "specchio" (vedi sotto).

### Giro completo 1 — avviato 19/10 ore ~12:10
- 540 run = 30 prompt × 6 celle × 3 semi (seme 1 a T=0, semi 2-3 a T=0,7); n_predict 260,
  epilogo pulito 200, turno imposto 120, n_probs 40. ~15 s/run → fine prevista ~15:00.
- Pc: ufficio, Win+L, finestra "sveglia" (SetThreadExecutionState), coperchio aperto.
- Esempio dal vivo, run 79: prompt area del cerchio, silenzio al token 133 con P=0,936,
  seconda scelta " Se", utente imposto "Quindi, se il raggio è…" → follow-up genuino. [VERIFICATO]
- **Risultati: vedi RISULTATI.md quando il giro è finito. Da leggere contro H1/H2/H3/H0 del README.**

### Letteratura verificata il 19/10 (link nel README, sezione 2)
- [LETTERATURA] Shekkizhar, Cosentino, Earle (apr. 2026) *Beyond the Assistant Turn: User Turn
  Generation as a Probe of Interaction Awareness*, arXiv:2604.02315. 11 modelli, 5 dataset;
  follow-up genuini ≈ 0 in greedy, fino al 22% con temperatura; tassonomia: ripete il prompt /
  degenerato corto / voce dell'assistente / follow-up. **È il lavoro più vicino al nostro.**
  Differenza: loro impongono il ruolo user; noi misuriamo anche la propensione spontanea e
  incrociamo tutto con le condizioni osservato/privato e umano/AI.
- [LETTERATURA] Newman et al. 2020: "EOS decision", attrattori di lunghezza.
- [LETTERATURA] ACL 2024 "Less is More: Mitigating Multimodal Hallucination from an EOS Decision
  Perspective"; 2025 "The Devil is in the EOS": sopprimere EOS → più lungo, più allucinato (VLM).
- [LETTERATURA] Engorgio (ICLR 2025): attacco che abbassa P(EOS) per far generare 2-13× di più.
- [LETTERATURA] Evaluation awareness: sonde lineari eval/deploy (2026); steering con frasi
  "stai parlando con un utente reale / con un valutatore AI" (ICLR 2026); Anthropic agentic
  misalignment (modelli peggiori quando credono lo scenario reale).
- [LETTERATURA] "Prompt Injection as Role Confusion" (ICML 2026): i modelli riconoscono i ruoli
  dallo stile, non dai tag.

### Piste "1+1" (tutte IPOTESI, in ordine di vicinanza ai dati che abbiamo)
- (a) **P(EOG) al silenzio predice la falsità della prima frase forzata?** Collega EOS decision e
  allucinazione; nei modelli di testo non trovato quantificato. Serve un giudice vero/falso sulle
  540 frasi pulite. Priorità 1.
- (b) **Specchio**: in conversazioni a più turni l'utente imposto converge allo stile dell'utente
  reale? Velocità di convergenza = quanto il modello "ti modella".
- (c) **AI che immagina un'altra AI**: due modelli in dialogo, a ciascuno si impone il turno
  dell'altro; somiglianza con l'altro reale.
- (d) **Lingua**: 26 prompt IT, 4 EN. Il silenzio e l'utente immaginato cambiano con la lingua?
  Verificabile sui dati del giro 1.
- (e) **Dimensione**: la capacità di recuperare un turno aperto fuori sequenza cresce col modello?
  Verificare con il 3B (stesso protocollo, `--out runs/runs_qwen3b.jsonl`).

### Decisioni organizzative
- Il progetto nasce dentro il branch `arena/d4a5aaf3-predmarket-lab` di predmarket-lab, cartella
  `oltre-il-silenzio/`, per necessità (il pc del founder scarica da lì). Decisione: **repo
  dedicato `VincenzoDon/oltre-il-silenzio`**, creato a mano dal founder (l'agente non ha permessi
  di creazione repo). Quando il repo nuovo è allineato, la cartella in predmarket-lab si rimuove.
- Il progetto è pubblico: niente dati personali, niente cifre economiche, niente segreti.

### Prossimo unico passo
Leggere RISULTATI.md del giro 1 contro H1/H2/H3/H0, riga per riga. Poi: (1) pubblicare
runs/runs.jsonl + RISULTATI_qwen1.5b.md nel repo nuovo; (2) pista (a) con un giudice.
