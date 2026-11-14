"""Hero v5: end a scene earlier with a code-drawn dune wipe (no credits, original untouched).

Wassim, 14 Nov 2026: the camera flickers in the last ~2 s of the perfume scene, so the black cut should come
2 s earlier, before the flicker. The clip's own closing dune is a straight dark edge (about 45 degrees, top-left
to bottom-right) sliding in from the left over ~13 frames; this draws the same kind of edge at an earlier frame,
then holds the clip's own black for the same tail it had before, and cuts the scene there.

Works on the raw YUV planes (no RGB round trip), blending to the clip's own measured black.

Usage:
  python scripts/orbit_endwipe.py <in.mp4> <out.mp4> --start 118 [--frames 13] [--tail 14] [--slope 1.0]
    --start   first frame of the wipe        --frames  wipe length in frames (edge enters -> frame fully black)
    --tail    black frames kept after it     --slope   horizontal run of the edge per pixel of height
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

W, H, FPS = 1280, 720, 24
YS, CS = W * H, (W // 2) * (H // 2)


def arg(name: str, default: float) -> float:
    return float(sys.argv[sys.argv.index(name) + 1]) if name in sys.argv else default


def read_yuv(video: Path) -> np.ndarray:
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(video), "-f", "rawvideo", "-pix_fmt", "yuv420p", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, YS + 2 * CS).copy()


def mask(p: float, w: int, h: int, slope: float, soft: float) -> np.ndarray:
    """1 = black. A straight edge x = x0 + slope*y; black on its left; p: 0 -> edge off-screen left, 1 -> covered."""
    x0 = -slope * h - soft + p * (w + slope * h + 2 * soft)
    yy, xx = np.mgrid[0:h, 0:w]
    d = (x0 + slope * yy) - xx                      # > 0 left of the edge
    return np.clip(0.5 + d / (2 * soft), 0, 1)


def main() -> int:
    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    start, n, tail = int(arg("--start", 118)), int(arg("--frames", 13)), int(arg("--tail", 14))
    slope = arg("--slope", 1.0)
    v = read_yuv(src)
    black = v[-6:].astype(float).mean(0)            # the clip's own black (its last frames are fully black)
    by, bu, bv = black[:YS].mean(), black[YS:YS + CS].mean(), black[YS + CS:].mean()
    end = start + n + tail
    out = v[:end].astype(float)
    for i in range(start, end):
        p = min(1.0, (i - start + 1) / n)
        p = p * p * (3 - 2 * p)                      # ease in and out, like a camera passing a dune
        my = mask(p, W, H, slope, 3.0).ravel()
        mc = mask(p, W // 2, H // 2, slope, 1.5).ravel()
        f = out[i]
        f[:YS] = f[:YS] * (1 - my) + by * my
        f[YS:YS + CS] = f[YS:YS + CS] * (1 - mc) + bu * mc
        f[YS + CS:] = f[YS + CS:] * (1 - mc) + bv * mc
    out = np.clip(out + 0.5, 0, 255).astype(np.uint8)
    with tempfile.TemporaryDirectory() as tmp:
        raw = Path(tmp) / "all.yuv"
        raw.write_bytes(out.tobytes())
        dst.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "yuv420p", "-s", f"{W}x{H}",
                        "-framerate", str(FPS), "-i", str(raw), "-c:v", "libx264", "-crf", "12", "-preset", "slow",
                        "-pix_fmt", "yuv420p", str(dst)], check=True)
    print(f"{src.name}: wipe frames {start}-{start + n - 1} ({start / FPS:.2f}-{(start + n) / FPS:.2f} s), black "
          f"Y {by:.1f}, scene now {end} frames = {end / FPS:.3f} s -> {dst}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
