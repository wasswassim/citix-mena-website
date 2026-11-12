# Higgsfield prompts — Prompt 1 drafts (stills)

Model: `marketing-studio/image` (2.0 Alpha), 2k, medium quality, `enhance_prompt: false`, one image per request, 2 variations per format. The exact text sent is in `scripts/prompt1_drafts.py`.

## Round 2 — OLD Tom (current)

Status: **quoted, awaiting Wassim's OK.**

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

Framing per format: 16:9 and 21:9 — *the totem fills about 82% of the frame height.* 9:16 — *Vertical composition: the totem fills about 68% of the frame height, anchored at the bottom, with a large area of empty sky above it.*

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
