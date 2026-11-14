"""Hero orbit, route 1 (real 3D camera): CONTENT PLATES generated on pure black.

The orbit, product, sand, light and wipes are built in code (components/OrbitLab.tsx). Higgsfield is only
used for the content that leaves the screen. Each plate = one still on black (Marketing Studio Image) and
one clip animated from it (Kling 4.0, locked camera, subject centred), later keyed by luminance and placed
in the 3D scene as a moving sprite.

Usage:
  python scripts/orbit_plates.py prompts [name]
  python scripts/orbit_plates.py quote   <name>            # free
  python scripts/orbit_plates.py still   <name> --yes      # generate the still only
  python scripts/orbit_plates.py clip    <name> --yes      # animate the approved still
State: media/hero_orbit/plates/jobs.json. Refuses above BUDGET_USD[name] or the .env spend cap.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import higgsfield as hf  # noqa: E402

IMG, VID = "marketing-studio/image", "kling-video/v4.0/image-to-video"
OUT = hf.ROOT / "media" / "hero_orbit" / "plates"
STATE = OUT / "jobs.json"
SPENT_BEFORE = 15.32          # project spend on 14 Nov 2026 before any plate
BUDGET_USD = {"falcon": 0.0}  # set to the approved quote per plate
DURATION, RESOLUTION = 4, "1080p"

BLACK = ("Pure black background (#000000), completely empty: no ground, no sky, no horizon, no dust, no haze, "
         "no light beams, no reflections.")
LOCK = ("The camera is locked off and does not move. The subject stays centred, at the same size and the same "
        "position in the frame for the whole shot. The background stays pure black throughout: no ground, sky, "
        "dust, haze or light appears. The lighting stays constant, with no flicker.")
PLATES = {
    "falcon": {
        "aspect_ratio": "16:9",
        "still": ("Photorealistic studio photograph of a single saker falcon in flight, seen from the front and "
                  "slightly below, flying straight toward the camera with its wings fully spread and level. The "
                  "bird is centred and the whole bird is visible, with clear empty space around both wingtips. "
                  f"{BLACK} The falcon is lit from behind and below by a cool white light, as if by a large "
                  "screen behind it: crisp feather detail, a thin cool rim light on the wings, cool blue-white "
                  "grading. No jesses, hood, leash or perch. No text, logos or people."),
        "clip": ("A falcon flies in place straight toward the camera, beating its wings in a steady, natural "
                 "rhythm: three full wingbeats, down and up, with the feathers flexing. Its head stays level "
                 f"and its eyes stay on the camera. {LOCK} One bird, exactly two wings and one head; no "
                 "morphing, no extra feathers, no text or logos."),
    },
}


def load() -> dict:
    return json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}


def save(state: dict) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def spent(state: dict) -> float:
    return sum(j.get("usd", 0) for j in state.values() if j.get("request_id") and j.get("status") not in ("failed", "nsfw"))


def still_params(name: str) -> dict:
    p = PLATES[name]
    return {"resolution": "2k", "quality": "medium", "enhance_prompt": False, "aspect_ratio": p["aspect_ratio"], "prompt": p["still"]}


def clip_params(name: str, upload: bool = True) -> dict:
    f = OUT / f"{name}_still.png"
    return {"image_url": hf.upload(f) if upload and f.exists() else "pending", "prompt": PLATES[name]["clip"],
            "duration": DURATION, "resolution": RESOLUTION}


def quote(name: str) -> tuple[float, float]:
    return hf.estimate(IMG, still_params(name)), hf.estimate(VID, clip_params(name, upload=False))


def submit(key: str, model: str, params: dict, usd: float, name: str, state: dict) -> Path:
    cap = hf.max_spend()
    mine = sum(j.get("usd", 0) for k, j in state.items() if k.startswith(name + "_") and j.get("request_id")
               and j.get("status") not in ("failed", "nsfw"))
    print(f"{key}: quote ${usd:.4f}; plate budget ${BUDGET_USD[name]:.3f} (used ${mine:.3f}); "
          f"project ${SPENT_BEFORE + spent(state) + usd:.2f} of cap ${cap:.2f}")
    if mine + usd > BUDGET_USD[name] + 1e-6:
        raise hf.HiggsfieldError("Refused: above the approved budget for this plate")
    if SPENT_BEFORE + spent(state) + usd > cap:
        raise hf.HiggsfieldError("Refused: total project spend would exceed HIGGSFIELD_MAX_SPEND_USD")
    if state.get(key, {}).get("request_id") and state[key].get("status") not in ("failed", "nsfw"):
        raise hf.HiggsfieldError(f"{key} was already submitted; rename the job for a new take")
    res = hf.generate(model, params, confirm=True)
    state[key] = {"request_id": res["request_id"], "usd": usd, "status": res.get("status")}
    save(state)
    res = hf.wait(res["request_id"])
    state[key]["status"] = res.get("status")
    if res.get("status") != "completed":
        state[key]["error"] = json.dumps(res)[:300]
        save(state)
        raise hf.HiggsfieldError(f"{key} ended as {res.get('status')}")
    f = hf.download(res, OUT, prefix=key)[0]
    final = f.with_name(f"{key}{f.suffix}")
    f.replace(final)
    state[key]["file"] = str(final)
    save(state)
    return final


def main(argv: list[str]) -> int:
    cmd = argv[0] if argv else ""
    name = argv[1] if len(argv) > 1 and argv[1] in PLATES else ""
    try:
        if cmd == "prompts":
            for n in ([name] if name else PLATES):
                print(f"#### plate: {n}\n- still: {IMG}, {PLATES[n]['aspect_ratio']}, 2k, medium, no reference images\n\n> {PLATES[n]['still']}\n\n"
                      f"- clip: {VID}, {DURATION} s, {RESOLUTION}, first frame = the approved still, no end frame\n\n> {PLATES[n]['clip']}\n")
        elif cmd == "quote" and name:
            s, c = quote(name)
            print(f"{name}: still ${s:.4f} + clip ${c:.4f} = ${s + c:.4f}")
        elif cmd in ("still", "clip") and name:
            if "--yes" not in argv:
                raise hf.HiggsfieldError("Add --yes after Wassim approves the quote")
            state = load()
            if cmd == "still":
                p = still_params(name)
                print(submit(f"{name}_still", IMG, p, hf.estimate(IMG, p), name, state))
            else:
                p = clip_params(name)
                print(submit(f"{name}_clip", VID, p, hf.estimate(VID, p), name, state))
        else:
            print(__doc__)
            return 1
    except hf.HiggsfieldError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
