# Changelog

What changed between releases, by principle ID, newest first. A change you cannot spot is a K3
factory ([SE1/U7](guide/02-unknowing.md#u7)), so every change is visible in three places:

- **Here**, by ID, with a full diff link per release.
- **Under the principle's heading**, as *New in v1.1 (date).* or *Changed in v1.1 (date).* — the
  release that last changed its meaning, a person's claim — or, where none did, *Since v1.0 (date).*,
  git's answer: the release at which the principle's current text first appeared. When wording moved
  later without the meaning, the line adds *text since*. `tools/since.js` writes these from the tags
  and `--check` verifies them, so a principle that reads as unchanged says since when, and no marker
  can drift.
- **In every copy**: AGENTS.md and the templates link to the release they came from, so a copy that
  is behind says so.

`tools/check.js` keeps the three in step, and compares every principle with the last release tag:
one whose text changed must have a marker for a later release, or — for wording only — be named
under that release's *Also changed*. Work toward a release goes under `## v1.4 — unreleased`; give it
a date when you tag it. Within SE1, a minor release may add principles, reword them, or extend what
they ask; it never moves an ID ([principle index](README.md#principle-index)). A patch release
(`v1.2.1`) changes no principle, no AGENTS.md, and no template: copies keep the minor's label, and
the checker holds a patch to that.

**If you keep a copy** of AGENTS.md or the templates, read *For copies* in each release newer than
yours.

## v1.4 — unreleased

[Changes on main since v1.3.2](https://github.com/wmacevoy/software-engineering/compare/v1.3.2...main)

**A proposal, on the branch `proposal/learning-chapter`:** a chapter on learning, with U9 pointing to
it. The author has not decided between the chapter and U9 as it was; nothing here is released.

### New

- [SE1/L1](guide/11-learning.md#l1) Doubt in order: the newest rule, then the rule written for a
  world that has changed, then the most-followed under evidence. The order that was U9's third
  medicine, with its reasons.
- [SE1/L2](guide/11-learning.md#l2) Read a rule's history before you keep or change it; supersede
  with a reason, never edit silently. R10 extended to every rule; a record keeps the citation it was
  written with.
- [SE1/L3](guide/11-learning.md#l3) A finding that changes no rule, test, or check is a lesson not
  learned. The template's *Changed* line as a principle; untested, and says so.
- [SE1/L4](guide/11-learning.md#l4) The one who follows a rule is the worst placed to see it
  failing. One project, one model; the least proven, and says so.

### Changed

- [SE1/U9](guide/02-unknowing.md#u9) Keeps what a rule carries — who, when, what would show it
  wrong; an agent's rule says so — and points to Learning for the order in which to doubt and how to
  change a rule.

## v1.3.2 — 2026-10-29

[Full diff from v1.3.1](https://github.com/wmacevoy/software-engineering/compare/v1.3.1...v1.3.2). No
principle, AGENTS.md, or template changed; copies at v1.3 are current. No review by another family
for this patch: it changes no guide text.

**For copies:** nothing to re-copy. At your next re-copy, ADOPT.md step 1 now also says to point the
repository guide's and the design's links at the new release; a requirements version keeps the links
it was written with, and the next version links the new release (PR #2).

### Also changed

- `se` reads requirements kept in table rows (`| **FMT-1** | *(since v1)* ... |`), not only bullets;
  lwext4-bsd's thirty had counted as none (PR #1, queue #8).
- `se` reads C++, module JavaScript, and other common test files (`.cpp`, `.hpp`, `.mjs`, `.tsx`,
  `.cs`, `.kt`, `.swift`, and kin) when tracing requirements to tests and scanning citations; a C++
  test in oopc had read as untested (PR #3).
- The doctor's citations row treats a FINDINGS entry and a done queue row as history: they keep the
  citation they were written with and are not stale. A bare ID takes the version named before it on
  the same line (`REQ10/TOOL-1, RST-3`). An open row and a test still answer to the newest version.
  Decided from PR #1's question.
- With no CONTRIBUTING.md or CLAUDE.md, a README alone names no check command; the doctor no longer
  takes the first backticked thing on a line that mentions tests, which on one course repository was
  a workflow path. The row says *none yet* (queue #9).
- ADOPT.md step 1: re-copying also updates the guide links in the repository guide and the design;
  GAPS gains the lwext4-bsd field report behind it (PR #2).

## v1.3.1 — 2026-10-28

[Full diff from v1.3](https://github.com/wmacevoy/software-engineering/compare/v1.3...v1.3.1). No
principle, AGENTS.md, or template changed; copies at v1.3 are current. No review by another family
for this patch: it changes no guide text.

### Also changed

- `docs/`: this repository's own working set, which the doctor had rightly reported as "none
  yet": REQUIREMENTS_v1 and DESIGN_v1, read off the repository and marked *(inferred)*, the QUEUE,
  and FINDINGS; GAPS stays for the principles in the field.
- `CONTRIBUTING.md`: this repository's own guide, from its own template: run, check, reset, the
  release procedure, the rules, and where things are. `tools/since.js --as vX.Y` lets a release
  commit carry dated markers before its tag exists.
- Every principle carries a marker with a date, written by `tools/since.js` from the release tags:
  *Since v1.0 (2026-10-20).* for the ninety that no release changed, the date beside each
  *New/Changed in*, and *text since* where wording moved after the meaning did. CI runs
  `node tools/since.js --check`. The checker and the tool share `tools/bodies.js`.
- `se`: three defects the data-mining guide exposed, each seen red on a fixture (queue #1,
  `docs/FINDINGS.md`). The release label is found when it wraps across a line. SE1's copy is known
  by the line that names this guide's release, so a sibling guide's agreement, labeled with its own
  release, is reported as not SE1's instead of being compared with SE1's releases. A `docs/` in
  another guide's shape is named instead of being reported as if empty; `se` checks SE1's shape
  only.
- `se` reads the repository guide's check command from its *The full check* line, or the fenced
  block under it; the CI row requires every part of that command and compares the interpreter's
  name literally, since treating `python3` and `python` as one had hidden a second recipe.
  `tools/check.sh` is the one recipe contributors and CI run (SE1/O3).

## v1.3 — 2026-10-28

[Full diff from v1.2.1](https://github.com/wmacevoy/software-engineering/compare/v1.2.1...v1.3) ·
100 principles

**For copies:** re-copy AGENTS.md (*Before you start* no longer asserts that the self test ran),
`se.py`, and the templates, which now link to v1.3.

### Also changed

- From the first review by an agent of another family (Codex,
  `archive/reviews/REVIEW-v1.2.1-codex.md`): AGENTS.md says to look for the self test's report and
  run it if absent, instead of asserting it ran; `se --post` is a self test in
  [SE1/T2](guide/06-testing.md#t2)'s sense, refusing with an exit code when the disk is below its
  floor and reporting the risks it cannot refuse; its rules no longer tell an agent to commit,
  which AGENTS.md forbids unless asked; the doctor and the self test name Claude Code where a row
  describes its configuration, and keep observed loading (the phrase test) apart from it; the
  tests run on Python 3.9, which CI now exercises beside the newest; `se --self` checks the pin
  against the released AGENTS.md, so unreleased edits to it do not go red.
- The checker's patch-release rule holds only while the patch is the newest CHANGELOG section.
- README gains *Why to trust this, and why to doubt it*: U9 applied to the guide on its front page.
  `archive/reviews/REVIEW-METHOD-other-family.md` records how the Codex review was run, with the
  brief verbatim, so the next can be run the same way. U8 stays where it is: an ID moves only in
  SE2.

## v1.2.1 — 2026-10-28

[Full diff from v1.2](https://github.com/wmacevoy/software-engineering/compare/v1.2...v1.2.1). No
principle, AGENTS.md, or template changed; copies at v1.2 are current.

### Also changed

- The reviews behind v1.1 and v1.2 are kept in `archive/reviews/`; README says that is where
  reviews go.
- CI runs the checker, `se`, and its tests on Linux, macOS, and Windows; `.gitattributes` keeps
  line endings LF, and `se` hashes AGENTS.md with line endings ignored.
- The checker and `se` understand patch releases: the doctor calls a copy current when its text
  equals the newest release's AGENTS.md, whatever its label.

## v1.2 — 2026-10-28

[Full diff from v1.1](https://github.com/wmacevoy/software-engineering/compare/v1.1...v1.2) · 100
principles

**For copies:** re-copy AGENTS.md (new section *After a gap*, a header that says who drafted it, a
pointer to ADOPT.md, and wording from a review) and the templates, which now link to v1.2; copy
`se`, `se.ps1`, and `se.py` beside AGENTS.md and run `./se --doctor`. Make sure your agents load
AGENTS.md at every start from a copy inside the working directory, and check that it loaded;
ADOPT.md and the doctor say how. A copy that has to be opened is not read.

### New

- [SE1/A11](guide/10-agents.md#a11) A summary is a concussion: check it from outside. After
  compaction or any handoff the summary is recalled, not observed. Load the rule at every start, and
  check that it loads; run a handoff check that compares the summary with the record, and that can
  say *wrong*: the word-overlap check found a planted gap and passed nearly every real compaction.
  The summary is not the only injury: a requirement freshly read is still left out of new work; in
  trials, only a check that ran on the work without the agent choosing to run it moved a store, and
  that once.
- [SE1/U8](guide/02-unknowing.md#u8) Leave whitespace: an agenda finds only what it looks for. K2 is
  what nobody is asking about; time with no agenda, for people and for agents, is the attention that
  notices it first.
- [SE1/U9](guide/02-unknowing.md#u9) Rules change: a rule says who made it, when, and what would
  show it wrong. Doubt the newest rules first, the ones written for a world that has changed next,
  and the most-followed under evidence; a rule an agent wrote says so; git keeps the history.

### Changed

- [SE1/A3](guide/10-agents.md#a3) An agent may ask; the client's answers reach the code only through
  the requirements, written down before anything is built on them. A private memory an agent keeps
  between sessions is a head, not the working set.
- [SE1/U7](guide/02-unknowing.md#u7) The K3 factories gain *torn work*: a change interrupted between
  started and done, which reads as the current state and says nothing.
- [SE1/H4](guide/09-people.md#h4) The stand-up gains a fourth question, *do you notice discomfort?
  can you name it?*: P3 asked out loud. The vocabulary table in chapter 8 says the same.
- [SE1/W7](guide/08-work.md#w7) The avoidance-gradient experiment is described as Brown (1948) ran
  it: an alley, a harness, pull measured near and far. The conclusion is unchanged.

### Also changed

- AGENTS.md: new section *After a gap*. The agent hand-off checklist gains a line for it. The header
  says who drafted the file and when (SE1/U9): every commit to it was co-authored by an agent, and
  the text did not say so.
- Wording only: [SE1/R8](guide/04-requirements.md#r8) says *medicine* where it said *cure*, as does
  U7 (marked changed above): a K3 factory is lessened, not fixed. GLOSSARY pins the word.
- Wording only: [SE1/W2](guide/08-work.md#w2): Royce's warning is in the sentence directly beneath
  the drawing, not two pages later. READING adds Brown (1948).
- Wording only: [SE1/T5](guide/06-testing.md#t5)'s table says global state is unrepeatable *if
  written*, as its prose already said.
- GAPS.md: a field report from agent trials, including the compaction trials behind A11; a second,
  on compaction in the author's own sessions (the check on real compactions, imports from outside
  the working directory, when compaction happens, and what is still untested); and a third, on
  agent tribes and checks (knowing is not doing; a guard tested against its own stub; the human
  found what the checks missed).
- `se`, `se.ps1`, `se.py`: a command-line companion for repositories that follow the guide.
  `./se --doctor` is ADOPT.md's checklist made executable: the copy's release (checked against the
  network when it can, with the age of its last check when it cannot), whether it loads, the
  handoff hook, the repository guide, the working set, versioned and moved citations, the trace,
  the queue's *since*, commits, and CI. `./se --post` is the session's power-on self test: can this
  session be torn, was it compacted, is disk low, and the rules that follow; it runs as a
  SessionStart hook. Tested with Claude Code only; CI runs its tests.
- AGENTS.md and README say that every trial, review, and tool ran with Claude models only, and ask
  agents of other families, and people, to push back and propose changes as pull requests.
- ADOPT.md: how to make a repository one that follows the guide, in eight steps, and what an agent
  does where the adoption is only partly done: no requirements document, no queue, no check
  command, no `Non-goals`, no glossary, no handoff check, or AGENTS.md not loaded. AGENTS.md points
  at it; README, llms.txt, and CHECKLISTS link it.
- AGENTS.md *After a gap*: import AGENTS.md from a copy kept inside the working directory, and
  check that it loaded; an instruction the summary reports is a claim; the handoff check is a hook,
  not a line the agent must choose to follow (so says the hand-off checklist). From an adversarial read of
  the file: what to do in a repository with no working set; a version update is a chore; what
  counts as a new noun or a recognizable implementation; the input cases are decided, not asked.

## v1.1 — 2026-10-20

[Full diff from v1.0](https://github.com/wmacevoy/software-engineering/compare/v1.0...v1.1) · 97
principles

**For copies:** re-copy AGENTS.md and the templates. Cite requirements with the version that last
changed them — `REQ2/UI-1`, not `UI-1` — in tests, commits, and the queue; cite designs as
`DESIGN_v2`.

### New

- [SE1/U7](guide/02-unknowing.md#u7) Find the K3 factories: anything that keeps saying "fine" with no
  way to say "wrong" — eight common ones, and three cures.

### Changed

- [SE1/R2](guide/04-requirements.md#r2) Requirements are numbered *and versioned*; unversioned
  references to requirements and design are K3 factories.
- [SE1/R10](guide/04-requirements.md#r10) Cite the version that last changed a requirement
  (`REQ2/UI-1`), and mark each requirement *(since v2)*.
- [SE1/R11](guide/04-requirements.md#r11) The trace is a search for the versioned requirement ID.
- [SE1/W11](guide/08-work.md#w11) The definition of done names the versioned requirement ID.

### Also changed

- AGENTS.md: *Find the requirement* and *Name the requirement in the test* ask for the versioned ID,
  and a citation older than its requirement is raised.
- Templates: requirements are marked *(since v1)*; the queue and design cite `REQ1/UI-1`.
- Wording only: [SE1/T3](guide/06-testing.md#t3) says "K3 factory" rather than "K3 generator";
  [SE1/A2](guide/10-agents.md#a2) cites U7; [SE1/U6](guide/02-unknowing.md#u6)'s templates link no
  longer 404s on the site.

## v1.0 — 2026-10-20

[Browse v1.0](https://github.com/wmacevoy/software-engineering/tree/v1.0) · 96 principles

The first major version, SE1. Principle IDs are cited as `SE1/<ID>` and do not move within SE1.
