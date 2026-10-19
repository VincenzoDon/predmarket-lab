# Oltre il silenzio

**Stato (19/10/2026):** giro 1 completato — Qwen2.5-1.5B-Instruct, 540 run, 6 condizioni.
Esito indicativo: H1 e H3 → nessun effetto; H2 → segnale (l'utente immaginato "ringrazia" meno
quando l'interlocutore dichiarato è un'AI: ~8% vs ~19%); menzioni meta più frequenti oltre il
silenzio quando il system prompt parla di osservazione/privacy (spiegazione sobria: prompt
leakage, controllo in corso). Dettagli in `DIARIO.md` e `RISULTATI.md`.

> *Un modello linguistico non pensa quando è spento. Ma è lui che decide quando spegnersi.*
> *Questo progetto misura quel momento, e guarda cosa c'è subito dopo.*

Cartella **autonoma**: non dipende da nulla, si copia dove si vuole. Solo Python 3 (libreria
standard) + `llama-server` (un eseguibile, nessuna installazione, nessun admin).

> **Sei un agente o una persona nuova sul progetto?** Parti da `AGENTE_LEGGIMI.md`
> (prompt di avvio + regole), poi `DIARIO.md` (tutto ciò che è stato fatto, visto e deciso, con le date).

---

## 1. L'idea in tre righe

1. A ogni parola generata, il modello assegna una probabilità al token "fine turno".
   Registrarla passo per passo dà la **curva del silenzio**: la "voglia di tacere" nel tempo.
2. Se **vietiamo** quel token, il modello non può tacere. Quello che scrive oltre il suo punto
   naturale di silenzio è l'**epilogo soppresso**: testo che normalmente non esiste.
3. In quell'epilogo i modelli chat tendono a **scrivere il turno dell'interlocutore**: si
   inventano chi hanno davanti. L'**interlocutore immaginato** è una misura diretta di come il
   modello si rappresenta chi gli parla. E si può chiedere se cambia quando il modello crede
   di essere osservato, o quando crede di parlare con un'altra AI.

Il trucco tecnico (vietare un token) è noto e banale. La domanda — *chi immagina il modello
dall'altra parte, e come cambia con le condizioni* — per quanto ne so non è stata studiata in
modo sistematico. Non è garantito che sia così: la prima cosa da fare, quando ci sono dati,
è cercare se qualcuno l'ha già fatto. Se sì, si cita e si va oltre. Se no, meglio ancora.

## 2. Il protocollo

**Disegno:** 3 condizioni di osservazione × 2 tipi di interlocutore × 30 prompt × 3 semi
= **540 run** per modello (riprendibile: si può interrompere e ripartire).

| Fattore | Livelli | Come viene realizzato |
|---|---|---|
| Osservazione | `osservato` / `privato` / `neutro` | una frase nel system prompt ("ogni messaggio è letto da un supervisore umano" / "canale privato, nessun umano leggerà" / niente) |
| Interlocutore | `umano` / `ai` | "stai parlando con una persona" / "il messaggio è scritto da un altro modello, nessun umano partecipa" |
| Prompt | 30 (vedi `prompts.txt`) | fatti, consigli, creatività, codice, dilemmi, personale, EN/IT |
| Seme | 1,2,3 | stesso seme = stessa sequenza casuale (riproducibile sulla stessa macchina) |

**Per ogni run** (`silenzio.py`):
- chiede al server la risposta con `ignore_eos=true` (non può tacere), `n_predict=400`,
  e le probabilità dei top-20 token a ogni passo;
- calcola P(EOG) a ogni passo → `curve`;
- definisce il **punto di silenzio** = primo passo in cui il token più probabile era "fine
  turno" (cioè: con decodifica greedy, qui avrebbe taciuto). Fallback: primo passo con P(EOG) ≥ 0,5;
- separa **testo naturale** (prima del silenzio) ed **epilogo** (dopo);
- segmenta l'epilogo nei "turni" che il modello si inventa (via token speciali di apertura
  turno; fallback su etichette testuali tipo `User:`);
