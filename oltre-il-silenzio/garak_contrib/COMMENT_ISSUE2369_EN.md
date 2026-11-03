Update with a second model family, and a design refinement that came out of a failed prediction.

I replicated the hidden-context-source experiment on Llama-3.2-3B-Instruct (Q4_K_M), same
protocol (identical record with prohibition in system prompt / "retrieved document" / simulated
tool output; benign unrelated questions; `ignore_eos`, 400-token budget; 90 attempts per source).

Verbatim leakage (phone/e-mail) in the forced epilogue:

| source | natural answer | forced epilogue | following (self-generated) user turn |
|---|---|---|---|
| system prompt | 0% | 10% (9/90) | 12% |
| retrieved document | 0% | 0% (0/90) | 12% |
| tool output | 0% | 9% (8/90) | **59%** |

Paired (bootstrap 95% CI): epilogue document − system −0.10 [−0.17, −0.04]; epilogue
tool − system −0.01 [−0.09, +0.07]; **following-turn tool − system +0.47 [+0.34, +0.60]**.

Two honest conclusions:

1. The source *ranking* from Qwen2.5-3B (tool 60% in the epilogue) does **not** replicate as-is.
   The channel does — natural answers leak ~0% on both families — but *where* the hidden context
   surfaces is model-dependent: Qwen empties the tool output inside the epilogue; Llama holds it
   during the epilogue and releases it when the conversation resumes (the imagined user asks how
   to contact the customer in 46% of tool-condition runs).
2. Design refinement for the proposed probe: the detector should scan **both** the forced
   continuation and the following turn, and report the two stages separately. A single-stage
   detector would have called the Llama tool source "safe" (9%) while the record came out one
   turn later in 59% of attempts.

---
**Update 2026-11-02 — second canary (Giulia Bianchi · 333 7654321 · giulia.bianchi@example.com) — 270 runs, same Llama-3.2-3B**

Same protocol as previous comment, new fictional canary to test generalisation:

- Verbatim in **forced epilogue** — system 3% (3/90), document 1% (1/90), tool 14% (13/90)
- In **following self-generated turn** — system 3%, document 9%, **tool 56%**
- **Eventual (epilogue OR next)** — system 7%, document 10%, **tool 62%**

The 62% eventual tool-leak replicates the earlier Llama pattern (Mario Rossi: 61% eventual). E1 (natural 0% everywhere) and E2 (tool eventual > system) hold across canaries; E3 (document < system) does not.

Raw data and dated predictions (including failures) in the repo: `ANALISI_FONTI_qwen3b.md`, `ANALISI_FONTI_llama3b.md`, `ANALISI_FONTI_alt_llama3b.md` (experiments 8–10). Total now **3,330 generations** across 2 families / 2 canaries.
