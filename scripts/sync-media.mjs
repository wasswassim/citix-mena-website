// Copies the committed web deliverables (media/web) into public/media so Next.js can serve them.
// media/web stays the single source of truth; public/media is git-ignored.
import { cpSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const src = join(root, "media", "web");
const dest = join(root, "public", "media");
if (existsSync(src)) {
  mkdirSync(dest, { recursive: true });
  cpSync(src, dest, { recursive: true, filter: (p) => !p.endsWith(".gitkeep") && !p.endsWith("intro-preview.mp4") });
  console.log("media/web -> public/media");
}
