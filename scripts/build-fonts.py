"""Build the web fonts (WOFF2) from the licensed Gilroy .ttf files.

Gilroy is a commercial font, so neither the .ttf nor the .woff2 files are committed (the repo is public):
the output folder public/fonts/ is git-ignored. Anyone with the licensed files can rebuild them:

    python scripts/build-fonts.py "C:/Users/wassi/Desktop/DOCS/Internship/01_Brand/Fonts_Gilroy"

Only the six upright weights the CSS uses are built (300 Light ... 800 ExtraBold). Each is subset to Latin
(Basic, Latin-1, Latin Extended-A, general punctuation, currency, arrows) to keep the files small. Gilroy has no
Arabic glyphs; Arabic text falls back to the next fonts in --font (see app/globals.css). The source .ttf files are
read only, never changed or moved. Needs: pip install fonttools brotli
"""

import sys
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont

WEIGHTS = {"Light": 300, "Regular": 400, "Medium": 500, "SemiBold": 600, "Bold": 700, "ExtraBold": 800}
# keep in sync with the unicode-range in app/globals.css
UNICODES = "U+0000-00FF,U+0100-017F,U+2000-206F,U+20A0-20CF,U+2190-21FF,U+2122,U+2212"


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    src = Path(sys.argv[1])
    out = Path(__file__).resolve().parent.parent / "public" / "fonts" / "gilroy"
    out.mkdir(parents=True, exist_ok=True)
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = ["*"]  # keep kerning and ligatures
    opts.name_IDs = ["*"]
    opts.notdef_outline = True
    for name, weight in WEIGHTS.items():
        ttf = src / f"Gilroy-{name}.ttf"
        if not ttf.is_file():
            sys.exit(f"missing {ttf}")
        font = TTFont(ttf)
        sub = subset.Subsetter(options=opts)
        sub.populate(unicodes=subset.parse_unicodes(UNICODES))
        sub.subset(font)
        dest = out / f"gilroy-{weight}.woff2"
        font.flavor = "woff2"
        font.save(dest)
        print(f"{dest.name}: {ttf.stat().st_size // 1024} KB ttf -> {dest.stat().st_size // 1024} KB woff2")


if __name__ == "__main__":
    main()
