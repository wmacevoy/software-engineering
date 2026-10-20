# 6. Testing

How to make tests worth trusting. (Keeping the environment around them the same, and testing what
runs in production, are in [7. Operating](07-operating.md).) Generalized from the ArduinoUnit
guidebook, *The Zen of Testing*, which was written for devices with two kilobytes of RAM and
therefore could not afford to be vague.

Terms used here:

| Term               | Meaning                                                                                         |
| ------------------ | ----------------------------------------------------------------------------------------------- |
| **Repeatable**     | The same test, run again — alone or beside any other, in any order, on any machine — gives the same verdict. |
| **State**          | Anything a test reads or writes that outlives it: a row, a file, an environment variable, the clock, a port, a singleton. |

---

### <a id="t1"></a>T1. A test is a fear with a name

"Tests retire the fear that I broke something" is true of a suite and too coarse to act on. Testing
is a family, and each member retires a different fear:

| Test what      | The question                                    | The fear it retires                                                |
| -------------- | ----------------------------------------------- | ------------------------------------------------------------------ |
| Configuration  | Is a startup requirement missing?               | "it will fail at 3am for something we could have checked at boot"  |
| Status         | Is a component broken right now?                | "it is broken and nobody can tell"                                 |
| Input          | Is the input absent, late, wrong, or lying?     | "garbage got in"                                                   |
| Output         | Is the result in bounds and in the right shape? | "we said something impossible"                                     |
| State          | Is what we hold still sane?                     | "we drifted into nonsense and kept answering"                      |
| Time           | Is it taking too long?                          | "it will not keep up"                                              |
| Space          | Is it taking too much room?                     | "it will fill up"                                                  |

