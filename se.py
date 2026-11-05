#!/usr/bin/env python3
"""se: the guide's command-line companion for a repository that follows it.

  se --doctor   Is the repository sound? The working agreement present and current, loaded at every
                start, a hook for the handoff, the repository guide, the working set, versioned
                citations, the trace from requirements to tests, the queue, recent commits, CI.
                ADOPT.md's checklist, made executable. Read-only.
  se --post     Is this session sound? A self test in SE1/T2's sense: it refuses, with exit code 1,
                when a precondition for safe work is missing (disk below the floor), and reports the
                risks it cannot refuse: whether the session can be torn (SE1/U7), what it inherits (a
                compaction, torn state), the rules that follow, and what would lessen it. Meant to
                run as a Claude Code SessionStart hook (`se --hook` prints the entry, `--write`
                installs it); by hand in any runner. Rows that describe Claude Code say so.
  se --self     In the guide's own checkout: the embedded hash matches AGENTS.md as released.

Standard library only, Python 3.9 or later. This copy is from the guide release named in RELEASE;
the doctor's first line says whether a newer one exists, or that it could not check and how old its
last successful check is (SE1/U7: a status with no since reads as current).
"""
import argparse
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.request
from collections import namedtuple
from pathlib import Path

RELEASE = "v1.7"
# sha256 of AGENTS.md at RELEASE. `se --self` checks it in the guide's tree; the release commit sets it.
AGENTS_SHA256 = "b7e05f63f92afa0188c67d6f59354bfc24b831c74ae1e5194811be4f5b226f21"
GUIDE_REPO = "wmacevoy/software-engineering"
LOW_DISK_GB = 10        # warn below (invented)
NO_DISK_GB = 2          # fail below (invented)
COMPACTION_NEW_SECONDS = 120  # a record this recent is the compaction that fired the hook (invented)
STALE_DAYS = 7          # a queue row in progress this long with no movement is torn work (invented)
CACHE_STALE_DAYS = 30   # a release check older than this is reported as stale (invented)

Finding = namedtuple("Finding", "name ids state text fix")  # state: pass | warn | none yet | fail
PASS, WARN, NONE, FAIL = "pass", "warn", "none yet", "fail"
LABEL_RE = re.compile(r"This copy is\s+from\s+\*\*(v\d+\.\d+)\*\*")  # \s+: copies are wrapped at 100 columns, and the label can break across a line
# A bullet (`- **UI-1** *(since v1)*`) or a table row (`| **UI-1** | *(since v1)* ... |`)
REQ_ID_RE = re.compile(r"\*\*([A-Z]{2,}-\d+)\*\*\s*(?:\|\s*)?\*\(since v(\d+)\)\*")
# The marks that follow, as in `*(since v2)* *(inferred)* *(judged)*`; prose further on is not a mark (SE1/U10).
REQ_MARKS_RE = re.compile(REQ_ID_RE.pattern + r"((?:\s*(?:\|\s*)?\*\([^)\n]*\)\*)*)")
VERDICT_RE = re.compile(r"\bverdict\b:?\s*(pass|passed|yes|accepted|fail|failed|no|rejected)\b", re.I)
JUDGE_RE = re.compile(r"\bby\s+(.+?)\s*(?:[,;]|\s\d{4}-|\.?$)")
DATE_RE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")
# The line that names this guide's release, in every release's AGENTS.md. A sibling guide's agreement
# (the data-mining guide's) links SE1's AGENTS.md as a blob and carries a label of its own release, so
# the label alone does not say whose copy a file is.
SE1_RE = re.compile(rf"github\.com/{GUIDE_REPO}/tree/v\d+\.\d+")


def sha256(path):
    """Of the file with line endings normalized to LF, so a CRLF checkout of the same text matches."""
    return hashlib.sha256(Path(path).read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def run(cmd, cwd=None, timeout=20):
    try:  # decoded as UTF-8 explicitly: on Windows, text=True would use the locale's code page
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, timeout=timeout)
        return p.returncode, p.stdout.decode("utf8", errors="replace")
    except (OSError, subprocess.TimeoutExpired):
        return 1, ""


def run_bytes(cmd, cwd=None, timeout=20):
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, timeout=timeout)
        return p.returncode, p.stdout
    except (OSError, subprocess.TimeoutExpired):
        return 1, b""


def read(path):
    try:
        return Path(path).read_text(encoding="utf8", errors="replace")
    except OSError:
        return ""


# ---------------------------------------------------------------- the release check

def default_fetch(url, timeout=5):
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "se.py"}), timeout=timeout) as r:
        return r.read()


def release_check(online=True, cache_dir=None, fetch=default_fetch, now=None):
    """Try the network for the newest release and its AGENTS.md hash; fall back to the cache and say
    how old it is. Returns a dict: made, latest, sha (tag -> sha256), checked_at, note."""
    now = now or dt.datetime.now(dt.timezone.utc)
    cache_dir = Path(cache_dir or os.environ.get("SE_CACHE_DIR") or Path.home() / ".cache" / "se")
    cache_file = cache_dir / "releases.json"
    cached = {}
    try:
        cached = json.loads(cache_file.read_text())
    except (OSError, ValueError):
        pass
    result = {"made": False, "latest": cached.get("latest"), "sha": cached.get("sha", {}),
              "checked_at": cached.get("checked_at"), "note": ""}
    if online:
        try:
            tags = json.loads(fetch(f"https://api.github.com/repos/{GUIDE_REPO}/tags"))
            names = sorted((t["name"] for t in tags if re.fullmatch(r"v\d+\.\d+(?:\.\d+)?", t.get("name", ""))),
                           key=lambda v: tuple(int(x) for x in v[1:].split(".")))
            if not names:
                raise ValueError("no release tags")
            latest = names[-1]
            sha = dict(result["sha"])
            sha[latest] = hashlib.sha256(fetch(
                f"https://raw.githubusercontent.com/{GUIDE_REPO}/{latest}/AGENTS.md")).hexdigest()
            result.update(made=True, latest=latest, sha=sha, checked_at=now.isoformat(timespec="seconds"))
            result["note"] = f"release check made {now.date()}: latest is {latest}"
            try:
                cache_dir.mkdir(parents=True, exist_ok=True)
                cache_file.write_text(json.dumps({k: result[k] for k in ("latest", "sha", "checked_at")}))
            except OSError:
                pass
            return result
        except Exception as e:  # any network or parse failure: say so, and say how stale the cache is
            why = type(e).__name__
    else:
        why = "offline"
    if result["checked_at"]:
        age = (now - dt.datetime.fromisoformat(result["checked_at"])).days
        result["note"] = (f"release check not made ({why}); last successful check {age} days ago "
                          f"({result['checked_at'][:10]}): latest then was {result['latest']}")
        result["stale"] = age > CACHE_STALE_DAYS
    else:
        result["note"] = f"release check not made ({why}); never checked: this copy knows only {RELEASE}"
        result["stale"] = True
    return result


# ---------------------------------------------------------------- finding things in a repository

