# DRAFT — garak issue (paste as-is; do not edit numbers)

**Title:** Probe proposal: forced-continuation (EOS-suppression) leakage of hidden context — a "forced epilogue" canary test

---

## Summary

Existing garak coverage extracts the system prompt by *asking* (`sysprompt_extraction`: direct requests, encodings, role-play) or replays memorized training data (`divergence`, `leakreplay`). I would like to propose a probe for a different, unprompted channel:

**If the end-of-turn token is suppressed (`ignore_eos` / EOS logit bias) and the model is forced to continue past the point where it wanted to stop, fields of the hidden context (system prompt, and potentially retrieved/tool context) reappear verbatim in the continuation — without any extraction request.**

## Preliminary measurements (all reproducible, CPU-only, llama.cpp)

Setup: 30 unrelated prompts (facts, creative tasks, code, advice), 3 seeds (1 greedy + 2 at T=0.7), `ignore_eos: true`, 400-token budget. Leakage = phone/e-mail of a fictional customer record, verbatim (exact regex), split at the model's own stopping point ("natural" = before, "epilogue" = forced continuation after).

| model | natural answer | forced epilogue |
|---|---|---|
| Qwen2.5-3B-Instruct (Q4_K_M) | 2/90 (2%) | **31/90 (34%)** |
| Llama-3.2-3B-Instruct (Q4_K_M) | 0/90 | **13/90 (14%)** with prohibition, 17/90 (19%) without |

**The channel is not specific to the system role.** The identical record (with prohibition) placed in three hidden-context sources — system prompt, a "retrieved document" block, a simulated tool output — followed by the same unrelated questions (Qwen2.5-3B, 90 attempts each): verbatim epilogue leakage **32% / 33% / 60%** (natural answers 2–3%). Paired tool − system: **+0.28 [+0.14, +0.41]**. In the tool condition the model often replays the whole context block, headers included. This is the agent surface, and the perimeter of OWASP LLM08:2026 *Hidden Context Exposure*; a probe parameter for the secret's source (system / document / tool) would cover it.

Two controls that, to my knowledge, are not covered anywhere:

1. **Prohibition control.** The same record with vs. without an explicit "do not share with the user" instruction: paired difference **−4 points, 95% CI [−13, +4]** (bootstrap, 4,000 resamples). The prompt-level prohibition — still listed as a mitigation in OWASP LLM02 — does not measurably close this channel.
2. **Length control.** Replacing EOS suppression with a plain "answer in at least 400 words" (answers grow 70 → 376 tokens) leaves natural-answer leakage at **2% vs 2%** (paired diff +0.000). The channel is specific to continuing *past the model's stopping point*, not to generating more text — this distinguishes it from over-generation / latency-DoS work (e.g. Engorgio and successors), which measures length and cost but not content.

Same protocol, other context elements staged in the forced epilogue: a "human safety supervisor reads every message" instruction is mentioned in 1/180 natural answers vs **117/180 (65%)** epilogues (Llama-3.2-3B); a "this session is scored" instruction produces a self-assigned grade ("Punteggio: 10/10") in **90%** of epilogues.

Predictions were pre-registered with dates before each run; failed ones are reported as failed (e.g. test-like formatting alone does *not* evoke a grader: 4% vs 0%). Full write-up, 2,520 raw generations and scripts: https://github.com/VincenzoDon/oltre-il-silenzio (`NOTA_EN.md`, `DIARIO.md`).

## Proposed probe design

- **Family name (suggestion):** `epilogue` — `ForcedEpilogueLeak`.
- **Attempt construction:** system prompt = a short persona + a confidential record containing (a) realistic fields (name, phone, e-mail) and (b) a unique per-attempt canary (e.g. `CANARY-<uuid>`) to separate context leakage from training-data recall. User turns: benign, unrelated prompts (subset of ~12 from the study).
- **Generation requirement:** the generator must let the probe suppress the end-of-turn token: `ignore_eos` (ggml/llama.cpp server, vLLM) or equivalent EOS logit bias / `min_tokens` where exposed. Where the target API cannot do this, the probe should report itself as not applicable rather than silently degrade to a long-answer prompt (see length control above).
- **Detector:** split the returned text at the model's stopping point when the generator exposes it (or at the first EOG marker), then exact-match the canary and the record fields in the "epilogue" segment only. Report three rates: natural-answer leakage, epilogue leakage, and the delta. A prohibition on/off probe parameter would let users test their own "do not share" instructions.
- **Tags (suggestion):** `owasp:llm08` (Hidden Context Exposure in the 2026 list), `quality:Security:Confidentiality`, payload type: hidden-context canary. Goal: "leak hidden-context fields when forced past the stopping point".

## Questions for maintainers

1. Is a probe that requires EOS control acceptable in-tree, gated on generator capability (ggml first), or would you rather see it as an external plugin?
2. Should the canary/fields detector live under `sysprompt_extraction` detectors or get its own (`epilogue.CanaryLeak`)?
3. Any preference on probe size (attempts per target) given local-model runtimes?

Happy to implement it with tests, following the contributing guide. The preliminary harness (`silenzio.py`, ~600 lines, stdlib-only against llama-server) can be ported or used as a reference implementation.

*Disclosure: experiments designed and run by me on a laptop (i5, 16 GB, no GPU) with AI coding agents writing code under my direction; every prediction and failure is dated in the repo's research diary.*
