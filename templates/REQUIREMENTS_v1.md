# Requirements — v1

What must be observably true, and what is not being built. Changes only with the client; a change is
a new version (`REQUIREMENTS_v2.md`), never an edit to this one. See
[R1–R11](../guide/04-requirements.md).

Client (the one voice who can decide): _name_ · Date sent: _yyyy-mm-dd_ · *Tell us what is wrong with it.*

## Glossary

Ten to thirty terms, one line each. A new noun is a decision ([D9](../guide/05-design.md#d9)).

| Term   | Meaning |
| ------ | ------- |
| _term_ | _one line_ |

## The pain

What happens today when it goes wrong, who gets the call, and what they say.

## People this touches

Every kind of person, including those not in the room, and anyone treated differently.

## Requirements

Numbered, observable, with numbers. Prefix by area with at least two letters and a hyphen
(`UI-1`, `COL-1`, …) so they are never confused with the guide's principle IDs (`U1`, `R6`).
Mark invented numbers *(invented)*.

- **UI-1** _A sentence a different team could satisfy a different way, checkable from outside._

## Inputs: absent, late, wrong, lying

| Input | Absent | Late | Wrong | Lying |
| ----- | ------ | ---- | ----- | ----- |
| _input_ | | | | |

## Operating envelope

- **Scale:** _how many, and in two years_ — and what we are explicitly not designing for.
- **Speed:** _latency, percentile, at what load_ (e.g. 95% of page loads under 1 s at the event peak).
- **Recovery:** _per component: behavior while down; how to get back, by whom, how long (timed)._
  How much data may we lose?
- **Availability:** _budget, period, beneficiary, maintenance window._

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
