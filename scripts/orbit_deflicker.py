"""Hero v5: remove the camera hitches ("flicker") from raw Seedance clips (no credits, originals untouched).

What it fixes (measured 14 Nov 2026):
  1. Seedance pads ~23 fps to 24 fps by repeating one frame per second (frames 35, 59, 83, 107, 131, 155 of
     every 8 s clip). The orbit freezes for one frame, then catches up: a visible hitch. The repeated frame is
     rebuilt as the motion-interpolated midpoint of its neighbours (ffmpeg minterpolate, motion-compensated).
  2. Optional frame ranges with a sudden camera jump (--jump a-b): those frames are rebuilt by interpolating
     between the good frames on either side, so the jump is spread over the range.

Everything is done on the raw YUV planes, never through RGB: the Seedance files keep very dark values below
video black (about half the pixels), and an RGB round trip shifts them and darkens the picture. Untouched
frames therefore keep their exact pixel values before the final encode.

Usage:
  python scripts/orbit_deflicker.py <in.mp4> <out.mp4> [--jump 162-166]
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

W, H, FPS = 1280, 720, 24
FRAME = W * H * 3 // 2                                  # yuv420p bytes per frame


def read_yuv(video: Path) -> np.ndarray:
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(video), "-f", "rawvideo", "-pix_fmt", "yuv420p", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, FRAME).copy()


def luma(fr: np.ndarray) -> np.ndarray:
    return fr[: W * H].reshape(H, W)[::4, ::4].astype(float)


def repeats(v: np.ndarray) -> list[int]:
    L = [luma(f) for f in v]
    m = np.array([x.mean() for x in L])
    d = np.array([np.abs(L[i] - L[i - 1]).mean() for i in range(1, len(L))])
    live = [i for i in range(1, len(L)) if m[i] > 20]       # 16 = video black
    # a repeat = far less change than the frames around it (local median, so fades and fast action don't hide it)
    return [i for i in live if d[i - 1] < 0.4 * np.median(d[max(0, i - 7): i + 6])]


def rebuild(v: np.ndarray, bad: list[int], work: Path) -> None:
    """Replace consecutive bad frames [k..k+n-1] by motion interpolation between k-1 and k+n."""
    groups, cur = [], []
    for i in sorted(set(bad)):
        if cur and i != cur[-1] + 1:
            groups.append(cur)
            cur = []
        cur.append(i)
    if cur:
        groups.append(cur)
    for g in groups:
        g0, g1, n = g[0] - 1, g[-1] + 1, len(g)
        if g0 < 1 or g1 > len(v) - 2:
            continue
        src = work / "in.yuv"
        src.write_bytes(b"".join(v[k].tobytes() for k in (g0 - 1, g0, g1, g1 + 1)))   # at t = 0, 1, 2, 3
        out = subprocess.run(["ffmpeg", "-v", "error", "-f", "rawvideo", "-pix_fmt", "yuv420p", "-s", f"{W}x{H}",
                              "-framerate", "1", "-i", str(src), "-vf",
                              f"minterpolate=fps={n + 1}:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1",
                              "-f", "rawvideo", "-pix_fmt", "yuv420p", "-"], capture_output=True, check=True).stdout
        o = np.frombuffer(out, np.uint8).reshape(-1, FRAME)
        for j, k in enumerate(g):                              # output index (n+1)*t: t = 1 + (j+1)/(n+1)
            v[k] = o[(n + 1) + j + 1]


def main(argv: list[str]) -> int:
    src, dst = Path(argv[0]), Path(argv[1])
    jump = []
    if "--jump" in argv:
        a, b = map(int, argv[argv.index("--jump") + 1].split("-"))
        jump = list(range(a, b + 1))
    v = read_yuv(src)
    orig = v.copy()
    rep = repeats(v)
    with tempfile.TemporaryDirectory() as tmp:
        rebuild(v, rep + jump, Path(tmp))
        raw = Path(tmp) / "all.yuv"
        raw.write_bytes(v.tobytes())
        dst.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "yuv420p", "-s", f"{W}x{H}",
                        "-framerate", str(FPS), "-i", str(raw), "-c:v", "libx264", "-crf", "12", "-preset", "slow",
                        "-pix_fmt", "yuv420p", str(dst)], check=True)
    changed = [i for i in range(len(v)) if not np.array_equal(v[i], orig[i])]
    print(f"{src.name}: repeated frames {rep}; jump frames {jump or 'none'}; frames rebuilt {changed}; -> {dst}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
