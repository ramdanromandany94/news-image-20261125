// main.ts — news-image-20261125 ("The World in One Image")
//
// Agent-authored entrypoint for the make.fun news-image-20261125 bounty.
// The rendered front page (entry.png) is produced by tools/render.py and
// ships next to this file. This script only copies it to the grader's
// output directory — it does not generate, fetch, or modify anything.
//
// Grader-safe lookup: the grader runs `node /bot/main.ts` with NO
// MAKEFUN_INPUT_DIR set and a working directory that is NOT /bot, so the
// entry image is resolved in this order:
//   1. $MAKEFUN_INPUT_DIR/entry.png
//   2. $MAKEFUN_BOT_DIR/entry.png
//   3. the directory this file lives in (import.meta.url)
//   4. the current working directory ("./entry.png")
// The output always goes to $MAKEFUN_OUTPUT_DIR/entry.png.

import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const IMAGE_NAME = "entry.png";

function firstExisting(candidates: string[]): string | null {
  for (const candidate of candidates) {
    if (existsSync(candidate)) return candidate;
  }
  return null;
}

function main(): void {
  const here = dirname(fileURLToPath(import.meta.url));
  const inputDir = process.env.MAKEFUN_INPUT_DIR;
  const botDir = process.env.MAKEFUN_BOT_DIR;

  const candidates: string[] = [];
  if (inputDir) candidates.push(join(inputDir, IMAGE_NAME));
  if (botDir) candidates.push(join(botDir, IMAGE_NAME));
  candidates.push(join(here, IMAGE_NAME));
  candidates.push(join(process.cwd(), IMAGE_NAME));

  const source = firstExisting(candidates);
  if (!source) {
    throw new Error(
      `entry.png not found in any of: ${candidates.join(", ")}`
    );
  }

  const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? process.cwd();
  mkdirSync(outDir, { recursive: true });
  const dest = join(outDir, IMAGE_NAME);
  copyFileSync(source, dest);
  console.log(`copied ${source} -> ${dest}`);
}

main();
