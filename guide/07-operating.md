# 7. Operating

Software spends most of its life running, not being written. This chapter follows it from the
machines it is built on to the ones it runs on: keeping it repeatable, observable, safe to change,
and recoverable once it is out there — the second half of
"reliable": *it says so when it is broken, and someone can fix it* ([SE1/P2](01-purpose.md#p2)).

## If you have never deployed anything

Suppose you put your class project on a server so other people can use it. Here is the vocabulary
of what happens next, in the order you will meet it:

- **Container and image.** Instead of installing your app by hand on the server, you describe its
  whole environment — operating system, language runtime, libraries — in a file. Building that file
  gives an **image**; running an image gives a **container**. The same image runs the same way on
  your laptop and on the server, almost ([SE1/O1](#o1)).
- **Dependencies and the lock.** Your app uses libraries, which use other libraries (**transitive**
  dependencies). A **lock file** records the exact version of every one, so every install gets the
  same code ([SE1/O2](#o2)).
- **CI workflow.** A script a service such as GitHub Actions runs on every push: build, test, and
  report pass or fail ([SE1/O3](#o3)).
- **Staging and production.** *Production* is the copy real users use. *Staging* is a copy set up
  the same way, where you try a release first.
- **Health check.** An endpoint like `/health` that answers "I'm working" only if the app really is
  ([SE1/O4](#o4) splits this into two checks). A deploy is **health-gated** when it is not
  considered finished until the health check passes ([SE1/O6](#o6)).
- **Rollback.** Putting the previous version back when the new one fails. When the system does it
  by itself because the health check failed, that is an *automatic revert*.
- **Logs, metrics, alerts.** Logs are lines the app writes about what it did; metrics are numbers it
  counts (requests, errors, response times); an **alert** is a rule that notifies — **pages** — a
  person when a metric looks wrong ([SE1/O4](#o4)).
- **Incident and runbook.** An *incident* is any time users are being hurt by a failure right now.
  A *runbook* is the written, step-by-step procedure for a known problem — "the database is full: do
  this" ([SE1/O9](#o9)).
- **Feature flag.** A setting that turns a feature on or off without a new deploy, so new code can
  ship switched off and be switched off again if it misbehaves.

At class-project scale most of this is a sentence each: a lock file committed, one CI workflow, a
`/health` endpoint, a note saying how to put the previous version back, and logs you have actually
read. The principles below are what those sentences grow into.

If what you ship is a library, firmware, or a file format rather than a service you run, the deploys
and rollbacks below belong to someone else; [SE1/O11](#o11) says what replaces them.

---

### <a id="o1"></a>O1. Repeatability is also a property of the environment

Same code, same tests, different machine. The question is whether the software *around* the code is
the same.

**A container makes the software identical and the machine similar.** An image tag is a family, not
a file: the same tag pulls an `arm64` build on an Apple-silicon laptop and an `amd64` build on a
typical CI runner. Native modules are compiled per architecture; some packages fall back to
emulation; numerical libraries differ; timing differs. Three honest choices: pin one platform and
emulate elsewhere; build and test on both; or accept *almost* and write down where it is
load-bearing. Not knowing which you chose is the only wrong answer.

**An image is only as repeatable as its inputs.** A tag like `node:20` floats to whatever is newest
at pull time; a digest (`node:20@sha256:…`) pins it — and only a per-platform digest names exact
bytes, since a multi-platform digest still resolves to a different image on each architecture. A
package install without a lock file resolves at build time — so two builds a week apart can contain
different library versions, and nothing records which.

**When a container is the wrong tool**, a package manager that understands platforms (`conda`,
`pixi`) describes the environment as constraints and records one exact resolution *per platform* in
a lock. A container reproduces one machine; a lock reproduces the same resolution decision on
every machine, with an answer recorded for each kind of machine.

| Condition                        | Why a container fails                                   | Example                     |
| -------------------------------- | ------------------------------------------------------- | --------------------------- |
| dependencies differ by hardware  | an image pins one answer; GPU passthrough is limited    | CUDA vs. Metal vs. CPU      |
| the toolchain is huge            | multi-gigabyte images, painful to rebuild and ship      | mobile SDKs                 |
| it has a real user interface     | forwarded windows are a poor substitute                 | IDEs, notebooks with plots  |
| it needs host resources          | devices and licences do not cross the boundary          | serial ports, cameras       |

If nothing varies across your users' machines, the container gives the stronger guarantee.

> **Ask:** "Which architecture did CI actually run on — and what did the build resolve?"

### <a id="o2"></a>O2. In the manifest, say what you are compatible with; in the lock, record what you ran; commit both

```
manifest — a promise about compatibility      lock — a record of one resolution
express    ^4.19        (>=4.19, <5)           express  4.19.2   sha512-…
torch      >=2.3,<3                            torch    2.3.1    <build hash>
```

Semantic versioning is the interface between you and a library's authors: the **major** changes when
something breaks, the **minor** when something is added, the **patch** when something is fixed. The
manifest names the major (the promise you depend on) and the minor (the floor of features you use);
the lock pins the exact patch and a hash, so everyone installs the same bytes and CI resolves what
you tested. (Below `1.0`, most tools treat the minor as breaking — `^0.4` means `<0.5` — so read
your tool's rules before trusting a range.)

| Policy in the manifest                        | Repeatable?      | When a vulnerability is published in a dependency (a CVE)          |
| --------------------------------------------- | ---------------- | ------------------------------------------------------------------ |
| nothing pinned (`*`, `latest`)                | no               | you already have the fix — and every breaking change, in production |
| every direct dependency pinned exactly, no lock | partly — the libraries *those* use still float | someone edits pins; without a bot doing it, this tends to be *never* |
| **major.minor in manifest, exact in lock**    | yes, by the lock | update, run the suite, commit the new lock — usually **hours**, not weeks |

The balance is **repeatability against survivability.** Pin everything and never update, and the
build stays the same while the software dies of neglect. Two practices keep updates cheap, whichever
policy you use:

- **The update is followed by the suite.** *The quality of your tests sets the price of every
  security fix you will ever take.* A team with a suite it trusts merges the update the day it
  appears; a transitive dependency that breaks is found by the suite, not by users.
- **The update is scheduled** — a bot (Dependabot, Renovate) or a named person's weekly job. A lock
  that is never regenerated is a hand pin with extra steps.

When a CVE is already open: check whether the vulnerable code is reachable from yours, take the fix
now if it is, and record in `FINDINGS` how long it sat — that delay is the real finding.

Install with the command that refuses drift: `npm ci`, `cargo build --locked`, `pixi install
--locked`.

> **Ask:** "What does a CVE in a dependency cost us, in hours?"

### <a id="o3"></a>O3. CI runs the command you run, everywhere you ship — and enforces what matters

Continuous integration is the idiot light with a URL ([SE1/T2](06-testing.md#t2)). It retires "it
works on my machine" and "we only ever built it on one kind of machine." Two rules make it worth
trusting:

- **CI runs the same command you do.** If the workflow's step is `./check.sh` and so is yours, there
  is no second recipe to drift.
- **The gate is in the script, not only in the workflow.** A script that runs the tests and stops on
  failure cannot produce artifacts locally that CI would have rejected.

**Build there, and run there.** Compiling for a platform and running on it are different claims; a
cross-compiler can make only the first. If you ship to two architectures or three operating systems,
test on each, with fail-fast off — when it breaks, the interesting question is *which* platforms
broke.

**A convention CI does not enforce is not a policy.** If a rule matters — formatting, the type
check, signed commits, the dependency rule, conformance — a check enforces it, so review can spend
its attention on what no tool can see ([SE1/F3](03-feedback.md#f3), [SE1/W11](08-work.md#w11)).

> **Ask:** "Is CI running the command I run, on the machines I ship to?"

### <a id="o4"></a>O4. Every failure needs a signal a person will see — and believe

The second half of reliability is detectable error status. In production that means:

- **Logs that explain decisions**, not just events: *"marked lot 3 stale: age 47 s exceeded 15 s"*,
  with the inputs that produced it ([SE1/D6](05-design.md#d6)). Structured (key–value), so they can
  be searched. **Never log secrets or personal data** — logs are copied, shipped, and kept far
  longer than the system they came from.
- **Metrics for the questions you will ask at 3am**: request rate, error rate, latency percentiles,
  saturation (queue depth, pool usage, disk). Sized from the numbers in the requirements
  ([SE1/R7](04-requirements.md#r7)).
- **Alerts on symptoms users feel** — the page is failing, the counts are stale — rather than on
  every cause. Each alert names its runbook ([SE1/O9](#o9)).
- **Status that can be trusted.** Two health checks, not one: *liveness* ("this process is running;
  restart me if not") checks only the process itself, while *readiness* ("I can serve requests right
  now") also checks what it depends on. Mixing them up makes a shared database outage restart every
  server at once. Beyond health, a derived state per component (`live`, `stale`, `unreachable`) says
  more than a single green light.

An alarm that fires when nothing is wrong is not a cautious alarm; it is a broken one, and its
brokenness is invisible until the night it was needed ([SE1/T4](06-testing.md#t4)). So:

- an injected fault is *tagged* as injected, so it can drive the alert you are testing without
  being counted as a real error or filling the error log;
- scheduled maintenance is a *state*, not a fault — a dashboard that goes red every night during the
  2am backup teaches its operators to ignore red;
- steady-state success is sampled or logged at low severity, so the transitions stand out.

Alerts and dashboards are code: test them by injecting the fault they are meant to catch and
watching them fire.

> **Ask:** "If this broke at 3am, what would tell us — and would anyone believe it?"

### <a id="o5"></a>O5. Handle failure on purpose: timeouts, bounded retries, and a stated fallback

Every call across a network needs a stated answer for absent, late, wrong, and lying
([SE1/R6](04-requirements.md#r6)). In code, that means:

- **Every remote call has an explicit timeout**, shorter than the caller's own deadline. A missing
  timeout is a decision to wait forever, made by nobody.
- **Retries are bounded, spaced, and safe.** Retry only operations that are idempotent or carry an
  idempotency key ([SE1/D4](05-design.md#d4)); back off exponentially with random jitter so a
  thousand callers do not retry in lockstep; cap the total number of retries, so a struggling
  dependency is not finished off by its callers. Retry at one layer only: three attempts at each of
  three layers is twenty-seven calls for one user click.
- **Stop calling what is clearly down.** A *circuit breaker* counts recent failures to a dependency
  and, past a threshold, fails immediately for a while instead of waiting on timeouts — then lets
  one trial request through to see whether it has recovered.
- **Choose fail-fast or degrade, per dependency, and say which.** Refuse, serve the last good value
  *with its age*, or show *unknown* — and the user can tell which happened.
- **Protect yourself from overload.** Bound queues and pools; when full, shed load early rather than
  slowly failing everyone (backpressure).
- **Never swallow an error.** Handle it, or pass it up with context. Degrading on purpose is
  handling it — when the fallback is chosen, recorded, and visible to the user. A `catch` that logs
  and carries on as if nothing happened is a decision to serve wrong answers quietly.

> **Ask:** "What does this call do when the other side is slow — and how many times will we retry?"

### <a id="o6"></a>O6. A deploy is a test whose failure is an outage

**A deploy is not finished when the bits land; it is finished when the thing reports healthy — and
the system should be the one to notice.** Health-gated, with automatic revert, with the rollback
timed *before* the maintenance window opens.

Concretely: a staging environment from the same definition as production; the health endpoint polled
with a timeout as the power-on self test ([SE1/T2](06-testing.md#t2)); the integration suite run
against it; promotion only on green. The deploy script is the one you run by hand.

Automatic revert only works if the old code can run against the new data. A schema change that the
previous version cannot read makes revert impossible — which is why data and interfaces change in
steps ([SE1/O7](#o7)).

> **Ask:** "Has the rollback been run, and how long did it take?"

### <a id="o7"></a>O7. Change data and interfaces in steps that can each be undone

The outages that hurt most come from changing a shape that something else depends on — a schema, an
API, a message format — in one move. During any deploy, old and new versions run at the same time;
for a fleet of devices or a set of browsers with cached pages, that mixed state is the normal
condition, not a moment. So:

- **Expand, then contract.** Add the new column or field alongside the old; deploy code that writes
  both and reads either; backfill; switch readers to the new; only then stop writing the old, and
  later remove it. Every step can be rolled back on its own.
- **Code that reads data must tolerate what it did not write**: ignore unknown fields, give missing
  ones a default, and never change what an existing field *means* ([SE1/D11](05-design.md#d11)).
- **Deprecate on a schedule.** Announce, measure who still uses the old shape, and remove it only
  when that number is zero or the date agreed has passed.
- **Size migrations against the data.** A migration that scans a table of hundreds of millions of
  rows may not fit in any window you have ([SE1/D12](05-design.md#d12)); measure it on a copy first.
- **Rehearse.** Run the migration and its rollback on a copy of production-sized data, timed.

> **Ask:** "Can the previous version still run against the data after this change?"

### <a id="o8"></a>O8. Secure by default

The threat model says who the adversary is ([SE1/R8](04-requirements.md#r8)); these defaults make
the common attacks expensive before anyone has to be clever:

- **Least privilege.** Each component, key, and account gets only the access its job needs. An
  administrator's login is not the key that signs releases ([SE1/D13](05-design.md#d13)).
- **Secrets never live in the repository, in prompts, or in logs.** Inject them at run time from a
  secret store; refer to them by name, never by value. A leaked secret is rotated, not deleted.
- **Authorize every request, on the server.** Hiding a button in the UI is presentation, not
  security; every endpoint checks its own permissions.
- **Treat every input as possibly lying** ([SE1/R6](04-requirements.md#r6)). Validate at the
  boundary; use parameterized queries and proper escaping, never string-built SQL or HTML.
- **No insecure fallbacks.** A missing secret or certificate is an exit code, not a default
  ([SE1/T2](06-testing.md#t2)).
- **Dependencies are trust** ([SE1/O2](#o2)). Prefer few, maintained ones; know which you have;
  update them on a schedule.
- **Demonstrate the attacks in your threat model** before trusting the defense
  ([SE1/T8](06-testing.md#t8)).

> **Ask:** "What can an attacker reach from here, and have we tried?"

### <a id="o9"></a>O9. In an incident, restore service first; learn afterward

- **Mitigate before diagnosing.** Roll back, fail over, turn the feature flag off, serve stale with
  its age. Understanding can wait until users are not paying for it.
- **One person leads**, one person communicates, and everyone else works on what the lead asks.
  Status goes out on a schedule, even when the news is "no news."
- **Runbooks are real only if someone has run them** — the restore, the failover, the rollback —
  timed, recently, on a copy ([SE1/R7](04-requirements.md#r7)).
- **Afterward, write it up without blame** ([SE1/H12](09-people.md#h12)): what happened, how it was
  detected, how long each phase took, what would have caught it sooner — and change a test, an
  alert, a runbook, or a checklist so nobody pays again. The write-up goes in `FINDINGS`.

> **Ask:** "What is the fastest way to stop the harm — and who is leading?"

### <a id="o10"></a>O10. Measure before you optimize; test at the scale you promised

Do not optimize what is not slow: measure first — with a profiler, which shows where the time
actually goes — and note where it would matter. Judge speed by percentiles (the 95th or 99th), not
averages: the average hides the slowest requests, and those are the ones users remember. But *do*
test at the numbers the requirements state ([SE1/R7](04-requirements.md#r7)) — a load test at the
event-peak rate, with production-sized data — because performance and capacity are requirements, and
a requirement nobody has tested is a hope. Run the load test again when the data grows, not only
when the code changes.

> **Ask:** "Have we run it at the peak we promised, against data the size we will have?"

### <a id="o11"></a>O11. A release you cannot roll back is a one-way door; ship it like one

Most of this chapter assumes a service you run: you deploy it, watch it, and put the previous
version back. A library, firmware, an installed app, or a file format has none of that. The deploy
is someone else's, months later, on hardware you will never see — and what it writes, such as bytes
on a user's card, stays written after you fix the bug. [SE1/O6](#o6)'s health gate and
[SE1/O7](#o7)'s rollback have nothing to pull. What replaces them:

- **Every release is a one-way door** ([SE1/D11](05-design.md#d11)): reviewed by someone who does
  not share the assumption, a release checklist run every time, and a version number that tells
  integrators what changed.
- **Refuse rather than guess.** Every feature an input can announce has a stated answer — refuse,
  read-only, or read-write ([SE1/R6](04-requirements.md#r6)) — and one you have never heard of gets
  refuse, or read-only if reading provably changes nothing.
- **Conformance to a format you don't own** is tested against the implementation that owns it
  ([SE1/T11](06-testing.md#t11)).
- **The device is part of the envelope**: code size, memory, stack, energy, and power lost at any
  instant ([SE1/R7](04-requirements.md#r7)). On a device, a cut mid-write is a normal event, not an
  incident, and a test makes it happen.
- **The signal comes back late, through other people**: bug reports, crash dumps, a downstream
  project's CI. Make them easy to send and cheap to reproduce ([SE1/T9](06-testing.md#t9)); they are
  your monitoring ([SE1/O4](#o4)).

> **Ask:** "If this release is wrong, what will already be written that we cannot take back?"

---

Next: [8. Work](08-work.md) — the shape of the work, and what time does to it.
