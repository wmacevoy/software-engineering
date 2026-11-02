#!/usr/bin/env python3
"""Checks the guide's own consistency, so the conventions are enforced rather than hoped for (O3):
every relative link and anchor resolves, every principle citation carries the current version and
points at the file that defines it, every bare citation such as "(SE1/A8, SE1/D9)" names a real
principle, chapter numbers agree, README's principle index matches the chapter headings exactly,
every file llms.txt links to exists, and CHANGELOG.md, the *New/Changed in vX* markers under
principle headings, and the release that AGENTS.md and the templates link to all agree; and every
principle whose text differs from the last tagged release is acknowledged in CHANGELOG.md.
Exits nonzero on any problem. Needs the release tags (git fetch --tags). Standard library only.
Usage: python3 tools/check.py"""
import os
import re
import subprocess
import sys
import unicodedata

sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # Windows' default code page cannot print every link
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # beside this file, even under -I
from bodies import HEADING, MARKER, WS, bodies, read  # noqa: E402

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_V = r"v[0-9]+\.[0-9]+(?:\.[0-9]+)?"
# Releases come from CHANGELOG.md's "## v1.1 — date" headings, newest first. The top one may say
# "unreleased" while work toward it is on main; copies link to the newest dated one.
RELEASE = re.compile(rf"^## ({_V}) — ([0-9]{{4}}-[0-9]{{2}}-[0-9]{{2}}|unreleased)$")
changelog = read(os.path.join(root, "CHANGELOG.md"))
release_lines = [m for m in (RELEASE.search(l) for l in changelog.split("\n")) if m]
releases = [m.group(1) for m in release_lines]
latest = next((m.group(1) for m in release_lines if m.group(2) != "unreleased"), None)


def version_key(v):
    x = [int(n) for n in v[1:].split(".")]
    return (x[0], x[1], x[2] if len(x) > 2 else 0)


def newer(a, b):
    a, b = version_key(a), version_key(b)
    return (a > b) - (a < b)


# A patch release (v1.2.1) changes no principle, AGENTS.md, or template, so copies keep the minor's label.
def minor(v):
    return ".".join(v.split(".")[:2])


# Copies of AGENTS.md and the templates link to a release tag; the guide's own pages may link to main.
GH = re.compile(
    r"^https://github\.com/wmacevoy/software-engineering/blob/(main|"
    + "|".join(re.escape(r) for r in releases) + ")/"
)
GH_README = "https://github.com/wmacevoy/software-engineering#"
# Every citation carries the major version (README, "Principle index"); headings define IDs bare.
VERSION = "SE1"


def posix(path):
    return path.replace(os.sep, "/")


def rel(path):  # forward slashes on every platform, so a report and a git path read the same
    return posix(os.path.relpath(path, root))


files = []
for folder, dirs, names in os.walk(root):
    dirs[:] = sorted(d for d in dirs if d != ".git")
    files += [os.path.join(folder, n) for n in sorted(names) if n.endswith(".md")]


def in_dir(path, name):
    return posix(rel(path)).startswith(name + "/")


def slug(heading):
    """GitHub's heading slug, close enough for the headings used here."""
    text = heading.strip(WS).lower()
    text = "".join(c for c in text if unicodedata.category(c)[0] in "LN" or c in WS or c in "_-")
    return "".join("-" if c in WS else c for c in text)


_anchor_cache = {}


def anchors_of(path):
    if path in _anchor_cache:
        return _anchor_cache[path]
    text = read(path)
    anchors = set()
    for line in text.split("\n"):
        if re.search(r"^#{1,6} ", line):
            anchors.add(slug(re.sub(r'<a id="[^"]+"></a>', "", re.sub(r"^#+ ", "", line, count=1), count=1)))
    anchors.update(re.findall(r'<a id="([^"]+)">', text))
    _anchor_cache[path] = anchors
    return anchors


problems = 0


def problem(msg):
    global problems
    print(msg)
    problems += 1


