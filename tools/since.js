#!/usr/bin/env node
// A since for every principle, mined from git: the release at which its current text first appeared
// and that release's date, written as the marker under the heading. A hand-made marker drifts and
// says nothing for a principle nobody touched; this one is recomputed from the tags and checked, so
// a principle that reads as unchanged says since when (SE1/U7: make it age visibly).
// Usage: node tools/since.js            print the expected marker for every principle
//        node tools/since.js --write    write them into the chapters
//        node tools/since.js --check    exit 1 where a chapter's marker differs from git's answer
// A New/Changed kind is a person's claim about meaning and is kept as written; this tool adds the
// release's date and, when the wording moved later without the meaning, "text since". A principle
// changed after the newest tag gets the unreleased section's name from CHANGELOG.md; the checker
// still demands a New/Changed claim or an *Also changed* line for it. Needs the release tags.
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');
const { HEADING, MARKER, bodies } = require('./bodies');

const root = path.resolve(__dirname, '..');
const git = (...args) => { try { return execFileSync('git', ['-C', root, ...args], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] }); } catch { return null; } };
const num = (v) => v.slice(1).split('.').map(Number);
const cmp = (a, b) => { const [x, y] = [num(a), num(b)]; return x[0] - y[0] || x[1] - y[1] || (x[2] || 0) - (y[2] || 0); };
const tags = (git('tag', '--list', 'v*') || '').split('\n').filter((t) => /^v\d+\.\d+(\.\d+)?$/.test(t)).sort(cmp);
if (!tags.length) { console.error('since: no release tags here (git fetch --tags)'); process.exit(2); }
const dateOf = Object.fromEntries(tags.map((t) => [t, (git('log', '-1', '--format=%cs', t) || '').trim()]));
const top = fs.readFileSync(path.join(root, 'CHANGELOG.md'), 'utf8').match(/^## (v\d+\.\d+(?:\.\d+)?) — unreleased$/m);
const unreleased = top ? top[1] : 'unreleased';
const mode = process.argv.includes('--write') ? 'write' : process.argv.includes('--check') ? 'check' : 'print';
const named = process.argv.slice(2).filter((a) => !a.startsWith('--'));
const chapters = named.length ? named.map((f) => path.resolve(root, f))
  : fs.readdirSync(path.join(root, 'guide')).filter((n) => /^\d\d-.*\.md$/.test(n)).sort().map((n) => path.join(root, 'guide', n));

let problems = 0, written = 0;
for (const file of chapters) {
  const rel = path.relative(root, file).split(path.sep).join('/');
  const text = fs.readFileSync(file, 'utf8');
  const lines = text.split('\n');
  const now = bodies(text);
  const at = Object.fromEntries(tags.map((t) => [t, bodies(git('show', `${t}:${rel}`) || '')]));
  const expected = [];
  for (const [id, body] of now) {
    // The text's since: the oldest tag from which the body has equalled today's in an unbroken run.
    let since = null;
    for (let i = tags.length - 1; i >= 0; i--) { if (at[tags[i]].get(id) === body) since = tags[i]; else break; }
    const textSince = since ? [since, dateOf[since]] : [unreleased, 'unreleased'];
    const index = lines.findIndex((l) => { const m = l.match(HEADING); return m && m[2] === id; });
    const mk = (lines[index + 2] || '').match(MARKER);
    const human = mk && mk[1] !== 'Since' ? { kind: mk[1], release: mk[2] } : null;
    let line;
    if (human) {
      const d = tags.includes(human.release) ? dateOf[human.release] : 'unreleased';
      line = `*${human.kind} in ${human.release} (${d})${textSince[0] !== human.release ? `; text since ${textSince[0]} (${textSince[1]})` : ''}.*`;
    } else {
      line = `*Since ${textSince[0]} (${textSince[1]}).*`;
    }
    expected.push({ id, line, index, has: !!mk });
  }
  if (mode === 'print') for (const e of expected) console.log(`${rel}\t${e.id}\t${e.line}`);
  if (mode === 'check') for (const e of expected) {
    const actual = e.has ? lines[e.index + 2] : '(no marker)';
    if (actual !== e.line) { problems++; console.log(`${rel} ${e.id}: marker is ${actual}; git says ${e.line}`); }
  }
  if (mode === 'write') {
    for (const e of expected.sort((a, b) => b.index - a.index)) {  // from the bottom, so indices hold
      if (e.has) { if (lines[e.index + 2] !== e.line) { lines[e.index + 2] = e.line; written++; } }
      else { lines.splice(e.index + 1, 0, '', e.line); written++; }
    }
    fs.writeFileSync(file, lines.join('\n'));
  }
}
if (mode === 'check') { console.log(`${chapters.length} chapters, ${problems} marker(s) differ from git`); process.exit(problems ? 1 : 0); }
if (mode === 'write') console.log(`${written} marker(s) written`);
