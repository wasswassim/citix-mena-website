"""Hero v5, P1: three look stills on the approved R3 glass-panel look (Marketing Studio Image, 16:9 1920x1080).

Every still uses media/hero_orbit/stills/R3_16x9_v3.png as its image reference and the same world / glass /
framing / avoid text that produced R3 v3 (imported from orbit_stills.py, unchanged). Only the content changes.

Usage:
  python scripts/orbit_v5_stills.py prompts
  python scripts/orbit_v5_stills.py quote            # free /estimate
  python scripts/orbit_v5_stills.py run --yes        # only after Wassim's OK on the exact quote
  python scripts/orbit_v5_stills.py sheet            # R3 v3 next to the 3 new stills
Options: --only S1,S4  (rerolls: --take N)
State: media/hero_orbit/v5/stills/jobs.json. Refuses above BUDGET_USD or the .env spend cap.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import higgsfield as hf  # noqa: E402
import orbit_stills as os3  # noqa: E402  (WORLD3, GLASS, FRAME3, AVOID: the exact R3 v3 wording)

MODEL = "marketing-studio/image"
ORBIT = hf.ROOT / "media" / "hero_orbit"
OUT = ORBIT / "v5" / "stills"
STATE = OUT / "jobs.json"
R3_STILL = ORBIT / "stills" / "R3_16x9_v3.png"
SPENT_BEFORE = 19.53          # project spend at the start of v5 (runbook v5, 14 Nov 2026)
BUDGET_USD = 0.0              # set to the exact quote only after Wassim's OK at GATE 1
W, H = 1920, 1080
BASE = {"resolution": "2k", "quality": "medium", "enhance_prompt": False, "aspect_ratio": "16:9"}

REF = (
    "REFERENCE IMAGE: keep everything from the reference image exactly: the same frameless glass panel at the "
    "same size, position and angle in the frame, the same low camera, the same dunes, the same darkness and the "
    "same cool slate-blue grading. Change ONLY what is inside the glass and what comes out of it: the mountains "
    "and the camel are gone completely."
)
CONTENT = {
    "S1_oasis": (
        "Inside the glass: a moonlit desert oasis, a dark, still pool of water fringed by date palms (long "
        "feather-shaped fronds), seen from inside the scene. Coming out of it: a smooth sheet of clear water pours "
        "forward through the glass surface, as if the glass were the edge of the pool, and spills onto the sand in "
        "a low wave that darkens the sand and spreads toward the camera, catching the cool light. A few date palm "
        "fronds push out through the glass surface into the open air in front of the panel. Low mist and a few "
        "drops follow the water. One colour family: cool teal and slate blue."
    ),
    "S3_perfume": (
        "Inside the glass: a deep pink-red haze (deep crimson-rose, not neon) with slowly drifting rose petals. "
        "The pink-red light stays inside the glass and on the sand just in front of it; everything else stays "
        "cool slate-blue. Coming out of it: one tall, faceted clear-glass perfume bottle with a heavy faceted "
        "glass stopper, no label, no logo, no text, halfway through the glass surface: its stopper and upper half "
        "already in the open air in front of the panel, its lower half still inside the pink haze. Rose petals "
        "and soft pink mist spill out with it and drift low over the sand. Exactly one bottle. One colour family: "
        "crimson-rose inside the glass, slate blue outside."
    ),
    "S4_suv": (
        "Inside the glass: a dark desert sand track between dunes at night. Coming out of it: a dark graphite, "
        "generic luxury full-size SUV bursts out of the glass front first, headlights on (cool white). Its front "
        "half is already in the open air in front of the panel, its front wheels are hitting the sand and "
        "throwing a spray of sand toward the camera, and its rear is still inside the glass. It is not any real "
        "model: plain body-colour grille, no badges, no logos, no grille emblem, no number plates, exactly four "
        "wheels. The glass stays perfectly intact: no shattering, no cracks, no fragments. One colour family: "
        "cool white on blue-black."
    ),
}


def _arg(flag: str) -> str:
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv and sys.argv.index(flag) + 1 < len(sys.argv) else ""


ONLY = [s for s in _arg("--only").split(",") if s]
TAKE = _arg("--take")


def prompt(s: str) -> str:
    return f"{REF} {os3.WORLD3} {os3.GLASS} {CONTENT[s]}{os3.FRAME3['16:9']} {os3.AVOID}"


def key(s: str) -> str:
    return f"{s}_t{TAKE}" if TAKE else s


def jobs(upload: bool = True) -> dict:
    ref = hf.upload(R3_STILL) if upload else R3_STILL.name
    return {key(s): {**BASE, "prompt": prompt(s), "image_urls": [ref]}
            for s in CONTENT if not ONLY or any(s.startswith(o) for o in ONLY)}


def load() -> dict:
    return json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}


def save(state: dict) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def spent(state: dict) -> float:
    return sum(j.get("usd", 0) for j in state.values() if j.get("request_id") and j.get("status") not in ("failed", "nsfw"))


def finish(k: str, res: dict, state: dict) -> None:
    from PIL import Image
    f = hf.download(res, OUT, prefix=k)[0]
    raw = f.with_name(f"{k}_raw{f.suffix}")
    f.replace(raw)
    im = Image.open(raw).convert("RGB")
    s = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x, y = (im.width - W) // 2, (im.height - H) // 2
    final = OUT / f"{k}.png"
    im.crop((x, y, x + W, y + H)).save(final)
    state[k].update(file=str(final), raw=str(raw))


def run(confirm: bool) -> None:
    state = load()
    todo = {k: p for k, p in jobs().items() if not state.get(k, {}).get("request_id")
            or state[k].get("status") in ("failed", "nsfw")}
    q = {k: hf.estimate(MODEL, p) for k, p in todo.items()}
    total, cap = sum(q.values()), hf.max_spend()
    print(f"{len(todo)} stills, quote ${total:.4f}; budget ${BUDGET_USD:.4f}; project "
          f"${SPENT_BEFORE + spent(state) + total:.2f} of cap ${cap:.2f}")
    if not confirm:
        return
    if total > BUDGET_USD + 1e-9:
        raise hf.HiggsfieldError("Refused: above the approved budget for this run")
    if SPENT_BEFORE + spent(state) + total > cap:
        raise hf.HiggsfieldError("Refused: total project spend would exceed HIGGSFIELD_MAX_SPEND_USD")
    for k, p in todo.items():
        res = hf.generate(MODEL, p, confirm=True)
        state[k] = {"request_id": res["request_id"], "usd": q[k], "status": res.get("status")}
        save(state)
    pending = [k for k in todo if state[k].get("status") not in ("failed", "nsfw")]
    start = time.time()
    while pending and time.time() - start < 1800:
        for k in list(pending):
            res = hf.status(state[k]["request_id"])
            state[k]["status"] = st = res.get("status")
            if st == "completed":
                finish(k, res, state)
                print(f"done   {k}")
                pending.remove(k)
            elif st in hf.TERMINAL:
                state[k]["error"] = json.dumps(res)[:300]
                print(f"{st:6} {k}")
                pending.remove(k)
            save(state)
        if pending:
            time.sleep(8)
    print(f"v5 stills spend ${spent(state):.4f}; project ${SPENT_BEFORE + spent(state):.2f}; pending: {', '.join(pending) or 'none'}")


def sheet() -> Path:
    from PIL import Image, ImageDraw, ImageFont
    F = ImageFont.truetype(r"C:\Windows\Fonts\GOTHICB.TTF", 22)
    tw, th = 768, 432
    tiles = [("R3 camel (approved look)", R3_STILL)]
    for s in CONTENT:
        takes = sorted(OUT.glob(f"{s}*.png"))
        takes = [t for t in takes if "_raw" not in t.stem]
        tiles.append((s, takes[-1] if takes else OUT / f"{s}.png"))
    S = Image.new("RGB", (40 + 2 * tw + 20 + 40, 70 + 2 * (th + 46)), (22, 22, 22))
    d = ImageDraw.Draw(S)
    d.text((40, 22), "Hero v5 - P1 look stills   media/hero_orbit/v5/stills/", font=F, fill=(255, 255, 255))
    for i, (label, f) in enumerate(tiles):
        x, y = 40 + (i % 2) * (tw + 20), 70 + (i // 2) * (th + 46)
        if f.exists():
            S.paste(Image.open(f).convert("RGB").resize((tw, th), Image.LANCZOS), (x, y))
        d.text((x, y + th + 6), f"{label}  -  {f.name}", font=F, fill=(224, 224, 224) if f.exists() else (253, 3, 50))
    out = OUT / "_v5_stills_sheet.jpg"
    OUT.mkdir(parents=True, exist_ok=True)
    S.save(out, quality=88)
    return out


def main(argv: list[str]) -> int:
    cmd = argv[0] if argv else ""
    try:
        if cmd == "prompts":
            for k, p in jobs(upload=False).items():
                print(f"#### {k}\n- {MODEL}, 16:9 -> {W}x{H}, {p['resolution']}, quality {p['quality']}, 1 variation; "
                      f"image ref `{R3_STILL.name}`\n\n> {p['prompt']}\n")
        elif cmd == "quote":
            q = {k: hf.estimate(MODEL, p) for k, p in jobs().items()}
            for k, usd in q.items():
                print(f"{k:12} ${usd:.4f}")
            print(f"TOTAL ${sum(q.values()):.4f}")
        elif cmd == "run":
            run("--yes" in argv)
        elif cmd == "sheet":
            print(sheet())
        else:
            print(__doc__)
            return 1
    except hf.HiggsfieldError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
