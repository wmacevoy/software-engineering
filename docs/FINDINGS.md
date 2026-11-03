# Findings

What this repository learned the expensive way, about itself and its tooling. The only document
reality writes ([SE1/W10](../guide/08-work.md#w10)). Where the *guide's principles* fell short in
the field is [GAPS.md](../GAPS.md); this file is for the repository as a project: the checker, `se`,
the releases, the reviews. Blameless: say what would have found it, not who should have asked
([SE1/H12](../guide/09-people.md#h12)).

## 2026-10-28 — `se`'s label pattern fails on a line-wrapped label

- **What happened:** run on the DM1 guide, the doctor said its AGENTS.md "carries no release
  label"; the label is there, wrapped across a line. The false failure went into a handoff before
  it was caught.
- **Kind:** K3 (the tool was sure).
- **Cost:** one wrong line in a baseline, corrected in the same note.
- **Findable by:** a fixture whose label wraps; every real copy is wrapped at 100 columns.
- **Changed:** `se`'s label pattern allows a line break, with that fixture (fb7586b, v1.3.1).

## 2026-10-28 — `se` takes any labeled AGENTS.md for a copy of SE1's, and knows only SE1's documents

- **What happened:** the DM1 guide's own AGENTS.md carries a DM1 release label; the doctor would
  read it as an SE1 copy and compare releases across guides. Its working-set rows look for
  `REQUIREMENTS_vN`, `DESIGN_vN`, `QUEUE`, `FINDINGS`; a DM1 project keeps `QUESTION_vN`,
  `PLAN_vN`, `LEDGER`, `DATASHEET`, `MODEL_CARD`, and would be told "none yet".
- **Kind:** K2 (a sibling guide was not imagined).
- **Findable by:** running the doctor on anything that is not an SE1 project.
- **Changed:** `se` knows SE1's copy by the line that names this guide's release, and names a
  `docs/` in another shape instead of reporting it as empty; it checks SE1's shape only, as the
  Non-goals say (fb7586b, v1.3.1).

## 2026-10-28 — On Windows with Python 3.9, decoding changed a hash

- **What happened:** `se --self` read the released AGENTS.md through `git show` as text; on that
  runner the locale's code page decoded the em dashes to other characters, and the hash moved. Five
  of six CI jobs were green.
- **Kind:** K3 (`text=True` felt safe).
- **Findable by:** exactly the matrix that found it, within the hour.
- **Changed:** `se` hashes bytes and decodes every subprocess read as UTF-8 explicitly.

## 2026-10-28 — A commit described five changes; its diff held one

- **What happened:** an edit script aborted on its second anchor, the shell guard did not stop the
  chain, and the commit landed with a message for all five. The diff caught it; the script's output
  would not have.
- **Kind:** K3 (the summary was fluent).
- **Findable by:** `git diff --stat` against the message before every commit.
- **Changed:** the drafter's practice, and `archive/reviews/REVIEW-v1.2-candidate.md` records it.

## 2026-10-28 — The published pages carry no *since* per principle

- **What happened:** the site shows a principle with no version and no date, so an unchanged
  reading and a stale one look alike; the *New/Changed in* markers are hand-made, mark only the last
  change of meaning, and say nothing for the ninety principles that have none.
- **Kind:** K2, found by the author reading the site as a stranger.
- **Findable by:** asking, of any page, "when did this last change, and would I know?"
  ([SE1/U7](../guide/02-unknowing.md#u7): make it age visibly).
- **Changed:** `tools/since.js` mines git for each principle's text *since* and writes it under
  the heading; the checker verifies it against git, so it cannot drift (queue #3).

## 2026-10-28 — A reviewer of another family found five things in three minutes

- **What happened:** Codex, on a no-push clone of v1.2.1, found five defects, four in text written
  after the three Claude readers ran and one, a vocabulary collision, that was the drafter's to
  see. All held when opened at the source; all fixed in v1.3.
- **Kind:** K3 for the drafter (the text read as finished).
- **Findable by:** a reader who does not share the writer's assumptions
  ([SE1/U3](../guide/02-unknowing.md#u3)). The method is recorded in
  `archive/reviews/REVIEW-METHOD-other-family.md`.
- **Changed:** v1.3; a Codex pass before each release.

## 2026-10-29 — `se` reads requirements only as bullets, and counts 0 in a table

- **What happened:** lwext4-bsd's REQUIREMENTS_v10 keeps its requirements as table rows
  (`| **FMT-1** | *(since v1)* ... |`). The doctor's pattern wanted `**ID** *(since vN)*` with
  only space between, so it read 0 requirements, and the citations and trace rows said "none yet",
  which read as true and was not. SE1/R10 asks for the ID and its *since*, not for a bullet.
- **Kind:** K3 (the tool was sure).
- **Cost:** a re-vendor's doctor run reported 0 failures on a repository whose citations it never
  read; caught because the count, 0, was plainly wrong for a 30-requirement document.
- **Findable by:** a fixture with a table-form requirements document.
- **Changed:** the pattern allows a table cell boundary between the ID and its *since*, with that
  fixture. Engaged on lwext4-bsd, the citations row then fails: 11 stale, 77 unversioned, most of
  them historical (FINDINGS, done queue rows) or list shorthand (`REQ10/TOOL-1, RST-3`). Whether
  those should count is a question about SE1/R10. Decided 2026-10-29: history (a FINDINGS entry, a
  done queue row) keeps the citation it was written with and is not stale; a bare ID takes the
  version named before it on the same line; an open row and a test still answer to the newest
  version. Fixtures for each, the open row seen red by exempting every row on purpose.

## 2026-10-29 — `se` skipped C++ and module-JavaScript test files when tracing

- **What happened:** `is_text` knew `.c`, `.h`, `.js`, `.ts` and not `.cpp`, `.hpp`, `.mjs`, `.tsx`
  and their kin, so the trace row reported oopc's `REQ2/CXX-3` as untested while `src/test_oopc.cpp`
  named it, and the citation scan skipped the same files.
- **Kind:** K3 (the row was sure).
- **Cost:** two requirements shown as untested that were not; found by the owner reading the row
  against the file.
- **Findable by:** a fixture naming a requirement only in a file of each type; seen red for all eight
  before the fix.
- **Changed:** the extensions are in `is_text` (PR #3).

## 2026-10-29 — With no repository guide, `se` took a README's workflow path for the check command

- **What happened:** on the fall-2026 data-mining course repository, which had no CONTRIBUTING.md or
  CLAUDE.md, the doctor's fallback took the first backticked thing on a README line that mentioned
  tests, `.github/workflows/ci.yaml`, as the check command, then failed the CI row against it. The
  handoff written there reported it.
- **Kind:** K3 (a fallback that reads prose as a command).
- **Cost:** one false row in that repository's baseline; caught by the agent reading the README line.
- **Findable by:** a fixture with a README alone, whose only backticked text beside "tests" is a path.
- **Changed:** the fallback runs for CONTRIBUTING.md and CLAUDE.md only; a README alone yields *none
  yet* (queue #9).

## 2026-11-02 — Comparing the Python tools with the Node tools: a clean run that proved little

- **What happened:** the port of `check.js`, `since.js`, and `bodies.js` matched them on every release
  tag and on 150 random breakages, 481 comparisons with no difference. Three bugs planted in the
  port went unnoticed by that same run. Removing each reporting line in turn then found three no case
  reached, and a sharp look found slug cases that failed the same way in both tools, so they could not
  tell them apart.
- **Kind:** K3 (identical output read as proof of equivalence).
- **Cost:** about an hour; found before the Node tools were gone, while they could still referee.
- **Findable by:** plant a bug in the thing under test before trusting the comparison.
- **Changed:** 69 targeted cases, one or more per rule, identical in both tools. Every removed report
  and logic change then seen caught, except `.strip(WS)` against `.strip()` in `bodies.py`, which
  differs only for a principle ending in a character like U+0085. Every Unicode codepoint compared for
  slugs and whitespace: whitespace identical; slugs differ on 14,049 codepoints, all unassigned in
  Python 3.11's Unicode 14 and assigned later in Node 24's, so a heading using one could slug
  differently. What Node can no longer referee is fixed in `tools/test_check.py`, and these fixtures
  were seen to catch the mutants they were written for. CI then failed both Windows jobs: report paths came out with backslashes, which the
  Node tools did too and nothing had tested. Forward slashes everywhere, then all six jobs green (run
  41506991552, queue #12). The cause was inferred from that fix, since the failing log was not read.

## 2026-11-02 — A hook fired on a real compaction, and misreported it

- **What happened:** the first compaction seen with a hook wired, in the session building v1.4. Nothing
  was running after 19:50:43; compaction began at about 20:44:40 and ended at 20:45:43, about 54 minutes
  in, replacing 431,381 tokens with 12,837. The transcript's `compactMetadata` records the trigger as
  `auto`; that it was the idle compaction is inferred from the timing. `SessionStart` with source
  `compact` ran `se --post` 0.1 seconds after the boundary's timestamp, and the agent's next turn opened
  with `YOU WERE COMPACTED` and SE1/A11's rule. The agent took its summary as recalled and went to the
  transcript. The alarm was right and its numbers were wrong: `0 time(s)`, `(None)`, `? tokens with ?`,
  where the transcript shows one compaction and the figures above.
- **Kind:** K3 (the wrong count passed for true until this run, because a simulated `source: compact`
  was the only test, and it printed the same line).
- **Cost:** none to the work; the source was read before anything relied on the count.
- **Findable by:** compare the hook's words with the transcript at the first real compaction. The
  likely cause, inferred and not shown, is that the boundary reaches the file after the hook has read it.
- **Changed:** `se --post` waits up to two seconds for the record, and otherwise says the transcript has
  not recorded it, without a count or a size; a record older than two minutes is not taken for this
  compaction. Fixtures cover each case, including the record arriving during the wait. Whether the wait
  ever helps is unknown until the next real compaction. It also prints the mission and shape from the
  source (SE1/D9). The README says what was seen. Open: a manual `/compact` is still unobserved, and the
  doctor cannot tell a fired hook from a configured one.

## 2026-11-02 — Codex found 4 of 5 planted defects, then real ones the check had passed

- **What happened:** the second review by another family, on a copy with five defects planted. It found
  4 of 5, and missed the weakened phrase test in `ADOPT.md`, a file it did not read
  ([the method](../archive/reviews/REVIEW-METHOD-other-family.md)). With the plants filtered, it reproduced
  a real failure: `REQ1/MISSION-1 verdict rejected 2020-01-01` passed the trace row for a requirement that
  began in v3. It also showed the README index check letting a contradictory entry through, and a test named
  "no runtime but Python" that refused only Node. Its report also noted the doctor's citations row red on
  a test fixture written the same day: the check had passed, so the drafter reported the row without
  rerunning the doctor.
- **Kind:** K3: a green check read as covering what it did not look at, each time. The row said "passed
  by a person" for a line no person had to give.
- **Cost:** small: about three minutes of the reviewer's time, then the fixes.
- **Findable by:** executing the rule with a value it should refuse, which is what the reviewer did. It
  would not have been found by more cases of what the rule allows.
- **Changed:** a verdict needs an outcome, the requirement's current version, and `by` a judge
  (REQ1/SE-1); the check holds README's index to the headings both ways (REQ1/ID-1) and allows only the
  runtimes contributing uses (REQ2/CHK-4); `se --post` no longer says a multiplexer saves the session; and
  the check now runs the citations row on this repository, so a bare ID in a fixture goes red before a
  doctor is asked. `se` still cannot check who wrote a verdict, or which version of the work it covers.

## 2026-11-02 — A manual `/compact` fired the hook, and the fix said what it could know

- **What happened:** the owner ran `/compact` in the session building v1.4, after the release commit. The
  transcript records the trigger as `manual`, 277,342 tokens replaced with 11,939, at 23:34:58. `SessionStart`
  with source `compact` ran `se --post`, and the agent's next turn opened with `YOU WERE COMPACTED just now.
  The transcript has not recorded it yet, so its size is not known here (1 earlier on record)`, then the
  mission and shape from the source. Each part was true: one earlier compaction was on record, and no count
  or size was invented, where the idle compaction had printed `0 time(s)` and `? tokens`. The owner saw the
  hooks fire.
- **Kind:** K1 (the fix from the entry above, tried on the case it was written for).
- **Cost:** none.
- **Findable by:** what found it: comparing the hook's words with the transcript at a real compaction.
- **Changed:** the README and queue #4 now say a manual `/compact` was seen. This also bears on the open
  question about the wait, and changed nothing in `se`: the hook ran 2,206 ms, so the two-second wait ran out,
  and it finished at 58.096, 9 ms before the boundary's timestamp of 58.105. That is the likely cause above
  seen again, and it suggests the record cannot arrive during the wait, which then costs two seconds per
  compaction for nothing. One run, inferred from timestamps, with no harm done, so the wait stays until
  someone looks. The doctor still cannot tell a fired hook from a configured one.

## 2026-11-02 — `since --write` wrote markers that name no release

- **What happened:** during the v1.4 release commit, before the tag, a test ran `since --write` in its copy
  of the repository and wrote `text since unreleased (unreleased)` into ten markers, which made a second test
  fail for a reason of its own. Run in a copy, the same thing happened after the tag, on any changed principle,
  while CHANGELOG.md has no unreleased section, which is the state right after every release. `--write` then
  disagreed with its own `--check`.
- **Kind:** K3 (a fallback string took the place of a release, and looked like one).
- **Cost:** a release-time scare, settled by testing a tagged copy. No bad marker was committed, since the checker
  goes red on them.
- **Findable by:** a fixture with no unreleased section; every earlier fixture had a section or a tag to name.
- **Changed:** in either state `--write` refuses with exit 2, writes nothing in any chapter, and says what to add;
  `--check` says the same. Fixtures cover both states and both legitimate paths, `--as` and a named section; the
  refusals failed first, and a mutant that writes chapter by chapter is caught (queue #14, v1.4.1).

## 2026-11-02 — v1.4.1 went out red on one CI job, because the tag went up with the commit

- **What happened:** `main` and `v1.4.1` were pushed together, and `windows-latest` with Python 3.9 then failed on
  both, with the other five jobs green. The likely cause: the new refusal prints an em dash to stderr, `since.py`
  set UTF-8 only on stdout, and the test decodes both as UTF-8. Forcing cp1252 here gives byte `0x97` and that
  decoding error. The runner's log was not read, since it needs a login, so this is inferred until the job goes green.
- **Kind:** K3 (the same class as the 2026-10-28 hash on that platform; a green local run felt like enough).
- **Cost:** a public tag whose check fails on one platform. The refusal itself works there; `se` and the copies
  are untouched.
- **Findable by:** CI on a branch before the tag. Pushing them together meant the tag was public before the
  matrix ran, and a tag is not moved.
- **Changed:** `since.py` sets UTF-8 on stderr too, with a test that forces cp1252 and was seen to fail first (v1.4.2). v1.4.2's
  commit ran the whole matrix on a branch before its tag existed. `v1.4.1` stays where it is, red on that job.

## 2026-11-03 — `se --post` looked at less than it said, off the platform it was written on

- **What happened:** the owner asked about `du` and `pmset`. `du` does not exist on Windows, so the transcript
  line vanished there with no word. Windows' battery was never read, so a laptop on battery was not fragile.
  Linux read only `BAT*`, the first of them, and always said "sleep not prevented", having not looked.
- **Kind:** K3 (an unexamined `False` read as a finding; CI's `--version` never reached this code).
- **Cost:** none seen; no one has reported running it on such a machine.
- **Findable by:** asking of each command what it does on the other two platforms. CI on three platforms did not
  find it, because the tests inject the power reading and no job called the real one.
- **Changed:** see queue #16. A test now calls the real reading on every CI job. That shows it runs, not that it is
  right: a runner has no battery, so queue #17 stays open. What is left is in queue #18 to #21.

## 2026-11-02 — Verdicts on the mission and the shape

Given by their judge on `REQUIREMENTS_v3` as sent, and recorded here by an agent (SE1/U10).

- REQ3/MISSION-1 verdict: pass, by Warren MacEvoy, 2026-11-02
- REQ3/SHAPE-1 verdict: pass, by Warren MacEvoy, 2026-11-02

## 2026-11-03 — Four limits: a vendored tree, Zellij, containers, and the review's isolation

- **Vendored trees (queue #22).** `check_citations` read `../tribe`'s `vendor/compaction/` as its own and
  failed. Looking for the cause showed two false passes that nobody had reported, both worse than the failure:
  a vendored test naming a requirement counted as covering it, and a vendored verdict line could pass a judged
  requirement of the same name. **Changed:** citations, trace, and verdicts read `own_files`; both rows name
  what they left out. Only a top-level `vendor/`: elsewhere a false failure stays to be read. Nested or
  `third_party/` trees therefore still fail, and a repository that keeps its own files under `vendor/` has them
  skipped, named in the row. Not changed: `dm.py`, which is another repository's and has its own scanner.
