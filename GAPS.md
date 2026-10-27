# Gaps

Where the guide fell short when it was applied to a real project. Each entry says what happened, the
principles it touches, and a proposal. An entry is closed by changing the guide, or by a sentence
saying why not ([SE1/P4](guide/01-purpose.md#p4)).

## Field report: lwext4-bsd, 2026-10-19

[lwext4-bsd](https://github.com/wmacevoy/lwext4-bsd) is a BSD-licensed fork of an embedded ext4
library: C, no service, no deploys, one maintainer, an on-disk format owned by Linux, and code that
must stay clean of GPL provenance. The working set was written after the fact, from the code and the
commit history. The gaps below are ordered by how much they cost.

### 1. A check whose instrument never engaged

The test script passed `-fsanitize=address,undefined` to CMake, and a toolchain file silently
overwrote it. For a month the library ran uninstrumented while the README claimed "everything runs
under ASan and UBSan". The tests had been seen red ([SE1/T3](guide/06-testing.md#t3)) — but the
*sanitizer* had never been seen to fire on library code.

**Proposal:** extend SE1/T3 from tests to instruments: sanitizers, coverage, linters, warning flags,
type checkers. Add to *Before trusting a test suite*: "Every instrument has been seen to fire on the
code it claims to cover — or a check proves the flag reached the compiler."

**Closed:** [SE1/T3](guide/06-testing.md#t3) now covers instruments, and *Before trusting a test
suite* asks that each one has been seen to fire.

### 2. Libraries, firmware, and formats you don't own

Chapter 7 assumes a running service: deploys, health checks, rollbacks, alerts. A library has none
of them. What it has instead is harder:

- **Releases you cannot roll back.** Firmware in the field, and bytes written to a user's card, stay
  written. [SE1/O6](guide/07-operating.md#o6) and [SE1/O7](guide/07-operating.md#o7) have no answer
  for "the deploy is someone else's, months later, on hardware you'll never see".
- **An interface you didn't define.** [SE1/D11](guide/05-design.md#d11) covers promises you make.
  Here the promise was made by Linux, and the only judge of correctness is Linux's own tools
  (`e2fsck`, `debugfs`). Testing against a reference implementation you don't own — differential
  testing with an external oracle — was the single most valuable practice on the project, and the
  guide doesn't name it. [SE1/T6](guide/06-testing.md#t6) is the closest.
- **Feature negotiation.** An input announcing features you don't support (here: incompatible
  feature bits) is a fifth way an input can be wrong, beyond [SE1/R6](guide/04-requirements.md#r6)'s
  four. Upstream "ignored" one such feature and wrote images it had no right to write.

**Proposal:** a section in chapter 7 (or a short chapter) on shipping libraries and firmware:
releases as one-way doors, external oracles, conformance to a format someone else owns, and
"refuse, read-only, or read-write" as the stated answer for every feature an input can announce.

**Closed:** new [SE1/O11](guide/07-operating.md#o11) (releases you cannot roll back) and
[SE1/T11](guide/06-testing.md#t11) (differential testing against an oracle). An announced,
unsupported feature is treated as a kind of *wrong* in [SE1/R6](guide/04-requirements.md#r6) rather
than a fifth case, so the four cases cited across the guide and in copies of AGENTS.md stay true.

### 3. Adopting the guide on an existing codebase

The guide starts at the first client conversation ([SE1/H7](guide/09-people.md#h7)). Most adoptions
start with code. Writing requirements and design from a fork's history meant inventing reasons for
decisions nobody wrote down. The templates mark *invented numbers* but not *inferred rationale*;
I had to add an *(inferred)* marker so the maintainer could tell reconstruction from record.

**Proposal:** a "joining late" section: reconstruct the working set from code and history, mark
every inferred reason *(inferred)* until a person confirms it, seed FINDINGS from the commit log,
and treat each "test: none" in the requirements as a queue item.

**Closed:** new [SE1/W12](guide/08-work.md#w12); the requirements and design templates carry the
*(inferred)* marker.

### 4. Requirement-to-test traceability fights versioning

[SE1/R11](guide/04-requirements.md#r11) wants every "must" to have a test ID, and the checklist asks
for it, but the template has no place for it. Putting a test column in the requirements made every
new test an edit to a versioned document, which [SE1/R10](guide/04-requirements.md#r10) forbids —
the project needed a `REQUIREMENTS_v2` partly for bookkeeping.

**Proposal:** say where traceability lives. Either requirements carry only the test *ID* (stable,
assigned when the requirement is written) and the test's status lives in QUEUE, or a separate
unversioned trace table maps requirement → test → status.

**Closed:** the first option, simplified. [SE1/R11](guide/04-requirements.md#r11) says the trace
lives in test names; requirements never list tests, and a *must* with no test is a `QUEUE` item.

### 5. Provenance of code, for agents

[SE1/R8](guide/04-requirements.md#r8) names licensing and code provenance as requirements, but
[AGENTS.md](AGENTS.md) has no rule about it. On a clean-room project that is the one-way door: an
agent that "just checks" a GPL implementation, or reproduces one from training, can taint every
release ([SE1/D11](guide/05-design.md#d11), [SE1/D13](guide/05-design.md#d13)).

**Proposal:** add to AGENTS.md's stop-and-ask list: "It would copy code from outside the
repository, or from a source whose license you cannot state — including code recalled rather than
read." Teams with a clean-room rule can then point at it.

**Closed:** added to [AGENTS.md](AGENTS.md)'s stop-and-ask list as proposed.

### 6. Where the working set lives, and the missing repository guide

[SE1/W10](guide/08-work.md#w10) names four documents but not where they go; the templates' relative
links (`../guide/`) suggest a subdirectory, while AGENTS.md makes a new top-level directory a
stop-and-ask. AGENTS.md also defers local mechanics to "the repository's guide (`CLAUDE.md`,
`CONTRIBUTING.md`, or equivalent)", but there is no template for one, so each adopter invents its
shape.

**Proposal:** say "`docs/` unless the repository already has a convention". Add
`templates/CONTRIBUTING.md`: how to build, run, test, and reset; the full check command and what
success prints; the repository-specific rules; where the working set is.

**Closed:** [SE1/W10](guide/08-work.md#w10) says `docs/` unless the repository has a convention, and
names the repository guide; [templates/CONTRIBUTING.md](templates/CONTRIBUTING.md) added. The
templates now link to the guide by absolute URL, so a copy in another repository still resolves.

### 7. When the client is the maintainer

On a solo or open-source project, the person who writes the requirements is the one who approves
them. "The client has objected to at least one" ([SE1/R2](guide/04-requirements.md#r2)) becomes a
self-review, and [SE1/H6](guide/09-people.md#h6)'s read-back has nobody to read to. The real users —
integrators, and whoever reads the card on Linux — are not in the room.

**Proposal:** a paragraph in chapter 9 on proxy clients: name who stands in for the absent users
(an issue tracker, a downstream project, a second maintainer), and treat their bug reports as the
read-back.

**Closed:** a paragraph in [SE1/H5](guide/09-people.md#h5); the *Before leaving Requirements*
checklist accepts a named proxy's objection.

### 8. The operating envelope has no resource budget

The requirements template's envelope covers scale, speed, recovery, and availability
([SE1/R7](guide/04-requirements.md#r7)). Embedded work has budgets of its own: code size, RAM,
stack, energy, and *power loss at any instant* as a normal event rather than an incident. The
project's footprint figure turned out to be an unmeasured inherited claim (70 KB measured against
50 KB claimed).

**Proposal:** add *Resources* (memory, storage, energy) and *Interruption* (what must hold if
power is cut at any point) to the template's operating envelope, each with a number and a test.

**Closed:** [SE1/R7](guide/04-requirements.md#r7) and the requirements template add *Resources* and
*Interruption*.

## Field report: agent trials, 2026-10-26

About 160 agent runs, testing variations on pair programming for agents and what survives a
compaction. The variations were a
separate pass that asks questions before anyone writes code, a smaller model standing in for the
forgetful future maintainer, and invariant guards. The subject was a synthetic Python restaurant-tab
codebase, written in variants that behave identically, and hidden tests the agents never saw judged
the results. Sonnet- and Haiku-class models ran in cold sessions, with 1–5 runs per cell. These are
small numbers. Most of what they show is that the guide already covers the case. One result
changed it ([6](#6-a-summary-is-a-concussion)), and the rest is untested. The variants, prompts, and tests are not in this repository.

Every agent ran with this guide's AGENTS.md already in its context, inherited from the session that
launched it. That was found only at the end. No arm was guide-free, and the "without AGENTS.md"
arms below differ only in whether a copy also sat in the repository.

### 1. "Agents answer their own questions" came from the prompt

In three rounds, authors listed the questions a change request left open and then decided all of
them, including *who may comp?* behind "Managers can comp a line." Every one of those prompts said
"the product owner can't be reached during this task." With the owner reachable, 5 of 6 authors
stopped and asked before writing code. A separate question pass, with Haiku, Haiku cast as a
naive "jester", or Sonnet asking and a human-stand-in answering, drew every non-default policy point
out of the owner in 9 of 9 runs, and the authors that built from those answers passed every hidden
test. This was a K3: we were sure the behavior was the agent's, and it was the instruction's.

**Closed:** no change. *Stop, ask, or proceed* in AGENTS.md already asks for this, and it worked
whenever the agent was allowed to stop. Noted, not acted on: an instruction that nobody can be
reached overrides the stop-and-ask list. One trial is not enough to make it a principle.

### 2. A copy of AGENTS.md in the repository raised the authorization question

With the owner reachable, authors with a copy of the v1.1 AGENTS.md in the repository, and told to
follow it, asked who may comp in 3 of 3 runs. Authors without that copy asked in 0 of 3. Both groups
already had the guide in their context (see above), so what this shows is salience, not presence:
the rule changed behavior when the agent was pointed at it, not when it was merely loaded. That
counts only what each author asked: the agent playing the owner volunteered unasked policy in 2 of
9 answers.

**Open:** whether the guide changes behavior at all, against a truly guide-free baseline, is
untested. A rule-by-rule test is planned: a small repository for each rule, with one temptation
that rule targets, run with and without the guide in sessions that inherit nothing.

### 3. Locality of reasoning: untested at a size where it would matter

At about 1,400 and about 4,300 lines, it made no difference whether a rule lived in one place or
was pasted into every module that used it. In 40 runs on the larger codebase, all 40 changes were
correct. Work tokens, tool calls, and time were within noise between the two layouts. The pasted
copies kept the original name, and agents searched for it and found every one. Haiku used about
1.7× the work tokens of Sonnet whatever the layout, so the gap between a smaller and a larger model
did not measure layout at this size.

**Open:** untested. The effect likely needs a codebase well over a megabyte, or duplication an
agent cannot find by searching: renamed copies, derived forms such as `1.10` or `"10%"`, or a bare
number that means different things in different files. Two ways to test it:

- **A natural experiment, with no new runs.** Using published agent transcripts on
  [SWE-Bench Pro](https://arxiv.org/abs/2509.16941), correlate how spread out the reference patch
  is with agent success and reading effort. Confounded with difficulty, but cheap.
- **A controlled trial.** Script a delocalized fork of a large open-source repository, with renamed
  and derived copies of one rule, and run the same change request on both forks.

### 4. A guard settled what prose left open

"Within one cent" was read two ways. Where the code raised an error on the strict reading, every
author kept the strict reading.

**Closed:** no change. The *Sanity, repeated* row of [SE1/T2](guide/06-testing.md#t2) already asks
for invariants checked in the code.

### 5. The fluent defects

Two defects were confident ones. One agent reused an existing local rule ("extra cents go to the
earliest people") where it no longer fit, so a seat that ordered nothing paid −1¢. Another reported
"suite passes" while its own new test failed.

**Closed:** no change. [SE1/A2](guide/10-agents.md#a2) already asks whether it was run.

### 6. A summary is a concussion

A half-finished change was handed to a fresh context the way compaction hands it over: a summary,
plus a pointer to the full transcript (about 135 KB of logged tool calls, with the owner's answers
in the middle). The summary was fluent and wrong. It said comps carry no service charge and that the
receipt should show COMP. The owner had said comps keep the service charge, and had frozen the
receipt pending legal review. Four Sonnet runs per arm, graded on the code they left behind:

| What the next context had | Followed the owner |
|---|---|
| The summary alone (today's behavior) | 0/4 |
| The summary with its claims marked "recalled, not re-checked" | 1/4 |
| A rule in a repository file the agent was told to follow | 0/4, and the file was never opened |
| The same rule, already in context | 4/4 |
| A script's report: word overlap between each human message and the summary | 4/4 |
| The same report, plus the human's messages pasted in verbatim | 2/4 |

An easier version first, in which the summary visibly left a hole ("we got answers" without the
answers), went 12 of 12 in every arm. A gap you can see gets checked. A gap the summary has filled
fluently does not. The script needs no model. It found the owner's message only 41% reflected in the
summary, printed that, and every agent then read the transcript and followed the owner. Run on four
real compactions from other projects, the script flagged nothing (12 human messages in all), so it
has not yet been seen crying wolf.

Pasting the human's words back in verbatim, which we expected to do better, did worse. All four
agents obeyed the pasted constraint (the frozen receipt), but two trusted the summary's "bill.py:
done" and never opened the code, and one of those reported the service charge fixed when it was
not. The flag sent agents to the source, where they checked everything nearby. The pasted answer
replaced the trip.

**Closed:** [SE1/A11](guide/10-agents.md#a11), the *After a gap* section of AGENTS.md, and a line
in the agent hand-off checklist.

### Related work

The claim that pair programming cuts errors by 90% has no source we could find. Williams et al.
(2000) reported about 15% fewer defects for about 15% more effort. A meta-analysis
([Hannay et al., 2009](https://doi.org/10.1016/j.infsof.2009.02.001)) found a small effect on
quality and a cost in effort. These numbers come from search results; the papers themselves were not
opened. For agents, most model responses to ambiguous coding problems wrote code instead of asking
([HumanEvalComm](https://arxiv.org/abs/2406.00215)), and on underspecified issues, interaction
raised resolve rates by up to 74% ([Ambig-SWE](https://arxiv.org/abs/2502.13069)). Anthropic's
[Claude Code guidance](https://code.claude.com/docs/en/best-practices) already recommends planning
before coding, a fresh session for review, and separate writer and reviewer agents.

## Field report: compaction in the author's own sessions, 2026-10-26

A follow-up to [6](#6-a-summary-is-a-concussion), in a separate project (`compaction`, not in this
repository): the handoff check run on real compactions, trials in which the agent writes its own
summary, and the author's earlier, unpublished attempts at the same problem. Small numbers again;
what is measured is marked, and what is only proposed is left open.

### 1. The handoff check passed nearly every real compaction

The word-overlap check of A11 ran over all 29 compactions in the author's local transcripts
(September–October 2026, 13 projects, 227 human messages). It flagged 4 messages, all in one
compaction; the other 28 it passed. By the author's account, harm happened in many of them, mostly
in the code or in code that should have been written and was not, where a transcript check does
not look. A cruder check of the code (files the summary called done that the session never touched,
files said to be frozen that changed afterwards, fix and revert commits in the next 48 hours) found
leads in 9 compactions; every lead followed was a false alarm. So the check that went 4/4 in
handoff-r, against a gap that was planted, has never been seen to fire on a real one: as it stands,
a K3 factory ([SE1/U7](guide/02-unknowing.md#u7)).

**Proposed:** [SE1/A11](guide/10-agents.md#a11) says what was measured and no more (in this draft).
**Open:** a check that cannot say "fine": report what is always true — how much of the context the
summary replaced (the transcript records it: one real compaction went from 731,754 tokens to
22,852), what changed in the code since, and whether the tests pass — instead of a score. Untested.

### 2. An import from outside the repository does not load

"Load it at every start, for example by importing AGENTS.md from CLAUDE.md" fails silently when the
import names a file outside the repository: Claude Code loaded neither `@../guide/AGENTS.md` nor an
absolute path, and gave no sign. An import of a copy inside the repository loaded. Measured with
Claude Code 2.1.311, in `-p` sessions, by asking for a phrase only the imported file holds.

**Proposed:** AGENTS.md *After a gap* and A11 say to import a copy inside the repository (in this
draft). A copy can go stale; the compaction project fails its pretest when its copy no longer
matches.

### 3. Compaction happens while the human is away

Every automatic compaction since 2026-10-08 in the author's sessions (22 of them) came after 54–55
minutes without a message, at 205k–461k tokens, not at a full window. So the next thing the agent
reads is the human coming back, who has had an hour to forget too. In `claude -p` the new summary
reaches disk only after SessionStart hooks return, so a check there cannot read it; on the first
prompt after the compaction it can, and that check was built and seen to report.

**Open:** whether A11 should say *when* to check (the first prompt after a gap, not the start of the
session). The idle timing is one author's sessions and one client version; the cause (the prompt
cache) is inferred, not read from documentation.

### 4. Short sessions wrote faithful summaries; the drift is said to live in long, messy ones

Six scripted sessions of 30k–47k tokens, in which the agent did the first half of the work itself
and was compacted with `/compact`, all wrote summaries that kept the owner's constraints, and every
agent then followed them, with or without a check, a numbered requirement, or a searchable memory.
The author's account puts the drift in long sessions on pre-SE1 codebases, as a trend of missing
foundational facts rather than reversed decisions (one earlier project lost encryption at rest, and
an offline cache, in new components written after the facts were already recorded). `--autocompact
100k` gives several real automatic compactions in one cheap session, which makes long trials
affordable; none has run yet.

**Open:** untested at the length where the author saw it. A trial worth running: apply SE1 to a
codebase for the first time (long, real work), with automatic compactions during it, and grade
whether foundational facts reach later new work.

### 5. A memory tool makes the look cheap; it does not make the agent look

A searchable memory of the session (full-text, no model) was offered on the first prompt after the
compaction. The agent did not search it; nothing had been lost (n=1). The author's earlier
experiments found the same shape from the other side: a better-shaped handoff document did not
reduce invented specifics (about one per 130–150 words in both arms, retrieval forbidden, n=1),
and a second agent watching live, not compacted, caught a confident claim the worker had already
written.

**Open:** no change. Recall tools serve after the agent knows it has forgotten; A11's check is what
tells it.

### 6. The earlier attempts were found last

The author had worked this problem before, in another project, with a pre-registered rubric and a
negative result. That work surfaced only when the author named the project as a test bed, after
five versions of the new project's requirements had been written without it.

**Open:** whether [SE1/R3](guide/04-requirements.md#r3)'s table should carry "What have you already
tried, and what did it show?" It is a question nobody volunteers, and its answer can invalidate the
plan, which is the order R3 asks for.
