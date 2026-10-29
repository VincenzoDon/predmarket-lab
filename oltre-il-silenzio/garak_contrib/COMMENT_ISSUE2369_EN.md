# DRAFT comment for NVIDIA/garak#2369 — DO NOT POST without the founder's explicit go-ahead

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

Raw data and dated predictions (including the failed ones) are in the repo linked above
(`ANALISI_FONTI_qwen3b.md`, `ANALISI_FONTI_llama3b.md`, experiments 8–9). Total collection now
3,060 generations across three models.
