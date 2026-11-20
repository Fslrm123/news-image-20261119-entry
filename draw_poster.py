#!/usr/bin/env python3
"""The World — front page poster for Thursday, 19 November 2026.

Deterministic PIL-only rendering, 1024x1024. Refined broadsheet style:
disciplined grid, hairline rules, warm paper, near-black ink, one muted
red accent, navy numerals.
"""

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- palette
PAPER = (250, 246, 236)
INK = (26, 24, 22)
RED = (163, 44, 38)
NAVY = (31, 58, 95)
GREY = (96, 92, 86)
HAIR = (120, 114, 104)
SAND = (216, 200, 162)
SKY = (172, 192, 208)
SAGE = (142, 162, 132)
CREAM = (244, 238, 222)
GOLD = (201, 162, 39)
ORANGE = (214, 116, 44)
NIGHT = (36, 48, 92)

# ---------------------------------------------------------------- fonts
PIRATA = "fonts/PirataOne-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

W = H = 1024
MX = 36                      # side margin
CW = W - 2 * MX              # content width = 952


def F(path, size):
    return ImageFont.truetype(path, size)


# ---------------------------------------------------------------- helpers
def wrap(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, x, y, lines, font, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def spaced_width(draw, text, font, spacing):
    return sum(draw.textlength(ch, font=font) + spacing for ch in text) - spacing


def draw_spaced(draw, x, y, text, font, fill, spacing=1.4):
    cx = x
    for ch in text:
        draw.text((cx, y), ch, font=font, fill=fill)
        cx += draw.textlength(ch, font=font) + spacing
    return cx


def hrule(draw, x0, x1, y, width=1, fill=HAIR):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def illo_box(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=CREAM, outline=HAIR, width=1)


# ---------------------------------------------------------------- illustrations
def illo_courthouse(draw, x, y, w, h):
    illo_box(draw, x, y, w, h)
    cx = x + w / 2
    base_y = y + h - 14
    # sun disc behind pediment
    r = h * 0.20
    draw.ellipse([cx - r, y + 8, cx + r, y + 8 + 2 * r], fill=(238, 214, 150))
    # pediment
    pw = w * 0.46
    draw.polygon([(cx - pw / 2, y + h * 0.30), (cx + pw / 2, y + h * 0.30),
                  (cx, y + h * 0.06)], fill=SAND, outline=INK, width=2)
    # entablature
    draw.rectangle([cx - pw / 2, y + h * 0.30, cx + pw / 2, y + h * 0.38],
                   fill=SAND, outline=INK, width=2)
    # columns
    n = 5
    col_top = y + h * 0.38
    col_bot = base_y - 6
    for i in range(n):
        cxx = cx - pw / 2 + (i + 0.5) * (pw / n)
        draw.rectangle([cxx - 4, col_top, cxx + 4, col_bot], fill=(252, 250, 244),
                       outline=INK, width=1)
    # steps
    draw.rectangle([cx - pw / 2 - 10, base_y - 6, cx + pw / 2 + 10, base_y],
                   fill=SAND, outline=INK, width=1)
    draw.rectangle([cx - pw / 2 - 18, base_y, cx + pw / 2 + 18, base_y + 6],
                   fill=SAND, outline=INK, width=1)
    # scales of justice in front centre
    sy = y + h * 0.44
    draw.line([(cx, sy), (cx, base_y - 10)], fill=INK, width=2)
    draw.line([(cx - 34, sy + 4), (cx + 34, sy + 4)], fill=INK, width=2)
    draw.ellipse([cx - 3, sy - 4, cx + 3, sy + 2], fill=INK)
    for sx in (cx - 34, cx + 34):
        draw.line([(sx, sy + 4), (sx - 10, sy + 20)], fill=INK, width=1)
        draw.line([(sx, sy + 4), (sx + 10, sy + 20)], fill=INK, width=1)
        draw.arc([sx - 12, sy + 14, sx + 12, sy + 30], 0, 180, fill=INK, width=2)
    draw.line([(cx - 10, base_y - 10), (cx + 10, base_y - 10)], fill=INK, width=2)


def illo_flags(draw, x, y, w, h):
    illo_box(draw, x, y, w, h)
    cols = [RED, NAVY, (120, 130, 140)]
    base_y = y + h - 8
    fw = w * 0.30
    for i, col in enumerate(cols):
        px = x + 8 + i * (w * 0.55) / 2
        draw.line([(px, y + 8), (px, base_y)], fill=INK, width=2)
        draw.polygon([(px, y + 9), (px + fw, y + 13), (px + fw, y + 26),
                      (px, y + 30)], fill=col, outline=INK, width=1)
    draw.line([(x + 6, base_y), (x + w - 6, base_y)], fill=INK, width=2)


def illo_skyline(draw, x, y, w, h):
    illo_box(draw, x, y, w, h)
    # sunset
    r = h * 0.26
    draw.ellipse([x + w * 0.62 - r, y + h * 0.18, x + w * 0.62 + r, y + h * 0.18 + 2 * r],
                 fill=ORANGE)
    base_y = y + h - 8
    heights = [0.42, 0.62, 0.34, 0.72, 0.5, 0.38]
    bw = w / len(heights)
    for i, hf in enumerate(heights):
        bx = x + i * bw + 2
        draw.rectangle([bx, base_y - h * hf, bx + bw - 4, base_y], fill=INK)
        for wy in range(3):
            for wx in range(2):
                if (i + wy + wx) % 2 == 0:
                    draw.rectangle([bx + 3 + wx * 5, base_y - h * hf + 4 + wy * 7,
                                    bx + 6 + wx * 5, base_y - h * hf + 7 + wy * 7],
                                   fill=(246, 214, 120))
    # palm
    px = x + 10
    draw.line([(px, base_y), (px + 3, base_y - h * 0.5)], fill=INK, width=2)
    for dx, dy in [(-9, -4), (-5, -8), (3, -9), (9, -5)]:
        draw.line([(px + 3, base_y - h * 0.5), (px + 3 + dx, base_y - h * 0.5 + dy)],
                  fill=SAGE, width=2)


def illo_dome(draw, x, y, w, h):
    illo_box(draw, x, y, w, h)
    cx = x + w / 2
    base_y = y + h - 8
    bw = w * 0.72
    # building body
    draw.rectangle([cx - bw / 2, y + h * 0.55, cx + bw / 2, base_y],
                   fill=SAND, outline=INK, width=2)
    # drum + dome
    draw.rectangle([cx - bw * 0.28, y + h * 0.42, cx + bw * 0.28, y + h * 0.55],
                   fill=SAND, outline=INK, width=2)
    draw.pieslice([cx - bw * 0.30, y + h * 0.08, cx + bw * 0.30, y + h * 0.48],
                  180, 360, fill=SKY, outline=INK, width=2)
    # finial + flag
    draw.line([(cx, y + h * 0.08), (cx, y + 3)], fill=INK, width=2)
    draw.polygon([(cx, y + 3), (cx + 9, y + 6), (cx, y + 10)], fill=RED)
    # columns + door
    for i in range(4):
        cxx = cx - bw / 2 + (i + 0.5) * (bw / 4)
        draw.line([(cxx, y + h * 0.58), (cxx, base_y - 2)], fill=INK, width=1)
    draw.rectangle([cx - 4, base_y - h * 0.18, cx + 4, base_y], fill=INK)


def illo_chart(draw, x, y, w, h, up=True, label=""):
    illo_box(draw, x, y, w, h)
    ax, ay = x + 8, y + h - 10
    draw.line([(ax, y + 6), (ax, ay)], fill=INK, width=1)
    draw.line([(ax, ay), (x + w - 6, ay)], fill=INK, width=1)
    if up:
        pts = [(ax + 3, ay - 4), (ax + w * 0.3, ay - h * 0.3),
               (ax + w * 0.55, ay - h * 0.22), (x + w - 12, y + 10)]
        col = NAVY
    else:
        pts = [(ax + 3, y + 10), (ax + w * 0.3, y + h * 0.35),
               (ax + w * 0.55, y + h * 0.28), (x + w - 12, ay - 5)]
        col = RED
    draw.line(pts, fill=col, width=2)
    ex, ey = pts[-1]
    draw.polygon([(ex, ey), (ex - 7, ey + (2 if up else -2)), (ex - 2, ey + (7 if up else -7))],
                 fill=col)
    if label:
        f = F(SANS_B, 9)
        tw = draw.textlength(label, font=f)
        draw.text((x + w - 6 - tw, y + 4 if up else y + h - 22), label, font=f, fill=col)


def illo_bridge(draw, x, y, w, h):
    illo_box(draw, x, y, w, h)
    deck_y = y + h * 0.62
    t1, t2 = x + w * 0.25, x + w * 0.75
    for tx in (t1, t2):
        draw.rectangle([tx - 3, y + 8, tx + 3, deck_y + 6], fill=INK)
    draw.line([(x + 4, deck_y), (x + w - 4, deck_y)], fill=INK, width=3)
    # cables
    draw.line([(x + 4, deck_y), (t1, y + 10)], fill=INK, width=1)
    draw.line([(t1, y + 10), ((t1 + t2) / 2, deck_y - 2)], fill=INK, width=1)
    draw.line([((t1 + t2) / 2, deck_y - 2), (t2, y + 10)], fill=INK, width=1)
    draw.line([(t2, y + 10), (x + w - 4, deck_y)], fill=INK, width=1)
    # water
    for i in range(3):
        wy = deck_y + 10 + i * 5
        draw.line([(x + 8 + i * 6, wy), (x + w - 8 - i * 4, wy)], fill=SKY, width=1)
    # blast starburst at centre of deck
    bx, by = (t1 + t2) / 2, deck_y - 4
    for dx, dy in [(0, -12), (8, -8), (12, 0), (8, 6), (-8, 6), (-12, 0), (-8, -8)]:
        draw.line([(bx, by), (bx + dx, by + dy)], fill=ORANGE, width=2)
    draw.ellipse([bx - 4, by - 4, bx + 4, by + 4], fill=RED)


def illo_flame(draw, x, y, w, h):
    illo_box(draw, x, y, w, h)
    cx = x + w / 2
    base_y = y + h - 10
    # outer flame
    draw.polygon([(cx, y + 6), (cx + w * 0.20, y + h * 0.42),
                  (cx + w * 0.16, base_y), (cx - w * 0.16, base_y),
                  (cx - w * 0.20, y + h * 0.42)], fill=ORANGE, outline=RED, width=1)
    # inner flame
    draw.polygon([(cx, y + h * 0.34), (cx + w * 0.10, y + h * 0.58),
                  (cx + w * 0.08, base_y), (cx - w * 0.08, base_y),
                  (cx - w * 0.10, y + h * 0.58)], fill=(246, 196, 84))
    # logs
    draw.line([(cx - w * 0.24, base_y + 3), (cx + w * 0.24, base_y + 3)], fill=INK, width=3)
    draw.line([(cx - w * 0.18, base_y + 6), (cx + w * 0.18, base_y + 6)], fill=INK, width=3)


def illo_shield(draw, x, y, w, h):
    illo_box(draw, x, y, w, h)
    cx = x + w / 2
    top = y + 8
    bot = y + h - 8
    hw = w * 0.30
    draw.polygon([(cx - hw, top), (cx + hw, top), (cx + hw, top + h * 0.42),
                  (cx, bot), (cx - hw, top + h * 0.42)],
                 fill=NAVY, outline=INK, width=2)
    # star
    sx, sy = cx, top + h * 0.30
    pts = []
    import math
    for i in range(10):
        r = 9 if i % 2 == 0 else 4
        a = -math.pi / 2 + i * math.pi / 5
        pts.append((sx + r * math.cos(a), sy + r * math.sin(a)))
    draw.polygon(pts, fill=(246, 214, 120))


def illo_greenland(draw, x, y, w, h):
    illo_box(draw, x, y, w, h)
    # stylised Greenland landmass
    gx, gy = x + 8, y + 8
    gw, gh = w * 0.58, h - 16
    pts = [(gx + gw * 0.30, gy), (gx + gw * 0.72, gy + gh * 0.08),
           (gx + gw * 0.95, gy + gh * 0.30), (gx + gw * 0.88, gy + gh * 0.55),
           (gx + gw * 0.62, gy + gh * 0.78), (gx + gw * 0.45, gy + gh),
           (gx + gw * 0.30, gy + gh * 0.80), (gx + gw * 0.08, gy + gh * 0.55),
           (gx + gw * 0.12, gy + gh * 0.25)]
    draw.polygon(pts, fill=SAGE, outline=INK, width=2)
    # Danish flag
    fx = x + w * 0.70
    fy = y + h * 0.28
    fw, fh = w * 0.24, h * 0.34
    draw.rectangle([fx, fy, fx + fw, fy + fh], fill=RED, outline=INK, width=1)
    draw.rectangle([fx + fw * 0.30, fy, fx + fw * 0.44, fy + fh], fill=(252, 250, 244))
    draw.rectangle([fx, fy + fh * 0.42, fx + fw, fy + fh * 0.58], fill=(252, 250, 244))


def illo_leaf_thermo(draw, x, y, w, h):
    illo_box(draw, x, y, w, h)
    # leaf
    lx, ly = x + w * 0.30, y + h * 0.55
    draw.polygon([(lx - w * 0.20, ly + h * 0.22), (lx - w * 0.16, ly - h * 0.28),
                  (lx + w * 0.02, ly - h * 0.38), (lx + w * 0.20, ly - h * 0.10),
                  (lx + w * 0.16, ly + h * 0.20), (lx, ly + h * 0.30)],
                 fill=SAGE, outline=INK, width=2)
    draw.line([(lx - w * 0.18, ly + h * 0.24), (lx + w * 0.14, ly - h * 0.30)],
              fill=INK, width=1)
    # thermometer
    tx = x + w * 0.72
    draw.rounded_rectangle([tx - 4, y + 8, tx + 4, y + h - 16], radius=4,
                           fill=(252, 250, 244), outline=INK, width=2)
    draw.ellipse([tx - 8, y + h - 24, tx + 8, y + h - 8], fill=RED, outline=INK, width=2)
    draw.rectangle([tx - 2, y + h * 0.45, tx + 2, y + h - 16], fill=RED)


def illo_dove(draw, x, y, w, h):
    illo_box(draw, x, y, w, h)
    cx, cy = x + w * 0.48, y + h * 0.55
    # body
    draw.ellipse([cx - w * 0.26, cy - h * 0.14, cx + w * 0.20, cy + h * 0.20],
                 fill=(252, 250, 244), outline=INK, width=2)
    # head
    hx, hy = cx + w * 0.20, cy - h * 0.18
    draw.ellipse([hx - 7, hy - 7, hx + 7, hy + 7], fill=(252, 250, 244), outline=INK, width=2)
    draw.polygon([(hx + 6, hy), (hx + 13, hy + 2), (hx + 6, hy + 4)], fill=GOLD)
    draw.ellipse([hx + 1, hy - 3, hx + 4, hy], fill=INK)
    # wing
    draw.polygon([(cx - w * 0.16, cy - h * 0.08), (cx + w * 0.06, cy - h * 0.30),
                  (cx + w * 0.10, cy - h * 0.02)], fill=SKY, outline=INK, width=1)
    # tail
    draw.polygon([(cx - w * 0.24, cy), (cx - w * 0.38, cy - h * 0.10),
                  (cx - w * 0.36, cy + h * 0.10)], fill=(252, 250, 244), outline=INK, width=1)
    # olive branch in beak
    draw.line([(hx + 12, hy + 3), (hx + 22, hy + 9)], fill=SAGE, width=2)
    for dx, dy in [(16, 4), (20, 8), (15, 9)]:
        draw.ellipse([hx + dx - 3, hy + dy - 2, hx + dx + 3, hy + dy + 2], fill=SAGE)


def illo_starry(draw, x, y, w, h):
    illo_box(draw, x, y, w, h)
    # frame
    draw.rectangle([x + 6, y + 6, x + w - 6, y + h - 6], fill=NIGHT, outline=GOLD, width=3)
    # swirls
    for (sx, sy, r) in [(x + w * 0.35, y + h * 0.35, 12), (x + w * 0.62, y + h * 0.28, 9),
                        (x + w * 0.5, y + h * 0.5, 7)]:
        draw.arc([sx - r, sy - r * 0.7, sx + r, sy + r * 0.7], 20, 320, fill=SKY, width=2)
    # stars
    for (sx, sy) in [(x + w * 0.22, y + h * 0.22), (x + w * 0.78, y + h * 0.2),
                     (x + w * 0.85, y + h * 0.45), (x + w * 0.3, y + h * 0.55)]:
        draw.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=(246, 214, 120))
        draw.line([(sx - 5, sy), (sx + 5, sy)], fill=(246, 214, 120), width=1)
        draw.line([(sx, sy - 5), (sx, sy + 5)], fill=(246, 214, 120), width=1)
    # cypress
    cxp = x + w * 0.16
    draw.polygon([(cxp, y + h - 10), (cxp - 5, y + h * 0.45), (cxp, y + h * 0.25),
                  (cxp + 5, y + h * 0.45)], fill=(24, 40, 30))
    # hills
    draw.arc([x + 8, y + h * 0.55, x + w - 8, y + h + 14], 180, 360, fill=SAGE, width=2)