defined_in = {}  # principle ID -> chapter file
headings = []    # index lines README must contain
marker = {}      # principle ID -> (kind, release)
for f in sorted(p for p in files if in_dir(p, "guide")):
    lines = read(f).split("\n")
    for i, line in enumerate(lines):
        m = HEADING.search(line)
        if not m:
            continue
        if m.group(2) in defined_in:
            problem(f"{m.group(2)} defined twice")
        defined_in[m.group(2)] = f
        headings.append(f"- [**{VERSION}/{m.group(2)}**](guide/{os.path.basename(f)}#{m.group(1)}) {m.group(3)}")
        # The marker, if any, is the first paragraph under the heading.
        mk = MARKER.search(lines[i + 2]) if i + 2 < len(lines) else None
        if mk:
            marker[m.group(2)] = (mk.group(1), mk.group(2))

for f in files:
    text = read(f)
    for m in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", text):
        label, href = m.group(1), m.group(2)
        gh = GH.search(href)
        where = f"{rel(f)}: {m.group(0)}"
        if not gh and href.startswith("https://github.com/wmacevoy/software-engineering/blob/"):
            problem(f"unknown ref    {where}")
            continue
        if gh:
            href = os.path.relpath(os.path.join(root, href[len(gh.group(0)):]), os.path.dirname(f))
        elif href.startswith(GH_README):
            href = os.path.relpath(os.path.join(root, "README.md"), os.path.dirname(f)) + "#" + href[len(GH_README):]
        elif re.search(r"^[a-z]+:", href):
            continue
        target, _, anchor = href.partition("#")
        target_file = os.path.normpath(os.path.join(os.path.dirname(f), target)) if target else f
        if not os.path.exists(target_file):
            problem(f"missing file   {where}")
            continue
        if anchor and anchor not in anchors_of(target_file):
            problem(f"missing anchor {where}")
        cite = label.replace("*", "")
        if re.search(r"^[PUFRDTOWHA][0-9]+$", cite):
            problem(f"unversioned    {where}")
            continue
        v = re.search(r"^(SE[0-9]+)/([A-Z][0-9]+)$", cite)
        if v:
            pid = v.group(2)
            if v.group(1) != VERSION:
                problem(f"wrong version  {where}")
            elif pid not in defined_in:
                problem(f"unknown ID     {where}")
            elif defined_in[pid] != target_file:
                problem(f"wrong file     {where} (defined in {rel(defined_in[pid])})")

# Bare citations — the form AGENTS.md uses, so it stays short when copied into other repositories.
# Only the chapter letters count, so "(K3)" and other parentheticals are left alone.
CITE = r"(?:SE[0-9]+/)?[PUFRDTOWHA][0-9]+"
_SEP = f"[{WS}]*"
for f in files:
    for m in re.finditer(rf"\(({CITE}(?:,{_SEP}{CITE})*)\)", read(f)):
        for cite in re.split(rf",{_SEP}", m.group(1)):
            where = f"{rel(f)}: {m.group(0)}"
            version, pid = cite.split("/", 1) if "/" in cite else (None, cite)
            if not version:
                problem(f"unversioned    {where}")
            elif version != VERSION:
                problem(f"wrong version  {where}")
            elif pid not in defined_in:
                problem(f"unknown ID     {where}")

# Chapter numbers: the file prefix, the title, and every link label that names a chapter agree.
chapter_title = {}  # "07-operating.md" -> "7. Operating"
for f in files:
    if not re.search(r"guide[\\/][0-9][0-9]-[a-z-]+\.md$", f):
        continue
    title = re.sub(r"^# ", "", read(f).split("\n")[0], count=1)
    n = int(os.path.basename(f)[:2])
    if not title.startswith(f"{n}. "):
        problem(f'title number   {rel(f)}: "{title}"')
    chapter_title[os.path.basename(f)] = title
for f in files:
    for m in re.finditer(r"\[([0-9]+)\. ([^\]]+)\]\(([^)#]*?)([0-9][0-9]-[a-z-]+\.md)\)", read(f)):
        title = chapter_title.get(m.group(4))
        if title and f"{m.group(1)}. {m.group(2)}" != title:
            problem(f'chapter label  {rel(f)}: {m.group(0)} (title is "{title}")')

