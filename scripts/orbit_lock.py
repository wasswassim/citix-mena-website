"""Hero orbit: lock the product in the frame of a generated clip (no credits).

Wassim (14 Nov 2026): the orbit must keep the same distance at the beginning, middle and end:
no push-in, no pull-back. Generated clips drift and zoom a little, and Seedance pulled back
before the final wipe. This tool removes that in the edit:

  1. track Tom in every frame: red side strip = position, upper screen = size (nothing crosses it);
  2. smooth the track;
  3. scale and shift every frame so Tom keeps ONE size and ONE position (frame edges are extended, not black);
  4. cut the clip where the needed zoom would get too soft (MAX_SCALE) and close it with a
     black dune wipe drawn in code, so the end is still a wipe to black.

Usage:
  python scripts/orbit_lock.py <in.mp4> <out.mp4> [--max-scale 1.35] [--wipe 0.8]
Prints the track before and after.
"""
from __future__ import annotations

import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter


PAD = 240  # px of edge extension around each source frame


def _arg(flag: str, default: float) -> float:
    return float(sys.argv[sys.argv.index(flag) + 1]) if flag in sys.argv else default


def probe(path: str) -> tuple[int, int, float]:
    out = subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                   "stream=width,height,r_frame_rate", "-of", "csv=p=0", path]).decode().strip().split(",")
    num, den = out[2].split("/")
    return int(out[0]), int(out[1]), float(num) / float(den)


def read(path: str, w: int, h: int) -> np.ndarray:
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-pix_fmt", "rgb24", "-f", "rawvideo", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3)


