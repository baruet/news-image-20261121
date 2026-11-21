import { copyFileSync, mkdirSync } from "node:fs";

// Entry program: copy the pre-rendered front page to the output directory.
// No network, no dependencies, deterministic: the same bytes every run.
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "out";
mkdirSync(outDir, { recursive: true });
copyFileSync(new URL("./entry.png", import.meta.url), `${outDir}/entry.png`);
