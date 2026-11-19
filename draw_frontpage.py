#!/usr/bin/env python3
"""Paint the front page for Thursday, 19 November 2026.

One 1024x1024 PNG that sums up the day's world news as a newspaper
front page. The build is data-first: the stories live in STORIES below
and the page is assembled from them, so changing the news means editing
data, not drawing code.

Composition, top to bottom:
  * nameplate: THE WORLD IN ONE DAY, with the date in red beneath it
  * hero frame: the Shenzhen trilateral summit, full width, with the
    lead headline and standfirst under the picture
  * three picture columns: the Hormuz tanker fires, the GTA VI launch,
    and the World Court's Rohingya ruling
  * ALSO TODAY: four shorter items in two columns
  * footer rule carrying the date once more

Run it with:  python3 draw_frontpage.py
It writes entry.png beside this file. The output is deterministic: the
same inputs always produce the same bytes, because every draw call is
fixed and Pillow writes no timestamps into the pixels.

The three photographs are AI illustrations made for this entry; they
live in assets/ and are cropped to fit their frames.
"""

from __future__ import annotations

import os
from pathlib import Path

from PIL import Image
from PIL import ImageDraw, ImageFont

HERE = Path(__file__).parent.resolve()
PICTURES = HERE / "assets"

PAGE = (1024, 1024)
NEWSPRINT = (247, 242, 232)
INK = (22, 20, 18)
ACCENT = (172, 32, 28)
MUTED = (96, 90, 80)
FAINT = (186, 178, 162)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
TITLE_FACE = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
BODY_FACE = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SANS_FACE = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_STRONG = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")


def face(path: str, size: int) -> ImageFont.FreeTypeFont:
    """Load a TrueType face at the requested point size."""
    return ImageFont.truetype(path, size)


def fit_lines(
    draw: ImageDraw.ImageDraw,
    text: str,
    fnt: ImageFont.FreeTypeFont,
    width: int,
) -> list[str]:
    """Break text into lines that fit inside width pixels."""
    out: list[str] = []
    for chunk in text.split("\n"):
        current = ""
        for word in chunk.split():
            candidate = f"{current} {word}".strip()
            if draw.textlength(candidate, font=fnt) <= width:
                current = candidate
            else:
                if current:
                    out.append(current)
                current = word
        if current:
            out.append(current)
    return out


