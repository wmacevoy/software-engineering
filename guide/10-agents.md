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

Every session starts from the repository. A constraint that lives only in a head is K2 to the agent
([SE1/U6](02-unknowing.md#u6)), and it will hand you a clean, tested, plausible violation of that
constraint faster than you can read the diff. The hallway correction — "no, not like that" — is
gone.

So the agent's memory is the [working set](08-work.md#w10) — requirements, design, queue, findings —
plus a repository guide (a `CONTRIBUTING.md`, `CLAUDE.md`, or equivalent) that says how to run, test, and
reset, and where the seams are. Anything said only in chat does not exist for the next session.

- **The client never talks to the agent.** What the client said reaches the agent only through the
  requirements.
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
| a secret appeared in a prompt                            | the prompt goes to a third party      | rotate the secret; refer to secrets by name, never by value        |

---

Back to the [index](../README.md).