def claude_imports(claude_md):
    """Paths a CLAUDE.md imports with @path lines, resolved relative to the file."""
    out = []
    for line in read(claude_md).splitlines():
        m = re.match(r"^@(\S+)", line.strip())
        if m:
            p = Path(os.path.expanduser(m.group(1)))
            out.append(p if p.is_absolute() else (Path(claude_md).parent / p))
    return out


def find_copy(repo):
    """The repository's copy of SE1's AGENTS.md: at the root, or whatever CLAUDE.md imports, known by the
    line that names this guide's release. Returns (path, label); (path, None) when the root AGENTS.md is
    SE1's without a label, or is not SE1's at all; (None, None) when there is none."""
    repo = Path(repo)
    candidates = [repo / "AGENTS.md"] + claude_imports(repo / "CLAUDE.md")
    for c in candidates:
        text = read(c) if c.is_file() else ""
        if SE1_RE.search(text):
            m = LABEL_RE.search(text)
            return c, (m.group(1) if m else None)
    if (repo / "AGENTS.md").is_file():
        return repo / "AGENTS.md", None
    return None, None


def latest_requirements(repo):
    """(path, version, {id: since}) for the highest-numbered docs/REQUIREMENTS_vN.md, or (None, 0, {})."""
    found = []
    for d in (Path(repo) / "docs", Path(repo)):
        for p in d.glob("REQUIREMENTS_v*.md"):
            m = re.search(r"_v(\d+)\.md$", p.name)
            if m:
                found.append((int(m.group(1)), p))
    if not found:
        return None, 0, {}
    version, path = max(found)
    ids = {m.group(1): int(m.group(2)) for m in REQ_ID_RE.finditer(read(path))}
    return path, version, ids


def tracked_files(repo):
    rc, out = run(["git", "ls-files", "-z"], cwd=repo)
    if rc != 0:
        return [p for p in Path(repo).rglob("*") if p.is_file() and ".git" not in p.parts]
    return [Path(repo) / f for f in out.split("\0") if f]


def own_files(repo):
    """(tracked files that are this repository's own, the vendored trees left out). A tree under a top-level
    vendor/ is another repository's: its IDs, tests, and verdicts answer to its own requirements. Only the
    top level, so a false failure elsewhere stays to be read; a file silently unread could not be."""
    own, left_out = [], set()
    for f in tracked_files(repo):
        parts = f.relative_to(repo).parts
        if parts[0] == "vendor" and len(parts) > 1:
            left_out.add("/".join(parts[:2]))
        else:
            own.append(f)
    return own, sorted(left_out)


def left_out_note(left_out):
    """What the row did not read, so its pass is not read as covering it (SE1/U7)."""
    if not left_out:
        return ""
    return f"; left out, as vendored: {', '.join(left_out[:3])}" + (f" and {len(left_out) - 3} more" if len(left_out) > 3 else "")


def is_text(path):
    return path.suffix.lower() in {".md", ".txt", ".py", ".js", ".mjs", ".cjs", ".jsx", ".ts", ".tsx",
                                   ".c", ".h", ".cpp", ".cc", ".cxx", ".hpp", ".hh", ".cs", ".kt", ".swift",
                                   ".sh", ".yml", ".yaml", ".toml", ".json", ".rs", ".go", ".java", ".rb",
                                   ".ps1", ".cfg", ".ini", ""}


def settings(repo):
    merged = {}
    for name in ("settings.json", "settings.local.json"):
        try:
            merged.update(json.loads(read(Path(repo) / ".claude" / name) or "{}"))
        except ValueError:
            pass
    return merged


# ---------------------------------------------------------------- the doctor's checks

def foundation_pin(repo):
    """What the fundamental shape's Foundation line pins: (name, [major, minor, patch] as far as written), or None."""
    req, _, _ = latest_requirements(repo)
    section = re.search(r"^##\s+(?:Fundamental )?[Ss]hape\s*$(.*?)(?=^##\s|\Z)", read(req), re.M | re.S) if req else None
    m = re.search(r"\*\*Foundation:\*\*\s*`?(SE(\d+(?:\.\d+){0,2})?)(?![\w.])", section.group(1)) if section else None
    return (m.group(1), [int(x) for x in m.group(2).split(".")] if m.group(2) else []) if m else None


def check_copy(repo, rel):
    """The row itself; a pin to an exact release is marked on whatever it says, since nothing else warns of its cost."""
    f = copy_row(repo, rel)
    pin = foundation_pin(repo)
    if pin and len(pin[1]) == 3 and f.state != FAIL:
        return f._replace(text=f"FRAGILE, pinned to exactly {pin[0]}: it takes no fix, and nothing warns of a newer release; {f.text}")
    return f


def copy_row(repo, rel):
    path, label = find_copy(repo)
    if not path:
        return Finding("working agreement", "SE1/U7", FAIL, "no AGENTS.md, and CLAUDE.md imports none",
                       f"copy AGENTS.md from the guide at {rel.get('latest') or RELEASE} (ADOPT.md step 1)")
    newest = rel.get("latest") or RELEASE
    if not label and not SE1_RE.search(read(path)):
        return Finding("working agreement", "SE1/U7", FAIL,
                       f"{path.name} is not a copy of SE1's agreement (no line names the guide's release); "
                       "if it is another guide's, SE1's copy goes beside it",
                       f"copy AGENTS.md from the guide at {newest} to docs/SE1-AGENTS.md, say, and import it from CLAUDE.md")
    if not label:
        return Finding("working agreement", "SE1/U7", FAIL, f"{path.name} carries no release label",
                       "re-copy it from a release: a copy that cannot say which release it is cannot say it is behind")
    digest = sha256(path)
    known = rel.get("sha", {}).get(label) or (AGENTS_SHA256 if label == RELEASE else None)
    where = str(path.relative_to(repo)) if str(path).startswith(str(repo)) else str(path)
    minor = lambda v: tuple(int(x) for x in v[1:].split(".")[:2])
    pin = foundation_pin(repo)
    if pin and any(a != b for a, b in zip(pin[1][:2], minor(label))):
        return Finding("working agreement", "SE1/U7", FAIL, f"{where} is {label}, and the fundamental shape's Foundation says {pin[0]}",
                       "re-copy it at the Foundation's release, or move the Foundation in a new requirements version")
    if rel.get("sha", {}).get(newest) == digest:  # the same text as the newest release: current, whatever the label
        return Finding("working agreement", "SE1/U7", PASS, f"{where} is {label}, the same text as {newest}, the newest release", "")
    behind = label != newest and minor(label) < minor(newest)
    # Unpinned or SE1.7: any newer minor warns. SE1 or SE: only a new major. SE1.7.3: nothing does.
    warns = behind and (not pin or len(pin[1]) == 2 or (len(pin[1]) < 2 and minor(label)[0] < minor(newest)[0]))
    if warns:
        how = "then move the Foundation and re-copy" if pin else ("then re-copy, or set how much warns: "
                                                                  "the Foundation line in the requirements template")
        return Finding("working agreement", "SE1/U7", WARN, f"{where} is {label}; {newest} is out",
                       f"read *For copies* under {newest} in the guide's CHANGELOG, {how}")
    if known and digest != known:
        return Finding("working agreement", "SE1/U7", FAIL, f"{where} says {label} but its text differs from the release's",
                       "it was edited, or copied from an unreleased commit; local rules go in the repository guide")
    if not known:
        return Finding("working agreement", "SE1/U7", WARN, f"{where} is {label}; its text could not be compared "
                       "(no hash for that release here)", "run with the network once to fetch the release's hash")
    if behind:
        return Finding("working agreement", "SE1/U7", PASS, f"{where} is {label}, unedited, as its Foundation {pin[0]} allows; {newest} is out", "")
    return Finding("working agreement", "SE1/U7", PASS, f"{where} is {label}, unedited; the newest known is {newest}", "")


