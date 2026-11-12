"""Cut Tom out of the chosen hero pair and build registered night/day cut-outs (local, no API cost).

Input : media/generated/drafts/hero_night_16x9_v1.png + hero_day_16x9_v1.png (same framing).
Output: media/generated/hero_cutout/tom_{night,day}.{png,webp} (transparent, identical canvas),
        preview_on_dark.jpg, preview_on_blue.jpg, proportions_compare.jpg

Method (all deterministic, so night and day stay pixel-registered):
  1. Mask from the DAY frame: Tom is the only dark object against a bright sky. Threshold,
     keep the component touching the bottom centre, fill the screens (enclosed bright areas).
     The same mask is applied to both frames.
  2. Restore the plinth, which the frame cut off: stretch the visible plinth strip downward
     to PLINTH_RATIO of the body height (ref 01: plinth is about 0.18 of the body height).
  3. Straighten the slight keystone (low camera) so the body's side edges are vertical: a
     true front view. Same transform for night and day.
  4. Uniform horizontal scale so the chosen proportion is exact.

  5. Day only: repaint the pale-blue sky reflection on the right side face in the body's black.

Usage: python scripts/hero_cutout.py [--mode overall|body]
  overall (default, CHOSEN by Wassim 12 Nov 2026): total height ground-to-cap : width = 3.5
                     (7 m x 2 m including plinth and cap)
  body             : screen body height : width = 3.5 (rejected: too narrow; outputs archived)
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
DRAFTS = ROOT / "media" / "generated" / "drafts"
OUT = ROOT / "media" / "generated" / "hero_cutout"
NIGHT, DAY = DRAFTS / "hero_night_16x9_v1.png", DRAFTS / "hero_day_16x9_v1.png"
PLINTH_RATIO = 0.18   # plinth height / body height, measured on ref 01
TARGET = 3.5          # height : width
PAD = 40              # transparent margin left/right/top in the exported canvas


def tom_mask(day: Image.Image) -> np.ndarray:
    """Boolean mask of Tom from the day frame."""
    rgb = np.asarray(day.convert("RGB")).astype(np.int16)
    lum = rgb.mean(axis=2)
    h, w = lum.shape
    dark = Image.fromarray(((lum < 95) * 255).astype(np.uint8))
    dark = dark.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.MinFilter(3))  # close pinholes
    # keep only the dark component connected to the plinth at the bottom centre
    seed_x = int(np.argmax(np.asarray(dark)[h - 3, :] > 0)) + 20
    comp = dark.copy()
    ImageDraw.floodfill(comp, (seed_x, h - 3), 128)
    body = np.asarray(comp) == 128
    # fill enclosed holes (the bright screens): flood the outside from a corner
    outside = Image.fromarray((~body * 255).astype(np.uint8)).copy()
    ImageDraw.floodfill(outside, (0, 0), 128)
    return np.asarray(outside) != 128


def measure(mask: np.ndarray) -> dict:
    h, w = mask.shape
    widths = mask.sum(axis=1)
    rows = np.where(widths > 0)[0]
    top = int(rows[0])
    body_w = int(np.percentile(widths[rows], 80))             # typical body width
    is_body = widths > body_w * 0.85
    body_rows = np.where(is_body)[0]
    body_top, body_bottom = int(body_rows[0]), int(body_rows[-1])
    cols = np.where(mask[body_top:body_bottom].any(axis=0))[0]
    return {"top": top, "body_top": body_top, "body_bottom": body_bottom, "bottom": h - 1,
            "left": int(cols[0]), "right": int(cols[-1]), "body_w": int(cols[-1] - cols[0] + 1),
            "body_h": body_bottom - body_top + 1, "plinth_visible": h - 1 - body_bottom}


def darken_day_side(day: Image.Image, mask: np.ndarray, g: dict) -> Image.Image:
    """Day frame only: the right side face picked up a pale-blue sky reflection. Repaint it in the
    body's own matte black so the side reads dark. Colour only: geometry and mask are untouched,
    so night/day registration is unchanged."""
    rgb = np.asarray(day.convert("RGB")).astype(np.int16).copy()
    band = np.zeros(mask.shape, bool)
    band[:, g["right"] - 17:] = True                      # the side face is about 17 px wide here
    lum = rgb.mean(axis=2)
    target = mask & band
    frame = mask & ~band & (lum < 45)                      # the body's own dark bezel pixels
    frame[:g["body_top"]] = False
    frame[g["body_bottom"]:] = False
    body_dark = np.median(rgb[frame], axis=0)
    rgb[target] = body_dark
    out = Image.fromarray(rgb.astype(np.uint8), "RGB")
    # soften the repainted band's inner seam by 1 px
    soft = out.filter(ImageFilter.GaussianBlur(1.0))
    m = Image.fromarray((target * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(3))
    out.paste(soft, (0, 0), m)
    return out


def cut(img: Image.Image, mask: np.ndarray) -> Image.Image:
    m = Image.fromarray((mask * 255).astype(np.uint8))
    m = m.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8))  # 1 px inset + soft edge
    out = img.convert("RGBA")
    out.putalpha(m)
    return out


def straighten(rgba: Image.Image, mask: np.ndarray, g: dict) -> tuple[Image.Image, dict]:
    """Make the body's left and right edges vertical (row-wise linear remap, y unchanged)."""
    w, h = rgba.size
    y1, y2 = g["body_top"] + 40, g["body_bottom"] - 40

    def edges(y: int) -> tuple[float, float]:
        cols = np.where(mask[y - 3:y + 4].all(axis=0))[0]
        return float(cols[0]), float(cols[-1])

    (l1, r1), (l2, r2) = edges(y1), edges(y2)
    left = lambda y: l1 + (l2 - l1) * (y - y1) / (y2 - y1)
    right = lambda y: r1 + (r2 - r1) * (y - y1) / (y2 - y1)
    ym = (y1 + y2) / 2
    L, R = left(ym), right(ym)

    def src_x(x: float, y: float) -> float:
        return left(y) + (x - L) * (right(y) - left(y)) / (R - L)

    quad = (src_x(0, 0), 0, src_x(0, h), h, src_x(w, h), h, src_x(w, 0), 0)  # UL, LL, LR, UR
    out = rgba.transform((w, h), Image.QUAD, quad, Image.BICUBIC)
    g2 = dict(g, left=round(L), right=round(R), body_w=round(R - L + 1))
    g2["keystone_px"] = (round(l1 - l2, 1), round(r1 - r2, 1))
    return out, g2


