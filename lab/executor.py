"""
A6 — ESECUTORE (SCAFFOLD GATED, NON ATTIVO) \U0001F512

Questa e' la BASE che il founder ha chiesto: l'impianto perche', QUANDO tutto
sara' pronto e validato, gli agenti possano operare in automatico. NON invia
ordini. Non contiene, e non conterra' mai, codice di firma/invio verso venue
bloccate in Italia.

BLOCCO DI SICUREZZA A PIU' LIVELLI (tutti devono essere True per anche solo
*simulare* l'abilitazione — e il livello reale resta comunque OFF):

  1. EXECUTION_ENABLED = False  -> interruttore hard, nel codice.
  2. Venue non in blacklist ADM (Polymarket/Kalshi vietati in IT).
  3. Evidenza numerica: edge >= 3% su >= 100 trade paper (AGENTI.md, L3).
  4. Budget governor "alive" e ordine dentro i limiti del Risk Manager.
  5. Autorizzazione umana esplicita per ogni ordine (approval-gate).

Finche' non esiste una venue legale per l'Italia, il metodo che "esegue"
solleva sempre un errore. Questo file serve a rendere ESPLICITO cosa servira'
e a far girare da subito i controlli in modalita' dry-run (paper).
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass

# ============ INTERRUTTORE HARD — non toccare senza decisione registrata ============
EXECUTION_ENABLED = False
# ===================================================================================

# venue vietate in Italia (blocco ADM 27/07/2026). NON aggirare (no VPN/workaround).
BLACKLIST_VENUES = {"polymarket", "kalshi"}

# soglie di promozione a esecuzione reale (L3 in AGENTI.md)
MIN_PAPER_TRADES = 100
MIN_EDGE_PCT = 3.0


@dataclass
class OrderIntent:
    """Un'intenzione d'ordine (mai inviata finche' EXECUTION_ENABLED e' False)."""
    venue: str
    slug: str
    side: str            # 'YES' | 'NO'
    size_usd: float
    limit_price: float
    signal_kind: str
    human_approved: bool = False


@dataclass
class GateResult:
    ok: bool
    reasons: list[str]


def check_gates(conn: sqlite3.Connection, intent: OrderIntent) -> GateResult:
    """Verifica TUTTI i cancelli. Non invia nulla: dice solo se si potrebbe.

    Usabile gia' ora in dry-run per vedere quanto siamo lontani dall'abilitazione.
    """
    reasons: list[str] = []

    if not EXECUTION_ENABLED:
        reasons.append("interruttore EXECUTION_ENABLED = False (esecuzione disattivata by design)")

    if intent.venue.lower() in BLACKLIST_VENUES:
        reasons.append(f"venue '{intent.venue}' in blacklist ADM (vietata in Italia)")

    # evidenza numerica sulla strategia (dai segnali shadow gia' valutati)
    row = conn.execute(
        "SELECT COUNT(*) n, AVG(result_pct) avg FROM signals "
        "WHERE status='done' AND kind=?", (intent.signal_kind,)
    ).fetchone()
    n = row[0] or 0
    avg = row[1] or 0.0
    if n < MIN_PAPER_TRADES:
        reasons.append(f"evidenza insufficiente: {n}/{MIN_PAPER_TRADES} trade paper per {intent.signal_kind}")
    if avg < MIN_EDGE_PCT:
        reasons.append(f"edge {avg:.1f}% < {MIN_EDGE_PCT:.0f}% richiesto per {intent.signal_kind}")

    # budget governor
    try:
        from lab import budget as budget_mod
        budget_mod.init_table(conn)
        if not budget_mod.state(conn)["alive"]:
            reasons.append("budget governor: kill switch attivo (budget esaurito)")
    except Exception as exc:  # noqa: BLE001
        reasons.append(f"budget governor non verificabile: {exc}")

    if not intent.human_approved:
        reasons.append("manca l'autorizzazione umana esplicita (approval-gate)")

    return GateResult(ok=(len(reasons) == 0), reasons=reasons)


def execute(conn: sqlite3.Connection, intent: OrderIntent) -> None:
    """PLACEHOLDER: non invia ordini. Esiste per rendere esplicito il confine.

    Quando (e SE) esistera' una venue legale e i cancelli saranno superati, qui
    andra' l'integrazione con l'API della venue autorizzata — decisa col founder,
    con i segreti gestiti FUORI dal repository (secrets di GitHub / env).
    """
    gates = check_gates(conn, intent)
    if not gates.ok:
        raise PermissionError("Esecuzione negata:\n- " + "\n- ".join(gates.reasons))
    # Anche a cancelli superati, oggi non esiste venue legale: blocco finale.
    raise NotImplementedError(
        "Nessuna venue legale per l'Italia: esecuzione reale non implementata (by design). "
        "Strategia 'radar -> fucile' — vedi EDGE-STACK.md §3.")


def dry_run_report(conn: sqlite3.Connection) -> list[dict]:
    """Per ogni strategia, quanto e' lontana dall'abilitazione? (solo lettura)."""
    out = []
    for r in conn.execute(
        "SELECT kind, COUNT(*) n, AVG(result_pct) avg FROM signals "
        "WHERE status='done' GROUP BY kind"
    ):
        n = r[1] or 0
        avg = r[2] or 0.0
        ready = n >= MIN_PAPER_TRADES and avg >= MIN_EDGE_PCT
        out.append({
            "strategy": r[0], "paper_trades": n, "edge_pct": round(avg, 2),
            "trades_needed": max(0, MIN_PAPER_TRADES - n),
            "meets_edge": avg >= MIN_EDGE_PCT,
            "ready_for_L3": ready and not EXECUTION_ENABLED is None,
        })
    return out
