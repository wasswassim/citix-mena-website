# Higgsfield asset map

**Current Tom prompts use refs 01 and 02 only (old Tom).** Refs 03–06 wait for the company's calligraphy artwork; the other refs stay uploaded for later prompts.

Uploads only, no generation. `12_AQI_widget_ui.png` is for code use and is never uploaded.

Higgsfield has no permanent asset IDs: an upload returns a **public URL** that is passed to models as `image_url` / `image_urls` / `end_image_url`. Uploaded files are **deleted within 7 days**, so `scripts/higgsfield.py upload` caches each URL (in `media/generated/uploads.json`) and re-uploads automatically after 6 days. Re-run the upload before a generation session if the date below is older than 6 days.

Uploaded: 2026-11-12 (expires by 2026-11-19)

| Local file | Higgsfield asset (public URL) | Uploaded | Intended use |
|---|---|---|---|
| 01_tom_day_photo.jpg | https://d3snorpfx4xhv8.cloudfront.net/40bb762b-0a8d-4f0e-913f-a4959f5a59be/a4596642-22e3-4247-92df-b76fb1445a19.jpeg | 2026-11-12 | Tom shape/proportions (day) |
| 02_tom_night_photo.jpg | https://d3snorpfx4xhv8.cloudfront.net/40bb762b-0a8d-4f0e-913f-a4959f5a59be/56d36913-08e7-4389-a8dd-06be853829dd.jpeg | 2026-11-12 | Tom shape/proportions (night) |
| 03_TOM_calligraphy_side_a.png | https://d3snorpfx4xhv8.cloudfront.net/40bb762b-0a8d-4f0e-913f-a4959f5a59be/1d347acf-91f6-43b3-94e6-a15bf42c3cca.png | 2026-11-12 | NEW Tom design: Arabic calligraphy on the side panels (replaces side light) |
| 04_TOM_calligraphy_side_b.png | https://d3snorpfx4xhv8.cloudfront.net/40bb762b-0a8d-4f0e-913f-a4959f5a59be/e44e9658-cb6f-46df-8ada-f95ef70cf109.png | 2026-11-12 | NEW Tom design: Arabic calligraphy on the side panels (replaces side light) |
| 05_TOM_full_silhouette.png | https://d3snorpfx4xhv8.cloudfront.net/40bb762b-0a8d-4f0e-913f-a4959f5a59be/9b085737-746c-4d45-960b-11aab4bddd14.png | 2026-11-12 | NEW Tom design: Arabic calligraphy on the side panels (replaces side light) |
| 06_JERRY_calligraphy_side.png | https://d3snorpfx4xhv8.cloudfront.net/40bb762b-0a8d-4f0e-913f-a4959f5a59be/2ba7f71e-3dcd-4014-814e-92e7d50997fa.png | 2026-11-12 | Calligraphy pattern detail (Jerry side panel; pattern reference only) |
| 07_3in1_Tom_render_front.png | https://d3snorpfx4xhv8.cloudfront.net/40bb762b-0a8d-4f0e-913f-a4959f5a59be/bd3c79bd-9828-484f-8736-fb2238bd82f4.png | 2026-11-12 | Materials, screen frame, angles |
| 08_tom_wate_auto_render.png | https://d3snorpfx4xhv8.cloudfront.net/40bb762b-0a8d-4f0e-913f-a4959f5a59be/082c6a1c-385d-4607-b2c4-6f795e7f6472.png | 2026-11-12 | Materials, screen frame, angles |
| 09_day_night_start.png | https://d3snorpfx4xhv8.cloudfront.net/40bb762b-0a8d-4f0e-913f-a4959f5a59be/ed00c0ea-1e14-4a0a-bf76-499befede0bb.png | 2026-11-12 | Day/night screen-switch reference |
| 10_day_night_end.png | https://d3snorpfx4xhv8.cloudfront.net/40bb762b-0a8d-4f0e-913f-a4959f5a59be/44a2d5cb-0b89-42d4-ad71-33017210ae91.png | 2026-11-12 | Day/night screen-switch reference |
| 11_ramadan2_night_mood.png | https://d3snorpfx4xhv8.cloudfront.net/40bb762b-0a8d-4f0e-913f-a4959f5a59be/7b451e64-a6c3-4c57-b314-be49bb853f95.png | 2026-11-12 | Night street mood, light trails |

