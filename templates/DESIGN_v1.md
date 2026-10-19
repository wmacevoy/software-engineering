# Design — v1

How we intend to satisfy the requirements, and what we rejected. Every mechanism here should be
replaceable without renegotiating a requirement ([R5](../guide/04-requirements.md#r5)).

## Components and the dependency rule

| Component | Layer | Kind | Contract (one line) | Holds state? |
| --------- | ----- | ---- | ------------------- | ------------ |

A component may depend only on strictly lower layers; a check enforces it ([D10](../guide/05-design.md#d10)).

## State

For every piece of state: owner, copies, how stale each copy may be, and what a user sees while it is
wrong ([D1](../guide/05-design.md#d1)–[D6](../guide/05-design.md#d6)).

| State | Owner (authoritative) | Copies | Max staleness | While wrong, the user sees |
| ----- | --------------------- | ------ | ------------- | -------------------------- |

## Essential complexity

Five to fifteen lines, each traceable to a requirement ID ([D8](../guide/05-design.md#d8)).

## One-way doors

Each with its review: who reviewed it, what assumption they did not share ([D11](../guide/05-design.md#d11)).

## Decisions

- **_Decision_** — _requirement IDs_ — _why_ — _rejected alternatives and why_

## Deferred

Named so they are not mistaken for oversights ([R9](../guide/04-requirements.md#r9)).

- _Not yet: …_ — _reason, and what would trigger it_
