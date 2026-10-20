# 2. Unknowing

Building something is mostly finding out what you did not know. This chapter names the five kinds of
not-knowing, says what each costs, and says how to move each one before it charges full price. The
labels `K0`–`K4` are used throughout the guide.

| #      | Category             | What it is                                                         | On a class project                                                  |
| ------ | -------------------- | ------------------------------------------------------------------ | ------------------------------------------------------------------- |
| **K0** | The known            | Things you know, that are true.                                    | Your language's `sort` is stable; you checked the docs.             |
| **K1** | The known unknown    | Things you know you don't know.                                    | "I don't know how the grader feeds input. I'll ask."                |
| **K2** | The unknown unknown  | Things you didn't know you didn't know.                            | The grader's input file has Windows line endings. Nobody thought to ask. |
| **K3** | Erroneous certainty  | What feels like K0 and is false.                                   | "My delete handles the head node." It doesn't.                      |
| **K4** | Chosen falsehood     | Things held as true, knowing they aren't, because they are useful. | "Input is well-formed" — written in the README, with what breaks if it isn't. |

---

### <a id="u1"></a>U1. K0 through K3 are in order of expense; K4 is a choice

K0 costs nothing; you already know it. Finding out a K1 is cheap — you know the question, so you can
look it up or ask. A K2 costs a rewrite, because it arrives as a surprise after you have built on
the wrong picture. A K3 costs the most: whatever was built on top of the belief, discovered at the
worst possible moment.

K4 is not on that ladder at all. It is a decision, and usually a good one.

### <a id="u2"></a>U2. Building is discovering, in the right order and at the right price, which category each part of the problem belongs to

Every practice in this guide is a way of moving something **toward K0** — from a more expensive
category to a cheaper one — before it charges full price:

| From | To     | How                                                                                                         |
| ---- | ------ | ----------------------------------------------------------------------------------------------------------- |
| K0   | stays  | Write it down so it stays known. Tests are executable knowledge, and unlike prose they complain when they go stale. |
| K1   | K0     | Spikes, prototypes, reading the source, asking the client. The only category you can simply decide to spend time on. |
| K2   | K1     | Exposure to reality, early and repeatedly: integrate, deploy, demo, inject faults, watch real use. You cannot search for these; you can only arrange to be surprised sooner and more cheaply — and asking someone who knows a domain you don't is the cheapest exposure there is ([SE1/R8](04-requirements.md#r8)). |
| K3   | K0     | Evidence: a test that could have failed, an output you actually looked at, a signature you checked, a second person who does not share your assumption. |
| K4   | chosen | Name the falsehood, write down where it is load-bearing, know the blast radius when it comes due.          |

> **Ask:** "Which category is this part of the problem in — and what is the cheapest way to move it?"

### <a id="u3"></a>U3. K3 is the one to be afraid of

K1 and K2 are honest. K3 is expensive precisely because it costs nothing at the time: no search is
triggered, no question is asked, no ticket is filed. You are not looking, because as far as you know
there is nothing to look for.

**Only two things find K3: reality, and someone who does not share your assumption.** That is the
whole justification for running the code instead of reasoning about it, for integrating early, and
for review by another person rather than by yourself an hour later — and for letting other people
say what needs testing: you cannot see past your own design, and a reviewer, the client at a demo,
or an attacker can.

