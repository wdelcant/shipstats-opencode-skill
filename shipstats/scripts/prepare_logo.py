#!/usr/bin/env python3
"""Resize a logo to 128x128 WebP and emit a data URI ready to embed in HTML.

Usage:
    python3 prepare_logo.py <path-to-logo>

Prints a single line to stdout:
    data:image/webp;base64,<...>

Errors go to stderr with a non-zero exit code.
"""

import argparse
import base64
import io
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.stderr.write(
        "Pillow not installed. Install with: pip install Pillow\n"
    )
    sys.exit(2)

TARGET_SIZE = 128
WEBP_QUALITY = 90


def prepare(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Logo file not found: {path}")

    img = Image.open(path)
    img = img.convert("RGBA")

    img.thumbnail((TARGET_SIZE, TARGET_SIZE), Image.Resampling.LANCZOS)

    canvas = Image.new("RGBA", (TARGET_SIZE, TARGET_SIZE), (0, 0, 0, 0))
    offset = (
        (TARGET_SIZE - img.width) // 2,
        (TARGET_SIZE - img.height) // 2,
    )
    canvas.paste(img, offset, img)

    buf = io.BytesIO()
    canvas.save(buf, format="WEBP", quality=WEBP_QUALITY, method=6)
    encoded = base64.b64encode(buf.getvalue()).decode("ascii")
    return f"data:image/webp;base64,{encoded}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="Path to logo (PNG/JPG/WebP/SVG raster)")
    args = parser.parse_args()

    try:
        print(prepare(args.path))
    except Exception as exc:
        sys.stderr.write(f"error: {exc}\n")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
