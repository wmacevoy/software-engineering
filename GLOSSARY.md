# Glossary

The terms this guide uses precisely. One thing, one word ([SE1/D9](guide/05-design.md#d9)): if you
find the guide using one of these loosely, that is a bug.

| Term                    | Meaning                                                                                              |
| ----------------------- | ---------------------------------------------------------------------------------------------------- |
| **K0**                  | Known, and true.                                                                                     |
| **K1**                  | A known unknown. Cheap: you can go find out.                                                         |
| **K2**                  | An unknown unknown. Only reality tells you; you can arrange to be told sooner.                       |
| **K3**                  | Erroneous certainty: feels like K0, is false. Triggers no search, so it is found last.               |
| **K3 factory**          | Anything that keeps saying "fine" with no way to say "wrong" — and so keeps producing K3s ([SE1/U7](guide/02-unknowing.md#u7)). |
| **K4**                  | A chosen falsehood: held on purpose because it is useful, with a note on where it is load-bearing.   |
| **Absent, late, wrong, lying** | The four failure cases every input needs a stated answer for.                                  |
| **Accidental complexity** | Complexity from how you chose to build it; it must justify its carry.                             |
| **Agent** | An AI system that reads a repository, edits files, and runs commands on a person's behalf — a coding assistant acting with some autonomy. |
| **Backfill** | Filling a newly added column or field for rows written before it existed. |
| **Backpressure** | Refusing or slowing new work when queues are full, so overload is shed early instead of failing everyone slowly. |
| **Blast radius** | Everything that breaks when an assumption stops being true. |
| **Bus factor** | How many people would have to vanish before the project stalls. One is the dangerous number. |
| **Cache**               | Any copy of state that might not match the original — whether or not anyone installed it as a cache. |
| **Carry**               | Everything paid for as long as code exists: reading, review, upgrades, security surface, onboarding. |
| **Chore** | A change that serves no requirement — a typo, a dependency update, a pure refactor — labeled as such. |
| **Circuit breaker** | A wrapper that, after repeated failures to a dependency, fails fast for a while instead of waiting, then probes for recovery. |
| **Comes due** | Said of a K4: the moment the world stops matching the useful falsehood. |
| **Conformance test** | A test suite any implementation of an interface must pass, run from outside without reading its source. |
| **Container / image** | An image is a built, self-contained description of an app's environment; a container is a running copy of one. |
| **Contract**            | What one part promises another, written down: what it accepts, what it returns, and how it fails.    |
| **Control plane** | A side channel — such as a test-only endpoint — that tells a component how to behave: slow, down, stuck, wrong. |
| **CVE** | A published security vulnerability, with an ID, in a specific version of some software. |
| **Design**              | The mechanism chosen to satisfy the requirements, and what was rejected. Changes with the team.      |
| **Differential testing** | Checking your implementation against another one that owns the definition of correct, by running both on the same inputs ([SE1/T11](guide/06-testing.md#t11)). |
| **Digest** | A content hash that names an exact image (per platform) rather than a tag that can move. |
| **Essential complexity**  | Complexity in the problem; it survives every rewrite.                                              |
| **Expand / contract** | Changing a shape in steps: add the new beside the old, move every reader, then remove the old. |
| **Feature flag** | A setting that turns a feature on or off without a new deploy. |
| **Fence**               | A checkpoint that proves something: a demo, a check that exits nonzero, a deploy. A meeting is not one. |
| **Health check** | An endpoint that reports whether the app is working; split into *liveness* and *readiness* (below). A deploy is *health-gated* when it waits for it. |
| **Idempotency key** | A unique value a caller attaches to a request so that sending it twice has the effect of sending it once. |
| **Idempotent**          | Doing it twice equals doing it once.                                                                 |
| **Idiot light**         | One pass/fail signal visible from across the room.                                                   |
| **Incident** | A time when users are being hurt by a failure right now. |
| **Inferred** | Said of a requirement or a reason reconstructed from code or history rather than stated by a person; marked *(inferred)* until someone confirms it ([SE1/W12](guide/08-work.md#w12)). |
| **Injected clock** | The current time passed in as an argument, so a test can choose it, instead of read from the system. |
| **Instrument** | Anything that measures: a clock, a feedback loop, a log, a sanitizer, a coverage report, a linter. Trusted only once seen to fire ([SE1/T3](guide/06-testing.md#t3)). |
| **Interface** | The surface one part shows another — signatures, schemas, endpoints. Its written promises are the **contract**; an **API** is an interface offered over a network or to other programs. |
| **Jitter** | Random variation added to retry delays so many callers do not retry at the same instant. |
| **Liveness / readiness** | "The process is running" (restart me if not) / "I can serve requests now" (send me traffic if so). |
| **Load-bearing** | Said of an assumption: something important depends on it being true. |
| **Local / sharded / global state** | Created and destroyed by one test / partitioned so each test owns a slice / shared by everyone. |
| **Manifest / lock**     | What you are compatible with / what you actually resolved and ran.                                   |
| **Mock** | A stand-in for a real component, used so its consumer can be built and tested first. A good one misbehaves on request. (Also called a fake or stand-in; this guide says mock.) |
| **Monotonic clock**     | A clock that only moves forward and does not jump when the wall clock is corrected.                  |
| **Observable**          | Checkable from outside, without reading the source.                                                  |
| **One-way door**        | A decision that cannot be cheaply undone: a schema with data under it, a published interface, a distributed key, data collected about people. |
| **Page (verb)** | To notify an on-call person urgently, by phone or pager, because an alert fired. |
| **Power-on self test**  | Refusing to start when a precondition is missing.                                                    |
| **Principle ID** | A versioned citation of one principle in this guide: `SE1/T3` is principle 3 of *Testing* in the first major version. Within a major version an ID never moves ([principle index](README.md#principle-index)). |
| **Production / staging** | The copy real users use / a copy set up the same way, for trying a release first. |
| **Provenance**          | Who made a claim, and how to check it later without asking them again.                               |
| **Reliable**            | Works when in good repair and used correctly, and has detectable error status when broken or misused. |
| **Repository guide** | The file that says how to build, run, test, and reset this repository, and its local rules — `CONTRIBUTING.md`, `CLAUDE.md`, or equivalent ([SE1/W10](guide/08-work.md#w10)). Not `AGENTS.md`, which it overrides. |
| **Requirement**         | A numbered, observable statement of what must be true. Changes only with the client. Cited with the version that last changed it: `REQ2/UI-1` ([SE1/R10](guide/04-requirements.md#r10)). |
| **Roles** | Architect (holds the design), Liaison (one voice to the client), Planner (holds the queue), Toolsmith (holds tests, CI, and the reset). See SE1/H3. |
| **Rollback** | Putting the previous version back. Done by the system itself on a failed health check, it is an *automatic revert*. |
| **Runbook** | A written, step-by-step procedure for a known problem, which someone has actually run. |
| **Seam** | The point where two parts — or two people's work — meet, and where the contract between them lives. |
| **Serve / rule**        | From embedded testing: code that answers questions from values (serve), versus the few lines that command the world — I/O, clocks, globals (rule). See SE1/D7. |
| **Signature (digital)** | A value computed from a message with a private key; anyone with the public key can check who sent it and that it was not altered. It proves origin, not truth. |
| **Small waterfall**     | Careful, front-loaded work — exact requirement, design on paper, independent review, done once — run around a one-way door inside an otherwise iterative process. |
| **Spike**               | A time-boxed investigation of one question, whose code is thrown away. A descent on purpose.        |
| **Symptom alert** | An alert on what users experience — errors, latency, stale data — rather than on an internal cause. |
| **Technical debt**      | Carry taken on knowingly, to be repaid.                                                              |
| **Thin vertical slice** | A narrow path through every layer, end to end, built first and then widened.                         |
| **Transitive dependency** | A library your libraries depend on — code you ship but never chose directly. |
| **Working set**         | `REQUIREMENTS_vX`, `DESIGN_vX`, `QUEUE`, `FINDINGS` — in the repository, versioned with the code.    |
