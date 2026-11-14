# How the R3 camel scene was made (for Claude AI)

Date: 14 Nov 2026 · Result: `media/hero_orbit/seedance/R3_ref.mp4` (8 s, 720p, 16:9, no audio) · Cost: $1.702

## The idea in one line
Use code for the camera and Seedance for the look. A plain 3D render made in code supplies the exact orbit geometry. The approved still supplies the photoreal look and content. Seedance 2.0 in **reference-to-video** mode combines the two.

## Why this route
- Earlier tests in Kling 4.0 and Seedance image-to-video, which start from a black frame and end on the still, could not follow the orbit from text. The camera pushed in, flew in from far away, slowed down or stopped.
- A pure code 3D orbit (three.js) gave perfect geometry, but code-built content (the falcon) looked pasted on, and Wassim rejected that mix.
- The fix: Seedance copies the *camera* from a code-rendered video and the *look* from the approved still. On R1 (Tom + falcon) this gave a much better orbit. The remaining push-in and pull-back of about 7 % were then removed with our own lock script, `scripts/orbit_lock.py`.

## Step 1: camera reference video (built by us, no credits)
- **Tool:** `components/OrbitLab.tsx`, a three.js lab page at `/en/orbit-lab?ref=1&product=glass`.
  - `ref=1` turns off the content and the on-screen overlay.
  - `product=glass` swaps Tom for a 3 m frameless glass panel.
- **Geometry:** the panel sits at the centre of a circle. The camera moves on that circle:
  - radius 15 m, at a fixed height, always aimed at the panel (look-at height 1.9 m);
  - constant speed of 8.5°/s, starting at 82°;
  - the panel's frame position is held with a lens shift, so it stays at about 2/3 of the frame width and the same size in every frame.
- **Timing:** a black dune covers the lens at the start and slides away. Another dune covers the lens at the end.
- **Rendering:** headless Microsoft Edge took 192 screenshots (8 s × 24 fps, 1280×720). ffmpeg joined them into `media/hero_orbit/lab/orbit_reference_R3_8s.mp4` (H.264).
- This is our own render. Nothing from bluesqx.com was used: their video was only studied for motion, never uploaded or reused.

## Step 2: look reference (already approved)
- `media/hero_orbit/stills/R3_16x9_v3.png`, the approved still from Marketing Studio Image:
  - a frameless clear glass panel on moonlit dunes, with a faint cool-white edge glow;
  - misty jagged mountains inside the glass, and the camel.

## Step 3: Seedance 2.0 call (Higgsfield API)
- **Model:** `bytedance/seedance-2.0/reference-to-video`
- **Script:** `scripts/orbit_seedance.py`, job `ref3`. It calls our client `scripts/higgsfield.py` (key read from `.env`, never printed).
- **Parameters:**
  - `image_urls` = [R3 still]
  - `video_urls` = [camera reference video]
  - `duration` 8, `resolution` 720p, `aspect_ratio` 16:9, `generate_audio` false
- **Price:** $0.2128/s (720p with video input) × 8 s = $1.702. The script checks the free `/estimate` endpoint first and refuses above the approved budget or the $40 cap in `.env`.
- **Prompt.** Writing approach:
  - The video is used ONLY for the camera, and the image ONLY for the look.
  - The action happens WHILE the camera orbits.
  - Each error seen in the R1 test is forbidden by name: push-in, mid zoom, pull-back, drift.

  Full prompt:

> Use the reference video ONLY for the camera: copy its camera path and its framing exactly. In it the camera travels along a circle around an upright square panel at a fixed radius and a fixed height, always aimed at the panel, at one constant speed. The panel stays at exactly the same position in the frame and at exactly the same size in every frame, from the first frame it is visible to the last; only its angle changes, from almost edge-on to a three-quarter view. The camera never moves closer, never moves away and never drifts sideways: no push-in at the start, no zoom in the middle, and NO pull-back before the end. Keep the timing too: the shot starts in darkness behind a black sand dune close to the lens, the dune slides away, and at the end another black dune slides across the lens while the panel is still at full size, and the shot ends in darkness. Do not copy the reference video's plain look. Use the reference image for the look, the object and the content: photorealistic cinematic night, very dark and low-key, a black void over desert sand dunes, cool slate-blue grading. The object is a frameless, perfectly clear square glass panel standing upright on the sand, a few centimetres thick, with a faint cool-white glow along its thin edges (white, not cyan), exactly as in the image. Inside the glass is a deep, misty night view of jagged rocky mountains; the glass is the only light, and a soft shaft of cool light and low mist spill from it onto the sand. Action, happening WHILE the camera orbits, never after it: a dromedary camel (one hump, no saddle, no harness, no rider) is first seen small and far away deep inside the mountain scene, walks forward toward the glass, its head and long neck pass through the glass surface, then its chest and front legs, then its whole body, and it steps out onto the sand and keeps walking calmly out of the frame, with a natural gait and exactly four legs. Mist flows out through the glass with it and spreads low over the sand. The camel clearly comes from inside the glass. The glass panel is a rigid, flat sheet that never changes shape and never gets a frame. No slow-down, no pause. No text, logos, people or buildings.

## What was NOT done to this clip
- **No correction:** the R1 lock script was not run.
- **No measurement or grading:** the file is raw from Higgsfield, at Wassim's request.

## Spend
- Project total after this clip: **$19.53 of the $40 cap**.
- Full log: `docs/higgsfield-map.md`.

## Reusable for R2, R4, R5
Same three steps for each:
1. Render a camera reference from OrbitLab, adding a product mode per object.
2. Use the approved still as the look reference.
3. Run Seedance reference-to-video with a prompt in the same structure.
