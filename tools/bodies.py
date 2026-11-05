"""Shared by tools/check.py and tools/since.py: what a principle's heading and marker look like, and
what counts as its text. One place, so the two tools can never disagree about it."""
import re

# Whitespace as the checker has always meant it, spelled out because Python's \s differs at the edges.
WS = "\t\n\x0b\x0c\r \u00a0\u1680" + "".join(map(chr, range(0x2000, 0x200b))) + "\u2028\u2029\u202f\u205f\u3000\ufeff"
_RUN = re.compile(f"[{WS}]+")

# The SE1/ is optional because older tags have none; tools/check.py requires it in the tree.
_CITED = re.compile(r"(</a>)SE[0-9]+/")
HEADING = re.compile(r'^### <a id="([a-z0-9]+)"></a>(?:SE[0-9]+/)?([A-Z][0-9]+)\. ([^\n\r\u2028\u2029]*)$')
# The marker is the first paragraph under a heading. New/Changed is a person's claim that the
# release changed the principle's meaning; Since is written by tools/since.py when no such claim
# exists. Each carries the release's date, and, when the wording moved later without the meaning,
# the text's own since. tools/since.py writes and checks them against the release tags.
MARKER = re.compile(
    r"^\*(New|Changed|Since) (?:in )?(v[0-9]+\.[0-9]+(?:\.[0-9]+)?)"
    r"(?: \(([0-9]{4}-[0-9]{2}-[0-9]{2}|unreleased)\))?"
    r"(?:; text since (v[0-9]+\.[0-9]+(?:\.[0-9]+)?) \(([0-9]{4}-[0-9]{2}-[0-9]{2}|unreleased)\))?\.\*$"
)
_ANY_HEADING = re.compile(r"^#{1,3} ")


def read(path):
    """A file's text, exactly: no newline translation, so a compare with git's bytes is honest."""
    with open(path, encoding="utf-8", newline="") as fh:
        return fh.read()


def collapse(text):
    return _RUN.sub(" ", text).strip(WS)


def bodies(text):
    """A principle's text: its heading to the next heading or horizontal rule, without its marker,
    whitespace collapsed so rewrapping is not a change, and the heading's SE1/ left out so adding it was not one. The rule matters: the `---` after a chapter's
    last principle is not its text, or adding a principle after it would "change" it (v1.2's A10)."""
    out = {}
    current, buf = None, []

    def flush():
        if current:
            out[current] = collapse(" ".join(l for l in buf if not MARKER.search(l)))

    for line in text.split("\n"):
        m = HEADING.search(line)
        if m or _ANY_HEADING.search(line) or line == "---":
            flush()
            current, buf = (m.group(2) if m else None), []
        if current:
            buf.append(_CITED.sub(r"\1", line, count=1) if m else line)
    flush()
    return out