The same reasoning says an attack should be *demonstrated before its defense is trusted*
([SE1/T8](06-testing.md#t8)). "Users can't see each other's orders" is K3 until you have logged in
as one user, requested another user's order by ID, and watched the request be refused. The same
holds for any check that guards against misuse — a signature check, an input validator, a permission
rule: you have not seen it work until you have seen it say no.

> **Ask:** "What would I see if I were wrong about this — and have I looked?"

### <a id="u4"></a>U4. Every abstraction rests on chosen falsehoods; write down where they are load-bearing

An abstraction is a simplified picture you agree to work with — "a network call returns a value,"
"`now()` tells the time" — and every simplified picture is false somewhere. You cannot build
anything without these K4s. A typical system holds a stack of them:

- The clock is correct.
- The network delivers.
- The input is honest.
- The configuration has not changed since startup.
- The login token reflects the user's current role. (It reflects their role as of when it was
  issued — hours ago, perhaps.)

The engineering act is not avoiding these. It is choosing them deliberately, recording them, and
knowing what breaks when one *comes due* — when the world stops matching the picture. A falsehood is
**load-bearing** where something important depends on it being true, and its **blast radius** is
everything that breaks when it stops being true. **An abstraction leaks exactly where its falsehood
was load-bearing.** A K4 you have chosen is an asset; the same falsehood held unknowingly is K3.

> **Ask:** "What are we assuming here that we know is not quite true — and where is that written?"

### <a id="u5"></a>U5. Estimate the category, not the task

"Two days" usually means "two days if nothing I haven't thought of happens" — a K0 statement about a
schedule governed by K2.

| The work is mostly | It estimates as                        |
| ------------------ | -------------------------------------- |
| K0                 | a number                               |
| K1                 | a range                                |
| K2                 | nothing; it can only be **time-boxed** |

Say which kind you are handing over. When it is unclear which category the work is in — integrating
with a vendor's API nobody on the team has used, say — treat it as K2: time-box a short spike to
find out what you don't know, then give a range for the rest.

> **Ask:** "Is this an estimate, a range, or a time box?"

### <a id="u6"></a>U6. Nothing important may live only in a head

A constraint that exists only in one person's head fails in both directions at once. For its holder
it is K3 — they believe everyone knows it. For everyone else it is K2 — you cannot ask about
something you have no idea exists.

It used to be a survivable liability: the person holding the constraint sat nearby, saw the change,
and said "no, not like that." Teammates leave, get sick, and forget. Agents were never in the room
([SE1/A3](10-agents.md#a3)). So the state of a project has to be **observable from where every party
stands**, in the repository, versioned with the code ([SE1/W10](08-work.md#w10),
[templates](../README.md#contents)).

> **Ask:** "If the person who knows this vanished on Friday, what could the rest of us not do on
> Monday?"

### <a id="u7"></a>U7. Find the K3 factories: anything that keeps saying "fine" with no way to say "wrong"

*New in v1.1.*

A K3 is one wrong belief ([SE1/U3](#u3)). A **K3 factory** is whatever keeps producing them: a signal
that says "fine," costs nothing to keep believing, and has no path by which it could say "wrong." It
makes confidence faster than evidence, and every belief it makes is found last. Some that are cheap
to fix once named:

- **Conversations that never move into documents.** Everyone in the room agreed; nobody else can find
  out what ([SE1/U6](#u6)).
- **Unversioned references** to requirements and design. The citation still resolves after the text
  it pointed at has moved ([SE1/R10](04-requirements.md#r10)).
- **Agent compaction.** When an agent's context is summarized to make room, the summary replaces what
  was said, and the agent carries on exactly as confidently ([SE1/A4](10-agents.md#a4)).
- **Documentation a small model could have written from the code**: a block that restates *what* the
  code does, away from the line it describes. It reads as documented, carries no *why*, and drifts.
  Put the comment at the line it explains, and let the code be the document of *what*.
- **Code and documents that cannot be searched for a concept.** A concept with three names, or none,
  returns nothing to a search, and "nothing found" reads as "we don't do that"
  ([SE1/D9](05-design.md#d9)).
- **A status with no *since*.** "Blocked" reads as current when it is three days old
  ([SE1/H4](09-people.md#h4)).
- **An alert never seen firing.** Silence looks exactly like health ([SE1/O4](07-operating.md#o4)).
- **A default nobody chose** — a timeout, a retention period, an unpinned version. It works, so
  nobody asks who decided ([SE1/R6](04-requirements.md#r6), [SE1/O2](07-operating.md#o2)).

Three cures, each the opposite of what makes a factory:

1. **Give the signal a way to fail, and watch it fail once** — a test seen red, an alert seen firing,
   an attack seen refused ([SE1/T3](06-testing.md#t3)).
2. **Make it age visibly** — a version on the citation, an age on the cached value, a *since* on the
   status ([SE1/R10](04-requirements.md#r10), [SE1/D2](05-design.md#d2)).
3. **Make its source checkable** — who said it, where it is written, and how to check it without
   asking them again ([SE1/D13](05-design.md#d13)).

> **Ask:** "What here would keep saying 'fine' if it were wrong?"


---

Next: [3. Feedback](03-feedback.md) — the cost of a test, and why software has to build its own
signals.
