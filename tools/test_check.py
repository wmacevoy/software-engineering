#!/usr/bin/env python3
"""Tests for tools/check.py and tools/since.py: each breakage is planted in a copy of this repository
and must turn the tool red (SE1/T3; REQ1/REL-1, REL-3, ID-3, REQ2/REL-4, CHK-4). Written not to need
editing at a release: it finds the current labels instead of naming them.
Run: python3 -I tools/test_check.py"""
import datetime
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

GUIDE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UNKNOWING = "guide/02-unknowing.md"


class Repo(unittest.TestCase):
    """A copy of this repository to plant breakages in, each undone after its test."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp()
        cls.repo = os.path.join(cls.tmp, "repo")
        shutil.copytree(GUIDE, cls.repo, ignore=shutil.ignore_patterns("__pycache__", ".claude"))
        # On a release commit before its tag, these tests would each see that one release's markers as unnamed. The
        # copy is tagged as it will be; `since --check` on the real tree is what covers the untagged state.
        with open(os.path.join(cls.repo, "CHANGELOG.md"), encoding="utf-8") as fh:
            top = re.search(r"^## (v[0-9.]+) — [0-9-]+$", fh.read(), re.M)
        if top:
            subprocess.run(["git", "-C", cls.repo, "tag", top.group(1)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def setUp(self):
        self.saved = {}

    def tearDown(self):
        for name, text in self.saved.items():
            self.write(name, text)

    def read(self, name):
        with open(os.path.join(self.repo, name), encoding="utf-8", newline="") as fh:
            return fh.read()

    def write(self, name, text):
        with open(os.path.join(self.repo, name), "w", encoding="utf-8", newline="") as fh:
            fh.write(text)

    def plant(self, name, change):
        before = self.read(name)
        self.saved.setdefault(name, before)
        after = change(before)
        self.assertNotEqual(before, after, f"the breakage did not land in {name}")
        self.write(name, after)

    def append(self, name, text):
        self.plant(name, lambda t: t + text)

    def tool(self, *args, env=None, isolated=True):  # -I ignores PYTHONIOENCODING, so a test of it runs without
        r = subprocess.run([sys.executable, *(["-I"] if isolated else []), *args], cwd=self.repo, env=env,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return r.returncode, r.stdout.decode("utf-8") + r.stderr.decode("utf-8")

    def red(self, words, tool="tools/check.py", *args):
        rc, out = self.tool(tool, *args)
        self.assertEqual(rc, 1, out)
        self.assertIn(words, out)

    def green(self, tool="tools/check.py", *args):
        rc, out = self.tool(tool, *args)
        self.assertEqual(rc, 0, out)


class Planted(Repo):
    def test_the_tree_itself_is_green(self):
        self.green()
        self.green("tools/since.py", "--check")

    def test_copy_mislabeled(self):
        self.plant("AGENTS.md", lambda t: re.sub(r"This copy is from \*\*v\d+\.\d+\*\*", "This copy is from **v0.1**", t))
        self.red("stale release  AGENTS.md")

    def test_template_links_another_release(self):
        self.plant("templates/QUEUE.md", lambda t: re.sub(r"blob/v\d+\.\d+/", "blob/v1.0/", t, count=1))
        self.red("stale release  templates/QUEUE.md")

    def test_principle_reworded_with_no_marker(self):
        self.plant(UNKNOWING, lambda t: t.replace("K0 costs nothing", "K0 costs little", 1))
        self.red("unacknowledged U1")

    def test_rewrapping_is_not_a_change(self):
        self.plant(UNKNOWING, lambda t: t.replace("K0 costs nothing; you", "K0 costs nothing;\nyou", 1))
        self.green()

    def test_rule_inserted_inside_a_body(self):
        self.plant(UNKNOWING, lambda t: t.replace("K0 costs nothing", "---\n\nK0 costs nothing", 1))
        self.red("unacknowledged U1")

    def test_index_line_dropped(self):
        self.plant("README.md", lambda t: re.sub(r"- \[\*\*SE1/U1\*\*\][^\n]*\n", "", t, count=1))
        self.red("README index out of date")

    def test_broken_link_and_anchor(self):
        self.append("GLOSSARY.md", "\n[x](no-such-file.md)\n")
        self.red("missing file")
        self.tearDown()
        self.saved = {}
        self.append("GLOSSARY.md", "\n[x](README.md#no-such-anchor)\n")
        self.red("missing anchor")

    def test_template_cites_an_id_its_release_lacks(self):
        self.append("templates/QUEUE.md", "\nSE1/Z9\n")
        self.red("ahead of label")

    def test_citations(self):
        for text, words in (("[U1](guide/02-unknowing.md#u1)", "unversioned"),
                            ("[SE1/U1](guide/03-feedback.md#f1)", "wrong file"),
                            ("(SE2/U1)", "wrong version"),
                            ("(SE1/U1, SE1/U99)", "unknown ID"),
                            ("(SE1/U1,\u00a0SE1/U99)", "unknown ID")):  # a list may wrap on any whitespace
            with self.subTest(text):
                self.append("GLOSSARY.md", f"\n{text}\n")
                self.red(words)
                self.tearDown()
                self.saved = {}

    def test_new_principle_needs_a_changelog_entry(self):
        self.plant("guide/03-feedback.md", lambda t: t.replace(
            "\n\n---\n", '\n\n### <a id="f99"></a>F99. Planted\n\nText.\n\n---\n', 1))
        self.red("A new principle is missing from CHANGELOG.md")

    def test_heading_slugs_outside_ascii(self):
        # Python's re has no \p{L}: an anchor must keep letters and digits of every script and drop the rest.
        self.append("GLOSSARY.md", "\n## Caf\u00e9 \u2014 \u65e5\u672c\u8a9e x_y A&B\n\n[a](#caf\u00e9--\u65e5\u672c\u8a9e-x_y-ab)\n")
        self.green()
        self.tearDown()
        self.saved = {}
        self.append("GLOSSARY.md", "\n## Caf\u00e9 \u2014 \u65e5\u672c\u8a9e x_y A&B\n\n[a](#cafe)\n")
        self.red("missing anchor")

    def test_heading_slugs_trim_every_whitespace(self):
        # A byte-order mark is whitespace here, as U+0085 is not; Python's own strip() has them backwards.
        self.append("GLOSSARY.md", "\n## \ufeffzed\n\n[a](#zed)\n")
        self.green()

    def test_a_non_ascii_problem_line_can_be_printed(self):
        # Windows' default code page cannot encode this; the tool must report it, not crash.
        self.append("GLOSSARY.md", "\n[\u65e5\u672c\u8a9e](no-such-file.md)\n")
        rc, out = self.tool("tools/check.py", env=dict(os.environ, PYTHONIOENCODING="ascii"), isolated=False)
        self.assertEqual(rc, 1, out)
        self.assertIn("\u65e5\u672c\u8a9e", out)
        self.assertNotIn("Traceback", out)

    def test_marker_edited_by_hand(self):
        self.plant(UNKNOWING, lambda t: re.sub(r"\*Since v\d+\.\d+ \(", "*Since v0.9 (", t, count=1))
        self.red("marker(s) differ from git", "tools/since.py", "--check")

    def test_since_writes_what_it_checks(self):
        marker = re.compile(r"\*Since v\d+\.\d+(\.\d+)? \([^)]*\)\.\*\n\n", re.M)
        self.plant(UNKNOWING, lambda t: marker.sub("", t, count=1))
        rc, out = self.tool("tools/since.py", "--write")
        self.assertEqual(rc, 0, out)
        self.green("tools/since.py", "--check")

    # SE1/U7: a marker names a release. With no release to name, --write refuses and touches nothing.
    NO_SECTION = staticmethod(lambda t: re.sub(r"^(## v[0-9.]+ — )unreleased$", r"\g<1>2026-01-01", t, flags=re.M))
    SECTION = staticmethod(lambda t: t.replace("\n## v", "\n## v9.9 — unreleased\n\n## v", 1))
    U1_CLAIMS_V9_9 = staticmethod(lambda t: re.sub(
        r'(<a id="u1"></a>[^\n]*\n\n)\*[^\n]*\*\n', r"\1*Changed in v9.9 (2026-01-01).*\n", t, count=1))
    FEEDBACK = "guide/03-feedback.md"

    def no_section(self):  # written not to need editing at a release: there may or may not be a section today
        self.saved.setdefault("CHANGELOG.md", self.read("CHANGELOG.md"))
        self.write("CHANGELOG.md", self.NO_SECTION(self.read("CHANGELOG.md")))

    def test_since_refuses_a_change_with_no_section_to_name_it(self):
        # Two chapters, the writable one first: one chapter's refusal must stop the others too.
        self.no_section()
        marker = re.compile(r"\*Since v\d+\.\d+(\.\d+)? \([^)]*\)\.\*\n\n", re.M)
        self.plant(UNKNOWING, lambda t: marker.sub("", t, count=1))
        self.plant(self.FEEDBACK, lambda t: re.sub(r'(<a id="f1"></a>[^\n]*\n\n\*[^\n]*\*\n\n)', r"\1Planted. ", t, count=1))
        before = self.read(UNKNOWING), self.read(self.FEEDBACK)
        rc, out = self.tool("tools/since.py", "--write")
        self.assertEqual(rc, 2, out)
        self.assertIn("F1", out)
        self.assertIn("## vX.Y — unreleased", out)
        self.assertIn("--as", out)
        self.assertEqual(before, (self.read(UNKNOWING), self.read(self.FEEDBACK)), "--write refused, yet wrote")

    def test_since_refuses_a_marker_naming_no_release(self):
        # A release commit before its tag, without --as: the claim names a release git does not have yet.
        self.no_section()
        self.plant(UNKNOWING, self.U1_CLAIMS_V9_9)
        before = self.read(UNKNOWING)
        rc, out = self.tool("tools/since.py", "--write")
        self.assertEqual(rc, 2, out)
        self.assertIn("U1", out)
        self.assertIn("v9.9", out)
        self.assertEqual(before, self.read(UNKNOWING), "--write refused, yet wrote")

    def test_since_refuses_in_utf8_whatever_the_code_page(self):
        # Windows with Python 3.9 wrote the refusal's em dash to stderr as cp1252 (FINDINGS 2026-11-02).
        self.no_section()
        self.plant(UNKNOWING, self.U1_CLAIMS_V9_9)
        rc, out = self.tool("tools/since.py", "--write", env=dict(os.environ, PYTHONIOENCODING="cp1252"), isolated=False)
        self.assertEqual(rc, 2, out)
        self.assertIn("## vX.Y \u2014 unreleased", out)

    def test_since_check_says_why_it_has_no_release_to_name(self):
        self.no_section()
        self.plant(UNKNOWING, self.U1_CLAIMS_V9_9)
        self.red("## vX.Y — unreleased", "tools/since.py", "--check")

    def test_since_check_passes_a_release_commit_before_its_tag(self):
        # So CI can pass on the very commit that gets tagged (FINDINGS 2026-11-04). The top section becomes the release
        # being made, dated today, as a release commit does: a made-up one above a tagged section, or today's unreleased one.
        today = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
        top = re.search(r"^## (v[0-9.]+) — (\S+)$", self.read("CHANGELOG.md"), re.M)
        name = top.group(1) if top.group(2) == "unreleased" else "v9.9"
        heading = f"## {name} — {today}"
        self.plant("CHANGELOG.md", lambda t: t.replace(top.group(0), heading if name == top.group(1) else f"{heading}\n\n{top.group(0)}", 1))
        self.plant(UNKNOWING, lambda t: self.U1_CLAIMS_V9_9(t).replace("Changed in v9.9", f"Changed in {name}", 1))
        self.plant(UNKNOWING, lambda t: t.replace("K0 costs nothing", "K0 costs little", 1))
        rc, out = self.tool("tools/since.py", "--write")  # --write is not eased: the release commit names itself with --as
        self.assertEqual(rc, 2, out)
        self.assertIn("--as", out)
        rc, out = self.tool("tools/since.py", "--write", "--as", name)
        self.assertEqual(rc, 0, out)
        rc, out = self.tool("tools/since.py", "--check")
        self.assertEqual(rc, 0, out)
        self.assertIn(f"{name} is dated in CHANGELOG.md and has no tag yet", out)
        # Still a check: a marker that is wrong stays red.
        self.plant(UNKNOWING, lambda t: t.replace(f"*Changed in {name} ({today})", f"*Changed in {name} (2001-01-01)", 1))
        self.red("marker(s) differ from git", "tools/since.py", "--check")

    def test_since_check_takes_only_a_dated_newer_section_as_the_release_being_made(self):
        self.no_section()
        for heading in ("## v9.9 — unreleased", "## v0.1 — 2026-01-01"):
            with self.subTest(heading=heading):
                self.write("CHANGELOG.md", self.NO_SECTION(self.saved["CHANGELOG.md"]).replace("\n## v", f"\n{heading}\n\n## v", 1))
                rc, out = self.tool("tools/since.py", "--check")
                self.assertNotIn("has no tag yet", out)

    def test_since_as_names_the_release_being_made(self):
        self.plant(UNKNOWING, self.U1_CLAIMS_V9_9)
        rc, out = self.tool("tools/since.py", "--write", "--as", "v9.9")
        self.assertEqual(rc, 0, out)
        self.assertNotIn("unreleased", re.search(r'<a id="u1"></a>[^\n]*\n\n(\*[^\n]*\*)', self.read(UNKNOWING)).group(1))

    def test_since_names_the_unreleased_section(self):
        # The real section when there is one: a principle new in it must stay named, so a second section would refuse.
        found = re.search(r"^## (v[0-9.]+) — unreleased$", self.read("CHANGELOG.md"), re.M)
        name = found.group(1) if found else "v9.9"
        if not found:
            self.plant("CHANGELOG.md", self.SECTION)
        self.plant(UNKNOWING, lambda t: self.U1_CLAIMS_V9_9(t).replace("Changed in v9.9", f"Changed in {name}", 1))
        self.plant(UNKNOWING, lambda t: t.replace("K0 costs nothing", "K0 costs little", 1))
        self.plant(self.FEEDBACK, lambda t: re.sub(r'(<a id="f1"></a>[^\n]*\n\n\*[^\n]*\*\n\n)', r"\1Planted. ", t, count=1))
        rc, out = self.tool("tools/since.py", "--write")
        self.assertEqual(rc, 0, out)
        self.assertIn(f"*Changed in {name} (unreleased).*", self.read(UNKNOWING))
        self.assertIn(f"*Since {name} (unreleased).*", self.read(self.FEEDBACK))
        self.green("tools/since.py", "--check")


class EveryReport(Repo):
    """One breakage per line the checker can report that the tests above do not reach. This
    file's claim, a breakage per rule, was measured: remove any one report from check.py and a test must fail."""

    GLOSSARY = "GLOSSARY.md"
    FEEDBACK = "guide/03-feedback.md"
    ROW = "- [SE1/{}](guide/02-unknowing.md#u1) x\n\n"

    def marker(self, text):
        self.plant(UNKNOWING, lambda t: re.sub(
            r'(<a id="u1"></a>[^\n]*\n\n)\*[^\n]*\*\n', lambda m: m.group(1) + text + "\n", t, count=1))

    def top_release(self, section):
        self.plant("CHANGELOG.md", lambda t: re.sub(
            r"^## v", "## v9.9 \u2014 unreleased\n\n" + section + "## v", t, count=1, flags=re.M))

    def cases(self):
        glossary = lambda text: lambda: self.append(self.GLOSSARY, f"\n{text}\n")
        llms = lambda text: lambda: self.append("llms.txt", f"\n{text}\n")
        raw = "https://raw.githubusercontent.com/wmacevoy/software-engineering/main/"
        undated = re.compile(r"^(## v\S+) \u2014 [0-9]{4}-[0-9]{2}-[0-9]{2}$", re.M)
        return {
            "defined twice": lambda: self.append(self.FEEDBACK, '\n### <a id="dup"></a>U1. Planted\n\nText.\n'),
            "unknown ref": glossary("[x](https://github.com/wmacevoy/software-engineering/blob/v0.0/README.md)"),
            "wrong version  GLOSSARY.md: [SE2": glossary("[SE2/U1](guide/02-unknowing.md#u1)"),
            "unknown ID     GLOSSARY.md: [SE1": glossary("[SE1/U99](guide/02-unknowing.md#u1)"),
            "wrong version  GLOSSARY.md: (SE2": glossary("(SE2/U1)"),
            "unknown ID     GLOSSARY.md: (SE1": glossary("(SE1/U99)"),
            "unversioned    GLOSSARY.md: (U1": glossary("(U1)"),
            "README index lists a principle no heading has": lambda: self.append("README.md", "\n- [**SE1/U1**](guide/02-unknowing.md#u1) A contradictory title\n"),
            "README index lists this twice": lambda: self.append("README.md", "\n" + re.search(r"^- \[\*\*SE1/U1\*\*\].*$", self.read("README.md"), re.M).group(0) + "\n"),
            "title number": lambda: self.plant(self.FEEDBACK, lambda t: t.replace("# 3. ", "# 4. ", 1)),
            "chapter label": glossary("[3. Planted](guide/03-feedback.md)"),
            "not a raw link": llms("[x](https://example.com/a)"),
            "missing file   llms.txt": llms(f"[x]({raw}no-such-file.md)"),
            "CHANGELOG.md has no": lambda: self.plant("CHANGELOG.md", lambda t: undated.sub(lambda m: m.group(1) + " \u2014 unreleased", t)),
            "unknown release U1": lambda: self.marker("*Since v7.7 (2026-10-20).*"),
            "not in CHANGELOG U1": lambda: self.marker("*Changed in v1.1 (2026-10-20).*"),
            "unknown ID     CHANGELOG.md v9.9 New: U99": lambda: self.top_release("### New\n\n" + self.ROW.format("U99")),
            "no marker      U1": lambda: self.top_release("### Changed\n\n" + self.ROW.format("U1")),
        }

    def test_each_report_can_fire(self):
        for words, plant in self.cases().items():
            with self.subTest(words):
                plant()
                self.red(words)
                self.tearDown()
                self.saved = {}


