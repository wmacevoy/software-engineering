# Adopting the guide

How to make a repository one that follows this guide, and what an agent should do in one where the
adoption is only partly done. Adopting means five things: [AGENTS.md](AGENTS.md) loaded into every
agent session at its start; a repository guide that says how to build, run, test, and reset the
system; the working set in `docs/`; one check command that CI runs; and a definition of done. Most
adoptions start with code already written ([SE1/W12](guide/08-work.md#w12)), so most of the working
set is rebuilt from the code and marked *(inferred)* until a person confirms it. The words used
here are defined in [GLOSSARY.md](GLOSSARY.md). The guide's `se` runs this checklist: copy `se`,
`se.ps1`, and `se.py` beside AGENTS.md, and `./se --doctor` says which steps are done, which are
"none yet", and which are wrong; `./se --hook --write` makes the session's self test run at every
start ([SE1/T2](guide/06-testing.md#t2)). Tested with Claude Code only, and its rows about loading
and hooks describe Claude Code's configuration, the only runner inspected; observed loading, for
any runner, is the phrase test in step 2. With another tool, read what it reports with that in
mind, and tell us.

## For the owner

In order. Each step is small, and the repository is better after any of them than before.

1. **Copy AGENTS.md at the release it names, and keep it current.** The copy says which release it
   came from, so a copy that is behind says so ([SE1/U7](guide/02-unknowing.md#u7)). When a newer
   release appears, read *For copies* under it in [CHANGELOG.md](CHANGELOG.md) and re-copy. Do not
   edit the copy: local rules go in the repository guide, which wins over it where they disagree.
   Point the repository guide's and the design's links to the guide at the new release. A
   requirements version keeps the links it was written with: it is never edited in place
   ([SE1/R10](guide/04-requirements.md#r10)), and the next version links the new release.

2. **Make it load at every start** ([SE1/A11](guide/10-agents.md#a11)). In trials, a rule in a file
   the agent was told to follow changed nothing, because the file was never opened; the same rule
   already in context worked ([GAPS](GAPS.md#6-a-summary-is-a-concussion)). Then check that it
   loads, with a test that does not depend on the tool: pick a phrase only AGENTS.md contains (any
   sentence of it will do), start a fresh session, and ask the agent to quote it without opening
   any file. An agent that cannot quote it, or that opens the file to answer, did not have it
   loaded.

   *Claude Code, as documented and measured on 2026-10-27 (version 2.1.311). Detail like this has
   a short shelf life ([SE1/A10](guide/10-agents.md#a10)); check the date against your tool.*
   - Since v2.1.277, with no `CLAUDE.md` at or above the working directory, Claude Code reads
     `AGENTS.md` by itself. A `CLAUDE.md` or `CLAUDE.local.md` switches that off; then import the
     copy from `CLAUDE.md` with a line `@AGENTS.md`.
   - An import whose path leaves the working directory needs an approval that only an interactive
     session shows; a `-p` session loads nothing and says nothing
     ([GAPS](GAPS.md#2-an-import-from-outside-the-repository-does-not-load)). Keep the copy inside
     the working directory, which is smaller than the repository when a session starts in a
     subdirectory.
   - Verify with `/memory` or `/context`, which list what loaded, or an `InstructionsLoaded` hook,
     which logs each file with its reason: `include` for an import, `compact` for the reload after
     compaction. The hook does not fire for an `AGENTS.md` read without a `CLAUDE.md`, so the
     import is the checkable path.
   - `--bare` skips CLAUDE.md and hooks (whether it also skips the AGENTS.md fallback is not
     documented), needs an API key rather than a subscription login, and is announced as the future
     default for `-p`. A scripted session will then load nothing unless it asks to
     ([GAPS](GAPS.md#7-a-scripted-session-may-soon-load-nothing-by-default)).

3. **Write the repository guide** from [templates/CONTRIBUTING.md](templates/CONTRIBUTING.md): how
   to build, run, and reset, and the one check command with the line success prints
   ([SE1/A2](guide/10-agents.md#a2), [SE1/W10](guide/08-work.md#w10)). An agent that cannot run
   the check cannot check its own claim. If there is no check yet, the guide says "none yet": that
   is true, and a queue item.

4. **Create `docs/` and the working set** from the templates: `REQUIREMENTS_v1`, `DESIGN_v1`,
   `QUEUE`, `FINDINGS` ([SE1/W10](guide/08-work.md#w10)). On an existing codebase, rebuild them in
   the order [SE1/W12](guide/08-work.md#w12) gives: requirements from behavior, design from
   structure, findings from history, queue from the gaps; every requirement and reason nobody
   stated is marked *(inferred)*. A reconstruction that marks nothing is claiming more than it
   knows. `Non-goals` and `Scope decisions` may be short, but they must exist, because AGENTS.md
   searches them before every task ([SE1/R9](guide/04-requirements.md#r9)).

5. **Map AGENTS.md's nouns to this repository** in the repository guide, so that "the queue" names
   one thing here ([SE1/D9](guide/05-design.md#d9)):

   | AGENTS.md says                 | In this repository                                           |
   | ------------------------------ | ------------------------------------------------------------ |
   | the repository guide           | `CONTRIBUTING.md`                                            |
   | the queue                      | `docs/QUEUE.md`, or the issue tracker, if that is the cursor |
   | findings                       | `docs/FINDINGS.md`                                           |
   | the check command              | `_command_`; success prints `_line_`                         |
   | the handoff check              | `_script or hook_`, or "none yet"                            |
   | `Non-goals`, `Scope decisions` | sections of `docs/REQUIREMENTS_vX.md`                        |

6. **Name the client, or the proxy.** When the client is the maintainer, the users are real and
   never in the room. Name who stands in for them (the issue tracker, a downstream maintainer, a
   second maintainer) at the top of the requirements, and treat their bug reports as the read-back
   ([SE1/H5](guide/09-people.md#h5)).

7. **Define done, and have CI run the check** ([SE1/W11](guide/08-work.md#w11),
   [SE1/O3](guide/07-operating.md#o3)). The definition of done is the list in
   [CHECKLISTS.md](CHECKLISTS.md#working); drop a line that retires no fear here, and say why. CI
   runs the command the repository guide names, so "passes locally" and "passes" are one claim.

8. **A handoff check after compaction** ([SE1/A11](guide/10-agents.md#a11)). The minimum is
   [After a gap](AGENTS.md#after-a-gap), loaded at every start: every summary is recalled, not
   observed, and the source wins. Where the tool has a `PostCompact` hook, that is the hook that
   receives the summary; a `SessionStart` hook on `compact` does not, and what it adds back is
   capped at 10,000 characters: read in `PostCompact`, point from `SessionStart`, keep the pointer
   short. A check that has not been seen to fire on a real compaction is a K3 factory
   ([SE1/U7](guide/02-unknowing.md#u7)), so the loaded rule is the floor, and the check is not a
   substitute for it.

## For the agent, in a repository that is only partly adopted

AGENTS.md assumes the things above are in place. Where one is missing, the rule here replaces the
rule that assumed it. Report each absence once; do not stop on every task for it, and do not invent
the missing thing to satisfy a rule.

- **No requirements document.** Say so once. If the task is a chore, call it one; otherwise treat
  the task's own text as the requirement for this task only, marked *(inferred)*, and name the task
  in the test where a requirement ID would go. Propose the [SE1/W12](guide/08-work.md#w12)
  reconstruction as a queue item rather than doing it unasked; it is a task of its own.
- **No queue.** The task description is the queue item. Give it a *done* sentence if it has none,
  marked *(inferred)*, and report its status (ready, in progress, blocked on what, review) in your
  report; only a human marks it *done*.
- **No check command.** Say so. Run what exists (the tests, the build, a linter) and report exactly
  what ran and what it printed. "No check exists" is a result; "should pass" is not
  ([SE1/A2](guide/10-agents.md#a2)).
- **No `Non-goals` or `Scope decisions`.** Say the search found no such sections, proceed, and
  propose them. A decision you had to make in their absence goes in your report, marked
  *(inferred)*, so the owner can write it down or reverse it.
- **No glossary.** List the nouns you introduced in your report, so the owner can accept or rename
  each ([SE1/D9](guide/05-design.md#d9)).
- **No handoff check.** [After a gap](AGENTS.md#after-a-gap) still applies: the summary is recalled,
  not observed. Open the source before acting on a decision the summary reports.
- **AGENTS.md was not loaded, and you found it by opening it.** Follow it for this session, and tell
  the owner, with the fix and the test in step 2 above: a copy inside the working directory,
  imported from `CLAUDE.md` where one exists, and a fresh session asked to quote a line of it.

## Adoption checklist

- [ ] AGENTS.md is a copy of the release it names, unedited; local rules are in the repository
      guide. ([SE1/U7](guide/02-unknowing.md#u7))
- [ ] It loads at every start: a phrase only it contains comes back in a fresh session.
      ([SE1/A11](guide/10-agents.md#a11))
- [ ] The repository guide names the check command, what success prints, and how to reset.
      ([SE1/A2](guide/10-agents.md#a2))
- [ ] `docs/` holds the working set; everything reconstructed is marked *(inferred)*.
      ([SE1/W10](guide/08-work.md#w10), [SE1/W12](guide/08-work.md#w12))
- [ ] `Non-goals` and `Scope decisions` exist, even if short.
      ([SE1/R9](guide/04-requirements.md#r9))
- [ ] The repository guide maps AGENTS.md's nouns to this repository.
      ([SE1/D9](guide/05-design.md#d9))
- [ ] The client, or the proxy for the users, is named. ([SE1/H5](guide/09-people.md#h5))
- [ ] Done is defined, and CI runs the check command. ([SE1/W11](guide/08-work.md#w11),
      [SE1/O3](guide/07-operating.md#o3))
- [ ] After compaction a check reads the summary from outside, or at least the loaded rule treats
      it as recalled. ([SE1/A11](guide/10-agents.md#a11))
- [ ] `./se --doctor` reports no failure, and `./se --post` runs at every start, resume, and
      compaction. ([SE1/T2](guide/06-testing.md#t2), [SE1/U7](guide/02-unknowing.md#u7))
