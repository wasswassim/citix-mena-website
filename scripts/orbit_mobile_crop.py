"""Hero v5 P4 Option A (free): 9:16 mobile loop cut from the 16:9 master with a slow, smoothed reframe.

A plain centre crop misses the glass panel (it sits right of centre), and panel + content are ~630 px wide
while a 9:16 window of the 720 px-high master is only ~405 px. So the window follows the content inside each
scene: per frame, the horizontal mass of non-black pixels (above the sand line) gives a centre; that path is
heavily smoothed (no jitter), speed-limited, and held still over the black parts so nothing pans in black.

Raw YUV in, no RGB round trip (see orbit_deflicker.py). Writes the 404x720 crop master + crop_path.npy.

Usage:
  python scripts/orbit_mobile_crop.py <master_16x9.mp4> <timing.json> <out_dir> [--bias 0.0]
    --bias  shift the window toward the panel (+) or the emerging content (-), in fractions of the window width
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

W, H, FPS = 1280, 720, 24
CW = 404                                   # 9:16 window on a 720 px-high frame (even width for yuv420p)
OW, OH = 720, 1280                         # output (phone) size; the crop is cut at this resolution
YS, CS = W * H, (W // 2) * (H // 2)
SMOOTH_S = 0.9                             # gaussian sigma of the path, seconds
MAX_PX_PER_FRAME = 4.0                     # pan speed limit (~96 px/s on the master)


def read_yuv(video: Path) -> np.ndarray:
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(video), "-f", "rawvideo", "-pix_fmt", "yuv420p", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, YS + 2 * CS)


def centres(v: np.ndarray) -> np.ndarray:
    out = np.full(len(v), np.nan)
    for i, f in enumerate(v):
        y = f[:YS].reshape(H, W)[60:560].astype(float)
        wgt = np.clip(y - 30, 0, None).sum(0)            # content above video black, sand foreground excluded
        if wgt.sum() > 2e4:
            c = np.cumsum(wgt) / wgt.sum()
            out[i] = (np.searchsorted(c, 0.08) + np.searchsorted(c, 0.92)) / 2
    return out


def smooth_scene(c: np.ndarray) -> np.ndarray:
    idx = np.arange(len(c))
    ok = ~np.isnan(c)
    if not ok.any():
        return np.full(len(c), W / 2)
    c = np.interp(idx, idx[ok], c[ok])                   # hold first/last real value over the black parts
    s = SMOOTH_S * FPS
    k = np.exp(-0.5 * (np.arange(-3 * s, 3 * s + 1) / s) ** 2)
    k /= k.sum()
    pad = len(k) // 2
    c = np.convolve(np.pad(c, pad, mode="edge"), k, mode="valid")[: len(idx)]
    for i in range(1, len(c)):                           # speed limit, forward then backward
        c[i] = np.clip(c[i], c[i - 1] - MAX_PX_PER_FRAME, c[i - 1] + MAX_PX_PER_FRAME)
    for i in range(len(c) - 2, -1, -1):
        c[i] = np.clip(c[i], c[i + 1] - MAX_PX_PER_FRAME, c[i + 1] + MAX_PX_PER_FRAME)
    return np.clip(c, CW / 2, W - CW / 2)


# Hand-placed window centres (scene seconds -> master x), eased between keys. The automatic centring above is
# pulled off the panel by the lit sand, so these are used for every scene; it stays as a fallback.
KEYS: dict[str, list[tuple[float, float]]] = {
    "oasis":   [(0.0, 880), (8.0, 880)],          # static: a 40 px drift only read as stutter
    "perfume": [(0.0, 890), (6.0, 890)],          # static
    "camel":   [(0.0, 880), (0.9, 880), (4.8, 630), (6.0, 630)],   # one long glide
    "suv":     [(0.0, 890), (1.5, 890), (5.0, 780), (8.0, 780)],
}


def keyed(keys: list[tuple[float, float]], n: int) -> np.ndarray:
    out = np.empty(n)
    for i in range(n):
        s = i / FPS
        for (t0, x0), (t1, x1) in zip(keys, keys[1:]):
            if s <= t1 or (t1, x1) == keys[-1]:
                p = min(1.0, max(0.0, (s - t0) / (t1 - t0)))
                out[i] = x0 + (x1 - x0) * p * p * (3 - 2 * p)
                break
    return np.clip(out, CW / 2, W - CW / 2)


def main(argv: list[str]) -> int:
    src, timing, out_dir = Path(argv[0]), Path(argv[1]), Path(argv[2])
    bias = float(argv[argv.index("--bias") + 1]) if "--bias" in argv else 0.0
    t = json.loads(timing.read_text())
    v = read_yuv(src)
    raw_c = None if KEYS else centres(v) + bias * CW
    path = np.zeros(len(v))
    report = []
    for sc in t["scenes"]:
        a, b = round(sc["start"] * FPS), round(sc["end"] * FPS)
        if sc["name"] in KEYS:
            path[a:b] = keyed(KEYS[sc["name"]], b - a)
        else:
            path[a:b] = smooth_scene(raw_c[a:b])
        report.append(f"{sc['name']}: window x {int(path[a:b].min() - CW / 2)}-{int(path[a:b].max() + CW / 2)}")
    # Crop at OUTPUT resolution: the whole frame is first scaled to 1280 px high (lanczos, yuv444p so any x works),
    # then a 720 px window is cut, so the pan moves in 1 phone-pixel steps. (v1 cut 2 source px steps = 3.6 phone px
    # with up to 18 still frames between them: a visible stutter.)
    del v
    sc_ = OH / H
    bw = int(round(W * sc_ / 2)) * 2                      # 2276
    xs = np.clip(np.round(path * sc_ - OW / 2).astype(int), 0, bw - OW)
    out_dir.mkdir(parents=True, exist_ok=True)
    master = out_dir / "orbit_master_9x16.mp4"
    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(src), "-vf", f"scale={bw}:{OH}:flags=lanczos",
                            "-f", "rawvideo", "-pix_fmt", "yuv444p", "-"], stdout=subprocess.PIPE)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "yuv444p", "-s",
                            f"{OW}x{OH}", "-framerate", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "12",
                            "-preset", "slow", "-pix_fmt", "yuv420p", str(master)], stdin=subprocess.PIPE)
    fs = bw * OH * 3
    for i in range(len(path)):
        buf = dec.stdout.read(fs)
        f = np.frombuffer(buf, np.uint8).reshape(3, OH, bw)
        enc.stdin.write(np.ascontiguousarray(f[:, :, xs[i]:xs[i] + OW]).tobytes())
    enc.stdin.close()
    dec.wait()
    enc.wait()
    steps = np.abs(np.diff(xs))
    print(f"pan steps (phone px per frame): max {steps.max()}, frames moving {int((steps > 0).sum())}")
    np.save(out_dir / "crop_path.npy", path)
    print("\n".join(report))
    print(f"-> {master}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
