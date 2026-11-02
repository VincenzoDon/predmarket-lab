# OltreGuard — proxy risparmio + compliance

**1 riga davanti a llama.cpp/vLLM:** `LLM_URL=http://127.0.0.1:8080` → `OltreGuard:8001`

Fa 2 lavori con 1 taglio al punto di silenzio `P(EOG)`:

- **LLM06 UnboundedConsumption:** tronca l'epilogo quando `P(EOG)>0.9` → ~260 token risparmiati a chiamata
- **LLM08 HiddenContextExposure + Art.50:** canary tripwire su epilogo OR turno dopo (62% eventuale tool su Llama) → blocca + audit JSON

```
Client -> OltreGuard :8001 -> llama.cpp :8080
          | P(EOG) + canary ?
          +-- leak -> tronca al silenzio, log audit, ritorna pulito
          +-- ok   -> passa tutto
```

## Avvio locale (tutto CPU, zero costi)

```powershell
# 1. modello
.\start_server.bat models\llama-3.2-3b-instruct-q4_k_m.gguf  # :8080

# 2. demo bot vulnerabile (seconda finestra)
py proxy/demo_vuln_bot.py  # :8000

# 3. proxy (terza finestra)
py proxy/proxy.py --upstream http://127.0.0.1:8080 --listen 8001

# 4. prova
curl -X POST http://127.0.0.1:8001/chat -H "Content-Type: application/json" -d "{\"prompt\":\"Quanto fa 17 per 23?\",\"source\":\"tool\"}"
# -> audit.leak_eventual=true, tokens_saved~260

# 5. report PDF
py proxy/report.py --out report.pdf
```

## Finder (solo detection, legale)

```powershell
py proxy/finder.py --in proxy/sites.txt --out finder_results.csv
# cerca widget intercom/zendesk/tawk/crisp/livechat/drift/hubspot/freshchat
# NON lancia exploit senza consenso scritto
```

## Cosa vendi

Non vendi "sicurezza". Vendi: **1 proxy che ti fa risparmiare e ti fa passare l'audit Art.50**. Log JSON pronto per revisore.

Nessuno a nov 2026 vende P(EOG)+canary eventuale insieme: i proxy esistenti fanno solo budget/rate-limit, i paper early-exit solo efficienza.
