# 4. Requirements

Nobody hands you the problem. Requirements are built, not collected — by writing claims precise
enough for the people who know the domain to reject them.

Two words used precisely in this chapter:

- **Observable** — checkable from outside, without reading the source. "The page shows the age of
  any count older than fifteen seconds" is observable. "The code is clean" is not.
- **Requirement vs. design** — a requirement is what must be observably true; a design is the
  mechanism chosen to make it true ([SE1/R5](04-requirements.md#r5)).

---

### <a id="r1"></a>R1. Keep the pain; test the solution

You are handed a sentence: *"We need an app that shows which lots have spaces."* That sentence is
not a requirement. It is a wish with a user interface already attached.

Nothing exists yet except two things:

- **a pain**, which is real evidence, and
- **a proposed solution**, which is a guess.

Clients almost always know their domain far better than you do, and that is exactly what makes
their proposed solution dangerous: it arrives confident and pre-formed, backed by the person paying,
and it does not look like a question — so it triggers no investigation. That is K3, inherited
without an audit.

Walk back up from the solution to the pain. *What happens today when a driver can't find a space?
Who gets the phone call? What do they say?* In the parking example the answer might be "gate staff
radio each other and guess," which means the real user may be gate staff and the real requirement
may be about trusting a number, not about a map.

> **Ask:** "What happens today when this goes wrong, and who gets the call?"

### <a id="r2"></a>R2. Specific and wrong beats vague and safe

*Changed in v1.1.*

Requirements do not exist, even in principle, until someone writes a candidate down. The client
cannot tell you what should happen when a sensor goes silent, because they have never thought about
it. They can tell you in two seconds when they read your sentence saying *the count freezes at its
last value and the page keeps showing it as current.* "No! Absolutely not."

So the first draft's job is **to be wrong in a way that is cheap to correct.** "The page refreshes
every five seconds" gets corrected. "The page is responsive and up to date" gets nodded at, agreed
to, and means something different to each person — discovered in week nine. A sentence that cannot
be wrong cannot teach you anything.

This is the same move as a test that fails before the fix: state the claim precisely so that reality
is *able* to reject it.

Requirements are therefore **numbered** *and versioned* (so tests, commits, and reviews can cite
them), **observable** (so they can be checked), and contain **numbers** — invented ones marked as
invented. An invented number that is written down can be challenged. An assumed one cannot.

Because requirements and design change, unversioned references to requirements and design documents
are K3 factories ([SE1/U7](02-unknowing.md#u7)): the citation keeps looking current after the
text it pointed at has moved ([SE1/R10](#r10)).

> **Ask:** "Could the client read this sentence and say 'no'?"

### <a id="r3"></a>R3. Ask the questions nobody volunteers — the ones that could invalidate the plan, first

None of these are about features. All of them get answers nobody offers unprompted.

| Ask                                                          | Because                                                                     |
| ------------------------------------------------------------ | --------------------------------------------------------------------------- |
| "Who are all the kinds of people this touches? Is any treated differently?" | A census of users. Answers arrive as nouns you have never heard.            |
| "How many? And in two years?"                                | "A city" is a mood. A number with a horizon is a design input.              |
| "What are we explicitly *not* building?"                     | The cheapest scope decision there is; it ends the same argument permanently.|
| "What if this input is absent? late? wrong? lying?"          | Four cases every consumer inherits by accident if nobody asks ([SE1/R6](04-requirements.md#r6)). |
| "What does a bad day look like? Show me the clipboard."      | Surfaces recovery, workarounds, and the special cases.                      |
| "How long may it be down, and when?"                         | Unstated, everyone quietly assumes 100% — the most expensive requirement you can accidentally accept. |
| "What data about people does this keep, and who may see it?" | The question with a regulator attached ([SE1/R8](04-requirements.md#r8)). |
| "Who is affected who isn't in this room?"                    | Bystanders, the surveilled, the person shown the wrong number.              |
| "What would you do differently with this answer?"            | Kills features fast. If nothing changes, nobody needs it.                   |

Order matters. **Questions whose answer could *invalidate* the plan come before questions whose
answer only *shapes* it.** Each is a sentence to ask in week one and a month to discover in week
four.

### <a id="r4"></a>R4. A requirement with no price attached is a wish

Every sentence in a requirements document is a purchase someone has to authorize. "Yes, and here is
what it moves" is the answer to "we want everything."

> **Ask:** "What does this sentence cost, and who agreed to pay it?"

### <a id="r5"></a>R5. A requirement says what must be observably true; a design says how

A requirement cannot change without the client; a design can. Put a design decision in the
requirements and you have promised the client a table name. Put a requirement in the design and
whoever edits the file next can quietly change it.

A sentence must pass both tests to be a requirement:

> **Could a different team satisfy this sentence a different way?**
> **Could you check it from outside, without reading the source?**

| Requirement (what must be observably true)               | Design (the mechanism chosen)                                           |
| -------------------------------------------------------- | ----------------------------------------------------------------------- |
| A stale count is never presented as current.             | The collector stamps receipt time; staleness is computed from elapsed time. |
| Every reading is attributable to a device.               | Each device signs readings with its own key; a registry holds the public keys. |
| One command returns the system to a known state.         | A script that deletes the database volume and reloads the seed data.   |
| A revoked device is rejected by the next poll.           | The collector re-reads the device table every cycle, so there is nothing to invalidate. |
| A person's identity is never joined to a location.       | The sightings table has no person column, and no view that could add one. |

The tells that a requirement has design in it: a table name, a library, a language, an HTTP status
code, an endpoint path, an algorithm. The tell that a design has a requirement in it: "the user must
be able to…" with no mechanism following.

**A change that edits a requirement to match what the code happens to do is a design change wearing
a costume.** And a gap between the requirements and the code is work to be done, not an error in the
requirements.

> **Ask:** "Could another team satisfy this a different way?"

### <a id="r6"></a>R6. Every input has four failure cases: absent, late, wrong, and lying

Most specifications describe the happy path and inherit the rest by accident — whatever the HTTP
library happens to do on timeout becomes the product's behavior, chosen by nobody.

For every input a component depends on, state an answer for each case:

| Case       | Example                                          | Someone must decide                         |
| ---------- | ------------------------------------------------ | ------------------------------------------- |
| **Absent** | the sensor does not answer                       | wait, serve stale, refuse — and tell whom?  |
| **Late**   | it answers after the next poll was due           | how long is too long, and who chose that?   |
| **Wrong**  | it reports more cars than the lot has spaces     | reject, clamp, or flag — and which is a fault? |
| **Lying**  | `200 OK`, plausible data, frozen since Tuesday   | how would anyone notice?                    |

One kind of *wrong* looks valid: an input that **announces a feature you do not support** — a
version number, a feature bit in a file header, a capability in a handshake. State an answer per
feature: **refuse**, **read-only** (use what you understand, change nothing), or **read-write**.
"Ignore it" is not an answer; it is how a program comes to write data it had no right to write.

A system that only works when its inputs behave is not finished. And an adversary is just the
unknown that optimizes: **security is this same discipline applied to an input chosen specifically
to find your K3.**

> **Ask:** "What happens when this input is absent, late, wrong, or lying?"

### <a id="r7"></a>R7. Scale, recovery, and availability are answered whether or not anyone writes them down

Unstated, the answer is whatever the implementation happened to do — chosen by nobody, discovered in
production. All of them are **client answers**, not engineering choices, and on day one each costs a
sentence. Later they cost a migration, a rewrite, or an outage.

**Scale** is an order of magnitude plus a horizon. "A city" is a mood; "a hundred lots, a hundred
thousand spaces, one sensor per lot reporting every five seconds, an event crowd arriving over two
hours, ninety days of history" is a design input. Ask "and in two years?" Then write down the number
you are explicitly *not* designing for. Do arithmetic on the answers: if the thousand-space lot
nearest the gate fills in the first twelve minutes, that is 1.4 cars a second, so a count ten
seconds old is already wrong by fourteen spaces. That is how a staleness threshold (say, fifteen
seconds) should be chosen: derived from the client's numbers, not picked because it is round.

**Speed** belongs here too. "Fast" is a mood; "the driver page loads in under a second for 95% of
requests at the event peak" is a requirement — a latency, a percentile, and the load it holds
under.

**Recovery** is two questions, and the second is the one that gets skipped. What does the system do
*while* X is down — degrade, wait, refuse, serve stale — and does the user learn which? And what
does it take to get back: who, which command, which backup, how long? That answer is real only if
someone has run it and timed it. Answer per component, not for "the system." And **how much data may
we lose** is itself a requirement, to be decided by someone entitled to decide it.

**Availability** is a budget with a period and a beneficiary: the driver page may be down forty
minutes a month; the ops screen a day; a missed sensor poll bothers nobody. Different parts deserve
different budgets — that is what lets you spend money where it matters. Unstated, people assume
100%, which quietly forbids deploys, restarts, and migrations. The number chooses the architecture,
mostly by choosing whether a human is allowed in the loop:

| Budget  | Down per month | What it implies                                         |
| ------- | -------------- | ------------------------------------------------------- |
| 99%     | 7 hours        | a person can notice and fix it                          |
| 99.9%   | 43 minutes     | alerting that pages, and a runbook someone has run      |
| 99.99%  | 4 minutes      | no human in the loop — paging someone and having them log in takes longer than the whole budget — so redundancy and automatic failover |

The shape of the answer matters as much as its value. "Forty minutes a month, never during an
event; maintenance allowed 02:00–04:00" is honest. Folded into a single number of nines, it would be
easier to agree to and mean nothing — because it would not say *when* the downtime may fall.

**Resources** belong in the envelope wherever they are finite — code size, memory, stack, storage,
energy — each as a number with a test that measures it. An inherited figure nobody has measured is a
K3 ([SE1/U3](02-unknowing.md#u3)). And where power or a connection can vanish at any instant,
**interruption** is a normal event, not an incident: say what must still hold after a cut at any
point — "the data on disk is the old version or the new one, never a mix" — and test it by cutting.

> **Ask:** "How many, in two years? How fast, at the peak? What happens when it breaks, and how long
> to get back? How long may it be down, for whom?"

### <a id="r8"></a>R8. Security, law, and ethics are always requirements

They are the easiest to postpone, because they are not software. No test fails without them, no user
files a ticket for them, they compete with visible features, and their absence looks exactly like
their presence until it doesn't. They are requirements on every project whether or not anyone states
them: a class project that logs license plates keeps location data about people, and a library
hands its license and its vulnerabilities to everyone who ships it. Two properties make deferring
them a mistake rather than a trade-off:

- **Their deadline is set by someone else** — a breach, an audit, a complaint, a regulator.
- **Violations are irreversible.** Leaked data cannot be unleaked. A person harmed is not fixed by a
  patch.

Left out, they are where a project keeps its most expensive unknowns ([SE1/U1](02-unknowing.md#u1)):

- **K2** — the rule nobody on the team had heard of: a privacy law, an accessibility requirement, a
  license term on a dependency.
- **K3** — the sentence everyone was sure of: "we don't store anything personal," "nobody would try
  that," "this code is ours to use" — while the logs hold plates, someone tries it, and the snippet
  came from a GPL file.

The usual cure for K2, exposure to reality ([SE1/U2](02-unknowing.md#u2)), arrives here as the
breach or the lawsuit. So do not wait to be surprised: ask, early, someone who knows the rule — the
client, a lawyer, a security reviewer, the people the data is about — and turn each into a K1 with
an answer written down.

In practice:

- **Security.** Write the threat model: who the adversary is, what they can do, what they want.
  Design against that, not a vague sense of danger. Every dependency is a transfer of trust.
- **Law.** Mostly about data: what you collect, how long you keep it, who you must notify, what you
  may reuse. Also licensing, and the provenance of code — including code an agent produced.
- **Ethics.** The people affected who are not in the room. Parking data is location data about
  people; *"counts, not locations"* is an ethical decision wearing technical clothes — nearly free
  to make now, nearly impossible to retrofit. **The safest record is the one you never kept.**
  Accessibility and translation live here too.

The cheapest moment to satisfy all three is while the requirements are still soft. After that you
are not adding a requirement; you are performing a migration.

> **Ask:** "Who, outside this room, does this system keep a record about?"

### <a id="r9"></a>R9. Write down what you decided not to do

Four short lists, each nearly free, each ending an argument permanently:

| List                 | Holds                                                         |
| -------------------- | ------------------------------------------------------------- |
| **Scope decisions**  | choices made, with the reason ("counts, not locations")       |
| **Non-goals**        | what is explicitly not being built                            |
| **Not yet answered** | open questions, stated as open — guesses nobody has agreed to |
| **Deferred**         | work not taken on *yet*, named so it is not mistaken for an oversight |

They also make a late collision findable. When the client asks for reservations in week four,
`grep -i reservation` finds the line in `Non-goals` in a second; unwritten, it is found in review in
week nine.

> **Ask:** "What did we decide against, and where would someone find that?"

### <a id="r10"></a>R10. Version requirements; never edit them in place

*Changed in v1.1.*

A superseded requirement is not deleted knowledge. Editing in place destroys the before-picture, and
the diff between `v1` and `v2` is the most useful conversation you will ever have with the client.
Once a second party depends on a statement, changing it is a version, not an edit — the same rule as
a published interface ([SE1/D11](05-design.md#d11)).

**Cite the version that last changed it.** A requirement is cited as `REQ2/UI-1`: UI-1 as worded in
`REQUIREMENTS_v2`. Each requirement carries the version that last changed it — `UI-1` *(since v2)* —
and citations use that version, not the newest. If v3 carries UI-1 over unchanged, `REQ2/UI-1` is
still exact and nothing is renamed. If v3 changes it, every `REQ2/UI-1` — in a test name, a commit,
a `QUEUE` item — is now visibly stale, and a search for it finds exactly the work to revisit. A
design is cited the same way: `DESIGN_v2`, never a bare `DESIGN`.

### <a id="r11"></a>R11. An API is the set of observables your acceptance tests need

*Changed in v1.1.*

The chain from a story to an interface runs through five artifacts, and the step people skip is
the one from the test to the observables it needs:

```
user story → acceptance criteria → acceptance test → observables the test needs → the contract
 who, what,    observable,          fails today       fields, states,              the API
 and why       numbered                               endpoints
```

- **Story:** *As a driver arriving for an event, I want to see which lots have space, so that I can
  go straight to one.* The reason is the pain; the want is a guess at the solution.
- **Criteria:** the page shows a count per lot; a count older than the staleness threshold is shown
  with its age and never as current; a lot with no trustworthy data reads as *unknown*, not missing.
- **Acceptance test**, written to fail today (the sensor's *control plane* is a test-only way to
  tell it to misbehave — see [SE1/F2](03-feedback.md#f2)):

  ```
  set lot 3's sensor to "stuck"        # answers 200 OK with a frozen timestamp
  wait past the staleness threshold
  GET the driver view
  assert lot 3 shows a count with an age, and is not marked current
  ```

- **Observables:** to assert "with an age," the view must expose an age. To assert "not current," it
  must expose a state. To drive the fault, the sensor must have a control plane. Those fields *are*
  the contract — and they exist because a test needed to observe them.

Design the tests and the API falls out. Design the API first and you ship fields nobody can test and
miss the ones somebody needed. A harder story makes the point sharper: *hold a space for thirty
minutes* forces an expiry time, an idempotency key (so a retried request does not take a second
space — [SE1/D4](05-design.md#d4)), and a race decided inside the database — the
test for "exactly one of two simultaneous requests wins" chooses the design.

Two consequences:

- **A story with no test is a wish.** It cannot be wrong, so it cannot be finished.
- **A test with no story is accidental complexity.** It protects something nobody asked for.

Name each test by the requirement it covers. Then a test run stops being a count of passes and
becomes a scoreboard — *these stories are green, that one turned green today* — which a client can
read without reading code. It is honest only while every green could have been red
([SE1/F5](03-feedback.md#f5)).

**The trace lives in the test names, not in the requirements.** A requirements document that lists
its tests turns every new test into an edit to a versioned document ([SE1/R10](#r10)). The test
carries the versioned requirement ID instead ([SE1/R10](#r10)), so a search for `REQ2/UI-1` across
the tests is the trace and the test run is the status. A *must* with no test yet is a `QUEUE` item, not an empty column.

> **Ask:** "What does the test have to observe to assert this?"


---

Next: [5. Design](05-design.md) — what software is made of, and what it costs to carry.
