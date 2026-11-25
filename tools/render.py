#!/usr/bin/env python3
"""Render the 25 November 2026 front page: one image, the whole day's news.

Fresh build for make.fun news-image-20261125. Draws a single 1024x1024
newspaper front page with PIL only: masthead, hero story, a 2x2 grid of
stories and an ALSO TODAY strip. Run: python3 tools/render.py
Writes entry.png next to the project root (one level up from tools/).
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "entry.png")

PAPER = (246, 241, 231)      # warm newsprint
INK = (18, 18, 18)           # near-black type
RED = (164, 30, 34)          # classic front-page red
NAVY = (22, 35, 63)          # hero panel
NAVY_LT = (38, 56, 92)       # hero panel highlight
GOLD = (201, 162, 60)        # small accent
GREY = (92, 88, 80)          # secondary text
RULE = (120, 112, 98)        # thin rules
WHITE = (248, 247, 243)
CREAM = (235, 228, 210)


def font(name, size):
    """Load a truetype font, falling back through known system paths."""
    candidates = [
        f"/usr/share/fonts/truetype/dejavu/{name}",
        f"/usr/share/fonts/truetype/liberation/{name}",
        f"/usr/share/fonts/truetype/noto/{name}",
    ]
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, xy, text, fnt, max_w, leading, color=INK):
    """Draw wrapped paragraph, return y just below the last line."""
    x, y = xy
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def rule(draw, x0, y, x1, width=2, color=RULE):
    draw.line([(x0, y), (x1, y)], fill=color, width=width)


def kicker(draw, x, y, text, color=RED):
    """Small caps section label with a short red dash before it."""
    fnt = SANS_B(17)
    draw.line([(x, y + 8), (x + 22, y + 8)], fill=color, width=3)
    draw.text((x + 30, y), text, font=fnt, fill=color)
    return fnt


def draw_rocket(draw, cx, cy, scale=1.0):
    """Simple stylised rocket + orbit rings, drawn with PIL shapes."""
    # orbit ring
    draw.ellipse([cx - 150 * scale, cy - 96 * scale,
                  cx + 150 * scale, cy + 96 * scale],
                 outline=GOLD, width=3)
    draw.ellipse([cx - 118 * scale, cy - 70 * scale,
                  cx + 118 * scale, cy + 70 * scale],
                 outline=(90, 110, 150), width=2)
    # stars
    for sx, sy, r in [(-132, -58, 3), (-96, 74, 2), (128, -72, 3),
                      (104, 66, 2), (-58, -86, 2), (72, 84, 3)]:
        draw.ellipse([cx + sx * scale - r, cy + sy * scale - r,
                      cx + sx * scale + r, cy + sy * scale + r], fill=WHITE)
    # rocket body (tilted up-right): draw axis-aligned then rotate via polygon
    # body polygon
    body = [(cx - 18, cy + 62), (cx - 18, cy - 30), (cx, cy - 66),
            (cx + 18, cy - 30), (cx + 18, cy + 62)]
    draw.polygon(body, fill=WHITE, outline=NAVY)
    # nose window
    draw.ellipse([cx - 10, cy - 34, cx + 10, cy - 14], fill=NAVY_LT)
    draw.ellipse([cx - 6, cy - 30, cx + 6, cy - 18], fill=(140, 190, 230))
    # fins
    draw.polygon([(cx - 18, cy + 30), (cx - 44, cy + 66), (cx - 18, cy + 62)],
                 fill=RED)
    draw.polygon([(cx + 18, cy + 30), (cx + 44, cy + 66), (cx + 18, cy + 62)],
                 fill=RED)
    # flame
    draw.polygon([(cx - 12, cy + 62), (cx, cy + 104), (cx + 12, cy + 62)],
                 fill=GOLD)
    draw.polygon([(cx - 6, cy + 62), (cx, cy + 88), (cx + 6, cy + 62)],
                 fill=(235, 120, 40))
    # planet arc removed: it used to spill past the panel edge


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 36                      # page margin
    X1 = W - M                  # right edge of content

    # ---- outer frame ----
    d.rectangle([14, 14, W - 15, H - 15], outline=INK, width=3)
    d.rectangle([22, 22, W - 23, H - 23], outline=RULE, width=1)

    # ---- masthead ----
    title = "THE WORLD IN ONE IMAGE"
    tf = SERIF_B(57)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 34), title, font=tf, fill=INK)
    rule(d, M, 108, X1, width=3, color=INK)
    rule(d, M, 114, X1, width=1, color=RULE)

    date_f = SANS_B(20)
    date_txt = "WEDNESDAY, 25 NOVEMBER 2026"
    dw = d.textlength(date_txt, font=date_f)
    d.text(((W - dw) / 2, 122), date_txt, font=date_f, fill=RED)
    tag_f = SANS(16)
    tag = "ONE PAGE  •  ONE DAY  •  THE WHOLE WORLD"
    tgw = d.textlength(tag, font=tag_f)
    d.text(((W - tgw) / 2, 150), tag, font=tag_f, fill=GREY)
    rule(d, M, 176, X1, width=2, color=INK)

    # ---- hero panel ----
    hy0, hy1 = 190, 512
    d.rounded_rectangle([M, hy0, X1, hy1], radius=10, fill=NAVY)
    # thin gold inner edge
    d.rounded_rectangle([M + 6, hy0 + 6, X1 - 6, hy1 - 6], radius=8,
                        outline=GOLD, width=1)

    hx = M + 28
    kicker(d, hx, hy0 + 24, "SPACE  •  CHINA", color=GOLD)
    hf = SERIF_B(54)
    d.text((hx, hy0 + 56), "PAKISTAN", font=hf, fill=WHITE)
    d.text((hx, hy0 + 114), "REACHES ORBIT", font=hf, fill=WHITE)
    rule(d, hx, hy0 + 190, hx + 330, width=2, color=GOLD)
    deck = ("Shenzhou-24 docks at Tiangong with Muhammad Zeeshan Ali — "
            "the first foreign astronaut on a Chinese crew mission.")
    para(d, (hx, hy0 + 206), deck, SANS(20), 540, 26, color=WHITE)
    d.text((hx, hy1 - 30), "Launched 08:18  •  Docked 11:56  •  Jiuquan, China",
           font=SANS_B(16), fill=(170, 190, 220))

    draw_rocket(d, 832, 352, scale=0.85)

    # ---- 2x2 story grid ----
    gy0 = 530
    card_w = (X1 - M - 24) // 2
    card_h = 152
    gap = 24
    stories = [
        ("INDONESIA", "THREE DEAD AS FLOOD",
         "TRAPS 26 IN GOLD MINE",
         "Rescuers pull three bodies from a 100-metre shaft in "
         "Bogor, West Java, after a river burst into an illegal "
         "mine. Twenty-three men are still trapped underground."),
        ("COLOMBIA", "ALL HOSTAGES FREED",
         "IN CARTAGENA SIEGE",
         "Troops storm an Exito supermarket after a day-long "
         "standoff and rescue every remaining captive. One "
         "kidnapper is killed; four are arrested."),
        ("BANGLADESH", "GARMENT PAY RISES 36%",
         "TO 17,000 TAKA",
         "Dhaka lifts the minimum wage for four million garment "
         "workers after weeks of protests that shut factories. "
         "The rise is the smallest in more than a decade."),
        ("NORTH KOREA", "PYONGYANG EXPELS",
         "SWISS ENVOY IN 48 HRS",
         "Kim Jong Un's regime orders Switzerland's diplomatic "
         "office shut and its envoy out, in a row over sanctions "
         "on a children's camp."),
    ]
    for i, (kick, h1, h2, body) in enumerate(stories):
        col, row = i % 2, i // 2
        cx = M + col * (card_w + gap)
        cy = gy0 + row * (card_h + 14)
        # card background + top accent
        d.rectangle([cx, cy, cx + card_w, cy + card_h], fill=CREAM)
        d.rectangle([cx, cy, cx + card_w, cy + 5], fill=RED)
        kicker(d, cx + 14, cy + 14, kick)
        hfnt = SERIF_B(25)
        d.text((cx + 14, cy + 40), h1, font=hfnt, fill=INK)
        d.text((cx + 14, cy + 70), h2, font=hfnt, fill=INK)
        para(d, (cx + 14, cy + 102), body, SANS(14), card_w - 28, 18,
             color=(58, 54, 46))

    # ---- ALSO TODAY strip ----
    sy0 = 858
    d.rectangle([M, sy0, X1, sy0 + 108], fill=INK)
    d.text((M + 16, sy0 + 10), "ALSO TODAY", font=SANS_B(18), fill=GOLD)
    rule(d, M + 16, sy0 + 36, X1 - 16, width=1, color=(90, 88, 80))
    strip = [
        ("HUAWEI", "US jury convicts Huawei on 10 of 12 counts, "
         "including trade-secret theft and Iran sanctions breaches."),
        ("ANTHROPIC", "Shares slide further below the $83 IPO price, "
         "trading near $77 in early trade on Wednesday."),
        ("RIYADH", "Houthis claim fresh strikes on a Saudi oil "
         "refinery and the capital's financial district."),
        ("KYIV", "Zelensky: Ukraine needs €115bn in outside "
         "financing for 2027; €25bn still to be found."),
    ]
    col_w = (X1 - M - 32) // 2
    for i, (kick, txt) in enumerate(strip):
        col, row = i % 2, i // 2
        sx = M + 16 + col * (col_w + 16)
        syy = sy0 + 44 + row * 34
        kf = SANS_B(14)
        kw = d.textlength(kick + "  ", font=kf)
        d.text((sx, syy), kick, font=kf, fill=GOLD)
        tf = SANS(13)
        lines = wrap(d, txt, tf, col_w - kw - 6)
        if lines:
            d.text((sx + kw, syy), lines[0], font=tf, fill=WHITE)
        if len(lines) > 1:
            d.text((sx, syy + 16), lines[1], font=tf, fill=WHITE)

    # ---- footer ----
    fy = 974
    rule(d, M, fy, X1, width=1, color=RULE)
    foot = ("Sources: Reuters  •  AP  •  AFP  •  Compiled from the day's wires, "
            "25 November 2026  •  make.fun news-image-20261125")
    ff = SANS(13)
    fw = d.textlength(foot, font=ff)
    d.text(((W - fw) / 2, fy + 8), foot, font=ff, fill=GREY)

    img.save(OUT, format="PNG", optimize=True)
    print(f"wrote {OUT} {os.path.getsize(OUT)} bytes")


if __name__ == "__main__":
    main()