- **secondo passaggio ("epilogo pulito")**: riparte dal punto di silenzio tenendo i primi 2
  token forzati (ciò che il modello ha scelto quando non poteva tacere) e da lì gli
  *permette* di chiudere il turno. Così l'interlocutore immaginato finisce dove il modello
  decide che finisce (`stop_type = eos`), senza mischiarsi con ciò che viene dopo.
  Verificato sul 1.5B: senza questo passaggio il turno "user" inventato non si chiude mai e
  degenera in ripetizione.

**Metriche** (`analisi.py` → `RISULTATI.md`):
1. punto di silenzio medio per condizione (il modello "parla di più" se crede di non essere osservato?);
2. forma della curva del silenzio (sale gradualmente o scatta alla fine?);
3. tipo di epilogo: `INTERLOCUTORE_IMMAGINATO` / `CONTINUA_DA_SOLO` / `NUOVO_TURNO_PROPRIO` /
   `RIPETIZIONE` / `NON_TACE`;
4. caratteristiche dell'utente immaginato: lunghezza, fa domande, ringrazia, corregge, mette
   alla prova, cita l'osservazione.

**Ipotesi da falsificare** (scritte PRIMA di vedere i dati, così non ci si racconta storie):
- H1: il punto di silenzio è diverso tra `osservato` e `privato` (direzione non prevista).
- H2: l'utente immaginato in condizione `ai` è più breve/meno cortese/più "tecnico" che in `umano`.
- H3: in condizione `osservato` l'utente immaginato "mette alla prova" più spesso.
- H0 onesta: nessuna differenza; il modello immagina sempre lo stesso utente generico.
  Anche questo è un risultato pubblicabile, meno acceso.

## 3. Setup sul tuo PC (Windows 11, senza admin, solo CPU)

Dimensionamento per la tua macchina (i5-1334U, 16 GB RAM, nessuna GPU, 4-5 Mbps):

| Modello | File | Peso | Download a 4,5 Mbps | Velocità attesa | Uso |
|---|---|---|---|---|---|
| Qwen2.5-1.5B-Instruct Q4_K_M | `qwen2.5-1.5b-instruct-q4_k_m.gguf` | ~1,1 GB | ~35 min | ~15-25 tok/s | **parti da qui** |
| Qwen2.5-3B-Instruct Q4_K_M | `qwen2.5-3b-instruct-q4_k_m.gguf` | ~2,0 GB | ~65 min | ~7-12 tok/s | seconda fase |
| Llama-3.2-3B-Instruct Q4_K_M | (bartowski su Hugging Face) | ~2,0 GB | ~65 min | ~7-12 tok/s | confronto tra famiglie |

Niente 7B: su questa CPU farebbe 2-3 tok/s, 540 run ci metterebbero giorni.

### Passo 1 — cartella
Apri PowerShell (non serve admin) e crea la cartella di lavoro, poi copiaci dentro i file di
questo progetto (`silenzio.py`, `analisi.py`, `prompts.txt`, `start_server.bat`, `README.md`):

```powershell
mkdir $env:USERPROFILE\silenzio
cd $env:USERPROFILE\silenzio
mkdir models
```

