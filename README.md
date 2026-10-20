# Software Engineering

A guide to building reliable, tested, maintainable software — written for humans and for the AI
agents working beside them.

It is organized as **numbered principles** (`SE1/T3`, `SE1/D2`, `SE1/R6`, …). Each states one idea
and says why it is true; most end with a question you can ask out loud in a meeting or a code
review. The IDs are versioned so that people and agents can cite them and still mean the same thing
later: *"this test has never been seen red (SE1/T3)"*, *"this copy of the user list can go stale;
how stale? (SE1/D2)"*.

## The argument in ten lines

1. **Engineering is making reliable things** on time, within constraints, while managing everyone's
   discomfort. Reliable means it works — *and says so when it doesn't*
   ([SE1/P1](guide/01-purpose.md#p1), [SE1/P2](guide/01-purpose.md#p2)).
2. **Every practice retires a named fear.** A practice that retires none gets dropped; one that
   relieves the fear without reducing the risk is worse than nothing
   ([SE1/P4](guide/01-purpose.md#p4)).
3. **Building is discovering what you didn't know**, in the right order, at the right price. The
   dangerous kind is confident and wrong, and only reality or another person finds it
   ([SE1/U2](guide/02-unknowing.md#u2), [SE1/U3](guide/02-unknowing.md#u3)).
4. **Software's tests are cheap, and software has no mass.** The first makes certainty affordable;
   the second makes it necessary, because a bad design never sags or cracks
   ([SE1/F1](guide/03-feedback.md#f1), [SE1/F4](guide/03-feedback.md#f4)).
5. **Nobody hands you the problem.** Write requirements specific enough to be wrong, and get them
   rejected early. They always include security, law, and ethics: nobody asks for those, and they
   are the most expensive to discover late ([SE1/R1](guide/04-requirements.md#r1),
   [SE1/R2](guide/04-requirements.md#r2), [SE1/R8](guide/04-requirements.md#r8)).
6. **Every input can be absent, late, wrong, or lying**, and each case needs a stated answer
   ([SE1/R6](guide/04-requirements.md#r6)).
7. **State is the material.** Name your caches, own your copies, and keep logic away from I/O
   ([SE1/D1](guide/05-design.md#d1), [SE1/D2](guide/05-design.md#d2),
   [SE1/D7](guide/05-design.md#d7)).
8. **A test you have never seen fail proves nothing**, and a flaky one is worse than none
   ([SE1/T3](guide/06-testing.md#t3), [SE1/T4](guide/06-testing.md#t4),
   [SE1/T5](guide/06-testing.md#t5)).
9. **Choose the method per decision by the cost of being wrong once**: loop fast around reversible
   choices, slow down around one-way doors ([SE1/W4](guide/08-work.md#w4),
   [SE1/D11](guide/05-design.md#d11)).
10. **Nothing important may live only in a head** — because teammates leave, and agents were never
    in the room ([SE1/U6](guide/02-unknowing.md#u6), [SE1/W10](guide/08-work.md#w10)).

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
| [CHANGELOG.md](CHANGELOG.md)       | what changed in each release, by principle ID                   |
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
IDs (such as `SE1/T3`).

## Principle index

Every citation carries the guide's major version: `SE1/T3` is principle 3 of *Testing* in the first
major version. Within SE1, which begins at the `v1.0` tag, a principle may be reworded, but its ID
never moves to a different idea; a retired principle keeps its ID with a note saying where its
content went, and new principles take the next number in their chapter. A later major version
(`SE2`) may renumber, and will publish a table mapping each SE1 ID to its new one; SE1 stays readable
at its tag. The version is on every citation, not declared once per document, so a citation copied
into a commit message, an issue, or another repository still says which guide it means. Releases
within SE1 (`v1.1`, …) are listed by ID in [CHANGELOG.md](CHANGELOG.md), and each principle changed
since v1.0 says so under its heading. The letters
are the chapters: **P**urpose, **U**nknowing, **F**eedback, **R**equirements, **D**esign, **T**esting,
**O**perating, **W**ork, **H**umans (people), **A**gents. (Requirement IDs in your own project
should use a different form, such as `REQ2/UI-1`, so they are never confused with these.)

**[1. Purpose](guide/01-purpose.md)**

- [**SE1/P1**](guide/01-purpose.md#p1) Engineers make reliable things, on time, within resource constraints, managing discomfort for the team, the client, and the users
- [**SE1/P2**](guide/01-purpose.md#p2) Reliable is not correct
- [**SE1/P3**](guide/01-purpose.md#p3) Discomfort is a leading indicator
- [**SE1/P4**](guide/01-purpose.md#p4) Every practice retires a named fear
- [**SE1/P5**](guide/01-purpose.md#p5) The deliverable is not the code

**[2. Unknowing](guide/02-unknowing.md)**

- [**SE1/U1**](guide/02-unknowing.md#u1) K0 through K3 are in order of expense; K4 is a choice
- [**SE1/U2**](guide/02-unknowing.md#u2) Building is discovering, in the right order and at the right price, which category each part of the problem belongs to
- [**SE1/U3**](guide/02-unknowing.md#u3) K3 is the one to be afraid of
- [**SE1/U4**](guide/02-unknowing.md#u4) Every abstraction rests on chosen falsehoods; write down where they are load-bearing
- [**SE1/U5**](guide/02-unknowing.md#u5) Estimate the category, not the task
- [**SE1/U6**](guide/02-unknowing.md#u6) Nothing important may live only in a head
- [**SE1/U7**](guide/02-unknowing.md#u7) Find the K3 factories: anything that keeps saying "fine" with no way to say "wrong"

**[3. Feedback](guide/03-feedback.md)**

- [**SE1/F1**](guide/03-feedback.md#f1) The cost of a test decides the method
- [**SE1/F2**](guide/03-feedback.md#f2) The cost of a test is designed, not given
- [**SE1/F3**](guide/03-feedback.md#f3) Push each class of error down to the cheapest loop that can catch it
- [**SE1/F4**](guide/03-feedback.md#f4) Nothing has mass, so build the signals
- [**SE1/F5**](guide/03-feedback.md#f5) When a measure becomes a target, it stops measuring

**[4. Requirements](guide/04-requirements.md)**

- [**SE1/R1**](guide/04-requirements.md#r1) Keep the pain; test the solution
- [**SE1/R2**](guide/04-requirements.md#r2) Specific and wrong beats vague and safe
- [**SE1/R3**](guide/04-requirements.md#r3) Ask the questions nobody volunteers — the ones that could invalidate the plan, first
- [**SE1/R4**](guide/04-requirements.md#r4) A requirement with no price attached is a wish
- [**SE1/R5**](guide/04-requirements.md#r5) A requirement says what must be observably true; a design says how
- [**SE1/R6**](guide/04-requirements.md#r6) Every input has four failure cases: absent, late, wrong, and lying
- [**SE1/R7**](guide/04-requirements.md#r7) Scale, recovery, and availability are answered whether or not anyone writes them down
- [**SE1/R8**](guide/04-requirements.md#r8) Security, law, and ethics are always requirements
- [**SE1/R9**](guide/04-requirements.md#r9) Write down what you decided not to do
- [**SE1/R10**](guide/04-requirements.md#r10) Version requirements; never edit them in place
- [**SE1/R11**](guide/04-requirements.md#r11) An API is the set of observables your acceptance tests need

**[5. Design](guide/05-design.md)**

- [**SE1/D1**](guide/05-design.md#d1) State is the material
- [**SE1/D2**](guide/05-design.md#d2) Anything that might be out of date is a cache
- [**SE1/D3**](guide/05-design.md#d3) There is no single "now"
- [**SE1/D4**](guide/05-design.md#d4) Make operations idempotent
- [**SE1/D5**](guide/05-design.md#d5) Wall-clock time and elapsed time are different instruments
- [**SE1/D6**](guide/05-design.md#d6) Derive instead of store; name the authority; record why
- [**SE1/D7**](guide/05-design.md#d7) Serve, don't rule: keep the logic away from the I/O
- [**SE1/D8**](guide/05-design.md#d8) Separate essential complexity from accidental complexity
- [**SE1/D9**](guide/05-design.md#d9) Conceptual integrity: one coherent design beats every good idea
- [**SE1/D10**](guide/05-design.md#d10) Locality of reasoning: use a part correctly without reading inside it
- [**SE1/D11**](guide/05-design.md#d11) Once someone depends on an interface, it is a promise
- [**SE1/D12**](guide/05-design.md#d12) Software is capital you carry
- [**SE1/D13**](guide/05-design.md#d13) Provenance: who said this, and can I check it later without asking them again?

**[6. Testing](guide/06-testing.md)**

- [**SE1/T1**](guide/06-testing.md#t1) A test is a fear with a name
- [**SE1/T2**](guide/06-testing.md#t2) Climb the reliability ladder: a reliable thing checks itself
- [**SE1/T3**](guide/06-testing.md#t3) A test that cannot fail proves nothing
- [**SE1/T4**](guide/06-testing.md#t4) A loop you do not trust is worse than none
- [**SE1/T5**](guide/06-testing.md#t5) Repeatability is a property of the state a test touches
- [**SE1/T6**](guide/06-testing.md#t6) The mock and the real thing answer to the same test
- [**SE1/T7**](guide/06-testing.md#t7) Test user interfaces by pulling the logic out first
- [**SE1/T8**](guide/06-testing.md#t8) When you don't know how to build it, write the tests that would pass when it works
- [**SE1/T9**](guide/06-testing.md#t9) A bug you cannot reproduce is a rumor
- [**SE1/T10**](guide/06-testing.md#t10) Let the machine generate the cases you would not think of
- [**SE1/T11**](guide/06-testing.md#t11) When someone else owns "correct," test against their implementation

**[7. Operating](guide/07-operating.md)**

- [**SE1/O1**](guide/07-operating.md#o1) Repeatability is also a property of the environment
- [**SE1/O2**](guide/07-operating.md#o2) In the manifest, say what you are compatible with; in the lock, record what you ran; commit both
- [**SE1/O3**](guide/07-operating.md#o3) CI runs the command you run, everywhere you ship — and enforces what matters
- [**SE1/O4**](guide/07-operating.md#o4) Every failure needs a signal a person will see — and believe
- [**SE1/O5**](guide/07-operating.md#o5) Handle failure on purpose: timeouts, bounded retries, and a stated fallback
- [**SE1/O6**](guide/07-operating.md#o6) A deploy is a test whose failure is an outage
- [**SE1/O7**](guide/07-operating.md#o7) Change data and interfaces in steps that can each be undone
- [**SE1/O8**](guide/07-operating.md#o8) Secure by default
- [**SE1/O9**](guide/07-operating.md#o9) In an incident, restore service first; learn afterward
- [**SE1/O10**](guide/07-operating.md#o10) Measure before you optimize; test at the scale you promised
- [**SE1/O11**](guide/07-operating.md#o11) A release you cannot roll back is a one-way door; ship it like one

**[8. Work](guide/08-work.md)**

- [**SE1/W1**](guide/08-work.md#w1) Every method runs the same six steps; they differ in batch size and in where the tests are
- [**SE1/W2**](guide/08-work.md#w2) Waterfall is correct when the only real test is expensive
- [**SE1/W3**](guide/08-work.md#w3) Iterative work puts a test inside every step
- [**SE1/W4**](guide/08-work.md#w4) Choose how carefully to work per decision, by the cost of being wrong once
- [**SE1/W5**](guide/08-work.md#w5) Flatten the schedule: a dependency is an unwritten interface
- [**SE1/W6**](guide/08-work.md#w6) Build a thin vertical slice first, then thicken it
- [**SE1/W7**](guide/08-work.md#w7) Deadlines produce an avoidance gradient; change the terrain, not the willpower
- [**SE1/W8**](guide/08-work.md#w8) Don't fall down the waterfall
- [**SE1/W9**](guide/08-work.md#w9) An iteration is time-boxed, ends on a fence, and produces four things
- [**SE1/W10**](guide/08-work.md#w10) Keep the working set in the repository
- [**SE1/W11**](guide/08-work.md#w11) Done means all of it, one concern per change, reviewed by someone else
- [**SE1/W12**](guide/08-work.md#w12) Joining late: rebuild the working set, and mark what you inferred

**[9. People](guide/09-people.md)**

- [**SE1/H1**](guide/09-people.md#h1) The team is a first-order variable
- [**SE1/H2**](guide/09-people.md#h2) A teammate fails the way an input fails
- [**SE1/H3**](guide/09-people.md#h3) Roles exist to retire fears; rotate them
- [**SE1/H4**](guide/09-people.md#h4) The interface between two people is a contract
- [**SE1/H5**](guide/09-people.md#h5) The client knows the domain, and cannot see its edges
- [**SE1/H6**](guide/09-people.md#h6) Read your assumptions to the client
- [**SE1/H7**](guide/09-people.md#h7) The first conversation: pain before solution, people before features, numbers before nouns
- [**SE1/H8**](guide/09-people.md#h8) A demo is a test, so run it like one
- [**SE1/H9**](guide/09-people.md#h9) With bad news, the delay is the cost
- [**SE1/H10**](guide/09-people.md#h10) Settle disagreements by category, then by reversibility
- [**SE1/H11**](guide/09-people.md#h11) Being behind is a systems failure with a schedule
- [**SE1/H12**](guide/09-people.md#h12) Fix the process, not the person

**[10. Agents](guide/10-agents.md)**

- [**SE1/A1**](guide/10-agents.md#a1) Producing code got cheaper faster than knowing it is right
- [**SE1/A2**](guide/10-agents.md#a2) An agent is a K3 factory; never let confidence substitute for a run
- [**SE1/A3**](guide/10-agents.md#a3) An agent arrives knowing nothing and leaves remembering nothing
- [**SE1/A4**](guide/10-agents.md#a4) Context is a budget, and it resets every session
- [**SE1/A5**](guide/10-agents.md#a5) Spend the speed on lowering the cost of testing
- [**SE1/A6**](guide/10-agents.md#a6) Review capacity is the bottleneck
- [**SE1/A7**](guide/10-agents.md#a7) Delegation is not abdication
- [**SE1/A8**](guide/10-agents.md#a8) Agents move the human up the waterfall
- [**SE1/A9**](guide/10-agents.md#a9) Hand it the search-shaped work; keep the decisions
- [**SE1/A10**](guide/10-agents.md#a10) Ask your agents, and write the answers down

## Twelve questions

If you remember nothing else, each of these can be asked out loud, and each has an answer.

| Ask                                                              | Checks |
| ---------------------------------------------------------------- | ------ |
| "Which fear does this retire — the risk, or only the fear?"      | [SE1/P4](guide/01-purpose.md#p4) |
| "What would I see if I were wrong about this — and have I looked?" | [SE1/U3](guide/02-unknowing.md#u3) |
| "What happens today when this goes wrong, and who gets the call?" | [SE1/R1](guide/04-requirements.md#r1) |
| "What happens when this input is absent, late, wrong, or lying?" | [SE1/R6](guide/04-requirements.md#r6) |
| "Who, outside this room, does this system keep a record about?"  | [SE1/R8](guide/04-requirements.md#r8) |
| "What is this a copy of, and how stale can it get?"              | [SE1/D2](guide/05-design.md#d2) |
| "What requirement would have to disappear for this to go away?"  | [SE1/D8](guide/05-design.md#d8) |
| "Can I use this without reading inside it?"                      | [SE1/D10](guide/05-design.md#d10) |
| "Have I seen this test fail?"                                    | [SE1/T3](guide/06-testing.md#t3) |
| "If this broke at 3am, what would tell us — and would anyone believe it?" | [SE1/O4](guide/07-operating.md#o4) |
| "What does it cost to be wrong about this once?"                 | [SE1/W4](guide/08-work.md#w4) |
| "If one of us vanished on Friday, what couldn't we do on Monday?" | [SE1/U6](guide/02-unknowing.md#u6) |

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

**This repository is the authority for these principles** ([SE1/D6](guide/05-design.md#d6)). The
course repository's essays are where they started, not a second copy: where the two disagree, this
guide wins, and changes to the principles are made here first.

Licensed under the [MIT License](LICENSE).
