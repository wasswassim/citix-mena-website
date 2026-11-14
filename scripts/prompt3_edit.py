"""PROMPT 3: edit the 15 s intro film (local, no API cost).

  python scripts/prompt3_edit.py shots     # build the five shots for both formats
  python scripts/prompt3_edit.py export    # assemble + export to media/web/
  python scripts/prompt3_edit.py all

Timeline at 24 fps (360 frames): S1 0-2.5 s | Shot 2 2.5-5 s | Baloo 5-8 s | Jumbo 8-10.5 s | Shot 5 10.5-15 s.
Intermediates: media/generated/edit/<fmt>/. Deliverables: media/web/.

Shot 2: deflicker the Kling clip, then "Tom lock": the clean still of Tom (cut from the clip's
        first frame, with the screen content already on it) is composited over every frame with
        a smoothed scale/position track, so Tom cannot flicker.
Shot 5: deflicker, paint out the lingering palm (16:9), screen content fades in with the
        power-on, the clip is eased onto the hero still's exact Tom size/position, then a
        12-frame dissolve ends on the still itself (last frame == hero night frame).
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
GEN = ROOT / "media" / "generated"
EDIT = GEN / "edit"
WEB = ROOT / "media" / "web"
FPS = 24
SIZES = {"16x9": (1920, 1080), "9x16": (1080, 1920)}
# Gilroy is not installed and no licensed font files were supplied: Century Gothic Bold stands in.
FONT_BOLD = "C:/Windows/Fonts/GOTHICB.TTF"
FONT_REG = "C:/Windows/Fonts/GOTHIC.TTF"
PULSE, PULSE_DARK = (253, 3, 50), (153, 3, 50)
DEFLICKER = "deflicker=mode=pm:size=5"


# ---------------------------------------------------------------- ffmpeg frame IO

def read(clip: Path, vf: str | None = None):
    w, h = (int(x) for x in subprocess.check_output(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
         "-of", "csv=p=0", str(clip)]).decode().strip().split(",")[:2])
    cmd = ["ffmpeg", "-v", "error", "-i", str(clip)] + (["-vf", vf] if vf else []) + \
          ["-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    n = w * h * 3
    while True:
        buf = proc.stdout.read(n)
        if len(buf) < n:
            break
        yield np.frombuffer(buf, np.uint8).reshape(h, w, 3)
    proc.wait()


class Writer:
    def __init__(self, path: Path, size: tuple[int, int]):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.p = subprocess.Popen(
            ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{size[0]}x{size[1]}",
             "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "fast", "-crf", "10", "-pix_fmt", "yuv420p",
             str(path)], stdin=subprocess.PIPE)

    def add(self, frame) -> None:
        self.p.stdin.write(np.asarray(frame, np.uint8).tobytes())

    def close(self) -> None:
        self.p.stdin.close()
        self.p.wait()


def ff(*args: str) -> None:
    subprocess.run(["ffmpeg", "-v", "error", "-y", *args], check=True)


# ---------------------------------------------------------------- screen content plates

def _grad(w: int, h: int, top: tuple, bottom: tuple) -> Image.Image:
    t = np.linspace(0, 1, h)[:, None, None]
    arr = np.array(top)[None, None, :] * (1 - t) + np.array(bottom)[None, None, :] * t
    return Image.fromarray(np.repeat(arr, w, axis=1).astype(np.uint8), "RGB")


def _centre(d: ImageDraw.ImageDraw, w: int, y: int, text: str, font, fill) -> None:
    d.text(((w - d.textlength(text, font=font)) / 2, y), text, font=font, fill=fill)


def plate_widget(w: int = 680, h: int = 1000) -> Image.Image:
    """Upper screen: CITIX-style night weather/time widget (after day_night.mp4 / refs 02, 10)."""
    img = _grad(w, h, (26, 18, 112), (52, 30, 176))
    d = ImageDraw.Draw(img)
    _centre(d, w, 60, "21:30", ImageFont.truetype(FONT_REG, 44), (206, 200, 255))
    _centre(d, w, 120, "Clear", ImageFont.truetype(FONT_BOLD, 92), (255, 255, 255))
    # crescent moon + star, drawn as outlines like the CITIX widget icon
    icon = Image.new("L", (w, h), 0)
    di = ImageDraw.Draw(icon)
    cx, cy, r = w // 2 - 10, 400, 118
    di.ellipse((cx - r, cy - r, cx + r, cy + r), fill=255)
    di.ellipse((cx - r + 70, cy - r - 46, cx + r + 70, cy + r - 46), fill=0)
    edge = ImageChops.subtract(icon.filter(ImageFilter.MaxFilter(13)), icon)
    glow = icon.filter(ImageFilter.GaussianBlur(26)).point(lambda v: int(v * 0.35))
    img.paste(Image.new("RGB", (w, h), (150, 120, 255)), (0, 0), glow)
    img.paste(Image.new("RGB", (w, h), (226, 214, 255)), (0, 0), edge)
    sx, sy = cx + 92, cy - 40
    star = [(sx, sy - 34), (sx + 9, sy - 9), (sx + 34, sy), (sx + 9, sy + 9), (sx, sy + 34),
            (sx - 9, sy + 9), (sx - 34, sy), (sx - 9, sy - 9)]
    d.polygon(star, fill=(226, 214, 255))
    _centre(d, w, 580, "Today", ImageFont.truetype(FONT_BOLD, 50), (255, 255, 255))
    _centre(d, w, 640, "24\u00b0", ImageFont.truetype(FONT_BOLD, 170), (255, 255, 255))
    d.rounded_rectangle((60, 860, w - 60, 950), radius=30, fill=(40, 24, 138))
    _centre(d, w, 882, "Enjoy a peaceful evening", ImageFont.truetype(FONT_REG, 38), (220, 214, 255))
    return img


def plate_ad(w: int = 680, h: int = 1060) -> Image.Image:
    """Lower screen: neutral CITIX brand message on the Pulse Red gradient. No third-party brands."""
    img = _grad(w, h, PULSE, PULSE_DARK)
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(FONT_BOLD, 118)
    y = 250
    for line in ("Smarter", "cities.", "Stronger", "brands."):
        d.text((64, y), line, font=f, fill=(255, 255, 255))
        y += 140 if line != "cities." else 190
    return img


def rounded_alpha(size: tuple[int, int], radius_frac: float = 0.045) -> Image.Image:
    m = Image.new("L", size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), radius=int(size[0] * radius_frac), fill=255)
    return m


def _coeffs(dst_quad, src_size):
    """PIL PERSPECTIVE coefficients mapping the output quad (TL, TR, BR, BL) back to the source rect."""
    w, h = src_size
    src = [(0, 0), (w, 0), (w, h), (0, h)]
    a = []
    for (x, y), (u, v) in zip(dst_quad, src):
        a.append([x, y, 1, 0, 0, 0, -u * x, -u * y])
        a.append([0, 0, 0, x, y, 1, -v * x, -v * y])
    b = np.array(src, float).reshape(8)
    return np.linalg.solve(np.array(a, float), b).tolist()


def paste_quad(base: Image.Image, plate: Image.Image, quad) -> None:
    """Warp plate (with rounded corners) into quad (TL, TR, BR, BL) on base, in place."""
    rgba = plate.convert("RGBA")
    rgba.putalpha(rounded_alpha(plate.size))
    warped = rgba.transform(base.size, Image.PERSPECTIVE, _coeffs(quad, plate.size), Image.BICUBIC)
    base.paste(warped, (0, 0), warped)


# ---------------------------------------------------------------- shot 2: Tom lock

# Geometry measured on clips_input/s2_first_16x9.png (1920x1080).
S2_POLY = [(1218, 157), (1335, 150), (1335, 122), (1492, 110), (1502, 113), (1502, 1047),
           (1332, 1050), (1332, 921), (1218, 915)]


def to_9x16(pt):  # the 9:16 first frame is a crop of the 16:9 pick: x 1400..2255 of 2688, scaled to 1080 wide
    x, y = pt
    return ((x * 1.4 - 1400) * 1.26316, y * 1.76842)


def s2_screen_quads(still: Image.Image, fmt: str):
    """Find the two lit screens in the still and return their quads, expanded to near edge-to-edge."""
    lum = np.asarray(still.convert("L")).astype(int)
    conv = (lambda p: p) if fmt == "16x9" else to_9x16
    xl, xr = conv((1236, 0))[0], conv((1470, 0))[0]
    pad = 5 if fmt == "16x9" else 8

    def runs(x: float):
        col = lum[:, int(x)] > 150
        y0, y1 = conv((0, 120))[1], conv((0, 960))[1]
        idx = np.where(col[int(y0):int(y1)])[0] + int(y0)
        splits = np.where(np.diff(idx) > 3)[0]
        segs = np.split(idx, splits + 1)
        segs = sorted(segs, key=len, reverse=True)[:2]
        segs.sort(key=lambda s: s[0])
        return [(int(s[0]), int(s[-1])) for s in segs]

    left, right = runs(xl), runs(xr)
    x_out_l, x_out_r = conv((1223, 0))[0], conv((1482, 0))[0]
    quads = []
    for (lt, lb), (rt, rb) in zip(left, right):
        def at(x, a, b):  # extend the edge line through (xl, a), (xr, b) to x
            return a + (b - a) * (x - xl) / (xr - xl)
        quads.append([(x_out_l, at(x_out_l, lt, rt) - pad), (x_out_r, at(x_out_r, lt, rt) - pad),
                      (x_out_r, at(x_out_r, lb, rb) + pad), (x_out_l, at(x_out_l, lb, rb) + pad)])
    return quads


def lit_box(frame: np.ndarray, win: tuple[float, float, float, float], thr: int):
    """Bounding box (x0, x1, y0, y1) of lit pixels inside a window given as fractions of the frame."""
    h, w = frame.shape[:2]
    x0, x1, y0, y1 = int(win[0] * w), int(win[1] * w), int(win[2] * h), int(win[3] * h)
    lum = frame[y0:y1, x0:x1].astype(np.int16).mean(axis=2)
    ys, xs = np.where(lum > thr)
    if len(xs) < 2000:
        return None
    bx0, bx1 = np.percentile(xs, [0.5, 99.5])
    by0, by1 = np.percentile(ys, [0.5, 99.5])
    return (x0 + bx0, x0 + bx1, y0 + by0, y0 + by1)


def shot2(fmt: str) -> Path:
    size = SIZES[fmt]
    still = Image.open(GEN / "clips_input" / f"s2_first_{fmt}.png").convert("RGB")
    conv = (lambda p: p) if fmt == "16x9" else to_9x16
    poly = [conv(p) for p in S2_POLY]
    # Tom layer = still + screen content, alpha = feathered polygon
    layer_rgb = still.copy()
    for quad, plate in zip(s2_screen_quads(still, fmt), (plate_widget(), plate_ad())):
        paste_quad(layer_rgb, plate, quad)
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).polygon(poly, fill=255)
    mask = mask.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(1.2))
    layer = layer_rgb.convert("RGBA")
    layer.putalpha(mask)

    xs = [p[0] for p in poly]; ys = [p[1] for p in poly]
    win = (min(xs) / size[0] - 0.02, max(xs) / size[0] + 0.0, max(min(ys) / size[1] - 0.02, 0), min(max(ys) / size[1], 1))
    clip = GEN / "clips" / f"s2_{fmt}_final_1080p.mp4"
    frames = list(read(clip, DEFLICKER))
    boxes = np.array([lit_box(f, win, 150) for f in frames], float)       # lit screens track the push-in
    cx, cy, hh = (boxes[:, 0] + boxes[:, 1]) / 2, (boxes[:, 2] + boxes[:, 3]) / 2, boxes[:, 3] - boxes[:, 2]
    t = np.arange(len(frames))
    fit = lambda v: np.polyval(np.polyfit(t, v, 2), t)                     # smooth: the move is slow and steady
    cx, cy, sc = fit(cx), fit(cy), fit(hh / hh[0])
    cx += boxes[0, [0, 1]].mean() - cx[0]; cy += boxes[0, [2, 3]].mean() - cy[0]; sc /= sc[0]
    c0 = (cx[0], cy[0])

    out = EDIT / fmt / "shot2.mp4"
    wr = Writer(out, size)
    for i in range(6, 66):                                                  # 60 frames = 2.5 s
        s = sc[i]
        moved = layer.transform(size, Image.AFFINE, (1 / s, 0, c0[0] - cx[i] / s, 0, 1 / s, c0[1] - cy[i] / s), Image.BICUBIC)
        base = Image.fromarray(frames[i]).convert("RGBA")
        base.alpha_composite(moved)
        wr.add(base.convert("RGB"))
    wr.close()
    print(f"shot2 {fmt}: push-in tracked, scale {sc[6]:.4f} -> {sc[65]:.4f}")
    return out


# ---------------------------------------------------------------- shot 5

def split_screens(frame: np.ndarray, box):
    """Split the lit box into upper and lower screen rects at the dark gap; expand slightly outward."""
    x0, x1, y0, y1 = box
    lum = frame[int(y0):int(y1), int(x0):int(x1)].astype(np.int16).mean(axis=(1, 2))
    n = len(lum)
    a, b = int(n * 0.35), int(n * 0.65)
    gap = a + int(np.argmin(lum[a:b]))
    g = max(2, round(n * 0.006))
    ex, ey = (x1 - x0) * 0.012, (y1 - y0) * 0.006
    return ((x0 - ex, y0 - ey, x1 + ex, y0 + gap - g), (x0 - ex, y0 + gap + g, x1 + ex, y1 + ey))


def draw_content(img: Image.Image, frame: np.ndarray, box, plates, alpha: float) -> None:
    if alpha <= 0:
        return
    for rect, plate in zip(split_screens(frame, box), plates):
        x0, y0, x1, y1 = (round(v) for v in rect)
        p = plate.resize((x1 - x0, y1 - y0), Image.LANCZOS)
        m = rounded_alpha(p.size).point(lambda v: int(v * alpha))
        img.paste(p, (x0, y0), m)


def smooth(v: np.ndarray, k: int = 7) -> np.ndarray:
    out = v.copy()
    ok = ~np.isnan(v)
    idx = np.where(ok)[0]
    for i in idx:
        seg = v[max(idx[0], i - k // 2):i + k // 2 + 1]
        out[i] = np.nanmedian(seg)
    out2 = out.copy()
    for i in idx:
        seg = out[max(idx[0], i - 2):i + 3]
        out2[i] = np.nanmean(seg)
    return out2


def paint_out_palm(frame: np.ndarray, weight: float) -> np.ndarray:
    """Fill non-sky pixels in the bottom-left corner with the sky gradient of the same rows."""
    if weight <= 0:
        return frame
    h, w = frame.shape[:2]
    y0, x1 = int(h * 0.62), int(w * 0.36)
    region = frame[y0:, :x1].astype(np.float32)
    sky = np.median(frame[y0:, x1:int(w * 0.42)].astype(np.float32), axis=1)[:, None, :]
    diff = np.abs(region - sky).max(axis=2)
    m = Image.fromarray(((diff > 9) * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(15)).filter(ImageFilter.GaussianBlur(6))
    a = (np.asarray(m, np.float32) / 255 * weight)[..., None]
    a[:, -40:] *= np.linspace(1, 0, 40)[None, :, None]            # soft right edge of the patch
    out = frame.copy()
    out[y0:, :x1] = (region * (1 - a) + sky * a).astype(np.uint8)
    return out


def end_still(fmt: str) -> Image.Image:
    """Hero night frame with the same screen content: the film's last frame and media/web end frame."""
    src = GEN / "clips_input" / f"s5_last_{fmt}.png"
    still = Image.open(src).convert("RGB")
    arr = np.asarray(still)
    box = lit_box(arr, (0.3, 0.7, 0.0, 1.0), 70)
    draw_content(still, arr, box, (plate_widget(), plate_ad()), 1.0)
    return still


