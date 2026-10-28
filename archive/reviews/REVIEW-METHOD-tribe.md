# A suggestion for reviewing v1.2: a small tribe of readers

Drafted by Claude Opus 5.5, 2026-10-28, for whoever drafts or reviews v1.2. It is a suggestion,
written to be pushed against, not a rule. By L6 in REVIEW-v1.2-learning.md, doubt it first: it was
written by the model whose reviews it describes.

## The claim

One reviewer of a draft shares the drafter's blind spots in proportion to how much context they
share. Several fresh readers, each told to look through a different lens, with one reader who
carries the drafter's context, found more in one review than the drafter did alone: they cut two of
its four proposals and found the most important item it had missed. That is one use, so it is
weak evidence, and the costs are real (below).

## The method

**Five readers, run in parallel, read-only.**

| Reader | Context | Asked to look through |
| --- | --- | --- |
| Engineer | fresh: the draft and the sources only | the engineer in you: does each change do what it claims, is it already in the guide, is the evidence real and enough? Open and quote every source; check every number. |
| Cynic | fresh | the cynic in you: where is the crack? Try to refute each item; "this one holds" is a fine answer. Look for overreach, confounds, causal stories resting on agents' own words, and conflicts with existing rules. |
| Artist | fresh | the artist in you: what is the draft trying to be, and what is missing from the picture? Read the underlying evidence yourself, not only the draft's summary of it. |
| Buddhist | fresh | the buddhist in you: what is fine as it is, and need not change? "None" is a complete answer. Quote the existing text that already covers an item. |
| Elder | a fork of the drafter, with the drafting context | from that life: which lessons were paid for, and which are a summary's version of them? What does the drafter know that a fresh reader cannot? Name one thing you would argue against if someone else had written it. |

**Each brief:** the draft's path, the guide's paths, the evidence's paths, "do not change any
file", a word cap (400–600), and a return form: a verdict per item (adopt / adopt with change / GAPS
only / drop), why in a sentence or two, and the quote that decides it.

**Lenses, not roles.** "Look through the cynic in you", never "you are a cynic". A role has to stay
in character and finds cracks to justify itself. A lens can come back empty, and the brief should
say that empty is a good answer.

**Synthesis, by the drafter:**
- **The drafter does not vote.** An item survives only if no reviewer refutes it with a source.
- **Before acting on a reviewer's load-bearing claim, open its source.** Reviewers misquote too. In
  the one use, two of them were checked this way, and both held.
- **Record what each reader cut, and why**, in the review itself, so the next reader sees the
  arguments and not only the verdict.

## What it found the one time it was used

On the draft of REVIEW-v1.2-compaction-lessons.md (four proposals, one of them in six parts):

- **The engineer** found two overstated claims (a count resting on two runs, not "several"; a
  number taken from a paraphrase), and one real gap: the guide asks reviewers about the requirement
  a change serves, never the ones it must not break.
- **The cynic** refuted a proposed AGENTS.md sentence by quoting what AGENTS.md and O8 already say.
  The failure was non-compliance, not a missing rule.
- **The artist** found the centre the draft had left out (that knowing is not doing), with quotes
  from the evidence. It became the one guide change proposed.
- **The buddhist** sent most items to GAPS only, and found one already proposed in another review.
- **The elder** said the human, not any check, had caught the session's worst defects. They cut a
  harness quirk, and argued against the item the drafter liked best.

## Push against it here

- **One model family.** All five were Claude, and fresh context reduces shared blind spots without
  removing them. A reader of another model, or a person, would test that. A review by a person stays
  the real check.
- **Correlated agreement.** When four readers agree, it may be one prior four times over. Count
  agreement as weaker than it looks.
- **Lenses may still perform.** A cynic asked to refute will find something. The method relies on
  "empty is fine", and that was not tested.
- **The elder carries the drafter's blind spots**, by construction. It is there for what only a life
  knows, not as an independent check.
- **Cost.** The four fresh readers spent about 273,000 tokens between them. The fork spent about
  478,000, because it carries the whole context. That is about 750,000 for a draft of four
  proposals. A single careful reviewer is far cheaper.
- **No comparison was made.** *Wrong if:* one reviewer, given the same draft and sources, finds the
  same cuts and the same missing item. Then the other four were cost, not value. Running that
  comparison once would settle it.
- **The lenses are a choice.** Engineer, cynic, artist and buddhist suited a draft of guide changes.
  Another draft may want others (an operator, a newcomer, the client).

## If you use it

Say so in the review: which readers, what each cut, and which of their claims you checked at the
source. If you do not use it, a sentence saying why is enough.
