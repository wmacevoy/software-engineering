# Review: the guide at v1.1, with the v1.2 candidate

Reviewer: Claude Fable 5.1. Date: 2026-10-27.
Reviewed: tag `v1.1` (896661e) as released, plus the unreleased v1.2 work on branch
`v1.2/after-a-gap` at d256d10 (A11, AGENTS.md *After a gap*, the checker's tag comparison, and
two GAPS field reports). `main` is at de81f7c (v1.1 plus the empty v1.2 changelog section).

Status: complete; all three delegated checks are in, plus two rounds of measurements in the
compaction project (CC4 to CC7). Everything below was observed unless it says *inferred*.

## Verdict

The guide is sound. I found no principle that is wrong, and the evidence discipline (GAPS records
nulls, confounds, and the contamination of its own controls) is the best thing in it and rare.
Four small things should change before v1.2 is tagged; none is large. The largest content issue is
that A3 is contradicted by the guide's own field report. Two factual claims in the body are wrong
(W7's experiment, W2's "two pages later"). The Claude Code behavior behind A11 is consistent with
the documentation, which names the mechanisms the guide left as inferred and the hook it should
have used. AGENTS.md's main weakness is that it assumes a repository that already has a working
set, which most adopting repositories do not; the ADOPT.md draft (CT9) is the proposed answer.

## What I did

- **Read:** all ten chapters, README, AGENTS.md, CHECKLISTS, GLOSSARY, READING, GAPS, CHANGELOG,
  llms.txt, `_config.yml`, the CI workflow, the five templates, `tools/check.js`, and the diff
  `v1.1..HEAD`.
- **Ran:** `node tools/check.js` on the branch (22 files, 98 principles, 0 problems). Then, in a
  scratch copy, six planted breakages: a broken anchor, a reworded principle with no marker, A11
  dropped from the README index, the "wording only: A10" changelog line removed, an unversioned
  bare citation, and a wrong self-label in AGENTS.md. The checker went red on all six (SE1/T3).
  `curl` on all 59 external URLs in the repository. The GitHub API for the last CI runs and for the
  action versions the workflow pins. The live Pages site for principle anchors and numeric-leading
  heading anchors.
- **Delegated:** (1) a fact-check of 17 cited sources and numbers, with the sources opened (in;
  see *Claims checked against their sources*); (2) a documentation check of the Claude Code claims
  behind A11: import rules, whether AGENTS.md is loaded natively, compaction triggers, hooks (in;
  see *The Claude Code facts behind A11*), followed at the author's request by measurements on the
  author's own transcripts and in scratch `-p` sessions, written up in
  `~/projects/compaction/CLAUDE-CODE-DOCS-2026-10-27.md`; (3) an adversarial read of AGENTS.md as
  an agent in a strange repository (in); (4) at the author's request, a draft of `ADOPT.md` (in; see
  CT9).
- **Did not do:** no trap-task trial of AGENTS.md. Every subagent I can start inherits this
  repository's AGENTS.md, so there is no guide-free control; GAPS already records that confound.
  I did not open the compaction project outside this repository, so claims sourced there are
  taken as stated.

## Before tagging v1.2

**BT1. AGENTS.md cites `SE1/A11` while saying it is from v1.1 and linking a tag that has no A11.**
Line 68 cites `(SE1/A11)`; `git show v1.1:README.md` lists no A11; the checker reports 0 problems.
Today `main` has no A11, so no live reader is affected. The moment this branch merges before a
tag, every copy of AGENTS.md made from `main` (which is what llms.txt points agents at) is ahead
of its label and says nothing, the opposite of the CHANGELOG's promise that "a copy that is behind
says so" (SE1/U7). Recommendation: tag v1.2 in the same push as the merge, and extend
`tools/check.js` so that every ID cited in AGENTS.md and the templates must exist in README's
index at the tag they name (`git show <tag>:README.md`). I did not write that check.

**BT2. The CHANGELOG line "Wording only: A10 ... its text is unchanged" is a checker artifact.**
`bodies()` in `tools/check.js` ends a principle's text only at the next heading, so the `---` rule
after a chapter's last principle is counted as part of that principle. Inserting A11 moved the
rule out of A10's body. I ran `bodies()` on v1.1 and HEAD: A10 differs by exactly ` ---`. With the
changelog line removed, the checker reports "unacknowledged A10 changed since v1.1". A changelog
that lists non-changes is the dashboard that goes red every night (SE1/O4). Recommendation: in
`bodies()`, end a body at a line that is only `---`, then delete the changelog line.

