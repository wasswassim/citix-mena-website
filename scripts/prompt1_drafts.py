"""Prompt 1 drafts, round 2 (OLD Tom, refs 01 + 02): 20 key stills with Marketing Studio Image.

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
BUDGET_USD = 1.90  # Wassim approved $1.80 for round 2 on 2026-11-12
OUT = hf.ROOT / "media" / "generated" / "drafts"
STATE = OUT / "jobs.json"
SRC = hf.ROOT / "media" / "source"
BASE = {"resolution": "2k", "quality": "medium", "enhance_prompt": False}

TOM = (
    "PRODUCT — reproduce the real object shown in reference images 1 (day) and 2 (night) exactly, do not "
    'redesign it: the CITIX "Tom" roadside smartboard, a tall, slim vertical totem about 7 m high and 2 m '
    "wide (body width to height about 1 : 3) with a very thin flat profile and a matte black metal body. "
    "The front face is almost entirely screen: two stacked portrait screens with rounded corners and very "
    "thin black bezels, separated by a thin black gap, the upper screen slightly shorter than the lower "
    "one. A small low black cap sits on the top edge, spanning from the middle to the right edge, with one "
    "round camera lens at its right end; the cap is completely plain, with no text or logo. The totem "
    "stands on a plain matte black rectangular plinth, narrower than the body (about 60% of its width), "
    "short (about one sixth of the body height) and flush with the body's right edge. A single thin "
    "vertical red LED light strip runs along the right side face of the totem from the cap down to the "
    "ground, exactly as in reference image 2. No other parts, text, logos, stickers, antennas or "
    "decoration. Ignore the content shown on the screens in the reference images."
)
AVOID = (
    "Avoid: warm, orange or yellow tones; neon, acid or oversaturated colours; sci-fi or futuristic "
    "styling; abstract CGI look; lens flares, fog, digital noise, clutter; mosques, domes, minarets or "
    "famous landmarks; identifiable people; billboards or other signage; any text, lettering, wordmark, "
    "logo or brand anywhere in the image, including on the totem's top cap; any pattern, engraving or "
    "ornament on the totem; any content, text or image on the screens."
)
GLOW = ("an even, cool, medium-white glow like a display at 40% brightness (light grey-white, never pure "
        "white, not blown out), with no content")

A = (
    "Photorealistic cinematic photograph at street level, blue hour just after sunset, on a wide "
    "palm-lined road in Sharjah, UAE. Reference image 3 is an aerial view of the same district at the "
    "same moment: match its cool blue-hour light and colour and show a similar cluster of modern "
    f"waterfront high-rise towers softly out of focus in the distance. {TOM} It stands on the grass verge "
    "beside the road, right of centre (around the right third of the frame), full height visible from the "
    "ground to the cap with clear headroom above the cap, seen from the same slight three-quarter angle "
    f"as in reference image 1. Both screens are switched ON but blank: {GLOW}. The red side light strip "
    "is lit. Traffic passes as motion-blurred streaks with white and red light trails; no readable "
    "plates, no people. Eye-level camera, 35 mm lens, shallow depth of field. Deep blue sky, clean high "
    f"contrast, crisp defined artificial light, neutral-cool white balance. {AVOID}"
)
A_V = " Vertical composition: the totem fills about 65% of the frame height, slightly right of centre, the road receding on the left."

B = (
    f"Photorealistic cinematic photograph at night on a wide, quiet road in Sharjah, UAE. {TOM} It stands "
    "on the roadside, perfectly front-facing, looking straight at the camera, exactly centred "
    "horizontally, full height visible from the ground to the cap. Eye-level camera, long lens, vertical "
    "edges parallel. The horizon is low: the road, a few palm trees and low-rise modern buildings stay in "
    "the lower third of the frame, softly out of focus, with long white and red light trails from passing "
    "traffic behind the totem. The upper two thirds of the frame are a clear, deep blue-black night sky "
    "with faint, sparse stars. Both screens are switched OFF: pure black glass with only faint "
    "reflections. The red side light strip is lit, visible as a thin red line along the totem's right "
    "edge. Soft, cool white street light defines the edges of the body. High contrast, clean, "
    f"neutral-cool white balance. {AVOID}"
)
B_V = " Vertical composition: the totem centred, filling about 60% of the frame height."

C = (
    f"Photorealistic cinematic photograph at night. {TOM} It is perfectly front-facing, looking straight "
    "at the viewer, with no three-quarter view, exactly centred horizontally. The camera is low and looks "
    "slightly up at it through a long lens, so the vertical edges stay almost parallel. The background is "
    "sky only: a clear, deep blue-black night sky with faint, sparse stars, completely empty — no street, "
    "no ground, no horizon, no buildings, no trees, no clouds. The totem's full height is visible: the "
    "cap near the top with clear sky above it, and the plinth at the bottom, BASE. It must read as a "
    "real, heavy object standing on the ground just below the frame, never floating. Both screens are "
    f"switched ON but blank: {GLOW}. The red side light strip is lit, visible only as a thin red line "
    "along the totem's right edge. A faint cool rim light defines the edges of the matte black body. "
    f"Wide, clean, empty sky on both sides of the totem. High contrast, clean, no noise. {AVOID}"
)
C_BASE = {
    1: "the bottom of the plinth is cut cleanly by the bottom edge of the frame",
    2: "the bottom of the plinth dissolves into a soft dark fade in the last few percent of the frame",
}
C_FRAME = {
    "16:9": " The totem is small in the frame: from the bottom edge up to its cap it fills only about 60% of the frame height, leaving the top 40% of the frame as open, empty sky.",
    "21:9": " The totem is small in the frame: from the bottom edge up to its cap it fills only about 60% of the frame height, leaving the top 40% of the frame as open, empty sky.",
    "9:16": " Vertical composition: the totem is small in the frame: from the bottom edge up to its cap it fills only about 55% of the frame height, leaving the top 45% of the frame as open, empty sky.",
}

D = (
    "Edit reference image 1 into the identical scene in daytime. Keep the camera, the framing, the "
    "totem's position, scale and every edge, and the way its base meets the bottom of the frame exactly "
    "as they are, pixel for pixel. Change only the light and the sky: a clear blue sky with a few soft "
    "white clouds, realistic neutral daylight on the matte black body as in reference image 2. Still sky "
    "only: no ground, no horizon, no buildings. The screens stay switched ON and blank with the same cool "
    "medium-white glow, naturally less bright against daylight. The red side light strip is switched off "
    f"and barely visible. Clean, realistic, minimal noise. {AVOID}"
)

PRODUCT_REFS = ["01_tom_day_photo.jpg", "02_tom_night_photo.jpg"]


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
                                                  "prompt": C.replace("BASE", C_BASE[v]) + C_FRAME[ar]}
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
