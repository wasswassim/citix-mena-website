# CITIX MENA — Hero "The Orbit" RUNBOOK (for Claude Code)

Written 14 Nov 2026 by Claude (claude.ai project "CitiX MENA Internship").
This file is the single source of truth for the hero build. It replaces the "docs: v4.1" prompt and the intro-film prompts, which are dropped.

## How to run this file
- Execute the phases H0 → H5 **in order**, autonomously.
- Stop **only** at the gates marked **⛔ GATE**. At a gate, show Wassim what he needs to see (open files on his screen + give local paths), then wait for his reply.
- Do everything on the computer yourself (files, folders, git, ffmpeg, `.env` edits, opening previews). Never ask Wassim to do a manual step that you can do.
- After each phase: commit, then print a 5-line status: phase done · spend so far · cap · next gate · anything blocked.

## Hard rules (always)
- **Secrets:** never print, echo, log or commit the Higgsfield key or `.env` contents.
  - When editing `.env`, change only the target line, using a script that does not print the file.
  - The key file `C:\Users\wassi\Desktop\DOCS\Internship\857b9f1a-...txt` must not be read again or copied into the repo.
- **Spending:** spend Higgsfield credits **only** after an explicit "OK" for an exact quote. Never exceed `HIGGSFIELD_MAX_SPEND_USD`.
- **Deleting:** don't delete or overwrite existing files. Archive into a new folder instead. Don't move originals; copy them.
- **Brand:**
  - Colours: black #000/#161616, white #FFF/#E0E0E0, Pulse Red #FD0332 (gradient to #990332). Fonts: Gilroy ExtraBold / Light.
  - No sci-fi, neon or warm/yellow casts; deserts only under moonlight / blue hour. Logo never bottom-right.
  - No owned landmarks (Burj Khalifa etc.), no mosques as subjects, no identifiable people, no third-party logos in generated media.
  - Vehicles unbranded; no Range Rover or other real-model replica.
- **Model routing:**
  - Fable 5.2: writing Higgsfield prompts and hard creative/technical decisions.
  - Opus: everything else.
  - Sonnet sub-agents are allowed for boilerplate, but they never touch `.env` or Higgsfield.
- **Creative freedom:** you may improve prompt wording and technical choices, as long as you keep every rule above.

## Plan summary (v4.2)
- Homepage modelled on bluesqx.com (structure and motion only; no copying of their code, video, images or text).
- Sections:
  1. Hero "The Orbit"
  2. Install / Operate / Create / Measure
  3. Who we serve
  4. Our Smartboards
  5. About + numbers
  6. Projects tabs
  7. Trusted by
  8. Newsletter
  9. Footer
- EN + AR (RTL); inner pages are "Coming soon".
- **Intro film is DROPPED.** Keep all its assets (`media/clips`, `media/hero_cutout`, `media/hero_test`, `media/generated/drafts`), tagged "reusable: products/about/projects sections + inner pages". Delete nothing.
- **Hero rotations (approved):**

| R | Screen | Content bursting out of the screen |
|---|---|---|
| R1 | Tom (old version, real refs, 1:3.5, red side strip) | Falcon flies out toward the camera, sand swirling |
| R2 | Jerry | Oasis: palm fronds and water spill onto the dunes |
| R3 | Plain glass square (ORIGINAL frameless clear panel, faint cool-white edge glow, no cyan outline) | Arabian oryx steps out; mist off Hajar-style mountains |
| R4 | Corner glass pair: TWO of the R3 frameless glass panels joined edge to edge at ~90°, like a screen wrapping a building corner. No tower/spire, no white borders or bezel, no building, no box body | Tall unbranded perfume bottle rises out of the corner seam toward the camera, pink-red light, rose petals and mist |
| R5 | Jumbo (corner screen, two faces) | Unbranded luxury SUV drifts out; sand hits the lens; the dust hits the hero frame (code overlay), then black, then the loop restarts |