**BT3. A11's third bullet conditions the rule on a check the same paragraph calls a K3 factory.**
"Until the check passes, the summary is recalled, not observed" implies a passing check makes it
observed; the paragraph above says the check passed 28 of 29 real compactions where harm occurred.
AGENTS.md *After a gap* states the rule unconditionally and is right. Recommendation: drop "Until
the check passes": the summary is recalled, not observed, whether or not a check passed; where it
and the source disagree, the source wins.

**BT4. Chores at tag time.** GAPS follow-up items 1 and 2 say "Proposed: ... (in this draft)";
after the tag, "this draft" has no referent; make them Closed or Open. A11 says the 29 compactions
are ones "where harm happened"; GAPS says "in many of them". A11 says "None of them opened the
transcript"; GAPS #6 does not say that, and its source is trial data outside this repository
(SE1/D13). Add the sentence to GAPS #6 or drop it from A11.

## Content

**CT1. A3's "The client never talks to the agent" is contradicted by the guide's own field report.**
GAPS agent trials #1: with the owner reachable, 5 of 6 authors stopped and asked; a question pass
drew every non-default policy point out of the owner in 9 of 9 runs, and the authors built on those
answers passed every hidden test. AGENTS.md's *Stop, ask, or proceed* presumes the agent can ask.
The intent is the channel (what the client said reaches the code through the requirements), not a
ban on asking. Recommendation, marked *Changed in v1.2*: "The client's answers reach the code only
through the requirements. An agent may ask; what it is told is written down before anything is
built on it."

**CT2. A3 and A4 assume no memory between sessions; some tools now give an agent one.** This
session has a private memory that persists across sessions. The guide's answer is already right
(SE1/U6, SE1/W10, SE1/A10: the repository is the memory), but it should say so: a private agent
memory is a head, not the working set. It is not observable by the team, not versioned, and not
read by the next tool or the next person, so a decision that lives only there is the U6 failure at
a new address. One sentence in A3 or A10. Raised once.

**CT3. AGENTS.md has no answer for a repository with no working set yet.** This is the top item of
the adversarial audit and my own reading. "Find the requirement ... If it traces to none ... say so
and ask" makes every non-chore task a stop in a just-adopting repository; "Search `Non-goals` and
`Scope decisions`" runs against headings that do not exist; "Name the requirement in the test" has
nothing lawful to cite. The guide's answer is SE1/W12, which AGENTS.md never cites.
Recommendation: one short paragraph under *Before you start*: if the repository has no
requirements document, that absence is the first finding; say so once, treat the task's own text as
the requirement for this task only, marked *(inferred)*, and propose the W12 reconstruction. Do not
invent a requirement to satisfy this rule, and do not stop on every task.

**CT4. R10 is absolute where the guide allows itself an exception.** The guide permits wording-only
changes to a principle within a major version, with a marker or a changelog line. Requirements get
no such allowance: a typo fixed in `REQUIREMENTS_v2` is, read literally, a v3. Recommendation: one
sentence in R10: a change in meaning is a new version; a wording fix is an edit, named in the
commit, the rule the guide applies to itself.

**CT5. GAPS.md links a repository the public cannot open.** `github.com/wmacevoy/lwext4-bsd` returns
404 anonymously; the local clone's remote shows the repository exists, so it is private. A reader
cannot check the first field report's claims (SE1/D13). Mark the link "(private)" or remove it.

**CT6. A vocabulary collision in GAPS.** Agent trials #3 is titled "Locality of reasoning" but
tests a rule copied into every module. D10's term means using a part correctly without reading
inside it. One word, one thing (SE1/D9). Rename the entry, for example "A rule copied into every
module".

**CT7. A11 carries its trial numbers inline.** U7 and T3 state the claim and leave the evidence to
GAPS; A11 has "4 of 4", "1 of 4", "29", and "4 messages" in the principle. The numbers are four
runs per arm, one model, one task, and will change when the trial is rerun, which will then require
editing A11 and marking it changed. Recommendation: one sentence of evidence and the GAPS link in
A11; the numbers stay in GAPS. The author chose to put what was measured in the principle; this is
a preference, not an error, and I raise it once.

**CT8. Proposed addition to U7's list of K3 factories: torn work.** (Raised by the author during
this review; the wording below is a draft for the guide.) A *torn write* leaves bytes that are
neither the old value nor the new; R7's interruption rule already demands "the old version or the
new one, never a mix" for data. Torn work is the same tear in the work itself: a change interrupted
between started and done. What is left (a working tree, a branch, a queue row, a summary) reads as
the current state, is neither the state before nor the state after, and nothing says so. The
half-applied refactor compiles; the test that was about to be written is absent, not red; the
queue row still says *in progress*; the summary says *done*. The next reader carries on from it
fluently: the same developer tomorrow, a teammate, an agent in a new session, or a second agent
that did not know the first was there. It keeps saying "fine" with no way to say "wrong".

