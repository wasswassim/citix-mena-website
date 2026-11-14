# Hero orbit — product references (H0, 14 Nov 2026)

Folder: `media/hero_orbit/refs/` (raw media, git-ignored). Sheet: `media/hero_orbit/refs/_refs_sheet.jpg`.
All files are **copies**; originals are untouched. Candidates that were not picked are in `refs/_candidates/`.

| Product | File | Source | Edit |
|---|---|---|---|
| Tom (old) | `tom/01_tom_day_photo_ad_neutral.png` | `media/source/01_tom_day_photo.jpg` | third-party ad (Emirates) on the lower screen replaced by a neutral cool panel |
| Tom (old) | `tom/02_tom_night_photo_ad_neutral.png` | `media/source/02_tom_night_photo.jpg` | same; red side strip kept |
| Tom (old) | `tom/tom_day.png`, `tom/tom_night.png`, `tom/tom_night_ref.png` | `media/generated/hero_cutout/` (option A, 1:3.5) | none |
| Jerry | `jerry/jerry_01_studio_grey.png` | sales PDF p12 (Image82) | "Azure" shoe ad on the lower screen neutralised |
| Jerry | `jerry/jerry_02_on_black.png` | sales PDF p15 (Image99), cropped | same |
| Baloo | `baloo/baloo_01_overview_t1.75.png`, `baloo_02_spire_screen_t1.75.png`, `baloo_03_screen_base_detail_t1.75.png` | `Média1pptx_s18_baloo_3d_video.mp4` @ 1.75 s (4K) | "JETOUR", "Built for the future", "X70" painted out; "TEJARA 1" building sign cropped out |
| Jumbo | `jumbo/jumbo_01..03_two_faces_t{3.75,6.25,9.25}.png` | `Média1pptx_s20_jumbo_3d_video.mp4` | perfume label (Gucci) and shop/bank/cinema signs blurred |

Notes
- Baloo: the camera moves between frames, so the three refs come from the one frame whose ad text could be cleanly removed (overview, spire + screen, screen base + CITIX band).
- The CITIX MENA logos on the Jerry cap, Baloo band and Tom cap are CITIX's own; generated images still keep caps plain and the real logo is composited later.
- Jumbo's screen content (bottle, tree) is a third-party ad; prompts use the refs for the building corner and two-face screen geometry only.
- Not used: new-Tom calligraphy refs 03–06, PDF images with the Burj Khalifa (p32 Emaar ad) or third-party ads.

- Added 14 Nov 2026: `jumbo/jumbo_03_two_faces_t9.25_screen_neutral.png` — the t9.25 frame had small Gucci logos on the screen-room floor (missed in H0); this copy desaturates the pink room to cool grey and blurs the bottle, tree and floor logos. Use it instead of jumbo_01/03 for R5.