# llms.txt points agents at raw files by URL, which the link check above never sees.
RAW = "https://raw.githubusercontent.com/wmacevoy/software-engineering/main/"
for m in re.finditer(r"\]\(([^)]+)\)", read(os.path.join(root, "llms.txt"))):
    if not m.group(1).startswith(RAW):
        problem(f"not a raw link llms.txt: {m.group(0)}")
    elif not os.path.exists(os.path.join(root, m.group(1)[len(RAW):])):
        problem(f"missing file   llms.txt: {m.group(0)}")

# Changes are easy to spot only while CHANGELOG.md, the markers, and the copies agree (SE1/U7).
if not latest:
    problem('CHANGELOG.md has no "## vX.Y — yyyy-mm-dd" release')
listed = {}  # "v1.1 New" -> set of IDs
release, kind, total, base = None, None, 0, None
for line in changelog.split("\n"):
    r = RELEASE.search(line)
    if r:
        release, kind = r.group(1), None
        continue
    k = re.search(r"^### (New|Changed|Also changed)$", line)
    if k:
        kind = k.group(1)
        continue
    count = re.search(r"· ([0-9]+) principles$", line)
    if count and release == releases[-1]:
        base = int(count.group(1))
    if release and kind == "Also changed":
        for m in re.finditer(r"\[SE1/([A-Z][0-9]+)\]\(", line):
            listed.setdefault(f"{release} Also changed", set()).add(m.group(1))
    item = re.search(r"^- \[SE1/([A-Z][0-9]+)\]\(", line)
    if not item or not release or kind not in ("New", "Changed"):
        continue
    listed.setdefault(f"{release} {kind}", set()).add(item.group(1))
    if kind == "New":
        total += 1
for pid, (mk_kind, mk_release) in marker.items():
    if mk_release not in releases:
        problem(f"unknown release {pid}: *{mk_kind} in {mk_release}.*")
    elif mk_kind == "Since":
        continue  # git's answer, not a claim about meaning; tools/since.py checks it
    elif pid not in listed.get(f"{mk_release} {mk_kind}", ()):
        problem(f"not in CHANGELOG {pid}: *{mk_kind} in {mk_release}.* has no entry under {mk_release} / {mk_kind}")
for key, ids in listed.items():
    rel_name = key.split(" ")[0]
    if key.endswith("Also changed"):
        continue
    for pid in ids:
        mk = marker.get(pid)
        if pid not in defined_in:
            problem(f"unknown ID     CHANGELOG.md {key}: {pid}")
        elif not mk or newer(mk[1], rel_name) < 0:
            problem(f"no marker      {pid}: CHANGELOG lists it under {key}, but its heading has no *New/Changed in {rel_name}* or later")
if base is not None and base + total != len(defined_in):
    problem(f"principle count {len(defined_in)} = {base} in {releases[-1]} + {total} New? A new principle is missing from CHANGELOG.md")
copies = ["AGENTS.md"] + [rel(f) for f in files if in_dir(f, "templates")]
for f in copies:
    for m in re.finditer(r"software-engineering/(?:blob|tree)/(v[0-9]+\.[0-9]+)", read(os.path.join(root, f))):
        if m.group(1) != minor(latest):
            problem(f"stale release  {f}: links to {m.group(1)}, latest is {latest} (copies link its minor, {minor(latest)})")


# Every principle whose text differs from the newest tagged release is acknowledged: a marker for a
# later release, or a mention under a later release's "Also changed" (a wording-only change).
class GitError(Exception):
    pass


