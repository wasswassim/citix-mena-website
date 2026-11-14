"""Hero orbit, route 3: Seedance 2.0 on Higgsfield (docs: docs.higgsfield.ai/docs/models/seedance-2.md).

Two tests for rotation R1 (Tom + falcon), 16:9, no audio, 720p by default (--res 1080p for finals):
  i2v  image-to-video      black plate -> approved still, with the corrected fixed-radius prompt (4 s)
  ref  reference-to-video  look from the approved still + camera motion from the code orbit render (8 s):
                           image_urls = [R1 still], video_urls = [orbit_reference_R1_8s.mp4]

Usage:
  python scripts/orbit_seedance.py prompts
  python scripts/orbit_seedance.py quote <i2v|ref>         # free
  python scripts/orbit_seedance.py run   <i2v|ref> --yes
State: media/hero_orbit/seedance/jobs.json. Refuses above BUDGET_USD[job] or the .env spend cap.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import higgsfield as hf  # noqa: E402
import orbit_clips as oc  # noqa: E402  (shares the corrected Kling prompt text)

I2V = "bytedance/seedance-2.0/image-to-video"
REF = "bytedance/seedance-2.0/reference-to-video"
ORBIT = hf.ROOT / "media" / "hero_orbit"
OUT = ORBIT / "seedance"
STATE = OUT / "jobs.json"
STILL = ORBIT / "stills" / "R1_16x9_v3.png"
MOTION = ORBIT / "lab" / "orbit_reference_R1_8s.mp4"
SPENT_BEFORE = 16.13                       # project spend on 14 Nov 2026 before any Seedance job
BUDGET_USD = {"i2v": 0.0, "ref": 1.7024, "ref3": 1.7024}  # ref: "Reference only $1.702"; ref3: "OK camel $1.702" (Wassim, 14 Nov 2026)
RES = sys.argv[sys.argv.index("--res") + 1] if "--res" in sys.argv else "720p"   # tests at 720p; finals at 1080p

REF_PROMPT = (
    "Use the reference video ONLY for the camera: copy its camera path exactly. In it the camera travels along a "
    "circle around a tall glowing totem at a fixed radius and a fixed height, always aimed at the totem, at one "
    "constant speed; the totem stays at the same position in the frame and at the same size from start to end "
    "and only its angle changes, from almost edge-on to a three-quarter view. Keep its timing too: the shot "
    "starts in darkness behind a black sand dune close to the lens, the dune slides away, and near the end "
    "another black dune slides across the lens and the shot ends in darkness. Do not copy the reference video's "
    "plain look. "
    "Use the reference image for the look, the product and the content: photorealistic cinematic night, very "
    "dark and low-key, a black void over desert sand dunes, cool blue grading; a tall, slim black smartboard "
    "totem with two stacked glowing screens, a plain top cap, a plinth and a thin red light strip on its side, "
    "exactly as in the image. The totem's screen is the only light: a soft shaft of cool light falls from it "
    "onto the sand. "
    "Action, happening WHILE the camera orbits, never after it: a falcon takes shape deep inside the lower "
    "screen, flies forward, breaks through the screen surface with its wings spreading and flies out toward the "
    "camera and away past it, while a stream of fine sand pours out of the lower screen and fans across the "
    "ground. The falcon clearly comes from inside the screen. "
    "The totem is a rigid, solid object that never changes shape. No push-in, no pull-back, no drifting, no "
    "slow-down, no pause. No text, logos, people or buildings."
)

# R3 (camel + glass panel). Lessons from the R1 test are written in: Seedance pushed in about 7 %, drifted
# sideways and pulled back before the final wipe, so the prompt forbids each of those by name.
STILL3 = ORBIT / "stills" / "R3_16x9_v3.png"
MOTION3 = ORBIT / "lab" / "orbit_reference_R3_8s.mp4"
REF3_PROMPT = (
    "Use the reference video ONLY for the camera: copy its camera path and its framing exactly. In it the "
    "camera travels along a circle around an upright square panel at a fixed radius and a fixed height, always "
    "aimed at the panel, at one constant speed. The panel stays at exactly the same position in the frame and "
    "at exactly the same size in every frame, from the first frame it is visible to the last; only its angle "
    "changes, from almost edge-on to a three-quarter view. The camera never moves closer, never moves away "
    "and never drifts sideways: no push-in at the start, no zoom in the middle, and NO pull-back before the "
    "end. Keep the timing too: the shot starts in darkness behind a black sand dune close to the lens, the "
    "dune slides away, and at the end another black dune slides across the lens while the panel is still at "
    "full size, and the shot ends in darkness. Do not copy the reference video's plain look. "
    "Use the reference image for the look, the object and the content: photorealistic cinematic night, very "
    "dark and low-key, a black void over desert sand dunes, cool slate-blue grading. The object is a "
    "frameless, perfectly clear square glass panel standing upright on the sand, a few centimetres thick, "
    "with a faint cool-white glow along its thin edges (white, not cyan), exactly as in the image. Inside the "
    "glass is a deep, misty night view of jagged rocky mountains; the glass is the only light, and a soft "
    "shaft of cool light and low mist spill from it onto the sand. "
    "Action, happening WHILE the camera orbits, never after it: a dromedary camel (one hump, no saddle, no "
    "harness, no rider) is first seen small and far away deep inside the mountain scene, walks forward toward "
    "the glass, its head and long neck pass through the glass surface, then its chest and front legs, then "
    "its whole body, and it steps out onto the sand and keeps walking calmly out of the frame, with a natural "
    "gait and exactly four legs. Mist flows out through the glass with it and spreads low over the sand. The "
    "camel clearly comes from inside the glass. "
    "The glass panel is a rigid, flat sheet that never changes shape and never gets a frame. No slow-down, no "
    "pause. No text, logos, people or buildings."
)
KEYS = {"ref3": "R3_ref"}


def jobs() -> dict:
    return {
        "i2v": (I2V, lambda: {"image_url": hf.upload(oc.plate("16x9")), "end_image_url": hf.upload(STILL),
                              "prompt": oc.prompt("R1", "A"), "duration": 4, "resolution": RES,
                              "generate_audio": False}),
        "ref3": (REF, lambda: {"image_urls": [hf.upload(STILL3)], "video_urls": [hf.upload(MOTION3)],
                               "prompt": REF3_PROMPT, "duration": 8, "resolution": RES, "aspect_ratio": "16:9",
                               "generate_audio": False}),
        "ref": (REF, lambda: {"image_urls": [hf.upload(STILL)], "video_urls": [hf.upload(MOTION)],
                              "prompt": REF_PROMPT, "duration": 8, "resolution": RES, "aspect_ratio": "16:9",
                              "generate_audio": False}),
    }


def load() -> dict:
    return json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}


def save(state: dict) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def spent(state: dict) -> float:
    return sum(j.get("usd", 0) for j in state.values() if j.get("request_id") and j.get("status") not in ("failed", "nsfw"))


def main(argv: list[str]) -> int:
    cmd = argv[0] if argv else ""
    name = argv[1] if len(argv) > 1 else ""
    try:
        if cmd == "prompts":
            if "R3" in argv:
                print(f"#### Seedance ref (R3): {REF}, 8 s, {RES}, 16:9, no audio; image ref {STILL3.name}, video ref {MOTION3.name}\n\n> {REF3_PROMPT}\n")
                return 0
            print(f"#### Seedance i2v (R1): {I2V}, 4 s, {RES}, no audio; first frame black plate, last frame {STILL.name}\n\n> {oc.prompt('R1', 'A')}\n")
            print(f"#### Seedance ref (R1): {REF}, 8 s, {RES}, 16:9, no audio; image ref {STILL.name}, video ref {MOTION.name}\n\n> {REF_PROMPT}\n")
            return 0
        if cmd not in ("quote", "run") or name not in BUDGET_USD:
            print(__doc__)
            return 1
        model, build = jobs()[name]
        params = build()
        usd = hf.estimate(model, params)
        state = load()
        cap = hf.max_spend()
        print(f"{name}: {model}, {params['duration']} s {params['resolution']} = ${usd:.4f}; budget ${BUDGET_USD[name]:.3f}; "
              f"project ${SPENT_BEFORE + spent(state) + usd:.2f} of cap ${cap:.2f}")
        if cmd == "quote":
            return 0
        if "--yes" not in argv:
            raise hf.HiggsfieldError("Add --yes after Wassim approves the quote")
        if usd > BUDGET_USD[name] + 1e-6:
            raise hf.HiggsfieldError("Refused: above the approved budget for this job")
        if SPENT_BEFORE + spent(state) + usd > cap:
            raise hf.HiggsfieldError("Refused: total project spend would exceed HIGGSFIELD_MAX_SPEND_USD")
        key = KEYS.get(name, f"R1_{name}") + (f"_t{argv[argv.index('--take') + 1]}" if "--take" in argv else "")
        if state.get(key, {}).get("request_id") and state[key].get("status") not in ("failed", "nsfw"):
            raise hf.HiggsfieldError(f"{key} was already submitted; use --take N for a new take")
        res = hf.generate(model, params, confirm=True)
        state[key] = {"request_id": res["request_id"], "usd": usd, "status": res.get("status")}
        save(state)
        res = hf.wait(res["request_id"], timeout_s=3000)
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
        sheet = final.with_name(f"{key}_sheet_4fps.jpg")
        n = params["duration"] * 4
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(final), "-vf",
                        f"fps=4,scale=480:-2,tile=4x{-(-n // 4)}:padding=4:color=0x161616", "-frames:v", "1", "-q:v", "3",
                        str(sheet)], check=True)
        print(final)
    except hf.HiggsfieldError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