- **World:** dark void over moonlit desert dunes, cool blue grading, volumetric light from the screen.
- **Logo marquee + "Trusted by" wall:** use exactly these 35 brands from the citixmena.com "Trusted by leading global brands" section:
  - Sony, Kia, Panasonic, Yokohama, Apple, L'Oréal, Rolex
  - McDonald's, Tiffany & Co., Coca-Cola, Lenovo, Lexus, Lufthansa, Bridgestone
  - Ülker, Mondelēz International, BMW, Red Bull, Kinder, Michelin, Volvo
  - H&M, Kenzo, Sprite, Audi, Hyundai, Samsung, Xiaomi
  - Bosch, Pandora, KFC, Unilever, Lancôme, Visa, P&G
- **Logo rules:**
  - Do NOT add Porsche, Ferrari or Mercedes.
  - Use official SVGs only (citixmena.com's own assets or brand press kits), white monochrome.
  - Never trace or redraw a logo. If a file is unobtainable, use a labelled placeholder and list it.
- **Budget for the hero:** ≈ $22–26. Spend to date: $11.43.

---

## H0 — Setup (no credits)
1. Copy this runbook into the repo as `docs/planning/HERO_ORBIT_RUNBOOK.md`.
2. Update the **repo's own** `CLAUDE.md` (do NOT use `claude_code_kit\CLAUDE.md`, which is the outdated original kit version). Edit it in place:
   - Add a "Current plan: v4.2 (BlueSquareX model)" section at the top with the Plan summary above.
   - **Keep as still valid:** old Tom (refs 01 and 02, red side strip, plain cap; the new calligraphy Tom, refs 03–06, stays on hold), brand rules, hard rules, model routing, scripts, and build standards.
   - **Move to an "Archived: intro film (dropped 14 Nov)" section, not deleted:** the sky-only front-facing end frame, the Shot 2 hard cut, the Shot 5 lower-and-tilt, the intro gate, and the intro budgets. Note that their assets are reusable.
   - Leave `components/IntroGate.tsx` in the code but disconnected from the homepage route. Don't delete it.
3. In `.env`, set `HIGGSFIELD_MAX_SPEND_USD=40`. Do it with a script that edits only that line and prints only "cap updated: 40". Confirm `.env` is still in `.gitignore`.
4. Build `media/hero_orbit/refs/` (copies only):
   - **Tom:** `media/generated/hero_cutout/tom_night.png` and `tom_day.png` (old Tom, option A 1:3.5), plus Tom refs 01 and 02 from `media/source/`. Do not use refs 03–06.
   - **Jerry:** the best 2 Jerry images from `C:\Users\wassi\Desktop\DOCS\Internship\Citix_sales_ver2_comments_maria_last.pdf`.
   - **Baloo:** 3 sharp frames from `C:\Users\wassi\Desktop\DOCS\Internship\Média1pptx_s18_baloo_3d_video.mp4`, with the spire fully visible.
   - **Jumbo:** 3 sharp frames from `C:\Users\wassi\Desktop\DOCS\Internship\Média1pptx_s20_jumbo_3d_video.mp4`, with both corner faces visible.
   - Exclude anything showing the Burj Khalifa, identifiable people, or third-party logos.
5. Make a labelled contact sheet `media/hero_orbit/refs/_refs_sheet.jpg` and open it on Wassim's screen.
6. Commit "hero-orbit: runbook, CLAUDE.md v4.2, spend cap, product refs" (no `.env`).

⛔ **GATE 0:** ask Wassim to approve the references (or swap any).

## H1 — Reveal stills (Marketing Studio Image)
- **Output:** 10 stills, 5 rotations × 16:9 (1920×1080) and 9:16 (1080×1920), 1 variation each, using refs from `media/hero_orbit/refs/`.
- **Shared look:** dark void above moonlit dunes, cool blue night grading, soft volumetric light from the screen onto the sand; camera at a 3/4 angle mid-orbit, cinematic 35 mm, light haze. The product stands alone, its screen is the light source, and the content BREAKS OUT of the screen plane into 3D space.
- **Negatives:** no warm/orange/yellow, neon, sci-fi, landmarks, buildings, people, text, logos or watermarks.
- **Rotation content:** as in the table. R5 SUV is generic: no badges, no grille logo, no plates, not a real model.
- **9:16:** recompose with the product centred and the burst going up and toward the camera. Don't crop the 16:9 version.

Steps:
1. Write the 10 prompts in `docs/higgsfield-map.md` (hero-orbit section).
2. ⛔ **GATE 1a:** quote the exact cost, then wait for "OK".
3. Generate into `media/hero_orbit/stills/R{n}_{16x9|9x16}_v{k}.png`. Check each product against its refs (shape, proportions, colours).
4. Build `_stills_sheet.jpg`, open it on screen, and give the paths.
5. ⛔ **GATE 1b:** Wassim picks or approves stills. Propose rerolls with reason and cost; reroll only after "OK".
6. Commit.

## H2 — Clips 16:9 (Kling 4.0 first/last frame, 1080p, 4 s, no audio)
- Create `media/hero_orbit/wipe/black_16x9.png`: near-black #050608 with a faint dark-blue gradient.
- For each rotation n, make two clips:
  - **Rn_A:** black → approved still. The camera orbits clockwise as the panel's dark edge sweeps off the lens, and the content starts bursting out, reaching the still's pose at the end.
  - **Rn_B:** still → black. The orbit continues clockwise while the content completes its exit (falcon past the lens, water lands, oryx walks out, bottle rises, SUV drifts toward the lens throwing sand). Then the product's dark body sweeps the lens to black.
- **R5_B:** the sand hits the lens, then black.
- Keep the same orbit direction and speed in every clip.

Steps:
1. Write the 10 clip prompts in `docs/higgsfield-map.md`.
2. ⛔ **GATE 2a:** quote the exact cost (10 × 4 s @ 1080p), then wait for "OK".
3. Generate into `media/hero_orbit/clips/16x9/`. Run `scripts/flicker_check.py`. Where a product screen flickers, apply the Tom-lock (composite the clean still over the screen area) plus ffmpeg deflicker.
4. Make a rough 40 s preview `media/hero_orbit/preview/orbit_16x9_preview.mp4` and open it on screen.
5. ⛔ **GATE 2b:** list proposed rerolls with reason and cost; reroll only after "OK".
6. Commit.

## H3 — Clips 9:16
- Same as H2, using the approved 9:16 stills and `black_9x16.png`.
- Output to `media/hero_orbit/clips/9x16/`, preview `orbit_9x16_preview.mp4`.
- Reuse the H2 prompts adapted for vertical framing.
- ⛔ **GATE 3a** (quote) and ⛔ **GATE 3b** (rerolls), then commit.

## H4 — Loop assembly + web encodes (no credits)
For each format (16x9, 9x16):
1. Assemble the 40 s loop R1_A → … → R5_B. Joins fall on black; add a 2–4 frame crossfade only where a cut is visible.
2. Check the loop is seamless: run a pixel diff between the first and last frames and report the value.
3. Export to `media/web/hero/`:
   - `orbit_{fmt}.mp4`: H.264, CRF tuned to ≤ 8 MB desktop / ≤ 5 MB mobile, preset veryfast, faststart, no audio.
   - `orbit_{fmt}.webm`: VP9, same size targets.
   - `orbit_{fmt}_poster.webp`: the R1 reveal frame, ≤ 150 KB.
4. Write `timing.json` with the start/end of each rotation and the exact second the R5 dust hits the lens.
5. Open both MP4s on screen. Commit.

⛔ **GATE 4:** Wassim approves the final loops.

## H5 — Hero section code (no credits)
Use the stack GSAP 3 + ScrollTrigger, Lenis and SplitType, with EN + AR (RTL).
- **Video:** muted, playsinline, loop, autoplay; WebM then MP4. Use the 9:16 file under 768 px wide or in portrait. Show the poster first for LCP and load the video after first paint. With `prefers-reduced-motion`, show the poster only.
- **H1:** two lines in Gilroy ExtraBold / Light, "Smarter Cities." / "Stronger Brands.", plus the Arabic version. SplitType letter reveal.
- **Header:** CITIX logo top-left, "Get in touch", menu button.
- **CTAs:** "Our Solutions" and "Latest Project", bottom-right (bottom-left in RTL). Outline style, white, Pulse Red on hover.
- **Logo marquee:** the 35 brands above as white monochrome SVGs, ~70% opacity (100% on hover), alt text on each. Infinite scroll that pauses on hover; static with reduced motion.
- **Dust overlay:** a canvas/WebGL particle burst over the WHOLE hero, including the text.
  - Triggered by `timing.json` via `requestVideoFrameCallback`, with `timeupdate` as fallback.
  - About 1.2 s burst, then fade; cool-graded sand particles.
  - Off with reduced motion; paused when the hero is off-screen.
- **Quality:** all text is real HTML. Lighthouse mobile targets LCP < 2.5 s and CLS < 0.05; report the scores.
- Serve locally and open desktop and mobile viewports on Wassim's screen. Commit and push to GitHub.

⛔ **GATE 5:** Wassim reviews the hero.

---

## Reusable assets (added in the repo copy, 14 Nov 2026)
The runbook's short paths map to the real folders below. Everything is kept; nothing is deleted. Tag: **reusable: products/about/projects sections + inner pages**.

**Scripts (reuse for the hero orbit)**
- `scripts/higgsfield.py`: API client (upload with cache, free estimate, quote → cap → confirm, status/wait/download). Every hero job goes through it.
- `scripts/flicker_check.py`: luminance stability on a tracked product area. H2/H3 screen-flicker check (box and track logic need adapting per product).
- `scripts/prompt3_edit.py`: ffmpeg/NumPy toolkit: Tom lock (clean still tracked over the clip), deflicker, paint-out, eased scale/position match, dissolves, concat, MP4/WebM/poster exports with size targets. Base for the H2 screen lock and the H4 loop assembly and encodes.
- `scripts/hero_cutout.py`, `scripts/hero_test_render.py`: product cut-outs (transparent PNG/WebP), restores and composite test renders in 16:9 / 21:9 / 9:16.
- `scripts/prompt1_drafts.py`, `scripts/prompt1_s5_regen.py`, `scripts/prompt2_clips.py`: job-runner pattern (job list, budget guard, `--yes`, contact/4-fps sheets) to copy for the H1–H3 runners.
- `scripts/sync-media.mjs` + the Next.js app (`app/`, `components/`, `lib/`): EN/AR routes, RTL, hreflang, video and reduced-motion patterns. The intro gate is archived; the H5 hero replaces it.

**Product references**
- `media/source/01_tom_day_photo.jpg`, `02_tom_night_photo.jpg`: the only Tom refs (old Tom, red side strip).
- `media/generated/hero_cutout/tom_day|tom_night.png/.webp` (option A, 1:3.5), `tom_night_ref.png`: clean old-Tom cut-outs. `archive_body35/` = rejected option B.
- `media/source/baloo_3d_real_4k.mp4`, `jumbo_3d_real.mp4`: same files as the DOCS `Média1pptx_s18/s20` videos.
- `media/source/03–06` (new-Tom calligraphy): **not** for prompts until the company artwork arrives.

**Intro-film media (dropped film, reusable elsewhere)**
- `media/generated/clips/`: Kling Shot 2 / Shot 5 finals (1080p) and drafts with flicker CSVs and 4-fps sheets.
- `media/generated/drafts/`: Marketing Studio stills (hero day/night 16:9 / 21:9 / 9:16, s2_end, s5_start, overlays).
- `media/generated/hero_test/`: hero test renders + `intro_end_frame_reference_1920x1080.png`.
- `media/generated/edit/{16x9,9x16}/`: per-shot renders of the 15 s film.
- `media/web/intro-*.mp4/.webm`, `poster*.jpg`, `end*.jpg`: the finished intro exports.
- `media/stock/`: Pexels clips (Flag Island, etc.) with `LICENSES.md`.
