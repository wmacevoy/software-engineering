# Design — v1

How this repository satisfies [REQUIREMENTS_v1](REQUIREMENTS_v1.md), and what was rejected. Written
2026-10-28 by joining late ([SE1/W12](../guide/08-work.md#w12)): the structure is as found; every
reason has its source, a commit or a review, or is marked *(inferred)*. Every mechanism here should
be replaceable without renegotiating a requirement ([SE1/R5](../guide/04-requirements.md#r5)).

## Components and the dependency rule

| Component | Layer | Kind | Contract (one line) | Holds state? |
| --------- | ----- | ---- | ------------------- | ------------ |
| `guide/`, README, GLOSSARY, CHECKLISTS, READING, GAPS, CHANGELOG | 0 | text | principles with IDs in a fixed heading grammar; the index matches the headings; the CHANGELOG lists releases | no |
| `AGENTS.md`, `ADOPT.md`, `templates/` | 0 | copies | self-labeled with a release; links are absolute tag URLs so a copy resolves anywhere | no |
| `archive/` | 0 | records | one entry per source or review; checksums; opened or not | no |
| `tools/bodies.js` | 1 | library | what a heading, a marker, and a principle's text are, for both tools | no |
| `tools/check.js` | 2 | check | REQ1/ID-1, ID-3, REL-1, REL-2 (copies' labels), REL-3; exits 1 on any problem | no |
| `tools/since.js` | 2 | check and writer | REQ1/REL-4: markers from the tags; `--check`, `--write`, `--as` | no |
| `tools/test_se.py` | 2 | tests | REQ1/SE-4: one fixture per doctor check, seen red | no |
| `se.py`, `se`, `se.ps1` | 2 | tool for adopters | REQ1/SE-1..3, REL-2, REL-5; standard library; copied unchanged | a release cache under `~/.cache/se` |
| `tools/check.sh`, `.github/workflows/check.yml` | 3 | the check and CI | REQ1/CHK-1: one recipe, six jobs | no |
| GitHub Pages, `_config.yml` | 3 | rendering | REQ1/CHK-3: `main` rendered with the named theme; nothing else | no |

A component depends only on lower layers: the tools read the text's grammar through `bodies.js`
and never the reverse; `se.py` depends on nothing in the repository but AGENTS.md's label and hash
at a release; CI runs the one script. No check enforces the layering yet *(inferred: a queue item
if it is ever broken)*.

## State

| State | Owner (authoritative) | Copies | Max staleness | While wrong, the user sees |
| ----- | --------------------- | ------ | ------------- | -------------------------- |
| Which release a text is | the git tag | the CHANGELOG section's date; AGENTS.md's label; the templates' links; `se.py`'s `RELEASE` and `AGENTS_SHA256` | until the release commit | `se --self` red; the checker's "stale release"; the doctor's "vX is out" |
| A principle's *since* | the tags, computed | the marker under the heading | until `since --write` after a release | `since --check` red in CI |
| A source's text | the source | the archive entry's checksum and extraction | forever, by design: the entry says what was true on the date | a re-fetch hashes differently |
| The newest release, in an adopter's doctor | the GitHub tags | `~/.cache/se/releases.json` | reported in days; stale after 30 | "release check not made; last successful check N days ago" |
| The rendered site | `main` | Pages' build | one build after a push | a failed build in the repository's actions |

## Essential complexity

Each line traces to a requirement.

1. Principles are cited by ID, so an ID must never move (REQ1/ID-1, ID-2).
2. The guide is copied, so a copy must say which release it is and be checkable against it
   (REQ1/REL-2, REL-5).
3. Releases are tags, so what changed between tags must be visible in three places that cannot
   drift apart (REQ1/REL-1, REL-4).
4. A patch may not change what adopters copy (REQ1/REL-3).
5. Claims rest on sources that move, so the source's bytes are hashed and the passage kept
   (REQ1/SRC-1).
6. Agents review and draft here, so a review is a proposal and a change has a recorded reason
   (REQ1/SRC-2, SRC-3, PPL-1).
7. One recipe checks all of it, everywhere (REQ1/CHK-1, CHK-2).

## One-way doors

- **An ID, once published** ([SE1/D11](../guide/05-design.md#d11)): reviewed by the author before
  each release; U8 was reviewed by three readers and kept.
- **A tag, once pushed** ([SE1/O11](../guide/07-operating.md#o11)): never retagged; a bad release
  is followed by a patch. v1.2.1 and v1.3 were cut this way on 2026-10-28.
- **`se`'s flags and output lines**, which adopters will script: `--doctor`, `--post`, `--hook`,
  `--self`, `--json`; the states pass, warn, none yet, fail. *(inferred: no adopter scripts them yet.)*
- **The marker grammar**, which `bodies.js` parses and every chapter carries.

## Decisions

- **A principle's text ends at a horizontal rule** — REQ1/REL-1 — the rule after a chapter's last
  principle counted as its text, so inserting A11 "changed" A10 — alternative rejected: a CHANGELOG
  line recording a non-change — source: commit e4bac77, REVIEW-v1.1-fable.md BT2.
- **A copy must not cite an ID its label lacks** — REQ1/REL-2 — AGENTS.md said v1.1 while citing
  A11 — source: commit dd11fe2, BT1.
- **A patch changes no principle, AGENTS.md, or template; copies keep the minor's label** —
  REQ1/REL-3 — the author's v1.2.1 — alternative rejected: relabeling every copy at every patch —
  source: commit bd7f029.
- **Markers are computed from the tags, with a person's New/Changed kept as written** —
  REQ1/REL-4 — hand-made markers drift and say nothing for unchanged principles — alternative
  rejected: generating at site build, which Pages cannot do — source: commit 642c0dd.
- **One check script for contributors and CI; the doctor compares literally** — REQ1/CHK-1 — a
  `python3`/`python` normalization had hidden a second recipe — source: commit 1eb6ec7, the author's
  "/* */" story.
- **`se --post` refuses on a missing precondition and only reports the rest** — REQ1/SE-2 — the
  glossary's power-on self test refuses; the tool had not — source: commit b054c54, the Codex
  review.
- **`se` hashes bytes, decodes subprocess output as UTF-8** — REQ1/SE-3 — Windows 3.9 decoded with
  the locale's code page — source: commit be92ca2.
- **The checker and the since tool share `bodies.js`** — REQ1/REL-1, REL-4 — one definition of a
  principle's text ([SE1/D10](../guide/05-design.md#d10)) — source: commit 642c0dd.
- **Sources in `archive/`, reviews in `archive/reviews/`** — REQ1/SRC-1, SRC-2 — the author, 2026-10-28
  — source: commits 55606ce, 8073297.
- **Full texts not stored unless the license allows** — REQ1/LAW-1 — Royce is IEEE's — source:
  archive/README.md *(inferred: the author has not ruled on arXiv's licenses case by case)*.
- **The release check tries the network and reports staleness** — REQ1/REL-2 — the author:
  "try to check releases, and warn if you didn't and how stale the check is" — source: commit
  186daaf.
- **SE1's copy is known by the line that names this guide's release, not by its label alone** —
  REQ1/REL-2 — the data-mining guide's agreement carries a label of its own release, and the doctor
  took it for SE1's — alternative rejected: teaching `se` other guides' labels, which Non-goals
  exclude — source: commit fb7586b, FINDINGS 2026-10-28.
- **History is not stale; shorthand is versioned by its line** — REQ1/SE-1 — a FINDINGS entry or a
  done queue row keeps the citation it was written with, and a bare ID takes the version named
  before it on the same line — alternatives rejected: keeping the check strict and having copies
  rewrite their records, which would make them false; exempting every queue row, which the open-row
  fixture refuses — source: PR #1's question, decided by the author 2026-10-29.
- **A README alone names no check command** — REQ1/SE-1 — the fallback that reads any line
  mentioning tests runs for CONTRIBUTING.md and CLAUDE.md only — alternative rejected: filtering
  path-like candidates, which guesses — source: FINDINGS 2026-10-29, the fall-2026 handoff.

## Deferred

- *Not yet:* a check that enforces the layering above; it has not been broken.
- *Not yet:* `se` knowing another guide's documents; it names a `docs/` in another shape and checks
  SE1's only (queue #5).
- *Not yet:* a `docs/` index page; the working set is hidden from the site's nav on purpose.
