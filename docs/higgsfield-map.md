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
