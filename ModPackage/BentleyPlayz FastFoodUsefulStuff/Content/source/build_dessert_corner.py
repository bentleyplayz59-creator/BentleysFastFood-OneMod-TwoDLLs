#!/usr/bin/env python3
"""Rebuilds assets/maps/z_DessertCorner.png (3.13.3) from the 3.13.2 original sheet.

Run from the Content folder:   python3 source/build_dessert_corner.py

Tile slots (16x16, 8 columns). Slots 0,1,11-16 are untouched originals.
  2-4   striped awning (now drawn on the Front layer at row 2, over the wall)
  5-7   kiosk counter (Buildings layer, row 4; Action tiles stay here)
  8-10  big sign, now reads DESSERT
  17    cafe table top        18  cafe table base (pink skirt)
  19    chair, back on left   20  chair, back on right
  21-23 "ORDER HERE" menu board (Buildings layer, row 3, behind the counter)
  24-26 items on the counter (Front layer, row 3): cake dome, bell + register, cake stand
  27-29 pink "order here" floor mat (Back layer, row 5, in front of the counter)
"""
import os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "z_DessertCorner_3.13.2_original.png")
OUT = os.path.join(HERE, "..", "assets", "maps", "z_DessertCorner.png")

# ---------------------------------------------------------------- palette
# main-restaurant wood (taken from the dining-room tables and chairs)
WOOD_OUT = (76, 48, 33)
WOOD_TOP = (220, 160, 102)
WOOD_RIM = (240, 210, 152)
WOOD_SPK = (196, 140, 82)
WOOD_MID = (164, 102, 59)
WOOD_LIT = (180, 118, 69)
WOOD_SHD = (142, 85, 51)
# dessert-corner pinks and creams (already in the 3.13.2 sheet)
PLUM = (70, 40, 45)
PINK_HI = (255, 190, 205)
PINK_A = (244, 140, 168)
PINK_B = (236, 128, 160)
PINK_C = (236, 110, 150)
PINK_D = (214, 100, 136)
PINK_E = (200, 90, 120)
CREAM = (255, 246, 228)
CREAM2 = (255, 243, 214)
CREAM3 = (250, 244, 232)
GLASS_HI = (236, 242, 248)
GLASS = (200, 226, 240)
GLASS_D = (170, 215, 240)
STEEL = (190, 196, 210)
STEEL_D = (120, 130, 150)
GOLD = (250, 215, 120)
CARAMEL = (222, 166, 92)
CHERRY = (196, 75, 60)
BOARD = (96, 58, 66)
T = (0, 0, 0, 0)


def px(p):
    return p if len(p) == 4 else (p[0], p[1], p[2], 255)


def draw_rows(img, ox, oy, rows, legend):
    """Draw ASCII rows onto img at (ox,oy). '.' = leave untouched/transparent."""
    for dy, row in enumerate(rows):
        for dx, ch in enumerate(row):
            if ch == ".":
                continue
            img.putpixel((ox + dx, oy + dy), px(legend[ch]))


