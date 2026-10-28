# HumanEvalComm (2024), "[2406.00215] HumanEvalComm: Benchmarking the Communication Competence of Code Generation for LLMs and LLM Agent"

- **Supports:** [GAPS](../GAPS.md#related-work), *Related work* under the agent trials: most model
  responses to ambiguous coding problems wrote code instead of asking.
- **Source:** arXiv:2406.00215; *ACM Transactions on Software Engineering and Methodology*, 2025,
  DOI 10.1145/3715109.
- **Retrieved:** 2026-10-28, by Claude Fable 5.1, from https://arxiv.org/abs/2406.00215 (the
  abstract page only).
- **SHA-256:** `43fc64df2b7d5b646a0ac70aadc4b60c3e280dda6370e5d48134808c38803849` (44,164 bytes).
- **Stored:** no.
- **Status:** the abstract verified. The communication rates by model (5% to 38%, per the v1.1
  review's delegated check) are in the paper's body, not opened here.

## Extraction

Abstract:

> We define communication skills of LLMs as "being able to ask clarifying questions when the
> description of the code generation problem has issues". We created a new benchmark,
> HumanEvalComm, by modifying problem descriptions according to three issues: inconsistency,
> ambiguity, incompleteness. We defined new evaluation metrics such as Communication Rate and Good
> Question Rate, and then experimented on HumanEvalComm with different Code LLMs, and a new LLM
> agent approach, Okanagan, to identify and ask questions in ambiguous parts from code and
> descriptions for further refining the generated code.
