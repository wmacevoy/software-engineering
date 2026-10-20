# Checklists

Every checklist in the guide, in the order a project meets them. Each item cites the principle that
explains it; if an item retires no fear on your project, drop it and say why
([SE1/P4](guide/01-purpose.md#p4)).

The "before leaving…" lists are not phase gates for a waterfall. In iterative work each iteration
passes through all of them in small ([SE1/W3](guide/08-work.md#w3)); use them whenever a piece of
work moves from one kind of step to the next.

## Starting

**The first conversation with the client** — see [SE1/H7](guide/09-people.md#h7) for the order and
[SE1/R3](guide/04-requirements.md#r3) for the questions.

- [ ] Pain before solution: what happens today when it goes wrong, and who gets the call?
      ([SE1/R1](guide/04-requirements.md#r1))
- [ ] A census of everyone the system touches, and who is treated differently.
      ([SE1/H7](guide/09-people.md#h7))
- [ ] Numbers with horizons; downtime budget; data about people.
      ([SE1/R7](guide/04-requirements.md#r7), [SE1/R8](guide/04-requirements.md#r8))
- [ ] The assumptions read back as questions. ([SE1/H6](guide/09-people.md#h6))

**Before leaving Requirements for Design**

- [ ] Every requirement is numbered and observable, and the client — or, with no client in the room,
      a named proxy for the users — has objected to at least one.
      ([SE1/R2](guide/04-requirements.md#r2), [SE1/H5](guide/09-people.md#h5))
- [ ] `Scope decisions`, `Non-goals`, `Not yet answered`, and `Deferred` exist and have been read
      aloud. ([SE1/R9](guide/04-requirements.md#r9))
- [ ] The questions with a regulator attached have named answers: what data about people, who may
      see it, what rule applies, and who said so. ([SE1/R8](guide/04-requirements.md#r8))
- [ ] Scale, speed, recovery, and availability have numbers, with horizons and periods — and so do
      resources and interruption, where they apply. ([SE1/R7](guide/04-requirements.md#r7))
- [ ] Every input has an answer for absent, late, wrong, and lying.
      ([SE1/R6](guide/04-requirements.md#r6))
- [ ] A glossary exists. ([SE1/D9](guide/05-design.md#d9))
- [ ] Every "must" is named by a test, or by a `QUEUE` item to write one.
      ([SE1/R11](guide/04-requirements.md#r11))

**Before leaving Design for Develop**

- [ ] Every one-way door is named and got the small-waterfall treatment: reviewed by someone who
      does not share the assumption, and done once. ([SE1/W4](guide/08-work.md#w4),
      [SE1/D11](guide/05-design.md#d11))
- [ ] The contract between the pieces is written and checked in. ([SE1/W5](guide/08-work.md#w5))
- [ ] Every mock misbehaves on request, and the mock and the real thing answer to one check.
      ([SE1/T6](guide/06-testing.md#t6))
- [ ] Every copy of state has an owner and a stated staleness. ([SE1/D2](guide/05-design.md#d2),
      [SE1/D6](guide/05-design.md#d6))
- [ ] The essential complexity fits on one page. ([SE1/D8](guide/05-design.md#d8))
- [ ] Nothing in the design changes a requirement. If it does, that is a conversation, not an edit.
      ([SE1/R5](guide/04-requirements.md#r5))

## Working

**Before splitting work between people (or agents)**

- [ ] The seam is named.
- [ ] Its shape is written: schema, signature, error codes, and what happens when the other side is
      absent, late, wrong, or lying.
- [ ] A mock exists that misbehaves on request.
- [ ] A test exists that fails today.
- [ ] Both sides can start tomorrow without talking. ([SE1/H4](guide/09-people.md#h4))

**Definition of done, for every change** ([SE1/W11](guide/08-work.md#w11), which has the reasons;
keep the two in step)

- [ ] It satisfies a stated requirement, and the change names its versioned ID (`REQ2/UI-1`) — or it
      is labeled a chore.
- [ ] A test names that same ID and has been seen to fail without the change.
- [ ] It builds and runs from a clean checkout.
- [ ] The full check suite passes locally.
- [ ] Anything it made untrue in the requirements, design, or repository guide is updated in the
      same change.
- [ ] New behavior that can fail has a way to make it fail on demand.
- [ ] It is one concern, and the description says what was deliberately left out.
- [ ] Someone other than the author reviewed it. For an agent-drafted change, the human who reads
      all of it and signs counts; a one-way door deserves a second human.
- [ ] It is signed by a person who has read all of it.

**Handing a task to an agent** ([SE1/A3](guide/10-agents.md#a3)–[SE1/A7](guide/10-agents.md#a7),
[SE1/A10](guide/10-agents.md#a10))

- [ ] The task is a done sentence with a versioned requirement ID.
- [ ] The relevant constraints are in the repository, not only in your head or the chat.
- [ ] The agent can run the system and the checks, and reset it.
- [ ] You asked for the smallest diff, one concern, named files.
- [ ] You read the whole diff and ran it yourself before signing.
- [ ] You asked the retro questions and wrote the answers into the repository.

## Iterating

**Every iteration** ([SE1/W9](guide/08-work.md#w9)) — the four outputs, then two habits:

- [ ] A running thing, from a clean reset.
- [ ] The requirements diffed, if anything changed, including `Non-goals`.
- [ ] A `FINDINGS` entry.
- [ ] A priced `QUEUE` with a *done* sentence per item.
- [ ] *Habit:* roles rotated; the hand-off surfaced what was in one head.
      ([SE1/H3](guide/09-people.md#h3))
- [ ] *Habit:* something deleted, or a sentence about why nothing was.
      ([SE1/D12](guide/05-design.md#d12))

**Every demo** ([SE1/H8](guide/09-people.md#h8))

- [ ] Real system, client drives, thirty minutes.
- [ ] Every "huh" written down verbatim; none answered in the room.
- [ ] A fault set in front of them.
- [ ] `Non-goals` read aloud.
- [ ] The assumptions read back as questions.

**When a surprise arrives** — a new requirement nobody mentioned (K2), or an assumption found to be
wrong (K3) ([SE1/H9](guide/09-people.md#h9), [SE1/H12](guide/09-people.md#h12), and the
[case study](guide/09-people.md#case-study-it-does-the-vip-spaces-too-right))

- [ ] Named in the room; no yes, no no.
- [ ] Costed against assumptions, not code — a table, with the whole team.
- [ ] Priced options with a recommendation, within the week.
- [ ] Requirements versioned, not edited.
- [ ] A `FINDINGS` entry naming the question that would have found it.
- [ ] That question added to the intake list.
- [ ] Re-planned with slack; nobody added.

## Trusting

**Before trusting a test suite** ([SE1/T5](guide/06-testing.md#t5),
[SE1/T3](guide/06-testing.md#t3))

- [ ] Every test owns its state, or owns a unique shard of it.
- [ ] The suite passes in any order and in parallel. Try it.
- [ ] No wall clock, no unseeded randomness, no fixed port.
- [ ] Every test has been seen red.
- [ ] Every instrument — sanitizer, coverage, linter, warning flag — has been seen to fire on the
      code it claims to cover, or a check proves it is engaged.
- [ ] CI runs the command you run, on every platform you ship to.
      ([SE1/O3](guide/07-operating.md#o3))

**Before trusting an environment** ([SE1/O1](guide/07-operating.md#o1),
[SE1/O2](guide/07-operating.md#o2))

- [ ] The manifest names the major and minor; the lock names the exact version; both are committed.
- [ ] The install refuses to run when the lock and manifest disagree.
- [ ] The base image is pinned by digest (or its floating tag is a written-down choice); the
      architectures you ship to are written down and tested.
- [ ] Updating dependencies is somebody's named job, and the suite runs after it.
- [ ] One command returns everything to a known state. ([SE1/T5](guide/06-testing.md#t5))

**Before trusting a deploy** ([SE1/T2](guide/06-testing.md#t2), [SE1/O6](guide/07-operating.md#o6))

- [ ] A power-on self test: a missing precondition is an exit code.
- [ ] A health check with a timeout, and an automatic revert when it is not met.
- [ ] The rollback has been run, and timed.
- [ ] The deploy script is the one you run by hand.
- [ ] Maintenance is a state, not a fault. ([SE1/O4](guide/07-operating.md#o4))
- [ ] The previous version can still run against the data after this deploy.
      ([SE1/O7](guide/07-operating.md#o7))

**Before trusting production** ([SE1/O4](guide/07-operating.md#o4),
[SE1/O5](guide/07-operating.md#o5), [SE1/O8](guide/07-operating.md#o8),
[SE1/O10](guide/07-operating.md#o10))

- [ ] Every alert fires on a symptom users feel, names a runbook, and has been seen to fire.
- [ ] Logs record the inputs to decisions, and contain no secrets or personal data.
- [ ] Every remote call has a timeout; retries are bounded, spaced, and only on idempotent
      operations.
- [ ] Each dependency has a stated fallback: fail fast, serve stale with its age, or show unknown.
- [ ] Secrets are injected at run time; every endpoint checks its own authorization.
- [ ] It has been load-tested at the peak the requirements promise, on data of the size you will
      have.

**Before changing a schema or an interface** ([SE1/O7](guide/07-operating.md#o7),
[SE1/D11](guide/05-design.md#d11))

- [ ] The change is expand-then-contract: old and new shapes coexist until every reader has moved.
- [ ] Readers ignore unknown fields and default missing ones; no existing field changes meaning.
- [ ] The migration and its rollback have been run, timed, on production-sized data.

**During and after an incident** ([SE1/O9](guide/07-operating.md#o9))

- [ ] Service restored first: rollback, failover, flag off, or stale-with-age.
- [ ] One lead, one communicator, status on a schedule.
- [ ] A blameless write-up in `FINDINGS`: detection, timeline, what would have caught it sooner.
- [ ] A test, alert, runbook, or checklist changed so nobody pays again.
