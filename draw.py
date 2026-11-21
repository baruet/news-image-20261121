#!/usr/bin/env python3
"""news-image-20261121 v2 — render "THE WORLD TODAY" front page (1024x1024).

All text is drawn programmatically with Pillow + system DejaVu fonts.
No network, no AI image generation, no external assets.
Usage: python3 draw.py [output.png]   (default: entry.png)
"""
import math
import random
import sys

from PIL import Image, ImageDraw, ImageFont

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
BOLD = FONT_DIR + "DejaVuSans-Bold.ttf"
REG = FONT_DIR + "DejaVuSans.ttf"

PAPER = (246, 241, 231)
INK = (26, 26, 26)
NAVY = (16, 36, 62)
GOLD = (201, 162, 39)
RED = (179, 35, 27)
RULE = (180, 172, 152)
GREY = (60, 60, 60)
GREY2 = (70, 70, 70)
WHITE = (255, 255, 255)
PANEL = (18, 28, 48)
LAND = (18, 58, 32)

W, H = 1024, 1024


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(fnt, text, width):
    """Greedy word wrap; returns list of lines that fit `width`."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if fnt.getlength(t) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_centered(d, cx, y, text, fnt, fill):
    d.text((cx - fnt.getlength(text) / 2, y), text, font=fnt, fill=fill)


def draw_stars(d, rng):
    for _ in range(28):
        x = rng.randint(22, 328)
        y = rng.randint(136, 330)
        r = rng.choice([1, 1, 2])
        c = rng.choice([(255, 255, 255), (220, 225, 240), (255, 240, 180)])
        d.ellipse([x - r, y - r, x + r, y + r], fill=c)


def draw_missiles_and_blast(d):
    # Two missile trails converging on the blast at (300, 330).
    for (x0, y0, x1, y1) in [(52, 168, 262, 308), (150, 150, 298, 326)]:
        d.line([(x0, y0), (x1, y1)], fill=(255, 110, 20), width=9)
        d.line([(x0, y0), (x1, y1)], fill=(255, 210, 60), width=4)
        d.ellipse([x1 - 9, y1 - 13, x1 + 9, y1 + 13], fill=(255, 170, 40))
        d.ellipse([x1 - 5, y1 - 8, x1 + 5, y1 + 8], fill=(255, 235, 150))
    # Starburst explosion: 12 yellow rays + bright core.
    cx, cy = 300, 330
    for i in range(12):
        ang = math.radians(i * 30)
        ln = 30 if i % 2 == 0 else 19
        x2 = cx + ln * math.cos(ang)
        y2 = cy + ln * math.sin(ang)
        d.line([(cx, cy), (x2, y2)], fill=(255, 205, 50), width=3)
    d.ellipse([cx - 15, cy - 15, cx + 15, cy + 15], fill=(255, 215, 70))
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=(255, 245, 180))


def icon_chart(d, cx, cy):
    # Axes + 4 descending bars + falling arrow.
    d.line([(cx - 54, cy + 30), (cx + 54, cy + 30)], fill=WHITE, width=3)
    d.line([(cx - 54, cy + 30), (cx - 54, cy - 30)], fill=WHITE, width=3)
    heights = [44, 34, 24, 14]
    for i, hh in enumerate(heights):
        x0 = cx - 44 + i * 24
        d.rectangle([x0, cy + 28 - hh, x0 + 14, cy + 28], fill=(255, 205, 80))
    d.line([(cx - 52, cy - 26), (cx + 50, cy + 16)], fill=WHITE, width=3)
    d.polygon([(cx + 50, cy + 16), (cx + 34, cy + 12), (cx + 46, cy + 26)],
              fill=WHITE)


def icon_globe(d, cx, cy):
    d.ellipse([cx - 34, cy - 34, cx + 34, cy + 34], fill=(52, 120, 190))
    d.ellipse([cx - 34, cy - 34, cx + 34, cy + 34], outline=WHITE, width=2)
    d.ellipse([cx - 14, cy - 34, cx + 14, cy + 34], outline=WHITE, width=2)
    d.line([(cx - 34, cy), (cx + 34, cy)], fill=WHITE, width=2)
    d.polygon([(cx - 18, cy + 8), (cx + 2, cy - 14), (cx + 20, cy + 10)],
              fill=(60, 170, 90))


def icon_cricket(d, cx, cy):
    # Three stumps + bails, angled bat, red ball.
    for i in range(3):
        x0 = cx - 46 + i * 9
        d.rectangle([x0, cy - 22, x0 + 5, cy + 24], fill=WHITE)
    d.rectangle([cx - 46, cy - 26, cx - 19, cy - 22], fill=WHITE)
    d.line([(cx + 4, cy + 30), (cx + 30, cy - 24)], fill=(230, 190, 130),
           width=9)
    d.ellipse([cx + 42, cy + 18, cx + 56, cy + 32], fill=(200, 40, 40))
    d.ellipse([cx + 42, cy + 18, cx + 56, cy + 32], outline=WHITE, width=1)


def icon_quake(d, cx, cy):
    # Sharp white seismograph zigzag across the band + small starburst.
    pts = [(cx - 148, cy + 4), (cx - 116, cy - 18), (cx - 92, cy + 16),
           (cx - 64, cy - 26), (cx - 36, cy + 10), (cx - 12, cy - 14),
           (cx + 16, cy + 20), (cx + 44, cy - 8), (cx + 76, cy + 12),
           (cx + 108, cy - 16), (cx + 140, cy + 2)]
    d.line(pts, fill=WHITE, width=3, joint="curve")
    for i in range(8):
        ang = math.radians(i * 45)
        x2 = cx + 12 * math.cos(ang)
        y2 = cy + 12 * math.sin(ang)
        d.line([(cx, cy), (x2, y2)], fill=(255, 210, 60), width=2)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(255, 230, 120))


def icon_flame(d, cx, cy):
    # Teardrop flame: orange outer, gold mid, bright core.
    d.polygon([(cx - 18, cy + 2), (cx, cy - 34), (cx + 18, cy + 2)],
              fill=(255, 140, 0))
    d.ellipse([cx - 20, cy - 4, cx + 20, cy + 34], fill=(255, 140, 0))
    d.ellipse([cx - 10, cy + 4, cx + 10, cy + 30], fill=(255, 205, 60))
    d.ellipse([cx - 5, cy + 12, cx + 5, cy + 28], fill=(255, 245, 180))


def icon_padlock(d, cx, cy):
    d.arc([cx - 16, cy - 28, cx + 16, cy + 6], 180, 360, fill=WHITE, width=6)
    d.rounded_rectangle([cx - 22, cy, cx + 22, cy + 32], radius=4,
                        fill=(255, 205, 60))
    d.ellipse([cx - 4, cy + 10, cx + 4, cy + 18], fill=(88, 32, 96))


CELLS = [
    ((122, 28, 24), icon_chart, "MARKETS  •  AI",
     "AI SELL-OFF PUSHES S&P INTO CORRECTION",
     "US stocks -3.7% on Friday; Anthropic -8.5% after $2tn debut"),
    ((24, 110, 60), icon_globe, "CLIMATE  •  TURKEY",
     "COP31 DEADLOCKED IN OVERTIME",
     "No deal as talks run past deadline; fossil-fuel text stripped"),
    ((140, 90, 10), icon_cricket, "SPORT  •  CRICKET",
     "INDIA ON TOP IN WELLINGTON",
     "Rahul 136, Gill 98; India 486/4, lead by 118 on day three"),
    ((16, 60, 110), icon_quake, "DISASTER  •  PERU",
     "6.8 QUAKE SHAKES PERU'S ANDES",
     "Lima residents flee to streets; no major damage reported"),
    ((179, 35, 27), icon_flame, "MIDDLE EAST  •  IRAQ",
     "BASRA POWER PLANT FIRE KILLS FOUR",
     "Blaze injures 35 at Hartha station"),
    ((88, 32, 96), icon_padlock, "USA  •  CYBER",
     "FBI AND USDA HIT BY HACKERS",
     "Crime database probed; farm payments knocked offline"),
]


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    rng = random.Random(42)

    # ---- Masthead ----
    d.rectangle([4, 4, 1019, 116], fill=NAVY)
    draw_centered(d, W // 2, 16, "T H E   W O R L D   T O D A Y",
                  font(BOLD, 26), GOLD)
    draw_centered(d, W // 2, 52, "SATURDAY 21 NOVEMBER 2026",
                  font(BOLD, 52), WHITE)
    d.line([(24, 112), (1000, 112)], fill=GOLD, width=2)

    # ---- Lead art panel ----
    d.rectangle([16, 130, 336, 424], fill=PANEL)
    draw_stars(d, rng)
    d.polygon([(16, 424), (16, 382), (70, 362), (140, 386), (210, 358),
               (275, 380), (336, 362), (336, 424)], fill=LAND)
    draw_missiles_and_blast(d)
    d.text((28, 392), "WARSAW • NATO PLEDGE", font=font(BOLD, 17), fill=WHITE)

    # ---- Lead text ----
    d.text((356, 138), "LEAD STORY  •  EUROPE", font=font(BOLD, 22), fill=RED)
    hl_lines = wrap(font(BOLD, 58),
                    "RUTTE IN WARSAW: NATO WILL DEFEND EVERY INCH", 648)
    for i, ln in enumerate(hl_lines):
        d.text((356, 158 + i * 64), ln, font=font(BOLD, 58), fill=INK)
    sub_lines = wrap(
        font(REG, 27),
        "A day after Russian missiles landed in Poland, the alliance "
        "chief pledges to defend Polish soil", 652)
    for i, ln in enumerate(sub_lines):
        d.text((356, 338 + i * 34), ln, font=font(REG, 27), fill=GREY)
    d.line([(356, 408), (1008, 408)], fill=RULE, width=2)

    # ---- Grid of 6 cells ----
    # NOTE (deviation from brief): cell height 268 (not 252) and rows at
    # y=430/704 (not 440/708); headline leading 28 (not 31), sub leading
    # 20 (not 23). The brief's 252px cells cannot hold a 3-line headline
    # + 3-line sub at the specified sizes/leadings without the sub crossing
    # the cell outline; the taller cells keep every line inside the frame.
    xs = [16, 352, 688]
    ys = [430, 704]
    for idx, (band, icon_fn, kicker, headline, sub) in enumerate(CELLS):
        x0 = xs[idx % 3]
        y0 = ys[idx // 3]
        d.rectangle([x0, y0, x0 + 319, y0 + 95], fill=band)
        icon_fn(d, x0 + 160, y0 + 48)
        d.rectangle([x0, y0, x0 + 319, y0 + 267], outline=RULE, width=2)
        d.text((x0 + 12, y0 + 106), kicker, font=font(BOLD, 17), fill=RED)
        hl = wrap(font(BOLD, 27), headline, 296)
        bottom = y0 + 122
        for i, ln in enumerate(hl):
            yy = y0 + 122 + i * 28
            d.text((x0 + 12, yy), ln, font=font(BOLD, 27), fill=INK)
            _, _, _, b = d.textbbox((x0 + 12, yy), ln, font=font(BOLD, 27))
            bottom = max(bottom, b)
        sb = wrap(font(REG, 19), sub, 296)
        for i, ln in enumerate(sb):
            d.text((x0 + 12, bottom + 4 + i * 20), ln, font=font(REG, 19),
                   fill=GREY2)

    # ---- Bottom ticker ----
    d.rectangle([4, 976, 1019, 1020], fill=NAVY)
    d.text((20, 988), "ALSO TODAY:", font=font(BOLD, 20), fill=GOLD)
    ticker_long = ("Bayer $7.25bn Roundup deal • Spain extends bank tax • "
                   "UN 'killer robot' talks")
    ticker_short = "Bayer $7.25bn deal • Spain bank tax • UN robot talks"
    ticker = (ticker_long if font(REG, 20).getlength(ticker_long) <= 836
              else ticker_short)
    d.text((172, 988), ticker, font=font(REG, 20), fill=WHITE)

    # ---- Outer frame (drawn last so it stays on top) ----
    d.rectangle([0, 0, 1023, 1023], outline=INK, width=4)

    img.save(out, optimize=True)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
