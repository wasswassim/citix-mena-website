# CITIX MENA — Intro film: Claude Code prompts (v1, 12 Nov 2026)

Model per prompt: **Prompt 0 → Opus** · **Prompts 1–2 → Fable 5.2** · **Prompt 3 → Fable 5.2** (edit + gate build), Opus may take over routine parts and use Sonnet sub-agents.

Run these **in order**, one at a time, in Claude Code. Prompt 0 creates the repo itself. Each prompt stops and waits for your approval before anything costs money. Plan reference: Project doc `Intro_Film_Plan.md`; brand rules: `3D_Animation_Inspiration_Playbook.md` §7.

Shot list used by all prompts (15 s loop, desktop 16:9 + mobile 9:16):

| # | Time | Shot | Source | Overlay (code) |
|---|---|---|---|---|
| 1 | 0–2.5 s | Drone over Flag Island, Sharjah, dusk | Pexels S1 | SMARTER CITIES. |
| 2 | 2.5–5 s | From the last frame of the Sharjah road drone shot, the camera descends to roadside level where the new Tom stands lit | Pexels S4 → Higgsfield Kling 4.0 (first/last frame) | — |
| 3 | 5–8 s | Baloo: the car bursts out of the corner screen | Real 4K footage | STRONGER BRANDS. |
| 4 | 8–10.5 s | Jumbo: the perfume 3D content | Real footage | — |
| 5 | 10.5–15 s | Tom at night: the screen powers on, then the camera tilts up until Tom stands alone against the night sky = **hero night frame** (held) | Higgsfield Kling 4.0 (first/last frame) | WE MAKE TOMORROW HAPPEN TODAY + Enter |

---

## PROMPT 0 — Set up the asset pipeline (no generation, no cost)

```
CONTEXT
Project: CITIX MENA website (homepage pitch). We are producing a 15-second intro film
that plays as a gate before the hero (WOW Media-style: muted loop, Enter + Unmute).
Brand rules: colours #000000, #161616, #FFFFFF, #E0E0E0, accent Pulse Red #FD0332;
Gilroy ExtraBold / Light; real city, high contrast, no sci-fi, no neon or warm/yellow
tones; smartboard is the focal point, centered or shifted right.

TASKS
0. Create the project folder and memory:
   - Create C:\Users\wassi\Projects\citix-mena-website (outside the Internship folder) and
     work only there from now on.
   - Copy C:\Users\wassi\Desktop\DOCS\Internship\07_Website_Project_Docs\claude_code_kit\CLAUDE.md to the repo root,
     read it fully and follow it for the whole project.
   - Copy into /docs/planning/: 07_Website_Project_Docs\claude_code_kit\CITIX_intro_ClaudeCode_prompts.md and
     C:\Users\wassi\Desktop\DOCS\Internship\07_Website_Project_Docs\3D_Animation_Inspiration_Playbook.md.
   - Check git, Node.js (LTS), Python 3, ffmpeg and GitHub CLI (gh) are installed; install
     missing ones with winget and tell me what you installed.
   - git init, then ask me for my GitHub repo URL (or offer to create a private repo with
     `gh repo create` — I run `gh auth login` myself if needed). Create a README.md
     describing the structure below.
1. Create this structure in the repo (keep raw media out of git; add to .gitignore):
   /media/source/        originals (not committed)
   /media/stock/         free stock clips (not committed)
   /media/generated/     Higgsfield outputs (not committed)
   /media/web/           compressed web deliverables (committed later)
   /docs/higgsfield-map.md   mapping table (committed)
   /scripts/             helper scripts
2. Copy these files from C:\Users\wassi\Desktop\DOCS\Internship\ into /media/source/
   (keep names):
   - 06_Photos_and_AI_References\Higgsfield_candidates\01_tom_day_photo.jpg … 11_ramadan2_night_mood.png (01–11)
   - 06_Photos_and_AI_References\Higgsfield_candidates\12_AQI_widget_ui.png (code use only, do NOT upload)
   - 03_Product_Videos\Baloo\Média1pptx_s18_baloo_3d_video.mp4  → rename baloo_3d_real_4k.mp4
   - 03_Product_Videos\Jumbo\Média1pptx_s20_jumbo_3d_video.mp4  → rename jumbo_3d_real.mp4
3. Download the two free Pexels clips (Pexels License: free commercial use, modification
   allowed, no attribution required) into /media/stock/, highest resolution available:
   - S1 Flag Island, Sharjah: https://www.pexels.com/video/drone-footage-of-flag-island-8396981/
   - S4 Sharjah road at dusk: https://www.pexels.com/video/aerial-view-of-modern-urban-landscape-5769445/
   If the download needs a browser click, tell me and I'll download them manually.
   Save a licence note (URL, author, date, "Pexels License") in /media/stock/LICENSES.md.
4. Check ffmpeg/ffprobe are installed (install if missing). Print a table of every file
   in /media/source and /media/stock: resolution, fps, duration, size.
5. Extract 6 evenly spaced frames from each stock clip to /media/stock/review/ and show me
   any frame with readable logos, brand names or identifiable faces.
6. Higgsfield API setup — create the environment files yourself:
   a. Read the Higgsfield auth docs first (https://docs.higgsfield.ai) to find the exact
      variable names the API needs (key only, or key + secret).
   b. Create .gitignore entries FIRST: .env, .env.local, /media/source/, /media/stock/,
      /media/generated/ — and confirm with `git check-ignore .env` that .env is ignored.
   c. My API credentials are in this text file:
        C:\Users\wassi\Desktop\DOCS\Internship\857b9f1a-55b7-4a06-aef1-873379bb5ef.txt
      Read it with a script and write the value(s) into .env WITHOUT ever displaying them
      (no cat/type/echo of the file or of .env, no printing in the terminal, no logging).
      If the file holds a key and a secret, map them to the variable names from the docs;
      if it's unclear which line is which, ask me which line is which (by line number
      only), never show the content. Final .env layout:
        HIGGSFIELD_API_KEY=<from file>
        HIGGSFIELD_API_SECRET=<from file, only if the docs require it>
        HIGGSFIELD_MAX_SPEND_USD=10      (scripts refuse any job above this)
   d. Create .env.example with the same variable names and empty values (this one IS
      committed, as documentation).
   e. Test the connection with a free/read-only call (e.g. balance or model list) and
      report success or the error. Never commit .env.
   f. After a successful test, ask me: "Delete the plain-text key file now?" and delete
      C:\Users\wassi\Desktop\DOCS\Internship\857b9f1a-55b7-4a06-aef1-873379bb5ef.txt only
      after I say yes (the key then lives only in .env). Make sure that .txt file is
      never copied into the repo.
   g. Read the official docs before writing any API code — start at https://docs.higgsfield.ai
   and each model's own API page on open.higgsfield.ai:
     - Marketing Studio Image  (open.higgsfield.ai/models/marketing-studio/image)
     - Kling 4.0               (open.higgsfield.ai/models/kling-video/v4.0)
     - Seedance 2.0            (open.higgsfield.ai/models/bytedance/seedance-2.0)
   Do not guess endpoints or parameters. Write /scripts/higgsfield.(py|ts) with:
   upload(file) → asset id, generate(model, params) → job, wait(job), download(result),
   and a cost/quote step if the API offers one.
7. Upload files 01–11 to Higgsfield (uploads only, no generation). Fill /docs/higgsfield-map.md:
   | Local file | Higgsfield asset ID | Intended use |
   Intended uses:
   01, 02 → Tom shape/proportions (day / night)
   03, 04, 05 → NEW Tom design: Arabic calligraphy on the side panels (replaces side light)
   06 → calligraphy pattern detail
   07, 08 → materials, screen frame, angles
   09, 10 → day/night screen-switch reference
   11 → night street mood, light trails
8. Stop and report: file table, frame review, mapping table. Do not generate anything.
```

