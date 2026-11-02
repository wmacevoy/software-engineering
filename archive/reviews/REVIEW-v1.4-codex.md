# v1.4 review — OpenAI Codex, 2026-11-02

Read-only review; only this report was written. Requirement: REQ1/SRC-2, reviews are proposals. Claims below distinguish opening archived evidence from opening its external original. No network was used.

## 1. Agreement with itself and its sources

1. **GAPS.md:278–279:** “It flagged 4 messages, across three compactions; the other 28 it passed.” Three flagged out of 29 leaves 26, not 28. SE1/A11 (`guide/10-agents.md:184`) instead says “all in one compaction”; U10:265 and GAPS:569 repeat 28/29. Opened all these passages; the underlying transcripts are outside this clone and unchecked, so I cannot choose the correct count.

2. **GAPS.md:404:** “Agents wrote D-9 into their own journals in 13 of 20 runs”. The cited extraction, `archive/compaction-findings-2026-10-28.md:26`, says “T and T2: 19 of 20” (and separately 9 A plus 8 AF). The published numerator lacks support in that extraction; reconcile the batch and count. Opened the archive, not the private original.

3. **README.md:306:** “an idle one and a manual `/compact`”. Its source, `docs/FINDINGS.md`, last entry, ends “a manual `/compact` is still unobserved”; the documented real event was inferred to be idle from timing. Remove the manual claim unless another observation is recorded. Opened the cited finding, not its transcript.

4. **archive/royce-1970.md:3:** “the warning against the drawing comes two pages later, not in the sentence directly beneath it.” The same entry's extraction at lines 20–22 places “risky and invites failure” directly beneath the caption, agreeing with SE1/W2 (`guide/08-work.md:32–34`). Correct the archive's support summary; W2 holds against the archived passage. Opened the extraction, not the PDF.

5. **CONTRIBUTING.md:59–60:** “an untested idea goes into GAPS as open, not into a principle.” U10 and W13 explicitly enter principles without trials; REQ1/SRC-3 (`docs/REQUIREMENTS_v3.md`) permits the author's stated decision. The requirement outranks the local guide, but the contribution rule still promises something the repository does not do. Proposed sentence: “A meaning change needs recorded evidence or an explicitly attributed author decision, with missing trials left open.” Opened both rules and the new principles.

The archive honestly marks Brown and pair-programming evidence as not opened, but that leaves their original claims unverified here; README:301's blanket checksum claim exceeds those entries, which owe checksums. Opened those entries only. Removed reviews and rewritten hashes are preparation conditions, not findings.

## 2. New since v1.3.2

6. **guide/02-unknowing.md:241:** “No spike finishes it.” Distinguishing a proxy from acceptance is useful, but changing preferences do not establish an irreducible kind of unknowability: a named person's judgment on a specified version and occasion can be observed. The falsifier at line 269 can always reclassify a successful case as “never essential,” leaving the existential claim untouched. Proposed sentence: “Some acceptance decisions remain human judgments; record their scope and revisit them when the artifact or audience changes.” Opened U1/U2/U10 and the untried-decision entry in GAPS; no trial supports the stronger claim.

7. **se.py:459:** “if dates and re.search(...)”. Any requirement version, any date, and either verdict outcome qualify; `check_trace` then describes it as “passed by a person.” An in-memory probe with `REQ1/MISSION-1 verdict rejected 2020-01-01` produced PASS, although today's mission originated in v3; neither judge nor artifact version is checked. Require an explicit outcome, current requirement version, judge, and reviewed artifact—or report only that a verdict-shaped record exists. Opened and executed the implementation.

   Thus *(judged)* does not textually excuse missing requirements: U10:250 says “Convert what converts,” and R2 retains observable claims. Operationally the trace row permits escaping test coverage by marking everything judged and supplying arbitrary dated lines. REQ3/MISSION-1 names a judge and occasion, but `docs/REQUIREMENTS_v3.md:47–48` leaves shape exclusions and exceptions “the author's to fill”; D9's requested boundaries remain unfinished, honestly labeled. Opened requirements, D9, R2, and trace code.