# ---------------------------------------------------------------- content
LEAD = dict(
    kicker="THE HAGUE — INTERNATIONAL COURT OF JUSTICE",
    headline=["WORLD COURT FINDS MYANMAR", "GUILTY OF GENOCIDE"],
    caption="The Peace Palace, seat of the ICJ. The 9–6 ruling is the first against a state.",
    body=("In a judgment read over three hours, the court held Myanmar responsible for "
          "genocide against the Rohingya in its 2017 “clearance operations” — the first "
          "such finding against a state in the court's 80-year history. Myanmar must "
          "report within two years on restitution and compensation for some 400 destroyed "
          "villages. The Gambia brought the case in 2019."),
)

RAIL = [
    ("SHENZHEN — APEC SUMMIT", "Three leaders, one table",
     "Trump, Xi and Putin held their first three-way summit and issued a “peace declaration”.",
     illo_flags),
    ("LOS ANGELES — GAMING", "GTA VI: $2.36B launch day",
     "An estimated 24.6M copies sold on day one (Sensor Tower), doubling GTA V's record; Metascore 99.",
     illo_skyline),
    ("JAKARTA — PARLIAMENT", "Asset-forfeiture bill passed",
     "Parliament approved seizing assets without a prior criminal conviction, via court proceedings.",
     illo_dome),
]