def track(frames: np.ndarray) -> np.ndarray:
    """Per frame: red-strip x, top y and bottom y of Tom's UPPER screen (NaN where not measurable).

    The upper screen is the size reference: it is evenly lit and no content crosses it, while the red
    strip's lower part goes dim in some frames and the lower screen is hidden by the falcon and the sand.
    """
    n, h, w = frames.shape[:3]
    out = np.full((n, 3), np.nan)
    for i, fr in enumerate(frames):
        f = fr.astype(np.int16)
        red = (f[..., 0] > 120) & (f[..., 1] < 75) & (f[..., 2] < 85)
        if red.sum() < 0.00012 * red.size:
            continue
        ys, xs = np.where(red)
        x = float(np.median(xs))
        keep = np.abs(xs - x) < 0.02 * w
        if keep.sum() < 30:
            continue
        x = float(np.median(xs[keep]))
        band = f[:, max(0, int(x - 0.035 * w)): max(1, int(x - 0.008 * w))].max(2).astype(np.float32)  # just left of the strip
        r = np.sort(band, 1)[:, -max(3, band.shape[1] // 3):].mean(1)
        lit = r > 0.55 * np.percentile(r, 99)
        runs, start = [], None
        for y in range(h):
            if lit[y] and start is None:
                start = y
            if (not lit[y] or y == h - 1) and start is not None:
                runs.append((start, y))
                start = None
        runs = [q for q in runs if q[1] - q[0] > 0.05 * h]
        if not runs:
            continue
        top, bottom = runs[0]
        if bottom - top > 0.45 * h:
            bottom = top + (bottom - top) * 0.506          # both screens read as one run: the upper one is 50.6 % of it
        elif len(runs) == 1 and bottom - top < 0.22 * h:
            continue                                        # partly hidden (dune wipe): not a size measurement
        elif len(runs) == 1 and bottom - top > 0.34 * h:
            continue                                        # merged but cut off: not a size measurement
        out[i] = (x, top, bottom)
    return out


def smooth(tr: np.ndarray, fps: float) -> np.ndarray:
    """Median filter, then a moving average (about 0.5 s), gaps filled by interpolation."""
    idx = np.arange(len(tr))
    ok = ~np.isnan(tr[:, 0])
    out = np.empty_like(tr)
    k = max(3, int(fps * 0.5) | 1)
    for c in range(3):
        v = np.interp(idx, idx[ok], tr[ok, c])
        med = np.array([np.median(v[max(0, i - 3): i + 4]) for i in idx])
        pad = np.pad(med, k // 2, mode="edge")
        out[:, c] = np.convolve(pad, np.ones(k) / k, mode="valid")
    return out


def dune_mask(w: int, h: int, p: float) -> Image.Image:
    """Black dune sliding in from the left: p = 0 nothing, p = 1 the whole frame is covered."""
    m = Image.new("L", (w, h), 0)
    if p > 0:
        cx = -1.3 * w + p * 2.5 * w
        ImageDraw.Draw(m).ellipse((cx - 1.6 * w, -0.35 * h, cx + 1.25 * w, 2.4 * h), fill=255)
        m = m.filter(ImageFilter.GaussianBlur(w * 0.004))
    return m


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 1
    src, dst = sys.argv[1], sys.argv[2]
    max_scale, wipe_s = _arg("--max-scale", 1.35), _arg("--wipe", 0.8)
    w, h, fps = probe(src)
    frames = read(src, w, h)
    raw = track(frames)
    ok = np.where(~np.isnan(raw[:, 0]))[0]
    first, last = int(ok[0]), int(ok[-1])
    tr = smooth(raw, fps)
    height = tr[:, 2] - tr[:, 1]
    steady = height[first + int(fps * 0.3): last - int(fps * 0.3)]
    target_h = float(np.percentile(steady, 90))               # lock to the closest (largest) steady size: only zoom in
    mid = (first + last) // 2
    target_x = float(np.median(tr[first:mid, 0]))
    target_top = float(np.median(tr[first:mid, 1]))
    scale = target_h / height
    # end of the usable part: last frame where the correction stays sharp enough
    usable = [i for i in range(first, last + 1) if scale[i] <= max_scale]
    end = usable[-1]
    for i in range(usable[0], usable[-1]):                    # stop at the first break after the middle
        if i > mid and scale[i + 1] > max_scale:
            end = i
            break
    wipe_n = int(round(wipe_s * fps))
    print(f"{w}x{h} @ {fps:.0f} fps, {len(frames)} frames; strip tracked {first / fps:.2f}-{last / fps:.2f} s")
    print(f"lock: upper screen {target_h / h * 100:.1f} % of frame height, x {target_x / w * 100:.1f} %, top y {target_top / h * 100:.1f} %")
    print(f"needed zoom: min {scale[first:end + 1].min():.3f}, max {scale[first:end + 1].max():.3f}; "
          f"cut at {end / fps:.2f} s (zoom would pass {max_scale}), dune wipe over the last {wipe_s:.1f} s")

    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}",
                            "-r", f"{fps}", "-i", "-", "-an", "-c:v", "libx264", "-crf", "15", "-preset", "medium",
                            "-pix_fmt", "yuv420p", dst], stdin=subprocess.PIPE)
    black = Image.new("RGB", (w, h), (0, 0, 0))
    for i in range(0, end + 1):
        j = min(max(i, first), last)                           # before/after tracking: hold the nearest correction
        s = float(np.clip(scale[j], 0.5, max_scale))
        ax, ay = tr[j, 0], tr[j, 1]                            # anchor = top of the upper screen at the strip
        # output pixel (X, Y) samples source ((X - target_x) / s + ax, (Y - target_top) / s + ay);
        # the source is edge-extended by PAD px so a shifted frame never shows a black border
        coef = (1 / s, 0, ax - target_x / s + PAD, 0, 1 / s, ay - target_top / s + PAD)
        padded = np.pad(frames[i], ((PAD, PAD), (PAD, PAD), (0, 0)), mode="edge")
        im = Image.fromarray(padded).transform((w, h), Image.AFFINE, coef, resample=Image.BICUBIC)
        left = end - i
        if left < wipe_n:
            p = 1 - left / wipe_n
            im = Image.composite(black, im, dune_mask(w, h, p * p * (3 - 2 * p)))
        enc.stdin.write(im.tobytes())
    enc.stdin.close()
    enc.wait()

    check = track(read(dst, w, h))
    print("  t      before: x%  upper-screen%   |   after: x%  upper-screen%")
    for i in range(first, end + 1, max(1, int(fps * 0.5))):
        b = raw[i]
        a = check[i] if i < len(check) else (np.nan,) * 3
        fmt = lambda v: "   -  " if np.isnan(v[0]) else f"{v[0] / w * 100:5.1f}  {(v[2] - v[1]) / h * 100:5.1f}"
        print(f"  {i / fps:4.2f}        {fmt(b)}      |        {fmt(a)}")
    print(f"-> {dst} ({(end + 1) / fps:.2f} s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
