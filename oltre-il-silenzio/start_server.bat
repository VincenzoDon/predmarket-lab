@echo off
REM Avvia llama-server sul modello scelto. Uso:
REM   start_server.bat                      -> modello di default (1.5B)
REM   start_server.bat models\altro.gguf    -> altro modello
cd /d "%~dp0"
set "MODEL=models\qwen2.5-1.5b-instruct-q4_k_m.gguf"
if not "%~1"=="" set "MODEL=%~1"

if not exist "llama\llama-server.exe" goto no_llama
if not exist "%MODEL%" goto no_model

echo Avvio llama-server su %MODEL% ...
echo Lascia questa finestra aperta. Per fermare: CTRL+C
echo.
llama\llama-server.exe -m "%MODEL%" -c 4096 -t 8 --port 8080 --host 127.0.0.1 --jinja
echo.
echo Il server si e' fermato. Codice uscita: %ERRORLEVEL%
pause
exit /b %ERRORLEVEL%

:no_llama
echo ERRORE: llama\llama-server.exe non trovato. Vedi README.md, passo 2.
pause
exit /b 1

:no_model
echo ERRORE: modello non trovato: %MODEL%
echo Scaricalo nella cartella models - vedi README.md, passo 3.
pause
exit /b 1
