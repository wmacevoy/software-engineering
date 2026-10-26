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

About 120 agent runs, testing variations on pair programming for agents. The variations were a
separate pass that asks questions before anyone writes code, a smaller model standing in for the
forgetful future maintainer, and invariant guards. The subject was a synthetic Python restaurant-tab
codebase, written in variants that behave identically, and hidden tests the agents never saw judged
the results. Sonnet- and Haiku-class models ran in cold sessions, with 1–5 runs per cell. These are
small numbers. Most of what they show is that the guide already covers the case; the rest is
untested. The variants, prompts, and tests are not in this repository.

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

### 2. AGENTS.md raised the authorization question

With the owner reachable, authors that had the v1.1 AGENTS.md asked who may comp in 3 of 3 runs.
Authors without it asked in 0 of 3. That counts only what each author asked: the agent playing the
owner volunteered unasked policy in 2 of 9 answers.

**Closed:** no change. This confirms the authorization item in *Stop, ask, or proceed*
([SE1/R8](guide/04-requirements.md#r8)).

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
