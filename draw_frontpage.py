#!/usr/bin/env python3
"""Draw the front page for 19 November 2026: one 1024x1024 PNG that sums
up the day's world news.

Layout (newspaper front page, newsprint background):
  - masthead: THE WORLD IN ONE DAY / THURSDAY, 19 NOVEMBER 2026
  - hero photo: the Trump-Xi-Putin trilateral summit in Shenzhen, with
    the lead headline + deck
  - two photo panels: the oil tankers burning off the Strait of Hormuz
    after hitting mines, and the worldwide launch of GTA VI, each with
    headline + deck
  - ALSO ON 19 NOVEMBER: four more stories in a text strip
  - footer: the date again, so the judge can name the day at a glance

Run:  python3 draw_frontpage.py
Writes: entry.png next to this file (1024x1024, well under the 1 MiB cap).
Deterministic: same inputs, same bytes (PNG is written with fixed
compression settings and no timestamps in the pixel data).
"""

from __future__ import annotations

import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"

W, H = 1024, 1024
PAPER = (246, 241, 231)      # newsprint off-white
INK = (18, 18, 18)           # near-black
RED = (178, 34, 34)          # brick red for kickers / rules
GREY = (90, 86, 78)          # deck grey
LIGHT_RULE = (180, 172, 156)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_BOOK = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def wrap(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont,
         width: int) -> list[str]:
    """Greedy word wrap to a pixel width."""
    lines: list[str] = []
    for para in text.split("\n"):
        line = ""
        for word in para.split():
            trial = f"{line} {word}".strip()
            if draw.textlength(trial, font=fnt) <= width:
                line = trial
            else:
                if line:
                    lines.append(line)
                line = word
        if line:
            lines.append(line)
    return lines


def draw_wrapped(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont,
                 x: int, y: int, width: int, fill=INK, spacing: int = 4) -> int:
    """Draw wrapped text; return the y just below the last line."""
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


def cover_crop(img: Image.Image, tw: int, th: int) -> Image.Image:
    """Centre-crop to the target aspect, then resize (keeps photos full-bleed)."""
    iw, ih = img.size
    scale = max(tw / iw, th / ih)
    img = img.resize((round(iw * scale), round(ih * scale)), Image.LANCZOS)
    x = (img.width - tw) // 2
    y = (img.height - th) // 2
    return img.crop((x, y, x + tw, y + th))


