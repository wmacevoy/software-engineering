# Reading

The longer arguments behind the guide, one line each on what the source actually says, so you can pick
one rather than all. Grouped by the chapter they support most.

**Purpose, unknowing, feedback** ([1](guide/01-purpose.md)–[3](guide/03-feedback.md))

- **Richard Cook, "How Complex Systems Fail"** — eighteen short paragraphs; the best return per page on
  this list, including on why blame is the wrong instrument.
- **Forsgren, Humble, and Kim, *Accelerate*** — the measured case that fast feedback and reliability are
  the same variable, not a trade.
- **Nancy Leveson, *Engineering a Safer World*** — safety as a property of the system, not of its
  components.

**Requirements** ([4](guide/04-requirements.md))

- **Donald Gause and Gerald Weinberg, *Exploring Requirements*** — the intake conversation as a method;
  the census question is theirs.
- **Donald Gause and Gerald Weinberg, *Are Your Lights On?*** — short, funny, and entirely about whose
  problem it is. Read it before the first client meeting.
- **Mike Cohn, *User Stories Applied*** — the story-to-acceptance-test chain at book length.

**Design** ([5](guide/05-design.md))

- **Fred Brooks, *The Mythical Man-Month*** — conceptual integrity, and why adding people to a late
  project makes it later. Chapters 2, 3, 4, 7, and 16 carry most of it.
- **Fred Brooks, "No Silver Bullet"** — essential versus accidental complexity, in about fifteen pages.
- **David Parnas, "On the Criteria To Be Used in Decomposing Systems into Modules"** — two ways to split
  the same program, and why the one that hides decisions wins.
- **John Ousterhout, *A Philosophy of Software Design*** — "deep modules" is the abstraction test stated
  as a design goal.
- **Rich Hickey, "Simple Made Easy"** (talk) — simple is about how tangled a thing is; easy is about how
  familiar. Confusing them is how accidental complexity gets defended.
- **Leslie Lamport, "Time, Clocks, and the Ordering of Events in a Distributed System"** — why there is no
  single "now."

**Testing** ([6](guide/06-testing.md))

- **The ArduinoUnit guidebook, "The Zen of Testing"** — `guidebook.md` in the
  [ArduinoUnit repository](https://github.com/mmurdoch/arduinounit); the source of chapter 6.
- **Martin Fowler, "Eradicating Non-Determinism in Tests"** — shared fixtures, asynchrony, time, and
  resource leaks, each with the fix.
- **Michael Feathers, *Working Effectively with Legacy Code*** — seams: serve, don't rule, applied to
  code that already exists.
- **Kent Beck, *Test-Driven Development: By Example*** — the map before the journey, as a daily practice.
- **Semantic Versioning** (semver.org) and **Reproducible Builds** (reproducible-builds.org) — the
  promise behind pinning, and how far "repeatable" can be pushed.

**Operating** ([7](guide/07-operating.md))

- **Michael Nygard, *Release It!*** — failure as an input, with the patterns named: timeouts, bulkheads,
  circuit breakers, health checks, and the deploy as a test.
- **Betsy Beyer et al., *Site Reliability Engineering*** (Google) — error budgets, symptom-based
  alerting, and blameless postmortems, from people who run very large systems.
- **Danilo Sato, "ParallelChange"** (martinfowler.com) — expand and contract, in one short article.
- **OWASP Top Ten** (owasp.org) — the most common ways web applications are attacked, with defenses.

**Work** ([8](guide/08-work.md))

- **Winston Royce, "Managing the Development of Large Software Systems"** — the waterfall diagram, and on
  the next pages the argument against it. Read past the figure.
- **Barry Boehm, "A Spiral Model of Software Development and Enhancement"** — do the riskiest thing first,
  in the smallest increment that retires the risk.
- **Craig Larman and Victor Basili, "Iterative and Incremental Development: A Brief History"** — the loop
  predates the word *agile* by forty years.
- **The Agile Manifesto** — four values and twelve principles on one page.
- **Ken Schwaber and Jeff Sutherland, *The Scrum Guide*** — the framework, defined by its authors in
  about thirteen pages. Read it before anyone's opinion of it.
- **Kent Beck, *Extreme Programming Explained*** — spikes, the planning game, the on-site customer, and
  the argument that practices reinforce each other and fail alone.

**People** ([9](guide/09-people.md))

- **Melvin Conway, "How Do Committees Invent?"** — four pages: the system copies the communication
  structure, so choose the structure.
- **Tom DeMarco and Timothy Lister, *Peopleware*** — the team as the unit of production, and what fear
  and interruption do to it.