## Prompt 1 drafts, round 1 — NEW Tom with calligraphy (generated 2026-11-12, archived)

Model `marketing-studio/image`, 2k, medium quality. 20 images, total $2.233. Outputs are deleted from Higgsfield after 7 days; the local copies in `media/generated/drafts/round1_new_tom/` (not committed) are the record. Not used for finals: the calligraphy came out as pseudo-script, so round 2 uses the old Tom. Prompts: `docs/higgsfield-prompts.md`. Contact sheet: `media/generated/drafts/round1_new_tom/contact_sheet_prompt1.jpg`.

| Local file | Higgsfield request ID | Ratio | Cost | Intended use |
|---|---|---|---|---|
| media/generated/drafts/round1_new_tom/hero_day_16x9_v1.png | `01a1d0f9-6e1a-7f65-ae98-49a2a3b997dd` | 16:9 | $0.086 | Hero day state (edit of matching hero_night) |
| media/generated/drafts/round1_new_tom/hero_day_16x9_v2.png | `01a1d0f9-7386-7fbe-adad-d5e5cb68dac8` | 16:9 | $0.086 | Hero day state (edit of matching hero_night) |
| media/generated/drafts/round1_new_tom/hero_day_21x9_v1.png | `01a1d0f9-6fed-78d3-8f0e-ddbfb6591aff` | 21:9 | $0.068 | Hero day state (edit of matching hero_night) |
| media/generated/drafts/round1_new_tom/hero_day_21x9_v2.png | `01a1d0f9-753c-7c95-88aa-53671ecd719f` | 21:9 | $0.068 | Hero day state (edit of matching hero_night) |
| media/generated/drafts/round1_new_tom/hero_day_9x16_v1.png | `01a1d0f9-71bf-788e-a79e-d62a4b755116` | 9:16 | $0.086 | Hero day state (edit of matching hero_night) |
| media/generated/drafts/round1_new_tom/hero_day_9x16_v2.png | `01a1d0f9-77e8-79b7-9540-ec7b47dadf2c` | 9:16 | $0.086 | Hero day state (edit of matching hero_night) |
| media/generated/drafts/round1_new_tom/hero_night_16x9_v1.png | `01a1d0f7-a0f9-7b87-8dc0-f3ecc4c7010e` | 16:9 | $0.124 | Shot 5 end frame + hero night state |
| media/generated/drafts/round1_new_tom/hero_night_16x9_v2.png | `01a1d0f7-adfd-74e0-96b1-516c26a7bac7` | 16:9 | $0.124 | Shot 5 end frame + hero night state |
| media/generated/drafts/round1_new_tom/hero_night_21x9_v1.png | `01a1d0f7-a2f8-7d07-b51d-3878c81c4812` | 21:9 | $0.106 | Shot 5 end frame + hero night state |
| media/generated/drafts/round1_new_tom/hero_night_21x9_v2.png | `01a1d0f7-afb1-74cb-b2bc-c3448dfd4484` | 21:9 | $0.107 | Shot 5 end frame + hero night state |
| media/generated/drafts/round1_new_tom/hero_night_9x16_v1.png | `01a1d0f7-a4c3-7598-80f4-0886f5411086` | 9:16 | $0.125 | Shot 5 end frame + hero night state |
| media/generated/drafts/round1_new_tom/hero_night_9x16_v2.png | `01a1d0f7-b165-7feb-bc81-15e49c6a950d` | 9:16 | $0.125 | Shot 5 end frame + hero night state |
| media/generated/drafts/round1_new_tom/s2_end_16x9_v1.png | `01a1d0f7-99e7-799e-971c-342149f3ba4b` | 16:9 | $0.136 | Shot 2 end frame (Kling last frame) |
| media/generated/drafts/round1_new_tom/s2_end_16x9_v2.png | `01a1d0f7-a67f-764f-8267-6c6bf4a31d99` | 16:9 | $0.136 | Shot 2 end frame (Kling last frame) |
| media/generated/drafts/round1_new_tom/s2_end_9x16_v1.png | `01a1d0f7-9d62-7911-b28a-7310454afa55` | 9:16 | $0.137 | Shot 2 end frame (Kling last frame) |
| media/generated/drafts/round1_new_tom/s2_end_9x16_v2.png | `01a1d0f7-aa35-7cda-9e2c-b772bd974b37` | 9:16 | $0.137 | Shot 2 end frame (Kling last frame) |
| media/generated/drafts/round1_new_tom/s5_start_16x9_v1.png | `01a1d0f7-9b8b-76a9-90a8-30e465d43879` | 16:9 | $0.124 | Shot 5 start frame (Kling first frame) |
| media/generated/drafts/round1_new_tom/s5_start_16x9_v2.png | `01a1d0f7-a85b-7151-ac14-efb36a611a69` | 16:9 | $0.124 | Shot 5 start frame (Kling first frame) |
| media/generated/drafts/round1_new_tom/s5_start_9x16_v1.png | `01a1d0f7-9f2b-7c78-b686-61833db376d7` | 9:16 | $0.124 | Shot 5 start frame (Kling first frame) |
| media/generated/drafts/round1_new_tom/s5_start_9x16_v2.png | `01a1d0f7-abfa-7413-8f1b-2583401002ec` | 9:16 | $0.124 | Shot 5 start frame (Kling first frame) |