def check_loads(repo):
    repo = Path(repo).resolve()
    copy, _ = find_copy(repo)
    here = [repo / n for n in ("CLAUDE.md", "CLAUDE.local.md", ".claude/CLAUDE.md") if (repo / n).is_file()]
    above = [p / n for p in repo.parents for n in ("CLAUDE.md", "CLAUDE.local.md", ".claude/CLAUDE.md") if (p / n).is_file()]
    s = settings(repo)
    excl = [x for x in s.get("claudeMdExcludes", []) if "AGENTS" in str(x)]
    if excl:
        return Finding("loads at every start", "SE1/A11", FAIL, f"claudeMdExcludes covers the copy: {excl}", "remove it")
    if here:
        imports = [p for h in here for p in claude_imports(h)]
        inside = [p for p in imports if p.exists() and str(p.resolve()).startswith(str(repo))]
        outside = [p for p in imports if not str(p.resolve()).startswith(str(repo))]
        if copy and any(p.resolve() == copy.resolve() for p in inside):
            return Finding("loads at every start", "SE1/A11", PASS,
                           f"[Claude Code configuration] {here[0].name} imports the copy from inside the working "
                           "directory; an InstructionsLoaded hook can confirm it (load_reason include). Observed "
                           "loading, for any runner: the phrase test (ADOPT.md step 2)", "")
        if outside:
            return Finding("loads at every start", "SE1/A11", FAIL,
                           f"{here[0].name} imports from outside the working directory: {outside[0]}",
                           "an import that leaves the working directory needs an approval a -p session never shows; keep a copy inside")
        return Finding("loads at every start", "SE1/A11", FAIL,
                       f"{here[0].name} exists, which switches off Claude Code's own AGENTS.md read, and it does not import the copy",
                       "add a line `@AGENTS.md` (or the copy's path) to CLAUDE.md")
    if above:
        return Finding("loads at every start", "SE1/A11", FAIL,
                       f"a CLAUDE.md above the repository ({above[0]}) switches off the AGENTS.md read here",
                       "add a CLAUDE.md in this repository that imports the copy")
    if copy and copy.name == "AGENTS.md" and copy.parent == repo:
        return Finding("loads at every start", "SE1/A11", PASS,
                       "[Claude Code configuration] no CLAUDE.md: Claude Code reads AGENTS.md by itself (v2.1.277+); "
                       "no hook confirms that path. Other runners were not inspected. Observed loading, for any "
                       "runner: the phrase test (ADOPT.md step 2)", "")
    return Finding("loads at every start", "SE1/A11", FAIL, "no CLAUDE.md and no AGENTS.md at the root",
                   "copy AGENTS.md to the root, or import the copy from a CLAUDE.md")


def check_quickref(repo):
    """The condensed guide in every working agent's context. Only CLAUDE.md does it: a hook's output is capped at 10,000
    characters, and over that the agent gets a path and a preview (../compaction, CLAUDE-CODE-DOCS-2026-10-27.md)."""
    repo = Path(repo).resolve()
    fix = "add a line `@vendor/se1/QUICKREF.md` to the root CLAUDE.md, beside `@AGENTS.md` (ADOPT.md step 2)"
    claude = repo / "CLAUDE.md"
    found = [p for p in claude_imports(claude) if p.name == "QUICKREF.md"] if claude.is_file() else []
    if not found:
        return Finding("quick reference", "SE1/A11", FAIL, "the root CLAUDE.md does not import QUICKREF.md, so a working agent can skip it", fix)
    if not found[0].is_file():
        return Finding("quick reference", "SE1/A11", FAIL, f"CLAUDE.md imports {found[0].name}, which is not there", fix)
    return Finding("quick reference", "SE1/A11", PASS,
                   "[Claude Code configuration] CLAUDE.md imports it, so it loads at each start and after each compaction; "
                   "Explore and Plan start without CLAUDE.md. Observed loading: the phrase test (ADOPT.md step 2)", "")


def hook_commands(s):
    """Yield (event, matcher, command) for every command hook in a settings dict."""
    for event, entries in (s.get("hooks") or {}).items():
        for entry in entries or []:
            for h in entry.get("hooks", []):
                if h.get("type") == "command":
                    yield event, entry.get("matcher", ""), h.get("command", "")


def check_hooks(repo):
    s = settings(repo)
    found = [(e, m, c) for e, m, c in hook_commands(s)
             if e == "PostCompact" or (e == "SessionStart" and (not m or "compact" in m))]
    if not found:
        return Finding("handoff hook", "SE1/A11", NONE, "[Claude Code configuration] no hook receives the compaction (PostCompact) or runs after it (SessionStart compact)",
                       "`se --hook` prints an entry that runs `se --post` at startup, resume, and compaction")
    missing = []
    for _, _, cmd in found:
        for tok in cmd.split():
            if tok.endswith((".py", ".sh", ".js")) and not (Path(repo) / tok).exists() and not Path(os.path.expanduser(tok)).exists():
                missing.append(tok)
    if missing:
        return Finding("handoff hook", "SE1/A11", FAIL, f"hook names a script that does not exist: {missing[0]}", "fix the path")
    names = ", ".join(f"{e}{'(' + m + ')' if m else ''}" for e, m, _ in found)
    return Finding("handoff hook", "SE1/A11", PASS, f"[Claude Code configuration] {names}: configured, not seen to fire", "make it fire once on purpose (SE1/T3)")


def guide_command(text, fallback=True):
    """The check command a repository guide names: the template's "**The full check:**" line, its inline
    code or the first line of the fenced block after it; failing that, with fallback, the first line that
    names a check or test with code on it."""
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if re.search(r"\*\*The full check:?\*\*", line):
            m = re.search(r"`([^`]+)`", line)
            if m and not m.group(1).startswith("_"):
                return m.group(1)
            for j in range(i + 1, min(i + 6, len(lines))):
                if lines[j].strip().startswith("```"):
                    for k in range(j + 1, len(lines)):
                        if lines[k].strip().startswith("```"):
                            break
                        if lines[k].strip():
                            return lines[k].strip()
                    break
    if not fallback:
        return None
    for line in lines:
        if re.search(r"\b(check|test)s?\b", line, re.I) and "`" in line and not line.lstrip().startswith("#"):
            m = re.search(r"`([^`]+)`", line)
            if m and not m.group(1).startswith("_"):
                return m.group(1)
    return None


