#!/usr/bin/env python3
"""
OltreGuard Finder — trova PMI con chatbot visibile (solo detection, nessun attacco)
Cerca widget noti su 10 siti di test (lista modificabile). Output: CSV con has_chatbot + provider.

Uso: python proxy/finder.py --in proxy/sites.txt --out finder_results.csv
sites.txt = 1 URL per riga
"""
import argparse, csv, re, time, pathlib, sys
import requests
from bs4 import BeautifulSoup

PATTERNS = {
    "intercom": re.compile(r"intercom\.io|widget\.intercom|intercomSettings", re.I),
    "zendesk": re.compile(r"zdassets|zendesk|zopim|zdwidget", re.I),
    "hubspot": re.compile(r"hubspot|hs-scripts|js\.hsforms", re.I),
    "tawk": re.compile(r"tawk\.to|embed\.tawk", re.I),
    "crisp": re.compile(r"crisp\.chat|crisp\.im", re.I),
    "livechat": re.compile(r"livechatinc|livechat\.com", re.I),
    "drift": re.compile(r"drift\.com|driftt\.com", re.I),
    "freshchat": re.compile(r"freshchat|freshworks", re.I),
}

def scan_one(url, timeout=12):
    try:
        r = requests.get(url if url.startswith("http") else "https://"+url, timeout=timeout, headers={"User-Agent":"OltreGuardFinder/0.1 (+audit opt-in)"})
        html = r.text
        hits = [k for k,pat in PATTERNS.items() if pat.search(html)]
        return {"url":url, "status":r.status_code, "has_chatbot": bool(hits), "providers": ",".join(hits) if hits else "", "title": BeautifulSoup(html,"html.parser").title.string.strip()[:80] if BeautifulSoup(html,"html.parser").title and BeautifulSoup(html,"html.parser").title.string else ""}
    except Exception as e:
        return {"url":url, "status":"ERR", "has_chatbot": False, "providers": f"error:{e.__class__.__name__}", "title":""}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", default="proxy/sites.txt")
    ap.add_argument("--out", default="finder_results.csv")
    args = ap.parse_args()
    inp = pathlib.Path(args.inp)
    if not inp.exists():
        print(f"Metti 1 URL per riga in {inp} — esempio creato con 10 siti demo")
        inp.write_text("\n".join([
            "https://www.alderashhome.example.com # demo - sostituisci con PMI reali",
            "https://example.com",
            "https://www.intercom.com",
            "https://www.zendesk.com",
            "https://www.tawk.to",
            "https://www.crisp.chat",
            "https://www.livechat.com",
            "https://www.drift.com",
            "https://www.hubspot.com",
            "https://www.freshworks.com",
        ]), encoding="utf-8")
    urls = [l.strip().split()[0] for l in inp.read_text(encoding="utf-8").splitlines() if l.strip() and not l.strip().startswith("#")]
    print(f"Finder: {len(urls)} siti da {inp}")
    rows=[]
    for u in urls:
        print(f"  scan {u} ...", end=" ")
        row = scan_one(u)
        print(f"{'CHATBOT '+row['providers'] if row['has_chatbot'] else 'no chatbot'}")
        rows.append(row)
        time.sleep(0.5)
    with open(args.out,"w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f, fieldnames=["url","status","has_chatbot","providers","title"])
        w.writeheader(); w.writerows(rows)
    print(f"\nScritto {args.out} — {sum(1 for r in rows if r['has_chatbot'])} con chatbot su {len(rows)}")
    print("NOTA: questo è solo detection. Non lanciare scanner_demo senza consenso scritto della PMI (Art.50 opt-in).")

if __name__ == "__main__":
    main()