8. **guide/08-work.md:328:** “A finding that changes no rule, test, or check is a lesson not learned.” The body at line 336 correctly allows recording why nothing changed, contradicting the categorical title. Confirming an existing rule, rejecting a false alarm, or reducing uncertainty can be learning without adding policy; a *Changed* line alone does not prove prevention. Proposed title: “Close each finding with its consequence, including a reason to change nothing.” Opened W13, GAPS, and this repository's FINDINGS; the rule explicitly has no trial.

9. **guide/08-work.md:275:** “Its description lists the requirements and decisions it must not break”. This holds as a cheap review prompt, with a limitation: GAPS:444–446 acknowledges that naming D-9 pointed at the defect and measured no false-alarm rate. Keep the caveat near the rule and do not treat an author's risk list as exhaustive. Opened W11, GAPS, and the archived 5/36 then 31/36 extraction; not the original reviews.

10. **tools/check.py:322:** “if line not in readme”. This checks heading inclusion, not exact index equality promised by REQ1/ID-1 and the module docstring. An in-memory README with an additional SE1/U1 entry carrying a contradictory title still returned “39 files, 102 principles, 0 problems”; `test_index_line_dropped` tests only omission. Compare parsed index entries in both directions. Opened code/test/requirement and ran the probe without editing files.

11. **tools/test_check.py:293:** “test_the_check_names_no_runtime_but_python”. Its assertion rejects only Node/npm. Supplying `ruby tools/check.rb` as both files' contents in memory still passed this test while REQ2/CHK-4 was broken. Test the permitted commands or execute with only the documented prerequisites available. Opened and executed the test; the current scripts themselves use Python as intended.

## 3. AGENTS.md in this context

12. **AGENTS.md:98:** “importing a copy ... from CLAUDE.md”. I had the full agreement in the user's initial message before any tool call, including “Humans own the structure. Agents author and advise.” That proves presence in this conversation, not filesystem auto-loading or survival after compaction. I subsequently opened AGENTS.md and CONTRIBUTING.md. Proposed sentence: “Use your runner's documented instruction-loading mechanism; CLAUDE.md imports and Claude hook events are Claude Code examples, and verify loading separately for each runner.” Opened the agreement; no Codex loader configuration or fresh-session experiment was inspected.

13. **se.py:708:** “the session survives a dropped connection or a closed window”. `--post` correctly detected a non-Claude runner, skipped Claude transcript/idle rows, and measured disk, but inferred overall ROBUST from a multiplexer without inspecting my runner's persistence. Proposed sentence: “A multiplexer protects terminal processes; runner persistence and compaction recovery remain uninspected.” The doctor correctly qualified its loading PASS as Claude configuration, but that PASS is not evidence about me; its hook diagnosis concerns Claude too. Its agreement mismatch is real unreleased text, and its citation failures point to fixture strings at `tools/test_se.py:500`, not production bare citations. Opened implementation and fixture; ran both commands.

## Runs, limits, and priority

- `git diff v1.3.2 --stat`: last line `32 files changed, 1913 insertions(+), 424 deletions(-)`.
- `python3 se.py --doctor --offline --repo .`: first row says “release check not made (offline); last successful check 0 days ago (2026-11-02): latest then was v1.3.2”; last line `11 checks, 2 failed` (exit 1).
- `python3 se.py --post`: last line `ordinary rules apply; the hand-off checklist still does.` (exit 0).
- `sh tools/check.sh`: last line `OK` (exit 0; 67 and 26 tests). In-memory probes above reproduced the reported gaps.

Unchecked: external papers, private trials/transcripts, CI and site behavior, all Unicode/port equivalence, live compaction, and a complete mutation audit of since.py. No guide edits, commits, or pushes.

The most important issue is that a green instrument can claim more than it observes. Keep human acceptance, but make the trace row describe its evidence accurately: a dated line is not an approving judge's verdict on today's artifact. This review itself found that exact failure while the full check remained green.
