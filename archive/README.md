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

## Reviews

A review of the guide is a proposal, not a change: what survives it goes into the principles,
GAPS, and the CHANGELOG, and the review itself is kept here so the arguments outlive the verdict
([SE1/A3](../guide/10-agents.md#a3): chat does not survive the session). Each says who reviewed,
what was opened, and what was only read.

| Review | What it is |
| --- | --- |
| [REVIEW-v1.1-fable.md](reviews/REVIEW-v1.1-fable.md) | v1.1 and the first v1.2 branch, reviewed 2026-10-27: four items before tagging, content findings, sources checked, the Claude Code facts behind A11 |
| [REVIEW-v1.2-learning.md](reviews/REVIEW-v1.2-learning.md) | a proposed chapter of six principles on learning, 2026-10-28; v1.2 took one of them as U9 |
| [REVIEW-v1.2-compaction-lessons.md](reviews/REVIEW-v1.2-compaction-lessons.md) | what the compaction trials should change, 2026-10-28, reviewed by a tribe of readers |
| [REVIEW-METHOD-tribe.md](reviews/REVIEW-METHOD-tribe.md) | the tribe-of-readers method, offered to be pushed against |
| [REVIEW-v1.2-candidate.md](reviews/REVIEW-v1.2-candidate.md) | the v1.2 drafter's trace: decisions, commits, the three readers' results, the release |
| [REVIEW-v1.2.1-codex.md](reviews/REVIEW-v1.2.1-codex.md) | the first review by an agent of another family (OpenAI Codex, 2026-10-28, three minutes): AGENTS.md against its own rules, and how it works in that runner |
| [REVIEW-METHOD-other-family.md](reviews/REVIEW-METHOD-other-family.md) | how that review was set up and read, with the brief verbatim, so the next can be run the same way; the planted-defect run still to make |
