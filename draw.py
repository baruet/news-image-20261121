#!/usr/bin/env python3
"""Draw the 21 November 2026 world-news front page.

One image, 1024x1024 PNG, all text rendered programmatically with PIL +
DejaVu so no glyph is ever garbled. Run:  python3 draw.py [out.png]
"""
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = sys.argv[1] if len(sys.argv) > 1 else "entry.png"

PAPER = (246, 241, 231)
INK = (26, 26, 26)
NAVY = (16, 36, 62)
NAVY2 = (24, 52, 88)
RED = (179, 35, 27)
GOLD = (201, 162, 39)
GREY = (90, 90, 86)
RULE = (180, 172, 152)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w):
    """Greedy word wrap into lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, lines, fnt, fill, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.12)
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def centered(d, cx, y, text, fnt, fill):
    w = d.textlength(text, font=fnt)
    d.text((cx - w / 2, y), text, font=fnt, fill=fill)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---- outer frame -------------------------------------------------------
d.rectangle([0, 0, W - 1, H - 1], outline=INK, width=4)

# ---- masthead ----------------------------------------------------------
d.rectangle([4, 4, W - 5, 116], fill=NAVY)
centered(d, W // 2, 16, "T H E   W O R L D   T O D A Y", font(FB, 26), GOLD)
centered(d, W // 2, 52, "SATURDAY 21 NOVEMBER 2026", font(FB, 52), (255, 255, 255))
d.line([24, 112, W - 24, 112], fill=GOLD, width=2)

# ---- lead story --------------------------------------------------------
# art panel: night sky over land, two missile streaks, explosion star
ax0, ay0, ax1, ay1 = 16, 130, 336, 424
d.rectangle([ax0, ay0, ax1, ay1], fill=(18, 28, 48))
for sx, sy in [(60, 170), (120, 150), (200, 185), (260, 160), (300, 200)]:
    d.ellipse([sx, sy, sx + 3, sy + 3], fill=(220, 220, 200))
# landmass
d.polygon([(16, 360), (120, 320), (210, 345), (336, 320), (336, 424), (16, 424)],
          fill=(52, 68, 54))
# missile streaks (red-orange trails, flame heads)
for (x0, y0, x1, y1) in [(60, 150, 150, 300), (230, 140, 285, 290)]:
    d.line([x0, y0, x1, y1], fill=(255, 120, 40), width=6)
    d.line([x0, y0, x1, y1], fill=(255, 220, 120), width=2)
    d.ellipse([x1 - 9, y1 - 9, x1 + 9, y1 + 9], fill=(255, 180, 60))
# explosion starburst
cx, cy = 300, 330
for ang in range(0, 360, 30):
    import math
    r1, r2 = 14, 34
    a = math.radians(ang)
    d.line([cx + r1 * math.cos(a), cy + r1 * math.sin(a),
            cx + r2 * math.cos(a), cy + r2 * math.sin(a)],
           fill=(255, 200, 60), width=5)
d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=(255, 230, 140))
d.text((28, 392), "POLAND  •  NATO AIRSPACE", font=font(FB, 17), fill=(255, 255, 255))

tx = 356
d.text((tx, 138), "LEAD STORY  •  EUROPE", font=font(FB, 22), fill=RED)
y = 168
y = text_block(d, tx, y,
               wrap(d, "RUSSIAN MISSILES LAND IN POLAND", font(FB, 58), 1024 - tx - 20),
               font(FB, 58), INK, leading=64)
y += 6
y = text_block(d, tx, y,
               wrap(d, "NATO calls it a \u201cgrave violation\u201d \u2014 Rutte heads to Warsaw today",
                    font(FR, 27), 1024 - tx - 20),
               font(FR, 27), (60, 60, 60), leading=34)
d.line([tx, 408, 1008, 408], fill=RULE, width=2)

# ---- supporting grid ---------------------------------------------------
cells = [
    # (band colour, icon, kicker, headline, sub)
    ((122, 28, 24), "chart",
     "MARKETS  •  AI",
     "ANTHROPIC SLUMPS AFTER IPO",
     "Shares -8.5% after debut"),
    ((88, 32, 96), "skyline",
     "CULTURE  •  GAMES",
     "GTA VI: $3.79BN IN A DAY",
     "Biggest entertainment launch in history"),
    ((16, 60, 110), "servers",
     "USA  •  TECH",
     "TRUMP THREATENS DATA-CENTRE TAX",
     "\u201cTremendous tax\u201d on firms building abroad"),
    ((14, 90, 110), "cyclone",
     "ASIA  •  WEATHER",
     "CYCLONE AKVAN HITS ODISHA",
     "370,000 evacuated; no major damage"),
    ((24, 110, 60), "globe",
     "CLIMATE  •  TURKEY",
     "COP31 IN FINAL STAGE",
     "UN summit nears a deal"),
    ((140, 90, 10), "cricket",
     "SPORT  •  CRICKET",
     "INDIA FIGHT BACK IN WELLINGTON",
     "159/1 at stumps on day two of the Test"),
]

CELL_W, CELL_H = 320, 252
GX = [16, 352, 688]
GY = [440, 708]


def icon_chart(d, x0, y0, w, h):
    d.line([x0 + 14, y0 + h - 18, x0 + w - 14, y0 + h - 18], fill=(255, 255, 255), width=3)
    d.line([x0 + 14, y0 + 14, x0 + 14, y0 + h - 18], fill=(255, 255, 255), width=3)
    bars = [(40, 96), (85, 74), (130, 52), (175, 30)]
    for bx, bh in bars:
        d.rectangle([x0 + bx, y0 + h - 18 - bh, x0 + bx + 34, y0 + h - 18], fill=(255, 120, 90))
    d.line([x0 + 40, y0 + 30, x0 + 220, y0 + 108], fill=(255, 220, 60), width=5)
    d.polygon([(x0 + 220, y0 + 108), (x0 + 204, y0 + 100), (x0 + 212, y0 + 122)],
              fill=(255, 220, 60))


def icon_skyline(d, x0, y0, w, h):
    for i, (bx, bw, bh) in enumerate([(20, 34, 70), (62, 26, 100), (96, 40, 60),
                                      (144, 30, 110), (182, 36, 78), (226, 30, 95)]):
        d.rectangle([x0 + bx, y0 + h - 14 - bh, x0 + bx + bw, y0 + h - 14], fill=(30, 16, 54))
        for wy in range(y0 + h - 14 - bh + 10, y0 + h - 20, 18):
            d.rectangle([x0 + bx + 6, wy, x0 + bx + 12, wy + 8], fill=(255, 200, 90))
    d.ellipse([x0 + w - 62, y0 + 12, x0 + w - 22, y0 + 52], fill=(255, 120, 160))


def icon_servers(d, x0, y0, w, h):
    for rx in (40, 120, 200):
        d.rectangle([x0 + rx, y0 + 16, x0 + rx + 56, y0 + h - 16], fill=(20, 40, 70),
                    outline=(255, 255, 255), width=2)
        for ry in range(y0 + 28, y0 + h - 24, 22):
            d.rectangle([x0 + rx + 8, ry, x0 + rx + 30, ry + 10], fill=(90, 200, 255))
            d.ellipse([x0 + rx + 40, ry + 2, x0 + rx + 48, ry + 10], fill=(255, 200, 60))


def icon_cyclone(d, x0, y0, w, h):
    cx, cy = x0 + w // 2, y0 + h // 2 - 4
    for r in (18, 32, 46, 60):
        d.arc([cx - r, cy - r, cx + r, cy + r], start=20, end=300,
              fill=(255, 255, 255), width=5)
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(255, 220, 60))
    for dx, dy in [(-70, 40), (-40, 55), (50, 50), (75, 35)]:
        d.line([cx + dx, cy + dy, cx + dx - 6, cy + dy + 16], fill=(140, 210, 255), width=4)


def icon_globe(d, x0, y0, w, h):
    cx, cy, r = x0 + w // 2, y0 + h // 2, 52
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(40, 130, 200))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255), width=3)
    d.ellipse([cx - 18, cy - r, cx + 18, cy + r], outline=(255, 255, 255), width=2)
    d.line([cx - r, cy, cx + r, cy], fill=(255, 255, 255), width=2)
    d.arc([cx - r, cy - 26, cx + r, cy + 26], start=0, end=180, fill=(255, 255, 255), width=2)
    d.polygon([(cx + 30, cy + 44), (cx + 66, cy + 30), (cx + 62, cy + 62)],
              fill=(60, 200, 90))


def icon_cricket(d, x0, y0, w, h):
    # stumps
    for sx in (60, 78, 96):
        d.rectangle([x0 + sx, y0 + 40, x0 + sx + 8, y0 + 110], fill=(240, 220, 160))
    d.rectangle([x0 + 58, y0 + 32, x0 + 108, y0 + 40], fill=(240, 220, 160))
    # bat, angled
    d.polygon([(x0 + 170, y0 + 30), (x0 + 196, y0 + 30), (x0 + 180, y0 + 120),
               (x0 + 162, y0 + 118)], fill=(220, 180, 120))
    d.rectangle([x0 + 176, y0 + 16, x0 + 186, y0 + 34], fill=(160, 120, 70))
    # ball
    d.ellipse([x0 + 230, y0 + 78, x0 + 262, y0 + 110], fill=(200, 30, 30))
    d.arc([x0 + 230, y0 + 78, x0 + 262, y0 + 110], start=300, end=60,
          fill=(255, 255, 255), width=2)


ICONS = {"chart": icon_chart, "skyline": icon_skyline, "servers": icon_servers,
         "cyclone": icon_cyclone, "globe": icon_globe, "cricket": icon_cricket}

for i, (band, icon, kicker, headline, sub) in enumerate(cells):
    x0 = GX[i % 3]
    y0 = GY[i // 3]
    d.rectangle([x0, y0, x0 + CELL_W - 1, y0 + CELL_H - 1], outline=RULE, width=2)
    d.rectangle([x0, y0, x0 + CELL_W - 1, y0 + 96], fill=band)
    ICONS[icon](d, x0, y0, CELL_W, 96)
    ty = y0 + 106
    d.text((x0 + 12, ty), kicker, font=font(FB, 17), fill=RED)
    ty += 24
    ty = text_block(d, x0 + 12, ty,
                    wrap(d, headline, font(FB, 27), CELL_W - 24),
                    font(FB, 27), INK, leading=31)
    ty += 4
    text_block(d, x0 + 12, ty,
               wrap(d, sub, font(FR, 19), CELL_W - 24),
               font(FR, 19), (70, 70, 70), leading=23)

# ---- bottom ticker -----------------------------------------------------
d.rectangle([4, 976, W - 5, 1020], fill=NAVY)
d.text((20, 988), "ALSO TODAY:", font=font(FB, 20), fill=GOLD)
d.text((172, 988),
       "Mongolia\u2019s president quits  •  Bolsonaro in hospital  •  EU \u20ac8bn for Ukraine",
       font=font(FR, 20), fill=(255, 255, 255))

img.save(OUT, "PNG", optimize=True)
print("wrote", OUT)