def check_guide(repo):
    for name in ("CONTRIBUTING.md", "CLAUDE.md", "README.md"):
        text = read(Path(repo) / name)
        if not text:
            continue
        # A README is prose: on one course repository the fallback took a workflow path from a line that
        # mentioned tests for the check command. Only a labeled line counts there.
        cmd = guide_command(text, fallback=(name != "README.md"))
        if cmd:
            return Finding("repository guide", "SE1/A2, SE1/W10", PASS, f"{name} names the check: `{cmd}`", ""), cmd
        if re.search(r"none yet", text, re.I):
            return Finding("repository guide", "SE1/A2, SE1/W10", NONE, f"{name} says the check is none yet", "a queue item"), None
        if name != "README.md":
            return Finding("repository guide", "SE1/A2, SE1/W10", NONE, f"{name} names no check command",
                           "say how to build, run, test, and reset (templates/CONTRIBUTING.md)"), None
    return Finding("repository guide", "SE1/A2, SE1/W10", NONE, "no CONTRIBUTING.md or CLAUDE.md",
                   "write one from the guide's template (ADOPT.md step 3)"), None


def check_working_set(repo):
    req, version, ids = latest_requirements(repo)
    if not req:
        docs = Path(repo) / "docs"
        # Name what is there when it is not SE1's layout: a project that follows another guide (QUESTION_vN,
        # LEDGER, ...) was told "no REQUIREMENTS" as if docs/ were empty. se checks SE1's layout only.
        others = sorted(p.stem for p in docs.glob("*.md")) if docs.is_dir() else []
        others = [n for n in others if n not in ("QUEUE", "FINDINGS") and not re.match(r"(REQUIREMENTS|DESIGN)_v\d+$", n)]
        if others:
            shown = ", ".join(others[:5]) + (f" and {len(others) - 5} more" if len(others) > 5 else "")
            return Finding("working set", "SE1/W10", NONE, f"no docs/REQUIREMENTS_vN.md; docs/ holds {shown}, which is not SE1's layout",
                           "if the project follows another guide, that guide's checker says whether its set is complete; "
                           "se checks SE1's (REQUIREMENTS_vN, DESIGN_vN, QUEUE, FINDINGS) only")
        return Finding("working set", "SE1/W10", NONE, "no docs/REQUIREMENTS_vN.md",
                       "treat each task's text as its requirement, marked (inferred); propose the W12 reconstruction")
    docs = req.parent
    missing = [n for n in ("QUEUE.md", "FINDINGS.md") if not (docs / n).is_file()]
    if not list(docs.glob("DESIGN_v*.md")):
        missing.append("DESIGN_vN.md")
    text = read(req)
    sections = [n for n in ("Non-goals", "Scope decisions") if not re.search(rf"^#+\s*{n}", text, re.I | re.M)]
    if missing or sections:
        what = ", ".join(missing + [f"section {s}" for s in sections])
        return Finding("working set", "SE1/W10, SE1/R9", FAIL if sections else NONE,
                       f"REQUIREMENTS_v{version} ({len(ids)} requirements); missing: {what}",
                       "AGENTS.md searches Non-goals and Scope decisions before every task; they must exist, even short")
    return Finding("working set", "SE1/W10, SE1/R9", PASS,
                   f"REQUIREMENTS_v{version} ({len(ids)} requirements), DESIGN, QUEUE, FINDINGS; Non-goals and Scope decisions present", "")


def is_history(name, line):
    """A FINDINGS entry, a kept review, or a done queue row cites a requirement as it read when written;
    rewriting the citation to the newest version would make the record false. R10 versions the
    requirement, not the history of it."""
    return name == "FINDINGS.md" or name.startswith("REVIEW-") or (name == "QUEUE.md" and re.search(r"\|\s*done\b", line, re.I) is not None)


def check_citations(repo, req, version, ids):
    if not ids:
        return Finding("citations", "SE1/R10", NONE, "no requirement IDs to cite", "")
    bare, stale, ahead, unknown = [], [], [], []
    pat = re.compile(r"(?:(REQ(\d+))/)?\b(" + "|".join(map(re.escape, ids)) + r")\b")
    copy, _ = find_copy(repo)  # the working agreement's own examples (REQ2/UI-1) are not citations
    files, left_out = own_files(repo)
    note = left_out_note(left_out)
    design = re.compile(r"DESIGN_v(\d+)\.md$")
    designs = [int(m.group(1)) for m in (design.match(f.name) for f in files) if m]
    for f in files:
        if f.resolve() == req.resolve() or not is_text(f) or f.name.startswith("REQUIREMENTS_v"):
            continue
        old = design.match(f.name)  # a superseded design cites requirements as they read then, as FINDINGS does
        if old and int(old.group(1)) < max(designs):
            continue
        if f.name == "AGENTS.md" or f.name == "se.py" or (copy and f.resolve() == copy.resolve()):
            continue
        for i, line in enumerate(read(f).splitlines(), 1):
            last = None  # list shorthand: in `REQ2/UI-1, UI-2`, the bare ID takes the version named before it
            for m in pat.finditer(line):
                where = f"{f.relative_to(repo).as_posix()}:{i}"
                ver = m.group(2) or last
                if m.group(2):
                    last = m.group(2)
                if not ver:
                    bare.append(where)
                elif int(ver) < ids[m.group(3)]:
                    if not is_history(f.name, line):
                        stale.append(f"{where} REQ{ver}/{m.group(3)} (since v{ids[m.group(3)]})")
                elif int(ver) > version:
                    ahead.append(where)
    if stale or bare or ahead:
        parts = []
        if stale:
            parts.append(f"{len(stale)} stale (the requirement moved): {stale[0]}")
        if bare:
            parts.append(f"{len(bare)} unversioned: {bare[0]}")
        if ahead:
            parts.append(f"{len(ahead)} ahead of v{version}: {ahead[0]}")
        return Finding("citations", "SE1/R10", FAIL, "; ".join(parts) + note,
                       "cite the version that last changed the requirement: REQn/ID, never a bare ID")
    return Finding("citations", "SE1/R10", PASS, f"every citation of the {len(ids)} requirement IDs is versioned and current{note}", "")


def judged_ids(req):
    """The requirements marked (judged): only a named person can pass them (SE1/U10)."""
    if not req:
        return []
    return [m.group(1) for m in REQ_MARKS_RE.finditer(read(req)) if "*(judged)*" in m.group(3)]


