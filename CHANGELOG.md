# Changelog

What changed between releases, by principle ID, newest first. A change you cannot spot is a K3
factory ([SE1/U7](guide/02-unknowing.md#u7)), so every change is visible in three places:

- **Here**, by ID, with a full diff link per release.
- **Under the principle's heading**, as *New in v1.1.* or *Changed in v1.1.* — the release that last
  changed its meaning. A principle with no marker is as it was in v1.0.
- **In every copy**: AGENTS.md and the templates link to the release they came from, so a copy that
  is behind says so.

`tools/check.js` keeps the three in step, and compares every principle with the last release tag:
one whose text changed must have a marker for a later release, or — for wording only — be named
under that release's *Also changed*. Work toward a release goes under `## v1.3 — unreleased`; give it
a date when you tag it. Within SE1, a minor release may add principles, reword them, or extend what
they ask; it never moves an ID ([principle index](README.md#principle-index)). A patch release
(`v1.2.1`) changes no principle, no AGENTS.md, and no template: copies keep the minor's label, and
the checker holds a patch to that.

**If you keep a copy** of AGENTS.md or the templates, read *For copies* in each release newer than
yours.

## v1.3 — unreleased

[Changes on main since v1.2.1](https://github.com/wmacevoy/software-engineering/compare/v1.2.1...main)

**For copies:** re-copy AGENTS.md (*Before you start* no longer asserts that the self test ran) and
`se.py`.

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