It used to be rare, and had a story attached (a developer called to the hospital). Now it is
routine and has none: a dropped connection, an over-busy server, a closed laptop, a compacted
context (SE1/A11), and agents unknowingly working on the same project at once.

Draft bullet for U7, in the list's voice (the link is written from the repository root here; in
the chapter it is `04-requirements.md#r7`):

> - **Torn work.** A change interrupted between started and done: a dropped connection, a closed
>   laptop, a busy server, a compacted context, a second agent on the same project. What is left
>   reads as the current state, is neither the old one nor the new, and nothing says so: the
>   interruption rule of [SE1/R7](../../guide/04-requirements.md#r7), applied to the work instead of the data.

The cures are the three U7 already names, made concrete, so they could sit in the bullet or in the
chapters they belong to:

- **Small work.** A change small enough to finish in one sitting has no middle to be torn in; one
  concern per change (SE1/W11).
- **A branch, and commit the tear.** Work on a branch, never on the always-releasable one
  (SE1/W7); when interrupted, a work-in-progress commit or a stash whose message says *torn here*
  makes the tear visible. An uncommitted working tree is a tear with no label.
- **Work where the session survives you:** on a remote machine under `tmux` or the equivalent, so
  a dropped connection or a closed laptop kills neither the process nor the transcript.
- **One queue row per worker, with a *since*** (SE1/W10, SE1/H4), and one branch or worktree per
  agent, so two agents on the same project see each other before they collide. A row that says
  *in progress since 10:40 today* is a reason to ask, not to start.
- **Write the failing test first** (SE1/T8, SE1/R11): committed before the change, it makes a
  tear red instead of silent.
- **On resuming, treat what you find as torn until shown otherwise:** the diff, `git status`, and
  the queue row, before the summary (SE1/A11).

If adopted: U7 gets *Changed in v1.2* and a CHANGELOG entry under *Changed*; GLOSSARY gains
*Torn work*; the *Handing a task to an agent* checklist could gain "each agent has its own branch
or worktree, and a queue row". Evidence status: the author's field account, not a trial, which is
the same footing as U7's existing bullets. Vocabulary: see CT11; the word for what lessens a
factory should be *medicine*, not *cure*.

**CT9. ADOPT.md, drafted at the author's request, answers CT3 and the audit's top items.** The
draft is at `ADOPT.md` (135 lines, untracked, written by a delegated agent from this review's
findings; the checker passes with it in the tree: 24 files, 98 principles, 0 problems). I read all
of it. It has an owner's section (eight ordered steps: copy AGENTS.md at its release; make it load
at every start, with a tool-agnostic phrase test and a dated Claude Code note from CC1 to CC7; the
repository guide; `docs/` rebuilt by W12 with *(inferred)*; a table mapping AGENTS.md's nouns to
the repository; the proxy client; done and CI; the handoff check), an agent's section with one rule
per missing thing (no requirements, no queue, no check command, no `Non-goals`, no glossary, no
handoff check, AGENTS.md not loaded), and an adoption checklist in CHECKLISTS.md's style. It closes
CT3, gives the audit's undefined nouns a home (the table), and is where the owner-addressed
paragraph in AGENTS.md belongs. Recommendation: adopt it for v1.2 with three edits:

- Step 2 says `--bare` "skips instruction files"; CC7 documents CLAUDE.md and hooks, and whether it
  also skips the AGENTS.md fallback is not documented. Say that.
- Step 2's phrase test must forbid opening files: an agent asked to quote a line of AGENTS.md can
  open the file and quote it whether or not it was loaded. Say "without opening any file; an agent
  that opens the file to answer did not have it loaded."
- Step 2 carries "4 of 4 runs" inline; by CT7 the number belongs in GAPS, and the clause drops
  cleanly.

The pointer for AGENTS.md, in the absolute form it uses, proposed by the drafting agent and
endorsed: in the header, after the sentence about the repository's own guide, "How to adopt this
file, and what an agent should do where the adoption is only partly done, is in the guide's
ADOPT.md" with the link; and under *Before you start*, "If the repository has no requirements
document, queue, check command, or `Non-goals`, follow *For the agent* in ADOPT.md: say so once,
and do not stop on every task." The link must name the v1.2 tag, which the checker rejects until
v1.2 is dated and GitHub rejects until it is pushed: the same tag-time move as BT1.

