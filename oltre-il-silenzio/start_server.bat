@echo off
REM Avvia llama-server sul modello scelto. Uso:
REM   start_server.bat                      -> modello di default (1.5B)
REM   start_server.bat models\altro.gguf    -> altro modello
cd /d "%~dp0"
set MODEL=models\qwen2.5-1.5b-instruct-q4_k_m.gguf
if not "%~1"=="" set MODEL=%~1
if not exist "%MODEL%" (
  echo Modello non trovato: %MODEL%
  echo Scaricalo nella cartella models\ (vedi README.md)
  pause
  exit /b 1
)
echo Avvio llama-server su %MODEL% ...
echo Lascia questa finestra aperta. Per fermare: CTRL+C
llama\llama-server.exe -m "%MODEL%" -c 4096 -t 8 --port 8080 --host 127.0.0.1 --jinja
pause
