# CITIX MENA Website — 3D & Animation Inspiration Playbook

Reference document for the CITIX MENA website rebuild. It lists the inspiration websites, what each one does (section by section), and the mandatory workflow for turning any referenced animation into a Higgsfield-generated asset via Claude Code.

Last reviewed: 4 Nov 2026. Analysis is based on each page's markup and asset names; motion that only runs in a live browser is marked **"verify live"**.

---

## 1. How to use this document

- When Wassim names an element ("the Apple start/end frame hero", "iCapital clouds", "Endurosat two-steps scroll"), find it in the **Element index (section 4)** to identify the source site and section.
- If the element is not in the index, or the description is ambiguous between two sites, **ask which site/section** before doing anything, then open that page (built-in browser preferred, WebFetch as fallback) to study it.
- Never invent how a reference animation behaves. If it is marked "verify live", open the page or ask for a screen recording before writing a prompt.

---

## 2. Mandatory workflow: reference → Claude Code prompt → Higgsfield asset

Every animation, scroll effect or 3D element goes through these five steps.

### Step 1 — Analyse the reference
Document, for the specific element:
- **Trigger:** autoplay on load, scroll-scrubbed (progress tied to scroll position), pinned/sticky section, hover, click/tab, drag.
- **Technique:** scroll-scrubbed video, image sequence, start-frame → end-frame transition, layered parallax (PNG/WebP layers), WebGL/3D model, CSS/text animation.
- **Camera & motion:** angle, move (orbit, dolly-in, pan, rise), speed, easing, duration.
- **Start frame and end frame:** what is on screen at 0% and 100%.
- **Lighting, palette, mood.**
- **What text/UI sits on top** of the motion and where.

