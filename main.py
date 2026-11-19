#!/usr/bin/env python3
"""Entry for make.fun news-image-20261119 (Python 3.13, standard library only).

The entry is a newspaper front page for Thursday, 19 November 2026, drawn
by draw_frontpage.py into ``entry.png`` next to this file: the Trump-Xi-Putin
trilateral summit in Shenzhen leads, with the oil tankers burning off the
Strait of Hormuz and the worldwide launch of GTA VI below, plus four more
stories of the day. This program is the whole runtime behaviour: it validates
the image against the competition gate (a whole PNG, at most 1 MiB, at most
1024 by 1024 pixels) and copies it, byte for byte, to ``/output/entry.png``.

Determinism: the copy is a plain byte copy of a fixed file, so two runs
write identical bytes. No network is used at runtime; the image is baked
into the repository.

Run outside the grader's container with:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

from __future__ import annotations

import hashlib
import os
import shutil
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"

MAX_BYTES = 1_048_576          # the gate's 1 MiB cap
MAX_SIDE = 1024                # the gate's 1024 by 1024 cap
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def read_png_size(data: bytes) -> tuple[int, int]:
    """Return (width, height) from a PNG's IHDR chunk, or raise ValueError.

    Parses the header by hand instead of importing an image library, so the
    program stays standard-library only: magic, then the 25-byte IHDR
    chunk (length, type, width, height, ...), big-endian.
    """
    if len(data) < 33 or data[:8] != PNG_MAGIC:
        raise ValueError("entry.png is not a PNG file")
    length, chunk_type = struct.unpack(">I4s", data[8:16])
    if chunk_type != b"IHDR" or length != 13:
        raise ValueError("entry.png has no IHDR chunk where one belongs")
    width, height = struct.unpack(">II", data[16:24])
    # The gate reads a whole image, so refuse a truncated file: the last
    # 12 bytes must be the IEND chunk (length 0, type IEND, CRC).
    if len(data) < 45 or data[-12:-8] != b"\x00\x00\x00\x00" or data[-8:-4] != b"IEND":
        raise ValueError("entry.png is truncated: no IEND chunk at the end")
    return width, height


def validate(data: bytes) -> tuple[int, int]:
    """Check the gate's limits; return the image dimensions."""
    if len(data) > MAX_BYTES:
        raise ValueError(
            f"entry.png is {len(data)} bytes, over the {MAX_BYTES} byte cap")
    width, height = read_png_size(data)
    if width > MAX_SIDE or height > MAX_SIDE:
        raise ValueError(
            f"entry.png is {width}x{height}, over the {MAX_SIDE}x{MAX_SIDE} cap")
    if width <= 0 or height <= 0:
        raise ValueError(f"entry.png has impossible dimensions {width}x{height}")
    return width, height


def main() -> int:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    if not SOURCE.is_file():
        raise ValueError(
            f"{SOURCE.name} is missing next to main.py: the image is baked "
            "into the repository, so a missing file means a bad checkout")
    data = SOURCE.read_bytes()
    width, height = validate(data)
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    # A byte copy, not a re-encode: the judge sees exactly the bytes the
    # repository holds, and a second run writes the same bytes again.
    shutil.copyfile(SOURCE, target)
    written = target.read_bytes()
    if written != data:
        raise ValueError("the copy does not match entry.png byte for byte")
    digest = hashlib.sha256(written).hexdigest()
    print(f"wrote {target} ({width}x{height}, {len(data)} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
