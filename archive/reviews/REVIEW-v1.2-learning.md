# Review: a proposed chapter on learning (rules change; what is is not what was)

Reviewer: Claude Opus 5.5, at the author's request. Date: 2026-10-28. By L6 below, a later model,
or a later version of this one, should doubt what this review proposes before the rest of the guide.
Against: branch `v1.2/after-a-gap` at d256d10. Status: **a proposal**. *Note, 2026-10-29: the L-numbers below are this draft's own six; the chapter as later proposed on the branch `proposal/learning-chapter` has four, numbered differently, so a bare "draft L5" here is not a citation of the guide.* No chapter, index, changelog
or checker file is edited. Everything below was observed unless it says *inferred*.

## The gap

The author, 2026-10-28: "a missing section of ../software-engineering is self-improvement. People
learn, rules change, and what is is not what was. Rules, especially recently changed ones, should
be questioned. rules endorsed often should be doubted under evidence. Git nicely keeps history."

The guide already records what was learned: FINDINGS ([SE1/W9](../../guide/08-work.md#w9)), the retro (in
[SE1/H4](../../guide/09-people.md#h4)'s table of meetings), asking agents ([SE1/A10](../../guide/10-agents.md#a10)). It versions
requirements ([SE1/R10](../../guide/04-requirements.md#r10)), and it names the things that say "fine"
with no way to say "wrong" ([SE1/U7](../../guide/02-unknowing.md#u7)). What it does not do is turn that on
**its rules**: the conventions, the agent files, the checklists, the decisions in USER_STORIES,
and its own principles. A rule in this guide's sense arrives with no date, no source, no record of
whether anyone measured it, and the same voice as every rule around it. Nothing says which rules
to doubt first, or how much an often-cited rule has earned.

## Evidence that it costs something

Each of these is a rule read with more authority than it had. I checked each source, except where
a line says otherwise.

- **This guide's A11 was 18 minutes old when it was frozen into a trial.** It was written in
  e1635f0 (2026-10-26 12:17) and rewritten in 594fadb (12:35). The compaction project's trials pin
  the guide at 594fadb (`trials/handoff-viki-se1/run.py`, `GUIDE_COMMIT`), so every member there has
  loaded a rule that changed 18 minutes before and changed again the next morning (d256d10). Nothing
  in the copy says how new it is.
- **A requirement that was an inference.** A field note left in *Life by the Numbers*
  (`llm/field-note-confident-error.md`, untracked in that repository) reports that "viki never forks
  — it can't on iOS" was written into a CLAUDE.md by an agent, never measured, and read for weeks
  "with precisely the authority of the sentence two paragraphs below it, which reports a measurement
  with a repro you can run." The owner retired it in one sentence: "even if i write a requirement
  does not mean it is correct." I did not check the original project's history.
- **A rule restated loses its content.** The viki snapshot's CLAUDE.md lists "D-9 Fossil is pinned
  at 2.28". USER_STORIES.md, D-9's source, says "**Encryption at rest** everywhere via the fossil-see
  build … Pins Fossil 2.28". The summary kept the pin and dropped the rule. In the compaction trials,
  no store of 50 was encrypted, and only a fresh reader shown D-9 *named* reliably saw the plaintext
  (31 of 36; 5 of 36 from "the requirements" in general; compaction repository, FINDINGS, DESIGN_v8).
- **A rule used often, wrong in a case nobody had seen.** That project's at-rest guard (v2) passed
  every test for two batches. The tests ran it against the guard's own stub of viki, and the stub
  printed a ledger viki never prints (compaction repository, `e4b2fe4`, DESIGN_v8). Its use was the
  endorsement, and the evidence that would have doubted it was one byte-comparison away.
- **Rules held as a record, not a check, hold less.** In the same trials, members wrote D-9 into
  their own journals in 19 of 20 runs and into their code in none. One store changed when a check
  refused it at a pause (H-10, by a Stop hook).

## Where it goes

**Recommended: a new chapter, 11. Learning, letter L.** It is not part of Work (how a team
schedules), Requirements (one kind of rule) or Agents (one kind of reader). It is about every rule
the other ten chapters produce, the guide's own included. *Alternative, if a new letter is too much
for a minor release:* add the principles to Work as W13–W17. That is the smaller change, but it files a cross-cutting idea under one chapter.
*Smallest, and close:* L1 alone as a new U8, L3's point added to U3, and R10 extended from
requirements to every rule. The familiar asked what the new letter adds beyond L1, since L2 overlaps
U3, L4 extends R10 and L5 leans on W11 and A11. My answer: the subject. The guide's rules about
rules would then live in one place, read together, and L3 (endorsement is not evidence) has no
home today. But the call is close, and the smallest option loses little.

A new chapter within SE1 is allowed by the index's rules: a minor release "may add principles … it
never moves an ID". What it touches is listed under *Changes this would need*.

## The draft chapter

Written to be cut. The titles carry the claim; the bodies are as short as I could make them. L6
was added after the author's review of this draft.

---

# 11. Learning

People learn; rules change; what is is not what was. A rule is anything that tells a person or an
agent what to do: a requirement, a decision, a convention, a line in AGENTS.md, a checklist item, a
principle in this guide. Every one of them was written by someone at some point, for a reason that
may have moved. This chapter is about keeping rules honest about where they came from.

### <a id="l1"></a>L1. Every rule says who made it, when, and what would show it wrong

*New in v1.2.*

A rule in the present tense speaks in one voice. "We never fork" reads the same whether someone
measured it or guessed. So write three things beside a rule that will be relied on: **who claimed
it** (measured, decided by a named person, or inferred), **when**, and **what would show it wrong**.
A rule with no falsifier is a mood handed on with a rule's grammar. If you cannot write the
falsifier, that is the finding; write that instead. The *who* matters most for agents, which write
fluent rules quickly and cannot later tell their own inference from a measurement
([SE1/A2](../../guide/10-agents.md#a2)). The *who* is [SE1/D13](../../guide/05-design.md#d13)'s question, asked of a rule;
what L1 adds is the *when* and the falsifier, and D13 says itself that knowing who said a thing is
"not that it is *true*".

### <a id="l2"></a>L2. Question the newest rules first

*New in v1.2.*

A rule that changed recently has had the least contact with the world, so it is where a K3 is
likeliest ([SE1/U3](../../guide/02-unknowing.md#u3)). It is also what a summary, a copy or a newcomer is most
likely to have mangled, since nobody has lived with it yet. When something is wrong and the cause is
not obvious, list the rules that changed since it last worked, and doubt them before the old ones.
`git log --since` on the working set finds them. This includes the rule you just wrote, and this
chapter.

### <a id="l3"></a>L3. Endorsement is not evidence; a much-cited rule still answers to it

*New in v1.2.*

A rule that is cited often has been selected by its successes. The cases where it misled nobody
recorded, because nobody was looking. Citation count measures how much a rule is liked, not how
often it was right. When evidence contradicts a well-loved rule, the evidence gets the hearing, and
the citations do not vote. The cheapest way to have that evidence is to ask what the rule predicts
and check it once against the real thing, not against a model of it. A test that only ever ran
against its own stub cannot fail where it matters, so it is an endorsement, not a check
([SE1/T3](../../guide/06-testing.md#t3)).

### <a id="l4"></a>L4. Read a rule's history before you keep it or change it

*New in v1.2.*

This guide's own A11 shows why. `git log -- guide/10-agents.md` gives its history: written in
e1635f0 at 12:17 on 2026-10-26, rewritten in 594fadb at 12:35, and changed again the next morning in
d256d10. A project that copied the guide at 594fadb froze a rule that was 18 minutes old, and its
copy cannot say so. Git kept that history; nothing else did.

Git keeps what a rule's text cannot: when it arrived, who wrote it, what it replaced, and the
commit message's *why*. `git log -S'<the rule>'` finds the commit that introduced it, and
`git blame` gives the line's last change. A rule whose history says "inferred", or carries no *why*,
is a candidate to measure before it is relied on. When a rule turns out wrong, supersede it and say
why, so the correction is what a reader meets first. Do not edit it away: a silently corrected rule
teaches the next reader nothing ([SE1/R10](../../guide/04-requirements.md#r10), extended from requirements to
every rule).

### <a id="l5"></a>L5. The one who follows a rule is the worst placed to see it failing

*New in v1.2.*

Knowledge moves badly from third person to first. A team can know a rule and still not apply it to
its own work; someone outside the work sees the gap at once. Ask someone who did not write the
change to check it against the rule, **named** ("does this meet R8?"), not in general ("does this
meet the requirements?"), at the moment it matters: before it is registered, merged or handed
across a gap ([SE1/W11](../../guide/08-work.md#w11), [SE1/A11](../../guide/10-agents.md#a11)). Better still, make the rule a
check that can refuse the change. A rule that can refuse you holds; a rule you only read is a
reminder.

*Who claims this, and what would show it wrong (L1, applied to L5).* It was measured in one
project, with one model (Claude Haiku), in 2026-10. Builders wrote D-9 into their records in 19 of
20 runs and into their code in none. Fresh readers shown the store saw the plaintext in 5 of 36
reviews against the requirements in general, and in 31 more once D-9 was named. *Wrong if:* builders
checking their own change against the named rule catch what an outsider does, in a project and model
not this one. Until then, L5 is the least proven principle here, and says so.

### <a id="l6"></a>L6. When the world changes, the rules written for the old one are the first suspects

*New in v1.2.*

L2 says to doubt the newest rules first. Evidence that the world changed says to doubt the old ones
too: a new tool, a new cost, a new kind of reader. A rule fitted to the old world keeps its wording,
and with it its authority. The obvious example is agents. Producing code got cheaper faster than
knowing it is right ([SE1/A1](../../guide/10-agents.md#a1)), and every rule priced when code was expensive
(write it carefully once; a reviewer can read every line) was priced for a world that has gone.

**A rule written by an agent says so, and names the agent.** An agent's rules carry its model,
version and date, and the next agent doubts them first. Their author's blind spots are the reader's
own, so a rule from the same model reads as authority it has not earned. Agents also change fast,
which is the change L6 is about. This guide's AGENTS.md is the case in point: every commit to it was
co-authored by an agent (Claude Opus 5.5), and it is obeyed by agents, that model among them. Prompting advice has "a short shelf life — this chapter's
included" ([SE1/A10](../../guide/10-agents.md#a10)), and that applies to the agreement too.

*Who claims this, and what would show it wrong.* The author proposed it (2026-10-28). The
authorship is measured: all 12 commits to AGENTS.md, from 2026-10-19 to 2026-10-27, carry
`Co-Authored-By: Claude Opus 5.5`, and the file's text does not say so. That doubting agent-written
rules first finds errors sooner is **inferred**, not measured. *Wrong if:* in a project that marks its
agent-written rules, those rules turn out no more often wrong than the human-written ones.

---

## Changes this would need

- **README.md:** the chapter in *Contents*, the letter in the index sentence ("**L**earning"), and
  L1–L6 in the *Principle index*. One of the *Twelve questions*, perhaps: "Which rule here changed
  last, and who measured it?" → SE1/L2.
- **tools/check.js:** the chapter letters it accepts (line 116 says "Only the chapter letters
  count"). I have not read how it finds chapters, so there may be more. The checker should go red
  on L-citations until this is done, and that is worth seeing first ([SE1/T3](../../guide/06-testing.md#t3)).
- **CHANGELOG.md, v1.2 — unreleased, New:** L1–L6. *For copies:* nothing to re-copy unless
  AGENTS.md gains the line below.
- **AGENTS.md:**
  - **Under its title, who wrote it**, for example: "Drafted by Claude Opus 5.5 with Warren MacEvoy,
    2026-10. A later model, or a later version of this one, should doubt these rules before
    following them, and say which it doubted (draft L6)." Today the file says nothing of its authorship,
    which git records for all 12 of its commits.
  - **Under *Before you start*:** "A rule that changed recently, that you are about to rely on
    heavily, or that was written for a world that has since changed, gets its history read before it
    is obeyed (draft L2, L4, L6)."
  - Both change every copy, so they are a stop-and-ask for the author, not a reviewer's edit.
  - One rule to look at first under L6: *keys* as a stop-and-ask. In the compaction trials, members
    gave it as the reason they did not encrypt a store that D-9 required. The rule may be right, and
    the fix is for the owner to answer the key question. But it is an agent-written rule binding
    agents, and L6 says to look at it first. This is suggestive (quotes, and one spike run), not
    measured.
- **CHECKLISTS.md:** a line in the review checklist, "the change was checked against the rules it
  touches, by name, by someone who did not write it (draft L5)".
- **GLOSSARY.md:** *rule*, as defined in the chapter's opening, if the word needs pinning.
- **GAPS.md:** the evidence above belongs there as a field report, with its sources, in the form the
  existing reports use.

## Questions for the author

1. **New chapter or W13–W17?** I recommend the chapter, and the alternative is smaller.
2. **Is L5 a principle here, or does it belong in People (H) as a review practice?** It is the
   least proven of the five: its evidence is one project's probe and trials, all with one model.
3. **L1 asks for three things beside every relied-on rule.** Is that too much for a requirement
   line? The lightest form may be a `(measured: …)` or `(inferred)` tag, with the history in git.
4. **Should every L principle carry its own "who claims this, wrong if" line**, as L5 now does?
   L1 asks it of every rule, and a chapter that exempts itself teaches the opposite. It is heavier
   than the guide's usual style, where evidence lives in GAPS.

5. **L6 names the agent; should L1's *who* do the same everywhere?** That would mean a rule in any
   file carries "(drafted by <model>, <date>)" when an agent wrote it, not only in AGENTS.md. Git
   already records it in the trailer. The question is whether the reader should meet it in the text.

## What I did not do

- I did not edit any chapter, the index, the changelog, AGENTS.md or the checker, and did not run
  `node tools/check.js` against a draft chapter, since none was added.
- I did not commit. `ADOPT.md` and `REVIEW-v1.1-fable.md` in this checkout are not mine, and I left
  them alone.
- I checked the A11 timestamps, the D-9 wording and the compaction findings at their sources. The
  field note's account of its original project I did not check.
- I ran it past the compaction project's familiar (`hooks/familiar.py`), a Haiku reader with no
  stake in it. Its cynic, artist and buddhist lenses caught L5 breaking L1, asked for A11's history
  inside the chapter, and asked what the new letter adds. All three are answered above. A review by
  a person, which is L5's real check, is still owed.