def shot5(fmt: str) -> Path:
    size = SIZES[fmt]
    plates = (plate_widget(), plate_ad())
    clip = GEN / "clips" / f"s5_{fmt}_final_1080p.mp4"
    src = list(read(clip, DEFLICKER))[13:121]                         # 108 frames = 4.5 s, ends on Kling's last frame
    n = len(src)
    win = (0.36, 0.64, 0.0, 1.0)
    raw, lum = np.full((n, 4), np.nan), np.zeros(n)
    for i, f in enumerate(src):
        b = lit_box(f, win, 70)
        if b:
            inside = f[int(b[2]):int(b[3]), int(b[0]):int(b[1])].astype(np.int16).mean()
            if inside > 60:
                raw[i], lum[i] = b, inside
    box = np.stack([smooth(raw[:, k]) for k in range(4)], axis=1)
    alpha = np.clip((lum - 75) / (150 - 75), 0, 1)
    alpha = np.maximum.accumulate(alpha)                             # content never fades back out

    still = end_still(fmt)
    sarr = np.asarray(Image.open(GEN / "clips_input" / f"s5_last_{fmt}.png").convert("RGB"))
    sb = np.array(lit_box(sarr, (0.3, 0.7, 0.0, 1.0), 70))
    still_np = np.asarray(still, np.float32)

    out = EDIT / fmt / "shot5.mp4"
    wr = Writer(out, size)
    pad = 120
    for i, f in enumerate(src):
        if fmt == "16x9":
            f = paint_out_palm(f, float(np.clip((i + 13 - 56) / 8, 0, 1)))
        img = Image.fromarray(f)
        if not np.isnan(box[i]).any():
            draw_content(img, f, box[i], plates, float(alpha[i]))
            # ease the whole frame so Tom's screens land exactly on the still's screens by frame 96
            u = float(np.clip((i - 60) / 36, 0, 1)); wgt = u * u * (3 - 2 * u)
            b = box[i]
            bc, bh = ((b[0] + b[1]) / 2, (b[2] + b[3]) / 2), b[3] - b[2]
            tc, th = ((sb[0] + sb[1]) / 2, (sb[2] + sb[3]) / 2), sb[3] - sb[2]
            dc = (bc[0] + wgt * (tc[0] - bc[0]), bc[1] + wgt * (tc[1] - bc[1]))
            s = (bh + wgt * (th - bh)) / bh
            padded = Image.fromarray(np.pad(np.asarray(img), ((pad, pad), (pad, pad), (0, 0)), mode="edge"))
            img = padded.transform(size, Image.AFFINE,
                                   (1 / s, 0, bc[0] + pad - dc[0] / s, 0, 1 / s, bc[1] + pad - dc[1] / s), Image.BICUBIC)
        if i >= n - 12:                                              # 12-frame dissolve onto the still
            a = (i - (n - 13)) / 12
            img = Image.fromarray((np.asarray(img, np.float32) * (1 - a) + still_np * a).astype(np.uint8))
        wr.add(img)
    wr.close()
    still.save(EDIT / fmt / "end_still.png")
    on = int(np.argmax(alpha > 0)); full = int(np.argmax(alpha >= 1))
    print(f"shot5 {fmt}: content fades in over shot frames {on}-{full} ({on / FPS:.2f}-{full / FPS:.2f} s); "
          f"end match scale {sb[3] - sb[2]:.0f}/{box[95][3] - box[95][2]:.0f} px")
    return out


