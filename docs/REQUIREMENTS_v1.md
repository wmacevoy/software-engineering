# Requirements — v1

What must be observably true of this repository, and what is not being built. Changes only with
the client; a change is a new version (`REQUIREMENTS_v2.md`), never an edit to this one. Written
2026-10-28 by joining late ([SE1/W12](../guide/08-work.md#w12)): every requirement below is read
off what the checker, `se`, CI, and the release procedure already enforce, and is marked
*(inferred)* until the client confirms it. See [SE1/R1–R11](../guide/04-requirements.md).

Client: Warren MacEvoy, the author, who is also the maintainer. The proxy for the users
([SE1/H5](../guide/09-people.md#h5)): adopters, through the doctor's rows and the field reports in
[GAPS.md](../GAPS.md), and the fall 2026 course. Date sent: 2026-10-28 · *Tell us what is wrong
with it.*

## Glossary

| Term | Meaning |
| ---- | ------- |
| Principle | One idea with an ID (`T3`), in one chapter, cited as `SE1/T3`. |
| Release | A git tag `vX.Y` (minor) or `vX.Y.Z` (patch), with a dated section in the CHANGELOG. |
| Copy | A file adopters copy at a release: AGENTS.md, the templates, `se`, `se.py`, `se.ps1`. |
| Marker | The first line under a principle's heading: a person's *New/Changed in*, or git's *Since*. |
| Archive entry | A record in `archive/` of a source: URL, date, checksum, opened or not, extraction. |
| Review | A proposal about the guide, kept in `archive/reviews/`; never an edit to it. |
| The check | `sh tools/check.sh`: the checker, the since check, `se --self`, the tests. |
| Working set | This directory: these requirements, the design, the queue, the findings. |

## The pain

The guide is cited by ID, copied into other repositories, and read by agents that trust fluent
text. A principle that moved, a copy that is behind, a claim with no source, or a check that
passes without checking is a K3 factory in a guide about K3 factories
([SE1/U7](../guide/02-unknowing.md#u7)). On 2026-10-28 the doctor passed a row on a line in README,
a commit described five changes while holding one, and a hash moved on one platform; each was
found by something outside the author's head. The requirements below are what that outside is.

## People this touches

- The author, who signs every release and teaches from the text.
- Adopters, who copy AGENTS.md, the templates, and `se`, and run the doctor on their repositories.
- Agents, Claude and others, that load AGENTS.md at every start and are told the testing was
  Claude-only.
- Students of the fall 2026 course, whose project is the running example's worked version.
- Reviewers, human and model, whose reviews are kept with what they opened and what they only
  read.
- People named in commits and trailers: the author by name, the agents by model.

## Requirements

Numbered, observable, with numbers. Cite them as `REQ1/ID-1`. Everything here is *(inferred)* from
the repository as it stands unless the client confirms it.

**Identity**

- **ID-1** *(since v1)* *(inferred)* Every principle has one ID, unique across the guide, and the
  README's index lists exactly the chapter headings; the checker fails on a duplicate or a mismatch.
- **ID-2** *(since v1)* *(inferred)* Within SE1 an ID never moves to a different idea; a retired
  principle keeps its ID with a note. Observable: no tag's index maps an ID to a different title
  than a later tag's, except by a CHANGELOG entry saying so.
- **ID-3** *(since v1)* *(inferred)* Every citation carries the major version (`SE1/T3`), and a
  link labeled with an ID points at the file that defines it; the checker fails on a bare or
  misdirected citation.

**Releases**

- **REL-1** *(since v1)* *(inferred)* Every principle whose text differs from the newest tag is
  acknowledged in the CHANGELOG, as a *New/Changed in* marker or an *Also changed* line, before the
  next release; the checker fails otherwise.
- **REL-2** *(since v1)* *(inferred)* Every copy says which release it came from and links that
  tag, and cites no ID the release lacks; `se --doctor` reports a copy behind the newest release,
  and tries the network for that, reporting the age of its last successful check when it cannot.
- **REL-3** *(since v1)* *(inferred)* A patch release changes no principle, no AGENTS.md, and no
  template; the checker fails a patch that does.
- **REL-4** *(since v1)* *(inferred)* Every principle carries a marker with the release and date at
  which its current text first appeared, computed from the tags; `node tools/since.js --check`
  fails on a marker that differs from git's answer.
- **REL-5** *(since v1)* *(inferred)* `se.py` names its release and the hash of AGENTS.md at that
  release; `se --self` fails when the released AGENTS.md hashes differently.

**Sources and reviews**

- **SRC-1** *(since v1)* *(inferred)* A number or quotation in the guide cites an archive entry
  holding the URL, the date, the SHA-256 of the bytes fetched, whether the reviewer opened the
  source, and the passage relied on. An entry for a source not opened says so.
- **SRC-2** *(since v1)* *(inferred)* A review is kept in `archive/reviews/` and edits nothing;
  what survives it enters the principles, GAPS, and the CHANGELOG by its own commits.
- **SRC-3** *(since v1)* *(inferred)* A principle's meaning changes only on evidence recorded in
  GAPS, a field report or a trial, or on the author's stated decision; the CHANGELOG entry names it.

**Checks**

- **CHK-1** *(since v1)* *(inferred)* One script, `tools/check.sh`, is the full check, run by
  contributors and by CI on Linux, macOS, and Windows with Python 3.9 and the newest; the doctor
  fails when the workflow runs anything other than the guide's named check.
- **CHK-2** *(since v1)* *(inferred)* Every check has been seen to fail on a planted breakage, and
  the breakage is recorded (FINDINGS, a commit message, or a test fixture) so it can be replanted.
- **CHK-3** *(since v1)* *(inferred)* The site renders every chapter and reference page from
  `main`: each returns HTTP 200 with the page's text in it, within one Pages build of a push.

**The tooling for adopters**

- **SE-1** *(since v1)* *(inferred)* `se --doctor` reports each row of ADOPT.md's checklist as
  pass, warn, none yet, or fail, with the principle and the fix; exit code 1 on any fail; "none
  yet" is never a failure.
- **SE-2** *(since v1)* *(inferred)* `se --post` refuses, exit code 1, when a precondition for
  safe work is missing (disk below its floor), reports the risks it cannot refuse, and runs as a
  hook; rows that describe one runner's configuration say which runner.
- **SE-3** *(since v1)* *(inferred)* `se.py` is standard-library Python 3.9 or newer, runs on the
  three platforms, and is copied unchanged; the wrappers pick the repository's own interpreter.
- **SE-4** *(since v1)* *(inferred)* Every doctor and self-test check has a fixture on which it is
  seen to fail, in `tools/test_se.py`.

**Law and people**

- **LAW-1** *(since v1)* *(inferred)* The guide is MIT-licensed; the archive stores a source's full
  text only where its license allows, and otherwise its checksum and a short extraction.
- **LAW-2** *(since v1)* *(inferred)* No secret, token, or personal data beyond the author's name
  and address in commits appears in the repository; `se --post` reports which runner it saw and
  never its credentials.
- **PPL-1** *(since v1)* *(inferred)* A commit an agent drafted carries its trailer; the author
  signs; an agent commits, tags, pushes, or publishes only when asked.

## Inputs: absent, late, wrong, lying

| Input | Absent | Late | Wrong | Lying |
| ----- | ------ | ---- | ----- | ----- |
| The release tags | the checker says `git fetch --tags` and fails | a tag pushed after the commit: `since --write` on the next commit | a tag on the wrong commit: `se --self` fails | — |
| A copy's label | fail: "carries no release label" | behind: "vX is out" | edited: "text differs from the release's" | a label claiming a release whose text it is not: the hash says so |
| The network, for the release check | report it, and the age of the last check | timeout 5 s, then as absent | — | a wrong tag list: the hash of the released AGENTS.md still decides |
| A review's claim | — | — | opened at the source before acting | the same: the source wins ([SE1/A11](../guide/10-agents.md#a11)) |
| A source behind a claim | "not opened" in the archive | — | the checksum differs on re-fetch: the extraction is what was true on the date | — |
| The site | a failed Pages build, visible in the repository's actions | — | a page that renders raw: an accepted known issue for CONTRIBUTING | — |

## Operating envelope

- **Scale:** 100 principles in 10 chapters, about 40 Markdown files, 7 archive entries, 7 reviews;
  in two years perhaps 120 principles and a second major version *(invented)*.
- **Speed:** the full check under one minute locally and under three in CI *(invented)*.
- **Recovery:** git; nothing else holds state. A bad release is followed by a patch, never
  retagged ([SE1/O11](../guide/07-operating.md#o11)).
- **Availability:** the site is GitHub Pages; an outage costs nothing but reading, and the
  Markdown is the source.
- **Resources:** none finite.
- **Interruption:** a cut session leaves a branch and a trace; commits are atomic; the markers are
  recomputed, never hand-kept ([SE1/U7](../guide/02-unknowing.md#u7), torn work).

## Security, law, and ethics

No data about people beyond git's authorship. Sources are cited, not redistributed, unless their
license allows. Reviews by agents are labeled with the model and date, and the front page says the
testing was Claude-only and asks others to push back.

## Assumptions (K4s), read back to the client

- "We're assuming the Markdown is the source and the site is only a rendering, so a rendering
  defect is never fixed in the source. True?" — *(not yet answered)*
- "We're assuming adopters copy AGENTS.md unchanged and put local rules in their own guide. True?"
  — *(not yet answered)*
- "We're assuming a patch release never changes a copy, so copies keep the minor's label. True?" —
  *(not yet answered)*
- "We're assuming reviews are proposals and never edit the live guide. True?" — *(not yet
  answered)*
- "We're assuming a principle changes meaning only on recorded evidence or your stated decision.
  True?" — *(not yet answered)*

## Scope decisions

- The guide, not the course, is the authority for the principles — the author
  ([README](../README.md#where-this-came-from)).
- IDs never move within SE1; a major version may renumber with a map — the author (README).
- A patch release changes no principle, AGENTS.md, or template — the author, 2026-10-28 ("I think
  v1.2.1; it's a small change").
- U8 stays where it is; moving an ID is SE2 — the author, 2026-10-28.
- Reviews live in `archive/reviews/` — the author, 2026-10-28 ("mv the reviews into the archive").
- The site's known rendering issues are accepted — the author, 2026-10-20.

## Non-goals

- Not a second copy of the course essays, and not a textbook: one set of principles, cited by ID.
- Not a linter for adopters' code: the doctor checks the adoption, not the software.
- Not a build: no step between the Markdown and the site but Pages' own.
- Not a framework for other guides: DM1 adapts the shape by hand; `se` serves SE1's documents
  (queue #1, #5).

## Not yet answered

- Which runner besides Claude Code the doctor should know — nobody has tried one but Codex, once.
- Whether `se` belongs in this repository or beside it, once a second guide uses it.

## Deferred

- *Not yet:* REQUIREMENTS for the compaction project's tooling, which lives elsewhere.
- *Not yet:* a `docs/` index page on the site; `docs/` is hidden from the nav on purpose.
