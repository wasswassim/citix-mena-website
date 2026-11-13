"""Prompt 2 clips with Kling 4.0 image-to-video (first frame + optional end frame).

Usage:
  python scripts/prompt2_clips.py quote  <job|group>
  python scripts/prompt2_clips.py run    <job|group> --yes
Groups: test (Shot 5 test), drafts (step 2 drafts), finals (1080p finals).

Approved by Wassim 2026-11-12: test $0.63; drafts $4.02 total pre-approved ONLY if the test
does not warp Tom. BUDGET_USD is raised step by step. State: media/generated/clips/jobs.json
(a job that already has a request ID is never submitted twice).
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import higgsfield as hf  # noqa: E402

MODEL = "kling-video/v4.0/image-to-video"
BUDGET_USD = 7.23          # drafts $4.022 (spent) + 1080p finals up to $3.20 (Wassim, 13 Nov 2026)
IN = hf.ROOT / "media" / "generated" / "clips_input"
OUT = hf.ROOT / "media" / "generated" / "clips"
STATE = OUT / "jobs.json"

RIGID = (
    "The totem is a rigid, solid object: its shape, proportions, straight edges, two screens, top cap, "
    "plinth and red side light strip stay exactly identical throughout. No morphing, no bending, no "
    "stretching, no extra parts, no text or logos anywhere. Smooth, steady, cinematic camera motion, one "
    "continuous shot, no cuts, no shake."
)
S5 = (
    "Night. The camera stays centred on the tall black smartboard totem while it slowly lowers toward the "
    "ground, eases back slightly and tilts up. The road, buildings, palm trees, street lights and light "
    "trails sink smoothly out of the bottom of the frame until only the totem remains, standing against a "
    "clear, deep blue-black sky with faint stars. During the move the totem's two screens power on "
    "together, rising from black to an even, soft, cool-white glow. " + RIGID
)
S2 = (
    "Blue hour. A very slow, gentle push-in of about PUSH toward the tall black smartboard totem on the "
    "roadside. Traffic keeps flowing as motion-blurred white and red light trails; palm fronds move very "
    "slightly. The totem's screens keep the same even cool-white glow and its red side strip stays lit. "
    "The skyline stays fixed and does not change. " + RIGID
)

# Step 2 wording (Wassim, 13 Nov 2026): in the test a palm top lingered bottom-left until about 4.25 s.
S5_V2 = (
    "Night. The camera stays centred on the tall black smartboard totem while it slowly lowers toward the "
    "ground, eases back slightly and tilts up. The road, buildings, palm trees, street lights and light "
    "trails sink smoothly and completely out of the bottom of the frame early in the shot: by the 3 "
    "second mark nothing of the street, the palms or the buildings is left anywhere in the frame, "
    "including the bottom corners. For the last 2 seconds only the totem remains, standing against a "
    "clear, deep blue-black sky with faint stars, while the camera settles gently. During the move the "
    "totem's two screens power on together, rising smoothly from black to an even, soft, cool-white "
    "glow. " + RIGID
)
S2_3 = S2.replace("PUSH", "3%")

JOBS = {
    # step 1 (done, approved by Wassim: smooth power-on, no deformation) = s5 16:9 variation 1
    "s5_test_16x9_720p": {"first": "s5_first_16x9.png", "last": "s5_last_16x9.png", "prompt": S5,
                          "duration": 5, "resolution": "720p", "group": "test"},
    # step 2 drafts
    "s2_16x9_v1": {"first": "s2_first_16x9.png", "prompt": S2_3, "duration": 3, "resolution": "720p", "group": "drafts"},
    "s2_16x9_v2": {"first": "s2_first_16x9.png", "prompt": S2_3, "duration": 3, "resolution": "720p", "group": "drafts"},
    "s2_9x16_v1": {"first": "s2_first_9x16.png", "prompt": S2_3, "duration": 3, "resolution": "720p", "group": "drafts"},
    "s2_9x16_v2": {"first": "s2_first_9x16.png", "prompt": S2_3, "duration": 3, "resolution": "720p", "group": "drafts"},
    "s5_16x9_v2": {"first": "s5_first_16x9.png", "last": "s5_last_16x9.png", "prompt": S5_V2,
                   "duration": 5, "resolution": "720p", "group": "drafts"},
    "s5_9x16_v1": {"first": "s5_first_9x16.png", "last": "s5_last_9x16.png", "prompt": S5_V2,
                   "duration": 5, "resolution": "720p", "group": "drafts"},
    "s5_9x16_v2": {"first": "s5_first_9x16.png", "last": "s5_last_9x16.png", "prompt": S5_V2,
                   "duration": 5, "resolution": "720p", "group": "drafts"},
    # finals, 1080p (Wassim, 13 Nov 2026): same inputs and prompts as the picked drafts
    # s2_16x9_v1, s2_9x16_v2, s5_16x9_v2, s5_9x16_v1. Kling is not deterministic, so these are new takes.
    "s2_16x9_final_1080p": {"first": "s2_first_16x9.png", "prompt": S2_3, "duration": 3, "resolution": "1080p", "group": "finals"},
    "s2_9x16_final_1080p": {"first": "s2_first_9x16.png", "prompt": S2_3, "duration": 3, "resolution": "1080p", "group": "finals"},
    "s5_16x9_final_1080p": {"first": "s5_first_16x9.png", "last": "s5_last_16x9.png", "prompt": S5_V2,
                            "duration": 5, "resolution": "1080p", "group": "finals"},
    "s5_9x16_final_1080p": {"first": "s5_first_9x16.png", "last": "s5_last_9x16.png", "prompt": S5_V2,
                            "duration": 5, "resolution": "1080p", "group": "finals"},
}


def params(job: dict) -> dict:
    p = {"image_url": hf.upload(IN / job["first"]), "prompt": job["prompt"],
         "duration": job["duration"], "resolution": job["resolution"]}
    if job.get("last"):
        p["end_image_url"] = hf.upload(IN / job["last"])
    return p


def load() -> dict:
    return json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}


def save(state: dict) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def spent(state: dict) -> float:
    return sum(j.get("usd", 0) for j in state.values() if j.get("status") not in ("failed", "nsfw"))


def frames_sheet(clip: Path, fps: int = 4) -> Path:
    """Contact sheet at 4 frames per second, read left to right, top to bottom."""
    probe = subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                     "stream=width,height:format=duration", "-of", "csv=p=0", str(clip)]).decode().split()
    w, h = (int(x) for x in probe[0].split(",")[:2])
    n = max(1, round(float(probe[1]) * fps))
    cols, cell = (5, 512) if w >= h else (10, 256)
    rows = -(-n // cols)
    sheet = clip.with_name(f"{clip.stem}_sheet_4fps.jpg")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(clip), "-vf",
                    f"fps={fps},scale={cell}:-2,tile={cols}x{rows}:padding=4:color=0x161616",
                    "-frames:v", "1", "-q:v", "3", str(sheet)], check=True)
    return sheet


def run(names: list[str], confirm: bool) -> None:
    state = load()
    todo = [n for n in names if not state.get(n, {}).get("request_id") or state[n].get("status") in ("failed", "nsfw")]
    built = {n: params(JOBS[n]) for n in todo}
    quotes = {n: hf.estimate(MODEL, p) for n, p in built.items()}
    for n, q in quotes.items():
        print(f"  {n}: {JOBS[n]['duration']} s {JOBS[n]['resolution']} = ${q:.3f}")
    total = sum(quotes.values())
    print(f"{len(todo)} clips, quote ${total:.3f} (already committed ${spent(state):.3f}, budget ${BUDGET_USD:.2f})")
    if spent(state) + total > BUDGET_USD + 1e-6:
        raise hf.HiggsfieldError("Refused: total would exceed the approved budget")
    if not confirm:
        return
    for n in todo:
        res = hf.generate(MODEL, built[n], confirm=True)
        state[n] = {"request_id": res["request_id"], "usd": quotes[n], "status": res.get("status")}
        save(state)
    pending = [n for n in names if state.get(n, {}).get("request_id") and not state[n].get("file")
               and state[n].get("status") not in ("failed", "nsfw")]
    start = time.time()
    while pending and time.time() - start < 2400:
        for n in list(pending):
            res = hf.status(state[n]["request_id"])
            state[n]["status"] = res.get("status")
            if res.get("status") == "completed":
                f = hf.download(res, OUT, prefix=n)[0]
                final = f.with_name(f"{n}{f.suffix}")
                f.replace(final)
                state[n]["file"] = str(final)
                state[n]["sheet"] = str(frames_sheet(final))
                print(f"done   {n} -> {final}")
                pending.remove(n)
            elif res.get("status") in hf.TERMINAL:
                state[n]["error"] = json.dumps(res)[:300]
                print(f"{res.get('status'):6} {n}")
                pending.remove(n)
            save(state)
        if pending:
            time.sleep(10)
    if pending:
        print("still pending:", ", ".join(pending))


def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[0] not in ("quote", "run"):
        print(__doc__)
        return 1
    names = [n for n, j in JOBS.items() if argv[1] in (n, j["group"])]
    try:
        run(names, confirm=argv[0] == "run" and "--yes" in argv)
    except hf.HiggsfieldError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