# ---------------------------------------------------------------- shots 1, 3, 4 (real footage)

BLUE_HOUR = ("eq=brightness=0.03:contrast=1.15:saturation=0.8:gamma=1.10,"
             "colorbalance=rs=-0.12:gs=-0.02:bs=0.14:rm=-0.10:gm=-0.01:bm=0.12:rh=-0.13:gh=-0.02:bh=0.10")
COOL_DAY = "eq=contrast=1.12:saturation=0.9,colorbalance=rs=-0.04:bs=0.05:rm=-0.04:bm=0.05:rh=-0.03:bh=0.04"

REAL = {
    # name: (source, start s, duration s, conform filter, grade, 9:16 crop "w:h:x:y" as expressions)
    "shot1": ("media/stock/S1_flag_island_sharjah_pexels_8396981.mp4", 0.5, 2.6, "setpts=N/24/TB", BLUE_HOUR,
              "ih*9/16:ih:iw*0.475-ih*9/32:0"),
    "shot3": ("media/source/baloo_3d_real_4k.mp4", 2.0, 3.0, "fps=24", COOL_DAY, "ih*9/16:ih:iw*0.555-ih*9/32:0"),
    "shot4": ("media/source/jumbo_3d_real.mp4", 2.5, 2.5, "fps=24", COOL_DAY, "ih*9/16:ih:iw*0.56-ih*9/32:0"),
}
FRAMES = {"shot1": 60, "shot2": 60, "shot3": 72, "shot4": 60, "shot5": 108}