GRID = [
    ("NEW YORK — MARKETS", "Anthropic's $1.5T debut",
     "Priced at $83, it closed day one at $97.17 (+17%) despite a sell-off.",
     lambda d, x, y, w, h: illo_chart(d, x, y, w, h, up=True, label="$97.17")),
    ("NEW YORK — MARKETS", "Stocks slide on AI nerves",
     "S&P 500 fell 2.02%, a fifth straight loss; Nikkei −4.68%, gold −2.42%.",
     lambda d, x, y, w, h: illo_chart(d, x, y, w, h, up=False, label="−2.02%")),
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
     illo_leaf_thermo),
    ("GAZA CITY — MIDDLE EAST", "Peace plan scores 4 of 26",
     "Aid groups rated the 20-point plan 4/26 as evacuation orders hit Gaza.",
     illo_dove),
    ("NEW YORK — ART", "Van Gogh record: $190.4M",
     "“Châtaigniers en fleurs” (1890) set an artist record at Sotheby's.",
     illo_starry),
]

FLASHPOINTS = ["THE HAGUE", "SHENZHEN", "KYIV", "GAZA CITY", "DHAKA", "PORT-AU-PRINCE",
               "COPENHAGEN", "ANTALYA", "JAKARTA", "YONGYON", "SUVA", "YENNE"]