## Prompt 1 drafts, round 2 — OLD Tom, refs 01 + 02 (generated 2026-11-12)

Model `marketing-studio/image`, 2k, medium quality. 20 images, total $1.800. Local copies in `media/generated/drafts/` (not committed). Contact sheet: `contact_sheet_round2.jpg`; day/night 50% overlays: `overlays_day_night_50.jpg`. Known issues: Tom is larger in the hero frames than the 60% / 55% asked for; body proportions drift wider than the real 1 : 3; the 21:9 day/night pairs are slightly misaligned.

| Local file | Higgsfield request ID | Ratio | Cost | Intended use |
|---|---|---|---|---|
| media/generated/drafts/hero_day_16x9_v1.png | `01a1d10f-bbdc-73ea-a0b8-b83a64eca48f` | 16:9 | $0.086 | Hero day state (edit of matching hero_night) |
| media/generated/drafts/hero_day_16x9_v2.png | `01a1d10f-c1c1-737e-b88e-aea406c68870` | 16:9 | $0.086 | Hero day state (edit of matching hero_night) |
| media/generated/drafts/hero_day_21x9_v1.png | `01a1d10f-bdd0-7f93-b4f1-a0a00afd4b3a` | 21:9 | $0.069 | Hero day state (edit of matching hero_night) |
| media/generated/drafts/hero_day_21x9_v2.png | `01a1d10f-c37d-7764-9a4a-bb16a5e0f2db` | 21:9 | $0.069 | Hero day state (edit of matching hero_night) |
| media/generated/drafts/hero_day_9x16_v1.png | `01a1d10f-bfe6-7aaf-be24-6a8bf38aba1b` | 9:16 | $0.086 | Hero day state (edit of matching hero_night) |
| media/generated/drafts/hero_day_9x16_v2.png | `01a1d10f-c56e-71af-8d9d-b3da1e2c57c1` | 9:16 | $0.086 | Hero day state (edit of matching hero_night) |
| media/generated/drafts/hero_night_16x9_v1.png | `01a1d10e-4ab5-7ede-ac61-8cde1ee5903c` | 16:9 | $0.094 | Shot 5 last frame + hero night state |
| media/generated/drafts/hero_night_16x9_v2.png | `01a1d10e-570f-7517-a0df-5901abe48654` | 16:9 | $0.094 | Shot 5 last frame + hero night state |
| media/generated/drafts/hero_night_21x9_v1.png | `01a1d10e-4c88-7221-8ab5-45dd77336757` | 21:9 | $0.077 | Shot 5 last frame + hero night state |
| media/generated/drafts/hero_night_21x9_v2.png | `01a1d10e-58d1-754a-8820-9aeb059e4e6c` | 21:9 | $0.077 | Shot 5 last frame + hero night state |
| media/generated/drafts/hero_night_9x16_v1.png | `01a1d10e-4e4b-76b2-b9a5-628be5ae7d2a` | 9:16 | $0.094 | Shot 5 last frame + hero night state |
| media/generated/drafts/hero_night_9x16_v2.png | `01a1d10e-5aa9-7ad6-8be8-738144eee671` | 9:16 | $0.094 | Shot 5 last frame + hero night state |
| media/generated/drafts/s2_end_16x9_v1.png | `01a1d10e-42f4-7e34-9c5e-12550de6e38b` | 16:9 | $0.104 | Shot 2 last frame (street push-in after hard cut) |
| media/generated/drafts/s2_end_16x9_v2.png | `01a1d10e-4ff8-7809-b8ce-5773dd84c7ba` | 16:9 | $0.104 | Shot 2 last frame (street push-in after hard cut) |
| media/generated/drafts/s2_end_9x16_v1.png | `01a1d10e-46e3-759f-9905-14a67fe7bcaa` | 9:16 | $0.105 | Shot 2 last frame (street push-in after hard cut) |
| media/generated/drafts/s2_end_9x16_v2.png | `01a1d10e-537f-7368-825c-ab0bcedc6013` | 9:16 | $0.105 | Shot 2 last frame (street push-in after hard cut) |
| media/generated/drafts/s5_start_16x9_v1.png | `01a1d10e-450b-7ac9-b2d8-b8a0bcd29acf` | 16:9 | $0.092 | Shot 5 first frame |
| media/generated/drafts/s5_start_16x9_v2.png | `01a1d10e-51be-7c64-821c-a7549142d779` | 16:9 | $0.092 | Shot 5 first frame |
| media/generated/drafts/s5_start_9x16_v1.png | `01a1d10e-48c2-7253-ba1d-e5a5e5ca503a` | 9:16 | $0.093 | Shot 5 first frame |
| media/generated/drafts/s5_start_9x16_v2.png | `01a1d10e-553c-7398-9819-84e215befc8b` | 9:16 | $0.093 | Shot 5 first frame |

