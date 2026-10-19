# Guida passo-passo (Windows 11, senza admin, solo CPU)

Ogni comando: copia, incolla in PowerShell, Invio, aspetta che torni il cursore.

## 0. Prima di cominciare
1. Portatile attaccato alla corrente.
2. Chiudi browser e programmi inutili.
3. Tasto Windows -> scrivi `powershell` -> Invio (NON come amministratore).

## 1. Cartella di lavoro
```powershell
mkdir $env:USERPROFILE\silenzio
cd $env:USERPROFILE\silenzio
mkdir models
```

## 2. Scarica i file del progetto
```powershell
$u = "https://raw.githubusercontent.com/VincenzoDon/predmarket-lab/arena/d4a5aaf3-predmarket-lab/oltre-il-silenzio"
curl.exe -L -o silenzio.py "$u/silenzio.py"
curl.exe -L -o analisi.py "$u/analisi.py"
curl.exe -L -o prompts.txt "$u/prompts.txt"
curl.exe -L -o start_server.bat "$u/start_server.bat"
curl.exe -L -o README.md "$u/README.md"
dir
```
Controllo: 5 file + cartella models. File da 0 byte -> rilancia quel comando.

## 3. Scarica llama-server (18 MB)
```powershell
curl.exe -L -o llama.zip https://github.com/ggml-org/llama.cpp/releases/download/b11724/llama-b11724-bin-win-cpu-x64.zip
Expand-Archive llama.zip -DestinationPath llama -Force
dir llama\llama-server.exe
```

## 4. Scarica il modello (1,1 GB, ~35-40 min)
```powershell
curl.exe -L -C - -o models\qwen2.5-1.5b-instruct-q4_k_m.gguf https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/resolve/main/qwen2.5-1.5b-instruct-q4_k_m.gguf
```
Se si interrompe: rilancia lo stesso comando, riprende (`-C -`).
Controllo: `dir models` -> circa 1.100.000.000 byte.

## 5. Avvia il server
```powershell
.\start_server.bat
```
- SmartScreen: "Ulteriori informazioni" -> "Esegui comunque".
- Firewall: "Consenti accesso" (o Annulla, funziona lo stesso).
- Pronto quando vedi: `server is listening on http://127.0.0.1:8080`.
- LASCIA QUESTA FINESTRA APERTA.

## 6. Verifica
Seconda finestra PowerShell:
```powershell
cd $env:USERPROFILE\silenzio
py silenzio.py --check
```
Deve finire con `CHECK OK`. Altrimenti: copia tutto l'output e incollalo in chat.

## 7. Pilota (12 run, 5-10 min)
```powershell
py silenzio.py --pilot
py analisi.py
notepad RISULTATI.md
```
Leggi la sezione 5 (esempi grezzi). Incolla il report in chat prima di procedere.

## 8. La notte (540 run, ~3-4 ore)
1. Impostazioni -> Sistema -> Alimentazione e batteria -> Schermo e sospensione ->
   "Se collegato, sospendi il dispositivo dopo: Mai".
2. Coperchio aperto, corrente attaccata, server acceso nella prima finestra.
3. Seconda finestra: `py silenzio.py`
4. Mattina: `py analisi.py` poi `notepad RISULTATI.md` -> incolla in chat (anche riassunto.csv).

## Se qualcosa va storto
| Sintomo | Cosa fare |
|---|---|
| `py` non riconosciuto | prova `python3 silenzio.py --check`; se no, chiedi |
| `curl.exe` non riconosciuto | chiedi la versione con Invoke-WebRequest |
| porta 8080 occupata | in start_server.bat cambia 8080 in 8081; script con `--server http://127.0.0.1:8081` |
| pc lentissimo | chiudi altri programmi: servono ~2 GB RAM libera |
| interrotto durante la notte | rilancia `py silenzio.py`: salta i run già fatti |
| errori rossi | Ctrl+C, copia gli errori in chat |
