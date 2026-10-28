// Shared by tools/check.js and tools/since.js: what a principle's heading and marker look like, and
// what counts as its text. One place, so the two tools can never disagree about it.
const HEADING = /^### <a id="([a-z0-9]+)"><\/a>([A-Z]\d+)\. (.*)$/;
// The marker is the first paragraph under a heading. New/Changed is a person's claim that the
// release changed the principle's meaning; Since is written by tools/since.js when no such claim
// exists. Each carries the release's date, and, when the wording moved later without the meaning,
// the text's own since. tools/since.js writes and checks them against the release tags.
const MARKER = /^\*(New|Changed|Since) (?:in )?(v\d+\.\d+(?:\.\d+)?)(?: \((\d{4}-\d{2}-\d{2}|unreleased)\))?(?:; text since (v\d+\.\d+(?:\.\d+)?) \((\d{4}-\d{2}-\d{2}|unreleased)\))?\.\*$/;
// A principle's text: its heading to the next heading or horizontal rule, without its marker,
// whitespace collapsed so rewrapping is not a change. The rule matters: the `---` after a chapter's
// last principle is not its text, or adding a principle after it would "change" it (v1.2's A10).
function bodies(text) {
  const out = new Map();
  let id = null, buf = [];
  const flush = () => { if (id) out.set(id, buf.filter((l) => !MARKER.test(l)).join(' ').replace(/\s+/g, ' ').trim()); };
  for (const line of text.split('\n')) {
    const m = line.match(HEADING);
    if (m || /^#{1,3} /.test(line) || line === '---') { flush(); id = m ? m[2] : null; buf = []; }
    if (id) buf.push(line);
  }
  flush();
  return out;
}
module.exports = { HEADING, MARKER, bodies };
