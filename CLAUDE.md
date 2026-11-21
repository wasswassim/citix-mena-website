# CITIX MENA website — project memory for Claude Code

Owner: Wassim Gatri (intern, CITIX MENA). Goal: a **homepage pitch** for the new CITIX MENA website (citixmena.com) with modern 3D, scroll and video effects, strictly on-brand. Other pages are "coming soon" placeholders until the homepage is approved. Code lives in Wassim's personal GitHub. Design is shared in Figma.

Planning happens in a claude.ai Project ("CitiX MENA Internship"); copies of the key docs are in `/docs/planning/`. If something here conflicts with a newer instruction from Wassim, follow Wassim.

**Current hero plan: v5, 4 glass-panel scenes (14 Nov 2026, evening).** The single source of truth for the hero build is `/docs/planning/HERO_ORBIT_RUNBOOK.md` (v5, phases P0 → P5, stop only at the ⛔ gates; v4.2 kept as `HERO_ORBIT_RUNBOOK_v4.2_archived.md`). Where this file and the runbook disagree, the runbook wins.

## Model routing
- **Fable 5.2**: writing and refining Higgsfield prompts, and the hardest creative-technical parts (hero orbit stills and clips, loop assembly, 3D/WebGL, dust overlay, scroll choreography).
- **Opus**: everything else (setup, scripts, components, SEO, QA). Opus may launch **Sonnet sub-agents** for parallel, well-scoped tasks (file inventories, frame extraction, compression, tests, lint, docs). Sub-agents never spend Higgsfield credits and never touch `.env`.

