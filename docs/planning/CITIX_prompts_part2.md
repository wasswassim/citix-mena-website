# CITIX MENA — Claude Code prompts, part 2 (12 Nov 2026)

Prompts 0–3 are in `docs/planning/CITIX_intro_ClaudeCode_prompts.md`. This file adds the missing steps: **1B** (finals of the chosen stills), **4** (hero day/night build) and **5** (preview link for the boss). Copy it to `docs/planning/` as well.

Full order: 1 → [review in claude.ai] → 1B → 2 → [review in claude.ai] → 3 → 4 → 5.

---

## PROMPT 1B — Final stills (after choosing drafts) — model: Fable 5.2

```
CONTEXT
Same project, CLAUDE.md rules. From the Prompt 1 drafts I choose:
  s2_end: <file>   s5_start: <file>   hero_night: <file>   hero_day: <file>
Changes requested: <list, or "none">

TASKS
1. Apply my requested changes. You may refine the prompts (creative freedom per CLAUDE.md),
   showing the final prompt and a one-line reason per change.
2. Quote the cost of the finals (per image and total) and wait for my OK.
3. Generate finals at full quality: 16:9 at least 1920x1080 (4K if the model allows at a
   reasonable cost), 21:9 for hero_night/hero_day, 9:16 at least 1080x1920.
4. hero_day and hero_night must share EXACTLY the same framing (same Tom position, scale,
   horizon). Check by overlaying them at 50% opacity; show me the overlay.
5. Compare each final against refs 01–07 again (proportions, calligraphy sides, logo,
   screen split) and list differences. Save to /media/generated/final/, update
   docs/higgsfield-map.md, commit the map (not the media). Stop.
```

---

## PROMPT 4 — Hero: Tom day/night (code) — model: Fable 5.2, Opus may use Sonnet sub-agents for routine parts

```
CONTEXT
Same project, CLAUDE.md rules. Approved stills: /media/generated/final/hero_day_* and
hero_night_* (16:9, 21:9, 9:16). The intro gate (Prompt 3) ends on hero_night; Enter must
reveal this hero with no visible cut.

REFERENCE (rebuild the effect, never copy their code or assets)
flyshare.design homepage, observed live 8 Nov: a central object over a full-screen sky; a
Night / Day two-button switch at the bottom; a ~5–7 s transition through dusk (starry dark
sky → pale-blue sky with soft clouds and a flock of birds) while the object turns and
changes material; a separate sound toggle (Web Audio, off by default, unlocked by a
click); hand-built canvas layers.
Also: CITIX 2D/day_night.mp4 (refs 09, 10): Tom's widget switching from day to night.

PLACEMENT
Page: homepage, section S1 (first section after the gate). Next section (S2 manifesto)
starts from inside Tom's screen: scrolling pushes the camera into the screen.
Layout: Tom centred (desktop: headline + sub-line + 2 CTAs on the left; mobile: below Tom).
Headline (H1, real HTML): "We make tomorrow happen today". CTAs: "Advertise with us",
"Partner with us" (Pulse Red). EN + AR ready (RTL).

BUILD
1. Ask me any missing Playbook §2 Step 3 question first.
2. Method per element (decide and explain in one line each; creative freedom per CLAUDE.md):
   - Tom: the approved day/night stills crossfaded in sync with the sky (or a short Kling
     day→night clip if you judge it better — quote the cost first).
   - Sky gradient, stars, clouds, birds (flocking): canvas/WebGL, code.
   - Tom's screen: real widgets composited in code (use ref 12 AQI style): top zone =
     time + weather (sun by day, moon by night), bottom zone = a neutral CITIX message
     (no third-party brands). Perspective-mapped onto the screen area.
   - Day/Night switch: two buttons bottom-centre, accessible, keyboard support.
     Default state follows the current time in the UAE (Asia/Dubai); the switch overrides it.
   - Transition ≈5 s, eased; dusk kept cool (no orange/yellow cast per brand rules).
   - Sound: off by default, toggle in the header; birdsong + soft wind by day, low city
     ambience by night; royalty-free files with free commercial licence (log in
     /media/stock/LICENSES.md) or Web Audio synthesis. Remember the choice.
   - Scroll handoff: push into Tom's screen (GSAP ScrollTrigger + Lenis or equivalent).
3. Performance: poster = hero_night still (LCP < 2.5 s), canvas paused when off-screen,
   mobile gets lighter layers (fewer birds/clouds, stills instead of clip).
4. prefers-reduced-motion: instant switch, no birds, no scroll push.
5. Crawlable text: H1, sub-line and CTAs as real HTML; alt text on stills.
6. Show me a local preview at desktop (1440) and mobile (390) widths, day and night, and
   record a short screen capture of the transition. Commit code (not raw media).
```

---

## PROMPT 5 — Preview link for the boss — model: Opus

```
CONTEXT
Same project. The homepage pitch (gate + hero, other sections as placeholders) must be
viewable by my boss via a link.

TASKS
1. Make sure all menu items and buttons link to a branded "Coming soon" page.
2. Compress final web media (/media/web/) and confirm sizes; only /media/web/ is committed.
3. Deploy a preview: Vercel (preferred, connect the GitHub repo; I log in myself if
   needed) or GitHub Pages. Add <meta name="robots" content="noindex"> on the preview so
   it isn't indexed before launch.
4. Run Lighthouse (mobile + desktop) and report Performance, Accessibility, SEO, LCP.
   Fix anything below 90 that is quick to fix.
5. Give me the preview URL and a 5-line summary I can send to my boss.
```
