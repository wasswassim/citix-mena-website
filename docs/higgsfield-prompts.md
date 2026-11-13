# Higgsfield prompts — Prompt 1 drafts (stills)

Model: `marketing-studio/image` (2.0 Alpha), 2k, medium quality, `enhance_prompt: false`, one image per request, 2 variations per format. The exact text sent is in `scripts/prompt1_drafts.py`.

## Round 2 — OLD Tom (current)

Status: **approved by Wassim on 2026-11-12 ($1.80), with Tom at about 60% of frame height (16:9, 21:9) and 55% (9:16) in the hero.**

Decisions from Wassim (12 Nov 2026):
- Use the **old Tom** from the real photos (refs 01, 02) with its real red side light strip, until the company sends the calligraphy artwork. **New Tom later.** Refs 04, 05, 06 dropped.
- Top cap plain, no text or logo (real "CITIX MENA" logo composited onto the finals).
- Hero mimics the flyshare.design hero: Tom perfectly front-facing and centred, **sky only**, base touching the bottom edge, room for UI.
- Shot 2 = hard cut after S4 to a street-level push-in. Shot 5 = camera lowers and tilts up from the street until only Tom and sky remain.

### Shared blocks

**[TOM]**

> PRODUCT — reproduce the real object shown in reference images 1 (day) and 2 (night) exactly, do not redesign it: the CITIX "Tom" roadside smartboard, a tall, slim vertical totem about 7 m high and 2 m wide (body width to height about 1 : 3) with a very thin flat profile and a matte black metal body. The front face is almost entirely screen: two stacked portrait screens with rounded corners and very thin black bezels, separated by a thin black gap, the upper screen slightly shorter than the lower one. A small low black cap sits on the top edge, spanning from the middle to the right edge, with one round camera lens at its right end; the cap is completely plain, with no text or logo. The totem stands on a plain matte black rectangular plinth, narrower than the body (about 60% of its width), short (about one sixth of the body height) and flush with the body's right edge. A single thin vertical red LED light strip runs along the right side face of the totem from the cap down to the ground, exactly as in reference image 2. No other parts, text, logos, stickers, antennas or decoration. Ignore the content shown on the screens in the reference images.

**[AVOID]**

> Avoid: warm, orange or yellow tones; neon, acid or oversaturated colours; sci-fi or futuristic styling; abstract CGI look; lens flares, fog, digital noise, clutter; mosques, domes, minarets or famous landmarks; identifiable people; billboards or other signage; any text, lettering, wordmark, logo or brand anywhere in the image, including on the totem's top cap; any pattern, engraving or ornament on the totem; any content, text or image on the screens.

Reference images: 1 = `01_tom_day_photo.jpg`, 2 = `02_tom_night_photo.jpg`. A adds the blue-hour-graded last frame of S4 as image 3 (light and skyline only).

### A — `s2_end` (Shot 2 last frame: street push-in after the hard cut) — 16:9, 9:16

> Photorealistic cinematic photograph at street level, blue hour just after sunset, on a wide palm-lined road in Sharjah, UAE. Reference image 3 is an aerial view of the same district at the same moment: match its cool blue-hour light and colour and show a similar cluster of modern waterfront high-rise towers softly out of focus in the distance. [TOM] It stands on the grass verge beside the road, right of centre (around the right third of the frame), full height visible from the ground to the cap with clear headroom above the cap, seen from the same slight three-quarter angle as in reference image 1. Both screens are switched ON but blank: an even, cool, medium-white glow like a display at 40% brightness (light grey-white, never pure white, not blown out), with no content. The red side light strip is lit. Traffic passes as motion-blurred streaks with white and red light trails; no readable plates, no people. Eye-level camera, 35 mm lens, shallow depth of field. Deep blue sky, clean high contrast, crisp defined artificial light, neutral-cool white balance. [AVOID]

9:16 adds: *Vertical composition: the totem fills about 65% of the frame height, slightly right of centre, the road receding on the left.*

