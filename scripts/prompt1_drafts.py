"""Prompt 1 drafts: 20 key stills with Marketing Studio Image (approved by Wassim 2026-11-12).

Usage:
  python scripts/prompt1_drafts.py quote          # free: total quote, no generation
  python scripts/prompt1_drafts.py run --yes      # submit, wait, download (resumable)

State is kept in media/generated/drafts/jobs.json so a re-run never pays twice for a
job that was already submitted. Refuses to start if the total quote exceeds BUDGET_USD.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import higgsfield as hf  # noqa: E402

MODEL = "marketing-studio/image"
BUDGET_USD = 2.40  # approved: about $2.15
OUT = hf.ROOT / "media" / "generated" / "drafts"
STATE = OUT / "jobs.json"
SRC = hf.ROOT / "media" / "source"
BASE = {"resolution": "2k", "quality": "medium", "enhance_prompt": False}

TOM = (
    'PRODUCT — must match the reference images exactly, do not redesign it: the CITIX "Tom" roadside '
    "smartboard, a tall, slim vertical totem about 7 m high and 2 m wide with a thin flat profile and a "
    "matte black / graphite metal body. The front face holds two stacked portrait screens of nearly equal "
    "height with rounded corners, separated by a thin black gap (upper screen = information zone, lower "
    "screen = advertising zone). A small, completely plain black cap sits on the top edge toward the "
    "right, with one round camera lens and no text or logo on it. The totem stands on a narrower plain "
    "dark rectangular plinth set toward the right under the body. The narrow side panels are matte black "
    "metal with flowing Arabic calligraphy engraved in low relief, running vertically along the full "
    "height as in the calligraphy references. There is NO light strip on the sides. No other text, logos, "
    "stickers, antennas, brackets or added parts."
)
AVOID = (
    "Avoid: warm, orange or yellow tones; neon, acid or oversaturated colours; sci-fi or futuristic "
    "styling; abstract CGI look; lens flares, fog, digital noise, clutter; mosques, domes, minarets or "
    "famous landmarks; identifiable people; billboards or other signage; any text, lettering, wordmark or "
    "logo anywhere in the image, including on the totem's top cap; any light strip on the sides of the "
    "totem; any content, text or image on the screens."
)

A = (
    "Photorealistic cinematic photograph, blue hour just after sunset in Sharjah, UAE. Reference image 6 "
    "is an aerial frame of this exact road at blue hour: keep the same straight dual carriageway with "
    "palm-lined grass verges, the same cluster of waterfront high-rise towers in the distance and the "
    "same light and colour, but the camera has now descended to about 3 m above the ground at the "
    f"roadside, looking along the road toward the skyline. {TOM} It stands on the grass verge beside the "
    "road, placed right of centre (around the right third of the frame), full height visible from plinth "
    "to cap with headroom above, seen from a slight three-quarter angle so the front screens and one "
    "engraved side panel are visible. Both screens are switched ON but blank: an even, soft, neutral "
    "cool-white glow with no content, spilling faintly onto the verge. Traffic passes as motion-blurred "
    "streaks with white and red light trails; no readable plates, no people. Cool blue-hour grade: deep "
    "blue sky, clean high contrast, crisp defined artificial light, neutral-cool white balance. 35 mm "
    f"lens, shallow depth of field so the skyline is softly out of focus. {AVOID}"
)
A_V = " Vertical composition: the totem fills about 70% of the frame height, slightly right of centre, the road receding on the left."

B = (
    "Photorealistic cinematic photograph at night on a wide, quiet road in Sharjah, UAE: palm trees, "
    "low-rise modern buildings in the background softly out of focus, clean pavement. Eye-level camera "
    f"(about 1.7 m), level horizon, 35 mm lens. {TOM} It stands on the roadside, centred in the frame, "
    "full height visible from plinth to cap, seen almost front-on with a very slight three-quarter turn "
    "so one engraved side panel catches the light. Both screens are switched OFF: pure black glass with "
    "only faint reflections of the street lights. Soft, cool white street lighting defines the edges of "
    "the totem and the engraved calligraphy; behind it, long white and red light trails from passing "
    "traffic. Deep blue-black sky taking the upper third of the frame. High contrast, clean, neutral-cool "
    f"white balance. {AVOID}"
)
B_V = " Vertical composition: the totem centred, filling about 65% of the frame height, sky above."

C = (
    "Photorealistic cinematic photograph at night. Low camera, about 1 m above the ground and well back "
    "from the subject, tilted slightly upward, long lens so the vertical edges stay almost parallel with "
    f"minimal perspective distortion. {TOM} It stands alone, exactly centred in the frame, VIEW, against "
    "a clear, deep blue-black night sky with faint, sparse stars; no buildings, no trees, nothing else in "
    "the sky. Only a thin strip of dark ground is visible at the very bottom of the frame. Both screens "
    "are switched ON but blank: an even, soft, neutral cool-white glow with no content. A faint cool rim "
    "light defines the edges of the body and the engraved calligraphy. Large, clean, empty sky on both "
    f"sides of the totem, especially on the left, for a headline. High contrast, clean, no noise. {AVOID}"
)
C_VIEW = {
    1: "seen straight front-on",
    2: "seen from a slight three-quarter angle (about 20 degrees) so one engraved calligraphy side panel is clearly visible",
}
C_V = " Vertical composition: the totem centred in the upper two thirds of the frame; the lower third is dark, empty ground and sky gradient for text."

D = (
    "Edit reference image 1 into the identical scene in daytime. Keep the camera, framing, the totem's "
    "position, scale, angle and every edge, and the horizon line exactly as they are. Change only the "
    "light and the sky: a clear blue sky with a few soft white clouds, realistic neutral daylight, soft "
    "natural shadows, the thin ground strip lit by daylight. The screens stay switched ON and blank with "
    "the same neutral glow, naturally less bright against daylight. Use reference image 2 only for how "
    f"the matte black body looks in real daylight. Clean, realistic, minimal noise. {AVOID}"
)

PRODUCT_REFS = ["01_tom_day_photo.jpg", "02_tom_night_photo.jpg", "05_TOM_full_silhouette.png",
                "04_TOM_calligraphy_side_b.png", "06_JERRY_calligraphy_side.png"]


def tag(ar: str) -> str:
    return ar.replace(":", "x")


def build_stage1() -> dict:
    refs = [hf.upload(SRC / n) for n in PRODUCT_REFS]
    s4 = hf.upload(OUT / "S4_last_frame_bluehour.jpg")
    jobs = {}
    for v in (1, 2):
        for ar in ("16:9", "9:16"):
            vert = ar == "9:16"
            jobs[f"s2_end_{tag(ar)}_v{v}"] = {**BASE, "aspect_ratio": ar, "prompt": A + (A_V if vert else ""),
                                              "image_urls": refs + [s4]}
            jobs[f"s5_start_{tag(ar)}_v{v}"] = {**BASE, "aspect_ratio": ar, "prompt": B + (B_V if vert else ""),
                                                "image_urls": refs}
        for ar in ("16:9", "21:9", "9:16"):
            jobs[f"hero_night_{tag(ar)}_v{v}"] = {**BASE, "aspect_ratio": ar, "image_urls": refs,
                                                  "prompt": C.replace("VIEW", C_VIEW[v]) + (C_V if ar == "9:16" else "")}
    return jobs


def build_stage2(state: dict) -> dict:
    day_ref = hf.upload(SRC / "01_tom_day_photo.jpg")
    jobs = {}
    for v in (1, 2):
        for ar in ("16:9", "21:9", "9:16"):
            night = state.get(f"hero_night_{tag(ar)}_v{v}", {})
            if night.get("file"):
                jobs[f"hero_day_{tag(ar)}_v{v}"] = {**BASE, "aspect_ratio": ar, "prompt": D,
                                                    "image_urls": [hf.upload(night["file"]), day_ref]}
    return jobs


def load() -> dict:
    return json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}


def save(state: dict) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def spent(state: dict) -> float:
    return sum(j.get("usd", 0) for j in state.values() if j.get("request_id") and j.get("status") not in ("failed", "nsfw"))


def run_stage(jobs: dict, state: dict, confirm: bool) -> None:
    todo = {k: p for k, p in jobs.items() if not state.get(k, {}).get("request_id")
            or state[k].get("status") in ("failed", "nsfw")}
    quotes = {k: hf.estimate(MODEL, p) for k, p in todo.items()}
    total = sum(quotes.values())
    print(f"{len(todo)} jobs to submit, quote ${total:.3f} (already committed ${spent(state):.3f}, budget ${BUDGET_USD:.2f})")
    if spent(state) + total > BUDGET_USD:
        raise hf.HiggsfieldError("Refused: total would exceed the approved budget")
    if not confirm:
        return
    for k, p in todo.items():
        res = hf.generate(MODEL, p, confirm=True)
        state[k] = {"request_id": res["request_id"], "usd": quotes[k], "status": res.get("status"),
                    "aspect_ratio": p["aspect_ratio"], "refs": len(p["image_urls"])}
        save(state)
    pending = [k for k in jobs if state.get(k, {}).get("request_id") and not state[k].get("file")
               and state[k].get("status") not in ("failed", "nsfw")]
    start = time.time()
    while pending and time.time() - start < 1800:
        for k in list(pending):
            res = hf.status(state[k]["request_id"])
            st = res.get("status")
            state[k]["status"] = st
            if st == "completed":
                files = hf.download(res, OUT, prefix=k)
                final = files[0].with_name(f"{k}{files[0].suffix}")
                files[0].replace(final)
                state[k]["file"] = str(final)
                print(f"done   {k}")
                pending.remove(k)
            elif st in hf.TERMINAL:
                state[k]["error"] = json.dumps(res)[:300]
                print(f"{st:6} {k}")
                pending.remove(k)
            save(state)
        if pending:
            time.sleep(8)
    if pending:
        print("still pending:", ", ".join(pending))


def main(argv: list[str]) -> int:
    confirm = "--yes" in argv
    cmd = argv[0] if argv else ""
    state = load()
    try:
        if cmd == "quote":
            s1 = build_stage1()
            q1 = sum(hf.estimate(MODEL, p) for p in s1.values())
            d = {**BASE, "aspect_ratio": "16:9", "prompt": D, "image_urls": [hf.upload(SRC / "01_tom_day_photo.jpg")] * 2}
            q2 = sum(hf.estimate(MODEL, {**d, "aspect_ratio": ar}) for ar in ("16:9", "21:9", "9:16")) * 2
            print(f"stage 1 (A, B, C: {len(s1)} images) ${q1:.3f} + stage 2 (D: 6 images) ${q2:.3f} = ${q1 + q2:.3f}")
        elif cmd == "run":
            run_stage(build_stage1(), state, confirm)
            if confirm:
                run_stage(build_stage2(state), state, confirm)
            done = sum(1 for j in state.values() if j.get("file"))
            print(f"{done} files, committed spend ${spent(state):.3f}")
        else:
            print(__doc__)
            return 1
    except hf.HiggsfieldError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
