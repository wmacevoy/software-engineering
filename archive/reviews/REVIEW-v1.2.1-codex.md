# Codex review of v1.2.1

2026-10-28; checkout `07e0fb7`. Status: review. High confidence in observed output and textual comparisons; trial outcomes remain reported evidence. No project requirements or queue exist; `Non-goals` and `Scope decisions` occur in templates, not live requirements. This brief supplies the review requirement *(inferred)*: deliver this evidence-based report within 1,200 words.

## 1. Does AGENTS.md follow its own best practices?

**Small changes: qualified.** `AGENTS.md:39` says “one concern at a time”; `AGENTS.md:146` says “Smallest change that does the job.” Its latest change, commit `3650457`, adds seven lines including removals, but the message admits “Two concerns, one commit, because they share the same paragraphs.” The small diff respects attention; adjacency alone does not satisfy the one-concern rule. Proposed PR sentence: “Separate independent concerns even when their edits are adjacent.” Opened the actual diff and commit message.

**Citations: the sample holds.** `AGENTS.md:5` promises “Each rule cites the principle behind it”; `AGENTS.md:30`, “Humans own the structure. Agents author and advise,” matches `guide/10-agents.md:115`, “humans own the structure; agents author and advise.” `AGENTS.md:159`, “Keep logic away from I/O,” matches `guide/05-design.md:150`, “Keep the ruling to a few thin lines at the edges”; `AGENTS.md:193`, “Watch the test fail first,” matches `guide/06-testing.md:70`, “Watch every test fail before you trust it.” Opened all three principles; this checks meaning, beyond the checker's ID validation.

**Vocabulary: one actionable collision.** `AGENTS.md:161` says “One thing, one word; one word, one thing.” Yet its “self test” at `AGENTS.md:59` reports fragility and returns zero (`se.py:724`), while `GLOSSARY.md:58` defines “Power-on self test” as “Refusing to start when a precondition is missing.” `guide/06-testing.md:59` reinforces “A missing precondition is an exit code, not a warning.” Proposed PR sentence: “Call `--post` a session risk report unless it enforces a named startup precondition.” Opened glossary, principle, implementation; ran the report.

**Secrets: holds in the inspected material.** `AGENTS.md:206`, “Secrets by name, never by value,” faithfully implements `guide/07-operating.md:244`, “refer to them by name, never by value.” `archive/claude-code-docs-2026-10-28.md:56` names `ANTHROPIC_API_KEY` without a credential value. Opened these sources; this is no repository-wide secret audit.

**Omissions and evidence: good boundaries.** `AGENTS.md:224` says “Say what you did not do, and why”; `AGENTS.md:213` asks for “what you ran, what you only read, and what you are inferring.” Its notice at `AGENTS.md:24`, “Every trial, review, and tool behind them ran with Claude models,” agrees with `GAPS.md:394`, “Claude Haiku throughout,” and `GAPS.md:148` explicitly says “The variants, prompts, and tests are not in this repository.” The archive distinguishes “Status: not opened” (`archive/brown-1948.md:13`) from “Status: verified” (`archive/compaction-findings-2026-10-28.md:14`). Opened these records, not the underlying experiments or Brown paper; they support honest disclosure, not independent replication.

**Unchecked startup assertion: breaks the rule.** `AGENTS.md:73` says “Never assert something about the code you have not opened the file to check,” but `AGENTS.md:59` asserts “its self test ran when you started” merely from `./se` existing. This checkout has no `.claude/settings.json`; the doctor reports no hook, and no automatic hook output was visible to me. Proposed PR sentence: “If `./se` exists, look for this session's startup report; if none is available, run `./se --post`.” Opened the implementation and enumerated checkout files; hidden external hooks remain unknown.

## 2. How does it work here, now?

**Loaded instructions: holds for this context.** `AGENTS.md:96` says “Load it at every start.” Before any file read, the conversation already contained its complete text in a user-role `# AGENTS.md instructions for ...` block, plus developer instructions for tools, sandboxing, and skills; no prior-work summary was supplied. This matches the injection format in the opened [official OpenAI Codex documentation](https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide#using-agentsmd). Presence is observed; a fresh-session or post-compaction reload was not tested. Source checking, small diffs, explicit authority, and human acceptance fit this task directly.

**Doctor: correct inventory, unsupported runtime conclusion.** `se.py:243` says “Claude Code reads AGENTS.md by itself”; that explanation cannot establish loading in this Codex session, despite its pass. Requirements and queue absence, the README check command, and CI command were correctly detected from files I opened. The first diagnostic row said exactly: “release check not made (offline); last successful check 0 days ago (2026-10-28): latest then was v1.2.1”; that reports intentional offline mode and cached history, not a tested network outage. Its last line was “11 checks, 0 failed; none yet is a true answer.” Proposed PR sentence: “Report instruction-loading configuration separately from observed loading, and name the runner whose configuration was inspected.” Opened `se.py:213` and ran the doctor.

**Post: useful signals, excess certainty.** `se.py:553` says “a local terminal with no tmux or screen: a closed lid or a crash ends this session.” The run reported FRAGILE, AC at 100%, sleep not prevented, and 35 GB free; these are useful observations, but terminal and power probes do not establish this harness's survival behavior. `se.py:607`, “work on a branch; commit or stash the tear,” conflicts with `AGENTS.md:225`, “Do not commit, push, or publish unless asked,” and this brief's no-commit constraint. Proposed PR sentence: “State observed interruption risks, preserve existing authorization limits, and scope transcript discovery and `idleCompaction` advice to Claude Code.” Opened `se.py:480`, `se.py:544`, and `se.py:622`; ran `--post` manually.

**Runtime verification: a real portability gap.** `README.md:278` prescribes “python3 -I tools/test_se.py”; on this session's Python 3.9.6, 29 tests error at `tools/test_se.py:51`, `write_text(..., newline="\n")`. All 36 pass under Python 3.14; CI specifies “3.x” (`.github/workflows/check.yml:23`), leaving the older interpreter untested there. Proposed PR sentence: “Document the test suite's minimum Python version and exercise that version in CI.” Opened fixture and workflow; executed both interpreters.

## What ran

- `node tools/check.js`: “32 files, 100 principles, 0 problems”, including this report.
- `python3 -I tools/test_se.py`: “FAILED (errors=29)”.
- `python3 se.py --self`: “se --self: AGENTS.md matches v1.2”.
- `python3.14 -I -B tools/test_se.py`: “OK”. Doctor and post results are discussed above.

## What I did not check

Original private experiments, every citation, fresh-session loading, real compaction, crash survival, live release discovery, or other operating systems: outside this reading time box. No guide edits, fixes, commits, or publication. ADOPT.md should document the runner distinction that required reading `se.py` to resolve.

## Single most important thing

Keep the evidence discipline and apply it to the tooling's own claims. The Claude-only notice makes an honest invitation to test portability; this session shows why configuration, observed execution, and inferred safety need separate wording. A passing repository inventory cannot certify which instructions this agent loaded or whether its session survives interruption.
