#!/usr/bin/env node
// Checks the guide's own consistency, so the conventions are enforced rather than hoped for (O3):
// every relative link and anchor resolves, every principle citation carries the current version and
// points at the file that defines it, every bare citation such as "(SE1/A8, SE1/D9)" names a real
// principle, chapter numbers agree, README's principle index matches the chapter headings exactly,
// every file llms.txt links to exists, and CHANGELOG.md, the *New/Changed in vX* markers under
// principle headings, and the release that AGENTS.md and the templates link to all agree.
// Exits nonzero on any problem.
// Usage: node tools/check.js
const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
// Releases come from CHANGELOG.md's "## v1.1 — date" headings, newest first.
const RELEASE = /^## (v\d+\.\d+) — \d{4}-\d{2}-\d{2}$/;
const changelog = fs.readFileSync(path.join(root, 'CHANGELOG.md'), 'utf8');
const releases = changelog.split('\n').map((l) => l.match(RELEASE)).filter(Boolean).map((m) => m[1]);
const latest = releases[0];
const newer = (a, b) => { const [x, y] = [a, b].map((v) => v.slice(1).split('.').map(Number)); return x[0] - y[0] || x[1] - y[1]; };
// Copies of AGENTS.md and the templates link to a release tag; the guide's own pages may link to main.
const GH = new RegExp(`^https://github\\.com/wmacevoy/software-engineering/blob/(main|${releases.map((r) => r.replace('.', '\\.')).join('|')})/`);
const GH_README = 'https://github.com/wmacevoy/software-engineering#';
const HEADING = /^### <a id="([a-z0-9]+)"><\/a>([A-Z]\d+)\. (.*)$/;
// Every citation carries the major version (README, "Principle index"); headings define IDs bare.
const VERSION = 'SE1';

const files = [];
(function walk(dir) {
  for (const name of fs.readdirSync(dir)) {
    if (name === '.git' || name === 'node_modules') continue;
    const p = path.join(dir, name);
    if (fs.statSync(p).isDirectory()) walk(p);
    else if (p.endsWith('.md')) files.push(p);
  }
})(root);

// GitHub's heading slug, close enough for the headings used here.
const slug = (h) => h.trim().toLowerCase().replace(/[^\p{L}\p{N}\s_-]/gu, '').replace(/\s/g, '-');

function anchorsOf(file) {
  const text = fs.readFileSync(file, 'utf8');
  const anchors = new Set();
  for (const line of text.split('\n')) {
    if (/^#{1,6} /.test(line)) anchors.add(slug(line.replace(/^#+ /, '').replace(/<a id="[^"]+"><\/a>/, '')));
  }
  for (const m of text.matchAll(/<a id="([^"]+)">/g)) anchors.add(m[1]);
  return anchors;
}

let problems = 0;
function problem(msg) { console.log(msg); problems++; }

const definedIn = new Map(); // principle ID -> chapter file
const headings = [];         // index lines README must contain
const marker = new Map();    // principle ID -> { kind: 'New' | 'Changed', release }
for (const f of files.filter((f) => f.includes(`${path.sep}guide${path.sep}`)).sort()) {
  const lines = fs.readFileSync(f, 'utf8').split('\n');
  lines.forEach((line, i) => {
    const m = line.match(HEADING);
    if (!m) return;
    if (definedIn.has(m[2])) problem(`${m[2]} defined twice`);
    definedIn.set(m[2], f);
    headings.push(`- [**${VERSION}/${m[2]}**](guide/${path.basename(f)}#${m[1]}) ${m[3]}`);
    // The marker, if any, is the first paragraph under the heading.
    const mk = (lines[i + 2] || '').match(/^\*(New|Changed) in (v\d+\.\d+)\.\*$/);
    if (mk) marker.set(m[2], { kind: mk[1], release: mk[2] });
  });
}

for (const f of files) {
  const text = fs.readFileSync(f, 'utf8');
  for (const m of text.matchAll(/\[([^\]]+)\]\(([^)]+)\)/g)) {
    let [, label, href] = m;
    const gh = href.match(GH);
    if (!gh && href.startsWith('https://github.com/wmacevoy/software-engineering/blob/')) { problem(`unknown ref    ${path.relative(root, f)}: ${m[0]}`); continue; }
    if (gh) href = path.relative(path.dirname(f), path.join(root, href.slice(gh[0].length)));
    else if (href.startsWith(GH_README)) href = path.relative(path.dirname(f), path.join(root, 'README.md')) + '#' + href.slice(GH_README.length);
    else if (/^[a-z]+:/.test(href)) continue;
    const [target, anchor] = href.split('#');
    const targetFile = target ? path.resolve(path.dirname(f), target) : f;
    const where = `${path.relative(root, f)}: ${m[0]}`;
    if (!fs.existsSync(targetFile)) { problem(`missing file   ${where}`); continue; }
    if (anchor && !anchorsOf(targetFile).has(anchor)) problem(`missing anchor ${where}`);
    const cite = label.replace(/\*/g, '');
    if (/^[PUFRDTOWHA]\d+$/.test(cite)) { problem(`unversioned    ${where}`); continue; }
    const v = cite.match(/^(SE\d+)\/([A-Z]\d+)$/);
    if (v) {
      const id = v[2];
      if (v[1] !== VERSION) problem(`wrong version  ${where}`);
      else if (!definedIn.has(id)) problem(`unknown ID     ${where}`);
      else if (definedIn.get(id) !== targetFile) problem(`wrong file     ${where} (defined in ${path.relative(root, definedIn.get(id))})`);
    }
  }
}