def real_shot(name: str, fmt: str) -> Path:
    src, ss, dur, conform, grade, crop = REAL[name]
    w, h = SIZES[fmt]
    vf = [conform]
    if fmt == "9x16":
        vf.append(f"crop={crop}")
    vf += [f"scale={w}:{h}:flags=lanczos", "setsar=1", grade]
    out = EDIT / fmt / f"{name}.mp4"
    out.parent.mkdir(parents=True, exist_ok=True)
    ff("-ss", str(ss), "-t", str(dur), "-i", str(ROOT / src), "-vf", ",".join(vf), "-r", str(FPS),
       "-frames:v", str(FRAMES[name]), "-an", "-c:v", "libx264", "-preset", "fast", "-crf", "10",
       "-pix_fmt", "yuv420p", str(out))
    return out


# ---------------------------------------------------------------- assembly + export

# common cool, slightly contrasty finish on shots 1-4 (t < 10.5 s)
FINISH = "eq=contrast=1.04:enable='lt(t,10.5)',colorbalance=bs=0.02:bm=0.01:enable='lt(t,10.5)'"
TITLES = [(0.0, 2.5, "SMARTER CITIES."), (5.0, 8.0, "STRONGER BRANDS."), (10.5, 15.0, "WE MAKE TOMORROW HAPPEN TODAY")]