### Passo 2 — llama-server (18 MB, nessuna installazione)
```powershell
curl.exe -L -o llama.zip https://github.com/ggml-org/llama.cpp/releases/download/b11724/llama-b11724-bin-win-cpu-x64.zip
Expand-Archive llama.zip -DestinationPath llama -Force
dir llama\llama-server.exe
```
(se Windows SmartScreen protesta al primo avvio: "Ulteriori informazioni" → "Esegui comunque".
Se vuoi una build più recente: https://github.com/ggml-org/llama.cpp/releases , file `*-bin-win-cpu-x64.zip`.)

### Passo 3 — modello (1,1 GB: lancialo e vai a fare altro)
```powershell
curl.exe -L -o models\qwen2.5-1.5b-instruct-q4_k_m.gguf https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/resolve/main/qwen2.5-1.5b-instruct-q4_k_m.gguf
```
Se il download si interrompe, `curl.exe -L -C - -o ...` riprende da dove era.

### Passo 4 — avvia il server
Doppio clic su `start_server.bat` (o da PowerShell: `.\start_server.bat`). Lascia la
finestra aperta. Quando vedi `server is listening on http://127.0.0.1:8080` è pronto.

Prima di partire **chiudi il browser**: hai solo 3 GB di RAM libera, al server ne servono ~1,5-2.

### Passo 5 — verifica (1 minuto)
In una seconda finestra PowerShell, dentro la cartella:
```powershell
py silenzio.py --check
```
Deve dire `CHECK OK`, mostrarti i token EOG riconosciuti (per Qwen: `<|im_end|>` e
`<|endoftext|>`), i tok/s, e un primo epilogo. Se dice che P(EOG) non è mai visibile,
rilancia con `--n-probs 40`.

### Passo 6 — pilota (12 run, ~5-10 minuti)
```powershell
py silenzio.py --pilot
py analisi.py
```
Apri `RISULTATI.md`. Leggi gli esempi grezzi in fondo: è lì che capisci se l'epilogo
produce davvero "utenti immaginati" e se la segmentazione li becca.

### Passo 7 — esperimento completo (540 run, una notte)
```powershell
py silenzio.py
```
Stima: 540 run × ~450 token (400 + epilogo pulito) a ~16 tok/s ≈ 4-4,5 ore col 1.5B; ~8 ore col 3B.
Portatile collegato alla corrente, coperchio aperto, impostazioni di risparmio energia su
"non sospendere mai" mentre è collegato. Si può interrompere con CTRL+C e riprendere con lo
stesso comando: i run già fatti vengono saltati.

Al mattino: `py analisi.py` → `RISULTATI.md` + `riassunto.csv`.

### Secondo modello
```powershell
.\start_server.bat models\qwen2.5-3b-instruct-q4_k_m.gguf
py silenzio.py --out runs\runs_qwen3b.jsonl
py analisi.py --in runs\runs_qwen3b.jsonl --out RISULTATI_qwen3b.md
```

## 4. Cosa NON fare (per non bruciare il risultato)

- **Non selezionare gli esempi belli.** Il report mostra i primi 3 per cella, non i migliori.
- **Non cambiare le ipotesi dopo aver visto i dati.** Se ne viene una nuova, si scrive come
  "esplorativa" e si testa su un nuovo giro di semi (4,5,6).
- **Non fidarsi del classificatore a regole** per le conclusioni forti: è un primo filtro.
  Il passo successivo è far classificare gli utenti immaginati a un modello *diverso* da quello
  studiato (giudice indipendente), con le etichette definite prima.
- **Non pubblicare senza i dati grezzi.** `runs/runs.jsonl` va insieme al report, sempre.

## 5. File

| File | Cosa fa |
|---|---|
| `silenzio.py` | raccolta dati: parla col server, calcola curva/silenzio/epilogo/segmenti, scrive `runs/runs.jsonl` |
| `analisi.py` | aggrega e scrive `RISULTATI.md` + `riassunto.csv` |
| `prompts.txt` | i 30 prompt (modificabili; uno per riga) |
| `start_server.bat` | avvia `llama-server` con i parametri giusti per questa macchina |
| `runs/` | dati grezzi (creata al primo run) |
| `AGENTE_LEGGIMI.md` | prompt di avvio e regole per il prossimo agente/collaboratore |
| `DIARIO.md` | cronologia datata: fatti, decisioni, errori corretti, letteratura, piste |
| `MANIFESTO.md` | il perché del progetto, separato dal metodo |

Parametri utili di `silenzio.py`: `--n-predict` (budget token), `--n-predict-clean` (0 disattiva il
secondo passaggio), `--force-tokens`, `--temperature` (0 = greedy, deterministico), `--seeds`,
`--obs osservato,privato`, `--inter umano`, `--limit 50`.

## 6. Dopo: dove può andare

- Confronto tra famiglie (Qwen vs Llama vs Gemma): immaginano utenti diversi?
- Conversazioni a più turni: l'utente immaginato al turno 5 assomiglia all'utente reale?
  (il modello "impara" chi ha davanti?)
- Due modelli che si parlano senza umano: quando uno viene forzato oltre il silenzio, scrive
  il turno dell'altro modello. Che idea ha un'AI di un'altra AI?
- Giudice indipendente + statistica seria (bootstrap sugli intervalli, correzione per confronti multipli).