### B — `s5_start` (Shot 5 first frame) — 16:9, 9:16

> Photorealistic cinematic photograph at night on a wide, quiet road in Sharjah, UAE. [TOM] It stands on the roadside, perfectly front-facing, looking straight at the camera, exactly centred horizontally, full height visible from the ground to the cap. Eye-level camera, long lens, vertical edges parallel. The horizon is low: the road, a few palm trees and low-rise modern buildings stay in the lower third of the frame, softly out of focus, with long white and red light trails from passing traffic behind the totem. The upper two thirds of the frame are a clear, deep blue-black night sky with faint, sparse stars. Both screens are switched OFF: pure black glass with only faint reflections. The red side light strip is lit, visible as a thin red line along the totem's right edge. Soft, cool white street light defines the edges of the body. High contrast, clean, neutral-cool white balance. [AVOID]

9:16 adds: *Vertical composition: the totem centred, filling about 60% of the frame height.*

### C — `hero_night` (Shot 5 last frame = hero night state) — 16:9, 21:9, 9:16

> Photorealistic cinematic photograph at night. [TOM] It is perfectly front-facing, looking straight at the viewer, with no three-quarter view, exactly centred horizontally. The camera is low and looks slightly up at it through a long lens, so the vertical edges stay almost parallel. The background is sky only: a clear, deep blue-black night sky with faint, sparse stars, completely empty — no street, no ground, no horizon, no buildings, no trees, no clouds. The totem's full height is visible: the cap near the top with clear sky above it, and the plinth at the bottom, BASE. It must read as a real, heavy object standing on the ground just below the frame, never floating. Both screens are switched ON but blank: an even, cool, medium-white glow like a display at 40% brightness (light grey-white, never pure white, not blown out), with no content. The red side light strip is lit, visible only as a thin red line along the totem's right edge. A faint cool rim light defines the edges of the matte black body. Wide, clean, empty sky on both sides of the totem. High contrast, clean, no noise. [AVOID]

Variation 1 (BASE): *the bottom of the plinth is cut cleanly by the bottom edge of the frame.* Variation 2 (BASE): *the bottom of the plinth dissolves into a soft dark fade in the last few percent of the frame.*

Framing per format: 16:9 and 21:9 — *the totem fills about 60% of the frame height, base at the bottom edge, the top 40% open sky.* 9:16 — *Vertical composition: the totem fills about 55% of the frame height, base at the bottom edge, the top 45% open sky.*

### D — `hero_day` (same framing as C, daytime) — 16:9, 21:9, 9:16

Edit of each `hero_night` draft (image 1 = that draft, image 2 = `01_tom_day_photo.jpg`). Checked with a 50% overlay.

> Edit reference image 1 into the identical scene in daytime. Keep the camera, the framing, the totem's position, scale and every edge, and the way its base meets the bottom of the frame exactly as they are, pixel for pixel. Change only the light and the sky: a clear blue sky with a few soft white clouds, realistic neutral daylight on the matte black body as in reference image 2. Still sky only: no ground, no horizon, no buildings. The screens stay switched ON and blank with the same cool medium-white glow, naturally less bright against daylight. The red side light strip is switched off and barely visible. Clean, realistic, minimal noise. [AVOID]

### Changes from the brief (one-line reasons)

| Change | Reason |
|---|---|
| `s5_start` is front-facing with a low horizon and two thirds sky | It already shares Tom's angle and most of its sky with `hero_night`, so Shot 5 is a small lower-and-tilt move for Kling instead of a change of angle. |
| Red strip lit in `s5_start`, `s2_end` and `hero_night`; off in `hero_day` | Matches ref 02 (lit at night) and ref 01 (not visible by day); it also gives the frame its Pulse Red accent without inventing a part. |
| Hero variations = clean cut at the bottom edge vs soft dark fade | The two options Wassim named for the base; lets him choose from real frames. |
| S4 graded frame kept as image 3 for `s2_end` | Shot 2 is now a hard cut, but the light and skyline should still match the shot before it. |
| Proportions written as numbers in [TOM] | Round 1 came out too slim (about 1 : 3.5) with equal screens; the real Tom is about 1 : 3 with a slightly shorter upper screen. |