// Bare citations — the form AGENTS.md uses, so it stays short when copied into other repositories.
// Only the chapter letters count, so "(K3)" and other parentheticals are left alone.
const CITE = '(?:SE\\d+\\/)?[PUFRDTOWHA]\\d+';
for (const f of files) {
  for (const m of fs.readFileSync(f, 'utf8').matchAll(new RegExp(`\\((${CITE}(?:,\\s*${CITE})*)\\)`, 'g'))) {
    for (const cite of m[1].split(/,\s*/)) {
      const where = `${path.relative(root, f)}: ${m[0]}`;
      const [version, id] = cite.includes('/') ? cite.split('/') : [null, cite];
      if (!version) problem(`unversioned    ${where}`);
      else if (version !== VERSION) problem(`wrong version  ${where}`);
      else if (!definedIn.has(id)) problem(`unknown ID     ${where}`);
    }
  }
}

// Chapter numbers: the file prefix, the title, and every link label that names a chapter agree.
const chapterTitle = new Map(); // "07-operating.md" -> "7. Operating"
for (const f of files.filter((f) => /guide[\\/]\d\d-[a-z-]+\.md$/.test(f))) {
  const title = fs.readFileSync(f, 'utf8').split('\n')[0].replace(/^# /, '');
  const n = parseInt(path.basename(f), 10);
  if (!title.startsWith(`${n}. `)) problem(`title number   ${path.relative(root, f)}: "${title}"`);
  chapterTitle.set(path.basename(f), title);
}
for (const f of files) {
  for (const m of fs.readFileSync(f, 'utf8').matchAll(/\[(\d+)\. ([^\]]+)\]\(([^)#]*?)(\d\d-[a-z-]+\.md)\)/g)) {
    const title = chapterTitle.get(m[4]);
    if (title && `${m[1]}. ${m[2]}` !== title) problem(`chapter label  ${path.relative(root, f)}: ${m[0]} (title is "${title}")`);
  }
}

// llms.txt points agents at raw files by URL, which the link check above never sees.
const RAW = 'https://raw.githubusercontent.com/wmacevoy/software-engineering/main/';
for (const m of fs.readFileSync(path.join(root, 'llms.txt'), 'utf8').matchAll(/\]\(([^)]+)\)/g)) {
  if (!m[1].startsWith(RAW)) problem(`not a raw link llms.txt: ${m[0]}`);
  else if (!fs.existsSync(path.join(root, m[1].slice(RAW.length)))) problem(`missing file   llms.txt: ${m[0]}`);
}

// Changes are easy to spot only while CHANGELOG.md, the markers, and the copies agree (SE1/U7).
if (!latest) problem('CHANGELOG.md has no "## vX.Y — yyyy-mm-dd" release');
const listed = new Map(); // "v1.1 New" -> Set of IDs
let release = null, kind = null, total = 0, base = null;
for (const line of changelog.split('\n')) {
  const r = line.match(RELEASE);
  if (r) { release = r[1]; kind = null; continue; }
  const k = line.match(/^### (New|Changed|Also changed)$/);
  if (k) { kind = k[1]; continue; }
  const count = line.match(/· (\d+) principles$/);
  if (count && release === releases[releases.length - 1]) base = Number(count[1]);
  const item = line.match(/^- \[SE1\/([A-Z]\d+)\]\(/);
  if (!item || !release || (kind !== 'New' && kind !== 'Changed')) continue;
  const key = `${release} ${kind}`;
  if (!listed.has(key)) listed.set(key, new Set());
  listed.get(key).add(item[1]);
  if (kind === 'New') total++;
}
for (const [id, mk] of marker) {
  if (!releases.includes(mk.release)) problem(`unknown release ${id}: *${mk.kind} in ${mk.release}.*`);
  else if (!listed.get(`${mk.release} ${mk.kind}`)?.has(id)) problem(`not in CHANGELOG ${id}: *${mk.kind} in ${mk.release}.* has no entry under ${mk.release} / ${mk.kind}`);
}
for (const [key, ids] of listed) {
  const [rel] = key.split(' ');
  for (const id of ids) {
    const mk = marker.get(id);
    if (!definedIn.has(id)) problem(`unknown ID     CHANGELOG.md ${key}: ${id}`);
    else if (!mk || newer(mk.release, rel) < 0) problem(`no marker      ${id}: CHANGELOG lists it under ${key}, but its heading has no *New/Changed in ${rel}* or later`);
  }
}
if (base !== null && base + total !== definedIn.size) problem(`principle count ${definedIn.size} = ${base} in ${releases[releases.length - 1]} + ${total} New? A new principle is missing from CHANGELOG.md`);
for (const f of ['AGENTS.md', ...files.filter((f) => f.includes(`${path.sep}templates${path.sep}`)).map((f) => path.relative(root, f))]) {
  for (const m of fs.readFileSync(path.join(root, f), 'utf8').matchAll(/software-engineering\/(?:blob|tree)\/(v\d+\.\d+)/g)) {
    if (m[1] !== latest) problem(`stale release  ${f}: links to ${m[1]}, latest is ${latest}`);
  }
}
const agents = fs.readFileSync(path.join(root, 'AGENTS.md'), 'utf8').match(/This copy is from \*\*(v\d+\.\d+)\*\*/);
if (!agents || agents[1] !== latest) problem(`stale release  AGENTS.md: says it is from ${agents ? agents[1] : 'nothing'}, latest is ${latest}`);

const readme = fs.readFileSync(path.join(root, 'README.md'), 'utf8');
for (const line of headings) if (!readme.includes(line)) problem(`README index out of date: ${line}`);

console.log(`${files.length} files, ${definedIn.size} principles, ${problems} problems`);
process.exit(problems ? 1 : 0);