def tile_xy(i):
    return (i % 8) * 16, (i // 8) * 16


def clear_tile(sheet, i):
    x0, y0 = tile_xy(i)
    for y in range(16):
        for x in range(16):
            sheet.putpixel((x0 + x, y0 + y), T)


def paste_canvas(sheet, canvas, first_tile):
    """Slice a (16*n x 16) canvas into n tiles starting at first_tile."""
    n = canvas.width // 16
    for k in range(n):
        x0, y0 = tile_xy(first_tile + k)
        sheet.paste(canvas.crop((k * 16, 0, k * 16 + 16, 16)), (x0, y0))


def check(rows):
    for r in rows:
        assert len(r) == 16, (len(r), r)
    assert len(rows) == 16, len(rows)
    return rows


sheet = Image.open(SRC).convert("RGBA")

# ================================================================ 1. SIGN
# 3 tiles = 48x16. Keep the original frame, wipe the old letters, write DESSERT.
sx0, sy0 = tile_xy(8)
sign = Image.new("RGBA", (48, 16), T)
for y in range(16):
    for x in range(48):
        sign.putpixel((x, y), sheet.getpixel((sx0 + x, sy0 + y)))
for y in range(4, 11):
    for x in range(3, 45):
        sign.putpixel((x, y), px(PINK_C))

FONT = {  # 4 wide x 5 tall
    "D": ["111.", "1..1", "1..1", "1..1", "111."],
    "E": ["1111", "1...", "111.", "1...", "1111"],
    "S": [".111", "1...", ".11.", "...1", "111."],
    "R": ["111.", "1..1", "111.", "1.1.", "1..1"],
    "T": ["1111", ".11.", ".11.", ".11.", ".11."],
}
word = "DESSERT"
text_w = len(word) * 4 + (len(word) - 1)  # 34
x_start = 24 - text_w // 2  # 7 -> letters span x7..x40, 4px margin both sides
for pass_color, dx, dy in ((PINK_E, 1, 1), (CREAM2, 0, 0)):  # shadow, then letters
    for i, ch in enumerate(word):
        gx = x_start + i * 5
        for r, line in enumerate(FONT[ch]):
            for c, bit in enumerate(line):
                if bit == "1":
                    sign.putpixel((gx + c + dx, 5 + r + dy), px(pass_color))
paste_canvas(sheet, sign, 8)

# ================================================================ 2. AWNING (tiles 2-4)
aw = Image.new("RGBA", (48, 16), T)
filled = set()
for x in range(48):
    pink = (x % 8) < 4
    col = PINK_A if pink else CREAM2
    for y in range(4, 14):
        aw.putpixel((x, y), px(col)); filled.add((x, y))
    if x % 4 in (1, 2):  # rounded scallop tip
        aw.putpixel((x, 14), px(col)); filled.add((x, 14))
for x in range(48):  # top rail
    aw.putpixel((x, 1), px(PLUM))
    aw.putpixel((x, 2), px(PINK_E))
    aw.putpixel((x, 3), px(PINK_D))
for y in range(1, 14):  # side outlines
    aw.putpixel((0, y), px(PLUM)); aw.putpixel((47, y), px(PLUM))
# outline under the scallops
for (x, y) in list(filled):
    for dx, dy in ((0, 1), (1, 0), (-1, 0)):
        nx, ny = x + dx, y + dy
        if 0 <= nx < 48 and ny < 16 and (nx, ny) not in filled and ny >= 12 and aw.getpixel((nx, ny))[3] == 0:
            aw.putpixel((nx, ny), px(PLUM))
# soft stripe shading: darker pixel at the bottom of each pink stripe
for x in range(48):
    if (x % 8) < 4 and 0 < x < 47:
        aw.putpixel((x, 13), px(PINK_B))
aw_up = Image.new("RGBA", (48, 16), T)
aw_up.paste(aw.crop((0, 1, 48, 16)), (0, 0))
paste_canvas(sheet, aw_up, 2)

# ================================================================ 3. MENU BOARD (tiles 21-23)
bd = Image.new("RGBA", (48, 16), px(BOARD))
for x in range(48):
    bd.putpixel((x, 0), px(PLUM)); bd.putpixel((x, 15), px(PLUM))
for y in range(16):
    bd.putpixel((0, y), px(PLUM)); bd.putpixel((47, y), px(PLUM))
for x in range(1, 47):  # pink trim line inside the top edge
    bd.putpixel((x, 1), px(PINK_A))
# lower half: faint chalk dots so it does not look empty behind the items
for x in range(3, 46, 4):
    bd.putpixel((x, 12), px(PINK_D))
FONT3 = {
    "O": ["111", "101", "101", "101", "111"],
    "R": ["110", "101", "110", "101", "101"],
    "D": ["110", "101", "101", "101", "110"],
    "E": ["111", "100", "110", "100", "111"],
    "H": ["101", "101", "111", "101", "101"],
}
def draw_word3(img, word, x, y, color):
    for i, ch in enumerate(word):
        for r, line in enumerate(FONT3[ch]):
            for c, bit in enumerate(line):
                if bit == "1":
                    img.putpixel((x + i * 4 + c, y + r), px(color))
draw_word3(bd, "ORDER", 5, 3, CREAM2)
draw_word3(bd, "HERE", 5 + 5 * 4 + 3, 3, CREAM2)   # "ORDER" = 19px, gap 4 -> HERE at x28
paste_canvas(sheet, bd, 21)

# ================================================================ 4. COUNTER + ITEMS (tiles 5-7 and 24-26)
# The counter is an opaque Buildings tile (row 4). The things standing on it are drawn on a
# 48x32 overlay: y0-15 is row 3 (Front layer tiles 24-26), y16-31 is row 4, whose pixels are
# baked into the counter tiles so each item is one continuous sprite.
counter = Image.new("RGBA", (48, 16), T)
for x in range(48):
    for y in range(0, 4):
        counter.putpixel((x, y), px(CREAM3))       # counter top surface
    counter.putpixel((x, 4), px(PLUM))              # front edge line
    counter.putpixel((x, 5), px(PINK_HI))           # lip highlight
    for y in range(6, 15):
        counter.putpixel((x, y), px(PINK_B))
    counter.putpixel((x, 15), px(PLUM))
    if x % 4 in (1, 2):                              # recessed panels (same rhythm as 3.13.2)
        for y in range(8, 14):
            counter.putpixel((x, y), px(PINK_D))
    if x % 4 == 0:
        counter.putpixel((x, 6), px(PINK_A))        # scallop trim under the lip
for y in range(16):
    counter.putpixel((0, y), px(PLUM)); counter.putpixel((47, y), px(PLUM))

items = Image.new("RGBA", (48, 32), T)
def P(x, y, c): items.putpixel((x, y), px(c))
def H(x0, x1, y, c):
    for x in range(x0, x1 + 1): P(x, y, c)

# ---- cake dome on a pink stand (x 0-15); top of the knob is y8, below the board lettering
for y in range(9, 17):
    for x in range(2, 14):
        dx = (x - 7.5) / 6.2
        dy = (y - 16) / 8.5
        if dx * dx + dy * dy <= 1.0:
            P(x, y, GLASS)
filled = {(x, y) for y in range(32) for x in range(16) if items.getpixel((x, y))[3]}
for (x, y) in filled:
    if any((x + dx, y + dy) not in filled for dx, dy in ((1, 0), (-1, 0), (0, -1))):
        P(x, y, STEEL_D)
P(7, 8, STEEL_D); P(8, 8, STEEL_D)                    # knob
for (x, y) in ((4, 13), (5, 12), (6, 11)):             # glass highlight
    P(x, y, GLASS_HI)
P(7, 11, CHERRY); P(8, 11, CHERRY)                    # strawberry
H(5, 10, 12, PINK_A)                                  # frosting
H(5, 10, 13, CREAM); H(5, 10, 14, PINK_D); H(5, 10, 15, CREAM)
H(2, 13, 16, STEEL_D)                                 # dome rim
H(2, 13, 17, PINK_HI); H(2, 13, 18, PINK_B)           # plate
P(2, 17, PLUM); P(13, 17, PLUM); P(2, 18, PLUM); P(13, 18, PLUM)

# ---- service bell + cash register (x 16-31)
draw_rows(items, 17, 12, [
    "...O...",
    "..OYO..",
    ".OYYYO.",
    ".OYLYO.",
    "OYYYYYO",
    "OOOOOOO",
    ".OCCCO.",
], {"O": PLUM, "Y": GOLD, "L": CREAM2, "C": CARAMEL})
draw_rows(items, 24, 11, [
    ".OOOOOO.",
    "OGHHHHGO",
    "OGGGGGGO",
    "OOOOOOOO",
    "OBCBCBBO",
    "OBBBBBBO",
    "OBBBBBBO",
    "OOOOOOOO",
], {"O": PLUM, "G": GLASS_D, "H": GLASS, "B": PINK_B, "C": CREAM2})

# ---- two-tier stand: cupcake on top, two donuts below (x 32-47)
S = 32
def SP(x, y, c): P(S + x, y, c)
def SH(x0, x1, y, c):
    for x in range(x0, x1 + 1): SP(x, y, c)
SP(7, 8, CHERRY); SP(8, 8, CHERRY)                     # cherry
SH(6, 9, 9, PINK_A); SH(5, 10, 10, PINK_HI)            # frosting
SH(5, 10, 11, PINK_D); SH(5, 10, 12, PINK_D)           # wrapper
SH(3, 12, 13, PLUM); SH(4, 11, 14, PINK_B)             # top plate
for y in (15, 16):
    SP(7, y, PLUM); SP(8, y, PINK_D)                   # stem
SH(1, 14, 17, PLUM); SH(1, 14, 18, PINK_B)             # bottom plate
for x0 in (2, 10):                                      # donuts: glaze over dough
    SH(x0, x0 + 3, 15, PINK_A); SH(x0, x0 + 3, 16, CARAMEL)
    SP(x0 + 1, 15, CREAM2)

full = Image.new("RGBA", (48, 16), T)
full.paste(counter, (0, 0))
full.alpha_composite(items.crop((0, 16, 48, 32)))
paste_canvas(sheet, full, 5)                            # counter tiles (Buildings, row 4)
paste_canvas(sheet, items.crop((0, 0, 48, 16)), 24)     # items above it (Front, row 3)

# ================================================================ 5. TABLE + CHAIRS
table_top = check([
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "..OOOOOOOOOOOO..",
    ".OIIIIIIIIIIIIO.",
    ".OJJJJJJRRJJJJO.",
    ".OJAASSSSSSAAJO.",
    ".OJBBMMMMMMBBJO.",
    ".OJCCGGGGGGCCJO.",
    ".OJKJJHHHHJJKJO.",
    ".OJJJJJYYJJJJJO.",
])
# row 5 above has 16 chars? verify
leg_tt = {"O": WOOD_OUT, "I": WOOD_RIM, "J": WOOD_TOP, "K": WOOD_SPK,
          "R": CHERRY, "S": PINK_A, "M": CREAM, "A": PINK_HI, "B": PINK_B,
          "C": PINK_D, "G": GLASS, "H": GLASS_D, "Y": STEEL}
clear_tile(sheet, 17)
draw_rows(sheet, *tile_xy(17), table_top, leg_tt)

table_base = check([
    ".OJJJJJJJJJJJJO.",
    ".OJKJJJJJJJJKJO.",
    ".OJJJJJJJJJJJJO.",
    ".OAAAAAAAAAAAAO.",
    ".OBBBBBBBBBBBBO.",
    ".OCCCCCCCCCCCCO.",
    "..dddddddddddd..",
    "...OwWO..OwWO...",
    "...OWWO..OWWO...",
    "...OWWO..OWWO...",
    "...OWWO..OWWO...",
    "...OWWO..OWWO...",
    "...OWWO..OWWO...",
    "...OWWO..OWWO...",
    "...OOOO..OOOO...",
    "................",
])
leg_tb = {"O": WOOD_OUT, "J": WOOD_TOP, "K": WOOD_SPK, "A": PINK_HI, "B": PINK_B,
          "C": PINK_D, "d": WOOD_SHD, "w": WOOD_LIT, "W": WOOD_MID}
clear_tile(sheet, 18)
draw_rows(sheet, *tile_xy(18), table_base, leg_tb)

chair_l = check([
    "................",
    "................",
    "................",
    "....OO..........",
    "...OAAO.........",
    "...OAQO.........",
    "...OAQO.........",
    "...OAQO.........",
    "...OAQO.........",
    "...OQQO.........",
    "...OOOOOOOOOOO..",
    "...OAAAAAAAAAO..",
    "...OQQQQQQQQQO..",
    "...OCCCCCCCCCO..",
    "...OWWOOOOOWWO..",
    "...OOOO...OOOO..",
])
leg_ch = {"O": WOOD_OUT, "A": PINK_HI, "Q": PINK_A, "C": PINK_D, "W": WOOD_MID}
clear_tile(sheet, 19)
draw_rows(sheet, *tile_xy(19), chair_l, leg_ch)
# right chair = mirror of the left one
x19, y19 = tile_xy(19)
mirror = sheet.crop((x19, y19, x19 + 16, y19 + 16)).transpose(Image.FLIP_LEFT_RIGHT)
x20, y20 = tile_xy(20)
clear_tile(sheet, 20)
sheet.paste(mirror, (x20, y20))

# ================================================================ 6. FLOOR MAT (tiles 27-29)
# base = the floor tiles that are under the mat in the map: x2 (tile1 cream), x3 (tile0 pink), x4 (tile1 cream)
mat = Image.new("RGBA", (48, 16), T)
for k, base in enumerate((1, 0, 1)):
    bx, by = tile_xy(base)
    mat.paste(sheet.crop((bx, by, bx + 16, by + 16)), (k * 16, 0))
for y in range(2, 14):
    for x in range(1, 47):
        edge = x in (1, 46) or y in (2, 13)
        # rounded corners
        if (x, y) in ((1, 2), (46, 2), (1, 13), (46, 13)):
            continue
        mat.putpixel((x, y), px(PINK_E if edge else PINK_C))
for y in range(4, 12):
    for x in range(3, 45):
        if x in (3, 44) or y in (4, 11):
            mat.putpixel((x, y), px(CREAM2)) if (x + y) % 2 == 0 else None
arrow = [
    "...X...",
    "..XXX..",
    ".XXXXX.",
    "XXXXXXX",
    "..XXX..",
    "..XXX..",
    "..XXX..",
]
for cxm in (8, 24, 40):
    for r, line in enumerate(arrow):
        for c, ch in enumerate(line):
            if ch == "X":
                mat.putpixel((cxm - 3 + c, 4 + r), px(CREAM2))
paste_canvas(sheet, mat, 27)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
sheet.save(OUT)
print("wrote", os.path.normpath(OUT), sheet.size)
