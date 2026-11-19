#!/usr/bin/env python3
"""Publish the 19 November 2026 front page for make.fun's news-image-20261119.

The picture itself is baked into this repository: draw_frontpage.py
renders the newspaper page into entry.png, and this program — the only
code the grader runs — checks that picture against the competition's
gate and hands it over byte for byte.

What it does, in order:
  1. reads entry.png from beside this file;
  2. refuses anything that is not a whole PNG inside the gate (at most
     1 MiB, at most 1024 by 1024 pixels, ending in a proper IEND chunk);
  3. copies those exact bytes to /output/entry.png
     (MAKEFUN_OUTPUT_DIR stands in for /output outside the grader);
  4. re-reads what it wrote and fails loudly if a single byte differs.

Two runs therefore write the same bytes: the input is fixed, the copy
is a plain byte copy, and nothing here touches the network or the clock.
Python 3.13, standard library only.

Try it outside the grader with:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

from __future__ import annotations

import hashlib
import os
import sys
from pathlib import Path

BASE = Path(__file__).parent.resolve()
PICTURE = BASE / "entry.png"

BYTE_CAP = 1_048_576
EDGE_CAP = 1024
PNG_HEAD = b"\x89PNG\r\n\x1a\n"


class GateError(ValueError):
    """Raised when entry.png breaks one of the competition's limits."""


def png_dimensions(blob: bytes) -> tuple[int, int]:
    """Pull (width, height) out of a PNG's IHDR chunk.

    The header is parsed by hand so the program needs no image library:
    eight magic bytes, then a 13-byte IHDR chunk whose first eight payload
    bytes are the width and height, big-endian.
    """
    if len(blob) < 33 or blob[:8] != PNG_HEAD:
        raise GateError("entry.png does not start with the PNG signature")
    size, kind = int.from_bytes(blob[8:12], "big"), blob[12:16]
    if kind != b"IHDR" or size != 13:
        raise GateError("entry.png has no IHDR chunk in second place")
    width = int.from_bytes(blob[16:20], "big")
    height = int.from_bytes(blob[20:24], "big")
    # IHDR's remaining fields sit right after the dimensions: one byte of
    # bit depth, one of colour type, then compression, filter and interlace
    # flags. A gate-worthy PNG uses a depth and colour type the format
    # actually defines, so refuse anything outside those sets.
    depth, colour = blob[24], blob[25]
    if depth not in (1, 2, 4, 8, 16) or colour not in (0, 2, 3, 4, 6):
        raise GateError(
            f"entry.png has an impossible IHDR: depth {depth}, colour {colour}")
    if len(blob) < 45 or blob[-12:-8] != b"\x00\x00\x00\x00" \
            or blob[-8:-4] != b"IEND":
        raise GateError("entry.png is cut short: no IEND chunk at its end")
    return width, height


def check_image(blob: bytes) -> tuple[int, int]:
    """Apply the gate's limits to the raw bytes; return the dimensions."""
    if len(blob) > BYTE_CAP:
        raise GateError(
            f"entry.png is {len(blob)} bytes, past the {BYTE_CAP} cap")
    width, height = png_dimensions(blob)
    if width > EDGE_CAP or height > EDGE_CAP:
        raise GateError(
            f"entry.png is {width}x{height}, past the {EDGE_CAP}x{EDGE_CAP} cap")
    if width <= 0 or height <= 0:
        raise GateError(f"entry.png claims impossible size {width}x{height}")
    return width, height


def publish_copy(blob: bytes) -> Path:
    """Write blob to the output directory and prove it landed intact."""
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    target.write_bytes(blob)
    if target.read_bytes() != blob:
        raise GateError("the copy in the output directory differs")
    return target


def main() -> int:
    blob = PICTURE.read_bytes()
    width, height = check_image(blob)
    target = publish_copy(blob)
    digest = hashlib.sha256(blob).hexdigest()
    print(f"wrote {target} ({width}x{height}, {len(blob)} bytes, "
          f"sha256 {digest})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
