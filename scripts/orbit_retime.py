"""Hero orbit: retime a Kling clip so the camera orbit runs at ONE constant speed (no credits).

Kling reaches a detailed end frame early and then holds, so a clip that should orbit for 4 s
turns for about 3 s and stands almost still for the rest. Wassim (14 Nov 2026): the rotation
must keep the same speed while the content comes out, in every shot.

Method: track the product's lit screen in each frame (left edge x = orbit progress, it moves
monotonically across the frame as the camera travels), then re-sample the frames so progress
is linear in time. Slow stretches (ease-in, settle/hold) are compressed by dropping frames;
nothing is slowed down or interpolated. Frames before the product is visible are kept 1:1.

Usage:
  python scripts/orbit_retime.py <clip.mp4> <out.mp4> [--band 0.28,0.46] [--thr 90] [--speed PX_PER_S]
    --band   vertical band (fractions of the height) where the screen is lit but no content crosses it
    --speed  target orbit speed in px/s at 960 px width; default = this clip's own median speed
Prints the measured speed curve, the chosen speed and the new duration.
"""
from __future__ import annotations

import subprocess
import sys

import numpy as np

W, H, FPS = 960, 540, 24


def _arg(flag: str, default: str) -> str:
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else default


def read_gray(path: str, w: int = W, h: int = H) -> np.ndarray:
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vf", f"scale={w}:{h},format=gray",
                          "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, h, w).astype(np.float32)


def progress(gray: np.ndarray, band: tuple[float, float], thr: float) -> np.ndarray:
    """Left edge (px) of the lit screen per frame; NaN while it is not visible."""
    y0, y1 = int(band[0] * gray.shape[1]), int(band[1] * gray.shape[1])
    p = np.full(len(gray), np.nan, np.float32)
    for i, fr in enumerate(gray):
        xs = np.where(fr[y0:y1].mean(0) > thr)[0]
        if len(xs):
            p[i] = xs.min()
    return p


def smooth(p: np.ndarray, k: int = 5) -> np.ndarray:
    out = p.copy()
    ok = ~np.isnan(p)
    idx = np.where(ok)[0]
    for i in idx:
        win = p[max(0, i - k // 2): i + k // 2 + 1]
        out[i] = np.nanmedian(win)
    # enforce monotonic travel (tracking jitter must not run the orbit backwards)
    out[idx] = np.maximum.accumulate(out[idx])
    return out


def plan(p: np.ndarray, speed: float | None) -> tuple[list[int], float, int, int]:
    """Return source frame indices for the constant-speed output, the speed (px/s), first and last tracked frame."""
    idx = np.where(~np.isnan(p))[0]
    first, last = int(idx[0]), int(idx[-1])
    d = np.diff(p[first:last + 1]) * FPS                    # px/s per frame step
    moving = d[d > np.percentile(d, 40)]                    # ignore the ease-in / hold when picking the speed
    v = float(speed or np.median(moving))
    frames = list(range(first))                             # reveal before the product is visible: 1:1
    target, end = float(p[first]), float(p[last])
    src = first
    while target <= end + 1e-6 and src <= last:
        while src < last and p[src] < target:               # first frame that has reached the target progress
            src += 1
        frames.append(src)
        if src >= last:
            break
        target += v / FPS
    return frames, v, first, last


def write(path: str, out: str, frames: list[int]) -> None:
    sel = "+".join(f"eq(n\\,{i})" for i in sorted(set(frames)))
    # select keeps each needed source frame once; repeats are not needed because we only ever drop frames
    order = sorted(set(frames))
    assert order == [f for i, f in enumerate(frames) if i == 0 or f != frames[i - 1]], "plan must be monotonic"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", path, "-an", "-vf", f"select='{sel}',setpts=N/{FPS}/TB",
                    "-r", str(FPS), "-c:v", "libx264", "-crf", "14", "-preset", "medium", "-pix_fmt", "yuv420p", out],
                   check=True)


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 1
    src, out = sys.argv[1], sys.argv[2]
    band = tuple(float(x) for x in _arg("--band", "0.28,0.46").split(","))
    thr = float(_arg("--thr", "90"))
    speed = float(_arg("--speed", "0")) or None
    gray = read_gray(src)
    p = smooth(progress(gray, band, thr))
    frames, v, first, last = plan(p, speed)
    frames = [f for i, f in enumerate(frames) if i == 0 or f != frames[i - 1]]
    d = np.diff(p[first:last + 1]) * FPS
    print(f"source: {len(gray)} frames ({len(gray) / FPS:.2f} s); product tracked from frame {first} to {last}")
    for s in range(0, len(d), 12):
        print(f"  {(first + s) / FPS:4.2f}-{(first + s + 12) / FPS:4.2f} s  orbit speed {d[s:s + 12].mean():6.1f} px/s")
    print(f"target speed {v:.1f} px/s -> {len(frames)} frames ({len(frames) / FPS:.2f} s), "
          f"{len(gray) - len(frames)} slow frames dropped")
    write(src, out, frames)
    q = smooth(progress(read_gray(out), band, thr))
    qi = np.where(~np.isnan(q))[0]
    dq = np.diff(q[qi[0]:qi[-1] + 1]) * FPS
    half = len(dq) // 2
    print(f"result: first half {dq[:half].mean():.1f} px/s, second half {dq[half:].mean():.1f} px/s -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
