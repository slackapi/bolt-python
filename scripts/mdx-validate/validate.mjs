#!/usr/bin/env node
// CI-only ground-truth validation for the generated API reference.
//
// The docs site (docs.slack.dev, Docusaurus v3) compiles every .md page as MDX
// with acorn. This script runs that exact compiler over the committed reference
// tree, so "does compile() throw?" is precisely "will the docs build choke?".
// It replaces the approximate regex hazard check that used to live in
// scripts/generate_api_docs.py. Node stays entirely in CI -- it is not part of
// local dev or the Python test suite.
//
// The committed tree is validated directly; the separate "Reference docs drift"
// CI job already guarantees that tree matches what generate_api_docs.py emits.
import { readFileSync, readdirSync } from "node:fs";
import { join, relative } from "node:path";
import { fileURLToPath } from "node:url";

import { compile } from "@mdx-js/mdx";
import remarkDirective from "remark-directive";
import remarkFrontmatter from "remark-frontmatter";
import remarkGfm from "remark-gfm";

const repoRoot = fileURLToPath(new URL("../..", import.meta.url));
const referenceDir = join(repoRoot, "docs", "english", "reference");

// Mirror Docusaurus v3's Markdown pipeline so the check matches the real build
// and does not raise false positives: MDX format, GFM, admonition directives
// (:::note), and YAML frontmatter (every generated page leads with a --- block).
const options = {
  format: "mdx",
  remarkPlugins: [remarkFrontmatter, remarkGfm, remarkDirective],
};

const files = readdirSync(referenceDir, { recursive: true })
  .filter((name) => name.endsWith(".md"))
  .map((name) => join(referenceDir, name))
  .sort();

let failures = 0;
for (const file of files) {
  const source = readFileSync(file, "utf8");
  try {
    await compile(source, options);
  } catch (error) {
    failures += 1;
    const at = error.line != null ? `:${error.line}:${error.column ?? 0}` : "";
    console.error(`✗ ${relative(repoRoot, file)}${at}: ${error.message}`);
  }
}

if (failures > 0) {
  console.error(`\nMDX validation failed for ${failures} of ${files.length} reference page(s).`);
  process.exit(1);
}
console.log(`MDX validation passed for ${files.length} reference page(s).`);
