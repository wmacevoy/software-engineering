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
under that release's *Also changed*. Work toward a release goes under `## v1.2 — unreleased`; give it
a date when you tag it. Within SE1, a minor release may add principles, reword them, or extend what
they ask; it never moves an ID ([principle index](README.md#principle-index)).

**If you keep a copy** of AGENTS.md or the templates, read *For copies* in each release newer than
yours.

## v1.2 — unreleased

[Changes on main since v1.1](https://github.com/wmacevoy/software-engineering/compare/v1.1...main)

Nothing yet.

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
