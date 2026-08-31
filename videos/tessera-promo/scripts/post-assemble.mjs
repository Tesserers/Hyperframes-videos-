#!/usr/bin/env node
// post-assemble.mjs — three repairs assemble-index.mjs cannot make itself.
// Run after EVERY `assemble-index` + `transitions inject`; each failure it fixes
// is silent rather than loud, which is exactly why it needs to be automatic.
//
//   1. GSAP. The assembler writes a jsdelivr <script> tag, and that CDN is blocked
//      by this environment's egress policy: the render browser fails with
//      ERR_TUNNEL_CONNECTION_FAILED and every timeline dies. Point it at the
//      vendored copy under assets/vendor/.
//
//   2. Background plates. The assembler's approved-video hoist is DESTRUCTIVE —
//      it lifts the <video> out of the frame file and leaves a comment behind, so
//      the next assemble finds nothing to hoist and the footage disappears with no
//      error at all. (A cut shipped that way once.) So the plates are declared here
//      instead, as the single source of truth, and injected on every run.
//
//   3. Compositing order. Media appended after the scene wrappers paints OVER them,
//      because ordering here follows DOM position and not data-track-index — a
//      full-bleed plate then hides the very scene it should sit behind. Plates go
//      ahead of the first scene wrapper.
//
//   node scripts/post-assemble.mjs

import { readFileSync, writeFileSync } from "node:fs";
import { resolve, dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const INDEX = join(ROOT, "index.html");

// The film's background plates: which scene each sits behind, and its source.
// Timing is read off the assembled scene so it survives any re-cut.
const PLATES = [
  { scene: "el-01-apertura", id: "plate-apertura", src: "assets/media/herobg-open.webm" },
  { scene: "el-07-cierre", id: "plate-cierre", src: "assets/media/herobg-close.webm" },
];

let html = readFileSync(INDEX, "utf8");
const before = html;
const notes = [];

// 1 · vendored gsap
const vendored = html.replace(
  /<script src="https:\/\/cdn\.jsdelivr\.net\/npm\/gsap@[^"]+"[^>]*><\/script>/,
  '<script src="assets/vendor/gsap.min.js"></script>',
);
if (vendored !== html) notes.push("gsap → assets/vendor");
html = vendored;

// 2 · drop anything already emitted for a plate, so re-runs stay idempotent
for (const p of PLATES) {
  html = html.replace(new RegExp(`[ \\t]*<video id="${p.id}"[\\s\\S]*?</video>\\n?`, "g"), "");
}
// and drop the assembler's own hoisted copies, which land in the wrong place
html = html.replace(/[ \t]*<video\b(?![^>]*id="plate-)[\s\S]*?<\/video>\n?/g, "");

// 3 · re-emit each plate with its scene's real timing, above the scene wrappers
const emitted = [];
for (const p of PLATES) {
  const tag = new RegExp(`<div\\s+id="${p.scene}"[^>]*>`, "s");
  const m = html.match(tag);
  if (!m) continue;
  const blockStart = html.indexOf(m[0]);
  const block = html.slice(blockStart, html.indexOf("></div>", blockStart));
  const start = (block.match(/data-start="([\d.]+)"/) || [])[1];
  const dur = (block.match(/data-duration="([\d.]+)"/) || [])[1];
  if (start === undefined || dur === undefined) continue;
  emitted.push(
    `      <video id="${p.id}" src="${p.src}" muted playsinline\n` +
      `        class="clip"\n` +
      `        style="position:absolute;left:0px;top:0px;width:1920px;height:1080px;object-fit:cover"\n` +
      `        data-start="${start}"\n` +
      `        data-duration="${dur}"\n` +
      `        data-track-index="1001"\n` +
      `      ></video>`,
  );
}
if (emitted.length) {
  const at = html.search(/[ \t]*<div\s+id="el-[^"]+"/);
  if (at !== -1) {
    const head = html.slice(0, at).replace(/[ \t]*$/, "");
    html = head + "\n" + emitted.join("\n\n") + "\n\n      " + html.slice(at).trimStart();
    notes.push(`${emitted.length} plate(s) mounted under the scenes`);
  }
}

if (html === before) {
  console.log("✓ post-assemble: nothing to repair");
} else {
  writeFileSync(INDEX, html);
  console.log("✓ post-assemble: " + notes.join(" · "));
}