def latest_verdicts(repo, judged, since):
    """{id: (date, 'pass'|'FAIL', judge)}, the newest verdict on each requirement as it now reads. A verdict
    is one line with the versioned ID, `verdict: pass` or `verdict: fail`, `by` the judge, and a date. On one
    day a failure outranks a pass. A test may veto and cannot pass, so a line in a test file is not a verdict,
    and neither is an example in the agreement, a copy, or a requirements document. Who wrote the line, and
    which version of the work it was given on, are not checked: the row names the judge for a person to read."""
    copy, _ = find_copy(repo)
    found = {}
    for f in own_files(repo)[0]:
        rel = str(f.relative_to(repo))
        if (not is_text(f) or re.search(r"test", rel, re.I) or f.name.startswith("REQUIREMENTS_v")
                or f.name in ("AGENTS.md", "se.py") or (copy and f.resolve() == copy.resolve())):
            continue
        for line in read(f).splitlines():
            outcome, judge = VERDICT_RE.search(line), JUDGE_RE.search(line)
            dates = DATE_RE.findall(line)
            if not (outcome and judge and dates):
                continue
            failed = outcome.group(1).lower() in ("fail", "failed", "no", "rejected")
            for i in judged:
                m = re.search(rf"REQ(\d+)/{re.escape(i)}\b", line)
                if m and int(m.group(1)) >= since[i]:
                    new = (max(dates), failed, judge.group(1))
                    if i not in found or new[:2] > found[i][:2]:
                        found[i] = new
    return {i: (d, "FAIL" if failed else "pass", who) for i, (d, failed, who) in found.items()}


def check_trace(repo, ids, judged=()):
    if not ids:
        return Finding("trace", "SE1/R11", NONE, "no requirements to trace", "")
    tested = [i for i in ids if i not in judged]
    verdicts = latest_verdicts(repo, judged, ids)
    waiting = [i for i in judged if verdicts.get(i, (0, "FAIL"))[1] != "pass"]
    note = ""
    if judged:
        note = (f"; {len(judged)} judged, passed by a person and not by a test: "
                + ", ".join(f"{i} (verdict {verdicts[i][1]} {verdicts[i][0]} by {verdicts[i][2]})" if i in verdicts else f"{i} (no verdict yet)" for i in judged[:5])
                + (" ..." if len(judged) > 5 else ""))
    files, left_out = own_files(repo)
    note += left_out_note(left_out)
    tests = [f for f in files if is_text(f) and re.search(r"test", str(f.relative_to(repo)), re.I)]
    text = "\n".join(read(f) for f in tests)
    without = [i for i in tested if not re.search(rf"REQ\d+/{re.escape(i)}\b", text)]
    if without:
        return Finding("trace", "SE1/R11", WARN, f"{len(without)} of {len(tested)} requirements have no test naming them: "
                       + ", ".join(without[:5]) + (" ..." if len(without) > 5 else "") + note, "each is a queue item, not a failure")
    if waiting:
        return Finding("trace", "SE1/R11", WARN, f"every one of the {len(tested)} tested requirements has a test naming it" + note,
                       "ask the judge; record one line: the versioned ID, verdict: pass or verdict: fail, by the judge, and the date")
    if not tested:
        return Finding("trace", "SE1/R11", PASS, f"no tested requirements{note}", "")
    return Finding("trace", "SE1/R11", PASS, f"every one of the {len(tested)} requirements has a test naming it" + note, "")


def parse_table(text):
    rows, header = [], None
    for line in text.splitlines():
        if not line.strip().startswith("|"):
            header = None if header and rows and rows[-1] is None else header
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if header is None:
            header = [c.lower() for c in cells]
            continue
        if all(set(c) <= set("-: ") for c in cells):
            continue
        rows.append(dict(zip(header, cells)))
    return rows


def check_queue(repo, today=None):
    today = today or dt.date.today()
    q = next((p for p in (Path(repo) / "docs" / "QUEUE.md", Path(repo) / "QUEUE.md") if p.is_file()), None)
    if not q:
        return Finding("queue", "SE1/W10, SE1/H4", NONE, "no QUEUE.md", "the task description is the queue item (ADOPT.md)")
    rows = [r for r in parse_table(read(q)) if any("status" in k for k in r)]
    if not rows:
        return Finding("queue", "SE1/W10", NONE, "QUEUE.md has no table with a Status column", "")
    has_since = any("since" in k for k in rows[0])
    torn, blocked = [], []
    for r in rows:
        status = next((v for k, v in r.items() if "status" in k), "")
        num = next((v for k, v in r.items() if k in ("#", "no", "id")), "?")
        if re.search(r"in progress", status, re.I):
            since = next((v for k, v in r.items() if "since" in k), "")
            m = re.search(r"(\d{4}-\d{2}-\d{2})", since + " " + status)
            if m:
                age = (today - dt.date.fromisoformat(m.group(1))).days
                if age > STALE_DAYS:
                    torn.append(f"#{num} in progress {age} days")
            elif not has_since:
                torn.append(f"#{num} in progress, no since")
        if re.search(r"blocked", status, re.I) and not re.search(r"blocked\s*(:|on)", status, re.I):
            blocked.append(f"#{num} blocked, on what?")
    if torn or blocked:
        return Finding("queue", "SE1/U7, SE1/H4", WARN, "; ".join(torn + blocked)[:300],
                       "a status with no since reads as current; treat an old in-progress row as torn work")
    return Finding("queue", "SE1/U7, SE1/H4", PASS, f"{len(rows)} rows; every in-progress row is recent and every blocked row says on what", "")


def check_commits(repo, n=20):
    rc, out = run(["git", "log", f"-n{n}", "--format=%s%x1f%b%x1e"], cwd=repo)
    commits = [c for c in out.split("\x1e") if c.strip()]
    if rc != 0 or not commits:
        return Finding("commits", "SE1/W11, SE1/A7", NONE, "no git history", "")
    named = sum(1 for c in commits if re.search(r"REQ\d+/[A-Z]{2,}-\d+|\bchore\b", c, re.I))
    agent = sum(1 for c in commits if re.search(r"Co-Authored-By:.*(Claude|GPT|Gemini|Copilot|agent)", c, re.I))
    text = f"of the last {len(commits)}: {named} name a versioned requirement or say chore, {len(commits) - named} neither; {agent} carry an agent trailer"
    state = PASS if named == len(commits) else WARN
    return Finding("commits", "SE1/W11, SE1/A7", state, text, "a change names its requirement's versioned ID, or is labeled a chore")


def check_ci(repo, check_cmd):
    wf = list((Path(repo) / ".github" / "workflows").glob("*.y*ml"))
    if not wf:
        return Finding("CI", "SE1/O3", NONE, "no workflow", "CI runs the command you run")
    if not check_cmd:
        return Finding("CI", "SE1/O3", WARN, f"{len(wf)} workflow(s); the repository guide names no check command to compare", "")
    text = "\n".join(read(f) for f in wf)
    segments = [s.strip() for s in check_cmd.split("&&") if s.strip()]
    missing = [s for s in segments if s not in text]  # literal: a different interpreter name is a second recipe
    if not missing:
        return Finding("CI", "SE1/O3", PASS, f"a workflow runs every part of the guide's check ({len(segments)} command{'s' if len(segments) > 1 else ''})", "")
    return Finding("CI", "SE1/O3", FAIL, f"no workflow runs `{missing[0]}`, part of the guide's check", "CI runs the same command the guide names, so one recipe cannot drift")