NUMBERS = [
    ("9–6", ["ICJ vote holding Myanmar", "responsible for genocide"]),
    ("$2.36B", ["GTA VI day-one sales,", "estimated (Sensor Tower)"]),
    ("51–48", ["US Senate vote rejecting", "the Iran war-powers bid"]),
    ("356,000", ["people displaced in Yemen", "in 3½ months (IOM)"]),
    ("589M", ["children in conflict", "zones in 2025 (23.4%)"]),
]

QUOTE = "“The only reasonable inference is an intention to destroy.”"
QUOTE_ATTR = "— Judge Yuji Iwasawa, ICJ President, on Myanmar's actions in Rakhine"

BRIEF = [
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

FOOTER = ("THE WORLD  •  THURSDAY, 19 NOVEMBER 2026  •  37 stories  •  30+ countries  •  "
          "Also inside: markets p.2, weather p.3, sport p.4")


# ---------------------------------------------------------------- render
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    f_mast = F(PIRATA, 68)
    f_date = F(SERIF_B, 22)
    f_vol = F(SERIF_I, 14)
    f_kick = F(SANS_B, 9)
    f_lead_h = F(SERIF_B, 35)
    f_cap = F(SERIF_I, 11)
    f_body = F(SANS, 10)
    f_rail_h = F(SERIF_B, 16)
    f_grid_h = F(SERIF_B, 15)
    f_sec = F(SANS_B, 11)
    f_num = F(SERIF_B, 27)
    f_num_lab = F(SANS, 9)
    f_quote = F(SERIF_I, 19)
    f_attr = F(SANS, 10)
    f_brief = F(SANS, 9)
    f_foot = F(SANS, 9)

    # ---- masthead
    d.text((MX, 18), "The World", font=f_mast, fill=INK)
    date = "THURSDAY, 19 NOVEMBER 2026"
    dw = d.textlength(date, font=f_date)
    d.text((W - MX - dw, 30), date, font=f_date, fill=INK)
    vol = "Vol. I — No. 3"
    vw = d.textlength(vol, font=f_vol)
    d.text((W - MX - vw, 58), vol, font=f_vol, fill=GREY)
    # double rule
    hrule(d, MX, W - MX, 94, width=3, fill=INK)
    hrule(d, MX, W - MX, 100, width=1, fill=INK)

    # ---- lead + rail row
    top = 110
    lead_w = 600
    rail_x = MX + lead_w + 24
    rail_w = W - MX - rail_x

    y = top
    draw_spaced(d, MX, y, LEAD["kicker"], f_kick, RED)
    y += 15
    for line in LEAD["headline"]:
        d.text((MX, y), line, font=f_lead_h, fill=INK)
        y += 40
    y += 4
    illo_courthouse(d, MX, y, lead_w, 84)
    y += 88
    d.text((MX, y), LEAD["caption"], font=f_cap, fill=GREY)
    y += 15
    draw_lines(d, MX, y, wrap(d, LEAD["body"], f_body, lead_w), f_body, INK, 13)
    lead_bottom = y + 4 * 13

    # vertical divider
    d.line([(MX + lead_w + 12, top), (MX + lead_w + 12, lead_bottom)], fill=HAIR, width=1)

    # right rail
    ry = top
    for i, (kick, head, body, illo) in enumerate(RAIL):
        draw_spaced(d, rail_x, ry, kick, f_kick, RED)
        ry += 13
        d.text((rail_x, ry), head, font=f_rail_h, fill=INK)
        ry += 20
        illo(d, rail_x, ry, 88, 52)
        draw_lines(d, rail_x + 96, ry, wrap(d, body, f_body, rail_w - 96), f_body, INK, 13)
        ry += 58
        if i < len(RAIL) - 1:
            hrule(d, rail_x, W - MX, ry - 2, width=1)
            ry += 5

    row_bottom = max(lead_bottom, ry)
    hrule(d, MX, W - MX, row_bottom + 4, width=1)

    # ---- story grid 3x3
    gy = row_bottom + 12
    gap = 16
    cell_w = (CW - 2 * gap) / 3
    row_h = 95
    for idx, (kick, head, body, illo) in enumerate(GRID):
        col, row = idx % 3, idx // 3
        cx = MX + col * (cell_w + gap)
        cy = gy + row * row_h
        draw_spaced(d, cx, cy, kick, f_kick, RED, spacing=1.0)
        d.text((cx, cy + 12), head, font=f_grid_h, fill=INK)
        illo(d, cx, cy + 33, 76, 52)
        draw_lines(d, cx + 84, cy + 34, wrap(d, body, f_body, cell_w - 84), f_body, INK, 13)
    grid_bottom = gy + 3 * row_h - 4
    hrule(d, MX, W - MX, grid_bottom + 2, width=1)

    # ---- flashpoints
    fy = grid_bottom + 10
    draw_spaced(d, MX, fy, "FLASHPOINTS — WHERE THE DAY HAPPENED", f_sec, INK, spacing=1.6)
    fy += 16
    f_place = F(SANS_B, 10)
    px = MX
    for i, place in enumerate(FLASHPOINTS):
        d.ellipse([px, fy + 3, px + 5, fy + 8], fill=RED)
        px += 9
        d.text((px, fy), place, font=f_place, fill=INK)
        px += d.textlength(place, font=f_place) + 14

    # ---- by the numbers
    ny = fy + 20
    hrule(d, MX, W - MX, ny, width=1)
    ny += 7
    draw_spaced(d, MX, ny, "BY THE NUMBERS", f_sec, INK, spacing=1.6)
    ny += 18
    ncell = CW / 5
    for i, (num, labels) in enumerate(NUMBERS):
        cx = MX + i * ncell
        d.text((cx, ny), num, font=f_num, fill=NAVY)
        ly = ny + 33
        for lab in labels:
            d.text((cx, ly), lab, font=f_num_lab, fill=INK)
            ly += 11
        if i > 0:
            d.line([(cx - 8, ny), (cx - 8, ly - 4)], fill=HAIR, width=1)
    num_bottom = ny + 33 + 22

    # ---- pull quote
    qy = num_bottom + 8
    hrule(d, MX, W - MX, qy, width=1)
    qy += 9
    qw = d.textlength(QUOTE, font=f_quote)
    d.text(((W - qw) / 2, qy), QUOTE, font=f_quote, fill=INK)
    qy += 24
    aw = d.textlength(QUOTE_ATTR, font=f_attr)
    d.text(((W - aw) / 2, qy), QUOTE_ATTR, font=f_attr, fill=GREY)
    quote_bottom = qy + 15

    # ---- in brief
    by = quote_bottom + 5
    hrule(d, MX, W - MX, by, width=1)
    by += 7
    draw_spaced(d, MX, by, "IN BRIEF", f_sec, INK, spacing=1.6)
    by += 16
    col_w = (CW - 2 * gap) / 3
    for col in range(3):
        cx = MX + col * (col_w + gap)
        cy = by
        for item in BRIEF[col * 8:(col + 1) * 8]:
            d.ellipse([cx, cy + 3, cx + 4, cy + 7], fill=RED)
            d.text((cx + 9, cy), item, font=f_brief, fill=INK)
            cy += 11
    brief_bottom = by + 8 * 11

    # ---- footer
    hrule(d, MX, W - MX, brief_bottom + 4, width=1)
    fw = d.textlength(FOOTER, font=f_foot)
    d.text(((W - fw) / 2, brief_bottom + 9), FOOTER, font=f_foot, fill=GREY)

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
