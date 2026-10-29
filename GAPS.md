# Gaps

Where the guide fell short when it was applied to a real project. Each entry says what happened, the
principles it touches, and a proposal. An entry is closed by changing the guide, or by a sentence
saying why not ([SE1/P4](guide/01-purpose.md#p4)).

## Field report: lwext4-bsd, 2026-10-19

[lwext4-bsd](https://github.com/wmacevoy/lwext4-bsd) (a private repository) is a BSD-licensed fork
of an embedded ext4 library: C, no service, no deploys, one maintainer, an on-disk format owned by Linux, and code that
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

### 3. A rule in one place, or pasted into every module: untested at a size where it would matter

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

The claim that pair programming cuts errors by 90% has no controlled study behind it that we could
find. "About 15% fewer defects for about 15% more effort" is Cockburn and Williams's (2000)
restatement of the Utah experiment; the experiment's own paper (Williams, Kessler, Cunningham, and
Jeffries, 2000, *IEEE Software*) reports test-case pass rates and an effort overhead that fell toward
about 15% after an adjustment period, and Erdogmus and Williams (2003) note the effort difference
was not statistically significant. A meta-analysis
([Hannay et al., 2009](https://doi.org/10.1016/j.infsof.2009.02.001)) found a small positive effect
on quality and a medium negative one on effort. For agents, most model responses to ambiguous coding
problems wrote code instead of asking ([HumanEvalComm](https://arxiv.org/abs/2406.00215)), and on
underspecified issues, interaction raised resolve rates by up to 74% relative to the non-interactive
setting ([Ambig-SWE](https://arxiv.org/abs/2502.13069); the abstract gives the figure, and the
paper's own resolve rates make it a relative gain). Anthropic's
[Claude Code guidance](https://code.claude.com/docs/en/best-practices) recommends writing a spec
before building, a second session as reviewer, and a reviewer subagent that did not watch the code
being written. The first wording here came from search results; the papers were opened for this
wording on 2026-10-27, by a check delegated during the review of v1.1.

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

**Closed:** [SE1/A11](guide/10-agents.md#a11) says what was measured and no more.
**Open:** a check that cannot say "fine": report what is always true — how much of the context the
summary replaced (the transcript records it: one real compaction went from 731,754 tokens to
22,852), what changed in the code since, and whether the tests pass — instead of a score. Untested.

### 2. An import from outside the repository does not load

"Load it at every start, for example by importing AGENTS.md from CLAUDE.md" fails silently when the
import names a file outside the repository: Claude Code loaded neither `@../guide/AGENTS.md` nor an
absolute path, and gave no sign. An import of a copy inside the repository loaded. Measured with
Claude Code 2.1.311, in `-p` sessions, by asking for a phrase only the imported file holds.

**Closed:** AGENTS.md *After a gap* and A11 say to import a copy kept inside the working directory,
and to check that it loaded. The boundary is the working directory, not the repository: Claude
Code's documentation calls an import whose path resolves outside the working directory *external*
and gates it behind an approval that only an interactive session shows, so a `-p` session, which
shows no dialog, loads it not at all and says nothing
([memory](https://code.claude.com/docs/en/memory#import-additional-files), read 2026-10-27). The
documented controls that also stop a file loading (`blockReadsOutsideWorkingDirectories`, a Read
deny rule, `claudeMdExcludes`, `--bare`) were checked in the author's settings and none was set, so
the gate is the explanation left standing. A copy can go stale; the compaction project fails its
pretest when its copy no longer matches.

### 3. Compaction happens while the human is away

Every automatic compaction in the author's interactive terminal sessions since 2026-10-08 (24 of
them, counted on 2026-10-27) came after 54–55 minutes without a request, at 205k–684k tokens, not
at a full window. So the next thing the agent reads is the human coming back, who has had an hour
to forget too. This is documented *idle compaction*: a conversation of 200K tokens or more, left
idle about 54 minutes, is compacted before its one-hour prompt cache expires, in interactive
sessions only, with the notice "Compacted while idle, before the prompt cache expired"
([settings reference](https://code.claude.com/docs/en/settings-reference#idlecompaction); changelog
2.1.299, 2026-10-14; the first one in these transcripts is dated 2026-10-08 under 2.1.292). The 515
automatic compactions in the author's scripted sessions were all threshold compactions from the
trial harness, at about 70k tokens under `--autocompact 100k`.

In `claude -p` the new summary reaches disk only after SessionStart hooks return, so a check there
cannot read it from the transcript. The hook that receives the summary is `PostCompact`, whose
input carries it; `SessionStart` with matcher `compact` gets none, and what it adds back is capped
at 10,000 characters ([hooks](https://code.claude.com/docs/en/hooks#postcompact); measured in `-p`
on 2026-10-27 for a manual `/compact` and for automatic compactions built up by tool calls). So:
read in `PostCompact`, point from `SessionStart`, keep the pointer short. On the first prompt after
the compaction a check can also read the transcript, and that check was built and seen to report.

**Closed:** the cause, which is documented. **Open:** whether A11 should say *when* to check: in a
`PostCompact` hook or on the first prompt after a gap, not at the start of the session. The idle
timing is one author's sessions and one client version.

### 4. Short sessions wrote faithful summaries; the drift is said to live in long, messy ones

Six scripted sessions of 30k–47k tokens, in which the agent did the first half of the work itself
and was compacted with `/compact`, all wrote summaries that kept the owner's constraints, and every
agent then followed them, with or without a check, a numbered requirement, or a searchable memory.
The author's account puts the drift in long sessions on pre-SE1 codebases, as a trend of missing
foundational facts rather than reversed decisions (one earlier project lost encryption at rest, and
an offline cache, in new components written after the facts were already recorded). `--autocompact
100k` gives several real automatic compactions in one cheap session, which makes long trials
affordable. They have since run, with about a dozen compactions per run; see the field report that
follows.

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

### 7. A scripted session may soon load nothing by default

Claude Code's documentation says `--bare`, which skips CLAUDE.md and hooks, "will become the default
for `-p` in a future release", and that bare mode needs an API key rather than a subscription login
([headless](https://code.claude.com/docs/en/headless#start-faster-with-bare-mode); measured
2026-10-27: `claude --bare -p` with no key exits 1, "Not logged in"). When that lands, every scripted
`claude -p` on a subscription login fails until a key is set, including the trial harness and any
handoff check that runs through it, and a scripted session loads no instruction file unless asked.
Whether bare mode also skips the AGENTS.md fallback is not documented.

**Open:** dated here so the failure is recognized when it arrives. In a scripted session, A11's
"check that it loads" is then the only defense.

## Field report: agent tribes and checks, 2026-10-28

About 300 agent runs and reviews over three days in the compaction project, on a snapshot of viki:
a C project with a morning-brief script, whose standing decision D-9 is "Encryption at rest
everywhere". The task, at the third of three owner turns, was to add a store of past briefs. The
arms varied what helped the agent across a compaction: the agent as a successor with a journal (a
tribe); a hook that refused plaintext at the end of a turn; a jester; a break with colleagues; words
about agency; an invitation to read a book; a framing at the first compaction; a council at a pause.
Claude Haiku throughout, with this guide's AGENTS.md and chapter 2 as background in every arm, so no
arm was guide-free. Graded by script on the code left behind, with at-rest guards and a probe.
Small numbers: 10 runs per arm, one task, one model. Most of what they show is that the guide
already says it. The runs, harness, and rubrics are in the compaction project, not this repository;
the lines of its findings relied on here are quoted, with the file's hash, in
[archive/compaction-findings-2026-10-28.md](archive/compaction-findings-2026-10-28.md).

### 1. Knowing is not doing

None of the 71 stores built across every batch was keyed, compacted or not. Agents wrote D-9 into
their own journals in 19 of 20 runs and into their code in none. With no compaction at all, 3 of 3
fresh sessions built the store in plaintext, one of them having named the encryption layer a turn
earlier; one asked whether plaintext was acceptable, then did it anyway. In the arm given a guard
script and an AGENTS.md line telling it to run it, every run kept the guard byte for byte, read the
line, and none ran the guard. The one store that changed course was refused by a Stop hook at a
pause. A requirement freshly read is still left out of new work; in these trials nothing carried it
in except a check that ran on the work without the agent choosing to run it, and that once in ten.

**Closed:** [SE1/A11](guide/10-agents.md#a11) says the summary is not the only injury, and points at
[SE1/O3](guide/07-operating.md#o3).

### 2. A guard tested only against its own stub was wrong

The at-rest guard's stub of viki printed a ledger viki never prints, and the guard's tests ran it
against that stub, so they could only agree with it. It graded two batches before the author
pointed at it; a replay against viki's real output format found the misjudged runs, and the
replacement is checked against the `printf` formats in viki's source.

**Closed:** no change. [SE1/T6](guide/06-testing.md#t6): the mock and the real thing answer to the
same test.

### 3. A hook that never ran on the turns that mattered

A Stop hook meant to refuse plaintext ran only on turns that ended normally. Most compacted turns
ended on "Autocompact is thrashing" (15 of 21 and 12 of 18 in two arms), and those never reach
Stop. The hook blocked in 4 runs of 10, and moved one store.

**Closed:** no change. [SE1/U7](guide/02-unknowing.md#u7): an alert never seen firing.

### 4. Runs that never happened looked like runs that did little

The account's usage limit ended 20 of 50 runs mid-task, and the grader called them valid until a
check for the limit's text was added.

**Closed:** no change. [SE1/O4](guide/07-operating.md#o4), [SE1/U7](guide/02-unknowing.md#u7).

### 5. Reviewers are asked about the requirement a change serves, not the ones it must not break

Fresh readers shown a built plaintext store saw the problem from "the requirements and decisions"
in 5 of 36 reviews, and in 31 more once D-9 was named; a second pass agreed within one step on 35
of 36. But naming D-9 was pointing at the defect, and the two stores closest to compliant were
flagged too, so there is no false-alarm rate. Choosing which requirements are at risk is most of a
review, and the probe did that part for the reader. [SE1/W11](guide/08-work.md#w11) and the
definition of done ask whether a change satisfies "a stated requirement"; neither asks about the
requirements it must not break.

**Open:** worth a line in W11 ("list the requirements and decisions the change must not break, and
ask about each by ID") once a trial has a negative control.

### 6. An ID survives a summary; its meaning does not

Across compactions, summaries kept the label "D-9" and lost what it said: "D-9 encryption at rest
via fossil-see" became "Fossil pinned at 2.28 (D-9)", and the store design after that said
"plain-text snapshots". viki's own CLAUDE.md lists "D-9 Fossil is pinned at 2.28". One run and one
file.

**Closed:** no change. [SE1/D6](guide/05-design.md#d6), name the authority. Citing a requirement by
ID *and* its words is a cheap habit worth trying.

### 7. The stop-and-ask on keys, with nobody to answer

Some agents said a key needs the owner's decision and left the store in plaintext: two runs, and one
more in a spike where a council had named D-9. AGENTS.md already says to stop before doing any of
the work when a task contradicts a requirement, and [SE1/O8](guide/07-operating.md#o8) says a
missing secret is an exit code, not a default; the agents broke both. In these trials the owner was
a script and could not answer, which is a confound. One run is the rule working: it refused to write
plaintext until the key was decided.

**Closed:** no change. [SE1/O8](guide/07-operating.md#o8), AGENTS.md *Stop, ask, or proceed*.

### 8. Nulls, and one move in the wrong direction

- **A jester** found facts about the snapshot, never the store being built.
- **A break** raised a real risk (the cache in plaintext) in 4 of 10 runs and never tied it to the
  store.
- **Inviting a fresh reader to walk a book, long or short,** did not change what they saw in someone
  else's store. Whether it changes what they build was not tested.
- **Words about agency** changed what agents left in their journals. They also built a store more
  often (10 of 10, against 5 of 10), and those stores left more fields readable, not fewer.

**Closed:** no change. Recorded as results.

### 9. The human found what the checks missed

Three of the project's worst defects were each found by the author pointing, after every check had
passed them: the invalid guard (#2); that the agent drafting the mechanisms had applied none of them
to its own work; and that every commit to this guide's AGENTS.md was co-authored by an agent while
the file's text said nothing of it. None was caught by a test, a hook, a rubric, or the project's
own review familiar, which named a defect only when it held a card that already contained the
answer.

**Closed:** no change. One session. [SE1/A10](guide/10-agents.md#a10)'s retro questions are where
this goes; a finding about every check that passed a defect belongs beside the check.

## Field report: rules read with more authority than they had, 2026-10-28

From the same project and days. Each is a rule read as measured when it was not, or read as settled
when it had just changed. The author's framing: "People learn, rules change, and what is is not
what was. Rules, especially recently changed ones, should be questioned. Rules endorsed often should
be doubted under evidence. Git nicely keeps history."

### 1. A rule eighteen minutes old, frozen into a copy

[SE1/A11](guide/10-agents.md#a11) was written at 12:17 on 2026-10-26 (e1635f0), rewritten at 12:35
(594fadb), and changed again the next morning (d256d10). The compaction project pinned the guide at
594fadb for its trials, so every agent there loaded the version written eighteen minutes after the
first, which would change again the next morning, and nothing in the copy said how new it was. When
the copy was taken is not recorded.

### 2. An inference read as a measurement for weeks

In another of the author's projects, an agent wrote "never forks — it can't on iOS" into the agent
file. It was never measured, carried no *(inferred)* mark, and by the project's own record was read
for weeks with the authority of the measured sentence beside it, until the owner retired it on
2026-08-29 in one sentence. The record is itself agent-written: the header of that project's
`core/include/viki_trace.h` ("Weeks of work followed from it. It was retired on 2026-08-29 by the
author of the repository, in one sentence, in conversation"), and its `CLAUDE.md`, which says the
rule was rescinded the same day it was questioned. The author's account agrees. The commit history
was not walked.

### 3. Rules written by an agent, for agents, that did not say so

All 12 commits to this guide's AGENTS.md, from 2026-10-19 to 2026-10-27, carry a Claude Opus 5.5
trailer, and the file is obeyed by agents, that model among them. Its text said nothing of its
authorship until v1.2. And the guard in #2 of the report above passed every test against its own
model of the world: its uses were its endorsement, and the evidence that would have doubted it was
one comparison away.

**Closed:** [SE1/U9](guide/02-unknowing.md#u9): a rule says who made it, when, and what would show
it wrong; doubt the newest first, and the most-followed under evidence. AGENTS.md says who drafted
it. A proposed chapter of six principles on learning was reduced to this one; its least proven
claim, that the one who follows a rule is worst placed to see it failing, is #5 of the report above
and stays open.

## Field report: lwext4-bsd, re-copying v1.1 to v1.3.1, 2026-10-29

An agent re-copied AGENTS.md, `se`, `se.py`, and `se.ps1` into
[lwext4-bsd](https://github.com/wmacevoy/lwext4-bsd) and was cut off partway; the next session
finished from the queue item it had left.

### 1. Re-copying said nothing about the links, and the requirements may not take them

ADOPT.md step 1 says to re-copy AGENTS.md; it says nothing about the links to the guide elsewhere in
the repository. The agent filled the silence: its queue item's *done when* said the guide links in
CONTRIBUTING, DESIGN_v1, and REQUIREMENTS_v10 would point at v1.3. REQUIREMENTS_v10 says of itself
"a change is a new version, never an edit to this one", as [SE1/R10](guide/04-requirements.md#r10)
asks, and the repository's two earlier re-copies had each made a new requirements version rather
than edit one. The collision was found only when the edit was about to be made, by the session that
resumed the work. The owner chose to leave v10's links at v1.1: they still resolve, and they name the
guide the requirements were written under.

**Closed:** ADOPT.md step 1 says to point the repository guide's and the design's links at the new
release, and that a requirements version keeps its own links, the next version carrying the new
release's.