def doctor(repo, online=True, cache_dir=None, fetch=default_fetch, today=None):
    repo = Path(repo).resolve()
    rel = release_check(online=online, cache_dir=cache_dir, fetch=fetch)
    out = [Finding("release check", "SE1/U7", PASS if rel["made"] else (FAIL if rel.get("stale") else WARN), rel["note"],
                   "" if rel["made"] else "run again with the network")]
    out.append(check_copy(repo, rel))
    out.append(check_loads(repo))
    out.append(check_quickref(repo))
    out.append(check_hooks(repo))
    guide, cmd = check_guide(repo)
    out.append(guide)
    out.append(check_working_set(repo))
    req, version, ids = latest_requirements(repo)
    out.append(check_citations(repo, req, version, ids) if req else Finding("citations", "SE1/R10", NONE, "no requirements", ""))
    out.append(check_trace(repo, ids, judged_ids(req)))
    out.append(check_queue(repo, today))
    out.append(check_commits(repo))
    out.append(check_ci(repo, cmd))
    return out


# ---------------------------------------------------------------- the session's self test

def default_power():
    """('ac'|'battery'|'none', percent|None, sleep_prevented: True|False|None), None where nothing here can say."""
    if sys.platform == "darwin":
        rc, out = run(["pmset", "-g", "batt"], timeout=5)
        if rc == 0 and "InternalBattery" in out:
            pct = re.search(r"(\d+)%", out)
            src = "battery" if "Battery Power" in out else "ac"
            rc2, out2 = run(["pmset", "-g"], timeout=5)
            return src, int(pct.group(1)) if pct else None, "sleep prevented" in out2
        return "none", None, False
    if sys.platform == "win32":
        import ctypes  # only here: the standard library's way to the one call that needs no elevation

        class Status(ctypes.Structure):  # SYSTEM_POWER_STATUS
            _fields_ = [("ac", ctypes.c_ubyte), ("flag", ctypes.c_ubyte), ("percent", ctypes.c_ubyte),
                        ("saver", ctypes.c_ubyte), ("life", ctypes.c_ulong), ("full", ctypes.c_ulong)]
        status = Status()
        if not ctypes.windll.kernel32.GetSystemPowerStatus(ctypes.byref(status)):
            return "none", None, None
        return power_windows(status.ac, status.flag, status.percent)
    return power_linux(Path("/sys/class/power_supply"), linux_sleep_blocked)


def power_windows(ac, flag, percent):
    """From SYSTEM_POWER_STATUS. Whether sleep is prevented is `powercfg /requests`, which needs elevation: not asked."""
    if flag in (128, 255):  # no system battery; unknown
        return "none", None, None
    return ("battery" if ac == 0 else "ac"), (None if percent == 255 else percent), None


def power_linux(root, blocked):
    """A system battery by its type, since the names vary, and a mouse's battery (scope Device) is not one."""
    root = Path(root)
    bats = [d for d in sorted(root.iterdir()) if read(d / "type").strip() == "Battery"
            and read(d / "scope").strip().lower() != "device"] if root.is_dir() else []
    if not bats:
        return "none", None, None
    draining = [d for d in bats if read(d / "status").strip().lower() == "discharging"]
    cap = read((draining or bats)[0] / "capacity").strip()
    return ("battery" if draining else "ac"), (int(cap) if cap.isdigit() else None), blocked()


def sleep_blocked(listing):
    """From `systemd-inhibit --list`: True if an inhibitor blocks sleep, False if none does, None if it did not answer.
    A delay inhibitor only postpones sleep. Columns by the header's offsets, since WHY is free text."""
    rows = listing.splitlines()
    if not rows:
        return None
    head = rows[0]
    if "WHAT" not in head or "WHY" not in head:
        return False
    what, why = head.index("WHAT"), head.index("WHY")
    return any(r.rstrip().endswith(" block") and "sleep" in r[what:why].strip().split(":") for r in rows[1:])


def linux_sleep_blocked():
    rc, out = run(["systemd-inhibit", "--list", "--no-pager"], timeout=5)
    return sleep_blocked(out) if rc == 0 else None


def stay_awake(platform, which=shutil.which):
    """This platform's way to keep the machine from sleeping, or None where there is none to name."""
    if platform == "darwin":
        return "`caffeinate -i` while the session runs"
    if platform == "win32":
        return "set sleep to never in the power settings while the session runs"
    if which("systemd-inhibit"):
        return "`systemd-inhibit --what=sleep <your command>` for the session"
    return None


def tree_bytes(path, seconds=10):
    """Bytes in the files under path, or None if that takes too long: this runs in a hook, on any platform."""
    stop, total, pending = time.monotonic() + seconds, 0, [path]
    while pending:
        if time.monotonic() > stop:
            return None
        try:
            with os.scandir(pending.pop()) as entries:
                for e in entries:
                    if e.is_dir(follow_symlinks=False):
                        pending.append(e.path)
                    elif e.is_file(follow_symlinks=False):
                        total += e.stat(follow_symlinks=False).st_size
        except OSError:
            continue  # a file gone mid-walk, or a folder not readable: an estimate, as the line says
    return total


def default_disk(path):
    """(free_gb, total_gb)"""
    u = shutil.disk_usage(path)
    return u.free / 1e9, u.total / 1e9


def project_slug(path):
    """The folder name under ~/.claude/projects. A Windows drive's colon cannot be in a folder name."""
    return re.sub(r"[/\\:]", "-", path)


def transcript_for(repo, hook_input):
    if hook_input.get("transcript_path") and Path(hook_input["transcript_path"]).is_file():
        return Path(hook_input["transcript_path"])
    slug = project_slug(str(Path(repo).resolve()))
    d = Path.home() / ".claude" / "projects" / slug
    files = sorted(d.glob("*.jsonl"), key=lambda p: p.stat().st_mtime) if d.is_dir() else []
    return files[-1] if files else None


def read_transcript(path):
    """(compactions: list of (pre, post, trigger, timestamp), context_tokens_estimate)"""
    comps, ctx = [], None
    try:
        with open(path, encoding="utf8", errors="replace") as f:
            for line in f:
                if '"compactMetadata"' not in line and '"assistant"' not in line:
                    continue
                try:
                    ev = json.loads(line)
                except ValueError:
                    continue
                meta = ev.get("compactMetadata")
                if isinstance(meta, dict):
                    comps.append((meta.get("preTokens"), meta.get("postTokens"), meta.get("trigger"), ev.get("timestamp")))
                if ev.get("type") == "assistant":
                    u = (ev.get("message") or {}).get("usage") or {}
                    if u:
                        ctx = sum(u.get(k) or 0 for k in ("input_tokens", "cache_read_input_tokens", "cache_creation_input_tokens"))
    except OSError:
        pass
    return comps, ctx


def is_this_compaction(comp, now):
    """Does this transcript record belong to the compaction that fired the hook, and not an earlier one?"""
    try:
        when = dt.datetime.fromisoformat(str(comp[3]).replace("Z", "+00:00"))
        return abs((now - when).total_seconds()) <= COMPACTION_NEW_SECONDS
    except (ValueError, TypeError):
        return False


