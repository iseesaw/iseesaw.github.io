#!/usr/bin/env python3
"""Normalize publication preview images to a uniform letterboxed canvas.

Scales each input to fit the canvas (no crop, no stretch), centers it on a
white background, and saves as an optimized JPEG named <input-stem>.jpg in
the output directory. Keep the stem identical to the `preview={...}` field
in _bibliography/papers.bib.

Usage:
  python3 normalize_thumbnail.py fig1.png fig2.jpg
  python3 normalize_thumbnail.py fig.png --width 2400 --height 1350   # sharper, larger files
"""

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow is required: python3 -m pip install Pillow")

DEFAULT_OUT = "assets/img/publication_preview"


def normalize(src: Path, out_dir: Path, width: int, height: int, quality: int) -> Path:
    im = Image.open(src).convert("RGB")
    scale = min(width / im.width, height / im.height)
    new_size = (round(im.width * scale), round(im.height * scale))
    im = im.resize(new_size, Image.LANCZOS)
    canvas = Image.new("RGB", (width, height), "#FFFFFF")
    canvas.paste(im, ((width - new_size[0]) // 2, (height - new_size[1]) // 2))
    out_path = out_dir / (src.stem + ".jpg")
    canvas.save(out_path, quality=quality, optimize=True)
    return out_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("inputs", nargs="+", type=Path, help="source figure images (any format/aspect ratio)")
    parser.add_argument("--out", type=Path, default=Path(DEFAULT_OUT), help=f"output directory (default: {DEFAULT_OUT})")
    parser.add_argument("--width", type=int, default=1600, help="canvas width (default: 1600)")
    parser.add_argument("--height", type=int, default=900, help="canvas height (default: 900)")
    parser.add_argument("--quality", type=int, default=88, help="JPEG quality (default: 88)")
    args = parser.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    for src in args.inputs:
        if not src.is_file():
            sys.exit(f"not a file: {src}")
        out_path = normalize(src, args.out, args.width, args.height, args.quality)
        print(f"{src} -> {out_path} ({out_path.stat().st_size // 1024}KB)")


if __name__ == "__main__":
    main()