def blurb(
    draw: ImageDraw.ImageDraw,
    text: str,
    fnt: ImageFont.FreeTypeFont,
    x: int,
    y: int,
    width: int,
    fill=INK,
    gap: int = 4,
) -> int:
    """Draw wrapped text starting at (x, y); return the y below it."""
    for line in fit_lines(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + gap
    return y


def fill_frame(img: Image.Image, tw: int, th: int) -> Image.Image:
    """Crop the picture to the frame's aspect, then scale it to fit."""
    iw, ih = img.size
    zoom = max(tw / iw, th / ih)
    grown = img.resize((round(iw * zoom), round(ih * zoom)), Image.LANCZOS)
    ox = (grown.width - tw) // 2
    oy = (grown.height - th) // 2
    return grown.crop((ox, oy, ox + tw, oy + th))


def centred(draw: ImageDraw.ImageDraw, text: str, fnt, y: int, fill) -> None:
    """Draw one line of text centred across the page at height y."""
    w = draw.textlength(text, font=fnt)
    draw.text(((PAGE[0] - w) / 2, y), text, font=fnt, fill=fill)


# ---------------------------------------------------------------- stories
# Each entry: picture file, kicker, headline, standfirst. The hero is
# handled separately above the columns; these three fill the row below it.

LEAD_KICKER = "SHENZHEN  ·  APEC SUMMIT"
LEAD_HEAD = "Trump, Xi and Putin sit down together in Shenzhen"
LEAD_DECK = (
    "The three leaders meet on the APEC sidelines with Ukraine, trade "
    "and the Gulf on the agenda; Xi sees Putin first, hours after "
    "Ukraine hits the Kerch Bridge for the third time in a week."
)

COLUMNS = [
    (
        "media-generation-hormuz-tankers-20261119-0-0e9470aa-2b60-4c55-80ab-876cb4e930b9.webp",
        "GULF  ·  STRAIT OF HORMUZ",
        "Three tankers burn after hitting mines",
        "Oil tankers catch fire east of the Strait of Hormuz as the "
        "US-Iran exchange of fire widens and Gulf states repel drones.",
    ),
    (
        "media-generation-vice-city-gta6-20261119-0-4b561517-d493-4a27-a69c-959383f9cc5b.webp",
        "CULTURE  ·  GAMES",
        "GTA VI launches worldwide",
        "Gamers flood Vice City as Rockstar's blockbuster begins its "
        "global rollout to near-perfect reviews after a 13-year wait.",
    ),
    (
        "media-generation-hague-court-20261119-0-b540b720-b95f-40d2-8527-bd5a025bd8af.webp",
        "THE HAGUE  ·  WORLD COURT",
        "Court rules on Rohingya genocide case",
        "The World Court gives its ruling on Myanmar's alleged "
        "genocide of the Rohingya, a case watched around the world.",
    ),
]

ALSO = [
    ("VOYAGER 1", "NASA probe reaches one light-day from Earth."),
    ("EU LOAN", "€45bn Ukraine loan, repaid from Russian reparations."),
    ("US HOUSE", "Jeffries set to be first Black Speaker."),
    ("KERCH BRIDGE", "Hit again overnight; traffic suspended."),
]


def paint() -> Path:
    """Draw the whole page and save it as entry.png."""
    sheet = Image.new("RGB", PAGE, NEWSPRINT)
    d = ImageDraw.Draw(sheet)
    margin = 24
    right = PAGE[0] - margin

    # ---- nameplate ---------------------------------------------------
    d.rectangle([0, 0, PAGE[0], 8], fill=INK)
    centred(d, "THE WORLD IN ONE DAY", face(TITLE_FACE, 56), 20, INK)
    centred(d, "THURSDAY, 19 NOVEMBER 2026", face(SANS_STRONG, 25), 90, ACCENT)
    centred(d, "The day's world news in one image",
            face(SANS_FACE, 19), 124, MUTED)
    d.line([margin, 156, right, 156], fill=INK, width=3)
    d.line([margin, 162, right, 162], fill=INK, width=1)

    # ---- hero: the Shenzhen summit ------------------------------------
    hero = Image.open(
        PICTURES / "media-generation-shenzhen-summit-20261119-0-2626b3e5-e718-47b2-8cae-3a78a768d5a3.webp"
    ).convert("RGB")
    sheet.paste(fill_frame(hero, PAGE[0] - 2 * margin, 218), (margin, 170))
    d.rectangle([margin, 170, right, 388], outline=INK, width=2)

    y = 400
    kick = face(SANS_STRONG, 20)
    d.text((margin, y), LEAD_KICKER, font=kick, fill=ACCENT)
    y += 30
    y = blurb(d, LEAD_HEAD, face(TITLE_FACE, 38), margin, y,
              PAGE[0] - 2 * margin, gap=2)
    y += 4
    y = blurb(d, LEAD_DECK, face(SANS_FACE, 19), margin, y,
              PAGE[0] - 2 * margin, gap=3)
    d.line([margin, y + 8, right, y + 8], fill=FAINT, width=2)
    y += 18

    # ---- three picture columns ----------------------------------------
    col_w = 309
    col_gap = (PAGE[0] - 2 * margin - 3 * col_w) // 2
    photo_h = 148
    lowest = y
    for i, (fname, kick_text, head, deck) in enumerate(COLUMNS):
        x = margin + i * (col_w + col_gap)
        pic = Image.open(PICTURES / fname).convert("RGB")
        sheet.paste(fill_frame(pic, col_w, photo_h), (x, y))
        d.rectangle([x, y, x + col_w, y + photo_h], outline=INK, width=2)
        yy = y + photo_h + 10
        d.text((x, yy), kick_text, font=kick, fill=ACCENT)
        yy += 28
        yy = blurb(d, head, face(TITLE_FACE, 22), x, yy, col_w, gap=1)
        yy += 2
        yy = blurb(d, deck, face(SANS_FACE, 15), x, yy, col_w, gap=2)
        lowest = max(lowest, yy)
    y = lowest + 6
    d.line([margin, y, right, y], fill=FAINT, width=2)
    y += 12

    # ---- also today -----------------------------------------------------
    d.text((margin, y), "ALSO ON 19 NOVEMBER 2026", font=kick, fill=ACCENT)
    y += 30
    lead_f = face(SANS_STRONG, 14)
    body_f = face(SANS_FACE, 14)
    half = (PAGE[0] - 2 * margin - col_gap) // 2
    top = y
    for i, (lead, body) in enumerate(ALSO):
        xx = margin if i % 2 == 0 else margin + half + col_gap
        yy = top + (i // 2) * 24
        d.text((xx, yy), "▪ ", font=body_f, fill=ACCENT)
        tag = lead + " — "
        d.text((xx + 18, yy), tag, font=lead_f, fill=INK)
        tag_w = d.textlength(tag, font=lead_f)
        d.text((xx + 18 + tag_w, yy), body, font=body_f, fill=INK)
    y = top + 2 * 24 + 6

    # ---- footer ---------------------------------------------------------
    d.line([margin, PAGE[1] - 44, right, PAGE[1] - 44], fill=INK, width=2)
    centred(d, "19 NOVEMBER 2026  ·  THE WORLD IN ONE IMAGE",
            face(SANS_STRONG, 17), PAGE[1] - 34, INK)

    target = HERE / "entry.png"
    sheet.save(target, format="PNG", optimize=True)
    print(f"wrote {target} {target.stat().st_size} bytes, {sheet.size}")
    return target


if __name__ == "__main__":
    paint()