## Hard rules (never break)
1. **Secrets:** API keys live only in `.env` (git-ignored). Never print, log, echo, `cat`/`type` or commit them. Never ask for keys in chat. Edit `.env` only with a script that changes the target line and prints nothing from the file.
2. **Spending:** before any Higgsfield generation, show the price per unit and the total, then wait for Wassim's explicit OK on that exact quote. Scripts refuse any job above `HIGGSFIELD_MAX_SPEND_USD` in `.env` (set to 40 on 14 Nov 2026).
3. **Approval gates:** show a contact sheet and wait for a choice before finals or rerolls. Default is drafts first (low res, 2 variations); for the hero orbit the runbook sets **1 variation per still**, with rerolls proposed (reason + cost) at the gate.
4. **Product accuracy:** never invent CITIX products, parts, logos or text. Build every product from the reference files (`media/hero_orbit/refs/`) and list any differences after each generation.
5. **No reuse of others' work:** don't copy code or assets from inspiration sites (bluesqx.com, flyshare.design, wowmedia.com, apple.com…). Copy structure and motion ideas only; rebuild the effect ourselves.
6. **Landmarks:** no Burj Khalifa, Burj Al Arab or other owned landmarks as a subject (Emaar's asset policy covers CGI too). No mosques as a framed subject. No identifiable people. No third-party logos in generated media. Vehicles unbranded; no Range Rover or other real-model replica.
7. **Don't delete or overwrite user files** without asking. Archive into a new folder instead; copy originals, don't move them. Never read again or copy the plain-text key file into the repo.

## Brand guardrails (brand book)
- Colours: Midnight Black #000000, Graphite Shadow #161616, Pure Snow #FFFFFF, Urban Mist #E0E0E0, **Pulse Red #FD0332** (gradient #FD0332 → #990332).
- Type: **Gilroy ExtraBold** (headings), **Gilroy Light** (body). Gilroy is live on the site (21 Nov 2026): 6 weights (300–800) built as WOFF2 by `scripts/build-fonts.py` from `Internship/01_Brand/Fonts_Gilroy` into `public/fonts/` (git-ignored: commercial font, public repo; a fresh clone falls back to Century Gothic). Latin only; Arabic uses system Arabic fonts. A web licence for Gilroy is needed before the site goes live.
- Look: a *real* city enhanced by CITIX ("the future is already part of the city"). Night: high contrast, light trails, defined artificial light. Day: realistic daylight, clean, minimal noise.
- **Hero orbit world (v4.2 exception):** dark void over moonlit desert dunes, cool blue grading, volumetric light from the screen. Deserts only under moonlight / blue hour.
- Avoid: sci-fi, abstract CGI, neon/acid or oversaturated colours, warm/yellowish tones, digital noise, clutter, staged static people (motion-blurred only), competitor-like aesthetics.
- Smartboard = main subject, centred or shifted right. Smooth, cinematic camera.
- Logo: never bottom-right; clear space = height of the "X"; never stretched, tilted, outlined-only or gradient-filled.
- Copy tone: confident, action-driven, concrete benefits, no startup clichés. Slogans: "Smarter cities. Stronger brands." / "We make tomorrow happen today."
- Exception approved for now: real city names (Sharjah, Abu Dhabi) may appear. Wassim will review this with his supervisor.

## Products (sales deck — some sizes still to confirm)
- Street smartboards: **Jerry** (pedestrian, 2.6 × 1 m), **Tom** (roadside, 7 × 2 m vertical totem; screen split: top = info widgets, bottom = ad), **Smart Pillar** (petrol stations).
- Giant 3D screens: **Baloo** (corner spire, Tejara 1), **Simba**, **Jumbo** (largest corner screen, premium mall). Software: **Citix OS**.
- **Tom to use NOW (decided 12 Nov 2026): the OLD Tom**, exactly as in the real photos (refs 01 day, 02 night), including its real **red side light strip** (thin vertical red LED line on the right side face, lit at night), proportions 1 : 3.5. All stills and clips use it until the company sends the calligraphy artwork. Only refs 01 and 02 (and the cut-outs made from them) go into Tom prompts. In generated images the top cap stays **plain, with no text or logo**; the real "CITIX MENA" logo is composited onto the finals.
- **New Tom (LATER):** engraved **Arabic calligraphy pattern on the side panels** instead of the side light strip (refs 03, 04, 06). Generation can't reproduce the real script (round 1 drafts gave pseudo-script), so wait for the company's calligraphy artwork or 3D model, then rebuild the Tom references and regenerate. Don't use refs 03–06 in prompts before that.
- Smartboard logic: widgets on top catch the eye like a phone notification, the ad sits below. Eye-tracking study: +53% conversion vs standard billboards.
- Real installations: Yas Island entrances, Abu Dhabi (first 2 Tom); Sharjah (Shurooq partnership: Al Qasba, Al Heera Beach, Flag Island, Khorfakkan…); Jumbo at an Abu Dhabi mall.

## Current plan: v5 (BlueSquareX model) — homepage + hero "The Orbit", 4 glass-panel scenes
- Homepage modelled on bluesqx.com (structure and motion only; no copying of their code, video, images or text). Sections: 1 Hero "The Orbit" · 2 Install / Operate / Create / Measure · 3 Who we serve · 4 Our Smartboards · 5 About + numbers · 6 Projects tabs · 7 Trusted by · 8 Newsletter · 9 Footer. EN + AR (RTL); inner pages "Coming soon".
- **Hero (v5):** 4 scenes × 8 s = 32 s loop, joined on black (dune wipes). Every scene is made **exactly like the approved R3 camel clip** (`media/hero_orbit/seedance/R3_ref.mp4`, method `docs/planning/R3_camel_method.md`): the same frameless glass panel, the same camera reference `media/hero_orbit/lab/orbit_reference_R3_8s.mp4`, the same look (`R3_16x9_v3.png` as image ref), Seedance 2.0 reference-to-video at 8 s / 720p / 16:9 / no audio, the same prompt structure. Only the content changes:
  - **Oasis:** water and date palms spill out of the glass.
  - **Camel:** done and approved; reuse `R3_ref.mp4` as is.
  - **Perfume:** an unbranded faceted bottle floats out with rose petals; pink-red only inside the glass.
  - **SUV (finale):** an unbranded generic SUV bursts out and drifts; the glass stays intact. (Code dust overlay dropped by Wassim, 15 Nov 2026.)
  - Loop order: the runbook says oasis → camel → perfume → SUV; Wassim's chat message (14 Nov) said oasis → perfume → camel → SUV. Confirm at GATE 3.
  - New outputs go in `media/hero_orbit/v5/`. No lock script or grading on raw clips unless Wassim asks.
  - **Hero approved at GATE 5 (15 Nov 2026), as built:** bluesqx-style shell (flat 50% overlay, fixed header, gradient H1 "Smarter Cities. / Stronger Brands.", outline CTAs, trusted-by marquee, announcement bar built but off in `lib/flags.ts`), with CITIX wording, EN/AR mirrored, CSS H1 reveal (no SplitType). Placeholders still: text wordmark (no CITIX logo file), boxed brand names (no official SVGs). Next: Wassim's direction to make the hero our own, distinct from bluesqx.
  - The products (Tom, Jerry, Baloo, Jumbo) leave the hero and are shown in the Smartboards section with real assets.
- **Trusted by / logo marquee:** exactly these 35 brands from citixmena.com's "Trusted by leading global brands": Sony, Kia, Panasonic, Yokohama, Apple, L'Oréal, Rolex, McDonald's, Tiffany & Co., Coca-Cola, Lenovo, Lexus, Lufthansa, Bridgestone, Ülker, Mondelēz International, BMW, Red Bull, Kinder, Michelin, Volvo, H&M, Kenzo, Sprite, Audi, Hyundai, Samsung, Xiaomi, Bosch, Pandora, KFC, Unilever, Lancôme, Visa, P&G. Do NOT add Porsche, Ferrari or Mercedes. Official SVGs only (citixmena.com assets or brand press kits), white monochrome; never trace or redraw; if unobtainable, use a labelled placeholder and list it.
- Hero budget v5 ≈ $9–12 on top of $19.53 already spent (project ≈ $29–32 of the $40 cap).
- Reference study of the bluesqx.com hero loop: `/docs/planning/bluesqx_motion_study.md` (frames stay outside the repo in `C:\Users\wassi\scratch\bluesqx_study\`, never committed or reused).
- Higgsfield via API (discounted models selected on the account): **Marketing Studio Image** (stills, up to 4K, image refs), **Kling 4.0** (first/last frame clips, 1080p), **Seedance 2.0** (up to 4K, backup). Read the docs (https://docs.higgsfield.ai and each model's page on open.higgsfield.ai) before writing API code; don't guess endpoints.
- Hero code stack: GSAP 3 + ScrollTrigger, Lenis, SplitType.
- Reusable scripts and assets: see "Reusable assets" at the end of the runbook copy.
- Stock: free Pexels clips only (Pexels License: commercial use and modification allowed). Licences logged in `/media/stock/LICENSES.md`.

## Creative freedom
You may rewrite and improve any Higgsfield prompt, parameter or approach (camera language, lens, lighting, motion, timing, shot split, model choice, number of variations, or code instead of generation) when you judge it gives a better film, website or animation, technically or creatively. Show the final prompt and a one-line reason per change before spending. The hard rules, brand guardrails, product accuracy, approval gates, formats and section handoffs are not negotiable.

## Website build standards
- Every visual has crawlable HTML text alongside it (SEO/GEO); one H1; semantic sections; EN + AR (RTL, hreflang).
- Video: MP4 (H.264) + WebM, poster image, end-frame still, lazy-loading, mobile-specific assets, `prefers-reduced-motion` fallback, sound off by default.
- Performance target: LCP < 2.5 s, CLS < 0.05; hero scripts paused when off-screen.
- 21st.dev components allowed if the licence permits; re-theme to the brand; avoid heavy dependencies for small effects.

## Archived (hero v4.2 rotations, replaced 14 Nov 2026 evening by plan v5 — kept for reference and asset reuse)
All stills and clips stay (`media/hero_orbit/stills/`, `clips/`, `seedance/`, `preview/`); delete nothing. Decisions as they stood:
- ~40 s loop of 5 product rotations, each = clip A (black → still) + clip B (still → black), same clockwise orbit (Kling first/last-frame method, later Seedance reference mode).
  - **R1 Tom** (old Tom, real refs, 1:3.5, red side strip): a falcon flies out toward the camera, sand swirling. Seedance R1 ref test + `orbit_lock.py` = `preview/seedance_R1_locked.mp4` (small residual wobble).
  - **R2 Jerry**: an oasis, palm fronds and water spilling onto the dunes.
  - **R3 Plain glass square**: a camel steps out; mist off Hajar-style mountains. Became the v5 model.
  - **R4 Corner glass pair**: two R3 panels joined at ~90° (convex, like a building corner); a perfume bottle rises from the seam.
  - **R5 Jumbo** (corner screen, two faces): an unbranded luxury SUV drifts out; the dust hits the hero frame (code overlay).

## Archived (intro film, dropped 14 Nov 2026 by plan v4.2 — kept for reference and asset reuse)
The intro film and gate are no longer built. All their assets stay (tag: reusable for products/about/projects sections + inner pages); delete nothing. Decisions as they stood:
- **Intro gate** (inspired by WOW Media's intro: muted looping film, Enter + Unmute, then the site). We copied the format, not their footage. Built in `components/IntroGate.tsx`, kept in the code but disconnected from the homepage route (Enter / Unmute / Skip, once per session, reduced-motion → straight to hero).
- **15 s loop** → Enter → **hero**: Tom (old Tom) alone, perfectly front-facing and centred against **sky only** (no street, buildings, ground or horizon; base touching the bottom edge), with a **day/night switch** (inspired by flyshare.design: sky transition, birds by day, opt-in sound). The film's last frame = the hero night frame (`media/generated/hero_test/intro_end_frame_reference_1920x1080.png`).
- Shot 2 is a **hard cut** after stock clip S4 to a street-level push-in on Tom (no continuous descent). Shot 5 lowers and tilts up from the street until only Tom and the sky remain (fallback: clean dissolve to the hero frame).
- Shot list and step-by-step prompts: `/docs/planning/CITIX_intro_ClaudeCode_prompts.md` and `CITIX_prompts_part2.md`; results in `docs/higgsfield-prompts.md` and `docs/higgsfield-map.md`; edit in `scripts/prompt3_edit.py`; exports in `media/web/intro-*`.
