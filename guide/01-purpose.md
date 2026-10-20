# 1. Purpose

What engineering is for, what "reliable" means, and why every practice in this guide should be able
to name the fear it retires.

---

### <a id="p1"></a>P1. Engineers make reliable things, on time, within resource constraints, managing discomfort for the team, the client, and the users

Four constraints that trade against each other — reliability, time, resources, discomfort — and a
fifth, **scope**, which is usually the honest one to move. A plan that does not say which of them is
fixed is not a plan; it is a wish with dates attached.

> **Ask:** "Which of these is fixed, and which one moves when we are wrong?"

### <a id="p2"></a>P2. Reliable is not correct

Correctness is a property of a program measured against a specification. Reliability is a property
of a system running in a world that contains bad inputs, hostile inputs, failing hardware, wrong
clocks, partial networks, and people. The gap between the two words is where most of the work is.

A working definition, from embedded systems, where nobody can afford to be vague:

> **A reliable thing works when it is in good repair and used correctly, and has detectable error
> status when it is broken or misused.**

The definition has two halves: *it works*, and *it says so when it does not*. Most testing effort
goes to the first half. The second half — a failure nobody can see — is what turns a small fault
into a long outage, because nothing starts the repair.

Reliability also compounds downward. N independent parts, each working with probability P, work
together with probability Pᴺ. Ten parts at 90% is 35%. For ten parts to give 99%, each must be
99.9%. **When every part must work, bigger systems need more reliable parts.** (Redundancy — two
parts where either will do — is the other way out, and it only helps if the two do not fail for the
same reason.)

> **Ask:** "When this is broken, how does anyone find out?"

### <a id="p3"></a>P3. Discomfort is a leading indicator

| Whose      | What it looks like                              | What reduces it                          |
| ---------- | ----------------------------------------------- | ---------------------------------------- |
| The users  | confusion, wasted time, distrust of the answer  | the product actually being good          |
| The client | surprise                                        | frequent, honest, boring status          |
| The team   | fear, thrash, heroics, weekends                 | slack, small steps, reversible decisions |

This is not about comfort as a goal. Fear degrades judgment, and a frightened team abandons exactly
the practices that would have prevented the fear. Discomfort is usually the earliest signal
available, arriving weeks before the schedule shows anything. Someone going quiet at stand-up is
data.

> **Ask:** "Who is uncomfortable right now, and what are they afraid of?"

### <a id="p4"></a>P4. Every practice retires a named fear

Backups, version control, tests, review, short iterations, demos, staging. Each is usually taught as
a rule. Each is better understood as a way of retiring one specific fear — and you should be able to
name which.

| Practice                | The fear it retires                          |
| ----------------------- | -------------------------------------------- |
| Backups                 | "I could lose the work."                     |
| Version control         | "I can't get back to when it worked."        |
| Tests                   | "I don't know if I just broke something."    |
| Continuous integration  | "It works on my machine."                    |
| Short iterations        | "We are building the wrong thing."           |
| Client demos            | "They will hate it in month six."            |
| Code review             | "Only one person understands this."          |
| Signed commits          | "Nobody vouched for this code."              |
| Fault injection         | "I don't know what happens when it breaks."  |

Two consequences, and both are load-bearing:

- **A practice that reduces no one's anxiety will be abandoned under pressure** — and should be.
  Ceremony that costs time and returns no relief gets dropped in week ten. If you cannot name the
  fear a practice retires, find it or stop doing it. Count the fears of people who are not in the
  room — users, bystanders, the people whose data you hold ([SE1/R8](04-requirements.md#r8)) — not
  just the team's.
- **A practice that reduces anxiety without reducing risk is worse than nothing.** A backup nobody
  has restored. A test suite that cannot fail. A green dashboard measuring the wrong thing. These
  are the most dangerous artifacts in engineering, because they quiet the alarm and leave the danger
  in place.

> **Ask:** "Which fear does this practice retire — and does it retire the risk, or only the fear?"

### <a id="p5"></a>P5. The deliverable is not the code

It is the code plus the ability of someone else to run it, reset it, deploy it, diagnose it at 3am,
and continue it in month seven. "It works on my machine" is a claim about a machine.

Over a system's life, maintenance usually costs more than the first build — most code is read and
changed far more often than it is written — and the reader you are writing for is most often
yourself, having forgotten. So the property being engineered is the **cost of the next change**.
Anyone can write the first version. A design shows its worth in the second, which is also when
nobody remembers why the first was shaped that way — so write that down while you still know.

> **Ask:** "Could someone who has never met me run, reset, and fix this from what is in the
> repository?"

---

## Why software is different

Two facts separate software from the older engineering disciplines, and most of this guide follows
from them:

- **Tests are cheap.** You cannot build a second bridge to find out whether the first one holds. You
  can run a suite a thousand times before lunch. Nearly every modern practice is downstream of that
  ([SE1/F1](03-feedback.md#f1)).
- **Software has no mass.** Nothing sags or cracks to tell you it is wrong, so every signal a
  physical structure gives away for free has to be built on purpose ([SE1/F4](03-feedback.md#f4)).
  And nothing occupies the space another part will need, so most schedule dependencies are optional
  ([SE1/W5](08-work.md#w5)).

The two pull in opposite directions. Cheap tests make certainty affordable; the absence of mass
makes it necessary to go buy some, because a bad design will hold itself up indefinitely, at full
speed, with the tests passing.

---

Next: [2. Unknowing](02-unknowing.md) — the five kinds of not-knowing, and which one to fear.
