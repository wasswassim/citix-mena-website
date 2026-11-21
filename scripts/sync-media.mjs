// Mirrors the committed web deliverables (media/web) into public/media so Next.js can serve them.
// media/web stays the single source of truth; public/media is git-ignored and rebuilt on every run, so a file
// removed from media/web is no longer served.
import { cpSync, existsSync, rmSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const src = join(root, "media", "web");
const dest = join(root, "public", "media");
if (existsSync(src)) {
  rmSync(dest, { recursive: true, force: true });
  cpSync(src, dest, { recursive: true, filter: (p) => !p.endsWith(".gitkeep") });
  console.log("media/web -> public/media");
}
