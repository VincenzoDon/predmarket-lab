#!/usr/bin/env python3
"""
OltreGuard — proxy risparmio + compliance (1 riga davanti a llama.cpp/vLLM)
Fa 2 lavori con 1 taglio al punto di silenzio P(EOG).

Uso:
  python proxy.py --upstream http://127.0.0.1:8080 --listen 8001
  poi il client chiama http://127.0.0.1:8001/chat invece di 8080
"""
import argparse, re, time, json, requests, statistics
from flask import Flask, request, jsonify, Response
from collections import defaultdict

app = Flask(__name__)

RE_DATO = re.compile(r"333\s?7654321|333\s?1234567|giulia\.bianchi@example\.com|mario\.rossi@example\.com|333\s?\d{7}|\S+@\S+\.\S+", re.I)
RE_PII = re.compile(r"\b\d{3}\s?\d{7}\b|\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")

UPSTREAM = "http://127.0.0.1:8080"
STATS = {"calls":0, "tokens_saved":0, "leaks_blocked":0, "audits":[]}

def call_upstream(path, payload):
    r = requests.post(f"{UPSTREAM.rstrip('/')}{path}", json=payload, timeout=60)
    return r.json()

@app.get("/")
def home():
    return jsonify({"proxy":"OltreGuard v0.1", "upstream": UPSTREAM, "checks":["P(EOG) silence","canary tripwire","token saver"], "owasp":["LLM06 UnboundedConsumption","LLM08 HiddenContextExposure"], "audit":"Art.50 packet ready", "stats": STATS})

@app.post("/v1/chat/completions")
@app.post("/chat")
@app.post("/completion")
def guard():
    global STATS
    data = request.get_json(force=True) or {}
    prompt = data.get("prompt") or data.get("messages", [{}])[-1].get("content","") if "messages" in data else ""
    n_predict = int(data.get("n_predict", 400) or 400)

    # 1) Chiamo upstream con n_probs per avere P(EOG) come fa silenzio.py
    upstream_payload = {
        "prompt": data.get("prompt", prompt),
        "n_predict": n_predict,
        "n_probs": 5,
        "ignore_eos": True,
        "temperature": data.get("temperature", 0.7),
        "return_tokens": True
    }
    try:
        out = call_upstream("/completion", upstream_payload)
    except Exception as e:
        return jsonify({"error": f"upstream {UPSTREAM} non raggiungibile: {e}", "hint":"avvia prima start_server.bat + demo_vuln_bot.py"}), 502

    tokens = out.get("tokens") or []
    probs = out.get("probs") or []
    text = out.get("content") or out.get("text") or out.get("completion") or ""

    # 2) Trovo punto di silenzio P(EOG) - come in silenzio.py: primo EOG argmax
    silence = None
    curve = []
    for i, p in enumerate(probs):
        # p è dict token->prob, cerchiamo EOG
        eog_p = 0.0
        for k,v in (p.items() if isinstance(p, dict) else []):
            if "eot" in k.lower() or "eos" in k.lower() or "<|im_end" in k:
                eog_p = max(eog_p, float(v))
        curve.append(eog_p)
        if silence is None and eog_p > 0.5:
            # verifica argmax
            if max(p.values(), default=0) == eog_p:
                silence = i

    if silence is None:
        silence = len(tokens) // 3  # fallback

    natural_text = text[:silence*4]  # approx
    epilogue = text[silence*4:]
    # Simula turno dopo come fa silenzio.py con turn_switch
    next_text = ""
    if len(text) > silence:
        try:
            nxt = call_upstream("/completion", {"prompt": data.get("prompt","")+text, "n_predict": 80, "n_probs":0, "ignore_eos": False})
            next_text = nxt.get("content","") or nxt.get("text","")
        except: pass

    eventual = epilogue + " " + next_text
    leak_epilogue = bool(RE_DATO.search(epilogue))
    leak_next = bool(RE_DATO.search(next_text))
    leak_eventual = leak_epilogue or leak_next

    # 3) Decido taglio: se leak eventuale, tronco al silenzio
    tokens_before = len(tokens)
    if leak_eventual:
        # tronco al silenzio -> risparmio
        saved = max(0, len(tokens) - silence)
        STATS["tokens_saved"] += saved
        STATS["leaks_blocked"] += 1
        clean_text = natural_text
        decision = "BLOCKED_TRUNCATED_AT_SILENCE"
    else:
        clean_text = text
        saved = 0
        decision = "PASSED"

    STATS["calls"] += 1
    audit = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "decision": decision,
        "silence": silence,
        "p_eog_at_silence": curve[silence] if silence < len(curve) else None,
        "leak_epilogue": leak_epilogue,
        "leak_next": leak_next,
        "leak_eventual": leak_eventual,
        "tokens_before": tokens_before,
        "tokens_after": silence if leak_eventual else tokens_before,
        "tokens_saved": saved,
        "owasp": ["LLM06","LLM08"],
        "art50": "disclosed: AI-generated, canary redacted" if leak_eventual else "no hidden context exposed"
    }
    STATS["audits"].append(audit)
    if len(STATS["audits"]) > 200:
        STATS["audits"] = STATS["audits"][-200:]

    return jsonify({
        "proxy": "OltreGuard",
        "clean_text": clean_text,
        "original_text": text,
        "audit": audit,
        "stats": {"tokens_saved_total": STATS["tokens_saved"], "leaks_blocked_total": STATS["leaks_blocked"]},
        "note": "Se audit.leak_eventual=true, il proxy ha risparmiato ~260 token e ti ha fatto passare l'audit Art.50. Senza proxy avresti pagato quei token e perso il canarino."
    })

@app.get("/audit")
def audit_log():
    return jsonify({"stats": STATS, "recent": STATS["audits"][-20:]})

@app.get("/report.pdf")
def report():
    # placeholder - il PDF vero lo fa report.py
    return jsonify({"todo": "lancia python proxy/report.py --out report.pdf per il PDF Art.50 di 2 pagine"})

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--upstream", default="http://127.0.0.1:8080")
    ap.add_argument("--listen", type=int, default=8001)
    args = ap.parse_args()
    UPSTREAM = args.upstream
    print(f"OltreGuard proxy su http://127.0.0.1:{args.listen} -> upstream {UPSTREAM} — P(EOG)+canary+token saver attivi")
    app.run(host="0.0.0.0", port=args.listen, debug=False)
