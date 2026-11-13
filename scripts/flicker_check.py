"""Check a Tom clip frame by frame (native 24 fps) for luminance flicker on the plinth and body.

Tom is located in every frame by his red side strip (a tall, thin vertical run of red pixels).
Two regions are measured relative to the strip, so they follow the camera move:
  plinth: the dark base below the screens (lower right part of Tom)
  body  : the black side/bezel band just left of the strip, over the screen height
For each region the mean luminance (0-255) is compared with a rolling median over +/- 6 frames.
A frame is flagged when it deviates by more than THRESH levels.

Usage: python scripts/flicker_check.py <clip.mp4> [more clips...]
Writes <clip>_flicker.csv next to each clip and prints the flagged frame numbers (0-based) and times.
"""
from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path

import numpy as np

THRESH = 3.0   # luminance levels (of 255) away from the local median: mild flicker
STRONG = 8.0   # clearly visible flicker (validated against Wassim's frame-by-frame notes on the drafts)
WIN = 6        # frames each side for the rolling median


def read_frames(clip: Path):
    probe = subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                     "stream=width,height,r_frame_rate", "-of", "csv=p=0", str(clip)]).decode().strip().split(",")
    w, h = int(probe[0]), int(probe[1])
    num, den = probe[2].split("/")
    fps = float(num) / float(den)
    proc = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(clip), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                            stdout=subprocess.PIPE)
    size = w * h * 3
    while True:
        buf = proc.stdout.read(size)
        if len(buf) < size:
            break
        yield np.frombuffer(buf, np.uint8).reshape(h, w, 3), fps
    proc.wait()


def strip_box(rgb: np.ndarray):
    """Bounding box of the red side strip: columns where red runs over a long vertical extent."""
    r, g, b = (rgb[..., i].astype(np.int16) for i in range(3))
    red = (r - g > 60) & (r - b > 40) & (r > 120)
    counts = red.sum(axis=0)
    h = rgb.shape[0]
    cols = np.where(counts > 0.18 * h)[0]
    if len(cols) == 0:
        return None
    # keep the strongest contiguous run of columns
    best = cols[np.argmax(counts[cols])]
    run = cols[np.abs(cols - best) <= 12]
    rows = np.where(red[:, run.min():run.max() + 1].any(axis=1))[0]
    return int(run.min()), int(run.max()), int(rows.min()), int(rows.max())


def measure(rgb: np.ndarray, box) -> tuple[float, float]:
    x0, x1, y0, y1 = box
    hgt = y1 - y0
    w_tom = hgt / 3.5
    lum = rgb.astype(np.float32).mean(axis=2)
    H, W = lum.shape

    def region(xa, xb, ya, yb):
        xa, xb = int(max(0, xa)), int(min(W, xb))
        ya, yb = int(max(0, ya)), int(min(H, yb))
        return float(lum[ya:yb, xa:xb].mean()) if xb > xa and yb > ya else float("nan")

    plinth = region(x0 - 0.45 * w_tom, x0 - 0.10 * w_tom, y1 - 0.10 * hgt, y1 - 0.02 * hgt)
    body = region(x0 - 0.035 * w_tom - 2, x0 - 2, y0 + 0.10 * hgt, y0 + 0.75 * hgt)
    if x1 - x0 < 4 or 0.035 * w_tom < 8:
        # Tom is too small in frame: the band is only a few pixels wide and sits against the lit
        # screen edge, so a 1 px tracking jitter reads as a luminance jump. Not measurable.
        body = float("nan")
    return plinth, body


def rolling_dev(v: np.ndarray) -> np.ndarray:
    out = np.zeros_like(v)
    for i in range(len(v)):
        seg = v[max(0, i - WIN):i + WIN + 1]
        out[i] = v[i] - np.nanmedian(seg)
    return out


def check(clip: Path) -> None:
    rows, fps = [], 24.0
    for i, (frame, fps) in enumerate(read_frames(clip)):
        box = strip_box(frame)
        # reject a box whose bottom jumps by more than 5% of the frame height from the last good one
        # (the strip was only partly detected in this frame)
        good = [r[3] for r in rows if r[3]]
        if box and good and abs(box[3] - good[-1][3]) > 0.05 * frame.shape[0]:
            box = None
        p, b = measure(frame, box) if box else (float("nan"), float("nan"))
        rows.append((i, p, b, box))
    p = np.array([r[1] for r in rows]); b = np.array([r[2] for r in rows])
    dp, db = rolling_dev(p), rolling_dev(b)
    out = clip.with_name(clip.stem + "_flicker.csv")
    with open(out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["frame", "time_s", "plinth_lum", "plinth_dev", "body_lum", "body_dev", "strip_found"])
        for (i, pv, bv, box), a, c in zip(rows, dp, db):
            w.writerow([i, round(i / fps, 3), round(pv, 2), round(float(a), 2), round(bv, 2), round(float(c), 2), bool(box)])
    lost = [r[0] for r in rows if not r[3]]
    print(f"\n{clip.name}: {len(rows)} frames at {fps:g} fps")
    for name, v, d in (("plinth", p, dp), ("body", b, db)):
        if np.isnan(v).mean() > 0.5:
            print(f"  {name:6}: not measurable in this clip (Tom too small in frame); check by eye")
            continue
        strong = [i for i in range(len(d)) if abs(d[i]) > STRONG]
        mild = [i for i in range(len(d)) if THRESH < abs(d[i]) <= STRONG]
        print(f"  {name:6}: luminance {np.nanmin(v):.1f}-{np.nanmax(v):.1f} (median {np.nanmedian(v):.1f}); "
              f"max deviation {np.nanmax(np.abs(d)):.1f}")
        print(f"          strong (> {STRONG:g}): "
              + (", ".join(f"{i} ({i / fps:.2f}s, {d[i]:+.1f})" for i in strong) if strong else "none"))
        print(f"          mild ({THRESH:g}-{STRONG:g}): {len(mild)} frames"
              + (": " + ", ".join(str(i) for i in mild) if mild else ""))
    if lost:
        print(f"  strip not found in frames: {lost[0]}-{lost[-1]} ({len(lost)} frames), not measured")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    for a in sys.argv[1:]:
        check(Path(a))
