"""Hero orbit H2/H3: Kling 4.0 first/last-frame clips, 4 s, 1080p (two per rotation).

Usage:
  python scripts/orbit_clips.py plates                    # make the near-black wipe plates (no credits)
  python scripts/orbit_clips.py prompts 16x9              # print the prompts as Markdown
  python scripts/orbit_clips.py quote  16x9 [--only R1_A,R5_B]
  python scripts/orbit_clips.py run    16x9 [--only ...] --yes
  python scripts/orbit_clips.py preview 16x9              # rough 40 s preview from the clips on disk

Rn_A: black plate -> approved still.   Rn_B: approved still -> black plate.
State: media/hero_orbit/clips/<fmt>/jobs.json (a job with a request ID is never submitted twice).
Refuses to run above BUDGET_USD[fmt] or if project spend would pass HIGGSFIELD_MAX_SPEND_USD.
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
DURATION, RESOLUTION = 4, "1080p"
BUDGET_USD = {"16x9": 1.504, "9x16": 0.0}   # 16x9: Wassim approved "Test R1_A $0.752" + "Re-test R1_A $0.752" (14 Nov 2026); raise at Gate 2a/3a
SPENT_BEFORE = 13.82                      # project spend after H1 (stills), 14 Nov 2026
ORBIT = hf.ROOT / "media" / "hero_orbit"
STILLS = ORBIT / "stills"
PICKS = {"R1": 3, "R2": 3, "R3": 3, "R4": 4, "R5": 3}   # approved at Gate 1b, 14 Nov 2026
SIZES = {"16x9": (1920, 1080), "9x16": (1080, 1920)}

CAMERA = (
    "One continuous shot at night, no cuts. The subject is locked in the frame like an object on a slow "
    "turntable: it stays at exactly the same position in the frame, at the same distance from the camera and "
    "at the same size for the whole shot, and only its angle changes. Geometry: the subject is the centre "
    "of a circle and the camera is a point on that circle, always looking straight at the centre; the camera "
    "travels clockwise along the circle, so the radius between camera and subject never changes. Fixed "
    "height too: no push-in, no pull-back, no drifting sideways, no rising or sinking. The turn has one constant speed from the first frame to the last: it never stops, "
    "never slows down, never pauses or holds, and never speeds up. "
    "Everything that happens on the screen happens WHILE the camera is orbiting, at the same time as the "
    "rotation, never after it. The orbit is slow and covers only a small arc, spread evenly over the whole "
    "duration, so the camera is still travelling at full speed in the very last frame. Smooth, steady, "
    "cinematic, no shake, no zoom. Very dark, low-key image: the "
    "screen is the only light source, the dunes are almost invisible."
)
MOVING_END = (" The shot passes through the final frame while the camera is still orbiting at the same "
              "speed, with no settling and no freeze.")
MOVING_START = ("The shot begins already in motion: the camera is orbiting at the same constant speed from the "
                "very first frame, with no hold on the opening image. ")
RULES = (
    "No text, logos, people, buildings or new objects appear. Keep deep blacks and the same cool grading "
    "throughout; no flicker, no brightness pumping."
)
OPEN = (
    "The shot starts in complete darkness: the black crest of a sand dune, very close to the lens, fills the "
    "frame. As the camera orbits, the dark crest slides out of frame and reveals SUBJECT, already at its final "
    "position and size in the frame, first seen almost edge-on as a thin lit sliver, then opening steadily to a three-quarter "
    "view as the camera keeps travelling. While the subject is still turning: "
)
CLOSE = (
    " All through this the camera keeps orbiting clockwise so SUBJECT turns steadily toward edge-on, and in "
    "the last second, without any change of speed, the "
    "black crest of a sand dune, very close to the lens, slides across the frame and covers it completely, "
    "ending in total darkness."
)
ROT = {
    "R1": {
        "subject": "a tall, slim black smartboard totem with two stacked glowing screens and a thin red light strip on its side",
        "rigid": "The totem is a rigid, solid object: its shape, proportions, straight edges, two screens, top "
                 "cap, plinth and red side strip stay exactly identical; no morphing, bending or extra parts.",
        "A": "a shaft of cool light pours from its lower screen onto the sand and a falcon takes shape deep inside the lower screen, flies forward, breaks through the screen surface "
             "with its wings spreading, and a stream of fine sand pours out with it and fans across the ground. "
             "By the final frame the falcon is in front of the screen, wings fully spread.",
        "B": "The falcon beats its wings once and flies out toward the camera, passing close over the lens and "
             "out of frame, while the stream of sand keeps pouring from the lower screen and spreading across the "
             "ground, then thins out.",
    },
    "R2": {
        "subject": "a slim black pedestrian smartboard totem with two stacked glowing screens",
        "rigid": "The totem is a rigid, solid object: its shape, proportions, two screens, top lens and pedestal "
                 "stay exactly identical; no morphing, bending or extra parts.",
        "A": "an oasis appears deep inside its lower screen; palm fronds grow "
             "forward and push out past the screen edge, and water begins to pour over the bottom edge of the "
             "screen onto the sand, the pool spreading toward the camera while small green shoots rise in the wet "
             "sand.",
        "B": "The water keeps falling and the pool keeps spreading across the sand toward the camera, catching "
             "cool reflections; the palm fronds sway gently and more shoots and reeds grow around the foot of the "
             "totem.",
    },
    "R3": {
        "subject": "a frameless clear glass panel standing upright on the sand, showing misty mountains inside it",
        "rigid": "The glass panel is a rigid, flat sheet: its square shape and thin faintly glowing white edges "
                 "stay exactly identical; no frame appears, no morphing.",
        "A": "mist rolls out of the mountain scene through the glass onto the "
             "sand; a camel walks forward from deep inside the scene, its head and neck pass through the glass "
             "surface, then its body, and it steps out onto the sand.",
        "B": "The camel keeps walking calmly out across the sand toward the camera and leaves the frame, with a "
             "natural gait and exactly four legs; the mist keeps flowing out of the glass and spreading low over "
             "the sand.",
    },
    "R4": {
        "subject": "two frameless clear glass panels joined at a right angle into an outward-pointing corner, glowing "
                   "crimson from the mist inside",
        "rigid": "The two glass panels are rigid, flat sheets joined at a fixed 90-degree outer corner: their "
                 "shape and thin faintly glowing white edges stay exactly identical; no frame appears, no morphing.",
        "A": "crimson mist swirls deep inside it; a tall slender perfume "
             "bottle with no label rises from inside the corner and pushes out through the corner seam into the "
             "open air, rose petals drifting out with it and settling on the sand, crimson light spreading over "
             "the ground.",
        "B": "The bottle keeps rising slowly and turns a little in the air in front of the corner; more rose "
             "petals drift out and scatter across the sand toward the camera, and low crimson mist spreads from the "
             "foot of the glass. The bottle stays plain: no label, no text.",
    },
    "R5": {
        "subject": "a massive plain pale block with a huge glowing corner screen that shows a bare white showroom",
        "rigid": "The block and its corner screen are rigid and solid: their shape and edges stay exactly "
                 "identical; no morphing. The SUV stays one consistent, generic vehicle with a plain grille: no "
                 "badge, no logo, no number plate, no text.",
        "A": "a dark SUV deep inside the showroom on the screen switches on its headlights and drives forward without "
             "waiting, crosses the screen surface and drops onto the sand in front "
             "of the block, turning into a drift and throwing up fine sand.",
        "B": "The SUV drifts across the sand toward the camera, its tyres throwing a growing wave of fine sand; "
             "the wave of sand flies straight at the lens, hits it and covers the whole frame, and the image goes "
             "to total darkness.",
    },
}


def prompt(r: str, part: str) -> str:
    x = ROT[r]
    if part == "A":
        body = OPEN.replace("SUBJECT", x["subject"]) + x["A"] + MOVING_END
    else:
        tail = (" The camera keeps orbiting at the same speed until the frame is dark." if r == "R5"
                else CLOSE.replace("SUBJECT", "the product"))
        body = MOVING_START + x["B"] + tail
    return f"{CAMERA} {body} {x['rigid']} {RULES}"


def _arg(flag: str) -> str:
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv and sys.argv.index(flag) + 1 < len(sys.argv) else ""


ONLY = [n for n in _arg("--only").split(",") if n]
TAKE = _arg("--take")                      # e.g. --take 2 -> jobs/files named R1_A_t2 (a new take, old one kept)
SUFFIX = f"_t{TAKE}" if TAKE else ""


def names() -> list[str]:
    return [n for r in ROT for n in (f"{r}_A", f"{r}_B") if not ONLY or n in ONLY]


def plate(fmt: str) -> Path:
    return ORBIT / "wipe" / f"black_{fmt}.png"


def still(r: str, fmt: str) -> Path:
    return STILLS / f"{r}_{fmt}_v{PICKS[r]}.png"


def make_plates() -> None:
    import numpy as np
    from PIL import Image
    for fmt, (w, h) in SIZES.items():
        y = np.linspace(0, 1, h)[:, None]
        x = np.linspace(-1, 1, w)[None, :]
        g = (0.35 + 0.65 * y) * (1 - 0.25 * x ** 2)          # faint: slightly bluer low and in the centre
        rgb = np.stack([5 + 1 * g, 6 + 2 * g, 8 + 6 * g], -1)  # #050608 rising to about #06080E
        p = plate(fmt)
        p.parent.mkdir(parents=True, exist_ok=True)
        if p.exists():
            print("exists", p)
            continue
        Image.fromarray(rgb.round().astype("uint8")).save(p)
        print("wrote", p)


def params(n: str, fmt: str) -> dict:
    r, part = n.split("_")
    first, last = (plate(fmt), still(r, fmt)) if part == "A" else (still(r, fmt), plate(fmt))
    return {"image_url": hf.upload(first), "end_image_url": hf.upload(last), "prompt": prompt(r, part),
            "duration": DURATION, "resolution": RESOLUTION}


def out_dir(fmt: str) -> Path:
    return ORBIT / "clips" / fmt


def load(fmt: str) -> dict:
    f = out_dir(fmt) / "jobs.json"
    return json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}


def save(fmt: str, state: dict) -> None:
    out_dir(fmt).mkdir(parents=True, exist_ok=True)
    (out_dir(fmt) / "jobs.json").write_text(json.dumps(state, indent=2), encoding="utf-8")


def spent(state: dict) -> float:
    return sum(j.get("usd", 0) for j in state.values()
               if j.get("request_id") and j.get("status") not in ("failed", "nsfw"))


def frames_sheet(clip: Path, fps: int = 4) -> Path:
    probe = subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                     "stream=width,height:format=duration", "-of", "csv=p=0", str(clip)]).decode().split()
    w, h = (int(v) for v in probe[0].split(",")[:2])
    n = max(1, round(float(probe[1]) * fps))
    cols, cell = (4, 480) if w >= h else (8, 240)
    sheet = clip.with_name(f"{clip.stem}_sheet_4fps.jpg")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(clip), "-vf",
                    f"fps={fps},scale={cell}:-2,tile={cols}x{-(-n // cols)}:padding=4:color=0x161616",
                    "-frames:v", "1", "-q:v", "3", str(sheet)], check=True)
    return sheet


def run(fmt: str, confirm: bool, quote_only: bool = False) -> None:
    state = load(fmt)
    other = spent(load("9x16" if fmt == "16x9" else "16x9"))
    todo = [n for n in names() if not state.get(n + SUFFIX, {}).get("request_id")
            or state[n + SUFFIX].get("status") in ("failed", "nsfw")]
    built = {n: params(n, fmt) for n in todo}
    quotes = {n: hf.estimate(MODEL, p) for n, p in built.items()}
    for n, q in quotes.items():
        print(f"  {n}_{fmt}: {DURATION} s {RESOLUTION} = ${q:.4f}")
    total = sum(quotes.values())
    project = SPENT_BEFORE + other + spent(state) + total
    cap = hf.max_spend()
    print(f"{len(todo)} clips, quote ${total:.3f} (this format committed ${spent(state):.3f}, budget "
          f"${BUDGET_USD[fmt]:.2f}); project ${project:.2f} of cap ${cap:.2f}")
    if quote_only:
        return
    if spent(state) + total > BUDGET_USD[fmt] + 1e-6:
        raise hf.HiggsfieldError("Refused: above the approved budget for this format")
    if project > cap:
        raise hf.HiggsfieldError("Refused: total project spend would exceed HIGGSFIELD_MAX_SPEND_USD")
    if not confirm:
        return
    for n in todo:
        res = hf.generate(MODEL, built[n], confirm=True)
        state[n + SUFFIX] = {"request_id": res["request_id"], "usd": quotes[n], "status": res.get("status")}
        save(fmt, state)
    pending = [n + SUFFIX for n in names() if state.get(n + SUFFIX, {}).get("request_id")
               and not state[n + SUFFIX].get("file") and state[n + SUFFIX].get("status") not in ("failed", "nsfw")]
    start = time.time()
    while pending and time.time() - start < 3000:
        for n in list(pending):
            res = hf.status(state[n]["request_id"])
            state[n]["status"] = res.get("status")
            if res.get("status") == "completed":
                f = hf.download(res, out_dir(fmt), prefix=n)[0]
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
            save(fmt, state)
        if pending:
            time.sleep(10)
    if pending:
        print("still pending:", ", ".join(pending))


def preview(fmt: str) -> None:
    clips = [out_dir(fmt) / f"{n}.mp4" for r in ROT for n in (f"{r}_A", f"{r}_B")]
    missing = [c.name for c in clips if not c.exists()]
    if missing:
        raise hf.HiggsfieldError("Missing clips: " + ", ".join(missing))
    w, h = SIZES[fmt]
    pw, ph = (1280, 720) if w > h else (720, 1280)
    dest = ORBIT / "preview" / f"orbit_{fmt}_preview.mp4"
    dest.parent.mkdir(parents=True, exist_ok=True)
    lst = dest.with_suffix(".txt")
    lst.write_text("".join(f"file '{c.as_posix()}'\n" for c in clips), encoding="utf-8")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-an",
                    "-vf", f"scale={pw}:{ph},fps=24", "-c:v", "libx264", "-crf", "23", "-preset", "veryfast",
                    "-movflags", "+faststart", str(dest)], check=True)
    print(dest)


def main(argv: list[str]) -> int:
    cmd = argv[0] if argv else ""
    fmt = argv[1] if len(argv) > 1 and argv[1] in SIZES else "16x9"
    try:
        if cmd == "plates":
            make_plates()
        elif cmd == "prompts":
            for n in names():
                r, part = n.split("_")
                a, b = ("black plate", still(r, fmt).name) if part == "A" else (still(r, fmt).name, "black plate")
                print(f"#### {n}_{fmt}\n- {MODEL}, {DURATION} s, {RESOLUTION}; first frame: {a}; last frame: {b}\n\n> {prompt(r, part)}\n")
        elif cmd in ("quote", "run"):
            run(fmt, confirm=cmd == "run" and "--yes" in argv, quote_only=cmd == "quote")
        elif cmd == "preview":
            preview(fmt)
        else:
            print(__doc__)
            return 1
    except hf.HiggsfieldError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