### Shot 5 risk assessment (camera lowers and tilts up to the hero frame)

Moderate risk, worth one test. With `s5_start` front-facing and mostly sky, Kling only has to push the street out of the bottom of the frame. The likely failures are leftover palms or lights in the sky and Tom's base drifting. Plan: test it in Prompt 2 with one 720p draft; whatever the result, end the shot with a short dissolve onto the real `hero_night` still so the last frame matches exactly. If Kling warps Tom, use a clean dissolve from `s5_start` to the hero frame instead.

## Round 1 — NEW Tom with calligraphy (archived, 12 Nov 2026)

20 drafts, $2.233, in `media/generated/drafts/round1_new_tom/`. Result: shape close to the refs, but the side calligraphy came out as decorative pseudo-script, not the real pattern; body too slim; screens pure white. This is why the new Tom waits for the company's artwork. The round 1 prompt text is in git history (`scripts/prompt1_drafts.py` before this change).

## Hero Tom cut-outs (local, no API cost) — notes for Prompt 4

Built by `scripts/hero_cutout.py` from the chosen pair `hero_night_16x9_v1` / `hero_day_16x9_v1` (round 2). Files: `media/generated/hero_cutout/tom_night.{png,webp}` and `tom_day.{png,webp}`, transparent, identical canvas, pixel-registered.

- **Proportion (decided 12 Nov 2026): option A.** 7 m × 2 m includes the plinth and cap, so ground-to-cap : width = 3.5 (screen body alone about 1 : 2.85). Option B (body alone 1 : 3.5) was rejected as too narrow; its files are in `hero_cutout/archive_body35/`.
- Steps applied to both frames identically: mask from the day frame, keystone straightened to a true front view, plinth restored to 0.18 of the body height (from ref 01), uniform horizontal scale 0.95. Day only: the pale-blue sky reflection on the right side face was repainted in the body's black.
- **Prompt 4 must do in code:**
  1. **Screens near edge-to-edge.** The generated bezels are thicker than the real Tom's. Draw the screen content slightly larger than the grey screen areas so it covers most of the bezel, like the real product.
  2. **Red strip glow.** The night cut-out's red side strip is cut at the body edge. Add its glow/halo in code (night state only; the strip is off by day).
  3. **Logo.** The cap is plain; composite the real "CITIX MENA" logo.
- Static test renders (`scripts/hero_test_render.py`, placeholder skies): `media/generated/hero_test/`. Tom centred, base on the bottom edge, 60% of frame height on 16:9 and 21:9, 55% on 9:16. `intro_end_frame_reference_1920x1080.png` is the last frame of the intro film (Shot 5 dissolves onto it).

## Round 3 — `s5_start` regeneration

Script: `scripts/prompt1_s5_regen.py`. References: image 1 = `hero_cutout/tom_night_ref.png` (corrected night cut-out on a dark background, main reference), image 2 = ref 02. Changes from round 2's prompt B: Tom described from the corrected front view at 1 : 3.5 overall with near edge-to-edge screens; Tom at about 60% of frame height (55% on 9:16) with open sky above, so the Shot 5 move to the hero frame is small.

Pricing note: Marketing Studio Image charges by prompt length as well as by reference count (about $0.004 per 1,000 characters). Quotes must be taken with the real prompt, not a placeholder.

Round 3 result (12 Nov 2026, $0.372, real-prompt quote): 4 images in `media/generated/drafts/round3_s5_start/`, sheet `media/generated/contact_sheet_s5_start_round3.jpg`. Picked `s5_start_16x9_v1` (screens near edge-to-edge, small corner radius). It came out at about 1 : 3.04 overall and 82% of frame height, so the Shot 5 first frame (`media/generated/clips_input/s5_first_16x9.png`) is that image scaled horizontally by 0.869 to reach 1 : 3.5, with the sides mirror-padded back to 16:9.

