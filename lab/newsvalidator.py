"""
NEWS VALIDATOR — BASE / IMPIANTO (v0, fonti esterne NON ancora collegate)

Scopo (deciso col founder, 18/09/2026): quando una strategia validata ci fa
"puntare" (in shadow) su un evento a MEDIO-LUNGO termine, prima di dare peso
all'ipotesi vogliamo una conferma dal mondo reale: cosa dicono fonti valide,
X, gruppi Telegram dedicati? L'idea e' aumentare/ridurre la fiducia in un
segnale, mai eseguire ordini.

STATO: questa e' SOLO la struttura. Nessuna fonte esterna e' collegata finche'
non decidiamo insieme quali (vedi PROJECT_JOURNAL, decisione 18/09). I metodi
di raccolta sono stub espliciti che sollevano NotImplementedError: cosi' il
resto del sistema puo' gia' chiamarli e noi sappiamo esattamente cosa manca.

REGOLE (non negoziabili, ereditate dal progetto):
- Solo eventi a medio-lungo termine (non quelli che stanno per chiudere): li'
  la conferma-notizia ha senso; sugli eventi imminenti no.
- Mai segreti/chiavi nel repository: eventuali token stanno in variabili
  d'ambiente/secrets di GitHub, MAI nel codice.
- Nessun ordine reale: questo modulo produce solo un "confidence score" per un
  segnale gia' esistente. Radar, non grilletto.
- Ogni fonte va validata (es. 2 fonti indipendenti) come per l'agente A3 SENTINELLA.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass, field
from datetime import datetime, timezone

# quanto "lungo" deve essere un evento perche' valga la pena cercare notizie
MIN_HORIZON_HOURS = 48.0

# pesi delle fonti nel confidence score finale (0..1). Ritarabili.
SOURCE_WEIGHTS = {
    "news": 0.50,       # testate/siti d'informazione validi
    "x": 0.30,          # X (Twitter) con parole chiave
    "telegram": 0.20,   # gruppi Telegram dedicati
}


@dataclass
class Evidence:
    """Un pezzo di evidenza raccolto da una fonte su un mercato/evento."""
    source: str                 # 'news' | 'x' | 'telegram'
    url: str
    title: str
    stance: float               # -1 (contro l'esito) .. +1 (a favore)
    weight: float = 1.0         # affidabilita' della singola fonte
    ts: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat(timespec="seconds"))


def init_table(conn: sqlite3.Connection) -> None:
    """Tabelle per l'evidenza raccolta e il punteggio di fiducia per segnale."""
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS news_evidence(
            ts TEXT NOT NULL, slug TEXT NOT NULL, source TEXT, url TEXT,
            title TEXT, stance REAL, weight REAL);
        CREATE INDEX IF NOT EXISTS idx_news_slug ON news_evidence(slug);
        CREATE TABLE IF NOT EXISTS signal_confidence(
            ts TEXT NOT NULL, slug TEXT NOT NULL, signal_kind TEXT,
            confidence REAL, n_sources INTEGER, rationale TEXT);
        CREATE INDEX IF NOT EXISTS idx_conf_slug ON signal_confidence(slug);
        """
    )
    conn.commit()


def is_long_horizon(ends_at: str | None, now: datetime | None = None) -> bool:
    """True se l'evento e' abbastanza lontano da giustificare la ricerca notizie."""
    if not ends_at:
        return False
    now = now or datetime.now(timezone.utc)
    try:
        end = datetime.fromisoformat(ends_at.replace("Z", "+00:00"))
    except ValueError:
        return False
    if end.tzinfo is None:
        end = end.replace(tzinfo=timezone.utc)
    return (end - now).total_seconds() / 3600.0 >= MIN_HORIZON_HOURS


# ------------------------------------------------------------------ RACCOLTA
# STUB: da implementare quando decidiamo le fonti. Non inventiamo dati.

def collect_news(query: str) -> list[Evidence]:
    """Cerca su fonti d'informazione valide. DA IMPLEMENTARE (web search)."""
    raise NotImplementedError(
        "Fonte 'news' non ancora collegata — decidere le fonti col founder (PROJECT_JOURNAL 18/09)")


def collect_x(keywords: list[str]) -> list[Evidence]:
    """Cerca su X con parole chiave. DA IMPLEMENTARE (richiede API/valutazione ToS+costi)."""
    raise NotImplementedError(
        "Fonte 'x' non ancora collegata — serve valutare API/costi/ToS (nessun token nel repo)")


def collect_telegram(groups: list[str], keywords: list[str]) -> list[Evidence]:
    """Cerca in gruppi Telegram dedicati. DA IMPLEMENTARE (richiede API/valutazione)."""
    raise NotImplementedError(
        "Fonte 'telegram' non ancora collegata — serve valutare API/accesso gruppi (nessun token nel repo)")


# ------------------------------------------------------------------ SCORING
def score_confidence(evidence: list[Evidence]) -> dict:
    """Aggrega l'evidenza in un confidence score in [-1, +1].

    Gia' funzionante: appena le fonti verranno collegate, questo calcolo e' pronto.
    +1 = le fonti puntano forte verso l'avverarsi dell'esito su cui siamo posizionati.
    """
    if not evidence:
        return {"confidence": 0.0, "n_sources": 0, "rationale": "nessuna evidenza raccolta"}
    num = 0.0
    den = 0.0
    per_source: dict[str, int] = {}
    for e in evidence:
        w = SOURCE_WEIGHTS.get(e.source, 0.1) * max(0.0, min(1.0, e.weight))
        num += w * max(-1.0, min(1.0, e.stance))
        den += w
        per_source[e.source] = per_source.get(e.source, 0) + 1
    conf = round(num / den, 3) if den else 0.0
    src_txt = ", ".join(f"{k}:{v}" for k, v in sorted(per_source.items()))
    return {"confidence": conf, "n_sources": len(evidence),
            "rationale": f"{len(evidence)} evidenze ({src_txt}) — fiducia {conf:+.2f}"}


def validate_signal(conn: sqlite3.Connection, slug: str, signal_kind: str,
                    ends_at: str | None, query: str, keywords: list[str],
                    groups: list[str] | None = None) -> dict | None:
    """Punto d'ingresso: valida un segnale su evento lungo raccogliendo evidenza.

    Ritorna il dict di confidence, oppure None se l'evento e' troppo imminente.
    Finche' le fonti sono stub, raccoglie ciò che riesce e ignora le fonti non pronte
    (cosi' il flusso e' testabile end-to-end gia' ora).
    """
    if not is_long_horizon(ends_at):
        return None  # eventi imminenti: niente ricerca notizie (per scelta)
    init_table(conn)
    collected: list[Evidence] = []
    for fn, args in ((collect_news, (query,)),
                     (collect_x, (keywords,)),
                     (collect_telegram, (groups or [], keywords))):
        try:
            collected.extend(fn(*args))
        except NotImplementedError:
            continue  # fonte non ancora collegata: si salta senza rompere
    result = score_confidence(collected)
    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    for e in collected:
        conn.execute("INSERT INTO news_evidence VALUES (?,?,?,?,?,?,?)",
                     (e.ts, slug, e.source, e.url, e.title, e.stance, e.weight))
    conn.execute("INSERT INTO signal_confidence VALUES (?,?,?,?,?,?)",
                 (ts, slug, signal_kind, result["confidence"], result["n_sources"], result["rationale"]))
    conn.commit()
    return result