If you cannot say which row a test belongs to, find the row or delete the test
([SE1/P4](01-purpose.md#p4)). And watch it fail once ([SE1/T3](06-testing.md#t3)).

> **Ask:** "Which fear does this test retire, and have I ever seen it fail?"

### <a id="t2"></a>T2. Climb the reliability ladder: a reliable thing checks itself

The guidebook's ladder of six checks, stated for a microcontroller and generalized. Each
generalization is usually something a larger system has forgotten to do — because, having gigabytes
to be careless in, it *could* forget.

| Step                    | On a microcontroller                                 | In general                                                                       |
| ----------------------- | ---------------------------------------------------- | -------------------------------------------------------------------------------- |
| The idiot light         | an LED blinks if any test has failed                 | one pass/fail visible from across the room: an exit code, a badge, a health endpoint |
| The power-on self test  | refuse to run if the flash or display is bad         | refuse to start if a precondition is missing — loudly, early, before serving anyone |
| Sanity, repeated        | rerun a sanity check; soft-reset when it fails       | invariants checked continuously in production, and a safe state to fall back to |
| IO                      | a mock stream stands in for the serial port          | a mock for every input, that misbehaves on request                                |
| Time                    | a budget in microseconds, safe across rollover       | a budget with an assertion, measured by a clock that only moves forward          |
| Space                   | free bytes above a floor; check every allocation     | rows, logs, memory, disk — sized from the numbers, every acquisition checked     |

Two deserve more than a row.

**The power-on self test.** *If your thing can't run without certain things, make sure those things
are OK, or stop.* The larger-system failure is the opposite: start anyway, log a warning, and serve
wrong answers until someone reads the log. A server that falls back to `secret = "dev-secret"` when
the real secret is missing is a self test that lets you drive off with the hood open — and the exact
shape of every "temporary" default that reaches production. **A missing precondition is an exit
code, not a warning**, unless someone has written down why not ([SE1/O8](07-operating.md#o8)).

**Sanity, with a safe state.** Invariants checked *while the system runs*, not only in the suite,
with a stated and tested move to a safe state when one is violated: restart, fail over, serve the
last good value *with its age attached*. The reboot is not the embarrassing part. The embarrassing
part is a system that has noticed it is insane and keeps answering.

> **Ask:** "Does the thing say so when it is broken?"

### <a id="t3"></a>T3. A test that cannot fail proves nothing

Watch every test fail before you trust it: write it, run it against the code without the change, see
red, then make it green. A test written after the fact and never observed red is a K3 factory
([SE1/U7](02-unknowing.md#u7)) with a green checkmark.

Tests that pin down behavior that already exists — before a refactor, or for legacy code — cannot
fail "without the change," because there is no change. Break the code on purpose instead (flip a
comparison, delete a line), watch the test go red, and restore it. Mutation testing automates
exactly this ([SE1/T10](#t10)).

The same holds for the **instruments** around the tests — sanitizers, coverage, linters, warning
flags, type checkers. Each is a test of the tests, and each can be switched off without a sound: a
build file that overwrites a flag, a config that excludes a directory, a tool that exits zero because
it found nothing to check. A suite seen red under an instrument that never engaged still proves
nothing about what the instrument was for. Make each one fire once on purpose — an out-of-bounds
write the sanitizer must catch, a branch the coverage report must show as missed — or have a check
prove the flag reached the compiler.

> **Ask:** "Have I seen this test fail — and this instrument fire?"

### <a id="t4"></a>T4. A loop you do not trust is worse than none

Flaky tests train a team to ignore red, and after that the suite that would have caught the real
failure has been disarmed. Unseeded randomness, the wall clock, shared mutable state, and fixed
ports are banned from tests for this reason, not for tidiness ([SE1/T5](#t5)). Fix or quarantine a
flaky test the day it is found; a suite with known-flaky tests is a suite nobody reads.

The same holds for production alarms ([SE1/O4](07-operating.md#o4)).

> **Ask:** "When this goes red, does everyone believe it?"

### <a id="t5"></a>T5. Repeatability is a property of the state a test touches

A flaky test trains a team to ignore red ([SE1/T4](#t4)). Repeatability is not a property of the
test; it is a property of **the state the test touches**, and that state has exactly three scopes:

| Scope       | What it means                                         | Repeatable?                                                    | Examples |
| ----------- | ----------------------------------------------------- | -------------------------------------------------------------- | -------- |
| **Local**   | the test creates it and destroys it                   | yes, and safe in parallel                                      | a pure function's arguments; a temp directory; a fresh object |
| **Sharded** | shared infrastructure, partitioned so each test owns a slice | yes — if the key is unique and the test stays in its slice | a schema per worker; a record the test creates and drops; a container per job |
| **Global**  | one instance, read and written by everyone            | no. **A test that modifies global state is a race condition, not a test.** | a shared dev database; a seeded row two tests update; environment variables; the system clock; a singleton; a fixed port |

A test that writes global state passes alone, then fails when another test runs first, or at the
same time, or against the rows yesterday's run left behind — and it tends to fail on someone else's
machine, where you cannot see why. Everything you have heard about flaky tests is that row.

Fixes, in order of preference:

1. **Make the state local.** Pull the logic out of the state ([SE1/D7](05-design.md#d7)) and pass
   the dependency in.
2. **Shard it.** Give each worker a slice with a key it owns: its own database schema, its own
   records, its own mock sensor. Two tests that share one mock sensor and each tell it to misbehave
   differently are racing; give each test its own sensor and the race is gone.
3. **Serialize it, and say so.** A lock, or a concurrency of one. It works and does not scale. Write
   down why, so the next person can undo it.

Read-only global state is fine. The dangerous combination is *global and mutated*. Two pieces of it
hide in plain sight:

- **The clock.** `now()` is a global read that differs every run. Inject the clock, exactly as you
  seed the random number generator.
- **The shared environment.** When some state really is global — a database shared by the
  integration tests — give it a reset: one command that returns the whole system to a known state.
  Make it cost ten seconds, so people actually run it.

> **Ask:** "What does this test write, and who else can read it?"

### <a id="t6"></a>T6. The mock and the real thing answer to the same test

You cannot test input handling without controlling the input, and the code that reads the real input
is exactly the code you want to test. The answer is a mock for every input that **misbehaves on
request** — a sensor that can be told to be slow, down, stuck, wrong, flapping, or skewed — plus a
design that keeps the reading separate from the deciding ([SE1/D7](05-design.md#d7)).

A mock is a K4: *the real thing behaves like this.* It is false the day you write it, because you
wrote it from your idea of the real thing, and the real thing has behaviors you have not imagined
yet. Two rules keep it honest:

- **One conformance check for both.** The mock and the shipped component answer to one
  specification, checkable from outside, so swapping them is an event with a result rather than a
  discovery.
- **Integrate continuously.** A mock converts a scheduling risk into an integration risk
  ([SE1/W5](08-work.md#w5)). Mock everything and integrate at the end, and every piece arrives on
  time into a system that does not work.

> **Ask:** "Does the mock fail the way the real thing fails — and does one test check both?"

### <a id="t7"></a>T7. Test user interfaces by pulling the logic out first

UI tests fail for one reason more than any other: they are global-state tests in disguise — a shared
server, a shared browser, the real clock, animations of variable length. Every fix in [SE1/T5](#t5)
applies, and one applies first: **pull the logic out of the UI.** If the server derives a value, the
value can be tested without a browser. If translation is a function `t(key, params)` that looks the
text up in a table, it is a pure function; test it as one.

Then three loops, cheapest first:

| Loop                                             | Latency | Catches                                                       |
| ------------------------------------------------ | ------- | ------------------------------------------------------------- |
| the logic behind the UI, as functions            | seconds | a wrong derivation, lookup, or state machine                  |
| the DOM in a headless browser, against a real server | minutes | the wiring: the click reaches the route, the response reaches the page |
| a person driving the real thing                  | days    | the wrong product                                             |

Assert on text and state, not pixels. A screenshot comparison fails when a font is hinted
differently on another architecture.

> **Ask:** "What logic is hiding in this UI that could be tested as a function?"

### <a id="t8"></a>T8. When you don't know how to build it, write the tests that would pass when it works

Planning every detail is a waste; so is charging into the woods. The map is the tests: write the
ones that would pass when the thing works, and they tell you what the thing is — including what it
does not have to be. For adversaries, the same rule: **for each attack in your threat model, write
the demonstration first and do not trust the defense until you have watched it refuse**, because a
defense nobody has seen refuse an attack is a K3 with a code review ([SE1/U3](02-unknowing.md#u3)).
Where an attack cannot be performed safely — stealing a real key, flooding a live service — perform
it against a copy or a simulation, and say which.

Solve problems in parts you can test, test the parts together, and keep the parts and their tests.
The guidebook's example is a hot dog cart that will, sooner or later, be asked to become a taco
stand: every project changes direction, and what survives the change is the code built in testable
parts.

> **Ask:** "What test would pass if this worked?"

### <a id="t9"></a>T9. A bug you cannot reproduce is a rumor

You cannot fix a rumor. You can only change something and then fail to observe the symptom — which
feels exactly like fixing it, and is the most common way a bug gets "fixed" twice.

**Reproduction converts an anecdote into an object** you can hold still, take apart, and verify you
have changed. So the first move on any bug report is not a hypothesis; it is a reproduction, ideally
captured as a failing test.

When it will not reproduce, do not guess-and-patch. Time-box the attempt, add logging that records
the inputs at the point of the suspected decision, tell the reporter what you are waiting to see,
and write the open question in `FINDINGS`. A rumor with better instruments becomes an object the
next time it happens.

Everything that makes reproduction cheap — seeded randomness, faults on demand, one-command reset,
logs that record the inputs to each decision — is an investment in the *next* investigation, not
this one. That is the shape of nearly all good engineering investment.

> **Ask:** "Can I make it happen on purpose?"

### <a id="t10"></a>T10. Let the machine generate the cases you would not think of

Example-based tests check the cases you imagined, which are the ones you were least likely to get
wrong. Three techniques check the rest, and each is cheap to start:

- **Property-based tests** state a rule that must hold for *every* input — "sorting twice equals
  sorting once," "a reading parsed and re-serialized is unchanged," "`available` is never negative"
  — and let a library generate hundreds of inputs, shrinking any failure to the smallest case.
- **Fuzzing** feeds malformed and hostile input to a parser or endpoint until something crashes:
  the *wrong* and *lying* cases of [SE1/R6](04-requirements.md#r6), automated.
- **Mutation testing** makes small changes to the code — flips a `<`, deletes a line — and reports
  every change the suite did *not* catch. It is [SE1/T3](#t3) at scale: it finds the tests that
  cannot fail.

> **Ask:** "What rule must hold for every input — and does a test check it?"

### <a id="t11"></a>T11. When someone else owns "correct," test against their implementation

Some interfaces were defined by someone else: a file format, a wire protocol, a standard. Their
specification is a K4 — it says what its authors meant. What everybody's data actually looks like is
decided by the implementation that owns the format, and that implementation is the only judge whose
verdict matters.

**Differential testing** makes it the oracle. Write with your code and check with theirs; write
with theirs and read with yours; compare. For a file-system library: create an image, run the
platform's own checker on it, then let the platform's tools change it and read it back. Every
disagreement is either your bug or a behavior the specification never mentioned — and the second is
a `FINDINGS` entry, because it is the K2 the document could not tell you
([SE1/U2](02-unknowing.md#u2)).

Use the oracle as a black box: run it, pin its version ([SE1/O2](07-operating.md#o2)), and test
against the versions your users actually have. Do not copy it, and on a clean-room project do not
read its source ([SE1/R8](04-requirements.md#r8)). Fed generated inputs ([SE1/T10](#t10)), it finds
cases neither you nor the specification thought of.

> **Ask:** "Who decides whether this output is correct — and does a test ask them?"


---

Checklists for this chapter and the next are in [CHECKLISTS.md](../CHECKLISTS.md), under *Trusting*.

Next: [7. Operating](07-operating.md) — keeping it repeatable, observable, and safe to change once
it runs.
