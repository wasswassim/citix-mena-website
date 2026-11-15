# CITIX MENA — Hero "The Orbit" RUNBOOK v5 (for Claude Code)

Updated 14 Nov 2026, 18:30, by Claude (claude.ai project "CitiX MENA Internship").
This file is the single source of truth for the hero build. It **replaces runbook v4.2**: the Tom, Jerry, Baloo and Jumbo rotations and the Kling first/last-frame method are dropped.

## Decision (Wassim, 14 Nov evening)
The R3 camel clip is the model for the whole hero:
- clip: `media/hero_orbit/seedance/R3_ref.mp4`
- method: `docs/planning/R3_camel_method.md`

The hero becomes **4 scenes, all made exactly like R3**:
- the same frameless glass panel;
- the same camera reference video (identical orbit);
- the same look (night dunes, slate-blue grade, cool-white edge glow);
- the same Seedance 2.0 reference-to-video call;
- the same prompt structure.

Only the content inside and coming out of the glass changes.

| Order in loop | Scene | Content | Status |
|---|---|---|---|
| 1 | Oasis | Water and palms spill out of the glass | to make |
| 2 | Camel (current R3) | Mountains inside, a dromedary walks out | **DONE, approved** (`R3_ref.mp4`) |
| 3 | Perfume (CITIX promo style) | An unbranded bottle floats out with rose petals | to make |
| 4 | SUV (finale) | An unbranded SUV bursts out and drifts; dust hits the lens | to make |

**Loop:** 4 × 8 s = **32 s**. Every scene starts and ends on black (the dune wipe), so the joins are invisible and the loop restarts at scene 1. This matches bluesqx (31.2 s).

The products (Tom, Jerry, Baloo, Jumbo) leave the hero. They will be shown in the Smartboards section (S4) with real assets. Keep all earlier stills and clips; archive them and delete nothing.

## How to run
- Run the phases P0 → P5 in order, autonomously.
- Stop **only** at the gates marked **⛔ GATE**. At a gate, open what Wassim needs to see on his screen, give him the local paths and the exact cost, then wait for his reply.
- Do every step yourself (files, git, ffmpeg, the OrbitLab renders, opening previews). Never ask Wassim to do a manual step you can do.
- After each phase: commit, then print a 5-line status: phase done · spend so far · cap · next gate · anything blocked.

## Hard rules (always)
- **Secrets:** never print, log or commit the Higgsfield key or `.env`. Spend credits only after an explicit "OK" on an exact quote (use the free `/estimate` first). Never exceed `HIGGSFIELD_MAX_SPEND_USD` ($40). Spend to date: **$19.53**.
- **Files:** delete or overwrite nothing; archive instead. Copy originals, never move them.
- **Brand:**
  - No warm/yellow cast outside the glass, no neon, no sci-fi.
  - No landmarks, people, text, or third-party logos/brands.
  - Vehicles and products unbranded; no real car-model replica.
- **bluesqx.com** is for study only. Never upload, copy or reuse their frames or video.
- **Model routing:**
  - Fable 5: prompts and creative/technical decisions.
  - Sonnet sub-agents: boilerplate only. They never touch `.env` or Higgsfield.
- **Creative freedom:** you may improve wording and technical details if a test shows it helps. You may not change the approved content, the R3 look, or these rules.
- **What "exactly like R3" means:**
  - the same camera reference file: `media/hero_orbit/lab/orbit_reference_R3_8s.mp4`;
  - the same panel, look and grading as `R3_16x9_v3.png`;
  - the same parameters: 8 s, 720p, 16:9, no audio;
  - the same prompt structure: camera block, then look block, then content block, then the action WHILE the camera orbits, then the forbidden errors by name.
  - Run no lock script and no grading on the raw clips unless Wassim asks.

---

## P0 — Sync (no credits)
1. Copy this runbook to `docs/planning/HERO_ORBIT_RUNBOOK.md`, keeping the old version as `HERO_ORBIT_RUNBOOK_v4.2_archived.md`.
2. Update `CLAUDE.md`:
   - Add "Current hero plan: v5, 4 glass-panel scenes".
   - Move the v4.2 rotations to the Archived section.
3. Move nothing. Create `media/hero_orbit/v5/` for all new outputs.
4. Commit "hero v5: 4 glass-panel scenes on the R3 method".

## P1 — 3 look stills (Marketing Studio Image, 16:9 1920×1080)
- Use `media/hero_orbit/stills/R3_16x9_v3.png` as the image reference in all three. The panel, its size and position, the camera angle, the dunes, the darkness and the grading must match R3. Only the content changes.
- Show the content at its most striking moment, partly through the glass.

| Still | Inside the glass | What is coming out |
|---|---|---|
| **S1 oasis** | A moonlit desert oasis: a dark, still pool fringed by date palms. | A smooth sheet of water pours forward through the glass surface onto the sand. Date palm fronds push out through the glass. Low mist. |
| **S3 perfume** | A deep pink-red haze with drifting rose petals. Only the inside of the glass is pink-red; the outside world stays cool slate-blue. | A tall, faceted clear-glass perfume bottle with a heavy glass stopper, no label, logo or text, halfway through the glass surface. Rose petals and pink mist spill out with it. |
| **S4 SUV** | A dark desert track between dunes at night. | A dark, generic luxury full-size SUV bursts out of the glass front-first, headlights on, sand spraying. It is not any real model: no badges, no grille emblem, no plates. The glass is intact, with no shattering or cracks. |

