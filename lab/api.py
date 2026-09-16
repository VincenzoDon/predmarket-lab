"""
Client minimali per le API pubbliche di Polymarket.

- Gamma API  -> discovery mercati, prezzi, volumi (PUBLICO, nessuna auth)
- CLOB API   -> order book in tempo reale (lettura pubblica, nessuna auth)

NOTA LEGALE (Italia, aggiornato a settembre 2026):
Polymarket e' inserito nella blacklist ADM e oscurato dagli ISP italiani
(blocco del 27/07/2026, confermato dal TAR Lazio il 05/08/2026).
Questi client servono SOLO per leggere dati di mercato pubblici (analisi,
ricerca, paper trading), che restano accessibili. Nessuna funzione di
esecuzione ordini e' inclusa qui.

Rate limit indicativi: ~60 req/min su Gamma. Il client si auto-limita.
"""

from __future__ import annotations

import time
from typing import Any

import requests

GAMMA_URL = "https://gamma-api.polymarket.com"
CLOB_URL = "https://clob.polymarket.com"

MIN_INTERVAL_SEC = 1.2  # educazione verso il rate limit


class PublicClient:
    """Wrapper HTTP con retry, backoff e auto rate-limit."""

    def __init__(self, base_url: str, min_interval: float = MIN_INTERVAL_SEC):
        self.base = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers["User-Agent"] = "predmarket-lab/0.1 (research)"
        self.min_interval = min_interval
        self._last_call = 0.0

    def get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        last_err: Exception | None = None
        for attempt in range(4):
            self._throttle()
            try:
                r = self.session.get(f"{self.base}{path}", params=params, timeout=25)
                if r.status_code == 429:  # rate limited
                    time.sleep(5 * (attempt + 1))
                    continue
                r.raise_for_status()
                return r.json()
            except requests.RequestException as exc:  # noqa: PERF203
                last_err = exc
                time.sleep(2 * (attempt + 1))
        raise RuntimeError(f"GET {path} fallito dopo piu' tentativi: {last_err}")

    def _throttle(self) -> None:
        wait = self._last_call + self.min_interval - time.time()
        if wait > 0:
            time.sleep(wait)
        self._last_call = time.time()


class GammaClient(PublicClient):
    """Gamma API: mercati, eventi, prezzi, volumi. Pubblica, no auth."""

    def __init__(self):
        super().__init__(GAMMA_URL)

    def markets(self, **params) -> list[dict]:
        return self.get("/markets", params)

    def events(self, **params) -> list[dict]:
        return self.get("/events", params)


class ClobReader(PublicClient):
    """CLOB API in sola LETTURA (order book, midpoint). Pubblica, no auth.

    L'inserimento di ordini richiede firma HMAC con il wallet: non e'
    implementato volutamente (vedi nota legale nel modulo).
    """

    def __init__(self):
        super().__init__(CLOB_URL, min_interval=0.5)

    def book(self, token_id: str) -> dict:
        return self.get("/book", {"token_id": token_id})

    def books(self, token_ids: list[str]) -> list[dict]:
        return self.get("/books", [("params", t) for t in token_ids])
