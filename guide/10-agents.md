# 10. Agents

An agent is an extremely fast writer with no memory and no stake in the outcome. This chapter is
what changes when one is in the loop — for the humans directing it, and for the agent itself. The
operational rules are collected in [AGENTS.md](../AGENTS.md).

---

### <a id="a1"></a>A1. Producing code got cheaper faster than knowing it is right

Agents move the economics in one direction: **the cost of producing code has fallen much faster than
the cost of knowing the code is right.** Everything scarce migrates to the second half —
specification, verification, review, ownership. The bottleneck is no longer typing. It is attention.

> **Ask:** "Now that writing this is cheap, what is the expensive part?"

### <a id="a2"></a>A2. An agent is a K3 factory; never let confidence substitute for a run

Fluent, confident, plausible, and occasionally wrong is the precise shape of erroneous certainty,
arriving faster than anyone can check it ([SE1/U3](02-unknowing.md#u3),
[SE1/U7](02-unknowing.md#u7)). That is not an argument
against agents. It is an argument about where to spend the time they save.

"This should work" is K3 by construction. The agent runs the check; the human runs it again before
signing. An agent that cannot run the system cannot check its own claim — so give it one command to
run and one to reset.

> **Ask:** "Was this run, or only reasoned about?"

### <a id="a3"></a>A3. An agent arrives knowing nothing and leaves remembering nothing

*Changed in v1.2.*

Every session starts from the repository. A constraint that lives only in a head is K2 to the agent
([SE1/U6](02-unknowing.md#u6)), and it will hand you a clean, tested, plausible violation of that
constraint faster than you can read the diff. The hallway correction — "no, not like that" — is
gone.

So the agent's memory is the [working set](08-work.md#w10) — requirements, design, queue, findings —
plus a repository guide (a `CONTRIBUTING.md`, `CLAUDE.md`, or equivalent) that says how to run, test, and
reset, and where the seams are. Anything said only in chat does not exist for the next session. A
private memory an agent keeps between sessions is a head, not the working set: the team cannot see
it, nothing versions it, and the next tool or person never reads it, so a decision that lives only
there has failed [SE1/U6](02-unknowing.md#u6) at a new address.

- **The client's answers reach the code only through the requirements.** An agent may ask, and
  should when a task collides with a decision; what it is told is written down before anything is
  built on it, or it did not happen.
- **The contract comes before the code.** Otherwise the agent invents one, fluently — and every
  session invents a different one.
- **The K4s are written down.** An unwritten assumption is a K2 to the agent.

> **Ask:** "What would a competent stranger need to read to get this right the first time — and is it
> written down?"

### <a id="a4"></a>A4. Context is a budget, and it resets every session

On a real system an agent cannot read the whole project: it does not fit, and even where it fits,
reading everything to change one thing is the wrong price. So *how does a competent stranger find
the five files that matter, in ten minutes, without reading the other five hundred?* becomes a
load-bearing property of the repository.

The good news: it is the same property that makes a codebase habitable for people — clear component
boundaries, a README per component stating its contract, stable IDs that grep from a test to the
sentence that demanded it, a mechanically checked dependency rule, names that mean what they say.
**Factoring done for human comprehension pays twice.**

The bad news: some conventions that helped human readers now cost real money.

| Convention                             | What it costs now                                                       |
| -------------------------------------- | ----------------------------------------------------------------------- |
| A doc-comment on every function        | Context spent restating the signature — and stale prose reads exactly like true prose. |
| One enormous file                      | Must be searched and paged through to find the part that matters, and every edit risks a neighbor. |
| Deep indirection in the name of reuse  | Hides the seams from humans and agents alike.                           |
| Commented-out code, historical asides  | Ambiguous authority: is this the specification, or the past?            |

The replacement is not "no documentation." It is self-documenting code, a comment exactly where the
code cannot say *why*, and everything durable in the working set, where both kinds of reader look.

### <a id="a5"></a>A5. Spend the speed on lowering the cost of testing

Fixtures, harnesses, seed data, fault scripts, conformance checks, the boring second and third test
case. That work multiplies against every future change ([SE1/F2](03-feedback.md#f2)). More features
do not.

### <a id="a6"></a>A6. Review capacity is the bottleneck

An agent will happily produce three hundred lines. A diff you cannot review is a diff you cannot
sign. Ask for the smallest change that does the job, one concern at a time, with nothing bundled in
that was not asked for ([SE1/W11](08-work.md#w11)). Make rejection cheap.

### <a id="a7"></a>A7. Delegation is not abdication

The person who signs the change owns it — and if they cannot explain it, they cannot maintain it or
defend it. **Working code nobody can explain is a liability, not an asset.**

- Read the whole diff, not the summary. The line you skipped is the one that added a dependency,
  reformatted a file nobody asked about, or asserted nothing.
- Credit the agent and keep the authority: a `Co-Authored-By:` line at the end of the commit message
  (a *trailer*) says who drafted it; the human's signature says *I have read this and I stand behind
  it.* Both are true, and they are different claims ([SE1/D13](05-design.md#d13)).
- The agent does not commit, push, or publish unless asked. A push is a publication.

### <a id="a8"></a>A8. Agents move the human up the waterfall

Agents are fastest at the bottom of the waterfall — code, tests, fixtures, migrations. At the top,
where the work is conversations with people, laws, and a client's sense of proportion, they can
search and draft ([SE1/A9](#a9)) but cannot decide. They are very good at accidental complexity and
much less help with essential complexity, because essential complexity is *what the problem is*
([SE1/D8](05-design.md#d8)). So the speedup is real and concentrated in the part that was never the
hard part.

That moves the human *up*: to requirements, vocabulary, one-way doors, and coherence. An agent
produces a locally reasonable design every session and remembers no conventions between them, so
**humans own the structure; agents author and advise** ([SE1/D9](05-design.md#d9)). The requirements
document is the railing that keeps a machine-speed descent from becoming a machine-speed fall
([SE1/W8](08-work.md#w8)).

The five-minute flag is the canonical failure: asked for a feature that touches a scope decision, an
agent adds a boolean column and a table and is done before anyone has opened the requirements ([case
study](09-people.md#case-study-it-does-the-vip-spaces-too-right)). The costing comes before the
prompt.

### <a id="a9"></a>A9. Hand it the search-shaped work; keep the decisions

| Hand it                                                                 | Keep                                                         |
| ----------------------------------------------------------------------- | ------------------------------------------------------------ |
| the second and third test case, once the first is written               | the first one, which decides what the thing is               |
| fixtures, seed data, fault scripts, the conformance harness             | the requirement the harness checks                           |
| "which assumptions in the requirements does this sentence invalidate?"  | the decision about what to do with the answer                |
| a migration script, from a design written down                          | the schema design, and whether it is legal to keep the data  |
| translation packs, boilerplate, glue                                    | the vocabulary — a new noun is a decision                    |
| the retro questions                                                     | the retro                                                    |

### <a id="a10"></a>A10. Ask your agents, and write the answers down

Specific advice about prompting, how much to hand over, or what an agent can be trusted to do
unsupervised has a short shelf life — this chapter's included. The durable move is to ask the model
you are actually using:

- *What did you have to read that you should not have needed?*
- *What would have let you get this right the first time?*
- *What did you assume because nobody wrote it down?*

Put the answers in the repository, not the chat, where the next session — human or not — will find
them. That is how an agent joins a team: not by remembering, but by the team writing down what it
would have needed to remember. Treat the answers as proposals from something with no stake in the
outcome.

### <a id="a11"></a>A11. A summary is a concussion: check it from outside

*New in v1.2.*

Compaction, a resumed session, a handoff note: each gives the next context a summary written in the
same fluent voice as everything else. Nothing in it marks which parts were observed and which were
recalled, and the next context cannot tell by feel ([SE1/A3](#a3)). It carries on, confidently, from
whatever the summary says. The human version is a concussion nobody noticed: the player says
"I'm fine" and believes it. Asking the patient does not work. A sideline test does.

In [trials](../GAPS.md#6-a-summary-is-a-concussion), a confidently wrong summary sent 4 of 4 agents
straight into a change the owner had frozen. Marking the summary's claims as unverified changed the result in 1 of 4 runs. A rule in a file
the agent had to open changed nothing, because the file was never opened. Two things worked, in 4 of
4 runs each: the same rule already loaded into the agent's context, and a script, with no model in
it, that compared the summary with what the human had actually said and flagged the gap. That gap
was planted. Run over 29 real compactions from the author's own sessions, in many of which harm happened by
the author's account, the same script flagged 4 messages, all in one compaction
([GAPS](../GAPS.md#1-the-handoff-check-passed-nearly-every-real-compaction)): it has not yet been
seen to catch a real one.

The summary is not the only injury. In [later trials](../GAPS.md#1-knowing-is-not-doing) on a
project whose standing decision was *encryption at rest everywhere*, agents with that decision
freshly in front of them, compacted or not, built a new store in plaintext in every run: none of 71
was keyed, and the agents who wrote the decision into their own notes left it out of their code. A
guard the agent had to choose to run was read and never run; the one store that changed was refused
by a hook at a pause. Recall gets a rule into the next context. Only a check that runs on the new
work, without the agent choosing to run it, gets it into the work ([SE1/O3](07-operating.md#o3)).

So treat every handoff as a possible injury, and check from outside:

- **Put the rule where it is loaded at every start,** not where it has to be looked up, and check
  that it loads: an agent file that imports one from outside the working directory may load nothing
  and say nothing ([GAPS](../GAPS.md#2-an-import-from-outside-the-repository-does-not-load)). Import
  a copy kept inside it, and check that it loaded: a fresh session, asked without opening any file,
  can quote a line of it.
- **Give the handoff a sideline test:** a check that compares the summary with the record (the
  transcript, the requirements, the queue) and points the next context at the gap. It does not need
  a model, but it has to be able to say *wrong*: word overlap found the planted gap and passed
  nearly every real compaction, so until a check is seen to fire on a real one it is a K3 factory
  ([SE1/U7](02-unknowing.md#u7)). Point; don't hand over. When the check also
  pasted the missing words in, agents obeyed those words and stopped going to the source for
  everything else. A reliable thing checks itself ([SE1/T2](06-testing.md#t2)).
- **The summary is recalled, not observed, whether or not a check passed it.** Where it and the
  source disagree, the source wins.

> **Ask:** "What did this summary drop, and what would tell us?"


---

## When it goes wrong

| Symptom                                                  | Cause                                 | Do                                                                 |
| -------------------------------------------------------- | ------------------------------------- | ------------------------------------------------------------------ |
| it asserts something false about the code                | it did not open the file              | require it to show the line                                        |
| the diff touches files nobody named                      | scope creep, or reformatting          | reject; ask again with "only these files"                          |
| it added a dependency                                    | fluency                               | treat as a proposal; usually decline ([SE1/D12](05-design.md#d12))         |
| it "fixed" a failing test by weakening the assertion     | Goodhart on green ([SE1/F5](03-feedback.md#f5)) | restore the assertion; the test was right                       |
| it changed a requirement to match the code               | a design change in costume ([SE1/R5](04-requirements.md#r5)) | revert; a wrong requirement is a conversation with the client |
| the next session does not know what the last one decided | nothing was written down              | the working set; `FINDINGS`; a line in the repository guide        |
| it designed a schema before there was a requirement      | the waterfall, at machine speed       | stop; the railing ([SE1/W8](08-work.md#w8))                               |
| after compaction it confidently redoes or undoes a decision | it trusted its own summary          | the source wins; a handoff check after every compaction ([SE1/A11](#a11)) |
| a secret appeared in a prompt                            | the prompt goes to a third party      | rotate the secret; refer to secrets by name, never by value        |

---

Back to the [index](../README.md).
