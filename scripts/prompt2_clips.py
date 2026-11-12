"""Prompt 2 clips with Kling 4.0 image-to-video (first frame + optional end frame).

Usage:
  python scripts/prompt2_clips.py quote  <job|group>
  python scripts/prompt2_clips.py run    <job|group> --yes
Groups: test (Shot 5 test), drafts (step 2 drafts).

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
BUDGET_USD = 0.63          # step 1 only (Shot 5 test)
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

JOBS = {
    "s5_test_16x9_720p": {"first": "s5_first_16x9.png", "last": "s5_last_16x9.png", "prompt": S5,
                          "duration": 5, "resolution": "720p", "group": "test"},
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


def frames_sheet(clip: Path, n: int = 6) -> Path:
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                         "-of", "csv=p=0", str(clip)]).decode().strip())
    stills = []
    for i in range(n):
        t = dur * i / (n - 1) if i < n - 1 else max(dur - 0.05, 0)
        out = clip.with_name(f"{clip.stem}_f{i + 1}.jpg")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", str(clip), "-frames:v", "1",
                        "-q:v", "2", str(out)], check=True)
        stills.append(out)
    sheet = clip.with_name(f"{clip.stem}_sheet.jpg")
    args = ["ffmpeg", "-v", "error", "-y"]
    for s in stills:
        args += ["-i", str(s)]
    lay = "".join(f"[{i}:v]scale=960:-2[v{i}];" for i in range(n))
    lay += "".join(f"[v{i}]" for i in range(n)) + f"xstack=inputs={n}:layout=0_0|w0_0|w0+w1_0|0_h0|w0_h0|w0+w1_h0"
    subprocess.run(args + ["-filter_complex", lay, "-frames:v", "1", "-q:v", "3", str(sheet)], check=True)
    for s in stills:
        s.unlink()
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