### Step 2 — Decide: replicate or adapt
- **Replicate:** same animation, our product instead of theirs (e.g. Apple's laptop-opening hero → a CITIX smartboard powering on).
- **Adapt:** similar animation with modifications so it fits our layout, our section order, or our brand rules.

### Step 3 — Clarify before generating (Claude Code must ask)
The goal is a **continuous, uninterrupted funnel**: each animation's end frame must hand off cleanly to the next section. Claude Code must ask any of the following that are not already answered:

1. Which page and which section is this for? Which section comes **immediately before and after**?
2. How should the animation **end** — what is the exact end frame (product position, scale, angle, background)?
3. Where must the **product sit** in the final frame (centered or shifted right, per brand book) and how much empty space is needed for headline/CTA?
4. Which **CITIX product** is shown (see section 6 — names must be confirmed)?
5. Trigger type: autoplay loop, scroll-scrubbed, or pinned scroll?
6. Night scene or day scene? Real city environment or studio/void?
7. Target aspect ratios: desktop (16:9 / 21:9) and mobile (9:16 / 4:5)?
8. Is there real product photography / 3D renders / UI screenshots to use as the start frame, or must Higgsfield generate the product from scratch?
9. What is on the smartboard screen (real UI capture, campaign creative, widget)?

If an answer is missing and the user is not available, take the most reasonable option, state it at the top of the output, and keep the end frame neutral so it can be re-cut.

### Step 4 — Craft the Higgsfield prompt (via Claude Code)
Claude Code uses Higgsfield (through the integration configured in Claude Code — confirm it is connected before starting) to:
- **Generate stills** (start frame, end frame, background plates, layers for parallax).
- **Animate** a still into video, or **interpolate start frame → end frame** where the chosen model supports it.
- Produce **separate desktop and mobile versions** when framing differs.

Use the template in section 5.

### Step 5 — Integrate and check continuity
- The last frame of the clip must match the first visual state of the next section (same background colour/gradient, same product position if the product persists).
- Export a **poster image** (first frame) and **end-frame still** for fallbacks.
- Implement with performance in mind: compressed MP4/WebM (H.264 + VP9/AV1), or WebP image sequence for scroll-scrub; lazy-load below the fold; `prefers-reduced-motion` fallback to the static end frame; mobile-specific assets.
- Check against brand rules (section 7) before shipping.

---

## 3. Reference library

### 3.1 iCapital — https://www.icapital.es/en/
**What it is:** Spanish wealth-management firm; homepage is a single long scrollytelling journey.

**Verified from markup:**
- A `scrollytelling` asset folder with layered WebP images: `scene-01-back`, `scene-01-front`, repeated `clouds` layers, scenes 02–07 (mobile PNG versions), and `birds` sprites.
- Text beats appear one line at a time over the scenes: "The value is in the *journey*" → "decisions… demand *perspective*" → "set the *course*" → … each with one italic emphasis word.
- `scrolldriver-start` / `scrolldriver-end` images (light and dark variants) — a scroll indicator/progress element that changes at start and end.
- "Rotate your device — optimized for portrait mode" message: the experience is designed portrait-first.

**Technique:** multi-layer parallax (back plate, front plate, cloud layers moving at different speeds) driven by scroll, with scene-to-scene transitions through clouds, plus text reveals per scroll step. Exact easing and transitions: **verify live**.

**What to borrow for CITIX:** a "journey through the city" homepage — scroll flies through night-city layers (skyline back plate, streets mid plate, light-trail/fog layers in front) and lands on each smartboard format in turn (Jerry → Tom → Baloo → Simba, growing in scale). Single-word emphasis in headlines maps well to Gilroy ExtraBold + Pulse Red accent.

**Higgsfield role:** generate each parallax layer as a separate still with transparent or easily keyed background; optionally animate cloud/fog/light-trail layers as short loops.

---

### 3.2 EnduroSat — Space Service — https://www.endurosat.com/space-service/
**What it is:** satellite manufacturer; service page explaining a mission in "Two steps".

**Verified from markup:**
- Hero: "SPACE MISSIONS MADE SIMPLE", then Challenge → Solution statements.
- **"Your mission in Two steps"** block with a 0 → 6 months timeline, then a **"Scroll to continue"** pinned sequence: 01 Define (application selector with icon cards: remote sensing vs connectivity sub-types) → Mission Analysis & Design → Payload Integration → Launch & Commissioning → 02 Receive your data.
- Cloud ops hub section: Command / Monitor / Access.
- Tech section with live-style parameter readouts (Charge rate 4.2A, Data rate 100 Mbps, Tx power 30 dBm).
- Cost comparison: 3000 vs 1 USD/GB (Traditional vs EnduroSat), counters (234 satellites, 344M total mission cost).
- Social proof counters: 100 satellites, 500 TB, 900 years; 450+ customers; logo wall ending with a "You?" tile.
- A custom **"Drag"** cursor label (draggable element).

**Technique:** pinned scroll storytelling with step progression, animated counters, interactive selectors, dashboard-style data. 3D satellite visuals and exact transitions: **verify live**.

**What to borrow for CITIX:**
- "How it works in N steps" pinned section for B2B/B2G (e.g. Location → Installation → Citix Panel → Revenue/Data).
- Application selector → choose a use case (Smart City alerts, navigation, AdTech campaign, 3D creative) and the smartboard screen content changes.
- Animated counters for network stats; "Traditional billboard vs Citix" comparison; logo wall ending with a "You?" tile for partners.
- Citix Panel shown as a live dashboard (fits brand book "Transparency and analytics").

**Higgsfield role:** product hero shots per step, screen-content loops on the smartboard, transition clips between steps that end on the next step's product framing.

---

### 3.3 Rialto — https://rialto.com.au/
**What it is:** landmark Melbourne office tower (40-year anniversary); leasing site.

**Verified from markup (text only):** sections "A Melbourne icon" → "Ambition lives here" → wellbeing amenities → "A taste of success / The pulse of Midtown" → "A connected community" (Concierge, Portal) → "Rise to the occasion" (spaces) → Business Lounge → "A rich history" (timeline) → "Join an icon". The heading "ACONNECTEDCOMMUNITY" appears as split letters in the markup, suggesting per-letter text animation.

**Animation/3D details:** not exposed in markup — **verify live** before referencing (ask Wassim which effect he means, then open the page).

**What to borrow for CITIX (provisional):** architectural, premium real-estate tone — relevant to the landowner/developer audience (Simba on rooftops, Baloo spire on Tejara 1). Building-scale reveals and kinetic typography for big statements.

---

### 3.4 Flyshare — https://flyshare.design/
**What it is:** portfolio of designer Marc Fleischer.

**Verified from markup:**
- **Day / Night mode** is the core concept: day shows client work, night shows personal 3D projects.
- Own-work pages: **The Flyshare Universe** (planets, /universe/), **FS-45 Spaceship** (logo turned into a stealth spaceship, /fs45/), **The Transformation** (interactive switch between spaceship and transformer, /fs45/transform/).

**3D/interaction details:** live on the sub-pages — **verify live** on the specific page before referencing.

**What to borrow for CITIX:**
- **Day/Night toggle** for showing smartboards in both lighting conditions (brand book defines separate night and day scene rules).
- **Logo → object transformation**: the CITIX "X" morphing into a product (the brand book already places the X logo on the Baloo spire).
- Interactive state switch (like spaceship ↔ transformer) for screen modes: Smart City mode ↔ advertising mode.

**Higgsfield role:** paired day/night renders of the same framing (identical camera, only lighting changes) so the toggle crossfades cleanly; morph clip from X logo to product.

---

### 3.5 Apple — MacBook Pro with PROLED XDR display — https://www.apple.com/it/macbook-pro/proled-xdr-display/
**What it is:** Apple product page (Italian).

**Verified from markup:** almost every visual is delivered as a **`_startframe` / `_endframe` image pair** with a video between them: hero, highlights gallery (display, touch, chip, AI), product viewer (hero, display, touch), display section, touch hero, performance hero. Other patterns:
- Highlights **gallery/carousel** with tabs (Display, Touch, Chips, AI, Battery, Dynamic Island).
- **Product viewer** with tabbed views (size, colours, display, touch, audio, camera, connectivity) and an AR "view in your space" model (`.usdz`).
- Big-number stat blocks (2000 nits, 10,000,000:1).
- Tabbed comparison charts (bars vs previous generations).
- Tabbed workflow showcase (AI, coding, photo, video, 3D, music, gaming), each with a screen image.

**Technique:** short pre-rendered videos that play from a defined start frame to a defined end frame when the section enters view (or on tab change); the end frame is held as a static image. This is the **exact pattern Higgsfield start/end-frame generation supports** — the most directly reproducible reference in this list.

**What to borrow for CITIX:**
- Hero: smartboard in a night street, screen off (start) → screen powers on with campaign content, light spills onto pavement (end).
- Product viewer with tabs per product: sizes (Jerry → Simba scale), screen modes, Smart City widgets, Citix Panel.
- Big-number stat blocks (screen size, brightness, network reach).

---

### 3.6 Apple — MacBook Pro with Liquid Retina XDR display — https://www.apple.com/it/macbook-pro/liquid-retina-xdr-display/
**Verified from markup:** same start/end-frame system. Hero is notable: a laptop seen from the side **rearranges into the shape of a "6"** (for the M6 chip) — product becomes a symbol. Product viewer (hero, sizes, chips, colours, display, connectivity, camera, audio, durability), performance hero, Cinema 4D render start/end, a "three chips" switcher, privacy icon start/end, display stats list, ports diagram.

**What to borrow for CITIX:** product-as-symbol transitions — e.g. the smartboard lineup arranging into the **X** of the logo, or a screen sequence forming "CITIX". Size-comparison viewer for the naming system (Jerry 2.6 m² → Simba ≈101 m²).

---

### 3.7 Microsoft — Surface Laptop Ultra — https://www.microsoft.com/en-us/surface/devices/surface-laptop-ultra
**Verified from markup:**
- Hero: autoplay **MP4 video** (desktop) with a static **poster image** for mobile; headline "The new shape of power".
- **"Inner craft. Outer beauty."** — three scroll-driven slides, each its own video (desktop) and poster (mobile).
- Feature cards with short videos (magnetic charging, haptics, ports).
- **Display section with Morning / Afternoon / Evening tabs**, each switching a video of the same device in different light.
- Local AI section: three videos (Build / Create / Analyze).
- Security cards, product family carousel, anchor sub-nav (Performance, Display, Local AI, Security, Specs), FAQ.

**What to borrow for CITIX:**
- **Time-of-day tabs** for smartboards: show the same screen at morning / afternoon / night — proves brightness/visibility and matches the brand's night-city aesthetic.
- Scroll "craft" slides for build quality: materials, frame, screen surface, installation.
- Desktop video + mobile poster pattern for performance.
- Product family carousel for the full lineup.

---

## 4. Element index (quick lookup)

| If Wassim says… | Source | Section |
|---|---|---|
| start/end frame hero, product video that stops on a still | Apple (both pages) | Hero, highlights, product viewer |
| product turns into a number/shape/logo | Apple Liquid Retina | Hero ("6") |
| product viewer, tabs for sizes/colours | Apple (both) | Product viewer |
| AR / view in your space | Apple (both) | Design / product viewer |
| big stats, comparison bars | Apple PROLED; EnduroSat | Display numbers; cost of data |
| parallax layers, clouds, birds, journey scroll | iCapital | Homepage scrollytelling |
| one emphasised italic word per headline | iCapital | Headlines |
| pinned "scroll to continue" steps, timeline | EnduroSat | "Two steps" |
| application selector / configurator | EnduroSat | 01 Define |
| counters, logo wall ending with "You?" | EnduroSat | Flight heritage / Trusted by |
| drag cursor | EnduroSat | (verify live) |
| day/night mode toggle | Flyshare | Homepage |
| logo becomes a 3D object / transformation | Flyshare | FS-45 pages (verify live) |
| morning/afternoon/evening tabs | Microsoft | Display ("Shines in any setting") |
| scroll craft slides, video per slide | Microsoft | "Inner craft. Outer beauty." |
| building / architectural reveal, split-letter headings | Rialto | (verify live) |

Anything not listed → ask which site and section.

---

## 5. Claude Code prompt template (Higgsfield)

```
CONTEXT
Project: CITIX MENA website. Brand rules: see brand book (colours #000000, #161616, #FFFFFF,
#E0E0E0, accent Pulse Red #FD0332; Gilroy ExtraBold / Light; night-city, high contrast,
no sci-fi, no neon/oversaturated or warm tones; smartboard is the focal point, centered
or shifted right).

REFERENCE
Site + section: <e.g. Apple PROLED XDR — hero start/end frame>
What it does: <trigger, technique, camera move, duration, start frame, end frame>
Mode: <replicate | adapt> — changes: <list>

PLACEMENT
Page/section: <...>   Previous section ends on: <...>   Next section starts with: <...>
Required end frame: <product, position, scale, angle, background colour, empty area for copy>
Trigger: <autoplay | scroll-scrubbed | pinned scroll | tab>   Duration: <s>
Formats: desktop <16:9/21:9>, mobile <9:16/4:5>

PRODUCT
Product: <confirmed CITIX product name + real dimensions>
Inputs available: <photos / renders / UI captures / none>
On-screen content: <...>

TASKS
1. Ask me any missing question from Playbook §2 Step 3 before generating.
2. Generate start frame and end frame stills in Higgsfield (both formats).
3. Generate the transition clip start → end (or animate the still).
4. Deliver: MP4 + WebM, poster (first frame), end-frame still, file sizes.
5. Implement in the section with reduced-motion fallback and confirm the end frame
   matches the next section's first state.
```

---

## 6. CITIX product reference (confirm names before use)

Two naming sources currently disagree — **confirm with the tutor before any product appears in an animation or label.**

- **Screen naming deck (updated):** Jerry 2.6 × 1 m (pedestrian), Tom 7 × 2 m (roadside), Baloo 8 × 4 m (architectural spire, X logo, Tejara 1), Simba 18.7 × 5.4 m (rooftop panoramic), Jumbo (reserved, TBD), Manny ≈12 × 6 m corner facade (alternatives: Lino, Gloria), Monstro largest future format (alternative: Baymax).
- **Brand book product list:** Tom Tom (roads), Shark (streets in motion), Jerry (pedestrians), XONE (indoor), Smart Space (gas stations), Smart Box (connect any screen), Jumbo (3D experiences), Smart Pillar, plus Citix Platform/Panel.

---

## 7. Brand guardrails every animation must pass

- **Palette:** Midnight Black #000000, Graphite Shadow #161616, Pure Snow #FFFFFF, Urban Mist #E0E0E0, Pulse Red #FD0332 (gradients per brand book, e.g. #FD0332 → #990332).
- **Type:** Gilroy ExtraBold (headings), Gilroy Light (body).
- **Look:** digitally enhanced *real* city, "the future is already part of the city". Night: high contrast, light trails, defined artificial light. Day: realistic daylight, clean, minimal noise. Overcast OK if clear.
- **Avoid:** sci-fi, abstract CGI, neon/acid or overly saturated colours, warm/yellowish tones, digital noise, cluttered compositions, staged static people, competitor-like aesthetics, recognisable specific cities.
- **People/vehicles:** motion-blurred only.
- **Camera:** smooth, cinematic. Smartboard = main subject, centered or shifted right; background softly blurred.
- **UI on screens:** prefer real UI captures; if composited, plan tracking.
- **Logo:** never in the bottom-right corner of a frame/post; respect clear space (height of the "X"); never stretched, tilted, outlined-only or gradient-filled.
- **Tone of copy:** confident, action-driven, concrete benefits; no startup clichés.
