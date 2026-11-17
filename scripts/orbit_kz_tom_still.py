"""Kazakhstan Tom orbit, step 1: one look still (Marketing Studio Image, 16:9 1920x1080), 17 Nov 2026.

Wassim: the hero orbit idea (rotation, content breaking out) for the real product in the company PDF photo
(Citix_about company.pdf p16). Choices: hero world, widget tiles pop out, ad area "keep the same ads" -> same
pop-art poster style only (no real festival name, no person, no logo: hard rule 6).

Image refs (uploaded):
  1. media/hero_orbit/stills/R3_16x9_v3.png               the approved hero look
  2. media/hero_orbit/refs/tom_kz/ref_kz_tom_studio_clean.png  PDF p9, ad area and cap text blacked out
  3. media/hero_orbit/refs/tom_kz/ref_kz_tom_street_clean.png  PDF p16, ad area and cap text blacked out

Usage:
  python scripts/orbit_kz_tom_still.py prompt
  python scripts/orbit_kz_tom_still.py quote          # free /estimate
  python scripts/orbit_kz_tom_still.py run --yes      # only after Wassim's OK on the exact quote
State: media/hero_orbit/v5/kz_tom/jobs.json. Refuses above BUDGET_USD or the .env spend cap.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import higgsfield as hf  # noqa: E402
import orbit_stills as os3  # noqa: E402  (WORLD3, FRAME3, AVOID: the R3 v3 wording)

MODEL = "marketing-studio/image"
ORBIT = hf.ROOT / "media" / "hero_orbit"
OUT = ORBIT / "v5" / "kz_tom"
STATE = OUT / "jobs.json"
REFS = [
    ORBIT / "stills" / "R3_16x9_v3.png",
    ORBIT / "refs" / "tom_kz" / "ref_kz_tom_studio_clean.png",
    ORBIT / "refs" / "tom_kz" / "ref_kz_tom_street_clean.png",
]
SPENT_BEFORE = 28.38          # project spend before this job (docs/higgsfield-map.md)
BUDGET_USD = 0.126            # Wassim approved "OK still $0.126" (3 refs, re-quoted), 17 Nov 2026
W, H = 1920, 1080
BASE = {"resolution": "2k", "quality": "medium", "enhance_prompt": False, "aspect_ratio": "16:9"}
KEY = "KZ_tom"

# The R3 world, without its last sentence (that one describes a scene spilling out of a glass doorway).
WORLD = os3.WORLD3.split(" The screen is a doorway")[0]
assert WORLD != os3.WORLD3

REF = (
    "REFERENCE IMAGES: image 1 gives the world, the light, the darkness, the camera height and the cool "
    "slate-blue grading, keep them exactly. Images 2 and 3 give the product only: reproduce its shape exactly "
    "and ignore their backgrounds, their light and the dark empty area at the bottom of their screens."
)
PRODUCT = (
    "PRODUCT (do not redesign): the CITIX roadside smartboard, a tall, slim vertical totem about 7 m high and "
    "2 m wide (body about 1 : 3.5), thin flat profile, matte black body. A low grey band across the full width "
    "of the top, completely plain, no text or logo. Below it one tall portrait screen fills almost the whole "
    "front, with a thin black bezel. A plain grey rectangular plinth at the bottom, the same width as the body. "
    "One thin vertical red LED light strip along the right side edge, lit."
)
SCREEN = (
    "Screen content, top to bottom, as rounded tiles on a black screen: a bright blue square widget tile with "
    "a large white ATM icon (a card slot dispensing a banknote) and a white round arrow button in its top right "
    "corner; under it two slim dark-grey rounded navigation rows, the first with a green round arrow button on "
    "its right, the second with a red round arrow button; below them the advertising area, about half of the "
    "screen: a bright pop-art festival poster in flat colour bands of pink, mint green, bright red and blue with "
    "bold chunky black typographic bars, rich but natural screen colours, not neon. The poster has no readable "
    "words, no person, no face and no logo."
)
ACTION = (
    "The widgets BREAK OUT of the flat screen: the blue ATM tile and the two navigation rows have lifted out of "
    "the screen surface toward the camera as thick glowing 3D tiles, floating in the air a little in front of "
    "the screen, each still facing the same way as the screen, lit by it and casting soft shadows on the sand. "
    "The poster stays flat inside the screen. The screen is the only real light source."
)
AVOID = os3.AVOID.replace(
    "any text, lettering, numbers, logo,",
    "any readable text, lettering, numbers or Cyrillic, any logo,",
)
assert AVOID != os3.AVOID


def prompt() -> str:
    return f"{REF} {WORLD} {PRODUCT} {SCREEN} {ACTION}{os3.FRAME3['16:9']} {AVOID}"


def job(upload: bool = True) -> dict:
    refs = [hf.upload(r) for r in REFS] if upload else [r.name for r in REFS]
    return {**BASE, "prompt": prompt(), "image_urls": refs}


def load() -> dict:
    return json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}


def save(state: dict) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def finish(res: dict, state: dict) -> None:
    from PIL import Image
    f = hf.download(res, OUT, prefix=KEY)[0]
    raw = f.with_name(f"{KEY}_raw{f.suffix}")
    f.replace(raw)
    im = Image.open(raw).convert("RGB")
    s = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x, y = (im.width - W) // 2, (im.height - H) // 2
    final = OUT / f"{KEY}.png"
    im.crop((x, y, x + W, y + H)).save(final)
    state[KEY].update(file=str(final), raw=str(raw))


def run(confirm: bool) -> None:
    state = load()
    if state.get(KEY, {}).get("request_id") and state[KEY].get("status") not in ("failed", "nsfw"):
        print(f"{KEY} already submitted: {state[KEY].get('status')}")
        return
    p = job()
    usd = hf.estimate(MODEL, p)
    cap = hf.max_spend()
    print(f"1 still, quote ${usd:.4f}; budget ${BUDGET_USD:.4f}; project ${SPENT_BEFORE + usd:.2f} of cap ${cap:.2f}")
    if not confirm:
        return
    if usd > BUDGET_USD + 1e-9:
        raise hf.HiggsfieldError("Refused: above the approved budget for this run")
    if SPENT_BEFORE + usd > cap:
        raise hf.HiggsfieldError("Refused: total project spend would exceed HIGGSFIELD_MAX_SPEND_USD")
    res = hf.generate(MODEL, p, confirm=True)
    state[KEY] = {"request_id": res["request_id"], "usd": usd, "status": res.get("status")}
    save(state)
    start = time.time()
    while time.time() - start < 1800:
        res = hf.status(state[KEY]["request_id"])
        state[KEY]["status"] = st = res.get("status")
        if st == "completed":
            finish(res, state)
            save(state)
            print(f"done {state[KEY]['file']}")
            return
        if st in hf.TERMINAL:
            state[KEY]["error"] = json.dumps(res)[:300]
            save(state)
            print(f"{st} {KEY}")
            return
        save(state)
        time.sleep(8)
    print("still pending after 30 min; re-run to keep polling is not supported, check jobs.json")


def main(argv: list[str]) -> int:
    cmd = argv[0] if argv else ""
    try:
        if cmd == "prompt":
            print(f"- {MODEL}, 16:9 -> {W}x{H}, 2k, medium, 1 variation; refs {[r.name for r in REFS]}\n")
            print(prompt())
        elif cmd == "quote":
            print(f"{KEY} ${hf.estimate(MODEL, job()):.4f}")
        elif cmd == "run":
            run("--yes" in argv)
        else:
            print(__doc__)
            return 1
    except hf.HiggsfieldError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
