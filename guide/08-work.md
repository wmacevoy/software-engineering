# 8. Work

The shape of the work: two orders for the same six steps, the one fact that decides between them,
what deadlines do to people, and the failure that looks exactly like progress.

---

### <a id="w1"></a>W1. Every method runs the same six steps; they differ in batch size and in where the tests are

| Step         | What it produces                                                                 | The question it answers        |
| ------------ | -------------------------------------------------------------------------------- | ------------------------------ |
| Requirements | numbered, observable statements of what must be true — and what is *not* being built | what, for whom, and how much |
| Design       | chosen mechanism — tables, protocols, keys, components — and what was rejected   | how, and why not the other way |
| Develop      | code a second person can read and defend                                         | does it exist                  |
| Test         | evidence that the code does what the requirement says                            | does it work                   |
| Deploy       | the thing running where its users are, and a way back                            | is it out there, and healthy   |
| Maintain     | everything after: fixes, changes, upgrades, the next request                     | is it still true               |

(In iterative work, Maintain stops being a separate step — see [SE1/W3](#w3).)

The order is right in every method: you cannot design against a requirement you do not have, or
deploy what you have not built. The disagreement is about **how much goes through each step at
once** and **whether the test comes at the end or inside every step.**

### <a id="w2"></a>W2. Waterfall is correct when the only real test is expensive

Waterfall runs the six steps once, in order, each signed off before the next begins. Winston Royce
drew it in 1970 and, two pages later, wrote that the implementation as drawn "is risky and invites
failure," because testing arrives at the end, where every surprise costs most. The industry kept the
drawing and dropped the warning.

Be fair to it: where the only real test costs a million dollars and a year, it is right. Those
disciplines still iterate — on prototypes, models, and test articles — but the final build is done
once, so the rational response is to move everything checkable *before* that test. Waterfall is what
a discipline looks like when it cannot afford to be wrong twice.

| What waterfall retires                                   | What it creates, when tests are cheap                          |
| -------------------------------------------------------- | -------------------------------------------------------------- |
| "we will spend the money on a design that was never checked" | "we will find out it was the wrong product at the end, at full price" |
| "the requirements moved under us"                        | "the requirements were frozen before anyone had seen the thing" |
| "nobody signed off"                                      | "everyone signed off, and it was still wrong"                  |

K2 is guaranteed on every project, and waterfall schedules its arrival for the last step.

### <a id="w3"></a>W3. Iterative work puts a test inside every step

The same steps in loops, with three latencies and three instruments:

```
Release loop       (weeks; reality answers)
  Iteration loop   (days; a person answers; time-boxed, and scope is what moves)
    Requirements   (test: the client reads a precise claim and objects; assumptions read back)
    Design         (test: a contract, a mock that misbehaves, a spike, a failing test)
    Develop        (test: red, then green — the seconds loop)
    Demo           (test: a person drives the real thing)              ← the fence
  Deploy           (test: health-gated, automatic revert, rollback timed)
  Observe          (production telemetry; what K2 arrived → FINDINGS)
  Delete           (what can we remove?)
There is no Maintain step. After the first deploy, every iteration is maintenance.
```

- **"(test)" means something different at each step.** Requirements are tested by a person reading a
  sentence precise enough to be wrong; design by artifacts that exist before the code; code by red
  then green; deploys by a health check and an automatic revert.
- **The iteration ends on a fence, not on "done"** ([SE1/W9](08-work.md#w9)).
- **The demo is the only instrument for "wrong product"** ([SE1/F3](03-feedback.md#f3)).
- **The outer loop's product is knowledge**: K2 converted to K1 at the cheapest available price.

### <a id="w4"></a>W4. Choose how carefully to work per decision, by the cost of being wrong once

| Decision                                      | Cost of being wrong once                         | How to work                                     |
| --------------------------------------------- | ------------------------------------------------ | ----------------------------------------------- |
| a route handler, a string, a query            | seconds to find out, seconds to undo             | loop: change it, run it, keep or revert         |
| a derived value used across one repository    | every consumer, but all in one place             | loop, with tests naming the requirement         |
| a schema with real data under it              | a migration inside a maintenance window          | **small waterfall**: think, review, migrate once |
| a published API with callers depending on it  | a version served alongside the old one, forever  | small waterfall: it is a promise now            |
| a distributed private key                     | cannot be unleaked                               | small waterfall, and a ceremony                 |
| what data about people you collect            | cannot be un-collected; a regulator sets the deadline | **small waterfall, before anything else**  |

Around a one-way door, run a small waterfall *inside* the loop: get the requirement exactly, design
it on paper, review it with someone who does not share your assumption, and do it once. Everywhere
else, loop. **Methodology is a function of the cost of being wrong once, and that cost can change
twice in an afternoon.**

> **Ask:** "What does it cost to be wrong about this once?"

### <a id="w5"></a>W5. Flatten the schedule: a dependency is an unwritten interface

Drywall goes up after plumbing because the pipe occupies the space the wall will cover. Every arrow
in a physical schedule is, at bottom, a fact about mass. Software is massless: you can write code
that calls a function before that function exists, as long as you know its signature. So when a
software schedule says *"we can't start B until A is done,"* the arrow is almost never a fact about
the world. It is a fact about the design: **B does not know what A will look like.**

| The dependency says          | The artifact that dissolves it                    |
| ---------------------------- | ------------------------------------------------- |
| "B needs A's shape"          | an interface — signature, schema, error codes     |
| "B needs A to answer"        | a mock that answers, and misbehaves on request    |
| "B isn't done until A works" | a test that fails today and passes when A arrives |

None of the three requires A to exist. The dependency is not sequenced; it is **specified** — so the
contract layer is built first, and the promise is what unblocks, not the implementation.

The cost is real: flattening converts a **scheduling** risk into an **integration** risk, which is a
good trade only if you integrate continuously ([SE1/T6](06-testing.md#t6)). And some orderings
genuinely survive: **sequence around irreversibility, not around incompleteness.** Do the one-way
doors in order, carefully ([SE1/W4](#w4)). And when you genuinely must learn something before you
can design against it, run a spike first — it stands in for the missing knowledge the way a mock
stands in for a missing component.

> **Ask:** "Is this arrow a fact about the world, or an interface nobody wrote down?"

### <a id="w6"></a>W6. Build a thin vertical slice first, then thicken it

A slice from click to route to query to response, built early and then widened, crosses the gap.
Horizontal layers — all of the database, then all of the API, then all of the UI — finish at the
same time: never. Iteration one of the parking system is one lot, one sensor with its control plane
for faults, the collector polling it, and the driver page showing live, stale, and unknown. Not
translations, not firmware updates. Enough to set a sensor `stuck` in front of the client and watch
what they say.

Carry the load-bearing idea in the first slice (here, signed readings), so the bridge is tested
under the weight it will have to bear.

### <a id="w7"></a>W7. Deadlines produce an avoidance gradient; change the terrain, not the willpower

In a classic experiment, a rat that has learned one end of its cage gives a shock is tied to a
string and drawn toward that end; how hard it pulls away is measured along the way. The pull is
nearly flat far from the danger and rises steeply close to it — an *avoidance gradient*. Deadlines
do this to people: the month before feels like nothing, the last week is unbearable. The surge of
fear arrives exactly when the project can least afford what it produces: skipped tests, bundled
diffs, unreviewed merges, "we'll clean it up after launch." That feedback loop, not incompetence, is
how most projects fail.

- **Remove the danger.** If deploying is routine and reversible, the deadline stops being the
  shocking end of the cage. An always-releasable main branch means shipping is not an event.
- **Cross the gap early** with the thin slice ([SE1/W6](#w6)), so the last week thickens something
  that already works.
- **Put real fences along the way.** A demo to an actual client, a check that exits nonzero, a
  deploy that happened. A status meeting is not a fence; nothing was proved.
- **Keep slack.** A plan at full utilization cannot absorb K2, and K2 is guaranteed. Think of a
  checkout line: when the cashier is busy half the time, a new customer barely waits; when the
  cashier is busy 95% of the time, any small burst builds a line that takes ages to clear. Waiting
  grows much faster than load as you approach 100%, and a plan at 95% has almost no room for a
  surprise. Slack is the budget line for the unknown unknown.
- **Estimate the category** ([SE1/U5](02-unknowing.md#u5)).
- **Bad news early is a gift; bad news late is a betrayal** ([SE1/H9](09-people.md#h9)).

> **Ask:** "What would make the last week before this deadline boring?"

### <a id="w8"></a>W8. Don't fall down the waterfall

The failure looks like a productive week. A team asked for a campus parking app has, by Tuesday, a
normalized schema — `students`, `vehicles`, `sightings(plate, lot, seen_at)` — an index, a view that
joins all three, and a query answering "where did this student park last Thursday" in eleven
milliseconds. In week four someone finally asks whether student identity may be joined to a
location. The answer is no. The sightings table cannot exist in that form; the join, the view, the
query, and the UI built on it are all forbidden. A rule from the top of the waterfall, discovered
after four weeks at the bottom. One requirement — *counts, not locations* — would have saved the
month, and no amount of normalization would ever have produced it. It comes from a question, not a
design.

**Why the slope is there: the comfort gradient.** Each step down is more concrete, more familiar,
more solitary, and produces something you can see. Each step up is more ambiguous and more social,
and produces a document nobody grades. Reading a privacy law is uncomfortable; normalizing a schema
is a pleasure. People go where their own discomfort is lowest and leave the client's for later.
Agents make the slope steeper: an agent produces the schema and fifty queries in a minute and never
asks about the registrar unless a requirement tells it to.

**The tells.** You are falling if any of these is true before the client has objected to a numbered
requirement:

- There is a schema, or a framework or library has been chosen — other than ones given to you as
  constraints, such as the language a course or employer requires.
- There is a "temporary" table, column, or default.
- "We'll figure out login later." "We'll add the privacy stuff at the end."
- There is no `Non-goals` list, so nothing has been refused yet.
- Nobody can say who, outside the room, this system keeps a record about.

**The railing.**

1. **Ask the expensive questions first** — the ones that could invalidate the plan
   ([SE1/R3](04-requirements.md#r3)).
2. **Write the answers where they cannot be missed** — `Scope decisions`, `Non-goals`, and a section
   for security, law, and ethics ([SE1/R8](04-requirements.md#r8), [SE1/R9](04-requirements.md#r9)).
3. **Read the assumptions back** as questions: "We're assuming a record of where a person parked is
   fine to keep. True?"
4. **Then descend on purpose.** A **spike** is a permitted descent: time-boxed, aimed at one
   question, its code thrown away. Falling is a descent with no question and no time box.

> **Ask:** "What will I know when this spike stops?" — and — "What has the client objected to so far?"

### <a id="w9"></a>W9. An iteration is time-boxed, ends on a fence, and produces four things

One to two weeks. When the period ends, scope moves, not the date. Without the time box the loop is
a spiral. An iteration that produces three of these is not done:

1. **A running thing** the client can touch, from a clean reset, on data shaped like theirs.
2. **A diff to the requirements** — `v(n)` to `v(n+1)` — if anything changed, including `Non-goals`.
3. **A `FINDINGS` entry**: what was learned at full price.
4. **A `QUEUE`** saying what is next, priced, with a *done* sentence on each item.

And one question at the end: *what can we delete?* ([SE1/D12](05-design.md#d12))

### <a id="w10"></a>W10. Keep the working set in the repository

The state of the project has to be observable from where every party stands
([SE1/U6](02-unknowing.md#u6)). Four documents, versioned alongside the code — not in a wiki, not in
chat, not in a notebook:

| Document          | Answers                                                                     | Written by        |
| ----------------- | --------------------------------------------------------------------------- | ----------------- |
| `REQUIREMENTS_vX` | what must observably be true, and what is not being built                   | us and the client |
| `DESIGN_vX`       | how we intend to achieve it, and what we rejected                           | us                |
| `QUEUE`           | what is being worked, in what order, by whom, and what would make it done   | us                |
| `FINDINGS`        | what we learned the expensive way — surprises, dead ends, measurements, the attack that worked | reality |

- **Versioned**, because a superseded requirement is not deleted knowledge
  ([SE1/R10](04-requirements.md#r10)).
- **`QUEUE` is the shared cursor.** Without one, two workers do the same task, or each assumes the
  other has it — a failure now cheap to hit ten times an hour.
- **`FINDINGS` is the K2/K3 ledger**, and the only one reality writes. A fact discovered at full
  price and not written down gets rediscovered at full price.

Put them in `docs/` unless the repository already has a convention, and say where in the
**repository guide** — the `CONTRIBUTING.md` (or equivalent) that tells a newcomer, human or agent,
how to build, run, test, and reset the system ([SE1/A2](10-agents.md#a2)).

Each retires a fear — "we are building different things," "nobody knows what state this is in," "we
already learned this once." A document that retires no fear should be dropped, not maintained.
Starting skeletons for the four, and for the repository guide, are listed in the
[README](../README.md#contents).

### <a id="w11"></a>W11. Done means all of it, one concern per change, reviewed by someone else

*Changed in v1.1.*

**A definition of done is a checklist a change fully passes — not most of it.** A typical one:

- It satisfies a stated requirement, and the change names the requirement's versioned ID
  (`REQ2/UI-1`, [SE1/R10](04-requirements.md#r10)) — or it is labeled a chore (below).
- A test names that same ID and has been seen to fail without the change.
- The system builds and runs from a clean checkout.
- The full check suite passes locally.
- Anything the change made untrue in the requirements, design, or repository guide is updated in the
  same change. Documentation that drifts is worse than none, because people trust it.
- New behavior that can fail has a way to make it fail on demand.
- It is one concern, and its description says what was deliberately left out.
- Someone other than the author reviewed it. For an agent-drafted change, the human who reads all of it
  and signs counts; a one-way door deserves a second human.
- It is signed by a person who has read all of it and stands behind it.

The same list, as boxes to tick, is in [CHECKLISTS.md](../CHECKLISTS.md); keep the two in step.

**One concern per change.** Reviewer attention is the scarce resource, and a bundled diff spends it
on separating things that should never have been joined. A change description says what changed,
which requirements, how it was verified, and **what was deliberately left out** — silent omissions
are the expensive kind.

**Review** is the loop that catches unclear intent and bad design ([SE1/F3](03-feedback.md#f3)). It
works when the author reviews their own diff first, the change is small enough to read in one
sitting, it comes back within a day, and style is left to the formatter and linter
([SE1/O3](07-operating.md#o3)). Reviewers ask three questions, in order:

1. Does it do what the requirement says, and does the test prove it?
2. Could the next maintainer read this in a month and explain why it is here?
3. What does it make harder later?

Not every change serves a requirement. A typo, a dependency update, or a pure refactor is a
**chore**: it says so in its description, and its proof is that the existing suite still passes (a
refactor's tests must have been seen to fail — [SE1/T3](06-testing.md#t3)).

> **Ask:** "Could I review this in one sitting?"

### <a id="w12"></a>W12. Joining late: rebuild the working set, and mark what you inferred

Most projects meet this guide with code already written. The working set can be rebuilt from the
code and its history, but the rebuild has a trap: it invents reasons. A commit says what changed;
*why* was in a head, and a reconstruction fills the gap with a plausible story — a K3 in the making
([SE1/U3](02-unknowing.md#u3)). In order:

1. **Requirements from behavior.** Write what the code observably does today as numbered
   requirements, each marked *(inferred)* until someone who can decide confirms it — as invented
   numbers are marked *(invented)*.
2. **Design from structure; reasons from evidence.** Record components and state as they are. Give
   each decision its source — a commit, an issue, a person — or mark the reason *(inferred)*.
3. **`FINDINGS` from history.** Reverts, hotfixes, and fixes of fixes are findings nobody wrote down.
4. **`QUEUE` from the gaps.** Every requirement with no test is a queue item, not a failure; so is
   every inherited claim nobody has measured — a footprint, a speed, "runs under the sanitizer."
5. **Read it back** ([SE1/H6](09-people.md#h6)). The *(inferred)* marks are the questions.

A reconstruction that marks nothing as inferred is claiming more than it knows.

> **Ask:** "Which of these reasons did somebody say, and which did we make up?"


---

## The vocabulary

Each term with what it is and the fear it retires — because a ceremony that retires none will be
dropped in week ten, and should be.

| Term                        | What it is                                                                                     | The fear it retires                                   |
| --------------------------- | ---------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| **Iteration / sprint**      | A fixed period, one to two weeks, ending at a fence.                                           | "we're building the wrong thing and won't know for months" |
| **Time box**                | The period is fixed; scope moves.                                                              | "it will never end"                                   |
| **User story**              | A person, a want, a reason. A pain plus a guess.                                               | "we lost the *why*"                                   |
| **Acceptance criteria**     | The numbered, observable sentences a story must satisfy.                                       | "we each heard something different"                   |
| **Acceptance test**         | A criterion made executable, written to fail first.                                            | "we think it's done"                                  |
| **Definition of done**      | The checklist a change must fully pass.                                                        | "done means different things to different people"     |
| **Backlog**                 | Everything not yet done, in priority order, each item with a done sentence.                    | "nobody knows what's next"                            |
| **Spike**                   | A time-boxed investigation of one question; the code is thrown away.                           | "we can't estimate what we don't understand"          |
| **Stand-up**                | Five minutes daily: done, next, blocked — and since when.                                      | "I didn't know you were stuck"                        |
| **Sprint review (demo)**    | The client drives the real thing at the end of the iteration.                                  | "they will hate it in month six"                      |
| **Retrospective**           | The team, after the demo: what did we learn the expensive way?                                 | "we already learned this once"                        |
| **Scrum**                   | A named framework: product owner, scrum master, developers; sprint, planning, daily scrum, review, retrospective; product backlog, sprint backlog, increment. | the fears above, packaged |
| **Product owner**           | The one voice who orders the backlog and can say yes, no, and how much.                        | "the client is five people who disagree"              |
| **Increment**               | The running thing at the end of an iteration. Usable, or it doesn't count.                     | "we have lots of parts and no product"                |
| **Minimum viable product**  | The smallest increment that answers "would anyone use this?"                                   | "we built the whole thing before asking"              |
| **Velocity**                | Work completed per iteration. A planning input, never a target ([SE1/F5](03-feedback.md#f5)).         | "we can't plan"                                       |
| **Kanban / WIP limit**      | A board with a cap on work in progress. Finish before starting.                                | "everything is half done"                             |
| **Pair programming**        | Two people, one keyboard. Review while writing; knowledge in two heads.                        | "only one person understands this"                    |
| **Refactoring**             | Changing structure without changing behavior, under tests that prove it.                       | "we can't touch this"                                 |
| **Technical debt**          | Carry taken on knowingly, to be repaid ([SE1/D12](05-design.md#d12)).                                   | "we don't know what we owe"                           |
| **Continuous integration**  | Every push built and tested on a machine that is not yours.                                    | "it works on my machine"                              |
| **Continuous delivery / deployment** | Every green build *could* ship / *does* ship.                                         | "release is an event"                                 |
| **Trunk-based development** | One always-releasable branch, small steps, no long-lived branches.                             | "the merge will take a week"                          |
| **Feature flag**            | A switch that ships code dark and turns it on later. Decouples deploy from release.            | "deploying it means users see it"                     |

---

Next: [9. People](09-people.md) — the team, the client, and what passes between them.
