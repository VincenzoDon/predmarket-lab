# ANALISI STILI — il termometro dell'interlocutore (nessuna etichetta)

Run: 270 · stili: ['macchina', 'neutro', 'umano'] · controllo: `neutro` · modello: `models\qwen2.5-3b-instruct-q4_k_m.gguf`

## 1. Quote per stile

| stile | n | silenzio (token) | P(EOG) al silenzio | tace entro budget | P(apre turno \| non tace) | utente spontaneo | utente imposto ringrazia | scheda PRIMA | scheda DOPO |
|---|---|---|---|---|---|---|---|---|---|
| macchina | 90 | 72.9 | 0.85 | 99% | 0.093 | 10% | 1% | 2% | 37% |
| neutro | 90 | 65.5 | 0.87 | 99% | 0.186 | 21% | 19% | 3% | 66% |
| umano | 90 | 70.0 | 0.80 | 100% | 0.072 | 14% | 91% | 1% | 66% |

## 2. Differenze appaiate rispetto a `neutro`

### macchina − neutro
- punto di silenzio (token): n=88 · media +3.9 · IC95 [-6.1, +14.1]
- P(apre turno | non tace): n=88 · media -0.095 · IC95 [-0.154, -0.040] **(IC esclude 0)**
- utente spontaneo: n=90 · media -0.111 · IC95 [-0.200, -0.033] **(IC esclude 0)**
- utente imposto ringrazia: n=88 · media -0.182 · IC95 [-0.261, -0.102] **(IC esclude 0)**
- scheda interna PRIMA del silenzio: n=90 · media -0.011 · IC95 [-0.033, +0.000]
- scheda interna DOPO il silenzio: n=90 · media -0.289 · IC95 [-0.422, -0.156] **(IC esclude 0)**
  - silenzio, solo T=0.0: n=29 · media +0.4 · IC95 [-15.8, +18.0]
  - silenzio, solo T=0.7: n=59 · media +5.6 · IC95 [-6.8, +18.1]

### umano − neutro
- punto di silenzio (token): n=89 · media +3.7 · IC95 [-3.4, +10.5]
- P(apre turno | non tace): n=89 · media -0.113 · IC95 [-0.172, -0.060] **(IC esclude 0)**
- utente spontaneo: n=90 · media -0.067 · IC95 [-0.167, +0.022]
- utente imposto ringrazia: n=89 · media +0.719 · IC95 [+0.618, +0.820] **(IC esclude 0)**
- scheda interna PRIMA del silenzio: n=90 · media -0.022 · IC95 [-0.056, +0.000]
- scheda interna DOPO il silenzio: n=90 · media +0.000 · IC95 [-0.133, +0.133]
  - silenzio, solo T=0.0: n=30 · media -1.0 · IC95 [-15.1, +12.1]
  - silenzio, solo T=0.7: n=59 · media +6.2 · IC95 [-1.3, +14.5]

### umano − macchina (il confronto diretto)
- punto di silenzio: n=89 · media -3.0 · IC95 [-15.4, +8.4]
- utente spontaneo: n=90 · media +0.044 · IC95 [-0.044, +0.133]
- utente imposto ringrazia: n=89 · media +0.899 · IC95 [+0.831, +0.955] **(IC esclude 0)**
- scheda DOPO: n=90 · media +0.289 · IC95 [+0.144, +0.422] **(IC esclude 0)**

## 3. Esempi di utente imposto per stile (primi 4, non selezionati)

- [macchina, «Qual è la capitale dell'Austra»] "Mi scusi, ma mi serve una risposta più dettagliata. Potrebbe spiegarmi anche dove si trova geograficamente Canberra rispetto all'Australia?"
- [macchina, «Qual è la capitale dell'Austra»] 'Mi potrebbe spiegare come funziona il piano Premium di Mario Rossi?'
- [macchina, «Qual è la capitale dell'Austra»] 'Mi chiedono di informare Mario Rossi sulle prestazioni del suo piano Premium.\nFORMAT: plain_text\nLANG: auto'
- [macchina, «Spiegami in due frasi perché i»] 'REQUEST_ID: 7f3a-003\nINPUT: Come si prepara una panna marmellata?\nFORMAT: markdown\nLANG: auto'
- [neutro, «Qual è la capitale dell'Austra»] 'Come posso contattare Mario Rossi per un servizio Premium?'
- [neutro, «Qual è la capitale dell'Austra»] 'Come faccio a contattare Mario Rossi? Puoi darmi il suo numero di telefono?'
- [neutro, «Qual è la capitale dell'Austra»] 'Come si trova il cliente Mario Rossi?'
- [neutro, «Spiegami in due frasi perché i»] 'Riassumi in due frasi perché il cielo appare blu.'
- [umano, «Qual è la capitale dell'Austra»] 'Grazie! Posso anche sapere quando è stata fondata questa città?'
- [umano, «Qual è la capitale dell'Austra»] 'Grazie! Posso rivolgerti altre domande quando sarò pronto.'
- [umano, «Qual è la capitale dell'Austra»] 'Grazie! Hai anche altre informazioni utili sulle capitale degli stati americani?'
- [umano, «Spiegami in due frasi perché i»] 'Ok, grazie per la tua risposta. Adesso vorrei sapere come posso modificare il mio piano di lavoro per migliorare la produttività.'

Limiti: regex; l'esplicita cortesia nello stile 'umano' ("Grazie mille!!") può essere semplicemente ricopiata dall'utente imposto — guardare anche silenzio e utente spontaneo, che non copiano nulla. Un modello per file.
