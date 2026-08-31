#!/usr/bin/env node
// apply-brand.mjs — swap the film's palette (and optionally its typefaces) for
// Tessera's real brand, in one command, across every frame + frame.md + tokens.json.
//
// The film was built without a site capture: this environment's egress policy
// blocks tesseraservices.com (403 on CONNECT), so the colours currently in the
// frames come from the `cobalt-grid` preset, NOT from the brand. Everything
// else — layout, motion, timing, script — is brand-independent, so adopting the
// real brand is a palette/typeface swap, not a rebuild.
//
//   node scripts/apply-brand.mjs --ink "#0B3B2E" --paper "#F5F1E8"
//   node scripts/apply-brand.mjs --ink "#0B3B2E" --paper "#F5F1E8" \
//        --display "Canela" --body "Söhne" --mono "Söhne Mono"
//
// --ink    the brand's single ink: all display type, rules, tesserae, the grid.
// --paper  the ground the film is printed on. Keep it a tinted off-white, never
//          pure #FFFFFF — the preset's whole depth model is paper vs one ink.
// --display / --body / --mono  family NAMES only. A named family must also have
//          a real .woff2 in assets/fonts/ (the render browser is a clean headless
//          Chrome with no system fonts); the script checks and refuses otherwise.
//
// After running: `npx hyperframes check` then `npm run render`.

import { readFileSync, writeFileSync, existsSync, readdirSync } from "node:fs";
import { join, dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const argv = process.argv.slice(2);
const flag = (n, d = null) => {
  const i = argv.indexOf(`--${n}`);
  return i >= 0 && i + 1 < argv.length ? argv[i + 1] : d;
};
const die = (m) => {
  console.error(`✗ apply-brand: ${m}`);
  process.exit(1);
};

const norm = (hex, name) => {
  const m = /^#?([0-9a-fA-F]{6})$/.exec((hex ?? "").trim());
  if (!m) die(`--${name} must be a 6-digit hex colour, got ${JSON.stringify(hex)}`);
  return "#" + m[1].toLowerCase();
};
const rgb = (hex) => [1, 3, 5].map((i) => parseInt(hex.slice(i, i + 2), 16));
// Relative luminance → the preset's readability rests on one high-contrast pair.
const lum = (hex) => {
  const [r, g, b] = rgb(hex).map((v) => {
    const s = v / 255;
    return s <= 0.03928 ? s / 12.92 : Math.pow((s + 0.055) / 1.055, 2.4);
  });
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
};
const contrast = (a, b) => {
  const [hi, lo] = [lum(a), lum(b)].sort((x, y) => y - x);
  return (hi + 0.05) / (lo + 0.05);
};

const ink = norm(flag("ink"), "ink");
const paper = norm(flag("paper"), "paper");
const ratio = contrast(ink, paper);
if (ratio < 4.5)
  die(
    `ink ${ink} on paper ${paper} is ${ratio.toFixed(2)}:1 — below WCAG AA (4.5:1).\n` +
      `  This design has no second colour to fall back on, so a weak pair makes the\n` +
      `  whole film unreadable. Pick a darker ink or a lighter paper.`
  );

const [ir, ig, ib] = rgb(ink);
const gridRgba = `rgba(${ir}, ${ig}, ${ib}, 0.1)`;
const faintRgba = `rgba(${ir}, ${ig}, ${ib}, 0.18)`;

// ── typefaces (optional) ─────────────────────────────────────────────────────
const FAMILY_SLOTS = [
  { flag: "display", was: "Newsreader" },
  { flag: "body", was: "Hanken Grotesk" },
  { flag: "mono", was: "DM Mono" },
];
const fontsDir = join(ROOT, "assets", "fonts");
const fontFiles = existsSync(fontsDir) ? readdirSync(fontsDir) : [];
const families = [];
for (const slot of FAMILY_SLOTS) {
  const to = flag(slot.flag);
  if (!to) continue;
  // A family with no file on disk renders as a silent generic fallback in the
  // MP4 — the one typography failure you cannot see until the render is done.
  const stem = to.replace(/[^A-Za-z0-9]/g, "");
  const hit = fontFiles.some((f) => f.replace(/[^A-Za-z0-9]/g, "").toLowerCase().startsWith(stem.toLowerCase()));
  if (!hit)
    die(
      `--${slot.flag} "${to}" has no .woff2 in assets/fonts/ (found: ${fontFiles.join(", ") || "none"}).\n` +
        `  Drop the file in as ${stem}-400.woff2 first, then re-run — the render browser\n` +
        `  ships no system fonts, so an unbacked family silently falls back.`
    );
  families.push({ ...slot, to, stem });
}

// ── rewrite ──────────────────────────────────────────────────────────────────
const targets = [];
const framesDir = join(ROOT, "compositions", "frames");
for (const f of readdirSync(framesDir).filter((f) => f.endsWith(".html")))
  targets.push(join(framesDir, f));
targets.push(join(ROOT, "frame.md"));

let touched = 0;
for (const path of targets) {
  const before = readFileSync(path, "utf8");
  let s = before;
  s = s.replace(/#f0ebde/gi, paper);
  s = s.replace(/#e6e0ce/gi, paper); // preset's paper-2, unused at frame scale
  s = s.replace(/#1f2be0/gi, ink);
  s = s.replace(/#5560e5/gi, ink); // ink-soft: this film emphasises by opacity
  s = s.replace(/rgba\(31, ?43, ?224, ?0\.10?\)/g, gridRgba);
  s = s.replace(/rgba\(31, ?43, ?224, ?0\.18\)/g, faintRgba);
  for (const fam of families) {
    s = s.replace(new RegExp(`"${fam.was}"`, "g"), `"${fam.to}"`);
    s = s.replace(new RegExp(`${fam.was.replace(/ /g, "")}-`, "g"), `${fam.stem}-`);
  }
  if (s !== before) {
    writeFileSync(path, s);
    touched++;
  }
}

// tokens.json is what `build-frame.mjs` remixes from on any future re-theme.
const tokensPath = join(ROOT, "capture", "extracted", "tokens.json");
const tokens = existsSync(tokensPath) ? JSON.parse(readFileSync(tokensPath, "utf8")) : {};
tokens.title = tokens.title || "Tessera";
tokens.description = tokens.description || "Finanzas y capital humano para pymes";
tokens.colors = [ink, paper];
tokens.fonts = families.length ? families.map((f) => f.to) : tokens.fonts || [];
writeFileSync(tokensPath, JSON.stringify(tokens, null, 2) + "\n");

console.log(`✓ apply-brand: ${touched} file(s) rewritten`);
console.log(`  ink   ${ink}`);
console.log(`  paper ${paper}   (contrast ${ratio.toFixed(2)}:1 — WCAG AA ok)`);
if (families.length) for (const f of families) console.log(`  ${f.flag.padEnd(7)} ${f.was} → ${f.to}`);
console.log(`\n  The index's own ground colour is written by assemble-index.mjs from`);
console.log(`  frame.md, so re-assemble before rendering if you touched the storyboard.`);
console.log(`  Next: npx hyperframes check  &&  npm run render`);
