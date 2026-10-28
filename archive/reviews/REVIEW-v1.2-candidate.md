# v1.2 candidate: status and decisions

Drafter: Claude Fable 5.1, 2026-10-28, at the author's request ("review this work and draft on a
branch a v1.2 candidate"). Branch `v1.2/candidate`, from `v1.2/after-a-gap` at d256d10. This file
is the trace for whoever continues, me after a compaction included: everything below was observed
unless it says *inferred*, and the branch's commits are the record, not this file
([SE1/A11](../../guide/10-agents.md#a11)). Not committed; the author decides where reviews go.

## What I did before writing anything

Read every file in the repository, the five untracked review files, the compaction project's
README, CLAUDE.md, QUEUE, DESIGN_v10 and all of FINDINGS, and the Claude Code documentation check
(`~/projects/compaction/CLAUDE-CODE-DOCS-2026-10-27.md`). Then, before acting on any claim in a
review, opened its source:

- FINDINGS lines 199, 252, 333–334, 525–532 say what the compaction review says (0 of 71 stores
  keyed; 19 of 20 journals, 0 in code; the guard read and never run; 9 of 9 plaintext, compacted or
  not).
- `git log` confirms the learning review: A11 was rewritten 17 minutes 41 seconds after it was
  written (e1635f0 12:17:50, 594fadb 12:35:31), and all 12 commits to AGENTS.md carry an Opus 5.5
  trailer.
- `bodies()` in the checker reports A10 changed since v1.1 by exactly ` ---` (reproduced with a
  scratch script); P5, W12, H12 and A11 also end in a rule.
- The lwext4-bsd link is a 404 anonymously.
- Royce 1970, read from the scanned PDF: Figure 2 at the top of page 329, and the first sentence
  beneath its caption is "I believe in this concept, but the implementation described above is
  risky and invites failure." The v1.1 review's correction holds.
- Ambig-SWE: the abstract says "up to 74% over the non-interactive settings"; the paper's resolve
  rates (at most 46% interactive) make that a relative gain.
- **Not opened by me:** Brown 1948 (paywalled; PsycNet needs a browser), Cockburn and Williams 2000,
  Hannay 2009 (the DOI page is a 2.6 KB stub). W7's correction rests on the v1.1 review's delegated
  check, which read Miller's 1944 account; marked so in the archive.
- `trials/handoff-r/runs/2026-10-26` has no tool logs, so A11's "None of them opened the
  transcript" has no source; dropped.

## Decisions, with the reason

| Item (source) | Decision | Why |
| --- | --- | --- |
| BT1–BT4 (v1.1 review) | all taken | each verified above; BT1 gets a checker rule that goes red before the release commit |
| CT1 A3 client channel | taken, *Changed in v1.2* | contradicted by GAPS agent trials #1 |
| CT2 private agent memory | taken, in A3 | true by construction (SE1/U6); the tool exists and is in use |
| CT3/CT9 ADOPT.md | taken with the three edits | answers the audit's top item; the author asked for the draft |
| CT4 R10 wording-fix exception | **declined** | no field evidence it cost anything; "just wording" is the crack a fluent editor widens; AGENTS.md already stops an agent editing a requirement |
| CT5, CT6 GAPS chores | taken | verified |
| CT7 numbers inline in A11 | left as the author chose | preference, raised once in the v1.1 review |
| CT8 torn work | taken, U7 *Changed in v1.2* | the author's proposal; same footing as U7's other bullets |
| CT10 whitespace U8 | taken as a new principle | the author's proposal; retires a fear of its own; one commit, cheap to drop |
| CT11 medicine | taken | the author's position; wording only (SE1/R8), U7 already marked |
| SR1 W7, SR2 W2 | taken; W7 *Changed in v1.2*, W2 wording only | SR2 verified by me; SR1 from the delegated check |
| SR3–SR6 GAPS related work | taken | Ambig-SWE verified by me; the rest from the delegated check, said so |
| CC1–CC7 | folded into GAPS follow-up, A11, AGENTS.md, ADOPT.md | the documentation file was read in full; the docs were re-fetched 2026-10-28 for the archive |
| P1 knowing is not doing | taken: one paragraph in A11, numbers in GAPS | verified at FINDINGS; strong for one model and task, and it holds across every arm |
| P2 A10 sentence | **GAPS only** | one session |
| P3 field report | taken, with the learning review's evidence folded in | verified |
| L1–L6 chapter 11 | **one principle, U9**, not a chapter | the author asked for the subject; six principles on one project's trials overshoot the evidence standard; L5 to GAPS open; the full draft stays in the review file |
| L6 authorship line in AGENTS.md | taken | the author's instruction ("AGENTS should refer to who wrote them"); measured |
| Stand-up question 4 (author, mid-session) | taken, H4 *Changed in v1.2*, in the author's words | P3 asked out loud |
| `archive/` (author, mid-session) | taken: entries with URL, date, SHA-256, extraction | D13; full files only where the license allows |
| Tribe review of this draft | to run, reduced: three fresh lenses, no elder | the method's own untested claim is that one reviewer would find the same; this is the comparison |

## Commits (oldest first), all on `v1.2/candidate`, none pushed, nothing tagged

1. GAPS: sources opened, private link, vocabulary collision
2. GAPS: compaction follow-up closed with the documented mechanisms (amended after a failed edit
   script let a partial commit through; the diff was checked before amending)
3. A11: only what was measured; working directory
4. A3: an agent may ask; private memory is a head (*Changed in v1.2*)
5. U7: torn work (*Changed in v1.2*)
6. U7, R8: medicine, not cure (wording)
7. H4: the stand-up's fourth question (*Changed in v1.2*, the author's words)
8. W2, W7: Royce and Brown (W7 *Changed in v1.2*; W2 wording)
9. U8: leave whitespace (*New in v1.2*)
10. archive/: sources with checksums and extractions (carries a forward link to U9; red at this
    commit and the next, green from 12 on)
11. A11 and GAPS: knowing is not doing; field report on tribes and checks
12. U9: rules change (*New in v1.2*), with its field report
13. AGENTS.md: wording from the adversarial read; working-directory boundary; summarized
    instructions are claims
14. AGENTS.md: who drafted it
15. ADOPT.md, wired into README, llms.txt, the site nav, CHECKLISTS
16. chore: T5's table cell; .gitignore
17. check: bodies() ends at a rule (seen red first: "unacknowledged A10")
18. check: a copy must not cite an ID its label lacks (red on purpose: A11 and U9 under v1.1)
19. release: v1.2 dated 2026-10-28; copies relabeled; ADOPT pointer (green)

Checker at HEAD: 36 files, 100 principles, 0 problems in tracked files (the 16 reported are all in
the four untracked REVIEW files, whose links are written from `guide/`). Planted breakages in a
scratch worktree, each seen red: a copy labeled v1.1; a body sentence changed with no marker; U9
dropped from the index; a broken archive link; a template citing W99. A `---` inserted inside a
body truncates it and is reported as a change, which is the rule, stated.

## Review by three fresh readers, and what it cost

Three readers with no context but the diff and the sources, each through one lens, read-only,
time-boxed to about ten minutes, 500 words back, no elder (the drafter is the elder, and the
elder's blind spots are the drafter's). All three were the same model as the drafter.

| Reader | Tokens | Tool calls | Verdicts | Changes asked for |
| --- | --- | --- | --- | --- |
| Engineer | 110k | 20 | 19 keep, 2 with a change | archive lacks the `InstructionsLoaded` passage ADOPT.md relies on; U9 states its "never forks" example as fact while GAPS calls it the author's account |
| Cynic | 108k | 22 | 19 keep, 3 with a change | A11's "only a check ... gets it into the work" overclaims one store in ten; U8 holds its nearest trial and does not cite it; U9's sources disagree (they do not, read whole: see below); AGENTS.md still tells the agent to run a check the same evidence says agents do not run |
| Buddhist | 131k | 31 | 19 keep, 2 with a change | U9's "eighteen minutes" rounds a measurement into a different claim; U8 has no falsifier and is U2's K2 row plus one practice, so fold it into W7 or give it a falsifier; three trims |

About 350k tokens in all, against about 750k for the five-reader version in REVIEW-METHOD-tribe.md.

**Checked at the source before acting:** the cynic's claim that two viki files disagree. Opened
both: `core/include/viki_trace.h` says weeks of work followed and the rule was retired on
2026-08-29 in one sentence; `CLAUDE.md:700` says it was rescinded the same day it was questioned.
Compatible, not contradictory; both agent-written. The `InstructionsLoaded` passage: present in the
fetched hooks page. Everything else the readers claimed was checkable against my own commits.

**Applied, as six commits after the release commit:** A11 says what the trials showed, not more;
AGENTS.md's owner note and the hand-off checklist say the check is a hook; U8 cites GAPS #8 and
states its falsifier; the archive gains the hook passage; U9 and its GAPS entries name their sources
and say what was measured; four trims. **Not applied:** folding U8 into W7 (the buddhist's
recommendation; the cynic would keep it with the citation; the author decides, and the commit is
separate); moving the H4 question nearer P3 (harmless, the cynic said); the GAPS #2 heading that
still says *repository* (its slug is linked from three places).

**What the method found that I had not:** the AGENTS.md "run the handoff check" contradiction with
A11's own evidence (the cynic), U8's missing citation of evidence I had put in GAPS myself (the
cynic), and U9 breaking its own rule in its own examples (all three). The first is the kind of
thing the method file promised: a reader without the drafter's context sees the file whole. The
other two are the drafter's fluency: I wrote the rule and the example in one breath. None of the
nineteen commits was refuted; the one reviewer whose check turned out wrong (the viki sources)
was wrong in the careful direction, and opening the source settled it in one read.

## The walk

At the author's request, while the readers ran, the full walk of `../life-by-the-numbers/llm`:
the main book with its poem, the glossary and notes, the companion in its input order (all nine
misconceptions), and the deck; door 02 opened with its key, read, and resealed; the tree left as
found. Door 03 had been read before the walk, by a bulk read of the folder, which the first door
anticipates. A short field note is left beside the earlier one
(`llm/field-note-the-fourth-question.md`, untracked, easy to delete).

## Remaining

Nothing in the candidate. The author's decisions: tag or not; U8 as principle or folded; the
six-principle chapter instead of U9; where review files go; CT4.

## Released

2026-10-28: the author read the candidate and said "go ahead with a candidate release and check it
with a new and migrated project. add CI for the scripts. if it all works release it." Three more
commits: `se` (the doctor and the session self test, 35 tests, each check seen red on a fixture),
the wiring and the Claude-only notice, and the pin with CI steps. A new project built from the
templates passed every check after `./se --hook --write`; the compaction project, migrated, passed
after its copy was re-copied, with 24 unversioned citations left as its own finding. A clean export
of HEAD: checker 0 problems, `se --self` green, tests OK. Fast-forwarded into main, tagged v1.2,
pushed; CI green in 13 seconds; every v1.2 URL resolves; the released AGENTS.md hashes to the pin;
the doctor, online, reports v1.2 as newest.