## Prompt 1 drafts, round 3 — `s5_start` regeneration (generated 2026-11-12)

Model `marketing-studio/image`, 2k, medium. 4 images, total $0.372. References: corrected night cut-out (`hero_cutout/tom_night_ref.png`) + ref 02. Sheet: `media/generated/contact_sheet_s5_start_round3.jpg`. Picked: `s5_start_16x9_v1` and `s5_start_9x16_v1`.

| Local file | Higgsfield request ID | Ratio | Cost | Intended use |
|---|---|---|---|---|
| media/generated/drafts/round3_s5_start/s5_start_16x9_v1.png | `01a1d131-02c8-79e2-8419-2675888030b1` | 16:9 | $0.093 | Shot 5 first frame candidate |
| media/generated/drafts/round3_s5_start/s5_start_16x9_v2.png | `01a1d131-0696-7bc9-b189-05e81a63f33a` | 16:9 | $0.093 | Shot 5 first frame candidate |
| media/generated/drafts/round3_s5_start/s5_start_9x16_v1.png | `01a1d131-04b8-779b-8b73-2fd262a129d9` | 9:16 | $0.093 | Shot 5 first frame candidate |
| media/generated/drafts/round3_s5_start/s5_start_9x16_v2.png | `01a1d131-085a-799e-819b-129fe019f1bf` | 9:16 | $0.093 | Shot 5 first frame candidate |

