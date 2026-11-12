"""Prompt 1, round 3: regenerate s5_start only (approved by Wassim 2026-11-12, $0.33).

Main reference = the corrected night cut-out of the chosen hero Tom (front view, 1 : 3.5 overall),
second reference = ref 02 (real Tom at night, for the red side strip and materials).

Usage:
  python scripts/prompt1_s5_regen.py quote
  python scripts/prompt1_s5_regen.py run --yes
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import higgsfield as hf  # noqa: E402
import prompt1_drafts as pd  # noqa: E402

pd.OUT = hf.ROOT / "media" / "generated" / "drafts" / "round3_s5_start"
pd.STATE = pd.OUT / "jobs.json"
pd.BUDGET_USD = 0.35

MAIN_REF = hf.ROOT / "media" / "generated" / "hero_cutout" / "tom_night_ref.png"
NIGHT_REF = hf.ROOT / "media" / "source" / "02_tom_night_photo.jpg"

TOM = (
    "PRODUCT — reference image 1 is the exact object to reproduce, seen straight from the front: the "
    'CITIX "Tom" roadside smartboard. Copy its shape, proportions and parts precisely and do not redesign '
    "it: a tall, slim vertical totem, 7 m high from the ground to the top of the cap and 2 m wide "
    "(overall width to height 1 : 3.5), very thin flat profile, matte black metal body. The front face "
    "is almost entirely screen: two stacked portrait screens with small rounded corners that run nearly "
    "edge to edge, with extremely thin black bezels and only a thin black gap between them, the upper "
    "screen slightly shorter than the lower one. A small low plain black cap sits on the top edge, from "
    "the middle to the right edge, with one round camera lens at its right end and no text or logo. A "
    "plain matte black plinth, narrower than the body (about 60% of its width) and short (about one "
    "sixth of the body height), flush with the body's right edge, carries it. A single thin vertical red "
    "LED light strip runs along the right side edge from the cap down to the ground, as in reference "
    "image 2 (the real object at night). No other parts, text, logos or decoration. Ignore the screen "
    "content shown in reference image 2."
)

B = (
    f"Photorealistic cinematic photograph at night on a wide, quiet road in Sharjah, UAE. {TOM} It stands "
    "on the roadside, perfectly front-facing, looking straight at the camera, exactly centred "
    "horizontally. FRAMING Eye-level camera, long lens, vertical edges parallel. The horizon is low: the "
    "road, a few palm trees and low-rise modern buildings stay in the lower third of the frame, softly "
    "out of focus, with long white and red light trails from passing traffic behind the totem. "
    "Everything above the lower third is a clear, deep blue-black night sky with faint, sparse stars, "
    "with open empty sky above the totem's cap. Both screens are switched OFF: pure black glass with "
    "only faint reflections. The red side light strip is lit, visible as a thin red line along the "
    "totem's right edge. Soft, cool white street light defines the edges of the body. High contrast, "
    f"clean, neutral-cool white balance. {pd.AVOID}"
)
FRAMING = {
    "16:9": "The totem fills about 60% of the frame height: its base stands on the ground about 8% above "
            "the bottom edge, and the top 30% of the frame is empty sky.",
    "9:16": "Vertical composition: the totem fills about 55% of the frame height: its base stands on the "
            "ground about 8% above the bottom edge, and the top 35% of the frame is empty sky.",
}


def build() -> dict:
    refs = [hf.upload(MAIN_REF), hf.upload(NIGHT_REF)]
    return {f"s5_start_{pd.tag(ar)}_v{v}": {**pd.BASE, "aspect_ratio": ar, "image_urls": refs,
                                           "prompt": B.replace("FRAMING", FRAMING[ar])}
            for v in (1, 2) for ar in ("16:9", "9:16")}


def main(argv: list[str]) -> int:
    try:
        jobs = build()
        if argv and argv[0] == "run":
            state = pd.load()
            pd.run_stage(jobs, state, "--yes" in argv)
            print(f"{sum(1 for j in state.values() if j.get('file'))} files, spend ${pd.spent(state):.3f}")
        else:
            print(f"{len(jobs)} images, quote ${sum(hf.estimate(pd.MODEL, p) for p in jobs.values()):.3f}")
    except hf.HiggsfieldError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
