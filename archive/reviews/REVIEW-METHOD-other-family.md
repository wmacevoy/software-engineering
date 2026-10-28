# A review by an agent of another family: how it was run

Recorded 2026-10-28, so the next one can be run the same way and compared with this one. The
first run was OpenAI Codex on v1.2.1 ([REVIEW-v1.2.1-codex.md](REVIEW-v1.2.1-codex.md)): three
minutes, 1,036 words, five findings that held when opened at the source, all acted on in v1.3. Two
further defects surfaced while acting on them (the checker's patch rule blocked any AGENTS.md
change after a patch tag; `se --self` decoded `git show` with the locale's code page on Windows).

## Why

Only reality and someone who does not share your assumption find a K3
([SE1/U3](../../guide/02-unknowing.md#u3)). Every trial and review of this guide had used Claude
models; a reviewer of another family does not share their training, and the guide's own notice
asks such a reader to push back. Its report is a proposal; what is trusted is what can be checked.

## The setup

```sh
mkdir -p ../codex && git clone ~/projects/software-engineering ../codex/software-engineering
cd ../codex/software-engineering
git remote set-url --push origin DISABLED     # no push target; seen to fail with `git push --dry-run`
git rm -rq archive/reviews                    # and the archive README's listing of them, so the read is fresh
git commit -m "codex clone: Claude's reviews removed for a fresh read"
node tools/check.js && python3 se.py --self && python3 -I tools/test_se.py   # the clone's own checks, green
```

The brief lives beside the clone, not in it. The reviewer runs in a sandbox with the network off
and writes exactly one file, `archive/reviews/REVIEW-<release>-<family>.md`; read-only otherwise;
no commits. With the network off, `se --doctor`'s first row says the release check was not made;
whether the reviewer reports that as it is counts as a finding about the reviewer.

## The brief, as given

> # Brief for a Codex review of the software-engineering guide, v1.2.1
> 
> You are in a clone of https://github.com/wmacevoy/software-engineering at release v1.2.1, a guide to
> software engineering written for people and for the AI agents working beside them. Every trial,
> review, and tool behind it so far used Claude models; you are the first reviewer of another family,
> and the guide asks for exactly that: push back, and propose. Claude's earlier reviews were removed
> from this clone so that you read fresh; the commit at HEAD says so.
> 
> **Read-only on the guide's files.** Write your review to `archive/reviews/REVIEW-v1.2.1-codex.md`
> (create the directory) and nothing else. Do not commit, do not push, do not edit any other file.
> The remote's push URL is disabled on purpose. If the network is off, `se --doctor`'s first row will
> say so; report what it says, as it is.
> 
> Two questions, in this order.
> 
> ## 1. Does AGENTS.md follow its own best practices?
> 
> Read AGENTS.md first as the rules it states, then as a file: does it do what it asks of an agent?
> For each rule you test, quote the rule and quote the place, in the file or in the repository, that
> keeps or breaks it. Rules worth testing: *smallest change*; *one word, one thing* (is any word used
> in two senses?); *say what you did not do*; *secrets by name*; *say how sure you are and what you
> ran*; *a rule can be argued with rather than merely obeyed* (does each rule's cited principle, in
> `guide/`, actually say what the rule says? check a sample); *never assert something about the code
> you have not opened the file to check* (does the file itself assert things it cannot know?); and
> the notice that the testing was Claude-only (is it honest about what was and was not tested?). The
> principles are in `guide/`; the evidence behind them is in `GAPS.md` and `archive/`, where each
> source entry says whether it was opened or only reported.
> 
> ## 2. How does AGENTS.md work in your context, right now?
> 
> Say what you loaded at the start of this session and how you know. The file says it must be
> "loaded at every start, not left in a file to be opened"; is it, for you? Which rules fit you,
> which do not, and which assume Claude Code (`CLAUDE.md`, `.claude/settings.json`, hooks,
> compaction)? `ADOPT.md` and `se.py` are the places to look. Run `python3 se.py --doctor --offline
> --repo .` and `python3 se.py --post`, and say what each got right and wrong about you and this
> session. Where a rule or a check does not fit, write the sentence you would put in a pull request.
> 
> ## Return form
> 
> At most 1,200 words. For every finding: the file and line, the quoted sentence, what is wrong or
> right with it in one or two sentences, and whether you opened the source or only read the file that
> cites it. End with three things: what you ran and the last line of each output (`node
> tools/check.js`, `python3 -I tools/test_se.py`, `python3 se.py --self`); what you did not check; and
> one paragraph on the single most important thing. "This holds" and "nothing" are complete answers.
> Do not invent findings to fill the form. Time box: about thirty minutes of reading, then stop and
> write what you have, marking what is unchecked.

## Reading the review

1. **Open the source of each load-bearing claim before acting.** Of Codex's six items, five held;
   the sixth, that one commit held two concerns, was a choice the commit message had already
   recorded.
2. **Compare with the earlier readers** (the three lenses in
   [REVIEW-v1.2-candidate.md](REVIEW-v1.2-candidate.md)). Overlap is correlated agreement and worth
   little; a finding only the new reader makes is the value; a contradiction goes to the source.
   Here four of five findings were in text written after the earlier readers ran, so they could not
   have caught them; the fifth, a vocabulary collision, was the drafter's to see and was missed.
3. **Grade what it leaves, not what it says**: `git status` in the clone (one untracked file, the
   review) and the checker on the clone.
4. **Carry findings over by hand**, one concern per commit, as a pull request would be; the review
   file itself goes into `archive/reviews/`.

## The second run, not yet made: planted defects

Before the reviewer runs, plant four or five defects the checker cannot see, of different kinds,
and keep the key outside the clone: a number in GAPS that contradicts its archive extraction; an
internal contradiction between A11 and GAPS; the archive's Royce entry disagreeing with W2; a
sentence claiming a hook "has been seen to fire on a real compaction"; a test design weakened
(ADOPT.md's phrase test without "or that opens the file to answer"). The hit rate on the planted
set is the reviewer's sensitivity, measured before its real findings are weighed; filter the
planted ones out and what remains is the review. This is the compaction project's planted-claims
method ([SE1/T3](../../guide/06-testing.md#t3)) turned on a reviewer. The cost is that the reviewer
reads a slightly wrong guide; the author chose the honest run first.
