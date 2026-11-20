#!/usr/bin/env python3
"""Draw "THE WORLD — THURSDAY, 19 NOVEMBER 2026", a one-page newspaper poster.

Deterministic PIL drawing: no external assets, no randomness. Output: entry.png (1024x1024).
All stories are real, dated 19 Nov 2026, verified against news reports of the day.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 24  # outer margin
PAPER = (247, 242, 231)
INK = (26, 26, 26)
RED = (176, 42, 30)
NAVY = (29, 58, 110)
GOLD = (180, 140, 30)
GREY = (92, 88, 80)
LIGHT = (232, 224, 205)
SKY = (168, 200, 226)
SEA = (86, 140, 180)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def F(path, size):
    return ImageFont.truetype(path, size)


def tw(text, font):
    return d.textlength(text, font=font)


def fit(text, path, size, max_w):
    """Shrink font size until text fits max_w."""
    while size > 7 and tw(text, F(path, size)) > max_w:
        size -= 1
    return F(path, size)


def wrap(text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if tw(trial, font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(x, y, text, font, max_w, leading, fill=INK, max_lines=None):
    lines = wrap(text, font, max_w)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


def rule(x0, x1, y, wdt=1, fill=INK):
    d.line([(x0, y), (x1, y)], fill=fill, width=wdt)


def kicker(x, y, text, fill=RED):
    d.text((x, y), text, font=F(SANS_B, 10), fill=fill)


# ---------------------------------------------------------------- illustrations
def illo_courthouse(x, y, w, h):
    """Peace Palace style courthouse with columns, pediment and scales."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 222, 232), outline=INK, width=1)
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(150, 160, 140))
    cx = x + w // 2 - 40
    bw = 260
    bx0, bx1 = cx - bw // 2, cx + bw // 2
    base_y = y + h - 16
    d.rectangle([bx0 - 14, base_y, bx1 + 14, base_y + 6], fill=(150, 140, 120), outline=INK)
    d.rectangle([bx0 - 6, base_y - 6, bx1 + 6, base_y], fill=(170, 160, 140), outline=INK)
    col_top = y + 40
    d.rectangle([bx0 + 8, col_top, bx1 - 8, base_y - 6], fill=(206, 188, 164))
    for i in range(7):
        cxp = bx0 + 24 + i * ((bw - 48) // 6)
        d.rectangle([cxp - 6, col_top, cxp + 6, base_y - 6], fill=(238, 232, 218), outline=INK)
    d.polygon([(bx0 - 8, col_top), (bx1 + 8, col_top), (cx, y + 8)], fill=(196, 84, 62), outline=INK)
    d.ellipse([cx - 8, y + 24, cx + 8, y + 40], fill=(247, 242, 231), outline=INK)
    d.rectangle([cx - 10, y + 2, cx + 10, y + 10], fill=(196, 84, 62), outline=INK)
    d.rectangle([cx - 14, col_top + 8, cx + 14, base_y - 6], fill=(120, 100, 80), outline=INK)
    # scales of justice, right side, larger
    sx, sy = x + w - 78, y + 30
    d.line([(sx, sy), (sx, sy + 56)], fill=INK, width=4)
    d.line([(sx - 34, sy + 8), (sx + 34, sy + 8)], fill=INK, width=4)
    d.ellipse([sx - 5, sy - 6, sx + 5, sy + 4], fill=GOLD, outline=INK)
    for px in (sx - 34, sx + 34):
        d.line([(px, sy + 8), (px - 11, sy + 30)], fill=INK, width=2)
        d.line([(px, sy + 8), (px + 11, sy + 30)], fill=INK, width=2)
        d.arc([px - 14, sy + 20, px + 14, sy + 42], 0, 180, fill=INK, width=3)
    d.line([(sx - 16, sy + 56), (sx + 16, sy + 56)], fill=INK, width=4)


def illo_flags(x, y, w, h):
    """Three flags: USA, China, Russia."""
    d.rectangle([x, y, x + w, y + h], fill=SKY, outline=INK, width=1)
    fw, fh = (w - 24) // 3, h - 26
    for i in range(3):
        fx = x + 8 + i * (fw + 4)
        d.line([(fx, y + 6), (fx, y + h - 4)], fill=INK, width=2)
        if i == 0:  # USA simplified
            for r in range(7):
                d.rectangle([fx + 2, y + 8 + r * (fh // 7), fx + fw, y + 8 + (r + 1) * (fh // 7)],
                            fill=(200, 60, 60) if r % 2 == 0 else (245, 245, 245))
            d.rectangle([fx + 2, y + 8, fx + fw // 2, y + 8 + fh // 2], fill=NAVY)
            for r in range(3):
                for c in range(4):
                    px = fx + 6 + c * 7
                    py = y + 12 + r * 7
                    d.ellipse([px, py, px + 3, py + 3], fill=(255, 255, 255))
        elif i == 1:  # China
            d.rectangle([fx + 2, y + 8, fx + fw, y + 8 + fh], fill=(204, 34, 34))
            d.ellipse([fx + 8, y + 14, fx + 18, y + 24], fill=(250, 210, 60))
            for dx, dy in ((22, 12), (26, 18), (26, 26), (22, 30)):
                d.ellipse([fx + dx, y + dy, fx + dx + 4, y + dy + 4], fill=(250, 210, 60))
        else:  # Russia
            third = fh // 3
            d.rectangle([fx + 2, y + 8, fx + fw, y + 8 + third], fill=(245, 245, 245))
            d.rectangle([fx + 2, y + 8 + third, fx + fw, y + 8 + 2 * third], fill=(40, 90, 180))
            d.rectangle([fx + 2, y + 8 + 2 * third, fx + fw, y + 8 + fh], fill=(200, 50, 50))


def illo_gta(x, y, w, h):
    """Vice-city skyline at sunset with palm tree."""
    for i in range(h):
        t = i / h
        col = (int(250 - 60 * t), int(150 - 40 * t), int(90 + 60 * t))
        d.line([(x, y + i), (x + w, y + i)], fill=col)
    d.ellipse([x + w - 34, y + 8, x + w - 8, y + 34], fill=(255, 220, 120))
    heights = [0.45, 0.7, 0.55, 0.85, 0.6, 0.75]
    bw = w // 6
    for i, hf in enumerate(heights):
        bx = x + i * bw + 2
        by = y + h - int(h * hf)
        d.rectangle([bx, by, bx + bw - 4, y + h], fill=(40, 34, 60))
        for wy in range(by + 6, y + h - 6, 10):
            for wx in range(bx + 4, bx + bw - 8, 8):
                if (wx + wy) % 3 == 0:
                    d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 230, 150))
    # palm
    px = x + 16
    d.line([(px, y + h), (px + 8, y + 22)], fill=(60, 40, 30), width=3)
    for dx, dy in ((-16, -6), (-8, -12), (4, -14), (14, -8), (18, 0)):
        d.line([(px + 8, y + 22), (px + 8 + dx, y + 22 + dy)], fill=(34, 120, 60), width=3)
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def illo_parliament(x, y, w, h):
    """Parliament dome building."""
    d.rectangle([x, y, x + w, y + h], fill=(220, 228, 216), outline=INK, width=1)
    cx = x + w // 2
    base_y = y + h - 8
    d.rectangle([x + 10, base_y - 26, x + w - 10, base_y], fill=(200, 190, 170), outline=INK)
    for i in range(6):
        cxp = x + 20 + i * ((w - 40) // 5)
        d.rectangle([cxp - 3, base_y - 24, cxp + 3, base_y - 2], fill=(240, 236, 224), outline=INK)
    d.pieslice([cx - 30, y + 8, cx + 30, y + 52], 180, 360, fill=(90, 140, 110), outline=INK)
    d.line([(cx, y + 4), (cx, y + 12)], fill=INK, width=2)
    d.polygon([(cx, y + 4), (cx + 14, y + 7), (cx, y + 10)], fill=RED)


def illo_chart(x, y, w, h, up=True, label=""):
    d.rectangle([x, y, x + w, y + h], fill=(250, 250, 248), outline=INK, width=1)
    pts = []
    n = 7
    for i in range(n):
        px = x + 8 + i * ((w - 16) // (n - 1))
        frac = i / (n - 1)
        py = y + h - 10 - int((h - 24) * (frac if up else 1 - frac)) - (6 if i % 2 else 0)
        pts.append((px, py))
    col = (30, 140, 60) if up else RED
    d.line(pts, fill=col, width=3)
    ex, ey = pts[-1]
    if up:
        d.polygon([(ex, ey - 8), (ex - 5, ey + 2), (ex + 5, ey + 2)], fill=col)
    else:
        d.polygon([(ex, ey + 8), (ex - 5, ey - 2), (ex + 5, ey - 2)], fill=col)
    if label:
        d.text((x + 6, y + 4), label, font=F(SANS_B, 11), fill=col)


def illo_bridge(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY, outline=INK, width=1)
    d.rectangle([x, y + h - 16, x + w, y + h], fill=SEA)
    deck_y = y + h - 26
    d.rectangle([x + 4, deck_y, x + w // 2 - 8, deck_y + 5], fill=(90, 90, 90), outline=INK)
    d.rectangle([x + w // 2 + 12, deck_y + 4, x + w - 4, deck_y + 9], fill=(90, 90, 90), outline=INK)
    for px in (x + 18, x + w - 22):
        d.rectangle([px, y + 10, px + 5, deck_y], fill=(110, 110, 110), outline=INK)
    d.line([(x + 20, y + 12), (x + w // 2 - 8, deck_y)], fill=INK, width=1)
    d.line([(x + w - 20, y + 12), (x + w // 2 + 12, deck_y + 4)], fill=INK, width=1)
    # blast star at the break
    bx, by = x + w // 2 + 2, deck_y - 2
    for dx, dy in ((0, -14), (10, -10), (14, 0), (10, 10), (0, 14), (-10, 10), (-14, 0), (-10, -10)):
        d.line([(bx, by), (bx + dx, by + dy)], fill=(240, 140, 30), width=3)
    d.ellipse([bx - 5, by - 5, bx + 5, by + 5], fill=(255, 200, 60), outline=RED)


def illo_flame(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(250, 238, 220), outline=INK, width=1)
    cx = x + w // 2
    d.polygon([(cx, y + 6), (cx + 16, y + h - 14), (cx - 16, y + h - 14)], fill=(240, 120, 30))
    d.polygon([(cx, y + 22), (cx + 10, y + h - 14), (cx - 10, y + h - 14)], fill=(250, 180, 50))
    d.polygon([(cx, y + 36), (cx + 5, y + h - 14), (cx - 5, y + h - 14)], fill=(255, 230, 140))
    d.rectangle([x + 8, y + h - 14, x + w - 8, y + h - 8], fill=(90, 70, 50))


def illo_shield(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(224, 232, 244), outline=INK, width=1)
    cx = x + w // 2
    d.polygon([(cx - 20, y + 8), (cx + 20, y + 8), (cx + 20, y + h - 26), (cx, y + h - 8),
               (cx - 20, y + h - 26)], fill=NAVY, outline=INK)
    d.polygon([(cx - 14, y + 14), (cx + 14, y + 14), (cx + 14, y + h - 30), (cx, y + h - 16),
               (cx - 14, y + h - 30)], fill=(60, 110, 190))
    d.ellipse([cx - 6, y + 22, cx + 6, y + 34], fill=(250, 210, 60), outline=INK)


def illo_greenland(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SEA, outline=INK, width=1)
    cx, cy = x + w // 2 - 8, y + h // 2
    pts = [(cx - 18, cy - 20), (cx + 4, cy - 26), (cx + 20, cy - 12), (cx + 14, cy + 8),
           (cx + 4, cy + 24), (cx - 8, cy + 18), (cx - 20, cy + 2)]
    d.polygon(pts, fill=(245, 248, 250), outline=INK)
    # Danish flag
    fx, fy = x + w - 30, y + 8
    d.rectangle([fx, fy, fx + 22, fy + 16], fill=(200, 30, 40), outline=INK)
    d.rectangle([fx + 6, fy, fx + 9, fy + 16], fill=(255, 255, 255))
    d.rectangle([fx, fy + 6, fx + 22, fy + 9], fill=(255, 255, 255))


def illo_leaf(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 240, 222), outline=INK, width=1)
    cx, cy = x + w // 2 - 10, y + h // 2
    d.ellipse([cx - 18, cy - 22, cx + 18, cy + 22], fill=(60, 160, 80), outline=INK)
    d.line([(cx - 12, cy + 18), (cx + 12, cy - 18)], fill=(30, 100, 50), width=2)
    # thermometer
    tx = x + w - 22
    d.rectangle([tx, y + 8, tx + 8, y + h - 18], fill=(255, 255, 255), outline=INK)
    d.rectangle([tx + 2, y + 22, tx + 6, y + h - 18], fill=RED)
    d.ellipse([tx - 3, y + h - 22, tx + 11, y + h - 8], fill=RED, outline=INK)


def illo_dove(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 240, 246), outline=INK, width=1)
    cx, cy = x + w // 2, y + h // 2 + 4
    d.ellipse([cx - 24, cy - 8, cx + 16, cy + 12], fill=(255, 255, 255), outline=INK)
    d.ellipse([cx + 10, cy - 16, cx + 26, cy - 2], fill=(255, 255, 255), outline=INK)
    d.polygon([(cx + 24, cy - 10), (cx + 34, cy - 7), (cx + 24, cy - 4)], fill=(240, 170, 40))
    d.ellipse([cx + 16, cy - 12, cx + 20, cy - 8], fill=INK)
    d.polygon([(cx - 22, cy - 2), (cx - 36, cy - 12), (cx - 30, cy + 4)], fill=(255, 255, 255), outline=INK)
    d.arc([cx - 14, cy - 18, cx + 8, cy + 2], 200, 340, fill=INK, width=2)
    # olive branch
    d.line([(cx + 26, cy - 4), (cx + 38, cy + 4)], fill=(60, 140, 70), width=2)
    for dx, dy in ((30, 0), (34, 2), (32, 6)):
        d.ellipse([cx + dx, cy + dy, cx + dx + 6, cy + dy + 4], fill=(60, 140, 70))


def illo_painting(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 232, 214), outline=INK, width=1)
    d.rectangle([x + 8, y + 8, x + w - 8, y + h - 8], fill=(30, 40, 110), outline=GOLD, width=3)
    for i, (dx, dy, r) in enumerate(((24, 20, 7), (46, 14, 5), (62, 26, 6), (34, 34, 4), (56, 42, 5))):
        d.ellipse([x + dx - r, y + dy - r, x + dx + r, y + dy + r], fill=(250, 220, 90))
        d.arc([x + dx - r - 4, y + dy - r - 4, x + dx + r + 4, y + dy + r + 4], 0, 360, fill=(140, 170, 240), width=2)
    d.arc([x + 14, y + h - 30, x + w - 14, y + h + 6], 180, 360, fill=(90, 140, 220), width=3)


# ---------------------------------------------------------------- masthead
rule(M, W - M, 14, 1)
rule(M, W - M, 18, 3)
mast = F(SERIF_B, 60)
d.text(((W - tw("THE WORLD", mast)) / 2, 24), "THE WORLD", font=mast, fill=INK)
d.text((M, 90), "Vol. I — No. 3", font=F(SANS, 11), fill=GREY)
dateline = "THURSDAY, 19 NOVEMBER 2026"
dfont = F(SANS_B, 22)
d.text(((W - tw(dateline, dfont)) / 2, 84), dateline, font=dfont, fill=RED)
rtext = "THURSDAY EDITION"
d.text((W - M - tw(rtext, F(SANS, 11)), 90), rtext, font=F(SANS, 11), fill=GREY)
rule(M, W - M, 112, 2)

# ---------------------------------------------------------------- lead story
LX, LW = M, 600
kicker(LX, 120, "THE HAGUE — INTERNATIONAL COURT OF JUSTICE")
head = fit("WORLD COURT FINDS MYANMAR", SERIF_B, 34, LW)
d.text((LX, 134), "WORLD COURT FINDS MYANMAR", font=head, fill=INK)
d.text((LX, 170), "GUILTY OF GENOCIDE", font=head, fill=INK)
illo_courthouse(LX, 210, LW, 104)
d.text((LX, 318), "The Peace Palace, seat of the ICJ. The 9–6 ruling is the first against a state.",
        font=F(SERIF_I, 11), fill=GREY)
lead_body = ("In a judgment read over three hours, the court held Myanmar responsible for genocide "
             "against the Rohingya in its 2017 “clearance operations” — the first such finding "
             "against a state in the court's 80-year history. Myanmar must report within two years "
             "on restitution and compensation for some 400 destroyed villages. The Gambia brought "
             "the case in 2019.")
text_block(LX, 334, lead_body, F(SANS, 12.5), LW, 16, max_lines=4)

# ---------------------------------------------------------------- right rail
RX, RW = 640, 360
d.line([(632, 120), (632, 400)], fill=INK, width=1)


def rail_story(y, kick, headline, body, illo):
    kicker(RX, y, kick)
    hf = fit(headline, SERIF_B, 17, RW - 104)
    lines = wrap(headline, hf, RW - 104)[:2]
    yy = y + 14
    for ln in lines:
        d.text((RX + 104, yy), ln, font=hf, fill=INK)
        yy += 20
    illo(RX, y + 14, 96, 66)
    text_block(RX + 104, yy + 2, body, F(SANS, 11), RW - 104, 14, max_lines=3)


rail_story(120, "SHENZHEN — APEC SUMMIT", "Three leaders, one table",
           "Trump, Xi and Putin held their first three-way summit and issued a “peace declaration”.",
           illo_flags)
rule(RX, W - M, 216, 1, GREY)
rail_story(224, "LOS ANGELES — GAMING", "GTA VI: $2.36B launch day",
           "An estimated 24.6M copies sold on day one (Sensor Tower), doubling GTA V's record; Metascore 99.",
           illo_gta)
rule(RX, W - M, 320, 1, GREY)
rail_story(328, "JAKARTA — PARLIAMENT", "Asset-forfeiture bill passed",
           "Parliament approved seizing assets without a prior criminal conviction, via court proceedings.",
           illo_parliament)

rule(M, W - M, 406, 2)

# ---------------------------------------------------------------- story grid
grid = [
    ("NEW YORK — MARKETS", "Anthropic's $1.5T debut",
     "Priced at $83, it closed day one at $97.17 (+17%) despite a sell-off.",
     lambda x, y, w, h: illo_chart(x, y, w, h, True, "$97.17")),
    ("NEW YORK — MARKETS", "Stocks slide on AI nerves",
     "S&P 500 fell 2.02%, a fifth straight loss; Nikkei −4.68%, gold −2.42%.",
     lambda x, y, w, h: illo_chart(x, y, w, h, False, "−2.02%")),
    ("KYIV — WAR IN UKRAINE", "Bridge hit a third time",
     "Ukraine hit the Crimean Bridge a third time in four days; Putin vowed revenge.",
     illo_bridge),
    ("DHAKA — BANGLADESH", "Yunus home torched",
     "Arson swept 28 districts; the interim leader's ancestral home was ablaze.",
     illo_flame),
    ("PORT-AU-PRINCE — HAITI", "34 gang members killed",
     "Police killed at least 34 alleged gang members in the capital.",
     illo_shield),
    ("COPENHAGEN — GREENLAND", "Greenland deal ratified 109–0",
     "Denmark's Folketing unanimously approved the US Greenland security deal.",
     illo_greenland),
    ("ANTALYA — COP31", "Ministers hunt a deal",
     "Negotiators worked late to unblock the climate text in the final stretch.",
     illo_leaf),
    ("GAZA CITY — MIDDLE EAST", "Peace plan scores 4 of 26",
     "Aid groups rated the 20-point plan 4/26 as evacuation orders hit Gaza.",
     illo_dove),
    ("NEW YORK — ART", "Van Gogh record: $190.4M",
     "“Châtaigniers en fleurs” (1890) set an artist record at Sotheby's.",
     illo_painting),
]

GX0, GY0 = M, 414
COLW, ROWH, GAPX, GAPY = 317, 82, 12, 5
for i, (kick, headline, body, illo) in enumerate(grid):
    cx = GX0 + (i % 3) * (COLW + GAPX)
    cy = GY0 + (i // 3) * (ROWH + GAPY)
    illo(cx, cy + 14, 84, 58)
    kicker(cx, cy, kick)
    hf = fit(headline, SERIF_B, 15, COLW - 92)
    lines = wrap(headline, hf, COLW - 92)[:2]
    yy = cy + 14
    for ln in lines:
        d.text((cx + 92, yy), ln, font=hf, fill=INK)
        yy += 17
    text_block(cx + 92, yy + 1, body, F(SANS, 10.5), COLW - 92, 12.5, max_lines=3)

GY1 = GY0 + 3 * ROWH + 2 * GAPY  # 414 + 268 = 682
rule(M, W - M, GY1 + 8, 2)

# ---------------------------------------------------------------- flashpoints
FY = GY1 + 16
d.text((M, FY), "FLASHPOINTS — WHERE THE DAY HAPPENED", font=F(SANS_B, 13), fill=RED)
places = ["THE HAGUE", "SHENZHEN", "KYIV", "GAZA CITY", "DHAKA", "PORT-AU-PRINCE",
          "COPENHAGEN", "ANTALYA", "JAKARTA", "YONGYON", "SUVA", "YENNE"]
pf = F(SANS_B, 12)
for r in range(2):
    yy = FY + 22 + r * 20
    xx = M
    for p in places[r * 6:(r + 1) * 6]:
        d.ellipse([xx, yy + 3, xx + 8, yy + 11], fill=RED)
        d.text((xx + 13, yy), p, font=pf, fill=INK)
        xx += 13 + tw(p, pf) + 26

# ---------------------------------------------------------------- by the numbers
NY = FY + 68
rule(M, W - M, NY, 1, GREY)
d.text((M, NY + 6), "BY THE NUMBERS", font=F(SANS_B, 13), fill=RED)
numbers = [
    ("9–6", "ICJ vote holding Myanmar\nresponsible for genocide"),
    ("$2.36B", "GTA VI day-one sales,\nestimated (Sensor Tower)"),
    ("51–48", "US Senate vote rejecting\nthe Iran war-powers bid"),
    ("356,000", "people displaced in Yemen\nin 3½ months (IOM)"),
    ("589M", "children in conflict\nzones in 2025 (23.4%)"),
]
BW = (W - 2 * M - 4 * 10) // 5
for i, (num, label) in enumerate(numbers):
    bx = M + i * (BW + 10)
    d.rectangle([bx, NY + 26, bx + BW, NY + 80], outline=INK, width=1)
    nf = fit(num, SERIF_B, 26, BW - 10)
    d.text((bx + (BW - tw(num, nf)) / 2, NY + 30), num, font=nf, fill=NAVY)
    ly = NY + 58
    for ln in label.split("\n"):
        d.text((bx + (BW - tw(ln, F(SANS, 9))) / 2, ly), ln, font=F(SANS, 9), fill=GREY)
        ly += 11

# ---------------------------------------------------------------- pull-quote
QY = NY + 88
quote = "“The only reasonable inference is an intention to destroy.”"
qf = F(SERIF_I, 17)
d.text(((W - tw(quote, qf)) / 2, QY), quote, font=qf, fill=INK)
attrib = "— Judge Yuji Iwasawa, ICJ President, on Myanmar's actions in Rakhine"
af = F(SANS, 10)
d.text(((W - tw(attrib, af)) / 2, QY + 24), attrib, font=af, fill=GREY)

# ---------------------------------------------------------------- in brief
BY = QY + 42
rule(M, W - M, BY, 2)
d.text((M, BY + 6), "IN BRIEF", font=F(SANS_B, 13), fill=RED)
brief = [
    "US Senate rejects Iran war-powers bid, 51–48",
    "UK + Norway pledge £100M+ for Ukrainian naval craft",
    "Serbia: Cupic elected parliament speaker, 140 votes",
    "589M children lived in conflict zones in 2025",
    "Fiji declares disaster over El Niño drought",
    "Yemen: 356,000 displaced in 3½ months — IOM",
    "Dozens missing as migrant boat capsizes off Senegal",
    "IAEA: North Korea expands uranium enrichment",
    "Pakistan: 22 militants killed in Khyber raids",
    "Iraq orders Kataib Hezbollah out of Jurf al-Nasr",
    "Spain's Sánchez admits mistakes in TV debate",
    "Voyager 1 now one light-day from Earth",
    "BepiColombo enters orbit around Mercury",
    "EU Commission confirms AI-tool cyberattack",
    "Kuwait repels first Iranian attack in two months",
    "IEA: Hormuz crisis a record energy threat",
    "APEC adopts Shenzhen Outlook on trade & AI",
    "Philippines and Chile sign free-trade deal",
    "EU–Mexico to scrap 95% of farm tariffs",
    "Hunger Games prequel premieres in Brazil",
    "India drop Siraj for first Test v New Zealand",
    "Trump pardons baseball's Pete Rose posthumously",
    "Democrats pick Jeffries for speaker, 251–11",
    "US and Venezuela sign military pact",
]
bf = F(SANS, 9.5)
BCOLW = (W - 2 * M - 2 * 16) // 3
for c in range(3):
    cx = M + c * (BCOLW + 16)
    yy = BY + 26
    for item in brief[c * 8:(c + 1) * 8]:
        d.ellipse([cx, yy + 4, cx + 5, yy + 9], fill=RED)
        line = wrap(item, bf, BCOLW - 12)[0]
        d.text((cx + 11, yy), line, font=bf, fill=INK)
        yy += 11.5

# ---------------------------------------------------------------- footer
foot = "THE WORLD • THURSDAY, 19 NOVEMBER 2026 • 37 stories • 30+ countries • Also inside: markets p.2, weather p.3, sport p.4"
ff = F(SANS, 9)
d.text(((W - tw(foot, ff)) / 2, H - 14), foot, font=ff, fill=GREY)

img.save("entry.png", optimize=True)
print("wrote entry.png")
