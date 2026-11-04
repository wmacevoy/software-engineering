#!/usr/bin/env python3
"""Tests for se.py: every doctor check is seen to fail on a fixture built to fail it (SE1/T3; REQ1/SE-4),
the doctor's rows and exit code (REQ1/SE-1), the self test's refusal and verdicts (REQ1/SE-2), the
release check's staleness and the copy's label (REQ1/REL-2), and the pin (REQ1/REL-5). Run: python3 -I tools/test_se.py. Standard library only; no network, no wall clock, no shared
state: every fixture is a fresh git repository in a temporary directory."""
import datetime as dt
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

GUIDE = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("se", GUIDE / "se.py")
se = importlib.util.module_from_spec(spec)
spec.loader.exec_module(se)

TODAY = dt.date(2026, 10, 28)
AGENTS_TEXT = (GUIDE / "AGENTS.md").read_text(encoding="utf8")
AGENTS_LABEL = se.LABEL_RE.search(AGENTS_TEXT).group(1)

GOOD = {
    "AGENTS.md": AGENTS_TEXT,
    "CLAUDE.md": "# Project\n\n@AGENTS.md\n",
    "se.py": "# a copy\n",
    ".claude/settings.json": json.dumps(se.hook_entry("python3 se.py --post")),
    "CONTRIBUTING.md": "## Check it\n\n- **The full check:** `python3 -m unittest` — the same one CI runs\n- **Success prints:** `OK`\n",
    "docs/REQUIREMENTS_v2.md": "# Requirements — v2\n\n## Requirements\n\n- **UI-1** *(since v1)* The page shows a count.\n- **UI-2** *(since v2)* A stale count shows its age.\n\n## Scope decisions\n\n- counts, not locations\n\n## Non-goals\n\n- reservations\n",
    "docs/DESIGN_v1.md": "# Design — v1\n",
    "docs/QUEUE.md": "# Queue\n\n| # | Item | Status | Since |\n| - | ---- | ------ | ----- |\n| 1 | the age | in progress | 2026-10-27 |\n| 2 | the map | blocked: on the client | 2026-10-20 |\n",
    "docs/FINDINGS.md": "# Findings\n",
    "tests/test_ui.py": "# REQ1/UI-1 and REQ2/UI-2 are covered here\n",
    ".github/workflows/check.yml": "on: push\njobs:\n  check:\n    steps:\n      - run: python3 -m unittest\n",
}

# Another guide's agreement at the root, in the shape of the data-mining guide's: it links SE1's AGENTS.md
# as a blob and carries a label of its own release, so it is not a copy of SE1's.
SIBLING = ("# AGENTS.md — data work\n\nIt **extends** the [SE1 working agreement]"
           "(https://github.com/wmacevoy/software-engineering/blob/v1.3/AGENTS.md) at SE1 v1.3.\n\n"
           "The DM1 IDs are defined in the guide at https://github.com/wmacevoy/data-mining/tree/main. This copy is\n"
           "from **v1.0**; what changed since, by ID, is in the guide's CHANGELOG.\n")


def git(repo, *args):
    return subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", *args], cwd=repo,
                          capture_output=True, text=True, check=True).stdout


def make_repo(tmp, files=GOOD, message="UI-1: show the count (REQ1/UI-1)"):
    repo = Path(tmp)
    for rel, text in files.items():
        p = repo / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, "w", encoding="utf8", newline="\n") as fh:  # Path.write_text(newline=) is 3.10+; this runs on 3.9
            fh.write(text)
    git(repo, "init", "-q")
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", message)
    return repo


def finding(findings, name):
    return next(f for f in findings if f.name == name)