---

## PROMPT 1 — Draft key stills (Marketing Studio Image) — quote first

```
CONTEXT
Same project and brand rules as before. Use /docs/higgsfield-map.md for asset IDs.
Product: TOM (roadside smartboard, 7 m tall x 2 m wide, vertical totem; screen split:
top = info widget, bottom = advertising). NEW VERSION: the side panels carry an engraved
Arabic calligraphy pattern (see refs 03, 04, 06) instead of a side light strip. Keep the
real proportions, frame, CITIX logo position (top) and screen split from refs 01, 02, 07.
Never invent extra parts, text or logos. Screen must be BLANK, plain dark grey (we add
real widgets and ads in code later) unless stated otherwise.

REFERENCE
Apple start/end-frame method (Playbook §3.5) and WOW Media intro (Playbook §3.8).

CREATIVE FREEDOM (model: Fable 5.2)
The descriptions below are a starting brief, not final Higgsfield prompts. Rewrite and
improve them as you judge best for the film, the website and the animations, technically
and creatively: wording, camera, lens, lighting, composition, negative prompts, seeds,
resolution, number of variations, model choice, or a different shot idea that serves the
handoffs better. Before spending, show me each final prompt with a one-line reason per
change. Non-negotiable: CLAUDE.md hard rules, brand guardrails, product accuracy, formats,
and the start/end frames that connect the shots.

TASKS
1. Ask me any missing question from Playbook §2 Step 3 before generating.
2. Before generating, give me the cost per image and the total. Wait for my OK.
3. Generate DRAFTS (lowest resolution that still shows detail), 2 variations each:
   A. "s2_end"  — Shot 2 end frame. Start from the LAST frame of /media/stock/S4 (extract
      it): the same Sharjah road at dusk, camera lowered to about 3 m above the ground,
      the new Tom standing on the roadside verge, screen glowing (blank), traffic
      motion-blurred, cool blue-hour grading. Tom placed right of centre.
      Formats: 16:9 and 9:16.
   B. "s5_start" — Shot 5 start frame. Night street in Sharjah (wide road, palms,
      low-rise buildings, no mosque, no landmark), the new Tom at eye level, screen OFF
      (black), soft street light, light trails behind. 16:9 and 9:16.
   C. "hero_night" — Shot 5 end frame AND the hero night state. Low camera angle, Tom
      alone and centred against a clear deep blue-black night sky with faint stars,
      ground barely visible at the bottom, screen ON (blank glow), subtle Pulse Red accent
      on the frame. Empty space left of Tom for the headline (desktop) and below (mobile).
      16:9, 21:9 and 9:16.
   D. "hero_day" — EXACTLY the same framing as C, daytime: clear blue sky, soft clouds,
      realistic daylight. 16:9, 21:9 and 9:16. (Used later for the day/night hero.)
4. Save to /media/generated/drafts/ with clear names, add them to the mapping table, then
   build one contact sheet image of all drafts and show it to me.
5. Check every draft against refs 01–07 (proportions, calligraphy sides, logo position,
   screen split) and list any differences you see. Stop and wait for my choice.
```