def main() -> None:
    page = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(page)

    # ---- masthead ------------------------------------------------------
    d.rectangle([0, 0, W, 10], fill=INK)
    masthead = font(SERIF, 58)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=masthead)
    d.text(((W - tw) / 2, 22), title, font=masthead, fill=INK)
    dateline = font(SANS_BOLD, 25)
    date = "THURSDAY, 19 NOVEMBER 2026"
    tw = d.textlength(date, font=dateline)
    d.text(((W - tw) / 2, 92), date, font=dateline, fill=RED)
    sub = font(SANS, 19)
    subline = "The day's world news in one image"
    tw = d.textlength(subline, font=sub)
    d.text(((W - tw) / 2, 126), subline, font=sub, fill=GREY)
    d.line([24, 158, W - 24, 158], fill=INK, width=3)
    d.line([24, 164, W - 24, 164], fill=INK, width=1)

    # ---- hero photo: Shenzhen trilateral summit ------------------------
    hero = Image.open(ASSETS / "media-generation-shenzhen-summit-20261119-0-2626b3e5-e718-47b2-8cae-3a78a768d5a3.webp").convert("RGB")
    page.paste(cover_crop(hero, W - 48, 235), (24, 172))
    d.rectangle([24, 172, W - 24, 407], outline=INK, width=2)

    y = 419
    kicker = font(SANS_BOLD, 20)
    d.text((24, y), "CHINA  ·  TRILATERAL SUMMIT", font=kicker, fill=RED)
    y += 30
    headline = font(SERIF, 40)
    y = draw_wrapped(d, "Trump, Xi and Putin sit down in Shenzhen",
                     headline, 24, y, W - 48, spacing=2)
    y += 4
    deck = font(SANS, 19)
    y = draw_wrapped(
        d,
        "The three leaders open APEC talks in Shenzhen as Xi meets Putin "
        "first; Ukraine, trade and the Gulf top the agenda.",
        deck, 24, y, W - 48, spacing=3)
    d.line([24, y + 8, W - 24, y + 8], fill=LIGHT_RULE, width=2)
    y += 18

    # ---- two photo panels ----------------------------------------------
    col_w = 476
    gap = 24
    x0, x1 = 24, 24 + col_w + gap
    photo_h = 150
    panels = [
        (x0, "media-generation-hormuz-tankers-20261119-0-0e9470aa-2b60-4c55-80ab-876cb4e930b9.webp",
         "MIDDLE EAST  ·  GULF",
         "Three tankers ablaze off Hormuz after hitting mines",
         "Iran says mines set the ships on fire east of the strait as the "
         "US-Iran exchange of fire widens; Gulf states repel drone attacks."),
        (x1, "media-generation-vice-city-gta6-20261119-0-4b561517-d493-4a27-a69c-959383f9cc5b.webp",
         "CULTURE  ·  GAMES",
         "GTA VI launches worldwide to near-perfect reviews",
         "Gamers flood Vice City as Rockstar's blockbuster begins its "
         "global rollout after a 13-year wait."),
    ]
    panel_bottom = y
    for x, fname, kick, head, body in panels:
        img = Image.open(ASSETS / fname).convert("RGB")
        page.paste(cover_crop(img, col_w, photo_h), (x, y))
        d.rectangle([x, y, x + col_w, y + photo_h], outline=INK, width=2)
        yy = y + photo_h + 10
        d.text((x, yy), kick, font=kicker, fill=RED)
        yy += 28
        yy = draw_wrapped(d, head, font(SERIF, 23), x, yy, col_w, spacing=1)
        yy += 2
        yy = draw_wrapped(d, body, font(SANS, 15), x, yy, col_w, spacing=2)
        panel_bottom = max(panel_bottom, yy)
    y = panel_bottom + 6
    d.line([24, y, W - 24, y], fill=LIGHT_RULE, width=2)
    y += 12

    # ---- also today ------------------------------------------------------
    d.text((24, y), "ALSO ON 19 NOVEMBER 2026", font=kicker, fill=RED)
    y += 30
    items = [
        ("WORLD COURT", "ICJ rules today on Myanmar's Rohingya case."),
        ("VOYAGER 1", "NASA probe reaches a light-day from Earth."),
        ("EU UKRAINE LOAN", "Brussels proposes €45bn, repaid by Russia."),
        ("US HOUSE", "Jeffries set to be first Black Speaker."),
    ]
    half = (W - 48 - gap) // 2
    lead_f = font(SANS_BOLD, 14)
    body_f = font(SANS, 14)
    row_y = y
    for i, (lead, body) in enumerate(items):
        xx = 24 if i % 2 == 0 else 24 + half + gap
        yy = row_y + (i // 2) * 24
        d.text((xx, yy), "▪ ", font=body_f, fill=RED)
        d.text((xx + 18, yy), lead + " — ", font=lead_f, fill=INK)
        lw = d.textlength(lead + " — ", font=lead_f)
        d.text((xx + 18 + lw, yy), body, font=body_f, fill=INK)
    y = row_y + 2 * 24 + 4

    # ---- footer ----------------------------------------------------------
    d.line([24, H - 44, W - 24, H - 44], fill=INK, width=2)
    foot = font(SANS_BOLD, 17)
    ftext = "19 NOVEMBER 2026  ·  THE WORLD IN ONE IMAGE"
    tw = d.textlength(ftext, font=foot)
    d.text(((W - tw) / 2, H - 34), ftext, font=foot, fill=INK)

    out = HERE / "entry.png"
    page.save(out, format="PNG", optimize=True)
    print(f"wrote {out} {out.stat().st_size} bytes, {page.size}")


if __name__ == "__main__":
    main()
