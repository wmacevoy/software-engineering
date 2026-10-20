# 5. Design

What software is made of, why it costs what it costs, and the handful of ideas that make a hundred
smaller rules stop being arbitrary.

---

### <a id="d1"></a>D1. State is the material

Every discipline has a material whose properties explain its rules. Software's material is not
code; code is the description. What actually runs is **state, plus the rules that change it.**

A pure function — inputs in, value out — is easy in a way you may not have noticed. Call it again,
get the same answer; write down an input and an expected output, and that test is true forever.
State has four properties, and each takes something away:

- **It persists.** It outlives the code that wrote it, so new code meets data written by old code
  that you cannot re-run. That is the whole migration problem.
- **It is shared.** Two parties read the same value and can disagree about what it is right now.
- **It ages.** A value true when read may be false when used. The type system knows nothing about
  freshness.
- **It changes while being observed.** Two writers, one value, no agreed order.

> **The difficulty of a system is not how many features it has. It is how much state a change can
> reach.** That is what "coupling" actually means.

Make a list of every piece of state in your system: who owns it, who else has a copy, how stale a
copy may be, and what a user sees while it is wrong. Twenty minutes, and roughly none of it is
visible in a class diagram. Then notice which components hold no state at all — those are the ones
that will stay easy.

> **Ask:** "How much state can this change reach?"

### <a id="d2"></a>D2. Anything that might be out of date is a cache

A cache is not something you install. It is **any copy of state that might not match the original**
— a variable holding something fetched five minutes ago, an array a timer refreshes, a count column
that duplicates what could be counted from other rows, a login token. Call it a cache and you
inherit the right questions: *how stale can it get, how would you know, and what happens to the user
while it is wrong?*

The same decision, made twice in opposite directions:

- **A signed login token carrying the user's role is a cache** with an eight-hour lifetime and no
  invalidation. Demote someone and they keep their old permissions until it expires. Described as
  "authentication," that is a quirk. Described accurately, it tells you exactly what can go wrong.
- **A device registry re-read on every poll** is a copy at most one poll old, chosen on purpose, so
  that revoking a compromised device takes effect within one poll — with nothing to invalidate.

Neither is universally right. Being able to say which one you chose, and what it costs, is the
skill. And how stale a permission may be is a requirement, not an implementation detail: ask the
client how long a demoted user may keep their old access. If the answer is "not at all," shorten the
token's lifetime, re-check the user's role on sensitive actions, or keep a revocation list the
server consults — each is a different price for the same answer.

> **Ask:** "What is this a copy of, and how stale can it get?"

### <a id="d3"></a>D3. There is no single "now"

Once state lives in two places joined by a network, there is no shared present. The sensor knows a
count; the collector knows what the sensor said four seconds ago; the browser knows what the server
said three seconds before that. All three are locally correct, and they disagree.

Keeping every copy exactly in sync is possible only at a steep price — every read waits on
coordination, and when the network between the copies breaks, the system must either stop
answering or risk answering differently in two places. So for most data the design
question is not "keep them in sync." It is:

> **How wrong may each copy be, and who gets told?**

Freshness and correctness are different properties: at peak arrival, a count that is fresh by the
clock can already be wrong by a dozen spaces.

Beliefs that feel like K0 and are K3:

| The belief                                    | Reality                                                          |
| --------------------------------------------- | ---------------------------------------------------------------- |
| The message arrives                           | It may not. Every call needs an explicit timeout.                |
| It arrives once                               | A retry means it may arrive twice.                               |
| It arrives in order                           | Two paths, two latencies, no guarantee.                          |
| The clock is right                            | A skewed clock produces plausible data with a valid signature.   |
| The write succeeded because the call returned | The response may be what got lost.                               |

> **Ask:** "How wrong may this copy be, and who finds out when it is?"

### <a id="d4"></a>D4. Make operations idempotent

The defense against "it may arrive twice" is a design technique, not a warning: make doing it twice
equal doing it once, and "did that go through?" stops being a question you have to answer.

*"Set available to 37"* is idempotent. *"One car arrived"* is not. Where an operation is inherently
not idempotent — *hold one space* — the request carries a key generated by the caller, and the same
key twice is the same hold once.

Idempotence handles duplicates, not order. If "set to 37" and then "set to 36" can arrive reversed,
carry a sequence number or version with each message and ignore anything older than what you have.

> **Ask:** "What happens if this request is sent twice?"

### <a id="d5"></a>D5. Wall-clock time and elapsed time are different instruments

Split *"how old is this?"* into two fields:

- **Wall-clock time** — when the value was taken. Meaningful across machines, and a lie whenever the
  clock is wrong.
