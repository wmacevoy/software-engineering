#!/usr/bin/env python3
"""Tests for tools/probe_isolation.py: every way out, left open, must turn the probe red (SE1/T3), because a
probe that only ever passes says nothing about the isolation it clears. Run: python3 -I tools/test_probe_isolation.py"""
import contextlib
import importlib.util
import io
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

spec = importlib.util.spec_from_file_location("probe_isolation", Path(__file__).resolve().parent / "probe_isolation.py")
pi = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pi)
OFF, ON = (lambda: False), (lambda: True)


class Probe(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.inside = self.root / "inside"
        self.inside.mkdir()
        self.absent = str(self.root / "absent")
        self.blocked = str(self.root / "no-such-dir" / "file")  # a write here fails, as under isolation

    def facts(self, hidden=None, outside=None, network=OFF):
        return pi.probe(hidden or [self.absent], outside or [self.blocked], self.inside, network)

    def bad(self, facts):
        return [line for line, ok in facts if not ok]

    def test_all_as_required_passes(self):
        self.assertEqual(self.bad(self.facts()), [])

    def test_a_readable_file_is_visible(self):
        f = self.root / "key"
        f.write_text("the answers")
        self.assertIn("VISIBLE", self.bad(self.facts(hidden=[str(f)]))[0])

    def test_a_directory_with_anything_in_it_is_visible(self):
        (self.root / "repo").mkdir()
        (self.root / "repo" / "x").write_text("")
        self.assertIn("VISIBLE", self.bad(self.facts(hidden=[str(self.root / "repo")]))[0])

    def test_a_mask_counts_as_hidden(self):
        (self.root / "emptied").mkdir()
        (self.root / "nulled").write_text("")
        self.assertEqual(self.bad(self.facts(hidden=[str(self.root / "emptied"), str(self.root / "nulled")])), [])

    def test_a_write_that_got_through_is_red_and_cleaned_up(self):
        target = self.root / "outside"
        self.assertIn("ALLOWED", self.bad(self.facts(outside=[str(target)]))[0])
        self.assertFalse(target.exists())

    def test_a_file_already_there_proves_nothing_and_survives(self):
        target = self.root / "outside"
        target.write_text("mine")
        self.assertIn("ALREADY THERE", self.bad(self.facts(outside=[str(target)]))[0])
        self.assertEqual(target.read_text(), "mine")

    def test_the_network_on_is_red(self):
        self.assertEqual(self.bad(self.facts(network=ON)), ["network: ON"])

    def test_no_write_inside_is_red(self):
        # A sandbox that blocks everything would pass every other fact, and no review could be written.
        facts = pi.probe([self.absent], [self.blocked], self.root / "no-such-dir", OFF)
        self.assertEqual(self.bad(facts), ["inside-write: BLOCKED"])

    def run_main(self, *argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out), mock.patch.object(pi, "network_on", OFF):
            return pi.main(list(argv)), out.getvalue()

    def test_exit_codes_say_whether_to_run_the_review(self):
        was = os.getcwd()
        os.chdir(self.inside)
        self.addCleanup(os.chdir, was)
        code, out = self.run_main("--hidden", self.absent, "--outside", self.blocked)
        self.assertEqual(code, 0, out)
        (self.inside / "x").write_text("x")
        code, out = self.run_main("--hidden", str(self.inside), "--outside", self.blocked)
        self.assertEqual(code, 3, out)

    def test_the_control_catches_a_misspelled_path(self):
        # A path that is not there reads as hidden, so a typo would pass: the control is what catches it.
        f = self.root / "key"
        f.write_text("the answers")
        self.assertEqual(self.run_main("--control", "--hidden", str(f))[0], 0)
        code, out = self.run_main("--control", "--hidden", str(f), "--hidden", self.absent)
        self.assertEqual(code, 2)
        self.assertIn("NOTHING THERE", out)

    def test_a_probe_of_nothing_is_refused(self):
        for argv in ([], ["--hidden", self.absent]):
            with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
                pi.main(argv)


if __name__ == "__main__":
    unittest.main()
