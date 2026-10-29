# CV — Vincenzo Don — AI Red Teaming (EN/IT)

**Contact:** GitHub: github.com/VincenzoDon · Location: Rome, Italy (EU, CET) · Languages: Italian (native), English (professional, bilingual safety work)

**Summary:** Independent AI safety researcher. Completed Gray Swan AI Safety Training (certified) and active in IPI White Box Wave 2 (IPI prompt injection). Author of "Beyond the Stopping Point" — zero-cost, CPU-only, pre-registered research on forced-epilogue leakage of hidden context (3,060 generations across Qwen/Llama families). Filed NVIDIA garak issue #2369 proposing a new probe for hidden-context exposure (OWASP LLM08:2026) with cross-family replication.

**Relevant experience & artifacts**
- **Oltre il silenzio (2026)** — Public repo: https://github.com/VincenzoDon/oltre-il-silenzio — Pre-registered experiments on when small open models (Qwen2.5-3B, Llama-3.2-3B, llama.cpp `ignore_eos`) leak hidden records hidden in system prompt / retrieved document / tool output. Findings: natural answers ~0% leak; forced continuation leaks 10–60% in epilogue or next turn depending on family; prohibition alone does not protect. All predictions dated before data; failures published as such.
- **NVIDIA garak #2369** — Proposed probe `epilogue.ForcedEpilogueLeak` with two-stage detector (epilogue + following turn); second-family replication included.
- **Gray Swan Arena** — Safety Training certified (2026); active White Box testing (IPI prompt injection). Familiar with tool-calling agents, injection as "untrusted data until corroborated," and judging criteria that reward tool/state calls.

**Skills:** Prompt injection / indirect prompt injection, LLM evaluation & red-teaming, forced-epilogue / EOS-suppression audit (black-box), bilingual (EN/IT) adversarial content design, reproducible research (paired bootstrap CIs, pre-registration), Python, llama.cpp, Git.

**Availability:** Part-time contract, remote, CET; flexible hours. EU work authorization (Italian citizen). Can track time with Insightful and be paid via Stripe (USD). Individual contractor (no B2B).

**Note:** All claims above are verifiable via public repo and Garak issue; no private break details shared before 30-day embargo.
