# bluesqx.com hero loop — motion study (H1 step 0)

Studied 14 Nov 2026 from https://www.bluesqx.com/ (hero background video, 1280×720, 30 fps, 31.2 s, about 4.5 MB, muted, looped, lazy-loaded behind a poster).
Method: one frame every 0.5 s (62 frames) saved to `C:\Users\wassi\scratch\bluesqx_study\` — outside the repo, never committed, never reused. Everything below is described in our own words; we take the *principles*, not their footage, code, images or text.

## 1. Structure and timing
- Two scenes, each shown twice with small variations, so the 31 s loop feels longer than it is:
  - **Scene A, "world in the panel"** (≈ 0.5–9.5 s and 16.5–24.5 s): about 8–9 s.
  - **Scene B, "empty glowing frame"** (≈ 10–15.5 s and 25–30.5 s): about 5–6 s.
- Inside a scene there are no cuts. Beats: reveal ≈ 1.5 s → slow growth and hold ≈ 5–6 s → wipe out ≈ 1 s. About 0.5–1 s of true black sits between scenes.
- The loop point is black, so the restart is invisible.

## 2. Composition and scale
- The panel is **small**: roughly 35–45 % of the frame height, sitting right of centre (about two-thirds across). It never fills the frame.
- More than half of every frame is pure black. The left half stays empty for the headline; the bottom strip stays dark for the logo row and buttons.
- The floor is not "lit scenery": it only exists where the panel's light falls on it.

## 3. How the content breaks the screen plane
- It does **not** jump at the camera. The panel is treated as a doorway into a deep world: inside it there is real depth (near plants, mid trees, far haze) that shifts with the camera.
- The world then **leaks out at the base**: plants appear on the floor at the foot of the panel, first a few, then a widening bed that ends up about 1.5 panel-widths wide, always on the side the light falls.
- A soft **shaft of light** pours out of the panel through haze and lands on the floor; small motes drift in it. The spill of light is what sells the 3D, more than any object crossing the glass.
- Growth is gradual and continuous over the whole hold, so the picture is never static even though the camera move is small.

## 4. Depth, scale and parallax
- The panel starts **edge-on** (a thin bright sliver) and opens to about three-quarter view as the camera travels; at the end it closes back toward edge-on. The foreshortening change is the main depth cue.
- Inner world and outer floor move at different rates (parallax): the far background inside the panel barely moves, the floor plants slide noticeably.
- The panel's thin dark side face stays visible most of the time, which keeps it reading as a physical object.

## 5. Camera
- One slow, constant-speed orbit in one direction for the whole loop (roughly 60–70° around the panel per scene), slightly low, with a very gentle push-in. No shake, no zooms, no cuts.

## 6. Dark wipes
- Scene changes are hidden by a **dark foreground shape** (a hill/rock silhouette close to the lens) sliding diagonally across the frame as the camera orbits. The frame goes black, and the next scene appears from behind the same kind of silhouette.
- So the wipe belongs to the world (terrain passing the lens), not to a graphic transition and not to the panel itself.

## 7. Light, particles, floor
- The panel is the only light source. No sky, no moon, no ambient fill.
- Each scene keeps **one colour family** (scene A green-yellow, scene B a single blue), which makes the scene change read clearly.
- Floor: dark, slightly rough; lit in a soft pool near the panel with fast fall-off; faint haze just above it.
- Particles are tiny and sparse (dust motes in the beam), never a storm.

## 8. Grading
- Very low-key: crushed but clean blacks, high contrast, heavy natural vignette, saturated only inside the light pool.

## What we take from it (and what we don't)
| Principle | Applied to the CITIX orbit |
|---|---|
| Small subject, lots of black, right of centre | Product ≈ 50 % of frame height at ~2/3 across in 16:9; left half near-black for the H1. Our v1 stills had products at 70–90 % height. |
| Screen = only light; floor exists only in the spill | Dunes almost invisible: faint moon rim on the crests + the screen's light pool. Our v1 dunes were evenly moonlit. |
| Content leaks out at the base and spreads | Each rotation gets a ground-level spill (sand fan, wet sand and shoots, mist, petals, tyre tracks) in addition to its hero subject. |
| Light shaft + sparse motes | Volumetric beam through thin haze with fine sand motes in every still. |
| Edge-on → 3/4 → edge-on | Stills are shot about 40° off the screen's front with the thin side visible, so clip A can open from edge-on and clip B can close. Our R1 v1 was almost frontal. |
| One colour family per scene | R1 cool white-blue, R2 teal-green, R3 slate-blue mist, R4 crimson, R5 cool white. |
| Terrain silhouette wipes | Clips: a dark dune crest crosses the lens to black (proposed instead of "the product's body sweeps the lens"; first/last frames stay black, so the runbook's joins are unchanged). |
| ≈ 8 s per scene, constant orbit | Matches our 4 s + 4 s per rotation. A: 0–1 s crest clears and the panel opens; 1–4 s growth to the still. B: 0–3 s the content completes its exit; 3–4 s crest wipe. |

Not taken: the cyan neon frame (brand rule: no neon; R3/R4 keep a faint white edge), their forest content, their exact framing, any asset.
Kept from our plan and not in theirs: a hero subject that clearly leaves the screen (falcon, camel, bottle, SUV), the R5 sand hitting the lens, moonlit-desert world, Pulse Red accents.

## Correction (14 Nov 2026, after Wassim's review)
Limits of this study: it was made from **still frames** (one every 0.5 s), not by watching the video play. Motion was inferred, and sections 4 and 5 got one thing wrong.

Measured on the frames of the "empty frame" scene (1280 px wide):
- Panel **height** stays 276 → 265 px over 4 s (about 4 %), until the wipe covers it.
- Panel **centre** moves only 760 → 790 px (about 2 % of the frame width).
- Panel **width** shrinks steadily 247 → 103 px, about 28 px per second, at an even rate.

So the subject is **locked in the frame**: same place, same distance, same size, and only its angle changes at a constant rate, as if the product stood on a slow turntable (a camera circling at a fixed radius while aimed at it gives the same picture). There is **no push-in** and no sideways travel of the subject; what slides past is the foreground terrain. Sections 4–5 above should be read with that correction.

Our R1_A test did not do this: Tom drifted from 48 % to 66 % of the frame width while turning. Fixes: (1) clip prompts now state the turntable lock (fixed position, distance and size; no push-in, pull-back or drift); (2) in the edit the product can also be pinned in place by tracking its screen and shifting each frame (no credits).
