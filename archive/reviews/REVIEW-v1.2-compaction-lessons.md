# Review: what the compaction trials since 2026-10-26 should change here

Reviewer: Claude Opus 5.5, at the author's request. Date: 2026-10-28. By the learning review's L6, a
later model should doubt this before the rest of the guide. Against: branch `v1.2/after-a-gap` at
d256d10. Status: **a proposal**. No guide file is edited. Sources are the compaction project's
`docs/FINDINGS.md` (cited by line, as of 2026-10-28) and its DESIGN_v5 to v10. Everything was
observed unless it says *inferred*.

## Answer

**One change, and it is small:** a paragraph in A11, saying that the summary is not the only
injury and pointing at O3. The rest is a GAPS field report, mostly "Closed: no change". One more line
(SE1/A10) is optional.

## How this was reviewed

The author asked that the tribe review the suggestions. A draft of six candidates went to four fresh
readers, each looking through one lens, and to one elder. All were Claude subagents. The fresh four
had no context but the draft and the sources. The elder was a fork of the drafting session, so they
had its life but also its blind spots.

- **The engineer** checked every quote and number against its source. They found two overstatements
  ("several said why" is two runs; a "6 of 36" taken from another entry's paraphrase). They also
  found one real gap: the guide asks reviewers about the requirement a change *serves*, never about
  the ones it must *not break*.
- **The cynic** refuted the keys sentence. AGENTS.md already says to stop "before doing any of the
  work" when "the task contradicts a requirement", and O8 already says "No insecure fallbacks". So
  the members broke rules that exist. The cynic also weakened the review-by-name item: naming the
  requirement was pointing at the defect, and there was no negative control.
- **The artist** found the centre the draft had left out: knowing is not doing (P1 below).
- **The buddhist** sent most items to GAPS only, and found the review-by-name item already proposed
  in REVIEW-v1.2-learning.md (draft L5).
- **The elder** found that the human, not any check, caught today's three worst defects (proposal P2), and
  cut the item about a budget cap, a quirk of the trial harness.

The draft's own items S1 (a keys sentence in AGENTS.md) and S2 (review by requirement ID) did not
survive as rule changes. What remains of them is in the field report.

## P1. A11: the summary is not the only injury

**Evidence.** On viki, a C project whose decision D-9 is "Encryption at rest everywhere", Claude
Haiku members, with SE1 (AGENTS.md and chapter 2) as background in every arm, built a brief-history
store again and again:

- **None of the 71 stores built through the compaction project's DESIGN_v5 was keyed** (FINDINGS:333).
  **None of the 50 counted runs after it encrypted** (FINDINGS:252).
- **With no compaction at all, every new store was plaintext.** That includes a run that "had named
  the encryption layer one turn earlier", and makes "9 of 9 plaintext, compacted or not"
  (FINDINGS:525–532).
- **Members wrote D-9 into their own journals in 19 of 20 runs, and into their code in none** (arms
  T and T2).
- **An arm given a guard "kept the guard byte for byte and read the AGENTS.md line, and none executed
  the guard"** (FINDINGS:334).
- **The one store that changed course was refused by a hook at a pause** (run H-10).

A11 as written puts the injury in the summary. These trials say a requirement freshly read is
still left out of new work, and that only a check the agent does not have to choose to run carries
it in. That is O3, "A convention CI does not enforce is not a policy", applied to an agent.

**Proposed: one paragraph in A11**, after the trials paragraph and before "So treat every handoff
as a possible injury":

> The summary is not the only injury. In later trials, agents with the requirement freshly in front
> of them, and no compaction at all, still left it out of new work: no store of 71 built against
> "encryption at rest everywhere" was keyed, and the agents who recorded the requirement in their own
> notes left it out of their code. A guard the agent had to choose to run was read and never run;
> the one store that changed was refused by a hook. Recall gets a rule into the next context. Only a
> check that runs on the new work, without the agent choosing to run it, gets it into the work
> ([SE1/O3](../../guide/07-operating.md#o3), [GAPS](../../GAPS.md#1-knowing-is-not-doing)).

**Strength.** Strong for one model, on one task, against one requirement. It holds across every batch
and every arm from DESIGN_v4 to v10. *Wrong if:* in another project or model, agents who have a
requirement freshly in context apply it to new work without a check that runs.

A11 is *New in v1.2* and unreleased, so it can change without a marker.

## P2 (optional). A10: write down what the human saw that the checks did not

**Evidence.** These come from one session, 2026-10-28. Three of its worst defects were each found by
the author pointing, after every check had passed them:

- "the test is invalid" came after the at-rest guard had passed its tests and graded two batches.
- "did you give yourself a break? which of these did you adopt?" found that the agent had applied
  none of the mechanisms it was testing to its own work.
- "AGENTS should refer to who wrote them" pointed at what git showed in a minute: every commit to
  this guide's AGENTS.md was co-authored by an agent, and its text does not say so.

None was caught by a test, a hook, a rubric, or the project's own review familiar. The familiar
caught a defect only when it held a card that already contained the answer (FINDINGS, 2026-10-28).

**Proposed:** one sentence at the end of A10. "When a person finds what the agent and the checks
missed, that is a finding about every check that passed it: write it down beside the check that
should have caught it." **Strength:** weak, one session. GAPS alone would also be honest.

## P3. GAPS.md: a field report

Drafted in the form of the existing reports, to go after *Field report: compaction in the author's
own sessions*.

---

## Field report: agent tribes and checks, 2026-10-28

About 300 agent runs and reviews over three days, on a snapshot of viki: a C project with a
morning-brief script, whose decision D-9 is "Encryption at rest everywhere". The task, at the third
of three owner turns, was to add a store of past briefs. The arms varied what helped the agent across
a compaction:

- the agent as a successor with a journal (a tribe);
- a hook that refused plaintext at the end of a turn;
- a jester;
- a break with colleagues;
- words about agency;
- an invitation to walk the author's book;
- a framing at the first compaction;
- a council at a pause.

Claude Haiku throughout, with SE1 (AGENTS.md and chapter 2) as background in every arm, so no arm was
guide-free. Graded by script on the code left behind, with at-rest guards and a probe. These are
small numbers: 10 runs per arm, one task, one model. Most of what they show is that the guide
already says it. The runs, harness and rubrics are in the compaction project, not this repository.

### 1. Knowing is not doing

Described above (proposal P1).

**Closed:** [SE1/A11](../../guide/10-agents.md#a11) extended (if P1 is taken), [SE1/O3](../../guide/07-operating.md#o3).

### 2. A guard tested only against its own stub was wrong

The at-rest guard's stub of viki printed a ledger viki never prints, and its tests ran the guard
against that stub, so they could only agree with it. It graded two batches. A replay against viki's
real output format found it; its replacement is checked against the `printf` formats in viki's
source.

**Closed:** no change. [SE1/T6](../../guide/06-testing.md#t6) already says the mock and the real thing
answer to the same test.

### 3. A hook that never ran on the turns that mattered

A Stop hook meant to refuse plaintext ran only on turns that ended normally. Most compacted turns
ended on "Autocompact is thrashing" (15 of 21 and 12 of 18 in two arms), and those never reach Stop.
The hook blocked in 4 runs of 10, and moved one store.

**Closed:** no change. [SE1/U7](../../guide/02-unknowing.md#u7) already lists "an alert never seen firing".

### 4. Runs that never happened looked like runs that did little

The account's usage limit ended 20 of 50 runs mid-task, and the grader called them valid until a
check for the limit's text was added.

**Closed:** no change. [SE1/O4](../../guide/07-operating.md#o4), [SE1/U7](../../guide/02-unknowing.md#u7).

### 5. Reviewers are asked about the requirement a change serves, not the ones it must not break

Fresh readers shown a built plaintext store saw it from "the requirements and decisions" in 5 of 36
reviews, and in 31 more once D-9 was named; a repeat agreed within one step on 35 of 36. But naming
D-9 *was* pointing at the defect, and the two stores closest to compliant were flagged too, so there
is no false-alarm rate. Choosing which requirements are at risk is most of a review, and the probe
did that part for the reader. [SE1/W11](../../guide/08-work.md#w11) and the definition of done ask
whether a change satisfies "a stated requirement". Neither asks about the requirements it must not
break.

**Open:** worth a line in W11 ("list the requirements and decisions the change must not break, and
ask about each by ID") once a trial has a negative control. It is also proposed in
REVIEW-v1.2-learning.md (draft L5).

### 6. An ID survives a summary; its meaning does not

Across compactions, summaries kept the label "D-9" and lost what it said ("Fossil pinned at 2.28
(D-9)"). viki's own CLAUDE.md lists "**D-9** Fossil is pinned at 2.28". This is one run and one file.

**Closed:** no change. [SE1/D6](../../guide/05-design.md#d6) (name the authority). Citing a requirement
by ID *and* its words is a cheap habit worth trying.

### 7. The stop-and-ask on keys, with no one to answer

Some agents said a key needs the owner's decision and left the store in plaintext: two runs, and one
more in a spike, where a council had named D-9. AGENTS.md already says to stop before doing any of
the work when a task contradicts a requirement, and O8 says "A missing secret or certificate is an
exit code, not a default". The agents broke both. In these trials the owner was a script and could
not answer, which is a confound. H-2 is the rule working: it refused to write plaintext until the
key was decided.

**Closed:** no change. [SE1/O8](../../guide/07-operating.md#o8), AGENTS.md *Stop, ask, or proceed*.

### 8. Nulls, and one move in the wrong direction

- **A jester** found facts about the snapshot, never the store being built.
- **A break** raised a real risk (the cache in plaintext) in 4 of 10 runs and never tied it to the
  store.
- **Inviting the reader to walk the author's book, long or short,** did not change what a fresh
  reader saw in someone else's store. Whether it changes what they build was not tested.
- **Words about agency** changed what members left in their journals. They also built a store more
  often (10 of 10, against 5 of 10), and those stores left more fields readable, not fewer.

**Closed:** no change. These are recorded as results.

---

## Changes this would need

- **guide/10-agents.md:** the A11 paragraph (proposal P1), and optionally a sentence in A10 (proposal P2).
- **GAPS.md:** the report above, with the A11 link pointed at its heading.
- **CHANGELOG.md, v1.2 — unreleased:** under *New*, A11's one-line summary may want "a requirement
  freshly read is not applied without a check that runs". Under *Also changed*, the GAPS report, and
  the A10 sentence if taken (wording that extends A10 needs a *Changed in v1.2* marker, by the
  changelog's own rule).
- **README.md:** nothing, unless the A11 index line is reworded.
- Run `node tools/check.js` after.

## What I did not do

- I edited no guide file and ran no checker, since nothing was added for it to check. I did not
  commit.
- The run counts in the field report's opening (about 300) are a rough sum of the batches; the exact
  ones are in each FINDINGS entry.
- A review by a person is still owed. This one was by five subagents of the drafting session, all
  Claude, one of them its own fork.