- **Elapsed time from a monotonic source** — a counter that only moves forward and does not jump
  when the clock is corrected. Meaningless across machines, and not forgeable by a bad clock.

Compute staleness from elapsed times only: the age the sender reports for its value (measured on its
monotonic clock), plus the time since the receiver got it (measured on the receiver's). A sender
with a fast wall clock then cannot make old data look fresh — and note that the receipt time alone
is not enough, because a frozen sender gets a fresh receipt on every poll. Keep the wall-clock
timestamps too, because **two independent clocks are what make disagreement detectable at all**:
when the wall-clock gap and the elapsed times disagree, the conclusion is that something on the
sender is broken — its clock, or what it reports — not merely that the data is old. Either way, the
reading is not shown as current.

A worked example. A sensor takes a count, and ten seconds later by its own monotonic clock sends it
with `age = 10 s` and a wall-clock timestamp. The collector receives it at 12:00:10 by its own wall
clock and holds it for 5 seconds by its monotonic clock. The value is 10 + 5 = 15 seconds old — no
wall clock involved. The collector expects the timestamp to say about 12:00:00 (receipt minus age).
If it says 12:02:00 instead, the age is still right, and the two-minute gap is how you learn the
sensor's clock is broken.

Wall clocks jump — corrected by time synchronization, adjusted for leap seconds — and local time is
worse: twice a year an hour never happens and an hour happens twice.
Almost every time bug is one instrument used where the other was required.

> **Ask:** "Which clock is this, and what happens when it jumps?"

### <a id="d6"></a>D6. Derive instead of store; name the authority; record why

- **Derive instead of store.** Anything computed cannot go stale. Compute `available` as
  `capacity − occupancy` in one piece of SQL that every query reuses, and never in the browser. One
  place can be wrong instead of five.
- **Say which copy is authoritative.** If a sensor reports a lot's capacity and the database also
  holds it, write down that the database wins and *a mismatch is a fault, not a correction.* Any
  value that exists twice needs this sentence somewhere.
- **Put state's age in the data, not just the label.** An `age_ms` field can be tested; "last
  updated" in the corner of a page cannot.
- **Record what a decision was based on.** *"Marked lot 3 stale: age 47s exceeded threshold 15s,"*
  not *"sensor returned 200."* State that explains itself is state you can debug a week later.

> **Ask:** "Which copy is authoritative — and could this be computed instead of stored?"

### <a id="d7"></a>D7. Serve, don't rule: keep the logic away from the I/O

The phrase comes from embedded testing. Code that **rules** commands the world: it reads the sensor,
the socket, the database, the clock, a global. Code that **serves** answers questions: a pure
function that takes values and returns values. Keep the ruling to a few thin lines at the edges, and
put the logic in functions that serve.

```js
// Rules and serves at once: untestable without a live store and a frozen clock.
function staleLots(store) {
  return store.latest()
    .filter(r => performance.now() - r.receivedMs + r.heldMs > 15000)
    .map(r => r.id);
}

// Split: the logic serves; one thin function rules.
function staleIds(readings, nowMs, thresholdMs) {           // pure — test it with plain arrays
  return readings.filter(r => nowMs - r.receivedMs + r.heldMs > thresholdMs).map(r => r.id);
}
function staleLotsNow(store) {                               // the only line that touches the world
  return staleIds(store.latest(), performance.now(), 15000);
}
```

(`receivedMs` is the receiver's monotonic clock when the reading arrived, and `heldMs` is the age the
sender reported for it: elapsed times only, as [SE1/D5](#d5) requires.)

The split costs essentially nothing at run time — it is the same work, arranged differently — and
the pure half can now be tested against numbers you chose.

- A signature's signing string is a pure function of the message, so the signing test needs no key,
  no device, and no network.
- Clock skew is arithmetic on three numbers a test can choose: when the receiver got the message,
  when the sender's clock says it took the value, and how long the sender says it has held the value
  since. If the sender's clock is right, `(received − taken) − held` is about zero (just the network
  delay); if not, that difference is the skew.
- A component built as a library can be called in-process with a fetch function that lies.
- A layer that holds no state at all has tests that are free.

**The ratio of serve to rule is the testability of a design**, and the diagnostic runs backwards: if
something is hard to test, look for the rule tangled into the serve.

> **Ask:** "What is the rule here, and what could serve?"

### <a id="d8"></a>D8. Separate essential complexity from accidental complexity

**Essential complexity is in the problem.** It survives every rewrite, framework, language, and
model: sensors lie, clocks disagree, networks drop requests, users speak eight languages, devices
cannot all be upgraded at once. You cannot engineer it away; you can only decide where to handle it.

**Accidental complexity is yours.** The build step, the bundler, the ORM, the five layers of
indirection, the config format invented on a Tuesday. Real work, needing maintenance, demanded by
nobody.

> **What requirement would have to disappear for this complexity to go away?**

If you can name one, the complexity is essential, and the conversation is with the client about
whether that requirement is worth its price. If the honest answer is "none," it is accidental, and
it must justify its carrying cost ([SE1/D12](05-design.md#d12)). Most design arguments are
**category disputes conducted as taste disputes** — "this is too complicated" versus "the problem is
complicated" — and the question turns an argument with no end into a question with an answer.

The trap: **accidental complexity you introduced is invisible to you, because you understand it.**
It is charged to strangers, and in about a month, to you. "It's simple once you know how it works"
is not a defense. Everything is.

The best move against accidental complexity is to make it not exist. To sign a message, both sides
must turn it into exactly the same bytes; two JSON encoders can order keys or format numbers
differently, so "sign the JSON" is a genuinely hard problem. Signing an explicit string —
`lot|count|time`, fields in a fixed order — avoids the problem instead of solving it. Likewise, one
cryptographic algorithm for every job is one thing to learn and no parameters to get wrong.

Write your system's essential complexity on one page, five to fifteen lines, each traceable to a
requirement. Anything you maintain that is not on that page should be able to say why it exists.

> **Ask:** "What requirement would have to disappear for this to go away?"

### <a id="d9"></a>D9. Conceptual integrity: one coherent design beats every good idea

People understand systems **by analogy**: learn how one part works, then guess how the next part
works. Coherence is what makes the guess right. Every place the guess fails is something to memorize
instead, and after a few dozen exceptions people stop reasoning and start copying whatever nearby
code seems to work. **A codebase becomes unmaintainable when guessing stops working** — which can
happen at a few thousand lines, long before it is "large."

**It shows up first in vocabulary**, the cheapest thing to get right:

- **One thing, one word.** If the client says "lot," the schema says "facility," and the UI says
  "garage," you have three mental models and a translation layer that lives in one person's head.
- **One word, one thing.** Worse, because silent. If `status` means both *the sensor's assessment of
  itself* and *whether the collector can reach the sensor*, every consumer inherits the confusion.
  (A sensor cannot report that it is offline — if it can answer, it is not offline. Reachability is
  a conclusion the consumer draws, so it gets its own name.)

Keep a glossary of ten to thirty terms at the top of the requirements. Treat a **new noun** as an
event that needs a decision: a new thing, or a second name for a thing we have?

**It shows up second in shape.** One error envelope on every endpoint. Retryability stated
explicitly rather than inferred from a status code. One README per component, all the same shape.
Stable IDs that grep from a test back to the sentence that demanded it. **If everything is uniform,
the one weird thing is a signal. If nothing is uniform, the weird thing is invisible.** An exception
is fine when it is written down with its reason.

**Somebody has to hold it.** Coherence lives *between* the parts, so no amount of careful local work
produces it and no test checks it. One person holds the whole shape, and most of that job is saying
no — especially to good ideas ([SE1/H3](09-people.md#h3)). This is also why agents author and humans
own the structure: each agent session sees a part, and ten locally reasonable designs compose into
something nobody can hold ([SE1/A8](10-agents.md#a8)).

> **Ask:** "Is that the same thing we called something else on Tuesday?"

### <a id="d10"></a>D10. Locality of reasoning: use a part correctly without reading inside it

The usual justification for interfaces is reuse. That reason is weaker than it sounds: reuse is a
bonus when it happens, and code bent to serve two callers that only look alike can end up worse at
both jobs. The real reason is arithmetic about human memory: nobody can hold a large system in their
head, so **correctness has to be establishable in pieces.** Check that A honors its contract,
separately check B, then use them together without re-reading A.

> **The test of an abstraction: can you use it correctly without reading its implementation?**

If you have to look inside to use it right, it is a function call with extra steps, and the boundary
it advertises is a lie — worse than no boundary, because a reader who trusts it is wrong in a way
they had no reason to check.

Abstractions fail the same way every time — something true inside escapes outside:

| Leak     | What it looks like                                                                    |
| -------- | ------------------------------------------------------------------------------------- |
| Failure  | A call whose contract says "returns a number" and whose reality includes a timeout.   |
| Time     | Something that looks like reading a variable and is a network round-trip.             |
| Meaning  | `200 OK` means the request succeeded, not that the data is *current*.                 |
| Trust    | Valid signature, plausible data, clock off by minutes: everything verifies, and the conclusion is wrong. |

**A contract that does not state how it fails has not stated anything**
([SE1/R6](04-requirements.md#r6)).

What locality justifies:

- **A dependency rule, checked mechanically.** For example: number the layers — shared definitions
  at 0, libraries at 1, running services at 2 — and let a folder import only from a lower number. A
  script that fails the build on a violation keeps it true; without one, folder boundaries become
  decoration within a month.
- **A contract that exists before its consumers**, so two people can build both sides without
  talking ([SE1/W5](08-work.md#w5)).
- **Conformance checkable from outside**: anything claiming to be a sensor can be verified against
  the specification without reading its source.
- **Choosing a library over a service on purpose** when a network hop would add a timeout and an
  outage that stops everything.

> **Ask:** "Can I use this without reading inside it — and does its contract say how it fails?"

### <a id="d11"></a>D11. Once someone depends on an interface, it is a promise

Renaming a variable is free to undo. A data format with data in it, a published URL, a distributed
key, an artifact someone installed — those are **one-way doors**, and they get careful, front-loaded
work ([SE1/W4](08-work.md#w4) says how to choose). Most arguments in software are conducted at the
wrong intensity for their reversibility. On a class project the one-way door is usually the
database: renaming a column is free until you have entered real data, and then it is a migration.

**The moment a second party depends on your interface, it stops being a decision and becomes a
promise.** Versioning is the mechanism for keeping the promise while still being allowed to change:
changing the *meaning* of an existing field is breaking even if its type is unchanged, so it needs a
new version or a new name.

> **Ask:** "Is this a one-way door? Who already depends on it?"

### <a id="d12"></a>D12. Software is capital you carry

> **cost = build + (carry × lifetime)**

**Carry** is everything paid for as long as the code exists: every future reader routing around it,
review time, dependency upgrades, security surface, onboarding, and the chance it breaks a neighbor.
None of it appears on a schedule. Most of the money in this industry goes there.

- **"Should we build this?" was never a build-cost question.** An afternoon's feature that lives
  five years is not an afternoon's decision.
- **Every dependency is a permanent obligation** — learned, trusted, audited, updated, forever,
  including the week a security vulnerability is published against it (a CVE). Adding one is a
  proposal, not a decision.
- **Deletion is usually the highest-return work available, and nobody schedules it.** So schedule
  it: at the end of every iteration, ask *what can we delete?*
- **Sunk cost is sunk.** The only live question is what code costs *from here*.
- **Declared carry is fine.** Technical debt is carry you took on knowingly, to be repaid. Unknowing
  carry is not debt; it is just cost. A `Deferred` list makes absence a decision instead of a gap
  ([SE1/R9](04-requirements.md#r9)).

**Data is the heaviest thing you own.** Code can be rewritten in an afternoon; data cannot. Twenty
readings a second is 630 million rows a year — and a migration that scans that table may no longer
fit in any maintenance window you have. The data you accumulate can *remove* future options, not
just make them expensive. Decide what to keep: record state transitions always, sample the
uneventful steady state, and execute retention as a policy.

> **Ask:** "What does this cost us every week for the next two years — and what can we delete?"

### <a id="d13"></a>D13. Provenance: who said this, and can I check it later without asking them again?

Every claim in a system has an author — a reading, a log record, a release artifact, a commit. The
same question applies at every layer. Where the answer must hold up without trusting the network or
the storage, the structure is usually the same: **a registry mapping identities to public keys, with
enrollment and revocation.** A device registry and a list of allowed commit signers are the same
object one layer apart.

(A digital signature is a short value computed from a message with a private key; anyone with the
matching public key can check that the message came from the key's holder and was not altered.)

Provenance turns "I'm sure this came from the sensor" — a feeling — into "this is signed by a key in
the registry, and here is the check" — evidence. Note what it proves: *who* said it and that it was
not altered, not that it is *true*. A correctly signed reading from a sensor with a skewed clock is
still wrong ([SE1/D10](#d10)), so provenance is necessary for trust, not sufficient. Keep identities
distinct — the device, the human caller, the key that signs a release, the artifact itself — so that
stealing one does not grant the others. An administrator's password is typed often and stored in
many places; if it could also sign software releases, anyone who phished it could ship malware to
every device.

On the human side, a signature is a person saying *I have read this and I stand behind it.* That
cannot be delegated, and capable agents make it more important rather than less
([SE1/A7](10-agents.md#a7)).

> **Ask:** "Who said this, and how would I check?"


---

Next: [6. Testing](06-testing.md) — making tests worth trusting.