Steps:
1. Write the 3 prompts in `docs/higgsfield-map.md` (v5 section).
2. ⛔ **GATE 1:** quote the cost (1 variation each), wait for "OK", then generate into `media/hero_orbit/v5/stills/`.
3. Build a sheet with R3 v3 next to the 3 new stills and open it on screen.
4. Wassim approves or asks for rerolls. Show the cost of each reroll first.

## P2 — 3 Seedance clips (exactly the R3 call)
- **Model:** `bytedance/seedance-2.0/reference-to-video`, via `scripts/orbit_seedance.py`, with new jobs `s1_oasis`, `s3_perfume` and `s4_suv`.
- **Inputs:** `image_urls` = [the approved still], `video_urls` = [`orbit_reference_R3_8s.mp4`].
- **Parameters:** 8 s, 720p, 16:9, `generate_audio` false.
- **Expected cost:** ≈ $0.2128/s × 8 s × 3 = **$5.11**.
- **Prompt:** keep the R3 prompt word for word up to and including "…a soft shaft of cool light and low mist spill from it onto the sand." Make one change inside that part: replace the sentence "Inside the glass is a deep, misty night view of jagged rocky mountains;" with the scene's "Inside the glass" line below. Then append the scene's action block and the closing line.

**S1 oasis**
- *Inside the glass:* "Inside the glass is a moonlit desert oasis: a dark, still pool of water fringed by date palms, seen from inside the scene;"
- *Action:* "Action, happening WHILE the camera orbits, never after it: the pool starts to ripple, then a smooth sheet of clear water flows forward and pours out through the glass surface as if the glass were the edge of the pool, spilling onto the sand in a low wave that spreads across the dunes and darkens the sand, catching the cool light. Date palm fronds push out through the glass and sway gently outward. Fine mist and a few drops follow the water. The water clearly comes from inside the glass."

**S3 perfume**
- *Inside the glass:* "Inside the glass is a deep pink-red haze with slowly drifting rose petals; the pink-red light stays inside the glass, everything outside stays cool slate-blue;"
- *Action:* "Action, happening WHILE the camera orbits, never after it: one tall faceted clear-glass perfume bottle with a heavy glass stopper, no label, no logo, no text, is first seen small and far away deep inside the pink haze, floats forward toward the glass, passes through the glass surface stopper first, comes fully out and hovers just in front of the panel, turning slowly, catching the light. A soft burst of rose petals and pink mist follows it out through the glass and drifts low over the sand. Exactly one bottle; it is rigid and keeps its shape. The bottle clearly comes from inside the glass."

**S4 SUV (finale)**
- *Inside the glass:* "Inside the glass is a dark desert track between dunes at night;"
- *Action:* "Action, happening WHILE the camera orbits, never after it: a dark luxury full-size SUV with its headlights on is first seen small and far away inside the glass, drives fast toward the glass, bursts out through the glass surface front first, lands on the sand outside, and swings into a controlled sideways drift across the frame toward the camera; its four wheels throw a big spray of sand and dust toward the lens, and the dust cloud fills the lens just before the black dune slides across it. The SUV is a generic design, not any real model: no badges, no logos, no grille emblem, no number plates, exactly four wheels, a consistent body. The glass panel stays intact: no shattering, no cracks, no fragments. The SUV clearly comes from inside the glass."

**Closing line for all three:** "The glass panel is a rigid, flat sheet that never changes shape and never gets a frame. No slow-down, no pause. No text, logos, people or buildings."

Steps:
1. ⛔ **GATE 2:** show the 3 final prompts and the `/estimate` total, then wait for "OK".
2. Generate into `media/hero_orbit/v5/clips/`.
3. Make a 3-up review sheet (frames every 1 s) and open each clip on screen.
4. Wassim approves or asks for rerolls. Show the cost of each reroll first.

## P3 — Loop assembly (no credits)
1. Order: S1 oasis → S2 camel (`R3_ref.mp4`) → S3 perfume → S4 SUV. Hard cuts on black; add a 2–4 frame crossfade only where a flash is visible.
2. Check the loop is seamless: run a pixel diff between the first and last frames and report the value.
3. Export to `media/web/hero/`:
   - `orbit_16x9.mp4`: H.264, preset veryfast, faststart, no audio, ≤ 8 MB.
   - `orbit_16x9.webm`: VP9.
   - `orbit_16x9_poster.webp`: the S1 oasis still, ≤ 150 KB.
4. Write `timing.json` with each scene's start/end and the exact second the S4 dust fills the lens. The code dust overlay syncs to this moment.
5. Open the loop on screen. ⛔ **GATE 3:** Wassim approves.

## P4 — Mobile 9:16 (decide at the gate)
- **Option A (free):** centre-crop the 16:9 loop for mobile, as bluesqx does. Check that the panel and the content stay in frame.
- **Option B (≈ $7 for 4 clips, plus stills):** render a 9:16 camera reference in OrbitLab and re-run the 4 scenes at 9:16 with the same prompts.
- Build Option A first, open it on screen, then ⛔ **GATE 4:** Wassim chooses A or B.

## P5 — Hero code
- Update the hero to use the new loop, `timing.json` and the SUV dust overlay (synced to S4).
- Keep the H1, CTAs, 35-logo marquee, EN/AR, reduced motion, LCP rules and everything else already built.
- Serve locally, open it on screen, commit and push. ⛔ **GATE 5.**

**Budget for v5:**
- Stills ≈ $1–1.5.
- Clips ≈ $5.11.
- Rerolls ≈ $3–5.
- Total ≈ **$9–12**, giving a project total of ≈ $29–32 of the $40 cap.
- Option B mobile adds about $7–8.
