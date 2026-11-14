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
    out = np.full((n, 4), np.nan)
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
        merged = bottom - top > 0.45 * h
        if not merged and len(runs) == 1 and not (0.22 * h <= bottom - top <= 0.34 * h):
            continue                                        # partly hidden or cut off: not a size measurement
        # Size = top edge of the upper screen -> centre of the dark divider between the two screens.
        # Both are found from the brightness profile itself (edge gradient / local minimum), to a fraction of
        # a pixel, so the result does not depend on a threshold that moves when the falcon or the sand flare up.
        g = np.diff(r[max(0, top - 7): top + 8])
        g = np.clip(g, 0, None)
        if g.sum() <= 0:
            continue
        top_sub = max(0, top - 7) + float((np.arange(len(g)) * g).sum() / g.sum()) + 0.5
        if merged:
            lo, hi = int(top + (bottom - top) * 0.40), int(top + (bottom - top) * 0.62)
        else:
            nxt = runs[1][0] if len(runs) > 1 else bottom + 8
            lo, hi = bottom - 6, min(h - 2, nxt + 6)
        seg = r[lo:hi]
        if len(seg) < 3:
            continue
        m = int(np.argmin(seg))
        div = lo + float(m)
        if 0 < m < len(seg) - 1:                             # parabola through the minimum: sub-pixel divider centre
            y0, y1, y2 = seg[m - 1], seg[m], seg[m + 1]
            den = y0 - 2 * y1 + y2
            if den > 1e-6:
                div += 0.5 * (y0 - y2) / den
        if not (0.2 * h < div - top_sub < 0.36 * h):
            continue
        # bottom edge of the LOWER screen: strongest falling edge below the divider (NaN-able: content covers it later)
        lo2, hi2 = int(div + 0.15 * h), min(h - 2, int(div + 0.42 * h))
        bot = np.nan
        if hi2 - lo2 > 8:
            fall = np.clip(-np.diff(r[lo2:hi2]), 0, None)
            kk = int(np.argmax(fall))
            a0 = max(0, kk - 5)
            seg2 = fall[a0: kk + 6]
            if seg2.sum() > 0:
                bot = lo2 + a0 + float((np.arange(len(seg2)) * seg2).sum() / seg2.sum()) + 0.5
        out[i] = (x, top_sub, div, bot)
    return out


def smooth(tr: np.ndarray, fps: float) -> np.ndarray:
    """Turn the per-frame track into a smooth correction (columns: x, top, top + size).

    Size ruler: the full screen stack (top of the upper screen -> bottom of the lower screen) while the lower
    screen is clean; once content covers it (falcon, sand), the upper screen (top -> divider) times the ratio
    measured just before. The divider alone is a poor ruler early on: its reading shifts as it comes into
    focus, which made an earlier version breathe in and out.
    Smoothing: a Gaussian of about 0.25 s, enough to drop measuring jitter and still follow real camera moves.
    """
    n = len(tr)
    idx = np.arange(n, dtype=float)
    ok = ~np.isnan(tr[:, 0])
    first, last = int(np.where(ok)[0][0]), int(np.where(ok)[0][-1])
    x = np.interp(idx, idx[ok], tr[ok, 0])
    top = np.interp(idx, idx[ok], tr[ok, 1])
    upper = np.interp(idx, idx[ok], tr[ok, 2] - tr[ok, 1])
    total = tr[:, 3] - tr[:, 1]

    # the stack is trusted until it first jumps (content reached the lower screen's bottom edge)
    med5 = lambda v, i: float(np.nanmedian(v[max(first, i - 5): i + 1]))
    switch = last + 1
    for i in range(first + 6, last + 1):
        ref = med5(total, i - 1)
        if np.isnan(total[i]) or abs(total[i] / ref - 1) > 0.02:
            if all(np.isnan(total[j]) or abs(total[j] / ref - 1) > 0.02 for j in range(i, min(last, i + 3) + 1)):
                switch = i
                break
    win = slice(max(first, switch - int(fps * 0.6)), switch)
    ratio = float(np.nanmedian(total[win] / upper[win]))
    size = np.where(idx < switch, total, upper * ratio)
    good = ~np.isnan(size) & ok
    size = np.interp(idx, idx[good], size[good])

    # The first half second after the product appears is still partly hidden by the dune wipe, so its
    # readings are unreliable: replace them with a straight-line projection from the 1.5 s that follow.
    t0, t1 = first + int(fps * 0.5), min(last, first + int(fps * 2.0))
    if t1 - t0 > 6:
        for v in (size, top):
            c = np.polyfit(idx[t0:t1], v[t0:t1], 1)
            v[:t0] = np.polyval(c, idx[:t0])

    def gauss(v: np.ndarray, sigma: float) -> np.ndarray:
        v = np.array([np.median(v[max(0, i - 2): i + 3]) for i in range(n)])
        r = int(3 * sigma)
        k = np.exp(-0.5 * (np.arange(-r, r + 1) / sigma) ** 2)
        return np.convolve(np.pad(v, r, mode="edge"), k / k.sum(), mode="valid")

    sigma = fps * 0.25
    x, top, size = gauss(x, sigma), gauss(top, sigma), gauss(size, sigma)
    out = np.stack([x, top, top + size], 1)
    out[:first] = out[first]
    out[last + 1:] = out[last]
    steady = float(np.median(size[first + (last - first) // 10: first + (last - first) * 6 // 10]))
    onset = last + 1
    for i in range(first + (last - first) // 2, last - 2):
        if all(size[i + k2] / steady < 0.93 for k2 in range(3)):
            onset = i
            break
    smooth.onset, smooth.switch, smooth.ratio = onset, switch, ratio
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
    onset = min(getattr(smooth, "onset", last + 1), last + 1)
    target_h = float(height[first:onset].max())               # lock to the closest steady size: only ever zoom in
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
    print(f"lock: screen stack {target_h / h * 100:.1f} % of frame height, x {target_x / w * 100:.1f} %, top y {target_top / h * 100:.1f} %")
    print(f"size ruler: full screen stack until {smooth.switch / fps:.2f} s, then upper screen x {smooth.ratio:.3f}")
    print(f"pull-back starts at about {onset / fps:.2f} s" if onset <= last else "no pull-back found")
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

    after = smooth(track(read(dst, w, h)), fps)
    before_h, after_h = height, after[:, 2] - after[:, 1]
    print("  t      before: x%  screens%   |   after: x%  screens%")
    for i in range(first, min(end, len(after) - 1) - int(wipe_s * fps) + 1, max(1, int(fps * 0.5))):
        print(f"  {i / fps:4.2f}        {tr[i, 0] / w * 100:5.1f}  {before_h[i] / h * 100:5.2f}      |        "
              f"{after[i, 0] / w * 100:5.1f}  {after_h[i] / h * 100:5.2f}")
    a0, b0 = first + int(fps * 0.3), min(end, len(after) - 1) - int(wipe_s * fps)
    print(f"size spread {before_h[a0:b0].min() / h * 100:.2f}-{before_h[a0:b0].max() / h * 100:.2f} % before, "
          f"{after_h[a0:b0].min() / h * 100:.2f}-{after_h[a0:b0].max() / h * 100:.2f} % after")
    print(f"-> {dst} ({(end + 1) / fps:.2f} s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
