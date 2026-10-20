# 9. People

Who builds the thing, who it is for, and what has to pass between them. The team is not a mood on
top of the technology; it is a first-order variable, and unlike the technology it gets chosen by
default unless somebody chooses it on purpose.

The chapter is written for a team of three to five and a real client. If your project has one
partner and a grader, the ideas still apply at smaller size:

| In this chapter         | On a two-person class project                                                     |
| ----------------------- | --------------------------------------------------------------------------------- |
| the client              | the assignment's author — ask them the questions in SE1/R3, by email or office hours |
| roles ([SE1/H3](#h3))       | split them two ways, and swap at the halfway point                                |
| the contract ([SE1/H4](#h4)) | the function signatures and data shapes you agree on before splitting the work  |
| the demo ([SE1/H8](#h8))    | showing a running build to someone outside the pair before the due date           |
| bad news ([SE1/H9](#h9))    | telling your partner the day you are stuck, not the night before it is due        |

---

### <a id="h1"></a>H1. The team is a first-order variable

- **The system will resemble the team.** A system's structure copies the communication structure of
  the organization that built it (Conway, 1968), because an interface between two components can
  only be as well specified as the conversation between the two people who own them. So a component
  table is also a team structure. Choose the shape on purpose, or the system inherits "who sat
  together."
- **Knowledge lives in heads, and heads leave.** Anything known to exactly one person has no backup
  ([SE1/U6](02-unknowing.md#u6)); when that person leaves, it is deleted without warning.
- **The team's fear sets its practice** ([SE1/P3](01-purpose.md#p3), [SE1/W7](08-work.md#w7)).
- **Coordination cost grows faster than headcount.** Four people are six pairs; six are fifteen.
  Every pair needs an interface, and the ones nobody wrote down get negotiated in meetings. That is
  why adding people to a late project makes it later, and why the fix is a smaller, written
  interface rather than another meeting.

The team's shape is a design decision with the same status as the schema: made early, hard to
change, assumed by everything after. Make it on purpose and write it down.

> **Ask:** "Does our team's shape match the system we want — and who is carrying more than one
> person's share of what only they know?"

### <a id="h2"></a>H2. A teammate fails the way an input fails

Every input needs an answer for absent, late, wrong, and lying ([SE1/R6](04-requirements.md#r6)). A
teammate is an input, and a plan that works only when everyone is present, on time, right, and
candid is not finished.

| Case   | On a team                                                     | What handles it                                                         |
| ------ | ------------------------------------------------------------- | ----------------------------------------------------------------------- |
| Absent | gone for a week — illness, an interview, another deadline     | nothing known only to one head: pairing on the scary parts, review, the working set |
| Late   | "almost done" for three weeks                                 | steps small enough that late is visible in days; a fence that runs or doesn't |
| Wrong  | a confident K3 in the design                                  | review by someone who does not share the assumption; demonstrate before defending |
| Lying  | status that reads green because red is uncomfortable          | status is a demo, not a sentence; reward bad news early, visibly, every time |

Nobody sets out to lie. "It's basically done" is the human version of a sensor stuck at `200 OK` — a
successful response with nothing behind it changed. The defense is the same: do not trust the status
field; check the age of the last thing that actually ran.

### <a id="h3"></a>H3. Roles exist to retire fears; rotate them

A team of three to five needs no titles and four roles. Everyone writes code; the roles rotate every
iteration so knowledge spreads.

| Role       | Holds                                                    | Fear it retires                                                     |
| ---------- | -------------------------------------------------------- | ------------------------------------------------------------------- |
| **Architect** | the glossary, the design, and the right to say no        | "four good local designs and one incoherent system"                 |
| **Liaison**| the requirements, the demo, one voice to the client      | "we each heard something different"; "the client was surprised"     |
| **Planner**| the `QUEUE`, what *done* means, this iteration's plan    | "two people did the same task"; "nobody knows what state we're in"  |
| **Toolsmith** | tests, CI, the one-command reset, the build           | "works on my machine"; "we can't tell whether it is broken"         |

- **Architect** holds the whole design and mostly says no, especially to good ideas
  ([SE1/D9](05-design.md#d9)). A new noun is an event that needs the Architect's decision.
- **Liaison** is one voice each way between the team and the client. What the client says goes
  through this role into the requirements, or it did not happen.
- **Planner** keeps the cursor. Nothing enters the queue without a sentence saying what would make
  it done.
- **Toolsmith** owns the cost of a test ([SE1/F2](03-feedback.md#f2)). When something is hard to
  test, the Toolsmith takes that to the Architect as design information.

Rotation costs a hand-off each iteration. The hand-off is where you discover which knowledge was
living in one head. That is not the cost of rotation; it is the point.

### <a id="h4"></a>H4. The interface between two people is a contract

The interface between two developers is the same object as the interface between two modules
([SE1/D10](05-design.md#d10)). "I'll build the collector, you build the driver page" names two
components and no seam, and schedules an argument for week nine. Before splitting work:

1. **Name the seam** — the call between the pieces, not the pieces.
2. **Write its shape** — signature, schema, error codes, and what happens when the other side is
   absent, late, wrong, or lying. Check it in.
3. **Write the mock that misbehaves on request** — accepts, refuses, hangs.
4. **Write the test that fails today** and passes when the real thing arrives.
5. **Integrate every day.** The mock is a K4, and daily integration is how you learn when it came
   due.

**Meetings are the tax on unwritten interfaces.** If the same meeting keeps happening on the same
topic, an interface is missing; write it and the meeting stops. The minimal set that survives:

| Meeting   | When                                   | Format                                              | Retires                         |
| --------- | -------------------------------------- | --------------------------------------------------- | ------------------------------- |
| Stand-up  | every working day, five minutes        | per person: done / next / blocked — and *since when* | "I didn't know you were stuck"  |
| Demo      | end of iteration                       | the client drives the real system                   | "we built the wrong thing"      |
| Planning  | right after the demo                   | the next queue, priced, with the client             | "we don't agree on what's next" |
| Retro     | after planning, team only              | what did we learn the expensive way → `FINDINGS`    | "we already learned this once"  |

*Since when* is the load-bearing field. A three-day-old blocker is stale data, and should be
presented as stale rather than as current.

> **Ask:** "What meeting keeps happening on the same topic?"

### <a id="h5"></a>H5. The client knows the domain, and cannot see its edges

| They know                                           | They cannot tell you                                         |
| --------------------------------------------------- | ------------------------------------------------------------ |
| the domain, better than you ever will               | what should happen in a case they have never had to think about |
| the pain: who calls, what it costs, who gets blamed | how big a requirement is in *your* world                     |
| the money, the politics, who else has a say         | what they will want once they see it running                 |
| the solution they have already imagined             | that it is a guess                                           |

The right-hand column is not a deficiency; it is the shape of expertise.

**The proportion mismatch.** The client sizes a requirement by its size in their world — spaces,
dollars, minutes. The design sizes it by how many assumptions it invalidates. **These two sizes have
nothing to do with each other.** A requirement covering one space in five hundred can be most of a
redesign; one that sounds enormous can be a line in `Non-goals`. The gap is where K2 lives, and
closing it is the team's job, because only the team knows what the assumptions are.

**What passes between you:**

| The client owes the team                         | The team owes the client                                    |
| ------------------------------------------------ | ----------------------------------------------------------- |
| decisions, on a date                             | no surprises — bad news within a day of knowing it          |
| numbers, with a horizon                          | priced options, with scope as the honest variable           |
| access: the site, the real users, the clipboard  | a running thing to react to, every iteration                |
| one voice that can decide                        | the list of what you are *not* building, read aloud         |
| answers to "what happens today?"                 | a new version, not an edit, when they change their mind     |

| The client who…      | Move                                                                                                     |
| -------------------- | -------------------------------------------------------------------------------------------------------- |
| doesn't show up      | Nominate a teammate to speak for them. Write invented numbers, marked invented. Demo on schedule anyway, and say so in the status. |
| changes their mind   | `REQUIREMENTS_v(n+1)`. Never edit `v(n)`; the diff is the most useful thing you will show them.          |
| wants everything     | Price it. "Yes, and here is what it moves."                                                              |
| is you               | The worst case: every guess confirmed by the only person who could dispute it. Name a proxy for the users, below, and get corrected on a schedule. |
| is surprised         | You failed, not them. Find the delay between knowing and telling; that delay is the bug.                 |

**When the client is the maintainer** — a solo or open-source project — the users are real but never
in the room: integrators, downstream projects, whoever opens the file on another system. Name who
stands in for them: the issue tracker, a downstream project's maintainer, a second maintainer who
did not write the requirement. Send them the requirements with the same sentence, *tell us what is
wrong with it*, and treat their bug reports as the read-back ([SE1/H6](#h6)): each one is a K3 you
held about them.

### <a id="h6"></a>H6. Read your assumptions to the client

The cheapest question in this guide. Every scope decision and every K4 in the requirements is a
sentence the team believes and the client has never been asked about. Read them back as questions:

- "We're assuming every space is the same. True?"
- "We're assuming nobody has a claim on a space before their car is in it. True?"
- "We're assuming a driver never tells the system anything — they only look. True?"
- "We're assuming a lot is either open or closed, and nothing in between. True?"

Each converts a K4 — or a K3 you did not know you held — into K1 for the price of one sentence. The
client answers most in two seconds, and one makes them stop and say "well, except…"

> **Ask:** "We're assuming X. True?"

### <a id="h7"></a>H7. The first conversation: pain before solution, people before features, numbers before nouns

Ninety minutes, in week one, at the site if there is one. The questions are the ones in
[SE1/R3](04-requirements.md#r3); this is the order to ask them in:

1. **The pain** — what happens today when it goes wrong, who gets the call, what they say.
2. **The census** — who are all the kinds of people this touches, and is any treated differently?
3. **The bad day** — walk me through it; show me the clipboard, the radio, the spreadsheet.
4. **The numbers** — how many, in two years; how fast at the peak; how long it may be down.
5. **The edges** — what we are not building; what data about people it keeps; who is affected who is
   not in the room.
6. **The assumptions**, read back as questions ([SE1/H6](#h6)).

The census is the one teams skip. It is not a features question, and its answers arrive as nouns
you have never heard — *season-ticket holders, the VIP gate, the tow contractor.* The client
will not volunteer them, because in their world those are not "the app."

**Output within forty-eight hours:** `REQUIREMENTS_v1` — numbered, observable, with numbers
(invented ones marked), a glossary, `Scope decisions`, `Non-goals`, and `Not yet answered` — sent
with one sentence: *tell us what is wrong with it.*

### <a id="h8"></a>H8. A demo is a test, so run it like one

1. **The real system**, from the one-command reset. Not slides, not a video, not a branch.
2. **The client drives.** Watch their hands and face, not the screen.
3. **Write down every "huh," "oh," "can it…," and "what about…" verbatim.** Do not answer in the
   room; cost them afterward, against the assumptions.
4. **Break something in front of them.** Set a sensor `stuck`. Their reaction to the stale display
   is a requirement they could not have stated in advance.
5. **Read `Non-goals` aloud**, every demo.
6. **Thirty minutes.** Attention is scarce on their side too.

Between demos, status is weekly, three lines, the same shape every time — done, next,
risk-and-since-when — so the one that deviates is a signal.

### <a id="h9"></a>H9. With bad news, the delay is the cost

A two-week slip found in week two is a planning problem; the same slip found in week eleven is a
crisis. The difference is entirely the reporting delay. So the rule is mechanical: **within a day of
knowing, to the person it affects, with a number and an option.**

> "We're a week behind on the collector. We can drop the operator screen from this iteration or slip the
> demo a week. We recommend dropping the operator screen."

Bad news with an option is planning. Bad news without one is a confession that makes the receiver
plan under worse conditions than you had. The same holds inside the team: "I'm stuck" on day one
costs a day; on day five it costs five, plus four days of others building on the assumption it was
coming.

> **Ask:** "How many days between knowing and telling?"

### <a id="h10"></a>H10. Settle disagreements by category, then by reversibility

Four moves, in order. Most arguments end at the first.

1. **Is it a category dispute?** *What requirement would have to disappear for this complexity to go
   away?* ([SE1/D8](05-design.md#d8))
2. **Set the intensity by reversibility.** A one-way door gets the whole team and a written
   decision. Everything else is decided by whoever holds the relevant role, with the reason written
   down and a revisit date.
3. **If it is still split and cheap to test, spike both** against the same test. An afternoon each
   beats a week of two competing K3s.
4. **Disagree in the conversation, not in the commit.** Once decided, it goes into `Scope decisions`
   with its reason; reopening it requires new information, not a new mood.

### <a id="h11"></a>H11. Being behind is a systems failure with a schedule

A person who is behind is like a queue near full utilization: every new item waits longer than the
last, and the delay grows faster than the load.

- **Do not add work to the person with the most knowledge.** That is the instinct, and it is the bus
  factor getting worse in real time.
- **Redistribute, pair, or cut scope** — in that order, and say which at stand-up, with *since
  when*.
- **It is not a character flaw.** Treat it as one and it will happen again, silently, because nobody
  will report it early.
- **Distribute discomfort deliberately and visibly** — on-call, review load, the tedious work.
  Burnout shows up as attrition.

The most dangerous team member is the one carrying the project. Rotate the roles anyway, and pair
them with the person who knows least.

### <a id="h12"></a>H12. Fix the process, not the person

Nobody is blamed for K2. A finding says *findable by X; X is now on the list* — not who should have
asked. A client who feels blamed for a surprise stops volunteering the next one, and the next one is
the expensive one. When a client says "I should have mentioned it," the answer is: "You did mention
it. We didn't ask."


---

## Case study: "It does the VIP spaces too, right?"

End of iteration two, four weeks in. The demo of the parking system went well. Walking to the door,
the client says:

> "This does the VIP spaces too, right? Season-ticket people book a space from their phone on the way
> in, it's held for thirty minutes, then it opens back up. It's only about two hundred spaces."

Two hundred in a hundred thousand — one in five hundred. To the client, a rounding error. The team's
first instinct matches: *a flag on the lot and a small table.* Here is what the sentence does to a
design that was not expecting it:

| The team believed                          | What the VIP sentence does to it                                                                    |
| ------------------------------------------ | --------------------------------------------------------------------------------------------------- |
| A lot is a count: `available = capacity − occupancy`. | A held space is free to the sensor and not to the driver. Availability has three inputs, one of which expires on a clock. |
| Counts, not locations.                     | A hold is (person, place, time): the first location record about a named person. Retention gains a legal dimension. |
| One sensor per lot.                        | VIP is rows *inside* lots. The sensor cannot see the boundary.                                      |
| Drivers are anonymous readers.             | The first write from the driver side; a new identity; authenticated writers.                       |
| The sensor is the only source.             | A second source — whoever says who is VIP — with four unfaulted failure cases.                      |
| Readings are idempotent ("set to 37").     | "Hold one space" is not. A retry double-books; it needs an idempotency key and a race decided in the database. |
| Time is for detecting skew.                | Thirty minutes is a promise to a person, kept by a clock. Daylight-saving's repeated hour now lands on a driver. Tests need an injectable clock. |
| A read can ride out a maintenance gap.     | A write cannot serve stale. Can anyone hold a space during the 2am migration?                      |
| `available` means one thing to every consumer. | If it now excludes held spaces, an existing field changed meaning — a breaking change.        |
| The peak is arrival.                       | A new peak: the instant holds open. A herd on a tiny resource.                                      |
| Reservations are a non-goal.               | The one line that was written down. `grep` finds the collision in a second.                         |

For one space in five hundred.

**The first casualty is a word.** `available` now means *physically free* to the sensor and *free
and not held* to a driver — one word, two things ([SE1/D9](05-design.md#d9)). Before any code moves,
the Architect settles the vocabulary: `available` keeps its meaning; a **zone** is part of a lot
with a class and a capacity; a **hold** is a claim on one space in a zone, by a **holder**, for a
bounded time, and is `held`, `arrived`, `expired`, or `released`. Three new nouns and one protected
old one. That is the whole pivot at the level where it is cheap.

**Why it was late.** It was findable in week one, at K1 price, by any of three questions already on
the intake list: the census of people ("season-ticket holders get the VIP rows"), the bad-day walk
(a printed list and a row of cones at the gate), or reading the assumption back ("nobody has a claim
on a space before their car is in it — true?" "Well — except VIP"). The client's sense of proportion
filtered it out; the team's should have overridden the filter, and could not, because nobody asked.
The site walk, done four weeks late, found a second surprise in ten minutes: "the VIP lot" is the
front two rows of four different lots.

**What late costs.** In week one: three glossary nouns, a derivation with three inputs, a new
identity, an injectable clock, a write budget — about a day, mostly conversation. In week four: all
of that, plus reopening scope decisions recorded so they would not be reopened, a schema change
under data, and *unlearning* "a lot is a count," which every teammate now holds as K0 — two weeks,
and the next iteration's plan. In week ten: plus a versioned API, because browsers and other callers
depend on it. After launch: plus the outage. The biggest step is not in code. It is in *belief*: the
point where a K4 that could have been chosen became a K3 that has to be excavated.

**The trap: "it's just a flag."** Someone — or an agent, in five minutes — proposes an `is_vip`
column, a `reservations` table, and a subtraction in the shared query. It runs. The tests pass.
Nothing collapses, because nothing in software has mass ([SE1/F4](03-feedback.md#f4)). Hidden in it:
`available` silently means two things; a retry double-books; the 2am migration blocks every hold and
nobody said whether that is allowed; the membership list's failure modes are whatever the HTTP
library does; the repeated hour expires holds early or late depending on a string comparison.

**What the team does:**

1. **Name it in the room, without yes or no.** "That's a new kind of thing — a claim on a space
   before a car is in it. Give us until Thursday to cost it."
2. **Cost it against the assumptions, not the code** — the table above, one hour, whole team, the
   Architect leads. The unit of cost is *invalidated assumptions*.
3. **Bring priced options, with scope as the variable, and recommend one:**

   | Option | What it is                                                             | Costs           | Forecloses                                  |
   | ------ | ---------------------------------------------------------------------- | --------------- | ------------------------------------------- |
   | A      | Counts only; a VIP zone shows its own count; gate staff keep holding.  | days            | nothing — the zone noun is in               |
   | B      | Holds with expiry and holder identity, confirmed at the gate.          | two iterations  | the next iteration's plan                   |
   | C      | Full reservations: payment, enforcement, cancellation.                 | the term        | payment is a one-way door with a regulator  |

   Recommend B if time allows two more iterations after it, A if not — and A is not a loss, because
   it introduces the zone noun and the stated assumption that B needs first.
4. **Version the requirements** — `v2`, with `Non-goals` changed and a reason on the line.
5. **Record the finding** — *VIP holds found at the week-four demo; findable in week one by the
   census question or the site walk; both are now on the intake list.*
6. **Fix the process, not the person** ([SE1/H12](09-people.md#h12)).
7. **Re-plan with slack, and do not add a person.** A cross-cutting change is coherence work, and
   coherence does not parallelize.
8. **Ask what became deletable.**

Notice what moved in the eventual design: not the sensor, not the collector, not the signing. Only
vocabulary, derivation, identity, time, and policy — the parts decided in week one by not deciding
them.

---

Next: [10. Agents](10-agents.md) — what changes when a teammate has no memory and no stake.
