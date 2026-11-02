#!/usr/bin/env python3
"""Tests for tools/check.py and tools/since.py: each breakage is planted in a copy of this repository
and must turn the tool red (SE1/T3; REQ1/REL-1, REL-3, ID-3, REQ2/REL-4, CHK-4). Written not to need
editing at a release: it finds the current labels instead of naming them.
Run: python3 -I tools/test_check.py"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

GUIDE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UNKNOWING = "guide/02-unknowing.md"


class Planted(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp()
        cls.repo = os.path.join(cls.tmp, "repo")
        shutil.copytree(GUIDE, cls.repo, ignore=shutil.ignore_patterns("__pycache__", ".claude"))

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

    def tool(self, *args):
        r = subprocess.run([sys.executable, "-I", *args], cwd=self.repo,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return r.returncode, r.stdout.decode("utf-8") + r.stderr.decode("utf-8")

    def red(self, words, tool="tools/check.py", *args):
        rc, out = self.tool(tool, *args)
        self.assertEqual(rc, 1, out)
        self.assertIn(words, out)

    def green(self, tool="tools/check.py", *args):
        rc, out = self.tool(tool, *args)
        self.assertEqual(rc, 0, out)

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

    def test_a_non_ascii_problem_line_can_be_printed(self):
        # Windows' default code page cannot encode this; the tool must report it, not crash.
        self.append("GLOSSARY.md", "\n[\u65e5\u672c\u8a9e](no-such-file.md)\n")
        rc, out = self.tool("tools/check.py")
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


class NoOtherRuntime(unittest.TestCase):
    def test_the_check_names_no_runtime_but_python(self):
        # REQ2/CHK-4: contributing needs Python and git; a Node step would come back here first.
        for name in ("tools/check.sh", ".github/workflows/check.yml"):
            with open(os.path.join(GUIDE, name), encoding="utf-8") as fh:
                self.assertNotRegex(fh.read(), r"(?i)\bnode\b|setup-node|\bnpm\b", name)


if __name__ == "__main__":
    unittest.main()