class PlantedInHistory(Repo):
    """Breakages that need the tags or the CHANGELOG's shape. A made-up v9.9 keeps these true at any release."""

    def setUp(self):
        super().setUp()
        self.made, self.removed = [], []

    def tearDown(self):
        super().tearDown()
        for tag in self.made:
            self.git("tag", "-d", tag)
        for tag, sha in self.removed:
            self.git("tag", tag, sha)

    def git(self, *args):
        r = subprocess.run(["git", "-C", self.repo, *args], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        return r.stdout.decode("utf-8").strip()

    def tag(self, name, at="HEAD"):
        self.git("tag", name, at)
        self.made.append(name)

    def tags(self):
        return self.git("tag", "--list", "v*").split()

    def release(self, heading, body=""):
        self.plant("CHANGELOG.md", lambda t: re.sub(r"^## v", f"{heading}\n\n{body}## v", t, count=1, flags=re.M))

    def test_no_tags_at_all(self):
        self.removed = [(t, self.git("rev-parse", t)) for t in self.tags()]
        for tag, _ in self.removed:
            self.git("tag", "-d", tag)
        self.red("no release tag")

    def test_a_patch_may_not_list_principles(self):
        self.release("## v9.9.1 \u2014 2026-01-01", "### New\n\n- [SE1/U1](guide/02-unknowing.md#u1) x\n\n")
        self.red("patch release  v9.9.1 lists principles under New")

    def test_a_patch_needs_its_minors_tag(self):
        self.release("## v9.9.1 \u2014 2026-01-01")
        self.red("needs its minor's tag v9.9")

    def test_a_patch_may_not_change_a_copy_or_a_principle(self):
        self.tag("v9.9")
        self.release("## v9.9.1 \u2014 2026-01-01")
        self.append("AGENTS.md", "\nplanted\n")
        self.plant(UNKNOWING, lambda t: t.replace("K0 costs nothing", "K0 costs little", 1))
        rc, out = self.tool("tools/check.py")
        self.assertEqual(rc, 1, out)
        self.assertIn("patch release  v9.9.1 changed AGENTS.md", out)
        self.assertIn("patch release  v9.9.1 changed U1", out)

    def test_a_minor_is_not_held_to_a_patchs_rules(self):
        self.tag("v9.9")
        self.release("## v9.9 \u2014 2026-01-01")
        self.append("AGENTS.md", "\nplanted\n")
        rc, out = self.tool("tools/check.py")
        self.assertNotIn("patch release", out)

    def test_a_since_marker_does_not_acknowledge_a_change(self):
        self.plant(UNKNOWING, lambda t: re.sub(r"K0 costs nothing", "K0 costs little", t, count=1))
        self.plant(UNKNOWING, lambda t: re.sub(
            r'(<a id="u1"></a>[^\n]*\n\n)\*[^\n]*\*\n', r"\1*Since v9.9 (2026-01-01).*\n", t, count=1))
        self.red("unacknowledged U1")

    def test_a_heading_ends_a_principle(self):
        self.plant("guide/03-feedback.md", lambda t: t.replace("\n\n---\n\nNext:", "\n\n## Aside\n\nNot F5's text.\n\n---\n\nNext:", 1))
        self.green()

    def test_v1_10_sorts_after_v1_9(self):
        self.tag("v1.9", self.git("rev-list", "--max-parents=0", "HEAD").split()[0])
        # Commit in the copy: a contributor runs this with uncommitted edits, and the tag must hold U10's text.
        self.git("add", "-A")
        self.git("-c", "user.name=test", "-c", "user.email=test@example.com", "commit", "-q", "--allow-empty", "-m", "planted")
        self.tag("v1.10")
        rc, out = self.tool("tools/since.py", UNKNOWING)
        self.assertEqual(rc, 0, out)
        self.assertRegex(out, r"U10\t[^\n]*since v1\.10|U10\t\*Since v1\.10")


class NoOtherRuntime(unittest.TestCase):
    """REQ2/CHK-4: contributing needs Python and git. These allow what is used, so any other runtime is refused,
    not only Node, the one that used to be here (Codex, 2026-11-02: ruby passed the first version of this)."""
    SCRIPT = re.compile(r"""(?:set -e|cd "|py=\$\(command -v python3|"\$py" )""")
    ACTION = re.compile(r"actions/(?:checkout|setup-python)@")
    RUN = re.compile(r"(?:sh tools/check\.sh|\./se --version|\./se\.ps1 --version)$")

    def script_lines_outside(self, text):
        lines = [l.strip() for l in text.splitlines() if l.strip() and not l.lstrip().startswith("#")]
        return [l for l in lines if not self.SCRIPT.match(l)]

    def workflow_lines_outside(self, text):
        out = []
        for line in text.splitlines():
            step = re.match(r"\s*(?:- )?(uses|run):\s*(.*)", line)
            if step and not (self.ACTION if step.group(1) == "uses" else self.RUN).match(step.group(2)):
                out.append(line.strip())
        return out

    def source(self, name):
        with open(os.path.join(GUIDE, name), encoding="utf-8") as fh:
            return fh.read()

    def test_the_check_names_no_runtime_but_python(self):
        self.assertEqual(self.script_lines_outside(self.source("tools/check.sh")), [])
        self.assertEqual(self.workflow_lines_outside(self.source(".github/workflows/check.yml")), [])

    def test_another_runtime_would_be_refused(self):
        self.assertEqual(self.script_lines_outside("#!/bin/sh\nruby tools/check.rb\n"), ["ruby tools/check.rb"])
        self.assertEqual(self.workflow_lines_outside("      - uses: actions/setup-node@v4\n        run: npm test\n"),
                         ["- uses: actions/setup-node@v4", "run: npm test"])


if __name__ == "__main__":
    unittest.main()