def export() -> None:
    WEB.mkdir(parents=True, exist_ok=True)
    report = []
    for fmt, tag, mp4_crf, webm_crf in (("16x9", "desktop", 21, 33), ("9x16", "mobile", 24, 37)):
        lst = EDIT / fmt / "concat.txt"
        lst.write_text("".join(f"file '{(EDIT / fmt / f'{s}.mp4').as_posix()}'\n" for s in FRAMES), encoding="utf-8")
        master = EDIT / fmt / "master.mp4"
        # shots 1-4 get the common finish; shot 5 must end exactly on the hero still, so it is left untouched
        ff("-f", "concat", "-safe", "0", "-i", str(lst), "-vf", FINISH, "-c:v", "libx264", "-preset", "slow", "-crf", "10", "-pix_fmt", "yuv420p", "-an", str(master))
        mp4, webm = WEB / f"intro-{tag}.mp4", WEB / f"intro-{tag}.webm"
        ff("-i", str(master), "-c:v", "libx264", "-preset", "slow", "-crf", str(mp4_crf), "-profile:v", "high",
           "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-an", str(mp4))
        ff("-i", str(master), "-c:v", "libvpx-vp9", "-crf", str(webm_crf), "-b:v", "0", "-row-mt", "1",
           "-pix_fmt", "yuv420p", "-an", str(webm))
        suffix = "" if tag == "desktop" else "-mobile"
        ff("-i", str(master), "-frames:v", "1", "-q:v", "3", str(WEB / f"poster{suffix}.jpg"))
        Image.open(EDIT / fmt / "end_still.png").save(WEB / f"end{suffix}.jpg", quality=90)
        for f in (mp4, webm):
            report.append(f"{f.name}: {f.stat().st_size / 1048576:.2f} MB")
    # review copy with the overlay lines burnt in (on the site they are real HTML over the video)
    font = FONT_BOLD.replace(":", "\\:")
    dt = ",".join(f"drawtext=fontfile='{font}':text='{t}':fontsize=44:fontcolor=white:x=60:y=h-110:"
                  f"enable='between(t,{a},{b - 0.01})'" for a, b, t in TITLES)
    ff("-i", str(EDIT / "16x9" / "master.mp4"), "-vf", f"scale=1280:720,{dt}", "-c:v", "libx264", "-preset", "slow",
       "-crf", "25", "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-an", str(WEB / "intro-preview.mp4"))
    report.append(f"intro-preview.mp4: {(WEB / 'intro-preview.mp4').stat().st_size / 1048576:.2f} MB")
    print("\n".join(report))


def shots() -> None:
    for fmt in SIZES:
        for name in REAL:
            real_shot(name, fmt)
        shot2(fmt)
        shot5(fmt)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd in ("shots", "all"):
        shots()
    if cmd in ("export", "all"):
        export()
    if cmd not in ("shots", "export", "all"):
        print(__doc__)
