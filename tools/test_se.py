#!/usr/bin/env python3
"""Tests for se.py: every doctor check is seen to fail on a fixture built to fail it (SE1/T3), the self
test's verdicts follow from the signals its providers are given, and the release check says how stale
it is. Run: python3 -I tools/test_se.py. Standard library only; no network, no wall clock, no shared
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
        f = self.doctor(self.changed(**{"AGENTS.md": "# AGENTS.md\n\nno label here\n"}))
        self.assertEqual(finding(f, "working agreement").state, se.FAIL)

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

    def test_bare_citation(self):
        f = self.doctor(self.changed(**{"tests/test_ui.py": "# UI-1 covered, REQ2/UI-2 covered\n"}))
        self.assertEqual(finding(f, "citations").state, se.FAIL)
        self.assertIn("unversioned", finding(f, "citations").text)

    def test_stale_citation_after_the_requirement_moved(self):
        f = self.doctor(self.changed(**{"tests/test_ui.py": "# REQ1/UI-1 and REQ1/UI-2\n"}))
        self.assertEqual(finding(f, "citations").state, se.FAIL)
        self.assertIn("stale", finding(f, "citations").text)

    def test_requirement_with_no_test(self):
        f = self.doctor(self.changed(**{"tests/test_ui.py": "# REQ1/UI-1 only\n"}))
        self.assertEqual(finding(f, "trace").state, se.WARN)
        self.assertIn("UI-2", finding(f, "trace").text)

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

    def post(self, env, power=("none", None, False), free=100.0, hook=None, transcript=None):
        return se.post(self.repo, hook_input=hook, env=env, power=lambda: power,
                       disk=lambda p: (free, 500.0), transcript=transcript, today=TODAY)

    def test_local_terminal_without_a_multiplexer_is_fragile(self):
        lines, verdict = self.post({})
        self.assertEqual(verdict, "fragile")
        self.assertTrue(any("closed lid" in l for l in lines))

    def test_multiplexer_on_ac_with_room_is_robust(self):
        lines, verdict = self.post({"TMUX": "1"}, power=("ac", 100, True))
        self.assertEqual(verdict, "robust")

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
        t.write_text(json.dumps({"type": "user", "compactMetadata": {"trigger": "auto", "preTokens": 300000, "postTokens": 20000}}) + "\n")
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


if __name__ == "__main__":
    unittest.main(verbosity=1)