---

## PROMPT 2 — Clips (Kling 4.0 first/last frame) — after I approve the stills

```
CONTEXT
Same project and rules. Approved stills: <I will list the chosen files>.

CREATIVE FREEDOM (model: Fable 5.2)
Same as Prompt 1: improve the motion prompts, durations, camera moves, model choice
(Kling 4.0 / Seedance 2.0) or split as you judge best for the film and the hero handoff.
Show the final prompts and a one-line reason per change before spending.

TASKS
1. Give me the cost per second and total before generating. Wait for my OK.
2. Clip "s2": Kling 4.0 first/last frame. First frame = last frame of /media/stock/S4.
   Last frame = approved "s2_end". Smooth cinematic drone descent, no cuts, no morphing of
   buildings, Tom must stay identical to the reference. 3 s. 16:9 and 9:16.
3. Clip "s5": first frame = approved "s5_start", last frame = approved "hero_night".
   Tom's screen powers on (glow appears), camera tilts up and pushes in slightly until the
   framing matches "hero_night" exactly. 4.5 s. 16:9 and 9:16.
4. Generate 2 variations each as drafts, extract 6 frames per clip into a contact sheet,
   flag any frame where Tom changes shape or the background warps. Stop for my choice.
5. If Kling keeps altering Tom, try Seedance 2.0 with the same frames and compare.
```

---

## PROMPT 3 — Edit, export and build the gate (code) — after clips are approved

```
CONTEXT
Same project and rules. Approved clips: s2, s5 (files: <…>). Real footage:
baloo_3d_real_4k.mp4 (use ≈5.0–8.0 s, skip the warm sunset ad around 17 s),
jumbo_3d_real.mp4 (use ≈2.5 s that best shows the 3D bottle).

TASKS
1. Assemble the 15 s film with ffmpeg following the shot list (S1 0–2.5 s, s2 2.5–5 s,
   Baloo 5–8 s, Jumbo 8–10.5 s, s5 10.5–15 s). Short crossfades (≤ 8 frames) only where
   the motion needs it; otherwise hard cuts on the beat. Grade all shots to a common cool,
   high-contrast look (no warm/yellow cast). The last frame must equal hero_night exactly
   so the loop end hands off to the hero.
2. Exports to /media/web/: intro-desktop.mp4 (H.264, 1920x1080) + .webm (VP9/AV1),
   intro-mobile.mp4 + .webm (1080x1920, centre the subject in each shot), poster.jpg
   (first frame), end.jpg (last frame = hero_night). Target ≤ 4 MB mobile, ≤ 8 MB desktop;
   report sizes.
3. Music: suggest 3 royalty-free tracks (Pixabay Music or similar free-commercial licence),
   ambient/cinematic, no vocals; I choose; mix it in a separate audio-only track loaded
   only when the user clicks Unmute. Log the licence in /media/stock/LICENSES.md.
4. Build the gate component (Playbook §5 template, method = code):
   - full-screen overlay over the real homepage (homepage HTML stays in the DOM and
     crawlable), muted autoplay loop, playsinline, poster first, video lazy-loaded
   - CITIX logo top-left (never bottom-right), overlay text as real HTML (SMARTER CITIES. /
     STRONGER BRANDS. / WE MAKE TOMORROW HAPPEN TODAY) timed to the shots, Gilroy, EN + AR
     ready (RTL)
   - buttons: Enter (Pulse Red), Unmute, Skip; Enter fades the overlay into the hero
     night state; show once per session (sessionStorage)
   - prefers-reduced-motion → no gate, straight to the hero end frame
   - keyboard accessible, focus visible, aria labels
5. Show me the result in a local preview, desktop and mobile widths.
```
