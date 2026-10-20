# Software Engineering

A guide to building reliable, tested, maintainable software — written for humans and for the AI
agents working beside them.

It is organized as **numbered principles** (`T3`, `D2`, `R6`, …). Each states one idea and says why
it is true; most end with a question you can ask out loud in a meeting or a code review. The IDs are
stable so that people and agents can cite them: *"this test has never been seen red (T3)"*, *"this
copy of the user list can go stale; how stale? (D2)"*.

## The argument in ten lines

1. **Engineering is making reliable things** on time, within constraints, while managing everyone's
   discomfort. Reliable means it works — *and says so when it doesn't*
   ([P1](guide/01-purpose.md#p1), [P2](guide/01-purpose.md#p2)).
2. **Every practice retires a named fear.** A practice that retires none gets dropped; one that
   relieves the fear without reducing the risk is worse than nothing ([P4](guide/01-purpose.md#p4)).
3. **Building is discovering what you didn't know**, in the right order, at the right price. The
   dangerous kind is confident and wrong, and only reality or another person finds it
   ([U2](guide/02-unknowing.md#u2), [U3](guide/02-unknowing.md#u3)).
4. **Software's tests are cheap, and software has no mass.** The first makes certainty affordable;
   the second makes it necessary, because a bad design never sags or cracks
   ([F1](guide/03-feedback.md#f1), [F4](guide/03-feedback.md#f4)).
5. **Nobody hands you the problem.** Write requirements specific enough to be wrong, and get them
   rejected early ([R1](guide/04-requirements.md#r1), [R2](guide/04-requirements.md#r2)).
6. **Every input can be absent, late, wrong, or lying**, and each case needs a stated answer
   ([R6](guide/04-requirements.md#r6)).
7. **State is the material.** Name your caches, own your copies, and keep logic away from I/O
   ([D1](guide/05-design.md#d1), [D2](guide/05-design.md#d2), [D7](guide/05-design.md#d7)).
8. **A test you have never seen fail proves nothing**, and a flaky one is worse than none
   ([T3](guide/06-testing.md#t3), [T4](guide/06-testing.md#t4), [T5](guide/06-testing.md#t5)).
9. **Choose the method per decision by the cost of being wrong once**: loop fast around reversible
   choices, slow down around one-way doors ([W4](guide/08-work.md#w4),
   [D11](guide/05-design.md#d11)).
10. **Nothing important may live only in a head** — because teammates leave, and agents were never
    in the room ([U6](guide/02-unknowing.md#u6), [W10](guide/08-work.md#w10)).

## How to read it

**People:** read the chapters in order the first time; each assumes the ones before it. After that,
use the index below and [CHECKLISTS.md](CHECKLISTS.md). Terms used precisely are in
[GLOSSARY.md](GLOSSARY.md).

**Agents:** read [AGENTS.md](AGENTS.md) — the working agreement — before acting in a repository that
follows this guide. Then read the chapter that bears on the task (design → 5, tests → 6, deploys and
production → 7). Cite principles by ID when you raise a concern or explain a choice.

**Teams adopting it:** copy [AGENTS.md](AGENTS.md) into your repository (or point your agent's
instruction file at it), and start your working set from the templates listed under [Contents](#contents).

## Contents

| Chapter                                     | Answers                                                         |
| ------------------------------------------- | --------------------------------------------------------------- |
| [1. Purpose](guide/01-purpose.md)           | what engineering is for, and what "reliable" means              |
| [2. Unknowing](guide/02-unknowing.md)       | the five kinds of not-knowing (`K0`–`K4`), and which to fear    |
| [3. Feedback](guide/03-feedback.md)         | what a test costs, and why software must build its own signals  |
| [4. Requirements](guide/04-requirements.md) | where the problem comes from, and how to write it down          |
| [5. Design](guide/05-design.md)             | state, complexity, coherence, interfaces, and carrying cost     |
| [6. Testing](guide/06-testing.md)           | tests worth trusting                                            |
| [7. Operating](guide/07-operating.md)       | environments, CI, observability, failure handling, deploys, migrations, security, incidents, releases you cannot roll back |
| [8. Work](guide/08-work.md)                 | the shape of the work: loops, waterfalls, deadlines, done       |
| [9. People](guide/09-people.md)             | the team, the client, and what passes between them              |
| [10. Agents](guide/10-agents.md)            | what changes when a teammate has no memory and no stake         |

| Reference                          | For                                                             |
| ---------------------------------- | --------------------------------------------------------------- |
| [AGENTS.md](AGENTS.md)             | the working agreement for agents, portable to any repository    |
| [CHECKLISTS.md](CHECKLISTS.md)     | every checklist, in the order a project meets them              |
| [GLOSSARY.md](GLOSSARY.md)         | the terms used precisely                                        |
| [READING.md](READING.md)           | the longer arguments, one line each                             |
| `templates/`                       | starting points: [REQUIREMENTS](templates/REQUIREMENTS_v1.md), [DESIGN](templates/DESIGN_v1.md), [QUEUE](templates/QUEUE.md), [FINDINGS](templates/FINDINGS.md), [CONTRIBUTING](templates/CONTRIBUTING.md) |
| [GAPS.md](GAPS.md)                 | where the guide fell short in the field, and how each gap was closed |

## The running example

Examples throughout come from one system, so they can build on each other: **a parking-occupancy
service** for a stadium's lots.

- **Lots and sensors.** About a hundred lots and a hundred thousand spaces. Each lot has one sensor
  that reports how many spaces are free, every five seconds — twenty readings a second in all.
- **The collector** polls every sensor, checks each reading, and decides whether that lot's count is
  `live`, `stale` (too old to trust), or `unreachable`.
- **The app** shows drivers which lots have space, and gives operators a screen of their own.
- **Signed readings.** Each sensor signs its readings with its own private key; a **device
  registry** holds the matching public keys, so anyone can check later which sensor sent a reading
  and that it was not altered.
- **A control plane for faults.** In tests, a sensor can be told to misbehave on request — go
  silent, answer slowly, freeze its count, report nonsense, flap, or drift its clock — so the
  handling of each failure can be seen to work.
- **The client** is the stadium's operations manager, who wants "an app that shows which lots have
  spaces."

A complete worked version, with requirements, design, and code, lives in the
[fall 2026 course repository](https://github.com/wmacevoy/software-engineering-wmacevoy-fall-2026).
Its requirement IDs (such as `T-3`) are that project's own and unrelated to this guide's principle
IDs (such as `T3`).

## Principle index

IDs are permanent from the first published version of this guide. A principle may be reworded, but
its ID never moves to a different idea; a retired principle keeps its ID with a note saying where
its content went, and new principles take the next number in their chapter. The letters are the
chapters: **P**urpose, **U**nknowing, **F**eedback, **R**equirements, **D**esign, **T**esting,
**O**perating, **W**ork, **H**umans (people), **A**gents. (Requirement IDs in your own project
should use a different form, such as `UI-1`, so they are never confused with these.)

**[1. Purpose](guide/01-purpose.md)**

- [**P1**](guide/01-purpose.md#p1) Engineers make reliable things, on time, within resource constraints, managing discomfort for the team, the client, and the users
- [**P2**](guide/01-purpose.md#p2) Reliable is not correct
- [**P3**](guide/01-purpose.md#p3) Discomfort is a leading indicator
- [**P4**](guide/01-purpose.md#p4) Every practice retires a named fear
- [**P5**](guide/01-purpose.md#p5) The deliverable is not the code

**[2. Unknowing](guide/02-unknowing.md)**

- [**U1**](guide/02-unknowing.md#u1) K0 through K3 are in order of expense; K4 is a choice
- [**U2**](guide/02-unknowing.md#u2) Building is discovering, in the right order and at the right price, which category each part of the problem belongs to
- [**U3**](guide/02-unknowing.md#u3) K3 is the one to be afraid of
- [**U4**](guide/02-unknowing.md#u4) Every abstraction rests on chosen falsehoods; write down where they are load-bearing
- [**U5**](guide/02-unknowing.md#u5) Estimate the category, not the task
- [**U6**](guide/02-unknowing.md#u6) Nothing important may live only in a head

**[3. Feedback](guide/03-feedback.md)**

- [**F1**](guide/03-feedback.md#f1) The cost of a test decides the method
- [**F2**](guide/03-feedback.md#f2) The cost of a test is designed, not given
- [**F3**](guide/03-feedback.md#f3) Push each class of error down to the cheapest loop that can catch it
- [**F4**](guide/03-feedback.md#f4) Nothing has mass, so build the signals
- [**F5**](guide/03-feedback.md#f5) When a measure becomes a target, it stops measuring

**[4. Requirements](guide/04-requirements.md)**

- [**R1**](guide/04-requirements.md#r1) Keep the pain; test the solution
- [**R2**](guide/04-requirements.md#r2) Specific and wrong beats vague and safe
- [**R3**](guide/04-requirements.md#r3) Ask the questions nobody volunteers — the ones that could invalidate the plan, first
- [**R4**](guide/04-requirements.md#r4) A requirement with no price attached is a wish
- [**R5**](guide/04-requirements.md#r5) A requirement says what must be observably true; a design says how
- [**R6**](guide/04-requirements.md#r6) Every input has four failure cases: absent, late, wrong, and lying
- [**R7**](guide/04-requirements.md#r7) Scale, recovery, and availability are answered whether or not anyone writes them down
- [**R8**](guide/04-requirements.md#r8) Security, law, and ethics are requirements
- [**R9**](guide/04-requirements.md#r9) Write down what you decided not to do
- [**R10**](guide/04-requirements.md#r10) Version requirements; never edit them in place
- [**R11**](guide/04-requirements.md#r11) An API is the set of observables your acceptance tests need

**[5. Design](guide/05-design.md)**

- [**D1**](guide/05-design.md#d1) State is the material
- [**D2**](guide/05-design.md#d2) Anything that might be out of date is a cache
- [**D3**](guide/05-design.md#d3) There is no single "now"
- [**D4**](guide/05-design.md#d4) Make operations idempotent
- [**D5**](guide/05-design.md#d5) Wall-clock time and elapsed time are different instruments
- [**D6**](guide/05-design.md#d6) Derive instead of store; name the authority; record why
- [**D7**](guide/05-design.md#d7) Serve, don't rule: keep the logic away from the I/O
- [**D8**](guide/05-design.md#d8) Separate essential complexity from accidental complexity
- [**D9**](guide/05-design.md#d9) Conceptual integrity: one coherent design beats every good idea
- [**D10**](guide/05-design.md#d10) Locality of reasoning: use a part correctly without reading inside it
- [**D11**](guide/05-design.md#d11) Once someone depends on an interface, it is a promise
- [**D12**](guide/05-design.md#d12) Software is capital you carry
- [**D13**](guide/05-design.md#d13) Provenance: who said this, and can I check it later without asking them again?

**[6. Testing](guide/06-testing.md)**

- [**T1**](guide/06-testing.md#t1) A test is a fear with a name
- [**T2**](guide/06-testing.md#t2) Climb the reliability ladder: a reliable thing checks itself
- [**T3**](guide/06-testing.md#t3) A test that cannot fail proves nothing
- [**T4**](guide/06-testing.md#t4) A loop you do not trust is worse than none
- [**T5**](guide/06-testing.md#t5) Repeatability is a property of the state a test touches
- [**T6**](guide/06-testing.md#t6) The mock and the real thing answer to the same test
- [**T7**](guide/06-testing.md#t7) Test user interfaces by pulling the logic out first
- [**T8**](guide/06-testing.md#t8) When you don't know how to build it, write the tests that would pass when it works
- [**T9**](guide/06-testing.md#t9) A bug you cannot reproduce is a rumor
- [**T10**](guide/06-testing.md#t10) Let the machine generate the cases you would not think of
- [**T11**](guide/06-testing.md#t11) When someone else owns "correct," test against their implementation

**[7. Operating](guide/07-operating.md)**

- [**O1**](guide/07-operating.md#o1) Repeatability is also a property of the environment
- [**O2**](guide/07-operating.md#o2) In the manifest, say what you are compatible with; in the lock, record what you ran; commit both
- [**O3**](guide/07-operating.md#o3) CI runs the command you run, everywhere you ship — and enforces what matters
- [**O4**](guide/07-operating.md#o4) Every failure needs a signal a person will see — and believe
- [**O5**](guide/07-operating.md#o5) Handle failure on purpose: timeouts, bounded retries, and a stated fallback
- [**O6**](guide/07-operating.md#o6) A deploy is a test whose failure is an outage
- [**O7**](guide/07-operating.md#o7) Change data and interfaces in steps that can each be undone
- [**O8**](guide/07-operating.md#o8) Secure by default
- [**O9**](guide/07-operating.md#o9) In an incident, restore service first; learn afterward
- [**O10**](guide/07-operating.md#o10) Measure before you optimize; test at the scale you promised
- [**O11**](guide/07-operating.md#o11) A release you cannot roll back is a one-way door; ship it like one

**[8. Work](guide/08-work.md)**

- [**W1**](guide/08-work.md#w1) Every method runs the same six steps; they differ in batch size and in where the tests are
- [**W2**](guide/08-work.md#w2) Waterfall is correct when the only real test is expensive
- [**W3**](guide/08-work.md#w3) Iterative work puts a test inside every step
- [**W4**](guide/08-work.md#w4) Choose how carefully to work per decision, by the cost of being wrong once
- [**W5**](guide/08-work.md#w5) Flatten the schedule: a dependency is an unwritten interface
- [**W6**](guide/08-work.md#w6) Build a thin vertical slice first, then thicken it
- [**W7**](guide/08-work.md#w7) Deadlines produce an avoidance gradient; change the terrain, not the willpower
- [**W8**](guide/08-work.md#w8) Don't fall down the waterfall
- [**W9**](guide/08-work.md#w9) An iteration is time-boxed, ends on a fence, and produces four things
- [**W10**](guide/08-work.md#w10) Keep the working set in the repository
- [**W11**](guide/08-work.md#w11) Done means all of it, one concern per change, reviewed by someone else
- [**W12**](guide/08-work.md#w12) Joining late: rebuild the working set, and mark what you inferred

**[9. People](guide/09-people.md)**

- [**H1**](guide/09-people.md#h1) The team is a first-order variable
- [**H2**](guide/09-people.md#h2) A teammate fails the way an input fails
- [**H3**](guide/09-people.md#h3) Roles exist to retire fears; rotate them
- [**H4**](guide/09-people.md#h4) The interface between two people is a contract
- [**H5**](guide/09-people.md#h5) The client knows the domain, and cannot see its edges
- [**H6**](guide/09-people.md#h6) Read your assumptions to the client
- [**H7**](guide/09-people.md#h7) The first conversation: pain before solution, people before features, numbers before nouns
- [**H8**](guide/09-people.md#h8) A demo is a test, so run it like one
- [**H9**](guide/09-people.md#h9) With bad news, the delay is the cost
- [**H10**](guide/09-people.md#h10) Settle disagreements by category, then by reversibility
- [**H11**](guide/09-people.md#h11) Being behind is a systems failure with a schedule
- [**H12**](guide/09-people.md#h12) Fix the process, not the person

**[10. Agents](guide/10-agents.md)**

- [**A1**](guide/10-agents.md#a1) Producing code got cheaper faster than knowing it is right
- [**A2**](guide/10-agents.md#a2) An agent is a K3 factory; never let confidence substitute for a run
- [**A3**](guide/10-agents.md#a3) An agent arrives knowing nothing and leaves remembering nothing
- [**A4**](guide/10-agents.md#a4) Context is a budget, and it resets every session
- [**A5**](guide/10-agents.md#a5) Spend the speed on lowering the cost of testing
- [**A6**](guide/10-agents.md#a6) Review capacity is the bottleneck
- [**A7**](guide/10-agents.md#a7) Delegation is not abdication
- [**A8**](guide/10-agents.md#a8) Agents move the human up the waterfall
- [**A9**](guide/10-agents.md#a9) Hand it the search-shaped work; keep the decisions
- [**A10**](guide/10-agents.md#a10) Ask your agents, and write the answers down

## Twelve questions

If you remember nothing else, each of these can be asked out loud, and each has an answer.

| Ask                                                              | Checks |
| ---------------------------------------------------------------- | ------ |
| "Which fear does this retire — the risk, or only the fear?"      | [P4](guide/01-purpose.md#p4) |
| "What would I see if I were wrong about this — and have I looked?" | [U3](guide/02-unknowing.md#u3) |
| "What happens today when this goes wrong, and who gets the call?" | [R1](guide/04-requirements.md#r1) |
| "What happens when this input is absent, late, wrong, or lying?" | [R6](guide/04-requirements.md#r6) |
| "Who, outside this room, does this system keep a record about?"  | [R8](guide/04-requirements.md#r8) |
| "What is this a copy of, and how stale can it get?"              | [D2](guide/05-design.md#d2) |
| "What requirement would have to disappear for this to go away?"  | [D8](guide/05-design.md#d8) |
| "Can I use this without reading inside it?"                      | [D10](guide/05-design.md#d10) |
| "Have I seen this test fail?"                                    | [T3](guide/06-testing.md#t3) |
| "If this broke at 3am, what would tell us — and would anyone believe it?" | [O4](guide/07-operating.md#o4) |
| "What does it cost to be wrong about this once?"                 | [W4](guide/08-work.md#w4) |
| "If one of us vanished on Friday, what couldn't we do on Monday?" | [U6](guide/02-unknowing.md#u6) |

## Changing this guide

The guide follows its own advice. Run `node tools/check.js` before committing: it fails if a link or
anchor is broken, a principle is cited from the wrong chapter, or this index no longer matches the
chapter headings. Reword freely; never reuse an ID for a different idea.

## Where this came from

Refactored from the essays and guidebooks of a software engineering course (fall 2026), with the
course-specific material removed and the ideas reorganized into one set of principles. The testing
chapter generalizes the ArduinoUnit guidebook, *The Zen of Testing*. Drafts were tested for clarity
by having AI agents read them as a newcomer, review them as a senior engineer, answer scenario
questions from them, and follow AGENTS.md on a task with traps in it; the findings shaped this
version. See [READING.md](READING.md) for the sources the arguments lean on.

**This repository is the authority for these principles** ([D6](guide/05-design.md#d6)). The
course repository's essays are where they started, not a second copy: where the two disagree, this
guide wins, and changes to the principles are made here first.

Licensed under the [MIT License](LICENSE).
