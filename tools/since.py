#!/usr/bin/env python3
"""A since for every principle, mined from git: the release at which its current text first appeared
and that release's date, written as the marker under the heading. A hand-made marker drifts and
says nothing for a principle nobody touched; this one is recomputed from the tags and checked, so
a principle that reads as unchanged says since when (SE1/U7: make it age visibly).
Usage: python3 tools/since.py            print the expected marker for every principle
       python3 tools/since.py --write    write them into the chapters
       python3 tools/since.py --check    exit 1 where a chapter's marker differs from git's answer
       python3 tools/since.py --write --as v1.4   treat the working tree as release v1.4, dated today,
                                         so the release commit carries dated markers before its tag
A New/Changed kind is a person's claim about meaning and is kept as written; this tool adds the
release's date and, when the wording moved later without the meaning, "text since". A principle
changed after the newest tag gets the unreleased section's name from CHANGELOG.md; the checker
still demands a New/Changed claim or an *Also changed* line for it. Needs the release tags."""
import datetime
import os
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # Windows' default code page cannot print every link
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # beside this file, even under -I
from bodies import HEADING, MARKER, bodies, read  # noqa: E402

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def git(*args):
    r = subprocess.run(["git", "-C", root, *args], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    return r.stdout.decode("utf-8") if r.returncode == 0 else None


def version_key(v):
    x = [int(n) for n in v[1:].split(".")]
    return (x[0], x[1], x[2] if len(x) > 2 else 0)


tags = sorted((t for t in (git("tag", "--list", "v*") or "").split("\n")
               if re.search(r"^v[0-9]+\.[0-9]+(\.[0-9]+)?$", t)), key=version_key)
if not tags:
    print("since: no release tags here (git fetch --tags)", file=sys.stderr)
    sys.exit(2)
date_of = {t: (git("log", "-1", "--format=%cs", t) or "").strip() for t in tags}
argv = sys.argv[1:]
as_release = argv[argv.index("--as") + 1] if "--as" in argv and argv.index("--as") + 1 < len(argv) else None
if "--as" in argv:  # a release being made: the working tree is it
    if not as_release or not re.search(r"^v[0-9]+\.[0-9]+(\.[0-9]+)?$", as_release):
        print("since: --as needs a release like v1.4", file=sys.stderr)
        sys.exit(2)
    if as_release not in tags:
        tags.append(as_release)
    date_of[as_release] = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
top = re.search(r"^## (v[0-9]+\.[0-9]+(?:\.[0-9]+)?) — unreleased$", read(os.path.join(root, "CHANGELOG.md")), re.M)
unreleased = top.group(1) if top else "unreleased"
mode = "write" if "--write" in argv else "check" if "--check" in argv else "print"
named = [a for i, a in enumerate(argv) if not a.startswith("--") and (i == 0 or argv[i - 1] != "--as")]
guide = os.path.join(root, "guide")
chapters = ([os.path.normpath(os.path.join(root, f)) for f in named] if named else
            [os.path.join(guide, n) for n in sorted(os.listdir(guide)) if re.search(r"^[0-9][0-9]-.*\.md$", n)])

problems, written = 0, 0
for path in chapters:
    rel = os.path.relpath(path, root).replace(os.sep, "/")
    text = read(path)
    lines = text.split("\n")
    now = bodies(text)
    at = {t: now if t == as_release else bodies(git("show", f"{t}:{rel}") or "") for t in tags}
    expected = []
    for pid, body in now.items():
        # The text's since: the oldest tag from which the body has equalled today's in an unbroken run.
        since = None
        for t in reversed(tags):
            if at[t].get(pid) != body:
                break
            since = t
        text_since = (since, date_of[since]) if since else (unreleased, "unreleased")
        index = next(i for i, l in enumerate(lines) if (lambda m: m and m.group(2) == pid)(HEADING.search(l)))
        mk = MARKER.search(lines[index + 2]) if index + 2 < len(lines) else None
        human = (mk.group(1), mk.group(2)) if mk and mk.group(1) != "Since" else None
        if human:
            d = date_of[human[1]] if human[1] in tags else "unreleased"
            extra = f"; text since {text_since[0]} ({text_since[1]})" if text_since[0] != human[1] else ""
            line = f"*{human[0]} in {human[1]} ({d}){extra}.*"
        else:
            line = f"*Since {text_since[0]} ({text_since[1]}).*"
        expected.append((pid, line, index, bool(mk)))
    if mode == "print":
        for pid, line, _, _ in expected:
            print(f"{rel}\t{pid}\t{line}")
    if mode == "check":
        for pid, line, index, has in expected:
            actual = lines[index + 2] if has else "(no marker)"
            if actual != line:
                problems += 1
                print(f"{rel} {pid}: marker is {actual}; git says {line}")
    if mode == "write":
        for pid, line, index, has in sorted(expected, key=lambda e: -e[2]):  # from the bottom, so indices hold
            if has:
                if lines[index + 2] != line:
                    lines[index + 2] = line
                    written += 1
            else:
                lines[index + 1:index + 1] = ["", line]
                written += 1
        with open(path, "w", encoding="utf-8", newline="") as fh:
            fh.write("\n".join(lines))
if mode == "check":
    print(f"{len(chapters)} chapters, {problems} marker(s) differ from git")
    sys.exit(1 if problems else 0)
if mode == "write":
    print(f"{written} marker(s) written")
