#!/usr/bin/env python3
"""QUICKREF.md is extracted from the `> **Quick:**` line of every principle, so it has one source.

   python3 tools/quickref.py --write   write it
   python3 tools/quickref.py --check   exit 1 if it differs from what the guide says
"""
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bodies import HEADING, QUICK, read  # noqa: E402

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OPENER = read(os.path.join(root, "tools", "quickref-opener.md")).rstrip("\n")

out = [OPENER, ""]
for path in sorted(glob.glob(os.path.join(root, "guide", "*.md"))):
    lines = read(path).split("\n")
    out += [f"#{lines[0]}", ""]
    current = None
    for line in lines:
        m = HEADING.search(line)
        if m:
            current = m.group(2)
        q = QUICK.search(line)
        if q and current:
            out.append(f"- **SE1/{current}** {q.group(1)}")
            current = None
    out.append("")
text = "\n".join(out).rstrip("\n") + "\n"

target = os.path.join(root, "QUICKREF.md")
if "--write" in sys.argv:
    with open(target, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)
elif "--check" in sys.argv:
    have = read(target) if os.path.exists(target) else ""
    if have.replace("\r\n", "\n") != text:
        print("QUICKREF.md differs from the guide's Quick lines: run python3 tools/quickref.py --write")
        sys.exit(1)
    print(f"QUICKREF.md matches the guide's {text.count('- **SE1/')} Quick lines")
else:
    sys.stdout.write(text)
