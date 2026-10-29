# 11. Learning

*A proposal, on a branch. The author has not decided whether learning is a chapter or stays as
[SE1/U9](02-unknowing.md#u9). Nothing here is released.*

People learn; rules change; what is is not what was. [SE1/U9](02-unknowing.md#u9) says what a rule
carries: who made it, when, and what would show it wrong. This chapter is how a project learns from
there: in what order to doubt its rules, how to change one, what a finding must change, and who can
see a rule failing. A *rule* here is anything that tells a person or an agent what to do: a
requirement, a scope decision, a convention, a line in an agent file, a checklist item, a principle
in this guide.

### <a id="l1"></a>L1. Doubt in order: the newest rule, then the rule written for a world that has changed, then the most-followed under evidence

*New in v1.4 (unreleased).*

A rule that changed recently has had the least contact with the world, so it is where a K3 is
likeliest ([SE1/U3](02-unknowing.md#u3)); it is also what a summary, a copy, or a newcomer is most
likely to have mangled, since nobody has lived with it yet. When something is wrong and the cause is
not obvious, list the rules that changed since it last worked and doubt them first; `git log --since`
on the working set finds them. This includes the rule you just wrote, and this chapter.

Next come the rules written for a world that has since changed: a new tool, a new cost, a new kind
of reader. A rule fitted to the old world keeps its wording, and with it its authority. Every rule
priced when code was expensive — write it carefully once, a reviewer can read every line — was priced
for a world that has gone ([SE1/A1](10-agents.md#a1)).

Last, and only under evidence, the most-followed. A rule cited often was selected by its successes;
the cases where it misled, nobody recorded, because nobody was looking. Citation count measures how
much a rule is liked, not how often it was right. When evidence contradicts a well-loved rule, the
evidence gets the hearing and the citations do not vote. The cheapest way to have that evidence is to
ask what the rule predicts and check it once against the real thing, not against a model of it: a
guard that only ever ran against its own stub is an endorsement, not a check
([SE1/T3](06-testing.md#t3)).

> **Ask:** "Which rules changed since this last worked, and which of them has anyone measured?"

### <a id="l2"></a>L2. Read a rule's history before you keep or change it; supersede with a reason, never edit silently

*New in v1.4 (unreleased).*

Git keeps what a rule's text cannot: when it arrived, who wrote it, what it replaced, and the commit
message's *why*. `git log -S'<the rule>'` finds the commit that introduced it, and `git blame` gives
the line's last change. A rule whose history says *(inferred)*, or carries no *why*, is a candidate
to measure before it is relied on. This guide's own [SE1/A11](10-agents.md#a11) is the case: a copy
pinned it at a commit made eighteen minutes after it was first written, it changed again the next
morning, and nothing in the copy said how new it was
([GAPS](../GAPS.md#1-a-rule-eighteen-minutes-old-frozen-into-a-copy)).

When a rule turns out wrong, supersede it and say why, so the correction is what the next reader
meets first. Do not edit it away: a silently corrected rule teaches the next reader nothing. This is
[SE1/R10](04-requirements.md#r10), extended from requirements to every rule. A record that cites the
old wording — a finding, a done queue row — keeps its citation: it says what was true when it was
written, and rewriting it would make it false.

> **Ask:** "Who wrote this rule, when, and what did it replace?"

### <a id="l3"></a>L3. A finding that changes no rule, test, or check is a lesson not learned

*New in v1.4 (unreleased).*

`FINDINGS` is the only document reality writes ([SE1/W10](08-work.md#w10)), and the retro's fear
is "we already learned this once" ([SE1/H4](09-people.md#h4)). The fear is retired only when the
finding changes something that will still be there when the people who learned it are not: a rule,
a test, a check that can refuse the change, or a line in the agent file. Every finding therefore ends
with what it changed, or with why it changed nothing, which is itself a decision to record. The
cheapest change is the one that catches the same class of error in a cheaper loop
([SE1/F3](03-feedback.md#f3)).

*Who claims this, and what would show it wrong.* The author proposed it (2026-10-29). Every entry in
this repository's own `docs/FINDINGS.md` carries a *Changed* line, and the template asks for one; no
trial has tested whether findings without one are relearned. *Wrong if:* a project whose findings
change nothing relearns them no more often than one whose findings do.

> **Ask:** "What did the last finding change, and would it hold if everyone here left?"

### <a id="l4"></a>L4. The one who follows a rule is the worst placed to see it failing

*New in v1.4 (unreleased).*

Knowledge moves badly from third person to first. A team can know a rule and still not apply it to
its own work; someone outside the work sees the gap at once. Ask someone who did not write the
change to check it against the rule, **named** ("does this meet R8?"), not in general ("does this
meet the requirements?"), at the moment it matters: before it is registered, merged, or handed
across a gap ([SE1/W11](08-work.md#w11), [SE1/A11](10-agents.md#a11)). Better still, make the rule a
check that can refuse the change. A rule that can refuse you holds; a rule you only read is a
reminder.

*Who claims this, and what would show it wrong.* Measured in one project, with one model, in
2026-10 ([GAPS](../GAPS.md#field-report-agent-tribes-and-checks-2026-10-28)): builders wrote the
encryption requirement into their records in 19 of 20 runs and into their code in none; fresh
readers shown the store saw the plaintext in 5 of 36 reviews against the requirements in general,
and in 31 more once the requirement was named. *Wrong if:* builders checking their own change
against the named rule catch what an outsider does, in a project and model not these. Until then,
L4 is the least proven principle here, and says so.

> **Ask:** "Who, other than the one who made this change, has checked it against the rule by name?"

---

This is the last chapter. The [principle index](../README.md#principle-index) lists every ID.