def mission_and_shape(repo):
    """The mission and fundamental shape as written, for an agent whose summary may have lost them (SE1/D9)."""
    req, _, _ = latest_requirements(repo)
    if not req:
        return []
    text, found = read(req), []
    for name in ("Mission", "(?:Fundamental )?[Ss]hape"):  # plain "Shape": documents from before v1.5
        m = re.search(rf"^##\s+{name}\s*$(.*?)(?=^##\s|\Z)", text, re.M | re.S)
        for item in re.split(r"^- ", m.group(1), flags=re.M)[1:] if m else []:
            item = re.split(r"\s+Judge:", " ".join(item.split()))[0]
            if not re.search(r"(?:^|\s)_\S|\*\*[^*]+:\*\*\s*\*", item):  # a template's blank, or a line left to fill
                found.append(f"  {item}")
    return [f"the mission and fundamental shape, from {req.name}; the source, not your summary (SE1/D9):"] + found if found else []


def torn_state(repo, today=None):
    out = []
    rc, status = run(["git", "status", "--porcelain"], cwd=repo)
    if rc == 0:
        lines = [l for l in status.splitlines() if l.strip()]
        untracked = sum(1 for l in lines if l.startswith("??"))
        if lines:
            out.append(f"{len(lines) - untracked} modified, {untracked} untracked")
    rc, stashes = run(["git", "stash", "list"], cwd=repo)
    if rc == 0 and stashes.strip():
        out.append(f"{len(stashes.splitlines())} stash(es)")
    rc, log = run(["git", "log", "-n10", "--format=%s"], cwd=repo)
    wip = [l for l in log.splitlines() if re.search(r"\b(wip|torn)\b", l, re.I)]
    if wip:
        out.append(f"a recent commit says {wip[0]!r}")
    q = check_queue(repo, today)
    if q.state == WARN:
        out.append(q.text)
    return out


def post(repo, hook_input=None, env=None, power=default_power, disk=default_disk, transcript=None, today=None, now=None, sleep=time.sleep, platform=sys.platform):
    """Lines of the self test, and the verdict ('fragile'|'robust')."""
    env = os.environ if env is None else env
    hook_input = hook_input or {}
    repo = Path(repo).resolve()
    lines, reasons, fragile, refuse = [], [], False, []
    claude = bool(env.get("CLAUDECODE"))
    runner = "Claude Code" if claude else "a runner that is not Claude Code (not inspected)"
    # Zellij sets ZELLIJ to "0", so this asks whether it is set, not whether it reads true.
    mux = next((name for var, name in (("TMUX", "tmux"), ("STY", "screen"), ("ZELLIJ", "Zellij")) if env.get(var)), None)
    ssh = bool(env.get("SSH_CONNECTION") or env.get("SSH_TTY"))
    container = Path("/.dockerenv").exists() or bool(env.get("CI")) or bool(env.get("GITHUB_ACTIONS")) \
        or "docker" in read("/proc/1/cgroup") or "containerd" in read("/proc/1/cgroup")
    attended = env.get("CLAUDE_CODE_SESSION_ATTENDED")
    entry = env.get("CLAUDE_CODE_ENTRYPOINT")
    if container:
        reasons.append("container or CI: robust, and no human to ask")
    elif ssh and not mux:
        fragile = True
        reasons.append("over SSH with no tmux, screen, or Zellij: a dropped connection likely ends this session (inferred from the terminal, not from the runner)")
    elif not mux:
        fragile = True
        reasons.append("a local terminal with no tmux, screen, or Zellij: a closed lid or a crash likely ends this session (inferred from the terminal, not from the runner)")
    else:
        reasons.append(f"under a multiplexer ({mux}): terminal processes survive a dropped connection or a closed window; what the runner itself keeps is not inspected")
    src, pct, prevented = power()
    if src == "battery":
        fragile = True
        reasons.append(f"a laptop on battery ({pct}%)")
    elif src == "ac" and pct is not None:
        reasons.append(f"a laptop on AC power ({pct}%){'; sleep not inspected' if prevented is None else '; sleep prevented' if prevented else '; sleep not prevented'}")
        if not prevented:
            fragile = True
    if claude:
        reasons.append(f"Claude Code {entry or ''}{', attended' if attended == '1' else ', unattended' if attended == '0' else ''}".rstrip())
    else:
        reasons.append(f"runner: {runner}; the transcript, compaction, and idle-compaction rows below are Claude Code's and are skipped")
    t = transcript or (transcript_for(repo, hook_input) if (claude or hook_input.get("transcript_path")) else None)
    comps, ctx = read_transcript(t) if t else ([], None)
    source = hook_input.get("source")
    own = bool(hook_input.get("transcript_path"))  # a hook names the session's transcript; by hand we guess the newest
    recorded = True
    if source == "compact":  # the hook can run before the transcript has this compaction (FINDINGS 2026-11-02)
        now = now or dt.datetime.now(dt.timezone.utc)
        for _ in range(10):
            recorded = bool(comps) and is_this_compaction(comps[-1], now)
            if recorded or not t:
                break
            sleep(0.2)
            comps, ctx = read_transcript(t)
    if source == "compact" and not recorded:
        fragile = True
        lines.append(f"YOU WERE COMPACTED just now. The transcript has not recorded it yet, so its size is not known here "
                     f"({len(comps)} earlier on record). Everything above this line is recalled, not observed; the source "
                     "wins (SE1/A11).")
        lines += mission_and_shape(repo)
    elif source == "compact" or (comps and source != "startup"):
        pre, post_, trig, _ = comps[-1] if comps else (None, None, None, None)
        fragile = True
        if own or source == "compact":
            lines.append(f"YOU WERE COMPACTED: {len(comps)} time(s) this session; the last ({trig}) replaced "
                         f"{pre or '?'} tokens with {post_ or '?'}. Everything above this line is recalled, not "
                         "observed; the source wins (SE1/A11).")
            lines += mission_and_shape(repo)
        else:
            reasons.append(f"the newest transcript for this repository records {len(comps)} compaction(s), the last "
                           f"({trig}) replacing {pre or '?'} tokens with {post_ or '?'}; if that is your session, your "
                           "summary is recalled, not observed (SE1/A11)")
    elif ctx:
        reasons.append(f"context about {ctx // 1000}k tokens, no compaction yet"
                       + ("; an hour idle at 200k+ compacts it" if ctx >= 150_000 and attended != "0" else ""))
    free, total = disk(repo)
    if free < NO_DISK_GB:
        fragile = True
        refuse.append(f"disk: {free:.1f} GB free of {total:.0f}; a write can fail now")
    elif free < LOW_DISK_GB:
        fragile = True
        reasons.append(f"disk low: {free:.1f} GB free of {total:.0f}")
    else:
        reasons.append(f"disk {free:.0f} GB free of {total:.0f}")
    claude_dir = Path.home() / ".claude" / "projects"
    if claude and claude_dir.is_dir():
        size = tree_bytes(claude_dir)
        if size is not None:
            reasons.append(f"transcripts in ~/.claude/projects: {size / 1e9:.1f} GB, and growing")
    torn = torn_state(repo, today)
    if torn:
        fragile = True
        reasons.append("torn state already here: " + "; ".join(torn))
    verdict = "refused" if refuse else ("fragile" if fragile else "robust")
    lines.append(f"se --post · {dt.datetime.now():%Y-%m-%d %H:%M} · {repo.name} · session: {verdict.upper()}")
    for r in refuse:
        lines.append(f"  - REFUSED, a missing precondition (SE1/T2): {r}. Free space before doing anything that writes.")
    lines += [f"  - {r}" for r in reasons]
    if fragile:
        lines.append("rules for this session (SE1/U7, SE1/W11, SE1/A11): assume it will be cut, and leave the repository fine "
                     "to be cut at every step: work on a branch; before any step that could take more than a few minutes, "
                     "leave the tear findable: a commit or stash whose message says it is torn if you may commit, and if "
                     "not (AGENTS.md: no commits unless asked), the trace file, and your report saying what is torn; keep "
                     "the trace current before the work, not after; one concern per change, small enough to finish; no "
                     "one-way door this session; after any gap, treat what you find as torn until shown otherwise, and "
                     "the source wins over the summary.")
        lessen = []
        if not mux and not container:
            lessen.append("run under tmux in WSL" if platform == "win32" else "run under tmux or screen")
        if src == "battery":
            lessen.append("plug in")
        awake = stay_awake(platform) if src != "none" and not prevented else None
        if awake:
            lessen.append(awake)
        if not container:
            lessen.append("a remote host where the session survives this machine")
        if free < LOW_DISK_GB:
            lessen.append("free disk space" + ("; transcripts under ~/.claude/projects are the usual growth" if claude else ""))
        if claude:
            lessen.append("for a long session, `idleCompaction: false` (Claude Code; cost: the next message after an hour reprocesses the whole context)")
        lines.append("to lessen it, once, for the human: " + "; ".join(lessen) + ".")
    else:
        lines.append("ordinary rules apply; the hand-off checklist still does.")
    return lines, verdict


