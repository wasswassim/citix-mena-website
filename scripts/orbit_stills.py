"""Hero orbit H1: 10 reveal stills (5 rotations x 16:9 / 9:16) with Marketing Studio Image.

Usage:
  python scripts/orbit_stills.py prompts          # print the prompts as Markdown (for docs/higgsfield-map.md)
  python scripts/orbit_stills.py quote [--q high] # free: exact quote, no generation
  python scripts/orbit_stills.py run --yes        # submit, wait, download, resize (resumable)
  python scripts/orbit_stills.py quote --v2 / run --v2 --yes   # Gate 1b rerolls (R4, R5)
  python scripts/orbit_stills.py sheet            # contact sheet media/hero_orbit/stills/_stills_sheet.jpg

State lives in media/hero_orbit/stills/jobs.json, so a re-run never pays twice.
Refuses to start if this run would exceed BUDGET_USD, or if total project spend
(SPENT_BEFORE + this run) would exceed HIGGSFIELD_MAX_SPEND_USD in .env.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import higgsfield as hf  # noqa: E402

MODEL = "marketing-studio/image"
BUDGET_USD = 0.908        # Wassim approved "OK medium $0.908" at Gate 1a, 14 Nov 2026
REROLL_BUDGET_USD = 0.0   # set to the approved Gate 1b reroll quote before `run --v2 --yes`
SPENT_BEFORE = 11.43      # project spend before the hero orbit (runbook)
REFS = hf.ROOT / "media" / "hero_orbit" / "refs"
OUT = hf.ROOT / "media" / "hero_orbit" / "stills"
STATE = OUT / "jobs.json"
SIZES = {"16:9": (1920, 1080), "9:16": (1080, 1920)}
QUALITY = "high" if "--q" in sys.argv and "high" in sys.argv else "medium"
BASE = {"resolution": "2k", "quality": QUALITY, "enhance_prompt": False}

WORLD = (
    "Photorealistic cinematic night photograph. An empty dark void above rolling moonlit desert sand dunes: "
    "deep blue-black sky with no horizon glow, soft cool moonlight raking across the dune ridges, a light haze "
    "low over the sand. Cool blue night grading, high contrast, clean, minimal noise. The product stands alone "
    "on the sand, the only man-made object in the scene. Its screen is the main light source and throws soft "
    "volumetric cool light and shadows onto the sand in front of it. Camera at a three-quarter angle, "
    "mid-orbit around the product, cinematic 35 mm lens, slightly low eye level, shallow depth of field. "
    "The screen content BREAKS OUT of the flat screen plane into real 3D space in front of it: it crosses the "
    "bezel, is lit by the screen and casts real shadows on the sand."
)
AVOID = (
    "Avoid: warm, orange, yellow or golden tones; daylight or sunset; neon, acid or oversaturated colours; "
    "sci-fi or futuristic styling; abstract CGI look; landmarks, buildings, roads, cities, people; any text, "
    "lettering, numbers, logo, badge, brand or watermark anywhere, including on the product and in the "
    "screen content."
)
FRAME = {
    "16:9": " Wide composition: the product slightly right of centre, its full height visible with headroom, "
            "open dark void and dunes on the left side of the frame.",
    "9:16": " Vertical composition, composed for portrait (not a crop of a wide shot): the product centred, "
            "its full height filling about 70% of the frame, the content bursting upward and toward the camera.",
}

TOM = (
    "PRODUCT (reference images 1-3, reproduce exactly, do not redesign): the CITIX \"Tom\" roadside "
    "smartboard, a tall, slim vertical totem about 7 m high and 2 m wide (body about 1 : 3.5), very thin flat "
    "profile, matte black metal body. The front is almost all screen: two stacked portrait screens with "
    "rounded corners and very thin black bezels, the upper screen slightly shorter than the lower one. A small "
    "low black cap on the top edge, from the middle to the right edge, with one round camera lens at its right "
    "end; the cap is completely plain, no text or logo. A plain matte black rectangular plinth, narrower than "
    "the body and flush with its right edge. One thin vertical red LED light strip along the right side face, "
    "lit, exactly as in reference image 2. Ignore the content shown on the screens in the references."
)
JERRY = (
    "PRODUCT (reference images 1-2, reproduce exactly, do not redesign): the CITIX \"Jerry\" pedestrian "
    "smartboard, a slim free-standing vertical totem about 2.6 m tall and 1 m wide, matte black body. Small "
    "black top cap with one round camera lens on its left, otherwise plain, no text or logo. The front is two "
    "stacked portrait screens with rounded corners and thin black bezels: a shorter upper screen and a taller "
    "lower screen. It stands on a short, narrow black rectangular pedestal centred under the body. Ignore the "
    "content shown on the screens in the references."
)
GLASS = (
    "PRODUCT: an original, frameless, perfectly clear glass square panel about 3 m by 3 m and a few "
    "centimetres thick, standing upright on its bottom edge on the sand. No frame, no stand, no bezel; only a "
    "faint cool-white glow along its thin edges (white, not cyan, no coloured outline)."
)
BALOO = (
    "PRODUCT (reference images 1-3, keep the shape exactly): the CITIX \"Baloo\" giant 3D screen, shown as a "
    "standalone tall white tower: a slim, very tall white-clad corner column crowned by a stepped, pointed "
    "white spire. High on its corner, a tall portrait screen wraps around the corner, with large rounded "
    "corners, inside a thick white rounded frame with a short horizontal indicator light at its top right. "
    "Below the screen a black horizontal band, plain, no text or logo; below that white square cladding tiles "
    "down to the sand. Only this tower, no rest of the building. Ignore the content in the reference screen."
)
JUMBO = (
    "PRODUCT (reference images 1-2, keep the shape exactly): the CITIX \"Jumbo\" giant corner screen, shown "
    "as a standalone monolith: a massive plain off-white rectangular block whose lower corner holds one huge "
    "LED screen wrapping seamlessly around the corner across two faces, recessed under a deep overhang with a "
    "thin dark-wood soffit edge, so the content reads as a deep 3D room. Only the block: no shops, signs, "
    "windows or rest of the building. Ignore the content in the reference screens."
)

CONTENT = {
    "R1": ("The upper screen shows only a soft cool glow. Bursting out of the lower screen: a single saker falcon, "
           "wings fully spread, flying out toward the camera, head and wingtips already past the bezel in 3D "
           "space, sharp feathers lit by the screen; a spiral of fine sand swirls out of the screen around it."),
    "R2": ("The upper screen shows only a soft cool glow. Spilling out of the lower screen: an oasis. Fresh green "
           "date-palm fronds reach out past the bezel and clear water pours over the bottom edge of the screen, "
           "splashing onto the dunes and forming a small pool on the sand, with cool moonlit reflections."),
    "R3": ("Inside the glass: a misty night view of jagged, rocky Hajar-style mountains. An Arabian oryx (white "
           "coat, long straight ringed horns, dark face markings) steps out of the glass toward the camera, head, "
           "chest and front legs already in the 3D space in front of the panel; cool mist rolls off the mountains "
           "and flows out through the glass onto the sand."),
    "R4": ("Rising out of the screen: a tall, elegant, unbranded glass perfume bottle with a plain faceted cap and "
           "no label, emerging from the screen's 3D depth and lifting above the frame into open air, bathed in a "
           "soft pink-red light (deep crimson, not neon) that spills onto the white frame and the sand."),
    "R5": ("Drifting out of the corner screen toward the camera: a generic modern luxury SUV, dark graphite paint, "
           "of no real make or model, no badges, no grille logo, no number plates. Its front wheels are already "
           "on the sand and it throws up a wave of fine sand that sprays toward the lens."),
}
# Gate 1b reroll proposals (v2). Only these rotations get a v2 job.
REROLL = {
    "R4": ("Rising out of the screen: a tall, slender, unbranded glass perfume bottle with a softly tapered "
           "cylindrical body and a small round cap, no label, no square or faceted shapes, clearly emerging from "
           "the screen's 3D depth and lifting above the top of the frame into open air, bathed in a soft "
           "pink-red light (deep crimson, not neon) that spills onto the white frame and the sand."),
    "R5": ("The reference screens show a third-party advert: do NOT reproduce it (no bottle, no tree, no pink or "
           "red light, no room interior). Here the corner screen shows a deep, dark, cool-blue moonlit dune "
           "landscape receding into the block, lit only by cool white light. Drifting out of that screen toward "
           "the camera: a generic modern luxury SUV, dark graphite paint, of no real make or model, no badges, no "
           "grille logo, no number plates. Its rear is still inside the screen and its front wheels are already "
           "on the sand in front of the block, throwing up a wave of fine sand that sprays toward the lens."),
}

PRODUCT = {
    "R1": (TOM, ["tom/01_tom_day_photo_ad_neutral.png", "tom/02_tom_night_photo_ad_neutral.png", "tom/tom_night.png"]),
    "R2": (JERRY, ["jerry/jerry_01_studio_grey.png", "jerry/jerry_02_on_black.png"]),
    "R3": (GLASS, []),
    "R4": (BALOO, ["baloo/baloo_02_spire_screen_t1.75.png", "baloo/baloo_01_overview_t1.75.png",
                   "baloo/baloo_03_screen_base_detail_t1.75.png"]),
    "R5": (JUMBO, ["jumbo/jumbo_01_two_faces_t3.75.png", "jumbo/jumbo_03_two_faces_t9.25.png"]),
}


def tag(ar: str) -> str:
    return ar.replace(":", "x")


def prompt(r: str, ar: str, v: int = 1) -> str:
    content = REROLL[r] if v == 2 else CONTENT[r]
    return f"{WORLD} {PRODUCT[r][0]} {content}{FRAME[ar]} {AVOID}"


def jobs(upload: bool = True, v: int = 1) -> dict:
    out = {}
    for r in (REROLL if v == 2 else PRODUCT):
        refs = [hf.upload(REFS / p) if upload else str(p) for p in PRODUCT[r][1]]
        for ar in SIZES:
            params = {**BASE, "aspect_ratio": ar, "prompt": prompt(r, ar, v)}
            if refs:
                params["image_urls"] = refs
            out[f"{r}_{tag(ar)}_v{v}"] = params
    return out


def load() -> dict:
    return json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}


def save(state: dict) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def spent(state: dict) -> float:
    return sum(j.get("usd", 0) for j in state.values()
               if j.get("request_id") and j.get("status") not in ("failed", "nsfw"))


def quote(js: dict) -> dict:
    return {k: hf.estimate(MODEL, p) for k, p in js.items()}


def finish(k: str, res: dict, state: dict) -> None:
    from PIL import Image
    files = hf.download(res, OUT, prefix=k)
    raw = files[0].with_name(f"{k}_raw{files[0].suffix}")
    files[0].replace(raw)
    im = Image.open(raw).convert("RGB")
    w, h = SIZES[state[k]["aspect_ratio"]]
    s = max(w / im.width, h / im.height)  # cover, then centre-crop the tiny ratio difference
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x, y = (im.width - w) // 2, (im.height - h) // 2
    final = OUT / f"{k}.png"
    im.crop((x, y, x + w, y + h)).save(final)
    state[k].update(file=str(final), raw=str(raw))


def run(confirm: bool, v: int = 1) -> None:
    state = load()
    js = jobs(v=v)
    todo = {k: p for k, p in js.items() if not state.get(k, {}).get("request_id")
            or state[k].get("status") in ("failed", "nsfw")}
    q = quote(todo)
    total = sum(q.values())
    cap = hf.max_spend()
    print(f"{len(todo)} jobs, quote ${total:.3f}; this run budget ${(REROLL_BUDGET_USD if v == 2 else BUDGET_USD):.2f}; "
          f"project ${SPENT_BEFORE + spent(state) + total:.2f} of cap ${cap:.2f}")
    phase = sum(j.get("usd", 0) for k, j in state.items() if k.endswith(f"_v{v}") and j.get("request_id")
                and j.get("status") not in ("failed", "nsfw"))
    if phase + total > (REROLL_BUDGET_USD if v == 2 else BUDGET_USD) + 1e-9:
        raise hf.HiggsfieldError("Refused: above the approved budget for this run")
    if SPENT_BEFORE + spent(state) + total > cap:
        raise hf.HiggsfieldError("Refused: total project spend would exceed HIGGSFIELD_MAX_SPEND_USD")
    if not confirm:
        return
    for k, p in todo.items():
        res = hf.generate(MODEL, p, confirm=True)
        state[k] = {"request_id": res["request_id"], "usd": q[k], "status": res.get("status"),
                    "aspect_ratio": p["aspect_ratio"], "refs": len(p.get("image_urls", []))}
        save(state)
    pending = [k for k in js if state.get(k, {}).get("request_id") and not state[k].get("file")
               and state[k].get("status") not in ("failed", "nsfw")]
    start = time.time()
    while pending and time.time() - start < 1800:
        for k in list(pending):
            res = hf.status(state[k]["request_id"])
            st = res.get("status")
            state[k]["status"] = st
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
    print(f"committed spend this phase ${spent(state):.3f}; pending: {', '.join(pending) or 'none'}")


def sheet() -> None:
    from PIL import Image, ImageDraw, ImageFont
    F = ImageFont.truetype(r"C:\Windows\Fonts\GOTHICB.TTF", 24)
    tw, th, vw = 768, 432, 243  # 16:9 tile and matching 9:16 tile width
    S = Image.new("RGB", (40 + tw + 20 + vw + 40, 70 + 5 * (th + 50)), (22, 22, 22))
    d = ImageDraw.Draw(S)
    d.text((40, 20), "Hero orbit - H1 reveal stills (GATE 1b)   media/hero_orbit/stills/", font=F, fill=(255, 255, 255))
    for i, r in enumerate(PRODUCT):
        y = 70 + i * (th + 50)
        for ar, x, w in (("16:9", 40, tw), ("9:16", 60 + tw, vw)):
            f = OUT / f"{r}_{tag(ar)}_v1.png"
            if f.exists():
                S.paste(Image.open(f).convert("RGB").resize((w, th), Image.LANCZOS), (x, y))
            d.text((x, y + th + 6), f.name, font=F, fill=(253, 3, 50) if not f.exists() else (224, 224, 224))
    S.save(OUT / "_stills_sheet.jpg", quality=88)
    print(OUT / "_stills_sheet.jpg")


def main(argv: list[str]) -> int:
    cmd = argv[0] if argv else ""
    try:
        if cmd == "prompts":
            for k, p in jobs(upload=False, v=2 if "--v2" in argv else 1).items():
                refs = ", ".join(f"`{u}`" for u in p.get("image_urls", [])) or "none (original design)"
                print(f"#### {k}\n- {MODEL}, {p['aspect_ratio']}, {p['resolution']}, quality {p['quality']}; refs: {refs}\n\n> {p['prompt']}\n")
        elif cmd == "quote":
            q = quote(jobs(v=2 if "--v2" in argv else 1))
            for k, usd in q.items():
                print(f"{k:12} ${usd:.4f}")
            print(f"TOTAL ${sum(q.values()):.4f} ({len(q)} images, quality {QUALITY})")
        elif cmd == "run":
            run("--yes" in argv, 2 if "--v2" in argv else 1)
        elif cmd == "sheet":
            sheet()
        else:
            print(__doc__)
            return 1
    except hf.HiggsfieldError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