def git(*args):
    r = subprocess.run(["git", "-C", root, *args], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    if r.returncode:
        raise GitError(args)
    return r.stdout.decode("utf-8")


def has_tag(tag):
    try:
        git("rev-parse", "-q", "--verify", f"refs/tags/{tag}")
        return True
    except GitError:
        return False


tagged = next((r for r in releases if has_tag(r)), None)
if not tagged:
    problem(f"no release tag: none of {', '.join(releases)} is tagged here (git fetch --tags)")
else:
    later = [r for r in releases if newer(r, tagged) > 0]
    for f in dict.fromkeys(defined_in.values()):
        path = posix(rel(f))
        try:
            before = bodies(git("show", f"{tagged}:{path}"))
        except GitError:
            before = {}
        for pid, now in bodies(read(f)).items():
            if pid not in before or before[pid] == now:
                continue
            mk = marker.get(pid)
            acknowledged = (mk and mk[0] != "Since" and newer(mk[1], tagged) > 0) or any(
                pid in listed.get(f"{r} Also changed", ()) for r in later)
            if not acknowledged:
                problem(f'unacknowledged {pid} changed since {tagged}: add *Changed in vX.Y.* under its heading, or name it under "Also changed" in CHANGELOG.md')

agents = re.search(r"This copy is from \*\*(v[0-9]+\.[0-9]+)\*\*", read(os.path.join(root, "AGENTS.md")))
if not agents or agents.group(1) != minor(latest):
    problem(f"stale release  AGENTS.md: says it is from {agents.group(1) if agents else 'nothing'}, latest is {latest} (copies say its minor, {minor(latest)})")

# A patch release may only change what is not a principle or a copy: compare with the minor's tag.
# The rule holds while the patch is the newest section; work toward the next release goes under an
# unreleased section above it, and from then on the minor-release rules apply.
top = release_lines[0].group(1) if release_lines else None
if latest and top == latest and len(latest.split(".")) == 3:
    patch_base = minor(latest)
    for k in ("New", "Changed"):
        if f"{latest} {k}" in listed:
            problem(f"patch release  {latest} lists principles under {k}; only a minor release may")
    try:
        git("rev-parse", "-q", "--verify", f"refs/tags/{patch_base}")
        for f in copies:
            if git("show", f"{patch_base}:{posix(f)}") != read(os.path.join(root, f)):
                problem(f"patch release  {latest} changed {f}; copies are only re-copied at a minor release")
        for f in dict.fromkeys(defined_in.values()):
            before = bodies(git("show", f"{patch_base}:{posix(rel(f))}"))
            for pid, now in bodies(read(f)).items():
                if before.get(pid) != now:
                    problem(f"patch release  {latest} changed {pid}; a principle changes only at a minor release")
    except GitError:
        problem(f"patch release  {latest} needs its minor's tag {patch_base} (git fetch --tags)")

readme = read(os.path.join(root, "README.md"))
index = [line for line in readme.splitlines() if line.startswith(f"- [**{VERSION}/")]
for line in headings:
    if line not in index:
        problem(f"README index out of date: {line}")
for i, line in enumerate(index):
    if line not in headings:
        problem(f"README index lists a principle no heading has: {line}")
    elif line in index[:i]:
        problem(f"README index lists this twice: {line}")


# A copy that is ahead of its label says nothing (SE1/U7): every principle AGENTS.md and the
# templates cite must be in README's index at the release they name, read from that tag when it
# exists and from the working tree otherwise (a release dated but not yet tagged).
def index_ids(text):
    return set(re.findall(r"\[\*\*SE[0-9]+/([A-Z][0-9]+)\*\*\]", text))


for f in copies:
    text = read(os.path.join(root, f))
    found = re.search(r"software-engineering/blob/(v[0-9]+\.[0-9]+)/", text)
    label = (agents.group(1) if agents else None) if f == "AGENTS.md" else (found.group(1) if found else None)
    if not label:
        continue
    try:
        ids = index_ids(git("show", f"{label}:README.md"))
    except GitError:
        ids = index_ids(readme)
    for pid in dict.fromkeys(re.findall(r"SE[0-9]+/([A-Z][0-9]+)", text)):
        if pid not in ids:
            problem(f"ahead of label  {f}: cites SE1/{pid}, which {label} does not define")

print(f"{len(files)} files, {len(defined_in)} principles, {problems} problems")
sys.exit(1 if problems else 0)
