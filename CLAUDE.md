# CITIX MENA website — project memory for Claude Code

Owner: Wassim Gatri (intern, CITIX MENA). Goal: a **homepage pitch** for the new CITIX MENA website (citixmena.com) with modern 3D, scroll and video effects, strictly on-brand. Other pages are "coming soon" placeholders until the homepage is approved. Code lives in Wassim's personal GitHub. Design is shared in Figma.

Planning happens in a claude.ai Project ("CitiX MENA Internship"); copies of the key docs are in `/docs/planning/`. If something here conflicts with a newer instruction from Wassim, follow Wassim.

## Model routing
- **Fable 5.2**: writing and refining Higgsfield prompts, and the hardest creative-technical parts (hero day/night scene, intro film edit, 3D/WebGL, scroll choreography).
- **Opus**: everything else (setup, scripts, components, SEO, QA). Opus may launch **Sonnet sub-agents** for parallel, well-scoped tasks (file inventories, frame extraction, compression, tests, lint, docs). Sub-agents never spend Higgsfield credits and never touch `.env`.

## Hard rules (never break)
1. **Secrets:** API keys live only in `.env` (git-ignored). Never print, log, echo, `cat`/`type` or commit them. Never ask for keys in chat.
2. **Spending:** before any Higgsfield generation, show the price per unit and the total, then wait for Wassim's OK. Scripts refuse any job above `HIGGSFIELD_MAX_SPEND_USD` in `.env`.
3. **Approval gates:** drafts first (low res, 2 variations), show a contact sheet, wait for a choice, then finals.
4. **Product accuracy:** never invent CITIX products, parts, logos or text. Build every product from the reference files and list any differences after each generation.
5. **No reuse of others' work:** don't copy code or assets from inspiration sites (flyshare.design, wowmedia.com, apple.com…). Rebuild the effect ourselves.
6. **Landmarks:** no Burj Khalifa, Burj Al Arab or other owned landmarks as a subject (Emaar's asset policy covers CGI too). No mosques as a framed subject. No identifiable people.
7. **Don't delete user files** without asking. Never copy the plain-text key file into the repo.

## Brand guardrails (brand book)
- Colours: Midnight Black #000000, Graphite Shadow #161616, Pure Snow #FFFFFF, Urban Mist #E0E0E0, **Pulse Red #FD0332** (gradient #FD0332 → #990332).
- Type: **Gilroy ExtraBold** (headings), **Gilroy Light** (body).
- Look: a *real* city enhanced by CITIX ("the future is already part of the city"). Night: high contrast, light trails, defined artificial light. Day: realistic daylight, clean, minimal noise.
- Avoid: sci-fi, abstract CGI, neon/acid or oversaturated colours, warm/yellowish tones, digital noise, clutter, staged static people (motion-blurred only), competitor-like aesthetics.
- Smartboard = main subject, centred or shifted right. Smooth, cinematic camera.
- Logo: never bottom-right; clear space = height of the "X"; never stretched, tilted, outlined-only or gradient-filled.
- Copy tone: confident, action-driven, concrete benefits, no startup clichés. Slogans: "Smarter cities. Stronger brands." / "We make tomorrow happen today."
- Exception approved for now: real city names (Sharjah, Abu Dhabi) may appear. Wassim will review this with his supervisor.

## Products (sales deck — some sizes still to confirm)
- Street smartboards: **Jerry** (pedestrian, 2.6 × 1 m), **Tom** (roadside, 7 × 2 m vertical totem; screen split: top = info widgets, bottom = ad), **Smart Pillar** (petrol stations).
- Giant 3D screens: **Baloo** (corner spire, Tejara 1), **Simba**, **Jumbo** (largest corner screen, premium mall). Software: **Citix OS**.
- **New Tom:** engraved **Arabic calligraphy pattern on the side panels** instead of the side light strip (refs 03, 04, 06). No full view of the new Tom exists yet; the team may send a 3D model. When it arrives, rebuild Tom references from it.
- Smartboard logic: widgets on top catch the eye like a phone notification, the ad sits below. Eye-tracking study: +53% conversion vs standard billboards.
- Real installations: Yas Island entrances, Abu Dhabi (first 2 Tom); Sharjah (Shurooq partnership: Al Qasba, Al Heera Beach, Flag Island, Khorfakkan…); Jumbo at an Abu Dhabi mall.

## Current workstream: intro film + hero
- **Intro gate** (inspired by WOW Media's intro: muted looping film, Enter + Unmute, then the site). We copy the format, not their footage.
- **15 s loop** → Enter → **hero**: the new Tom alone in the centre under the sky, with a **day/night switch** (inspired by flyshare.design: sky transition, birds by day, opt-in sound). The film's last frame = the hero night frame.
- Shot list and step-by-step prompts: `/docs/planning/CITIX_intro_ClaudeCode_prompts.md`.
- Higgsfield via API (discounted models selected on the account): **Marketing Studio Image** (stills, up to 4K, image refs), **Kling 4.0** (first/last frame clips, 1080p), **Seedance 2.0** (up to 4K, backup). Read the docs (https://docs.higgsfield.ai and each model's page on open.higgsfield.ai) before writing API code; don't guess endpoints.
- Stock: free Pexels clips only (Pexels License: commercial use and modification allowed). Licences logged in `/media/stock/LICENSES.md`.

## Creative freedom
You may rewrite and improve any Higgsfield prompt, parameter or approach (camera language, lens, lighting, motion, timing, shot split, model choice, number of variations, or code instead of generation) when you judge it gives a better film, website or animation, technically or creatively. Show the final prompt and a one-line reason per change before spending. The hard rules, brand guardrails, product accuracy, approval gates, formats and section handoffs are not negotiable.

## Website build standards
- Every visual has crawlable HTML text alongside it (SEO/GEO); one H1; semantic sections; EN + AR (RTL, hreflang).
- Video: MP4 (H.264) + WebM, poster image, end-frame still, lazy-loading, mobile-specific assets, `prefers-reduced-motion` fallback, sound off by default.
- Performance target: LCP < 2.5 s; hero and gate scripts paused when off-screen.
- 21st.dev components allowed if the licence permits; re-theme to the brand; avoid heavy dependencies for small effects.