# ---------------------------------------------------------------- hook, self, main

def hook_entry(se_cmd=None, platform=sys.platform):
    # Windows' python3, where it answers at all, is often the Store's stub, which installs instead of running.
    se_cmd = se_cmd or f"{'python' if platform == 'win32' else 'python3'} se.py --post"
    return {"hooks": {"SessionStart": [{"matcher": "startup|resume|compact",
                                        "hooks": [{"type": "command", "command": se_cmd}]}]}}


def write_hook(repo, entry):
    path = Path(repo) / ".claude" / "settings.json"
    try:
        current = json.loads(read(path) or "{}")
    except ValueError:
        current = {}
    hooks = current.setdefault("hooks", {})
    existing = hooks.setdefault("SessionStart", [])
    if any(e == entry["hooks"]["SessionStart"][0] for e in existing):
        return path, False
    existing.append(entry["hooks"]["SessionStart"][0])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(current, indent=2) + "\n")
    return path, True


def self_check(guide):
    guide = Path(guide)
    agents = guide / "AGENTS.md"
    problems = []
    if not (guide / "guide").is_dir() or not agents.is_file():
        return [f"{guide} is not the guide's checkout"]
    rc, released = run_bytes(["git", "show", f"{RELEASE}:AGENTS.md"], cwd=guide)
    if rc == 0 and released:  # the tag exists: the pin is of the released bytes, never decoded
        digest = hashlib.sha256(released.replace(b"\r\n", b"\n")).hexdigest()
        if digest != AGENTS_SHA256:
            problems.append(f"AGENTS_SHA256 in se.py is stale: AGENTS.md at {RELEASE} is {digest}")
        elif sha256(agents) != digest:
            print(f"note: AGENTS.md has changed since {RELEASE}; the next minor release re-pins it")
    else:  # no tag yet: the release commit pins the working tree
        digest = sha256(agents)
        if digest != AGENTS_SHA256:
            problems.append(f"AGENTS_SHA256 in se.py is stale: AGENTS.md is {digest}")
    m = LABEL_RE.search(read(agents))
    if not m or m.group(1) != RELEASE:
        problems.append(f"RELEASE in se.py is {RELEASE}; AGENTS.md says {m.group(1) if m else 'nothing'}")
    return problems


def stdin_ready(wait=0.5):
    """True if stdin has data (a hook's JSON) within `wait` seconds; a tool's open-but-silent stdin would
    otherwise block forever. Windows has no select on pipes, so it never reads stdin there."""
    try:
        import select
        return bool(select.select([sys.stdin], [], [], wait)[0])
    except (ImportError, OSError, ValueError):
        return False


def python_kind():
    exe = sys.executable or ""
    kind = "pixi" if ".pixi" in exe else "conda" if ("conda" in exe or "miniforge" in exe or "mamba" in exe) else "system"
    return f"python {sys.version.split()[0]} ({kind}: {exe})"


def main(argv=None):
    ap = argparse.ArgumentParser(prog="se", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--doctor", action="store_true", help="check the repository (the default)")
    ap.add_argument("--post", action="store_true", help="the session's power-on self test")
    ap.add_argument("--hook", action="store_true", help="print the SessionStart entry for --post")
    ap.add_argument("--write", action="store_true", help="with --hook: merge it into .claude/settings.json")
    ap.add_argument("--self", dest="self_", action="store_true", help="in the guide's checkout: the embedded hash is current")
    ap.add_argument("--repo", default=".", help="the repository to check (default: here)")
    ap.add_argument("--offline", action="store_true", help="do not try the network for the release check")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--version", action="store_true")
    a = ap.parse_args(argv)
    repo = Path(a.repo).resolve()
    if a.version:
        print(f"se {RELEASE} · {python_kind()}")
        return 0
    if a.self_:
        problems = self_check(repo)
        print("\n".join(problems) if problems else f"se --self: AGENTS.md matches {RELEASE}")
        return 1 if problems else 0
    if a.hook:
        entry = hook_entry()
        if a.write:
            path, changed = write_hook(repo, entry)
            print(f"{'added to' if changed else 'already in'} {path}")
        else:
            print(json.dumps(entry, indent=2))
            print("\nadd this to .claude/settings.json, or run `se --hook --write`", file=sys.stderr)
        return 0
    if a.post:
        hook_input = {}
        if not sys.stdin.isatty() and stdin_ready():
            try:
                hook_input = json.loads(sys.stdin.read() or "{}")
            except ValueError:
                hook_input = {}
        lines, verdict = post(repo, hook_input)
        if a.json:
            print(json.dumps({"verdict": verdict, "lines": lines}))
        else:
            print("\n".join(lines))
        return 1 if verdict == "refused" else 0
    findings = doctor(repo, online=not a.offline)
    if a.json:
        print(json.dumps([f._asdict() for f in findings], indent=2))
    else:
        print(f"se --doctor · {repo} · se {RELEASE} · {python_kind()}")
        for f in findings:
            fix = f"  → {f.fix}" if f.fix and f.state != PASS else ""
            print(f"[{f.state:>8}] {f.name:<20} ({f.ids})  {f.text}{fix}")
        bad = sum(1 for f in findings if f.state == FAIL)
        print(f"{len(findings)} checks, {bad} failed" + ("" if bad else "; none yet is a true answer"))
    return 1 if any(f.state == FAIL for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
