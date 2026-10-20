# 3. Feedback

How you find out you are wrong: what a test costs, which loop catches which error, why software has
to build its own warning signals, and what happens to a signal once it becomes a target. (How to
write tests worth trusting is [6. Testing](06-testing.md).)

---

### <a id="f1"></a>F1. The cost of a test decides the method

You cannot build a second bridge to see whether the first one stands. A wind-tunnel hour is
expensive, a chip mask set is expensive, a recall is catastrophic. So those disciplines front-load
everything — analysis, simulation, review, sign-off — before anything is cut. That is not a bad
habit; it is the correct response to a test that costs a million dollars and takes a year.

Software tests can be free, run in a second, and run ten thousand times a day. Nearly everything
filed under "agile" is downstream of that single fact.

The cost is **per decision, not per project.** Changing a route handler takes seconds to verify.
Changing a schema with real data under it does not. A leaked private key cannot be unleaked. A
published interface with users on it is a promise. So you run a careful, front-loaded process around
the decisions that are expensive to test, and fast loops around the cheap ones — and that can change
twice in an afternoon ([SE1/W4](08-work.md#w4)).

> **Ask:** "What does it cost to find out we are wrong about this — and to undo it?"

### <a id="f2"></a>F2. The cost of a test is designed, not given

Lowering it is ordinary engineering work with a known toolkit:

- pure functions, with state pushed to the edges ([SE1/D7](05-design.md#d7));
- deterministic seeds, and an **injected clock** — the current time passed in as an argument
  instead of read from the system — so a failure is the same failure tomorrow;
- faults driven on demand through a **control plane** — a side channel, such as a test-only
  endpoint, that tells a component to be slow, down, or wrong — instead of waited for;
- one command that returns the whole system to a known state;
- **conformance** checkable from outside: a test suite that any implementation of an interface must
  pass, run without reading that implementation's source;
- logs that record the inputs that drove each decision, so a failure explains itself.

**Lowering the cost of a test is often the highest-leverage work available, because it multiplies
against every future change.** And the inverse is diagnostic: *if something is hard to test, that is
information about the design, not about testing.*

> **Ask:** "What would make this cheap to test — and what does its being expensive say about the
> design?"

### <a id="f3"></a>F3. Push each class of error down to the cheapest loop that can catch it

Testing is one feedback loop among several. Each has a cost, a latency, and a fidelity, and each
catches a different class of error:

| Loop                  | Latency  | Catches                                                     |
| --------------------- | -------- | ----------------------------------------------------------- |
| Compiler, type checker, linter | instant | typos, wrong types, banned patterns — and style, so review needn't |
| Running the thing     | seconds  | "it doesn't work at all"                                    |
| Unit test             | seconds  | broken logic, regressions                                   |
| Integration test      | minutes  | wrong assumptions between components                        |
| Human review          | hours    | unclear intent, missing cases, bad design                   |
| Client demo           | days     | building the wrong product                                  |
| Production telemetry  | live     | everything you didn't imagine — at the worst possible price |

Some errors are catchable *only* by an expensive loop. No test suite in the world detects "we built
the wrong thing." Only a person looking at the running thing does.

> **Ask:** "What is the cheapest loop that could have caught this?"

### <a id="f4"></a>F4. Nothing has mass, so build the signals

Mass supplies error signals for free: a bad structure sags, cracks, or falls down, and nobody has to
be clever to notice. **Software has no gravity, so nothing collapses to tell you.** A bad design
holds itself up indefinitely, at full speed, with the tests passing.

Every feedback loop in this chapter exists to replace a signal that mass would have given away. None
of them arrive by default.

> **Ask:** "If this design were wrong, what would tell us — and when?"

### <a id="f5"></a>F5. When a measure becomes a target, it stops measuring

Not because people are dishonest. Structurally: the measure was a proxy for something you cared
about, and optimizing the proxy detaches it from the thing.

- Aim at coverage percentage, and you get tests with no assertions.
- Aim at velocity, and estimates inflate.
- Aim at uptime, and incidents get reclassified as maintenance.
- Require "every requirement has a test that names it," and you will get tests that name the
  requirement and assert nothing.

The only defense is to keep the *reason* attached to the rule everywhere the rule appears. A
practice whose purpose has been forgotten is already being gamed — including by people who think
they are following it.

> **Ask:** "If this were graded, what is the cheapest way to fake it?"


---

Next: [4. Requirements](04-requirements.md) — where the problem comes from.
