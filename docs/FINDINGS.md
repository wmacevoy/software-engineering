# Findings

What this repository learned the expensive way, about itself and its tooling. The only document
reality writes ([SE1/W10](../guide/08-work.md#w10)). Where the *guide's principles* fell short in
the field is [GAPS.md](../GAPS.md); this file is for the repository as a project: the checker, `se`,
the releases, the reviews. Blameless: say what would have found it, not who should have asked
([SE1/H12](../guide/09-people.md#h12)).

## 2026-10-28 — `se`'s label pattern fails on a line-wrapped label

- **What happened:** run on the DM1 guide, the doctor said its AGENTS.md "carries no release
  label"; the label is there, wrapped across a line. The false failure went into a handoff before
  it was caught.
- **Kind:** K3 (the tool was sure).
- **Cost:** one wrong line in a baseline, corrected in the same note.
- **Findable by:** a fixture whose label wraps; every real copy is wrapped at 100 columns.
- **Changed:** `se`'s label pattern allows a line break, with that fixture (fb7586b, v1.3.1).

## 2026-10-28 — `se` takes any labeled AGENTS.md for a copy of SE1's, and knows only SE1's documents

- **What happened:** the DM1 guide's own AGENTS.md carries a DM1 release label; the doctor would
  read it as an SE1 copy and compare releases across guides. Its working-set rows look for
  `REQUIREMENTS_vN`, `DESIGN_vN`, `QUEUE`, `FINDINGS`; a DM1 project keeps `QUESTION_vN`,
  `PLAN_vN`, `LEDGER`, `DATASHEET`, `MODEL_CARD`, and would be told "none yet".
- **Kind:** K2 (a sibling guide was not imagined).
- **Findable by:** running the doctor on anything that is not an SE1 project.
- **Changed:** `se` knows SE1's copy by the line that names this guide's release, and names a
  `docs/` in another shape instead of reporting it as empty; it checks SE1's shape only, as the
  Non-goals say (fb7586b, v1.3.1).

## 2026-10-28 — On Windows with Python 3.9, decoding changed a hash

- **What happened:** `se --self` read the released AGENTS.md through `git show` as text; on that
  runner the locale's code page decoded the em dashes to other characters, and the hash moved. Five
  of six CI jobs were green.
- **Kind:** K3 (`text=True` felt safe).
- **Findable by:** exactly the matrix that found it, within the hour.
- **Changed:** `se` hashes bytes and decodes every subprocess read as UTF-8 explicitly.

## 2026-10-28 — A commit described five changes; its diff held one

- **What happened:** an edit script aborted on its second anchor, the shell guard did not stop the
  chain, and the commit landed with a message for all five. The diff caught it; the script's output
  would not have.
- **Kind:** K3 (the summary was fluent).
- **Findable by:** `git diff --stat` against the message before every commit.
- **Changed:** the drafter's practice, and `archive/reviews/REVIEW-v1.2-candidate.md` records it.

## 2026-10-28 — The published pages carry no *since* per principle

- **What happened:** the site shows a principle with no version and no date, so an unchanged
  reading and a stale one look alike; the *New/Changed in* markers are hand-made, mark only the last
  change of meaning, and say nothing for the ninety principles that have none.
- **Kind:** K2, found by the author reading the site as a stranger.
- **Findable by:** asking, of any page, "when did this last change, and would I know?"
  ([SE1/U7](../guide/02-unknowing.md#u7): make it age visibly).
- **Changed:** `tools/since.js` mines git for each principle's text *since* and writes it under
  the heading; the checker verifies it against git, so it cannot drift (queue #3).

## 2026-10-28 — A reviewer of another family found five things in three minutes

- **What happened:** Codex, on a no-push clone of v1.2.1, found five defects, four in text written
  after the three Claude readers ran and one, a vocabulary collision, that was the drafter's to
  see. All held when opened at the source; all fixed in v1.3.
- **Kind:** K3 for the drafter (the text read as finished).
- **Findable by:** a reader who does not share the writer's assumptions
  ([SE1/U3](../guide/02-unknowing.md#u3)). The method is recorded in
  `archive/reviews/REVIEW-METHOD-other-family.md`.
- **Changed:** v1.3; a Codex pass before each release.

## 2026-10-29 — `se` reads requirements only as bullets, and counts 0 in a table

- **What happened:** lwext4-bsd's REQUIREMENTS_v10 keeps its requirements as table rows
  (`| **FMT-1** | *(since v1)* ... |`). The doctor's pattern wanted `**ID** *(since vN)*` with
  only space between, so it read 0 requirements, and the citations and trace rows said "none yet",
  which read as true and was not. SE1/R10 asks for the ID and its *since*, not for a bullet.
- **Kind:** K3 (the tool was sure).
- **Cost:** a re-vendor's doctor run reported 0 failures on a repository whose citations it never
  read; caught because the count, 0, was plainly wrong for a 30-requirement document.
- **Findable by:** a fixture with a table-form requirements document.
- **Changed:** the pattern allows a table cell boundary between the ID and its *since*, with that
  fixture. Engaged on lwext4-bsd, the citations row then fails: 11 stale, 77 unversioned, most of
  them historical (FINDINGS, done queue rows) or list shorthand (`REQ10/TOOL-1, RST-3`). Whether
  those should count is a question about SE1/R10, left open.
