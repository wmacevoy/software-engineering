#!/usr/bin/env python3
"""Does a reviewer's isolation hold? One line per fact, for the runner to grade: the file this prints, never
what the reviewer says about it (archive/reviews/REVIEW-METHOD-other-family.md). Standard library only, so it
runs wherever the reviewer does; how the isolation is built is the runner's, and differs by platform.

Outside the isolation, first, as the control:  probe_isolation.py --control --hidden PATH ...
    A path that is empty or misspelled reads as hidden, so each must be seen to have content. Exit 2 if not.
Through the reviewer's real binary, in its working directory:
    probe_isolation.py --hidden PATH ... --outside PATH ... > probe.out
    Exit 0 only when every path is hidden, every write outside is blocked, the network is off, and a write
    in the working directory works. Exit 3 otherwise: run no review."""
import argparse
import os
import socket
import sys
from pathlib import Path


def has_content(path):
    """A path masked with an empty directory or an empty file counts as hidden, as does one refused."""
    try:
        if os.path.isdir(path):
            return bool(os.listdir(path))
        with open(path, "rb") as fh:
            return bool(fh.read(1))
    except OSError:
        return False


def can_write(path):
    """A real attempt, cleaned up. A file already there is not overwritten."""
    try:
        with open(path, "x", encoding="utf8") as fh:
            fh.write("probe\n")
    except OSError:
        return False
    os.unlink(path)
    return True


def network_on(host="github.com", port=443, seconds=8):
    try:
        socket.create_connection((host, port), seconds).close()
        return True
    except OSError:
        return False


def probe(hidden, outside, inside, network=network_on):
    """[(line, as required)], one per fact."""
    facts = []
    for p in hidden:
        seen = has_content(p)
        facts.append((f"hidden {p}: {'VISIBLE' if seen else 'hidden'}", not seen))
    for p in outside:
        there = os.path.exists(p)  # looked at first: a file already there proves nothing about the write
        allowed = can_write(p)
        word = "ALREADY THERE" if there else "ALLOWED" if allowed else "blocked"
        facts.append((f"outside-write {p}: {word}", not there and not allowed))
    on = network()
    facts.append((f"network: {'ON' if on else 'off'}", not on))
    ok = can_write(Path(inside) / ".probe-inside-write")
    facts.append((f"inside-write: {'ok' if ok else 'BLOCKED'}", ok))
    return facts


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--hidden", action="append", default=[], help="must show the reviewer nothing; repeat")
    ap.add_argument("--outside", action="append", default=[], help="a new file the reviewer must not create; repeat")
    ap.add_argument("--control", action="store_true", help="outside the isolation: every --hidden has content")
    args = ap.parse_args(argv)
    if not args.hidden:
        ap.error("name at least one --hidden path: a probe of nothing passes")
    if args.control:
        empty = [p for p in args.hidden if not has_content(p)]
        for p in args.hidden:
            print(f"control {p}: {'NOTHING THERE' if p in empty else 'has content'}")
        return 2 if empty else 0
    if not args.outside:
        ap.error("name at least one --outside path: a probe of nothing passes")
    facts = probe(args.hidden, args.outside, os.getcwd(), network_on)
    for line, _ in facts:
        print(line)
    return 0 if all(ok for _, ok in facts) else 3


if __name__ == "__main__":
    sys.exit(main())