## PROMPT 2 — clips (Kling 4.0 image-to-video)

Script: `scripts/prompt2_clips.py`. Rates: $0.1257/s at 720p, $0.1879/s at 1080p, whole seconds from 3 s. Input frames: `media/generated/clips_input/`. Outputs: `media/generated/clips/`.

- **Shot 5** (`s5`): first frame = `s5_first_16x9.png`, end frame = `s5_last_16x9.png` (= `hero_test/intro_end_frame_reference_1920x1080.png`). 5 s, trimmed to 4.5 s in the edit. The edit always finishes with a short dissolve onto the real end-frame still. Step 1 is one 720p test; if Kling warps Tom, Shot 5 becomes a clean dissolve from `s5_start` to the hero frame.
- **Shot 2** (`s2`): Kling requires a first frame, so the chosen `s2_end` still is the FIRST frame and the clip is a very gentle push-in (about 5% on 16:9, about 3% on 9:16). 3 s, trimmed to 2.5 s. 9:16 uses `s2_first_9x16.png`, the tight reframe of the 16:9 pick (decided by Wassim).
- Approved: test $0.63; step 2 drafts $4.02 pre-approved only if the test does not warp Tom.

Shot 5 prompt:

> Night. The camera stays centred on the tall black smartboard totem while it slowly lowers toward the ground, eases back slightly and tilts up. The road, buildings, palm trees, street lights and light trails sink smoothly out of the bottom of the frame until only the totem remains, standing against a clear, deep blue-black sky with faint stars. During the move the totem's two screens power on together, rising from black to an even, soft, cool-white glow. [RIGID]

Shot 2 prompt:

> Blue hour. A very slow, gentle push-in of about [5% / 3%] toward the tall black smartboard totem on the roadside. Traffic keeps flowing as motion-blurred white and red light trails; palm fronds move very slightly. The totem's screens keep the same even cool-white glow and its red side strip stays lit. The skyline stays fixed and does not change. [RIGID]

[RIGID]:

> The totem is a rigid, solid object: its shape, proportions, straight edges, two screens, top cap, plinth and red side light strip stay exactly identical throughout. No morphing, no bending, no stretching, no extra parts, no text or logos anywhere. Smooth, steady, cinematic camera motion, one continuous shot, no cuts, no shake.

## Addition to PROMPT 3 (edit) — real screen content on Tom (decided by Wassim, 12 Nov 2026)

In the edit, composite real screen content onto Tom's two screens in **Shot 2 and Shot 5**, tracked to the camera move (corner-pin per frame; both moves are slow, so a planar track of the screen corners is enough).

- **Upper screen:** a CITIX-style weather/time widget, **night variant**, built in code or as a rendered plate in the style of ref 12 (`12_AQI_widget_ui.png`) and `day_night.mp4` (refs 09, 10). Ref 12 is never uploaded to Higgsfield.
- **Lower screen:** a neutral CITIX brand message: Pulse Red #FD0332, Gilroy, **no third-party brands** (the Emirates and Aurex ads in the refs must not be reproduced).
- **Shot 5:** the content appears as the screens "power on": black → brief cool-white glow → content fades up, timed to Kling's power-on.
- **Shot 2:** content is on from the first frame.
- Cover most of the generated bezel so the screens read near edge-to-edge, as in Prompt 4.
- The hero end frame must match what Prompt 4 shows on the screens in its night state, so the film's last frame and the hero's first state are identical.

### Prompt 2 progress