def restore_plinth(rgba: Image.Image, g: dict) -> Image.Image:
    """Stretch the visible plinth strip down to the full plinth height."""
    w, h = rgba.size
    full = round(g["body_h"] * PLINTH_RATIO)
    y0 = g["body_bottom"] + 6                      # just below the body's lower edge
    strip = rgba.crop((0, y0, w, h))
    need = full - 6
    strip = strip.resize((w, need), Image.LANCZOS)
    canvas = Image.new("RGBA", (w, y0 + need), (0, 0, 0, 0))
    canvas.paste(rgba.crop((0, 0, w, y0)), (0, 0))
    canvas.paste(strip, (0, y0))
    return canvas


def finalize(rgba: Image.Image, g: dict, mode: str) -> tuple[Image.Image, dict]:
    full_plinth = round(g["body_h"] * PLINTH_RATIO)
    total_h = (g["body_bottom"] - g["top"] + 1) + full_plinth
    crop = rgba.crop((g["left"] - PAD, max(g["top"] - PAD, 0), g["right"] + 1 + PAD, rgba.size[1]))
    ref_h = total_h if mode == "overall" else g["body_h"]
    new_body_w = ref_h / TARGET
    sx = new_body_w / g["body_w"]
    new_w = round(crop.size[0] * sx)
    crop = crop.resize((new_w, crop.size[1]), Image.LANCZOS)
    info = {"mode": mode, "x_scale": round(sx, 4), "body_w": round(new_body_w), "body_h": g["body_h"],
            "total_h": total_h, "body_ratio": round(g["body_h"] / new_body_w, 2),
            "overall_ratio": round(total_h / new_body_w, 2), "canvas": crop.size}
    return crop, info


def on_bg(rgba: Image.Image, colour: tuple) -> Image.Image:
    bg = Image.new("RGBA", rgba.size, colour + (255,))
    bg.alpha_composite(rgba)
    return bg.convert("RGB")


def main(argv: list[str]) -> int:
    mode = argv[argv.index("--mode") + 1] if "--mode" in argv else "overall"
    suffix = "" if mode == "overall" else "_body35"
    OUT.mkdir(parents=True, exist_ok=True)
    night, day = Image.open(NIGHT), Image.open(DAY)
    assert night.size == day.size, "night and day frames differ in size"
    mask = tom_mask(day)
    g = measure(mask)
    print("measured in source frame:", g, "| body ratio 1 :", round(g["body_h"] / g["body_w"], 2))
    results = {}
    day = darken_day_side(day, mask, g)
    for name, img in (("night", night), ("day", day)):
        straight, g2 = straighten(cut(img, mask), mask, g)
        rgba, info = finalize(restore_plinth(straight, g2), g2, mode)
        rgba.save(OUT / f"tom_{name}{suffix}.png")
        rgba.save(OUT / f"tom_{name}{suffix}.webp", quality=92, method=6)
        results[name] = rgba
    print("keystone removed (left, right edge drift in px):", g2["keystone_px"])
    print("export:", info)
    if mode == "overall":
        for label, colour in (("dark", (22, 22, 22)), ("blue", (70, 140, 215))):
            a, b = on_bg(results["night"], colour), on_bg(results["day"], colour)
            sheet = Image.new("RGB", (a.size[0] * 2, a.size[1]), colour)
            sheet.paste(a, (0, 0)); sheet.paste(b, (a.size[0], 0))
            sheet.save(OUT / f"preview_on_{label}.jpg", quality=92)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
