# Archive

The sources behind the guide's claims, kept so that a review can check a citation without fetching
it again, and so that a later reader can tell whether a source has changed since it was read
([SE1/D13](../guide/05-design.md#d13)). Retrieving and reading sources was the costliest step of the
v1.1 and v1.2 reviews; this directory is the memory of that work.

One file per source, or per fetch of a set of pages that change together, holding:

- **Supports:** the principle or GAPS entry the source is cited for, by versioned ID.
- **Source:** the citation, and the URL it was fetched from.
- **Retrieved:** the date, and by whom (a person, or a model and version).
- **SHA-256** of the bytes retrieved, and their size. Re-fetch the URL and run `shasum -a 256` on
  the result: a match means you hold what the review read; a mismatch means the source changed, and
  the extraction below is what was true on the date.
- **Stored:** whether the full file is kept here. It is kept only when its license allows
  redistribution; otherwise the checksum stands in for it.
- **Status:** *verified* when the reviewer opened the source; *not opened* when the entry records
  what a secondary account or a delegated check reported, so the next reviewer knows what is owed.
- **Extraction:** the passage the claim rests on, quoted exactly, with its page or location, and
  no more than a review needs. The extraction is what a reader checks the guide against.

A private source, such as a repository the public cannot open, gets its commit and git blob hash
instead of a URL: anyone with access can confirm the lines, and anyone without can read the
extraction and knows exactly what they are trusting.

A review cites an entry by linking it. To add one: fetch with `curl -sL -o <file> <url>`, hash with
`shasum -a 256 <file>`, quote the passage, say which claim it supports, and say whether you opened
the source yourself.

| Entry | For |
| --- | --- |
| [royce-1970.md](royce-1970.md) | SE1/W2: where Royce's warning sits |
| [brown-1948.md](brown-1948.md) | SE1/W7: the avoidance-gradient experiment (not opened) |
| [ambig-swe-2025.md](ambig-swe-2025.md) | GAPS related work: the 74% figure |
| [humanevalcomm-2024.md](humanevalcomm-2024.md) | GAPS related work: code instead of questions |
| [pair-programming-studies.md](pair-programming-studies.md) | GAPS related work: the 90% and 15/15 claims (not opened) |
| [claude-code-docs-2026-10-28.md](claude-code-docs-2026-10-28.md) | SE1/A11, ADOPT.md, GAPS: what Claude Code documents |
| [compaction-findings-2026-10-28.md](compaction-findings-2026-10-28.md) | GAPS field reports of 2026-10-28, SE1/A11, SE1/U9: the lines relied on |
