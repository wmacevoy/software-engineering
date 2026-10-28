# Contributing

How to work on this repository — for a new teammate and for an agent, who both arrive knowing
nothing ([SE1/A3](guide/10-agents.md#a3)). Keep it short and true: a change that makes a line here
untrue updates it in the same change ([SE1/W11](guide/08-work.md#w11)). This is the repository
guide that [SE1/W10](guide/08-work.md#w10) asks for; the guide itself is in `guide/`.

## Run it

- **Prerequisites:** git with the release tags (`git fetch --tags`); Node 24 or any recent Node;
  Python 3.9 or newer, standard library only. Nothing to install.
- **Build:** none. The Markdown is the source. GitHub Pages renders `main` with the theme named in
  `_config.yml`; there is no local build, and `tools/check.js` is what keeps the rendering honest.
- **Run:** `./se --doctor --offline` reports this repository's state (it is the guide, not an
  adopter, so most rows say "none yet", truthfully); `./se --post` reports the session's.
- **Reset to a known state:** `git checkout -- . && git clean -fd`. Nothing is generated except
  `__pycache__`, which is ignored. ([SE1/T5](guide/06-testing.md#t5))

## Check it

- **The full check**, the same script CI runs on Linux, macOS, and Windows with Python 3.9 and the
  newest, so there is no second recipe to drift ([SE1/O3](guide/07-operating.md#o3)):

  ```sh
  sh tools/check.sh
  ```

  It runs `node tools/check.js`, `node tools/since.js --check`, `se.py --self`, and
  `tools/test_se.py`, with the interpreter `se` would choose.

- **Success prints:** `N files, 100 principles, 0 problems` · `10 chapters, 0 marker(s) differ
  from git` · `se --self: AGENTS.md matches vX.Y` · `OK`.
- **Instruments, and how each was seen to fire** ([SE1/T3](guide/06-testing.md#t3)): the checker
  on six planted breakages (a copy mislabeled, a principle reworded with no marker, an index line
  dropped, a broken link, a template citing an ID the release lacks, a rule inserted inside a body);
  `since --check` on a marker edited by hand; `test_se.py` on one fixture per doctor check; `se
  --self` on a stale pin. When you touch one, make it fire again.

## Rules for this repository

- **An ID never moves within SE1.** Reword freely; a retired principle keeps its ID with a note
  saying where its content went ([README](README.md#principle-index)).
- **A principle whose text changes must say so**: *Changed in vX.Y* under its heading, or an *Also
  changed* line in the CHANGELOG for wording only. The checker compares every principle with the
  last tag and refuses the unacknowledged. The marker's date, and the *Since* markers on the
  principles no release changed, are written by `node tools/since.js --write`; do not edit them by
  hand, `--check` will refuse it.
- **Releases.** A minor release (`v1.4`) may add or change principles, AGENTS.md, and the
  templates; a patch (`v1.3.1`) may change none of those, and the checker holds it to that. The
  release commit: date the CHANGELOG section and give it the full-diff link and the principle
  count; relabel AGENTS.md and the templates to the tag; set `RELEASE` and `AGENTS_SHA256` in
  `se.py` (`se --self` is red until you do); run `node tools/since.js --write --as vX.Y` so the
  markers carry the release's date before the tag exists; then tag, push the tag with `main`, and
  watch CI. Copies read *For copies* under the release in the CHANGELOG.
- **Sources.** A number or a quotation in the guide cites an entry in `archive/`, which records
  the URL, the date, the checksum, and whether the reviewer opened it
  ([SE1/D13](guide/05-design.md#d13)). Reviews of the guide are proposals and live in
  `archive/reviews/`; what survives one goes into the principles, GAPS, and the CHANGELOG.
- **Changes to the guide's meaning rest on evidence**: a field report in GAPS, or a trial; an
  untested idea goes into GAPS as open, not into a principle.
- **Commits.** One concern per commit; an agent commits, pushes, or tags only when asked; the
  trailer credits the agent, the author signs ([SE1/A7](guide/10-agents.md#a7)).
- **Accepted known issues:** `templates/CONTRIBUTING.md` renders as raw Markdown on the site, and
  template lines run past 100 columns because of their absolute URLs; both are chosen.

## Where things are

- **The guide:** `guide/` (ten chapters), `README.md` (the argument and the principle index),
  `GLOSSARY.md`, `CHECKLISTS.md`, `READING.md`, `GAPS.md` (where the principles fell short in the
  field), `CHANGELOG.md` (what each release changed, by ID).
- **This repository's working set:** `docs/REQUIREMENTS_v1.md`, `docs/DESIGN_v1.md`,
  `docs/QUEUE.md`, `docs/FINDINGS.md`. The requirements were read off the repository on 2026-10-28
  and are marked *(inferred)* until the author confirms them ([SE1/W12](guide/08-work.md#w12)).
- **For adopters:** `AGENTS.md`, `ADOPT.md`, `templates/`, and `se`, `se.py`, `se.ps1`, all copied
  at a release.
- **Sources and reviews:** `archive/`.
- **Tools:** `tools/check.js`, `tools/since.js`, `tools/bodies.js` (shared by both),
  `tools/test_se.py`.
- **Agents:** there is no `CLAUDE.md` here, so Claude Code reads `AGENTS.md` by itself; other
  runners load it as they do. Read it, then this file, before acting.