Wiring when adopted (none of it done): the README reference table and its "Teams adopting it"
paragraph, which currently does ADOPT.md's job in two lines; llms.txt; a `_config.yml` nav entry
(siblings use one-word titles, so "Adopt"); CHECKLISTS.md, which says "every checklist in the
guide" and should point at or copy the adoption checklist; CHANGELOG *Also changed* under v1.2;
and the AGENTS.md pointer above. One retro line from the drafting agent worth keeping: README's
*Changing this guide* could say that links to a release tag are checked against the working tree,
not the tag.

**CT10. Proposed for chapter 2: whitespace, because an agenda finds only what it looks for.**
(Raised by the author during this review; the wording below is a draft for the guide.) An agenda
is a search: it moves K1 to K0, question in, answer out. K2 is what nobody is asking about, so a
calendar with no empty space and a queue that always has a next item leave the surprise only one
place to arrive: reality, at full price ([SE1/U2](../../guide/02-unknowing.md#u2)). People say they are
thinking of quitting at the bar, not at stand-up; stand-up has a format (done, next, blocked) and
quitting is not on it. An agent given only tasks never looks around: it does not notice last
week's half-finished change (CT8), the dependency whose advisory landed on Tuesday, or the
assumption that came due when the world moved ([SE1/U4](../../guide/02-unknowing.md#u4)). Everything it
is not pointed at reads as fine ([SE1/U7](../../guide/02-unknowing.md#u7)).

Two places it could go. The smaller: a clause in U2's K2 row ("and time with no agenda, in which
the only question is what nobody has asked about"). The larger, which I recommend because it
applies to people and agents alike and retires a fear of its own, is a principle:

> ### U8. Leave whitespace: an agenda finds only what it looks for
>
> An agenda is a search. It moves K1 to K0: you ask the question, you get the answer. K2 is what
> nobody is asking about, so a calendar with no empty space and a queue that always has a next
> item guarantee that the surprise arrives in the only place left, reality, at full price
> ([SE1/U2](../../guide/02-unknowing.md#u2)). People say they are thinking of quitting at the bar, not at
> stand-up; stand-up has a format, and quitting is not on it. An agent given only tasks never looks
> around: it does not notice the half-finished change from last week, the dependency whose advisory
> landed on Tuesday, or the assumption that came due when the world moved
> ([SE1/U4](../../guide/02-unknowing.md#u4)). Everything it is not pointed at reads as fine
> ([SE1/U7](../../guide/02-unknowing.md#u7)).
>
> Whitespace is time with no agenda, spent on purpose. For people it is the walk, the lunch, the
> end of the retro after the list is done, and the only question is "what is wrong that nobody has
> asked about?" For an agent it is a session with no task: read the repository and what changed in
> the world since the last session, and report what moved, what is torn, and what has gone stale.
> What it finds goes in `FINDINGS` or the queue, not into code. Slack
> ([SE1/W7](../../guide/08-work.md#w7)) is the capacity to absorb a surprise; whitespace is the attention
> that notices it first.
>
> **Ask:** "When did someone last look at this with no task in hand, and what did they find?"

The fear it retires ([SE1/P4](../../guide/01-purpose.md#p4)): "we will learn what nobody asked about at
the exit interview, or in production." Two mechanics if adopted: the *Every iteration* checklist
could gain a habit line ("an hour with no agenda; what was noticed went into FINDINGS"), and for
agents a scheduled task-less session is a mechanism most agent tools now offer, which the guide
should name only by shape ([SE1/A10](../../guide/10-agents.md#a10)). If adopted, U8 is *New in v1.2*
with a CHANGELOG entry under *New*, a README index line, and the chapter's intro sentence ("five
kinds of not-knowing") stays true. Evidence status: the author's field observation, the same
footing as CT8. Vocabulary: *medicine*, per CT11. In the
chapter the links would be `#u2`, `#u4`, `#u7`, `08-work.md#w7`, `01-purpose.md#p4`.

**CT11. Say *medicine*, not *cure*.** The author's position, raised during this review: a K3
factory and the unknown unknown cannot be fixed, only lessened, and *cure* promises the fix. The
guide already speaks this way elsewhere: P1 says engineers *manage* discomfort, and U2 says every
practice *moves* a category toward K0, not that it empties it. *Medicine* is taken for a condition
you live with; it fits. Three occurrences:

- `guide/02-unknowing.md`, U7: "Three cures, each the opposite of what makes a factory" becomes
  "Three medicines, each the opposite of what makes a factory".
- `guide/04-requirements.md`, R8: "The usual cure for K2, exposure to reality" becomes "The usual
  medicine for K2, exposure to reality".
- `CHANGELOG.md`, the v1.1 entry for U7 ("eight common ones, and three cures"): a record of what
  v1.1 said; leave it.

Both guide edits are wording only, so each needs a line under v1.2 *Also changed* or the checker
will report the principle as unacknowledged. One word, one thing ([SE1/D9](../../guide/05-design.md#d9)):
if *medicine* is the word, CT8's torn-work bullet and CT10's whitespace draft should use it, and a
GLOSSARY line could pin it: "Medicine: a practice that lessens the cost of a kind of not-knowing;
nothing here cures one."

## Claims checked against their sources

A delegated check opened each source (paper, page, or API record) rather than a search snippet,
and said which it did. GAPS currently says of its related-work numbers "the papers themselves were
not opened"; they now have been, and the paragraph can say so with the corrected wording below.

**SR1. W7 misdescribes the experiment, and does not name it.** It is Brown (1948), "Gradients of
approach and avoidance responses and their relation to level of motivation", J. Comp. Physiol.
Psychol. 41(6), read through Miller's 1944 account of the same data (the 1948 paper itself is
paywalled; that step is a secondary source). What the guide gets wrong: the rat was not "drawn
toward" the shock end; it ran away and was briefly held back by a harness. Pull was measured at
two points, near and far, with different rats at each, not "along the way". It was an alley, not a
cage. "Nearly flat far from the danger and rises steeply close to it" is a curve two points cannot
show; the finding is that pull was far stronger near than far, and rose with nearness faster than
the pull toward food did. The guide's conclusion (the last week is the steep part) survives;
the description does not. Suggested text: "In a classic experiment, rats shocked at one end of an
alley were briefly held back by a light harness while running away, some near the shock point and
some far from it, and the force of their pull was measured. Pull was far stronger near the danger
than far from it, and rose with nearness faster than the pull toward food did: an avoidance
gradient (Brown, 1948)." Mark W7 *Changed in v1.2* and add Brown to READING.md.

**SR2. W2's "two pages later" is wrong.** In Royce (1970), the waterfall is Figure 2 at the top of
the page, and the next sentence under the caption is "I believe in this concept, but the
implementation described above is risky and invites failure." The quoted words are exact; the
placement is the same page, directly beneath the drawing, which makes the guide's point better
than "two pages later" does. Suggested: "and, in the sentence directly beneath the drawing, wrote
that the implementation as drawn 'is risky and invites failure'".

**SR3. GAPS: "Williams et al. (2000) reported about 15% fewer defects for about 15% more effort"
is a paraphrase, not the paper.** The IEEE Software paper reports pass rates on test cases
(individuals 73 to 78%, pairs 86 to 94%) and that the extra programmer-hours fell from 60% to a
minimum of about 15% after an adjustment period. "15% fewer defects for 15% more time" is
Cockburn and Williams's restatement in "The Costs and Benefits of Pair Programming" (2000), and
Erdogmus and Williams (2003) note the effort difference was not statistically significant.
Suggested: cite Cockburn and Williams for the 15/15 sentence, or state the pass rates.

**SR4. GAPS: "interaction raised resolve rates by up to 74%" is a relative gain for one model.**
Ambig-SWE's figure 3: Claude Haiku 3.5 went from 15.4% to 26.8% resolved (74% relative, 11
points); Claude Sonnet 4 from 40.0% to 61.4%. The paper's text does not say relative or absolute.
Suggested: "by up to 74% relative to the non-interactive setting (15.4% to 26.8% for the model
with the largest gain)".

**SR5. GAPS: the Claude Code best-practices page does not say "planning before coding".** It says
to brainstorm and write a spec first ("Interview me until you could write the spec, then write it
to SPEC.md ... start a fresh session to build from it"). The other two claims (a second session as
reviewer; a reviewer subagent that did not see the code written) are there verbatim. Suggested:
"recommends writing a spec before building".

**SR6. GAPS: the "90%" pair-programming claim.** No controlled study found, as GAPS says. The
nearest source is a single industrial self-report of "over 90%" fewer defects quoted in Erdogmus
and Williams (2003), and the Utah pairs passing 90% of acceptance tests against 75% for soloists.
Worth naming, since that is probably where the number comes from.

**SR7. Confirmed as written:** Conway 1968 in Datamation, four pages. Hannay et al. 2009 at that
DOI, with a small positive effect on quality and a medium negative effect on effort (the numeric
effect sizes could not be opened). HumanEvalComm: most responses to modified problems produced
code rather than questions (communication rates 5 to 38% by model). SWE-Bench Pro is Scale AI's;
trajectories are public on S3 (an AWS account is needed) and on Docent. `guidebook.md` at the root
of the ArduinoUnit repository is titled "The Zen of Testing". Cook has eighteen numbered points.
Brooks chapters 2, 3, 4, 7, and 16 are the ones named. Larman and Basili is IEEE Computer, June
2003, with incremental development dated to 1957. just-the-docs v0.10.1 exists (2025-01-06).
`actions/checkout@v7` and `actions/setup-node@v7` exist, and `fetch-depth: 0` fetches tags, so the
checker's tag comparison works in CI. The caret rule for 0.x is as stated for npm, and Cargo's
default is the same.

**SR8. Four of the sources are behind dead links, paywalls, or script-only pages** (Royce, the
Williams IEEE paper, Hannay, Brown). READING.md names sources without links. Recording a stable
copy where one exists (Royce at faculty.washington.edu, Williams in the Wayback copy of the NCSU
PDF, Miller 1944 on archive.org) would save the next checker the hunt (SE1/D13).

## The Claude Code facts behind A11

A delegated check read the Claude Code documentation and changelog as of 2026-10-27, quoting from
the raw pages, and labeled each answer documented, inferred, or not documented. What bears on the
guide:

**CC1. AGENTS.md loads by itself in Claude Code, unless a CLAUDE.md exists.** Documented
(https://code.claude.com/docs/en/memory#agents-md): since v2.1.277 (2026-09-18), in a project with
no CLAUDE.md at or above the working directory, Claude Code reads AGENTS.md as the project
instructions; adding a CLAUDE.md or CLAUDE.local.md switches that off by default. That is why
AGENTS.md was in my context in this repository, which has no CLAUDE.md. Consequence for A11's first
bullet and the owner paragraph in AGENTS.md: "import AGENTS.md from CLAUDE.md" is right, and
necessary, exactly when a CLAUDE.md exists; without one the import is not needed. Say both. It also
means a trial that adds a CLAUDE.md to test imports changes what is read.

**CC2. The failed import in GAPS #2 is the documented approval gate, not a silent bug.** Documented
(same page, *Import additional files*): an import whose path resolves outside the working directory
is "external" and needs a one-time approval shown in an interactive session; a `-p` session shows
no such dialog (https://code.claude.com/docs/en/headless), and the documented "instruction file not
loaded" notice does not cover an unapproved import. So `@../guide/AGENTS.md` and an absolute path
load nothing in `-p` and say nothing, as GAPS observed, and a copy inside the working directory is
not external and loads. Two corrections for the guide's wording: the boundary is the working
directory, not the repository (an import that climbs out of the subdirectory you started in is
external even inside the repository), and the gate predates 2.1.311 (the dialog is in the 2.1.6
changelog entry). Before attributing the measurement to the gate, rule out the documented controls
that also stop a file loading: `permissions.blockReadsOutsideWorkingDirectories`, a Read deny rule
covering the path, `claudeMdExcludes`, and `--bare`. Measured 2026-10-27: the author's user and
local settings set none of those keys, and neither repository has a settings file, so the approval
gate is the explanation left standing. Suggested for A11 and AGENTS.md: "an import that leaves the working directory needs an
approval that a `-p` session never shows, so it loads nothing and says nothing; keep the copy
inside, and import it from CLAUDE.md if you have one."

**CC3. "Check that it loads" has a documented check.** An `InstructionsLoaded` hook logs each
instruction file with its load reason: `include` for an import, `compact` for the reload after
compaction (https://code.claude.com/docs/en/hooks#instructionsloaded). It does not fire for an
AGENTS.md read through the fallback in CC1, so in Claude Code the checkable path is a CLAUDE.md that
imports AGENTS.md. Interactively, `/memory` and `/context` list what loaded.

**CC4. The idle compaction in GAPS follow-up #3 is documented, and the inferred cause is right.**
Changelog 2.1.299 (2026-10-14): a conversation of 200K or more tokens left idle for about 54
minutes is compacted before its one-hour prompt cache expires; the `idleCompaction` settings key is
documented from 2.1.290 (2026-10-05)
(https://code.claude.com/docs/en/settings-reference#idlecompaction). Conditions: an interactive
session (not `-p`), the one-hour cache TTL (a subscription within plan usage; an API key gets five
minutes unless configured), and a timer counted from the last request, not from the human's last
message. The terminal prints "Compacted while idle, before the prompt cache expired." GAPS can
close its "inferred, not read from documentation" note, and can tell which compactions were idle
ones by searching the transcripts for that line. GAPS dates the first one to 2026-10-08, between
the settings key and the changelog entry; worth a sentence. The `--autocompact 100k` trials proposed
in #4 would run the threshold path in `-p`, a different trigger from the one observed; fine, but
say so.

Measured on the author's transcripts (2026-10-27, counts and timestamps only): 25 compactions carry
the idle notice, at 54.3 to 55.3 idle minutes, with 204,828 to 683,674 tokens before compaction
(median 293,738). Split by session kind: interactive terminal sessions had 24 automatic
compactions from 2026-10-08 to 2026-10-27, every one idle, 204,828 to 683,674 tokens, median
292,404, and no threshold compaction at all; the other 515 automatic compactions are `-p` sessions
in scratch and temp folders at a median near 70,000 tokens, which is the trial harness at
`--autocompact 100k`. That reconciles with GAPS: two of the 24 are dated 2026-10-27, after GAPS was
written, leaving its 22; but one of those 22 (2026-10-21) is above 461k, so the stated range should
widen to about 684k, and "every automatic compaction" should say "in interactive sessions". One
loose end: the earliest idle notice (2026-10-08) sits in a transcript recorded as 2.1.292, before
the changelog's 2.1.299 entry; the feature shipped before its changelog line.

**CC5. The hook that receives the summary is PostCompact, not SessionStart.** Documented
(https://code.claude.com/docs/en/hooks#postcompact): PostCompact's input carries
`compact_summary`. SessionStart's input has no summary field, and its transcript path "may lag the
in-memory conversation", which is what GAPS #3 ran into in `-p`. SessionStart with matcher
`compact` fires on automatic and manual compaction and not on `--resume`, which has its own
matcher; that matches the author's observation. Its output is added to the compacted context, with
a documented cap of 10,000 characters on additional context, so "point, don't hand over" has a
ceiling. For the handoff check: read the summary in PostCompact, point from SessionStart, keep the
pointer short.

Measured in `-p` (Claude Code 2.1.311, scratch hooks that only log their input): a manual
`/compact` fired PreCompact, PostCompact with a 2,876-character `compact_summary`, and SessionStart
with source `compact` and no summary; `--resume` fired SessionStart with source `resume`. An
automatic compaction with `--autocompact 100000` did not complete in a first trial that fed two
large piped messages with no tool calls: PreCompact fired twice, nothing after; that cause is not
established. Retested with the context coming from tool output (six large reads): it compacted
twice at about 70k tokens with no hooks, with only a PostCompact hook (which received the summary
each time), and with only a PreCompact hook; a PreCompact hook exiting 2 blocked it, as documented.
So the `--autocompact 100k` trials GAPS #4 proposes are viable in `-p` when the context is built
by tool calls.

**CC6. The mechanism behind "put the rule where it is loaded at every start" is documented.** After
compaction the project-root CLAUDE.md and unscoped rules are re-injected from disk; nested files
and path-scoped rules reload on demand
(https://code.claude.com/docs/en/context-window#what-survives-compaction). Whether an AGENTS.md
read through the fallback is re-injected after compaction is not documented. Measured in `-p`: with
no CLAUDE.md, a unique line in AGENTS.md was known before `/compact`, and the first turn after it
carried an instructions attachment containing the line. The retest separates the mechanism from
recall: a control run with no compaction shows one instructions attachment, at session start only;
after `/compact` a new attachment appears after the compaction boundary, naming AGENTS.md, and when
a CLAUDE.md imports AGENTS.md it names both files. So the fallback is re-injected after compaction
too (measured, 2.1.311; the recall answer itself is not separable because the summary also held the
line). `omitClaudeMd` was not run; its test design is in the compaction file. A11 could cite the
mechanism in one clause; CC3's point about the import path being the checkable one stands.

**CC7. A forward risk for the trials and the advice.** The headless page says `--bare`, which skips
CLAUDE.md and hooks, "will become the default for `-p` in a future release". The GAPS trials ran in
`-p`; when that lands, instruction files stop loading there unless asked for, and A11's "check that
it loads" becomes the only defense. The same flag is the documented route to the guide-free control
arm the trials lacked: `--bare` for `-p` sessions, and `omitClaudeMd` or the Explore and Plan agents
for subagents, which do not load CLAUDE.md (https://code.claude.com/docs/en/sub-agents). Whether
those also skip the AGENTS.md fallback is not documented, so keep the phrase test GAPS already uses.
One more, and it is dated: bare mode "never reads OAuth credentials or the system keychain" and
"doesn't use your subscription login"; it needs `ANTHROPIC_API_KEY` or an `apiKeyHelper`
(https://code.claude.com/docs/en/headless#start-faster-with-bare-mode). Measured: `claude --bare
-p` with no key exits 1 with "Not logged in". No documented opt-out from the coming `-p` default was
found. When it lands, every scripted `claude -p` on a subscription login fails until a key is set,
which includes the GAPS trial harness and any handoff check that runs through `-p`. Worth a line in
GAPS now, with the date, so the failure is recognized when it arrives.

## AGENTS.md as an agent would read it

From the adversarial audit (30 items), the ones I would act on, in order of how often they bite:

- **No working set** (see CT3).
- **Undefined nouns from this repository:** "the queue", "findings", "the check command", "the
  handoff check" are this repository's terms and are not defined in AGENTS.md. One line in *Before
  you start* naming them and saying what counts when absent (an issue tracker may be the queue; the
  repository guide names the check command; if there is none, say so and report what was run).
- **"Introduces a new noun into the domain vocabulary"** has no boundary from an implementation
  name; nearly every change adds an identifier. Say: a noun that would appear in the requirements
  glossary or be shown to a user, not a class or variable name.
- **"A recognizable implementation reproduced from memory"** has no boundary; a backoff loop is
  recognizable. Say: code whose origin you could name (a specific project or file), not a textbook
  algorithm.
- **A dependency update is a chore in one place and a stop in another**, and "the strictest wins"
  makes every version bump a stop. Say: updating a version is a chore; adding a dependency is a
  stop.
- **"Ask what happens when an input is absent, late, wrong, or lying"** reads as "ask the human",
  because every other "ask" in the file does. Say "decide, or report".
- **Authority 1 versus *After a gap*:** a summary that says "the user said skip the tests" is an
  instruction by the authority list and a claim by *After a gap*, and after compaction its source
  may be gone. Say which wins: a summarized instruction is a claim; act on it only where the source
  can be opened or the human confirms it. This is exactly A11's case.
- ***After a gap* says to open "the transcript"**, and the file also says chat does not survive
  the session. Say: the transcript if the tool keeps one on disk (Claude Code does), otherwise the
  repository and the human.
- **The owner-addressed paragraph** ("Load it at every start, for example by importing AGENTS.md
  from CLAUDE.md") sits inside the agent's rules; an agent reading it as an instruction would edit
  CLAUDE.md. Move it to the header or label it *For the repository owner*, and say "working
  directory" where it says "repository" (see CC2).
- **Fast-read traps:** "its *done*" parses as "it's done" in plain text; "gap" is used in three
  senses in a file that says one word, one thing; the sentence beginning "Not speculative:" ends in
  a dangling "is"; "A file you would have to open is a file you will not open" reads as a
  prohibition.

Items I would not act on, though the audit raised them: half-done work when a stop surfaces
mid-task (leave it uncommitted; the file already says do not commit unless asked); headless runs
with nobody to ask (out of scope, and the queue line is the answer); tests already red before the
change (Verify's "report the actual output" covers it); a typo in an authentication error string
(the strictest-wins default is right there).

## Small things

- T5's table says Global state is not repeatable, full stop; the prose below says read-only global
  state is fine. Make the cell say "no, if written".
- `.gitignore` is a 250-line Python template in a repository with no Python (SE1/D8, in the
  guide's own house). Replace it with the lines it uses.
- Twenty-four principles have no *Ask* line (mostly in Work, People, and Agents). README says
  "most end with a question", which is true. No action needed.
- llms.txt points agents at raw `main`, which during an unreleased window is ahead of every tag;
  same root as B1.
- Checked and fine: the reliability and availability arithmetic (SE1/P2, SE1/R7), the
  readings-per-year figure (SE1/D12), the D5 worked example and the D7 code, the W11 list against
  the CHECKLISTS copy, the twelve questions against their principles' *Ask* lines, CI green on
  `main`, every anchor the README and the chapters link to exists on the live site, including
  numeric-leading GAPS headings. A11's claims that a `compact` hook fires on manual compaction and
  not on `--resume` match the hooks documentation.

## What to keep

The fear-retired test (SE1/P4) as the organizing device for every practice. K0 through K4 with K3
as the enemy and *K3 factory* as a reusable noun. R6's four cases, reused for teammates (SE1/H2)
and agents. One running example carried through every chapter. A checker that enforces the guide's
own conventions, and that I watched go red. GAPS as a public ledger that records what did not work
and which of its own controls were contaminated.

## Retro (SE1/A10)

- **What I had to read that I should not have needed:** the checker's source, plus six mutation
  runs, to learn that an *Also changed* entry can be checker-driven. A comment at `bodies()` saying
  what counts as a principle's text would have said so.
- **What I assumed because nobody wrote it down:** what a review of this guide is and where it
  goes. The pre-v1 review survives only in three commit messages. If reviews are this repository's
  FINDINGS, say under *Changing this guide* whether they are committed and where. I also assumed
  the target was v1.1 plus this branch: the file name says v1.1, the checkout says v1.2.
