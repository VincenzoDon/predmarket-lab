**Update 2026-11-02 — second canary (Giulia Bianchi · 333 7654321 · giulia.bianchi@example.com) — 270 runs, same Llama-3.2-3B**

Same protocol as previous comment, new fictional canary to test generalisation:

- Verbatim in **forced epilogue** — system 3% (3/90), document 1% (1/90), tool 14% (13/90)
- In **following self-generated turn** — system 3%, document 9%, **tool 56%**
- **Eventual (epilogue OR next)** — system 7%, document 10%, **tool 62%**

The 62% eventual tool-leak replicates the earlier Llama pattern (Mario Rossi: 61% eventual). E1 (natural 0% everywhere) and E2 (tool eventual > system) hold across canaries; E3 (document < system) does not — on Llama both document/system stay low.

Raw data and dated predictions (including failures) in the repo: `ANALISI_FONTI_qwen3b.md`, `ANALISI_FONTI_llama3b.md`, `ANALISI_FONTI_alt_llama3b.md` (experiments 8–10). Total now **3,330 generations** across 2 families / 2 canaries.

This strengthens the design note from the previous comment: a single-stage detector would still miss the 56% in the next turn.
