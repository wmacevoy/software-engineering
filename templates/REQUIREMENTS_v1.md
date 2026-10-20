# Requirements — v1

What must be observably true, and what is not being built. Changes only with the client; a change is
a new version (`REQUIREMENTS_v2.md`), never an edit to this one. See
[SE1/R1–R11](https://github.com/wmacevoy/software-engineering/blob/v1.1/guide/04-requirements.md).

Client (the one voice who can decide — or, with none in the room, the named proxy for the users; see
[SE1/H5](https://github.com/wmacevoy/software-engineering/blob/v1.1/guide/09-people.md#h5)): _name_
· Date sent: _yyyy-mm-dd_ · *Tell us what is wrong with it.*

## Glossary

Ten to thirty terms, one line each. A new noun is a decision
([SE1/D9](https://github.com/wmacevoy/software-engineering/blob/v1.1/guide/05-design.md#d9)).

| Term   | Meaning |
| ------ | ------- |
| _term_ | _one line_ |

## The pain

What happens today when it goes wrong, who gets the call, and what they say.

## People this touches

Every kind of person, including those not in the room, and anyone treated differently.

## Requirements

Numbered, observable, with numbers. Prefix by area with at least two letters and a hyphen (`UI-1`,
`COL-1`, …), and mark each with the version that last changed it. Cite them with that version —
`REQ1/UI-1` — in tests, commits, and the queue
([SE1/R10](https://github.com/wmacevoy/software-engineering/blob/v1.1/guide/04-requirements.md#r10)). Mark
invented numbers *(invented)*, and requirements read off existing code rather than agreed with the
client *(inferred)*
([SE1/W12](https://github.com/wmacevoy/software-engineering/blob/v1.1/guide/08-work.md#w12)). Tests
name these IDs; this document never lists its tests
([SE1/R11](https://github.com/wmacevoy/software-engineering/blob/v1.1/guide/04-requirements.md#r11)).

- **UI-1** *(since v1)* _A sentence a different team could satisfy a different way, checkable from
  outside._

## Inputs: absent, late, wrong, lying

| Input | Absent | Late | Wrong | Lying |
| ----- | ------ | ---- | ----- | ----- |
| _input_ | | | | |

## Operating envelope

- **Scale:** _how many, and in two years_ — and what we are explicitly not designing for.
- **Speed:** _latency, percentile, at what load_ (e.g. 95% of page loads under 1 s at the event
  peak).
- **Recovery:** _per component: behavior while down; how to get back, by whom, how long (timed)._
  How much data may we lose?
- **Availability:** _budget, period, beneficiary, maintenance window._
- **Resources** (where finite): _code size, memory, stack, storage, energy — each a number, and the
  test that measures it._
- **Interruption:** _what must still hold if power or the connection is cut at any instant, and the
  test that cuts it._

## Security, law, and ethics

Threat model. What data about people is collected, kept, for how long, who may see it, which rule
applies, and who said so.

## Assumptions (K4s), read back to the client

- "We're assuming _…_. True?" — _answer, date_

## Scope decisions

- _Decision_ — _reason_

## Non-goals

- _Not building …_ — _reason_

## Not yet answered

Guesses nobody has agreed to.

- _Question_ — _who can answer, by when_

## Deferred

Wanted and agreed, but not in this version — named so it is not mistaken for an oversight
([SE1/R9](https://github.com/wmacevoy/software-engineering/blob/v1.1/guide/04-requirements.md#r9)).

- _Not yet: …_ — _reason, and what would trigger it_