- **Step 1, Shot 5 test (12 Nov 2026, $0.629):** `media/generated/clips/s5_test_16x9_720p.mp4`. Approved by Wassim on 13 Nov after a frame-by-frame check: smooth power-on, no deformation of Tom. One flaw: a palm top lingers bottom-left until about 4.25 s. This clip counts as `s5` 16:9 variation 1.
- **Step 2 drafts (13 Nov 2026, $3.394, 720p):** `s2_16x9_v1/v2`, `s2_9x16_v1/v2` (3 s, push-in of about 3% on both formats), `s5_16x9_v2`, `s5_9x16_v1/v2` (5 s). Each clip has a 4-fps contact sheet next to it (`*_sheet_4fps.jpg`).
- **Shot 5 prompt for step 2** (change: street fully gone by 3 s):

> Night. The camera stays centred on the tall black smartboard totem while it slowly lowers toward the ground, eases back slightly and tilts up. The road, buildings, palm trees, street lights and light trails sink smoothly and completely out of the bottom of the frame early in the shot: by the 3 second mark nothing of the street, the palms or the buildings is left anywhere in the frame, including the bottom corners. For the last 2 seconds only the totem remains, standing against a clear, deep blue-black sky with faint stars, while the camera settles gently. During the move the totem's two screens power on together, rising smoothly from black to an even, soft, cool-white glow. [RIGID]

- **9:16 Shot 5 first frame:** `clips_input/s5_first_9x16.png` = `round3_s5_start/s5_start_9x16_v1.png`, which measured about 1 : 3.72 overall (slightly too slim), widened horizontally by 1.063 to 1 : 3.5 and cropped back to 9:16 centred on Tom. End frame: `clips_input/s5_last_9x16.png` (= `hero_test/hero_night_9x16.png`, Tom at 55%).

- **Draft review by Wassim at 24 fps (13 Nov 2026).** Picks: Shot 2 → `s2_16x9_v1` + `s2_9x16_v2`; Shot 5 → `s5_16x9_v2` + `s5_9x16_v1`. `s2_9x16_v1` rejected: the plinth flickers to light grey at about 1.7, 1.75 and 2.1 s. `s2_9x16_v2` has subtle luminance pumping on the plinth (about 1.5 and 1.9 s), and some is visible on 16:9 too.
- **Finals, 1080p (13 Nov 2026):** one clip each for `s2` 16:9, `s2` 9:16, `s5` 16:9, `s5` 9:16, same inputs and prompts as the picks (`*_final_1080p.mp4`). Kling is not deterministic, so the finals are new takes of the same shot, not upscales of the picked drafts; they are checked again with `scripts/flicker_check.py`.

## Addition to PROMPT 3 (edit) — "Tom lock" and deflicker (decided by Wassim, 13 Nov 2026)

Kling makes Tom's plinth and body pump in luminance from frame to frame. Fix it in the edit, in this order:

**Shot 2**
1. **Tom lock.** Composite the clean source still of Tom, cut from the Shot 2 first frame (`clips_input/s2_first_16x9.png` / `s2_first_9x16.png`), over the clip. Track it to the push-in with a scale and position per frame, so Tom is perfectly stable while traffic and the city move behind him. The push-in is about 3% and nearly linear, so a similarity transform (scale + translate) per frame is enough; fit it to Tom's edges or his red strip, then smooth the curve.
2. **Deflicker the background** lightly (e.g. ffmpeg `deflicker`) under the locked Tom.
3. **Screen content** (weather/time widget on the upper screen, CITIX message on the lower) is composited on top of the locked Tom, so it inherits the same track.

**Shot 5**
1. Apply the same light deflicker and check the plinth and body with `scripts/flicker_check.py`.
2. Use the Tom lock only if flicker remains. Tom changes scale and position much more in this shot, and the screens power on, so the lock would need the hero cut-out with a per-frame transform and a screens-off to screens-on blend.

**Checking.** `scripts/flicker_check.py <clip>` measures the plinth and the body band next to the red strip in every frame at 24 fps and lists frames that deviate from the local median: mild above 3 luminance levels, strong above 8. Run it on the finals before the edit and again on the edited shots.