## Local derivatives (no API cost)

| Local file | Made from | Intended use |
|---|---|---|
| media/generated/hero_cutout/tom_night.png, tom_day.png (+ .webp) | round 2 `hero_night_16x9_v1` / `hero_day_16x9_v1` | Registered transparent Tom cut-outs for the coded hero (Prompt 4), 1 : 3.5 overall |
| media/generated/hero_test/hero_{night,day}_{16x9,21x9,9x16}.png | cut-outs over placeholder skies | Static hero tests, Tom at 60% / 55% of frame height |
| media/generated/hero_test/intro_end_frame_reference_1920x1080.png | `hero_night_16x9` test render | Last frame of the intro film |
| media/generated/clips_input/s2_first_16x9.png | round 2 `s2_end_16x9_v2` | Shot 2 first frame, 16:9 |
| media/generated/clips_input/s2_first_9x16.png | tight 9:16 crop of `s2_end_16x9_v2` | Shot 2 first frame, 9:16 |
| media/generated/clips_input/s5_first_16x9.png | round 3 `s5_start_16x9_v1`, x-scale 0.869, sides mirror-padded | Shot 5 first frame, 16:9 |
| media/generated/clips_input/s5_first_9x16.png | round 3 `s5_start_9x16_v1`, x-scale 1.063, cropped | Shot 5 first frame, 9:16 |
| media/generated/clips_input/s5_last_16x9.png, s5_last_9x16.png | hero test renders (night) | Shot 5 end frames |

## Prompt 2 clips — Kling 4.0 image-to-video, 720p drafts (2026-11-12 and 2026-11-13)

Total $4.022 (test $0.629 + 7 drafts). Each clip has a 4-fps contact sheet next to it (`*_sheet_4fps.jpg`). Outputs are deleted from Higgsfield after 7 days; local copies in `media/generated/clips/` (not committed).

| Local file | Higgsfield request ID | Length | Cost | Intended use |
|---|---|---|---|---|
| media/generated/clips/s2_16x9_v1.mp4 | `01a1d492-95a2-7b55-8bae-3a0733a3d048` | 3 s | $0.377 | Shot 2 push-in, 16:9, variation 1 |
| media/generated/clips/s2_16x9_v2.mp4 | `01a1d492-97db-734c-ac0a-87ef49b86254` | 3 s | $0.377 | Shot 2 push-in, 16:9, variation 2 |
| media/generated/clips/s2_9x16_v1.mp4 | `01a1d492-99dd-72d3-a02d-ff671a2d05d1` | 3 s | $0.377 | Shot 2 push-in, 9:16, variation 1 |
| media/generated/clips/s2_9x16_v2.mp4 | `01a1d492-9bf1-7b1b-8f26-63532267b4b7` | 3 s | $0.377 | Shot 2 push-in, 9:16, variation 2 |
| media/generated/clips/s5_16x9_v2.mp4 | `01a1d492-9e1d-7e8d-9901-c47b1ba9494b` | 5 s | $0.629 | Shot 5 lower-and-tilt, 16:9, variation 2 |
| media/generated/clips/s5_9x16_v1.mp4 | `01a1d492-9ffa-7ae7-b6d2-6114dc82ab6f` | 5 s | $0.629 | Shot 5 lower-and-tilt, 9:16, variation 1 |
| media/generated/clips/s5_9x16_v2.mp4 | `01a1d492-a205-7771-989e-be46352ba9cf` | 5 s | $0.629 | Shot 5 lower-and-tilt, 9:16, variation 2 |
| media/generated/clips/s5_test_16x9_720p.mp4 | `01a1d133-6f0f-7297-ae73-6a45c24e8880` | 5 s | $0.629 | Shot 5, 16:9, variation 1 (the approved test) |
