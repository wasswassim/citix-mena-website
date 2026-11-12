"""Static hero test renders: Tom cut-out over a simple coded night sky and day sky (local, no API cost).

Tom is centred, base on the bottom edge, at 60% of frame height (16:9, 21:9) and 55% (9:16).
The skies here are placeholders for the canvas sky that Prompt 4 builds in code.

Output: media/generated/hero_test/hero_{night,day}_{16x9,21x9,9x16}.png, sheet.jpg,
        intro_end_frame_reference_1920x1080.png (= night 16:9, the intro film's last frame),
        ../hero_cutout/proportions_compare.jpg
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
CUT = ROOT / "media" / "generated" / "hero_cutout"
OUT = ROOT / "media" / "generated" / "hero_test"
PAD_TOP = 40  # transparent margin above the cap in the cut-out (see hero_cutout.PAD)
FORMATS = {"16x9": (3840, 2160, 0.60), "21x9": (3440, 1440, 0.60), "9x16": (1080, 1920, 0.55)}


def gradient(w: int, h: int, top: tuple, bottom: tuple) -> Image.Image:
    t = np.linspace(0, 1, h)[:, None, None]
    arr = np.array(top)[None, None, :] * (1 - t) + np.array(bottom)[None, None, :] * t
    return Image.fromarray(np.repeat(arr, w, axis=1).astype(np.uint8), "RGB")


def night_sky(w: int, h: int) -> Image.Image:
    img = gradient(w, h, (2, 5, 14), (10, 24, 54))
    rng = np.random.default_rng(7)
    layer = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(layer)
    for _ in range(int(w * h / 14000)):
        x, y = rng.uniform(0, w), rng.uniform(0, h * 0.9)
        r = rng.choice([0.6, 0.8, 1.1, 1.6], p=[0.5, 0.3, 0.15, 0.05]) * w / 3840 + 0.4
        a = int(rng.uniform(60, 190) * (1 - 0.6 * y / h))
        d.ellipse((x - r, y - r, x + r, y + r), fill=a)
    layer = layer.filter(ImageFilter.GaussianBlur(0.6))
    img.paste(Image.new("RGB", (w, h), (225, 232, 255)), (0, 0), layer)
    return img


def day_sky(w: int, h: int) -> Image.Image:
    img = gradient(w, h, (46, 124, 214), (158, 204, 244))
    rng = np.random.default_rng(11)
    s = 8
    layer = Image.new("L", (w // s, h // s), 0)
    d = ImageDraw.Draw(layer)
    for _ in range(9):
        cx, cy = rng.uniform(0, w / s), rng.uniform(h / s * 0.08, h / s * 0.8)
        if abs(cx - w / s / 2) < w / s * 0.09:      # keep the column behind Tom clear
            continue
        for _ in range(14):
            rx, ry = rng.uniform(10, 34) * w / 3840 * 1.6, rng.uniform(5, 13) * w / 3840 * 1.6
            ox, oy = rng.normal(0, 26 * w / 3840), rng.normal(0, 6 * w / 3840)
            d.ellipse((cx + ox - rx, cy + oy - ry, cx + ox + rx, cy + oy + ry), fill=int(rng.uniform(90, 170)))
    layer = layer.filter(ImageFilter.GaussianBlur(5 * w / 3840 + 2)).resize((w, h), Image.BICUBIC)
    img.paste(Image.new("RGB", (w, h), (250, 252, 255)), (0, 0), layer)
    return img


def place(sky: Image.Image, tom: Image.Image, frac: float) -> Image.Image:
    w, h = sky.size
    scale = frac * h / (tom.size[1] - PAD_TOP)
    t = tom.resize((round(tom.size[0] * scale), round(tom.size[1] * scale)), Image.LANCZOS)
    out = sky.convert("RGBA")
    out.alpha_composite(t, ((w - t.size[0]) // 2, h - t.size[1]))
    return out.convert("RGB")


def label(img: Image.Image, text: str) -> Image.Image:
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 22)
    d.rectangle((0, 0, img.size[0], 34), fill=(0, 0, 0))
    d.text((8, 5), text, fill=(255, 255, 255), font=font)
    return img


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    toms = {n: Image.open(CUT / f"tom_{n}.png") for n in ("night", "day")}
    thumbs = {}
    for tag, (w, h, frac) in FORMATS.items():
        for name, sky in (("night", night_sky(w, h)), ("day", day_sky(w, h))):
            img = place(sky, toms[name], frac)
            img.save(OUT / f"hero_{name}_{tag}.png")
            th = img.resize((round(img.size[0] * 520 / img.size[1]), 520), Image.LANCZOS)
            thumbs[(name, tag)] = label(th, f"hero_{name}_{tag}  (Tom = {int(frac * 100)}% of height)")
    Image.open(OUT / "hero_night_16x9.png").resize((1920, 1080), Image.LANCZOS).save(
        OUT / "intro_end_frame_reference_1920x1080.png")
    rows = []
    for name in ("night", "day"):
        ims = [thumbs[(name, t)] for t in FORMATS]
        row = Image.new("RGB", (sum(i.size[0] for i in ims) + 8 * (len(ims) - 1), 520), (22, 22, 22))
        x = 0
        for i in ims:
            row.paste(i, (x, 0)); x += i.size[0] + 8
        rows.append(row)
    sheet = Image.new("RGB", (rows[0].size[0], 520 * 2 + 8), (22, 22, 22))
    sheet.paste(rows[0], (0, 0)); sheet.paste(rows[1], (0, 528))
    sheet.save(OUT / "sheet.jpg", quality=90)

    # proportions comparison: real photo (ref 01) | overall 1:3.5 | body 1:3.5
    ref = Image.open(ROOT / "media" / "source" / "01_tom_day_photo.jpg").convert("RGB").crop((200, 85, 575, 1335))
    H = 1000
    panels = [label(ref.resize((round(ref.size[0] * H / ref.size[1]), H), Image.LANCZOS), "ref 01 (real, 3/4 view)")]
    for f, text in (("tom_day.png", "A: 7 x 2 m incl. plinth (chosen)"), ("archive_body35/tom_day_body35.png", "B: screen body 1 : 3.5 (rejected)")):
        t = Image.open(CUT / f)
        bg = Image.new("RGBA", (max(t.size[0], 330), t.size[1]), (120, 140, 160, 255))
        bg.alpha_composite(t, ((bg.size[0] - t.size[0]) // 2, 0))
        panels.append(label(bg.convert("RGB").resize((round(bg.size[0] * H / bg.size[1]), H), Image.LANCZOS), text))
    comp = Image.new("RGB", (sum(p.size[0] for p in panels) + 16, H), (22, 22, 22))
    x = 0
    for pnl in panels:
        comp.paste(pnl, (x, 0)); x += pnl.size[0] + 8
    comp.save(CUT / "proportions_compare.jpg", quality=92)
    print("rendered", len(FORMATS) * 2, "frames")
    return 0


if __name__ == "__main__":
    sys.exit(main())