class Fixture(unittest.TestCase):
    """A fresh repository per test, with se's hash pinned to the copy so only the fixture's one defect shows."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.cache = tempfile.TemporaryDirectory()
        self.saved = se.AGENTS_SHA256
        se.AGENTS_SHA256 = hashlib.sha256(AGENTS_TEXT.replace("\r\n", "\n").encode("utf8")).hexdigest()

    def tearDown(self):
        se.AGENTS_SHA256 = self.saved
        self.tmp.cleanup()
        self.cache.cleanup()

    def doctor(self, files=GOOD, message="UI-1: show the count (REQ1/UI-1)"):
        repo = make_repo(self.tmp.name, files, message)
        return se.doctor(repo, online=False, cache_dir=self.cache.name, today=TODAY)

    def changed(self, **edits):
        files = dict(GOOD)
        for k, v in edits.items():
            if v is None:
                files.pop(k, None)
            else:
                files[k] = v
        return files


class TestDoctorGood(Fixture):
    def test_good_repo_passes_every_check_but_the_offline_release(self):
        f = self.doctor()
        states = {x.name: x.state for x in f}
        self.assertEqual(states["release check"], se.FAIL)  # never checked, offline: a true fail
        for name in ("working agreement", "loads at every start", "handoff hook", "repository guide",
                     "working set", "citations", "trace", "queue", "commits", "CI"):
            self.assertEqual(states[name], se.PASS, name)

    def test_requirements_in_a_table_are_read(self):
        # REQ1/SE-1: a requirement in a table row (`| **UI-1** | *(since v1)* ... |`) is a requirement;
        # lwext4-bsd's REQUIREMENTS_v10 has 30 of them, and the doctor counted 0 (FINDINGS 2026-10-29)
        req = ("# Requirements — v2\n\n## Requirements\n\n| ID | Requirement |\n| -- | ----------- |\n"
               "| **UI-1** | *(since v1)* The page shows a count. |\n| **UI-2** | *(since v2)* A stale count shows its age. |\n\n"
               "## Scope decisions\n\n- counts, not locations\n\n## Non-goals\n\n- reservations\n")
        f = self.doctor(self.changed(**{"docs/REQUIREMENTS_v2.md": req}))
        self.assertIn("(2 requirements)", finding(f, "working set").text)
        self.assertEqual(finding(f, "citations").state, se.PASS)
        self.assertEqual(finding(f, "trace").state, se.PASS)


class TestJudged(Fixture):
    """REQ1/SE-1, SE1/U10: a requirement marked (judged) is passed by its judge. A test may veto it, so a
    test naming it must not read as coverage, and no test naming it must not read as a gap."""
    REQ = ("# Requirements \u2014 v2\n\n## Requirements\n\n"
           "- **UI-1** *(since v1)* The page shows a count.\n"
           "- **UI-2** *(since v2)* *(judged)* Judge: the supervisor, at each demo.\n\n"
           "## Scope decisions\n\n- counts, not locations\n\n## Non-goals\n\n- reservations\n")

    def trace(self, tests, **more):
        files = {"docs/REQUIREMENTS_v2.md": self.REQ, "tests/test_ui.py": tests}
        files.update(more)
        return finding(self.doctor(self.changed(**files)), "trace")

    PASSED = "REQ2/UI-2 verdict: pass, by the supervisor, 2026-10-01"

    def findings(self, *lines):
        return GOOD["docs/FINDINGS.md"] + "\n" + "\n".join(lines) + "\n"

    def test_a_veto_test_is_not_coverage(self):
        row = self.trace("# REQ1/UI-1 and REQ2/UI-2\n")
        self.assertEqual(row.state, se.WARN)
        self.assertIn("UI-2 (no verdict yet)", row.text)

    def test_no_test_on_a_judged_requirement_is_not_a_gap(self):
        row = self.trace("# REQ1/UI-1\n")
        self.assertNotIn("have no test", row.text)
        self.assertIn("UI-2 (no verdict yet)", row.text)

    def test_an_ordinary_gap_is_still_reported(self):
        row = self.trace("# REQ2/UI-2\n", **{"docs/FINDINGS.md": self.findings(self.PASSED)})
        self.assertEqual(row.state, se.WARN)
        self.assertIn("1 of 1 requirements have no test", row.text)
        self.assertIn("UI-1", row.text)

    def test_a_recorded_verdict_passes_and_the_latest_is_shown(self):
        row = self.trace("# REQ1/UI-1\n", **{"docs/FINDINGS.md": self.findings(
            "REQ2/UI-2 verdict: fail, by the supervisor, 2026-09-01", self.PASSED)})
        self.assertEqual(row.state, se.PASS)
        self.assertIn("UI-2 (verdict pass 2026-10-01 by the supervisor)", row.text)

    def test_a_later_failure_stands_and_does_not_pass(self):
        # Codex, 2026-11-02: "verdict rejected" passed the row.
        for word in ("fail", "failed", "no", "rejected", "FAIL"):
            with self.subTest(word):
                row = self.trace("# REQ1/UI-1\n", **{"docs/FINDINGS.md": self.findings(
                    self.PASSED, f"REQ2/UI-2 verdict: {word}, by the supervisor, 2026-10-02")})
                self.assertEqual(row.state, se.WARN)
                self.assertIn("UI-2 (verdict FAIL 2026-10-02 by the supervisor)", row.text)

    def test_on_the_same_day_a_failure_outranks_a_pass(self):
        failed = "REQ2/UI-2 verdict: fail, by the supervisor, 2026-10-01"
        for lines in ((failed, self.PASSED), (self.PASSED, failed)):
            row = self.trace("# REQ1/UI-1\n", **{"docs/FINDINGS.md": self.findings(*lines)})
            self.assertEqual(row.state, se.WARN, lines)

    def test_a_verdict_on_an_older_version_of_the_requirement_is_none(self):
        row = self.trace("# REQ1/UI-1\n", **{"docs/FINDINGS.md": self.findings(
            "REQ1/UI-2 verdict: pass, by the supervisor, 2026-10-01")})
        self.assertEqual(row.state, se.WARN)
        self.assertIn("UI-2 (no verdict yet)", row.text)

    def test_a_verdict_names_an_outcome_and_a_judge(self):
        for line in ("REQ2/UI-2 verdict: by the supervisor, 2026-10-01",
                     "REQ2/UI-2 verdict: pending, by the supervisor, 2026-10-01",
                     "REQ2/UI-2 verdict: pass, 2026-10-01",
                     "REQ2/UI-2 verdict: passable by the supervisor, 2026-10-01"):
            with self.subTest(line):
                row = self.trace("# REQ1/UI-1\n", **{"docs/FINDINGS.md": self.findings(line)})
                self.assertEqual(row.state, se.WARN)
                self.assertIn("UI-2 (no verdict yet)", row.text)

    def test_a_test_cannot_record_a_verdict(self):
        row = self.trace("# REQ1/UI-1\n# " + self.PASSED + "\n")
        self.assertEqual(row.state, se.WARN)
        self.assertIn("UI-2 (no verdict yet)", row.text)

    def test_a_line_with_no_date_or_no_verdict_is_not_one(self):
        row = self.trace("# REQ1/UI-1\n", **{"docs/FINDINGS.md": self.findings(
            "REQ2/UI-2 verdict: pending", "REQ2/UI-2 was demoed 2026-10-01")})
        self.assertIn("UI-2 (no verdict yet)", row.text)

    def test_the_other_marks_and_table_rows_are_read(self):
        for req in ("- **UI-2** *(since v2)* *(inferred)* *(judged)* Judge: the supervisor.\n",
                    "- **UI-2** *(since v2)* *(judged)* *(inferred)* Judge: the supervisor.\n",
                    "- **UI-2** *(since v2)*\n  *(judged)* Judge: the supervisor.\n",
                    "| **UI-2** | *(since v2)* | *(judged)* | Judge: the supervisor. |\n"):
            with self.subTest(req):
                self.REQ = "# R\n\n## Requirements\n\n- **UI-1** *(since v1)* A count.\n" + req
                row = self.trace("# REQ1/UI-1\n")
                self.assertIn("UI-2 (no verdict yet)", row.text)

    def test_the_word_in_prose_does_not_mark_a_requirement(self):
        self.REQ = "# R\n\n- **UI-1** *(since v1)* A count.\n- **UI-2** *(since v2)* Unlike *(judged)* ones, a test passes this.\n"
        row = self.trace("# REQ1/UI-1\n# REQ2/UI-2\n")
        self.assertEqual(row.state, se.PASS)
        self.assertNotIn("judged", row.text)


class TestVendored(Fixture):
    """A repository that vendors another reads its own citations, and says what it left out (queue #22;
    `../tribe` at se v1.4.3, which vendors compaction with the same requirement names)."""

    VENDORED = {"vendor/other/docs/FINDINGS.md": "UI-1 bare, and REQ9/UI-2 ahead of this repository's version\n"}

    def test_a_vendored_trees_citations_are_not_this_repositorys(self):
        f = finding(self.doctor(self.changed(**self.VENDORED)), "citations")
        self.assertEqual(f.state, se.PASS, f.text)
        self.assertIn("vendor/other", f.text)

    def test_a_bad_citation_outside_the_tree_still_fails(self):
        f = finding(self.doctor(self.changed(**self.VENDORED, **{"docs/NOTES.md": "UI-1 bare\n"})), "citations")
        self.assertEqual(f.state, se.FAIL)
        self.assertIn("docs/NOTES.md:1", f.text)
        self.assertNotIn("vendor/other/docs", f.text)
        self.assertIn("vendor/other", f.text)

    def test_a_vendored_test_does_not_cover_this_repositorys_requirement(self):
        files = self.changed(**{"tests/test_ui.py": "# REQ1/UI-1 only\n",
                                "vendor/other/tests/test_ui.py": "# REQ2/UI-2\n"})
        f = finding(self.doctor(files), "trace")
        self.assertEqual(f.state, se.WARN, f.text)
        self.assertIn("UI-2", f.text)
        self.assertIn("vendor/other", f.text)

    def test_a_vendored_verdict_does_not_pass_this_repositorys_judge(self):
        req = GOOD["docs/REQUIREMENTS_v2.md"].replace("**UI-2** *(since v2)*", "**UI-2** *(since v2)* *(judged)*")
        self.assertIn("*(judged)*", req)
        files = self.changed(**{"docs/REQUIREMENTS_v2.md": req, "vendor/other/docs/FINDINGS.md":
                                "REQ2/UI-2 verdict: pass, by Someone Else, 2026-10-27\n"})
        f = finding(self.doctor(files), "trace")
        self.assertIn("UI-2 (no verdict yet)", f.text)

    def test_only_the_top_level_is_left_out(self):
        # a nested vendor/ stays loud: a false failure can be read, a file silently unread cannot.
        f = finding(self.doctor(self.changed(**{"src/vendor/x.md": "UI-1 bare\n"})), "citations")
        self.assertEqual(f.state, se.FAIL)

    def test_a_repository_with_nothing_vendored_says_nothing_of_it(self):
        findings = self.doctor()
        self.assertNotIn("left out", finding(findings, "citations").text)
        self.assertNotIn("left out", finding(findings, "trace").text)


class TestDoctorRed(Fixture):
    def test_missing_agents_md(self):
        f = self.doctor(self.changed(**{"AGENTS.md": None, "CLAUDE.md": "# none\n"}))
        self.assertEqual(finding(f, "working agreement").state, se.FAIL)

    def test_copy_behind_the_newest_release(self):
        repo = make_repo(self.tmp.name, self.changed(**{"AGENTS.md": AGENTS_TEXT.replace(AGENTS_LABEL, "v0.9")}))
        rel = {"latest": AGENTS_LABEL, "sha": {}}
        self.assertEqual(se.check_copy(repo, rel).state, se.FAIL)
        self.assertIn("is out", se.check_copy(repo, rel).text)

    def test_patch_release_with_the_same_text_is_current(self):
        repo = make_repo(self.tmp.name)
        rel = {"latest": "v9.9.1", "sha": {"v9.9.1": se.sha256(Path(repo, "AGENTS.md"))}}
        f = se.check_copy(repo, rel)
        self.assertEqual(f.state, se.PASS)
        self.assertIn("same text", f.text)

    def test_edited_copy(self):
        f = self.doctor(self.changed(**{"AGENTS.md": AGENTS_TEXT + "\n- a local rule\n"}))
        self.assertEqual(finding(f, "working agreement").state, se.FAIL)
        self.assertIn("differs", finding(f, "working agreement").text)

    def test_unlabeled_copy(self):
        # REQ1/REL-2: SE1's agreement with its label removed is still SE1's, and is told it has no label
        f = self.doctor(self.changed(**{"AGENTS.md": AGENTS_TEXT.replace(f"This copy is from **{AGENTS_LABEL}**",
                                                                           "This copy is from a release")}))
        self.assertEqual(finding(f, "working agreement").state, se.FAIL)
        self.assertIn("no release label", finding(f, "working agreement").text)

    def test_wrapped_label_is_still_a_label(self):
        # REQ1/REL-2: real copies are wrapped at 100 columns, and the label can break across a line (FINDINGS 2026-10-28)
        wrapped = AGENTS_TEXT.replace(f"This copy is from **{AGENTS_LABEL}**", f"This copy is\nfrom **{AGENTS_LABEL}**")
        repo = make_repo(self.tmp.name, self.changed(**{"AGENTS.md": wrapped}))
        self.assertEqual(se.find_copy(repo)[1], AGENTS_LABEL)
        row = finding(se.doctor(repo, online=False, cache_dir=self.cache.name, today=TODAY), "working agreement")
        self.assertNotIn("no release label", row.text)
        self.assertIn(AGENTS_LABEL, row.text)  # rewrapped is edited, and the row says so by label

    def test_another_guides_agents_md_is_not_a_copy_of_se1s(self):
        # REQ1/REL-2: a sibling guide's agreement carries a label of its own release; it is not SE1's copy
        row = finding(self.doctor(self.changed(**{"AGENTS.md": SIBLING})), "working agreement")
        self.assertEqual(row.state, se.FAIL)
        self.assertIn("not a copy of SE1", row.text)
        self.assertNotIn("v1.0", row.text)  # its label is not compared with SE1's releases

    def test_se1_copy_imported_beside_another_guides_agents_md(self):
        # REQ1/REL-2: the copy CLAUDE.md imports is found past the sibling's file at the root
        f = self.doctor(self.changed(**{"AGENTS.md": SIBLING, "docs/SE1-AGENTS.md": AGENTS_TEXT,
                                        "CLAUDE.md": "# Project\n\n@AGENTS.md\n@docs/SE1-AGENTS.md\n"}))
        self.assertEqual(finding(f, "working agreement").state, se.PASS)
        self.assertEqual(finding(f, "loads at every start").state, se.PASS)

    def test_claude_md_without_import(self):
        f = self.doctor(self.changed(**{"CLAUDE.md": "# Project\n\nno import\n"}))
        self.assertEqual(finding(f, "loads at every start").state, se.FAIL)

    def test_import_from_outside_the_working_directory(self):
        f = self.doctor(self.changed(**{"CLAUDE.md": "@../elsewhere/AGENTS.md\n"}))
        self.assertEqual(finding(f, "loads at every start").state, se.FAIL)
        self.assertIn("outside", finding(f, "loads at every start").text)

    def test_claude_md_excludes_the_copy(self):
        s = json.loads(GOOD[".claude/settings.json"])
        s["claudeMdExcludes"] = ["**/AGENTS.md"]
        f = self.doctor(self.changed(**{".claude/settings.json": json.dumps(s)}))
        self.assertEqual(finding(f, "loads at every start").state, se.FAIL)

    def test_no_claude_md_means_the_fallback(self):
        f = self.doctor(self.changed(**{"CLAUDE.md": None}))
        self.assertEqual(finding(f, "loads at every start").state, se.PASS)
        self.assertIn("by itself", finding(f, "loads at every start").text)

    def test_no_hook_is_none_yet(self):
        f = self.doctor(self.changed(**{".claude/settings.json": None}))
        self.assertEqual(finding(f, "handoff hook").state, se.NONE)

    def test_hook_script_missing(self):
        f = self.doctor(self.changed(**{".claude/settings.json": json.dumps(se.hook_entry("python3 gone.py --post"))}))
        self.assertEqual(finding(f, "handoff hook").state, se.FAIL)

    def test_guide_command_in_a_fenced_block_after_the_label(self):
        guide = "## Check it\n\n- **The full check:**\n\n  ```sh\n  python3 -m unittest && node x.js\n  ```\n\n- `since --check` on a marker edited by hand\n"
        self.assertEqual(se.guide_command(guide), "python3 -m unittest && node x.js")
        f = self.doctor(self.changed(**{"CONTRIBUTING.md": guide, ".github/workflows/check.yml": "jobs:\n  x:\n    steps:\n      - run: python3 -m unittest\n      - run: node x.js\n"}))
        self.assertEqual(finding(f, "CI").state, se.PASS)

    def test_ci_with_a_different_interpreter_name_is_a_second_recipe(self):
        guide = "- **The full check:** `python3 -m unittest`\n"
        f = self.doctor(self.changed(**{"CONTRIBUTING.md": guide, ".github/workflows/check.yml": "jobs:\n  x:\n    steps:\n      - run: python -m unittest\n"}))
        self.assertEqual(finding(f, "CI").state, se.FAIL)

    def test_ci_missing_one_part_of_the_check(self):
        guide = "- **The full check:** `python3 -m unittest && node x.js`\n"
        f = self.doctor(self.changed(**{"CONTRIBUTING.md": guide}))  # the workflow runs only the first part
        self.assertEqual(finding(f, "CI").state, se.FAIL)
        self.assertIn("node x.js", finding(f, "CI").text)

    def test_no_repository_guide(self):
        f = self.doctor(self.changed(**{"CONTRIBUTING.md": None, "CLAUDE.md": "@AGENTS.md\n"}))
        self.assertEqual(finding(f, "repository guide").state, se.NONE)

    def test_readme_alone_names_no_check_command(self):
        # REQ1/SE-1: with no repository guide, a README line that mentions tests beside a path is not the
        # check command; the row says none yet (the fall-2026 course repository, FINDINGS 2026-10-29)
        readme = "# Project\n\n`.github/workflows/ci.yaml` runs lint and tests on Ubuntu, macOS, and Windows.\n"
        f = self.doctor(self.changed(**{"CONTRIBUTING.md": None, "CLAUDE.md": None, "README.md": readme}))
        self.assertEqual(finding(f, "repository guide").state, se.NONE)
        self.assertNotIn("ci.yaml", finding(f, "repository guide").text)

    def test_requirements_without_non_goals(self):
        req = GOOD["docs/REQUIREMENTS_v2.md"].replace("## Non-goals", "## Later")
        f = self.doctor(self.changed(**{"docs/REQUIREMENTS_v2.md": req}))
        self.assertEqual(finding(f, "working set").state, se.FAIL)
        self.assertIn("Non-goals", finding(f, "working set").text)

    def test_no_working_set(self):
        f = self.doctor(self.changed(**{"docs/REQUIREMENTS_v2.md": None, "docs/DESIGN_v1.md": None,
                                        "docs/QUEUE.md": None, "docs/FINDINGS.md": None,
                                        "tests/test_ui.py": "# nothing\n"}))
        self.assertEqual(finding(f, "working set").state, se.NONE)
        self.assertEqual(finding(f, "queue").state, se.NONE)

    def test_working_set_in_another_guides_shape(self):
        # REQ1/SE-1: a docs/ in another guide's layout is named, not reported as if nothing were there (FINDINGS 2026-10-28)
        f = self.doctor(self.changed(**{"docs/REQUIREMENTS_v2.md": None, "docs/DESIGN_v1.md": None,
                                        "docs/QUEUE.md": None, "docs/FINDINGS.md": None, "tests/test_ui.py": "# nothing\n",
                                        "docs/QUESTION_v1.md": "# Question\n", "docs/PLAN_v1.md": "# Plan\n",
                                        "docs/LEDGER.md": "# Ledger\n", "docs/DATASHEET.md": "# Datasheet\n",
                                        "docs/MODEL_CARD.md": "# Model card\n"}))
        row = finding(f, "working set")
        self.assertEqual(row.state, se.NONE)
        self.assertIn("QUESTION_v1", row.text)
        self.assertIn("not SE1's layout", row.text)

    def test_bare_citation(self):
        f = self.doctor(self.changed(**{"tests/test_ui.py": "# UI-1 covered, REQ2/UI-2 covered\n"}))
        self.assertEqual(finding(f, "citations").state, se.FAIL)
        self.assertIn("unversioned", finding(f, "citations").text)

    def test_stale_citation_after_the_requirement_moved(self):
        f = self.doctor(self.changed(**{"tests/test_ui.py": "# REQ1/UI-1 and REQ1/UI-2\n"}))
        self.assertEqual(finding(f, "citations").state, se.FAIL)
        self.assertIn("stale", finding(f, "citations").text)

    def test_a_kept_review_keeps_its_citations(self):
        # SE1/R10: a review is kept as written, so what it quotes cannot be rewritten to the newest version.
        old = "It reads REQ1/UI-2.\n"
        f = self.doctor(self.changed(**{"archive/reviews/REVIEW-v1-other.md": old}))
        self.assertEqual(finding(f, "citations").state, se.PASS)
        f = self.doctor(self.changed(**{"archive/reviews/NOTES.md": old}))
        self.assertEqual(finding(f, "citations").state, se.FAIL)

    def test_a_superseded_design_keeps_its_citations(self):
        # REQ1/SE-1, SE1/R10: DESIGN_v1 cited the requirement as it read then; DESIGN_v2 answers to the newest.
        old = "# Design - v1\n\nThe age (REQ1/UI-2).\n"
        f = self.doctor(self.changed(**{"docs/DESIGN_v1.md": old, "docs/DESIGN_v2.md": "# Design - v2\n"}))
        self.assertEqual(finding(f, "citations").state, se.PASS)
        f = self.doctor(self.changed(**{"docs/DESIGN_v1.md": "# Design - v1\n", "docs/DESIGN_v2.md": old}))
        self.assertEqual(finding(f, "citations").state, se.FAIL)
        self.assertIn("DESIGN_v2.md", finding(f, "citations").text)
        f = self.doctor(self.changed(**{"docs/DESIGN_v1.md": old}))  # the only design is the current one
        self.assertEqual(finding(f, "citations").state, se.FAIL)

    def test_history_cites_the_version_in_force_when_it_was_written(self):
        # REQ1/SE-1, SE1/R10: a FINDINGS entry and a done queue row keep the citation they were written
        # with; rewriting them to the newest version would make them false (PR #1's question, 2026-10-29)
        findings = GOOD["docs/FINDINGS.md"] + "\n## 2026-10-01 — the age\n\n- **What happened:** REQ1/UI-2 was wrong.\n"
        queue = GOOD["docs/QUEUE.md"] + "| 3 | the count (REQ1/UI-2) | done | 2026-10-01 |\n"
        f = self.doctor(self.changed(**{"docs/FINDINGS.md": findings, "docs/QUEUE.md": queue}))
        self.assertEqual(finding(f, "citations").state, se.PASS)

    def test_an_open_queue_row_is_not_history(self):
        # REQ1/SE-1, SE1/R10: a row still to be done cites the current wording, or is stale
        queue = GOOD["docs/QUEUE.md"] + "| 3 | the count (REQ1/UI-2) | ready | 2026-10-01 |\n"
        f = self.doctor(self.changed(**{"docs/QUEUE.md": queue}))
        self.assertEqual(finding(f, "citations").state, se.FAIL)
        self.assertIn("stale", finding(f, "citations").text)

    def test_a_bare_id_inherits_the_version_named_before_it_on_the_line(self):
        # REQ1/SE-1, SE1/R10: list shorthand, `REQ2/UI-1, UI-2`, names one version for both; a bare ID
        # with no versioned citation before it on the line is still unversioned (test_bare_citation)
        f = self.doctor(self.changed(**{"tests/test_ui.py": "# REQ2/UI-1, UI-2 covered\n"}))
        self.assertEqual(finding(f, "citations").state, se.PASS)

    def test_requirement_with_no_test(self):
        f = self.doctor(self.changed(**{"tests/test_ui.py": "# REQ1/UI-1 only\n"}))
        self.assertEqual(finding(f, "trace").state, se.WARN)
        self.assertIn("UI-2", finding(f, "trace").text)

    def test_requirement_named_in_a_cpp_or_module_js_test(self):
        for name in ("tests/test_ui.cpp", "tests/test_ui.cc", "tests/test_ui.hpp", "tests/test_ui.mjs",
                     "tests/test_ui.cjs", "tests/test_ui.tsx", "tests/TestUi.cs", "tests/TestUi.kt"):
            with self.subTest(name=name):
                f = self.doctor(self.changed(**{"tests/test_ui.py": "# REQ1/UI-1 only\n",
                                                name: "// REQ2/UI-2 covered\n"}))
                self.assertEqual(finding(f, "trace").state, se.PASS)

    def test_queue_row_in_progress_too_long(self):
        q = GOOD["docs/QUEUE.md"].replace("2026-10-27", "2026-09-01")
        f = self.doctor(self.changed(**{"docs/QUEUE.md": q}))
        self.assertEqual(finding(f, "queue").state, se.WARN)
        self.assertIn("in progress", finding(f, "queue").text)

    def test_queue_row_blocked_on_nothing(self):
        q = GOOD["docs/QUEUE.md"].replace("blocked: on the client", "blocked")
        f = self.doctor(self.changed(**{"docs/QUEUE.md": q}))
        self.assertEqual(finding(f, "queue").state, se.WARN)
        self.assertIn("on what", finding(f, "queue").text)

    def test_commit_naming_nothing(self):
        f = self.doctor(message="fix stuff")
        self.assertEqual(finding(f, "commits").state, se.WARN)

    def test_ci_runs_a_different_command(self):
        f = self.doctor(self.changed(**{".github/workflows/check.yml": "jobs:\n  x:\n    steps:\n      - run: make\n"}))
        self.assertEqual(finding(f, "CI").state, se.FAIL)

    def test_no_ci(self):
        f = self.doctor(self.changed(**{".github/workflows/check.yml": None}))
        self.assertEqual(finding(f, "CI").state, se.NONE)


class TestReleaseCheck(unittest.TestCase):
    def setUp(self):
        self.cache = tempfile.TemporaryDirectory()
        self.now = dt.datetime(2026, 10, 28, tzinfo=dt.timezone.utc)

    def tearDown(self):
        self.cache.cleanup()

    def test_never_checked_offline_is_stale(self):
        r = se.release_check(online=False, cache_dir=self.cache.name, now=self.now)
        self.assertFalse(r["made"])
        self.assertTrue(r["stale"])
        self.assertIn("never checked", r["note"])

    def test_network_failure_reports_the_age_of_the_last_check(self):
        Path(self.cache.name, "releases.json").write_text(json.dumps(
            {"latest": "v1.1", "sha": {}, "checked_at": "2026-09-01T00:00:00+00:00"}))
        def boom(url):
            raise OSError("no network")
        r = se.release_check(online=True, cache_dir=self.cache.name, fetch=boom, now=self.now)
        self.assertFalse(r["made"])
        self.assertIn("57 days ago", r["note"])
        self.assertTrue(r["stale"])

    def test_recent_cache_is_not_stale(self):
        Path(self.cache.name, "releases.json").write_text(json.dumps(
            {"latest": "v1.1", "sha": {}, "checked_at": "2026-10-26T00:00:00+00:00"}))
        r = se.release_check(online=False, cache_dir=self.cache.name, now=self.now)
        self.assertFalse(r["stale"])
        self.assertIn("2 days ago", r["note"])

    def test_online_check_is_made_and_cached(self):
        agents = b"# AGENTS.md\n"
        def fetch(url):
            if url.endswith("/tags"):
                return json.dumps([{"name": "v1.1"}, {"name": "v1.2"}, {"name": "not-a-release"}]).encode()
            return agents
        r = se.release_check(online=True, cache_dir=self.cache.name, fetch=fetch, now=self.now)
        self.assertTrue(r["made"])
        self.assertEqual(r["latest"], "v1.2")
        self.assertEqual(r["sha"]["v1.2"], hashlib.sha256(agents).hexdigest())
        cached = json.loads(Path(self.cache.name, "releases.json").read_text())
        self.assertEqual(cached["latest"], "v1.2")


class TestPost(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = make_repo(self.tmp.name, {"README.md": "# x\n"}, "chore: start")

    def tearDown(self):
        self.tmp.cleanup()

    def post(self, env, power=("none", None, False), free=100.0, hook=None, transcript=None, sleep=lambda s: None, **kw):
        return se.post(self.repo, hook_input=hook, env=env, power=lambda: power, disk=lambda p: (free, 500.0),
                       transcript=transcript, today=TODAY, now=self.NOW, sleep=sleep, **kw)

    NOW = se.dt.datetime(2026, 11, 2, 20, 45, 44, tzinfo=se.dt.timezone.utc)
    JUST_NOW = "2026-11-02T20:45:43.726Z"

    @staticmethod
    def record(when, pre=431381, post=12837):
        return json.dumps({"type": "system", "timestamp": when,
                           "compactMetadata": {"trigger": "auto", "preTokens": pre, "postTokens": post}}) + "\n"

    def test_a_compaction_not_yet_in_the_transcript_is_not_counted_as_none(self):
        # As seen on the first real compaction (FINDINGS 2026-11-02): the hook ran before the record was there.
        t = Path(self.tmp.name, "t.jsonl")
        t.write_text("")
        lines, verdict = self.post({"TMUX": "1"}, hook={"source": "compact"}, transcript=t)
        self.assertEqual(verdict, "fragile")
        self.assertTrue(lines[0].startswith("YOU WERE COMPACTED just now"))
        self.assertIn("has not recorded it", lines[0])
        for wrong in ("0 time", "None", "? tokens"):
            self.assertNotIn(wrong, lines[0])

    def test_an_earlier_compaction_is_not_reported_as_this_one(self):
        t = Path(self.tmp.name, "t.jsonl")
        t.write_text(self.record("2026-11-02T18:00:00.000Z", pre=999111))
        lines, verdict = self.post({"TMUX": "1"}, hook={"source": "compact"}, transcript=t)
        self.assertIn("1 earlier on record", lines[0])
        self.assertNotIn("999111", lines[0])

    def test_the_hook_waits_briefly_for_the_record(self):
        t = Path(self.tmp.name, "t.jsonl")
        t.write_text("")
        lines, verdict = self.post({"TMUX": "1"}, hook={"source": "compact"}, transcript=t,
                                   sleep=lambda s: t.write_text(self.record(self.JUST_NOW)))
        self.assertTrue(lines[0].startswith("YOU WERE COMPACTED: 1 time"))
        self.assertIn("431381", lines[0])

    def test_a_timestamp_it_cannot_read_is_not_this_compaction(self):
        t = Path(self.tmp.name, "t.jsonl")
        t.write_text(self.record("not a date", pre=999111))
        lines, verdict = self.post({"TMUX": "1"}, hook={"source": "compact"}, transcript=t)
        self.assertNotIn("999111", lines[0])

    def test_after_a_compaction_the_mission_and_shape_come_from_the_source(self):
        # SE1/D9: a summary can lose them. A template's blank and a line left to fill are not printed.
        Path(self.repo, "docs").mkdir(exist_ok=True)
        t = Path(self.tmp.name, "t.jsonl")
        # "Shape" is the heading in documents written before v1.5, which the rename must not silence.
        for heading in ("Fundamental shape", "Fundamental Shape", "Shape"):
            Path(self.repo, "docs/REQUIREMENTS_v1.md").write_text(
                "# R\n\n## Mission\n\n- **AIM-1** *(since v1)* *(judged)* Drivers go straight to a lot.\n"
                f"  Judge: the supervisor. Veto: a thing.\n\n## {heading}\n\nHeld by: Ann.\n\n"
                "- **RULE-1** *(since v1)* *(judged)* _A rule._ Judge: _the holder_.\n- **RULE-2** *(since v1)* One error envelope.\n"
                "- **Says no to:** *to fill.*\n\n## The pain\n\n- not this\n")
            for text in (self.record(self.JUST_NOW), ""):  # recorded yet or not
                with self.subTest(heading=heading, recorded=bool(text)):
                    t.write_text(text)
                    lines, verdict = self.post({"TMUX": "1"}, hook={"source": "compact"}, transcript=t)
                    self.assertIn("the mission and fundamental shape", lines[1])
                    self.assertIn("REQUIREMENTS_v1.md", lines[1])
                    self.assertIn("Drivers go straight to a lot.", lines[2])
                    self.assertNotIn("Judge", lines[2])
                    self.assertIn("One error envelope", lines[3])
                    self.assertFalse(any(x in "\n".join(lines) for x in ("A rule", "to fill", "not this")))

    def test_with_no_mission_nothing_is_said_of_one(self):
        t = Path(self.tmp.name, "t.jsonl")
        t.write_text(self.record(self.JUST_NOW))
        lines, verdict = self.post({"TMUX": "1"}, hook={"source": "compact"}, transcript=t)
        self.assertFalse(any("fundamental shape" in l for l in lines))

    def test_local_terminal_without_a_multiplexer_is_fragile(self):
        lines, verdict = self.post({})
        self.assertEqual(verdict, "fragile")
        self.assertTrue(any("closed lid" in l for l in lines))

    def test_each_multiplexer_is_named(self):
        # Zellij sets ZELLIJ to the string "0": zellij-client/src/lib.rs, read 2026-11-03. Not run under one.
        for env, name in (({"TMUX": "/tmp/t,1,0"}, "tmux"), ({"STY": "1.pts"}, "screen"), ({"ZELLIJ": "0"}, "Zellij")):
            with self.subTest(name=name):
                lines, _ = self.post(env, power=("none", None, None))
                said = "\n".join(lines)
                self.assertIn(f"under a multiplexer ({name})", said)
                self.assertNotIn("run under tmux or screen", said)

    def test_no_multiplexer_names_the_three_it_looks_for(self):
        lines, verdict = self.post({})
        self.assertEqual(verdict, "fragile")
        self.assertIn("no tmux, screen, or Zellij", "\n".join(lines))

    def test_a_multiplexer_is_not_said_to_save_the_session(self):
        # Codex, 2026-11-02: tmux keeps terminal processes; what the runner keeps was never looked at.
        lines, verdict = self.post({"TMUX": "1"})
        said = "\n".join(lines)
        self.assertIn("terminal processes survive", said)
        self.assertIn("what the runner itself keeps is not inspected", said)
        self.assertNotIn("the session survives a dropped", said)

    def test_multiplexer_on_ac_with_room_is_robust(self):
        lines, verdict = self.post({"TMUX": "1"}, power=("ac", 100, True))
        self.assertEqual(verdict, "robust")

    # Cross-platform: what `se --post` reads must exist on Linux, macOS, and Windows, or it says it did not look.
    def test_transcript_size_needs_no_du(self):
        real = se.run
        denied = lambda cmd, **kw: (127, "") if cmd[0] == "du" else real(cmd, **kw)
        with tempfile.TemporaryDirectory() as home:
            (Path(home) / ".claude" / "projects").mkdir(parents=True)
            with mock.patch.object(se.Path, "home", return_value=Path(home)), mock.patch.object(se, "run", denied), \
                    mock.patch.object(se, "tree_bytes", return_value=1.5e9):
                lines, _ = self.post({"TMUX": "1", "CLAUDECODE": "1"})
        self.assertIn("transcripts in ~/.claude/projects: 1.5 GB", "\n".join(lines))

    def test_tree_bytes_adds_every_file_and_gives_up_on_time(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "a" / "b").mkdir(parents=True)
            (Path(d) / "x").write_bytes(b"1" * 10)
            (Path(d) / "a" / "b" / "y").write_bytes(b"2" * 32)
            self.assertEqual(se.tree_bytes(d), 42)
            self.assertIsNone(se.tree_bytes(d, seconds=-1))

    def test_the_real_power_reading_runs_here(self):
        # Real on each of CI's three platforms: not what it reads, which a runner cannot vary, but that it reads.
        src, pct, prevented = se.default_power()
        self.assertIn(src, ("ac", "battery", "none"))
        self.assertIn(prevented, (True, False, None))

    def test_windows_power_status(self):
        self.assertEqual(se.power_windows(0, 8, 40), ("battery", 40, None))
        self.assertEqual(se.power_windows(1, 8, 90), ("ac", 90, None))
        self.assertEqual(se.power_windows(1, 128, 255), ("none", None, None))
        self.assertEqual(se.power_windows(0, 255, 255), ("none", None, None))
        self.assertEqual(se.power_windows(0, 8, 255), ("battery", None, None))

    def power_supply(self, root, name, **files):
        (root / name).mkdir()
        for k, v in files.items():
            (root / name / k).write_text(v + "\n")

    def test_linux_finds_the_battery_by_type_not_by_name(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            self.power_supply(root, "AC", type="Mains")
            self.power_supply(root, "hidpp_battery_0", type="Battery", scope="Device", status="Discharging", capacity="5")
            self.assertEqual(se.power_linux(root, lambda: None), ("none", None, None))
            self.power_supply(root, "CMB0", type="Battery", status="Discharging", capacity="61")
            self.assertEqual(se.power_linux(root, lambda: None), ("battery", 61, None))

    def test_linux_any_discharging_battery_counts(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            self.power_supply(root, "BAT0", type="Battery", status="Not charging", capacity="99")
            self.power_supply(root, "BAT1", type="Battery", status="Discharging", capacity="30")
            self.assertEqual(se.power_linux(root, lambda: True), ("battery", 30, True))
            self.assertEqual(se.power_linux(root / "none", lambda: True), ("none", None, None))

    # The columns as systemd-inhibit printed them here, 2026-11-03, with WHAT wide enough for its longest value.
    INHIBIT_HEAD = "WHO                          UID USER PID COMM            WHAT       WHY                         MODE\n"

    def test_linux_sleep_is_prevented_only_by_a_blocking_sleep_inhibitor(self):
        row = "Someone                      0   root 915 someone         {:<10} {:<27} {}\n\n1 inhibitors listed.\n"
        said = lambda what, why, mode: se.sleep_blocked(self.INHIBIT_HEAD + row.format(what, why, mode))
        self.assertIs(said("sleep", "a job", "block"), True)
        self.assertIs(said("idle:sleep", "a job", "block"), True)
        self.assertIs(said("sleep", "wait for it", "delay"), False)
        self.assertIs(said("shutdown", "no sleep here", "block"), False)
        self.assertIs(se.sleep_blocked("No inhibitors.\n"), False)
        self.assertIs(se.sleep_blocked(""), None)

    def test_not_looking_at_sleep_does_not_say_it_is_not_prevented(self):
        lines, _ = self.post({"TMUX": "1"}, power=("ac", 80, None))
        said = "\n".join(lines)
        self.assertIn("sleep not inspected", said)
        self.assertNotIn("sleep not prevented", said)

    def test_each_platform_is_told_its_own_way_to_stay_awake(self):
        found = lambda name: "/bin/" + name
        self.assertIn("caffeinate", se.stay_awake("darwin", found))
        self.assertIn("systemd-inhibit", se.stay_awake("linux", found))
        self.assertIsNone(se.stay_awake("linux", lambda name: None))
        self.assertIn("power settings", se.stay_awake("win32", found))

    def test_windows_is_not_told_to_run_tmux_as_if_it_had_it(self):
        lines, _ = self.post({}, platform="win32")
        self.assertIn("tmux in WSL", lines[-1])
        lines, _ = self.post({}, platform="linux")
        self.assertIn("run under tmux or screen", lines[-1])

    def test_the_fallback_transcript_folder_can_exist_on_windows(self):
        self.assertEqual(se.project_slug("/home/me/my-repo"), "-home-me-my-repo")
        self.assertEqual(se.project_slug("C:\\Users\\me\\repo"), "C--Users-me-repo")

    def test_the_hook_names_the_python_windows_has(self):
        command = lambda platform: se.hook_entry(platform=platform)["hooks"]["SessionStart"][0]["hooks"][0]["command"]
        self.assertEqual(command("linux"), "python3 se.py --post")
        self.assertEqual(command("win32"), "python se.py --post")

    def test_battery_is_fragile(self):
        lines, verdict = self.post({"TMUX": "1"}, power=("battery", 40, True))
        self.assertEqual(verdict, "fragile")
        self.assertTrue(any("battery (40%)" in l for l in lines))

    def test_low_disk_is_fragile_and_named(self):
        lines, verdict = self.post({"TMUX": "1"}, free=3.0)
        self.assertEqual(verdict, "fragile")
        self.assertTrue(any("disk low" in l for l in lines))

    def test_disk_below_the_floor_is_refused(self):
        lines, verdict = self.post({"TMUX": "1"}, free=0.5)
        self.assertEqual(verdict, "refused")
        self.assertTrue(any("REFUSED" in l for l in lines))

    def test_rules_do_not_tell_an_agent_to_commit(self):
        lines, verdict = self.post({})
        rules = next(l for l in lines if l.startswith("rules for this session"))
        self.assertIn("if you may commit", rules)
        self.assertIn("no commits unless asked", rules)

    def test_another_runner_skips_claude_code_rows(self):
        lines, verdict = self.post({"TMUX": "1", "CI": "1"})
        self.assertTrue(any("not Claude Code" in l for l in lines))
        self.assertFalse(any("idleCompaction" in l for l in lines))

    def test_compaction_is_announced_first(self):
        t = Path(self.tmp.name, "t.jsonl")
        t.write_text(self.record(self.JUST_NOW, pre=300000, post=20000))
        lines, verdict = self.post({"TMUX": "1"}, hook={"source": "compact"}, transcript=t)
        self.assertEqual(verdict, "fragile")
        self.assertTrue(lines[0].startswith("YOU WERE COMPACTED: 1 time"))
        self.assertIn("300000", lines[0])

    def test_torn_state_is_named(self):
        Path(self.repo, "new.txt").write_text("x")
        lines, verdict = self.post({"TMUX": "1"})
        self.assertEqual(verdict, "fragile")
        self.assertTrue(any("torn state" in l for l in lines))


class TestHookAndSelf(unittest.TestCase):
    def test_write_hook_merges_once(self):
        with tempfile.TemporaryDirectory() as tmp:
            path, changed = se.write_hook(tmp, se.hook_entry())
            self.assertTrue(changed)
            path, changed = se.write_hook(tmp, se.hook_entry())
            self.assertFalse(changed)
            s = json.loads(path.read_text())
            self.assertEqual(len(s["hooks"]["SessionStart"]), 1)

    def test_self_check_sees_a_stale_hash(self):
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "guide").mkdir()
            Path(tmp, "AGENTS.md").write_text(f"This copy is from **{se.RELEASE}**;\n")
            saved = se.AGENTS_SHA256
            try:
                se.AGENTS_SHA256 = se.sha256(Path(tmp, "AGENTS.md"))
                self.assertEqual(se.self_check(tmp), [])
                Path(tmp, "AGENTS.md").write_text(f"This copy is from **{se.RELEASE}**; edited\n")
                self.assertTrue(any("stale" in p for p in se.self_check(tmp)))
            finally:
                se.AGENTS_SHA256 = saved

    def test_parse_table(self):
        rows = se.parse_table("| # | Status | Since |\n| - | - | - |\n| 1 | ready | 2026-10-01 |\n")
        self.assertEqual(rows, [{"#": "1", "status": "ready", "since": "2026-10-01"}])


class TestThisRepository(unittest.TestCase):
    def test_its_own_citations_are_versioned(self):
        # SE1/R10: a fixture of mine named real IDs bare, and only the doctor saw it (FINDINGS 2026-11-02).
        repo = Path(__file__).resolve().parents[1]
        req, version, ids = se.latest_requirements(repo)
        row = se.check_citations(repo, req, version, ids)
        self.assertEqual(row.state, se.PASS, row.text)


if __name__ == "__main__":
    unittest.main(verbosity=1)
