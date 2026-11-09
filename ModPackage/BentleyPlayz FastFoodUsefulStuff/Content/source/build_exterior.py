#!/usr/bin/env python3
"""
Redraws the Bentley's Fast Food exterior tilesheet (128x112 = 8x7 tiles of 16px).

* Tile grid / tile indices are NOT changed, so ForestRestaurant.tmx, ForestDoorStep.tmx,
  ForestDoorClosed.tmx and every Content Patcher patch keep working untouched.
* Sign (x37-90,y36-50), menu board (x33-45,y74-96) and hours poster (x83-95,y74-96) are
  copied pixel-for-pixel from the ORIGINAL sheet.
* Everything else is redrawn using colours sampled from vanilla Pierre's General Store.
"""
import sys
from PIL import Image

SRC = sys.argv[1]          # original sheet
DST = sys.argv[2]          # output sheet
orig = Image.open(SRC).convert("RGBA")
W, H = orig.size
assert (W, H) == (128, 112)

img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
px = img.load()
op = orig.load()


def C(h):
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 255)


# ---------------------------------------------------------------- palette (vanilla-sampled)
OUT, OUT2 = C("2c201a"), C("470303")
RH, RM, RS, RD, RDD = C("ff9651"), C("dd6f40"), C("c5632e"), C("b04b34"), C("92412b")
FD, FDD = C("782929"), C("582a2d")
WH, WM, WL, WLN = C("ffdba3"), C("f1be94"), C("edaa73"), C("c79053")
TH, TM, TD, TDD = C("954b36"), C("7c3a27"), C("57251a"), C("3b2018")
SH, SM, SD, SDD = C("a99a6c"), C("847354"), C("5f513c"), C("473d31")
GL, GLH, GLD, GLDD = C("94d4e4"), C("dbfdff"), C("69b7d5"), C("538baf")
GOLD, GOLD2, GOLDH = C("ffbd54"), C("ae6823"), C("ffdba3")
AR, ARH, ARS, ARD = C("c8332b"), C("e0574a"), C("992019"), C("550414")
AC, ACH, ACS = C("f6e4b4"), C("fff3d0"), C("d9bd86")
GRN, GRN2 = C("2a5023"), C("4a8a35")
FLR, FLY, FLP = C("ca1210"), C("ffd37a"), C("ff8fa8")


def hs(x, y):
    return ((x * 73856093) ^ (y * 19349663)) & 0xFFFF


def P(x, y, c):
    if 0 <= x < W and 0 <= y < H:
        px[x, y] = c


def R(x0, y0, x1, y1, c):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            P(x, y, c)


def shade(x0, y0, x1, y1, f):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            r, g, b, a = px[x, y]
            if a:
                px[x, y] = (int(r * f), int(g * f * 0.98), int(b * f * 0.96), a)


def outline(mask, color, dirs=((-1, 0), (1, 0), (0, -1), (0, 1))):
    out = []
    for (x, y) in mask:
        for dx, dy in dirs:
            if (x + dx, y + dy) not in mask:
                out.append((x, y))
                break
    for x, y in out:
        P(x, y, color)


# ================================================================ WALL (clapboard)
WALL_X0, WALL_X1, WALL_Y0, WALL_Y1 = 4, 123, 37, 102
for y in range(WALL_Y0, WALL_Y1 + 1):
    t = (y - WALL_Y0) % 5
    row = y - WALL_Y0
    for x in range(WALL_X0, WALL_X1 + 1):
        c = WH if t == 0 else (WLN if t == 4 else (WL if t == 3 else WM))
        # staggered butt joints
        if t in (1, 2, 3) and (x + (row // 5) * 17) % 41 == 0:
            c = WLN
        if t in (1, 2) and hs(x, y) % 53 == 0:
            c = WL
        P(x, y, c)

# ================================================================ ROOF
def xl(y):   # outer left silhouette
    return int(round(27 - (y - 6) * 0.88))


def xa(y):   # left arris (hip line)
    return int(round(36 - (y - 6) * 0.78))


roof = set()
# ridge cap
for y in range(5, 9):
    x0 = 27 + (1 if y == 5 else 0)
    for x in range(x0, 127 - x0 + 1):
        roof.add((x, y))
for y in range(9, 33):
    for x in range(xl(y), 127 - xl(y) + 1):
        roof.add((x, y))

# eave lip first (full width, overhang past the walls)
for x in range(0, 128):
    P(x, 33, RH)
    P(x, 34, RM)
    P(x, 35, RDD)
    P(x, 36, OUT2)
P(0, 33, OUT2); P(127, 33, OUT2)
P(0, 34, OUT2); P(127, 34, OUT2)
P(0, 35, OUT2); P(127, 35, OUT2)
for x in range(0, 128):
    if hs(x, 7) % 9 == 0:
        P(x, 34, RS)

# ridge cap
for x in range(27, 101):
    P(x, 6, RH)
    P(x, 7, RM)
    P(x, 8, RDD)
    if hs(x, 3) % 7 == 0:
        P(x, 7, RS)

# courses
for y in range(9, 33):
    c = (y - 9) // 8
    t = (y - 9) % 8
    a_l, a_r = xa(y), 127 - xa(y)
    for x in range(xl(y), 127 - xl(y) + 1):
        if x < a_l:                                   # left hip facet (dark, away from light)
            if t == 0: col = RDD
            elif t >= 6: col = FDD
            else: col = FD
            if (x - xl(y) + c * 5) % 10 == 0 and t < 7: col = FDD
        elif x > a_r:                                 # right hip facet (mid)
            if t == 0: col = RS
            elif t == 6: col = RDD
            elif t == 7: col = C("7c3a27")
            else: col = RD
            if ((127 - xl(y)) - x + c * 5) % 10 == 0 and t < 7: col = RS
            if 1 <= t <= 5 and hs(x, y) % 31 == 0: col = RS
        else:                                         # front face (lit)
            off = (c % 2) * 12 + c * 3
            j = (x - off) % 24
            if t == 0: col = RH
            elif t == 6: col = RS
            elif t == 7: col = RDD
            else: col = RM
            if t < 7:
                if j == 0: col = RD
                elif j == 23 and t < 6: col = RH if t else RH
            if 1 <= t <= 4 and hs(x, y) % 19 == 0: col = RS
            if x == a_l: col = RH if t < 6 else RS
            if x == a_r: col = RDD
        P(x, y, col)
# hip-line crease between facets and front face
for y in range(9, 33):
    P(xa(y) - 1, y, FDD)
    P(127 - xa(y) + 1, y, RDD)

outline(roof, OUT2, dirs=((-1, 0), (1, 0), (0, -1)))
for x in range(xl(32), 127 - xl(32) + 1):
    P(x, 32, OUT2)

# ================================================================ CHIMNEYS (in front of roof)
# stone chimney, right
cx0, cx1 = 80, 91
for y in range(1, 17):
    for x in range(cx0, cx1 + 1):
        col = SM
        if x == cx0: col = SD
        if x == cx1: col = SH
        if (y % 4) == 0: col = SDD
        elif ((x + (y // 4) * 5) % 6) == 0: col = SDD
        elif hs(x, y) % 11 == 0: col = SH
        P(x, y, col)
R(cx0 - 1, 0, cx1 + 1, 3, SM)
R(cx0 - 1, 0, cx1 + 1, 0, SH)
R(cx0, 1, cx1, 2, OUT)              # flue opening
R(cx0 - 1, 3, cx1 + 1, 3, SD)
for y in range(0, 4):
    P(cx0 - 2, y, OUT2); P(cx1 + 2, y, OUT2)
for x in range(cx0 - 2, cx1 + 3):
    P(x, 4, OUT2)
for y in range(4, 17):
    P(cx0 - 1, y, OUT2); P(cx1 + 1, y, OUT2)
for x in range(cx0 - 1, cx1 + 2):
    P(x, 17, FDD)                   # flashing on roof
    P(x, 18, OUT2)
# metal vent pipe, left
for y in range(2, 13):
    for x in range(45, 49):
        P(x, y, C("7b787e") if x in (46, 47) else C("47434f"))
    P(48, y, C("b9bac2"))
R(44, 1, 49, 2, C("7b787e")); R(44, 1, 49, 1, C("b9bac2"))
for y in range(1, 13):
    P(43 if y < 3 else 44, y, OUT2); P(50 if y < 3 else 49, y, OUT2)
R(44, 0, 49, 0, OUT2); R(44, 13, 49, 13, OUT2)

# ================================================================ UPPER WALL: sign + small windows
sign = {(x, y): op[x, y] for y in range(36, 51) for x in range(37, 91)}
for (x, y), c in sign.items():
    px[x, y] = c
for x in range(37, 91):
    P(x, 51, OUT)                    # contact line under sign
# iron brackets
for xx in (33, 34, 35, 36):
    P(xx, 41, OUT); P(xx, 47, OUT)
    P(127 - xx, 41, OUT); P(127 - xx, 47, OUT)
    P(xx, 40, WLN if xx > 33 else WM); P(127 - xx, 40, WLN)


def small_window(x0, y0):           # 14 x 11
    R(x0, y0, x0 + 13, y0 + 10, TDD)
    R(x0 + 1, y0 + 1, x0 + 12, y0 + 9, TM)
    R(x0 + 1, y0 + 1, x0 + 12, y0 + 1, TH)
    R(x0 + 12, y0 + 1, x0 + 12, y0 + 9, TH)
    R(x0 + 2, y0 + 2, x0 + 11, y0 + 8, GL)
    R(x0 + 6, y0 + 2, x0 + 7, y0 + 8, TM)
    R(x0 + 2, y0 + 5, x0 + 11, y0 + 5, TM)
    for (ax, ay) in ((x0 + 3, y0 + 3), (x0 + 4, y0 + 4)):
        P(ax, ay, GLH)
    for (ax, ay) in ((x0 + 9, y0 + 3), (x0 + 10, y0 + 4)):
        P(ax, ay, GLH)
    for ax in range(x0 + 2, x0 + 12):
        if ax not in (x0 + 6, x0 + 7):
            P(ax, y0 + 8, GLD)
    R(x0 - 1, y0 + 11, x0 + 14, y0 + 11, WLN)      # sill
    R(x0 - 1, y0 + 11, x0 + 14, y0 + 11, WLN)
    R(x0, y0 + 11, x0 + 13, y0 + 11, WL)


small_window(15, 39)
small_window(99, 39)

# ================================================================ AWNING
awn = set()
for y in range(52, 62):
    for x in range(1, 127):
        awn.add((x, y))
for s in range(0, 21):
    x0 = 1 + s * 6
    for x in range(x0 + 1, x0 + 5):
        awn.add((x, 62))
    for x in range(x0 + 2, x0 + 4):
        awn.add((x, 63))
    awn.discard((x0, 62)); awn.discard((x0 + 5, 62))
for (x, y) in awn:
    s = (x - 1) // 6
    red = (s % 2 == 0)
    xi = (x - 1) % 6
    if y <= 55:                         # sloped top plane (lit)
        col = ARH if red else ACH
        if y == 55: col = AR if red else AC
    else:                               # hanging valance
        col = AR if red else AC
        if xi == 0: col = ARS if red else ACS
        if xi == 5: col = ARH if red else ACH
        if y == 56: col = ARS if red else ACS
        if y >= 61: col = ARS if red else ACS
    P(x, y, col)
outline(awn, ARD, dirs=((-1, 0), (1, 0), (0, 1)))
for x in range(0, 128):
    P(x, 51, ARD)
for x in range(2, 126):
    if (x, 51) in sign:
        pass
for x in range(37, 91):
    P(x, 51, OUT)

# ================================================================ POSTS
def post(x0):
    for y in range(37, 103):
        for i, col in enumerate((TD, TM, TM, TH, TD)):
            c = col
            if i in (1, 2) and hs(x0 + i, y) % 13 == 0:
                c = TD
            P(x0 + i, y, c)
    for i in range(5):
        P(x0 + i, 37, TDD)


post(4)
post(119)

# shadow cast by the awning, then by the eave
shade(9, 64, 118, 64, 0.62)
shade(9, 65, 118, 65, 0.74)
shade(9, 66, 118, 66, 0.86)
shade(9, 67, 118, 67, 0.94)
for yy, f in ((37, 0.60), (38, 0.72), (39, 0.86)):
    shade(4, yy, 36, yy, f)
    shade(91, yy, 123, yy, f)
# the hours/menu posters hang over the shadow, redrawn later

# ================================================================ GROUND-FLOOR WINDOWS
def big_window(x0):                 # 22 wide x 23 tall (outer), y 69..91
    y0 = 69
    R(x0, y0, x0 + 21, y0 + 19, TDD)                       # outline
    R(x0 + 1, y0 + 1, x0 + 20, y0 + 18, TM)                # frame
    R(x0 + 1, y0 + 1, x0 + 20, y0 + 2, TH)                 # lit lintel
    R(x0 + 19, y0 + 1, x0 + 20, y0 + 18, TH)               # lit right jamb
    R(x0 + 1, y0 + 1, x0 + 2, y0 + 18, TD)                 # shaded left jamb
    R(x0 + 3, y0 + 3, x0 + 18, y0 + 18, GL)                # glass 16x16
    # interior scene: curtain valance, horizon, counter
    R(x0 + 3, y0 + 3, x0 + 18, y0 + 3, GOLD)
    for k in range(0, 16):
        P(x0 + 3 + k, y0 + 4, GOLD if k % 2 == 0 else GOLD2)
    R(x0 + 3, y0 + 9, x0 + 18, y0 + 13, GLD)
    R(x0 + 3, y0 + 14, x0 + 18, y0 + 18, WLN)
    R(x0 + 3, y0 + 14, x0 + 18, y0 + 14, WL)
    R(x0 + 3, y0 + 18, x0 + 18, y0 + 18, TM)
    # mullions
    R(x0 + 10, y0 + 3, x0 + 11, y0 + 18, TM)
    R(x0 + 10, y0 + 3, x0 + 10, y0 + 18, TD)
    R(x0 + 3, y0 + 10, x0 + 18, y0 + 10, TM)
    # glass glints
    for (gx, gy) in ((x0 + 5, y0 + 6), (x0 + 6, y0 + 7), (x0 + 7, y0 + 8),
                     (x0 + 13, y0 + 6), (x0 + 14, y0 + 7), (x0 + 15, y0 + 8)):
        P(gx, gy, GLH)
    # sill
    R(x0 - 1, y0 + 19, x0 + 22, y0 + 19, WL)
    R(x0 - 1, y0 + 20, x0 + 22, y0 + 21, WLN)
    R(x0 - 1, y0 + 21, x0 + 22, y0 + 21, TH)
    R(x0, y0 + 22, x0 + 21, y0 + 22, C("a5644b"))
    # window box with flowers
    R(x0 + 1, y0 + 23, x0 + 20, y0 + 30, TM)
    R(x0 + 1, y0 + 23, x0 + 20, y0 + 23, TH)
    R(x0 + 1, y0 + 30, x0 + 20, y0 + 30, TD)
    for k in range(x0 + 4, x0 + 20, 5):
        R(k, y0 + 24, k, y0 + 29, TD)
    for k in range(x0 + 1, x0 + 21):
        P(k, y0 + 22, GRN)
        if hs(k, 5) % 3:
            P(k, y0 + 21, GRN2)
    for k, c in zip(range(x0 + 2, x0 + 21, 3), (FLR, FLY, FLP, FLR, FLY, FLP, FLR)):
        P(k, y0 + 21, c)
        P(k, y0 + 22, GRN2)
    R(x0, y0 + 31, x0 + 21, y0 + 31, WLN)  # box shadow on wall


# the window boxes end at y 100, plinth begins at 103
big_window(10)
big_window(96)

# ================================================================ POSTERS (copied from original, pixel-exact)
for (x0, x1) in ((33, 45), (83, 95)):
    for y in range(74, 97):
        for x in range(x0, x1 + 1):
            px[x, y] = op[x, y]
    for x in range(x0 + 1, x1 + 2):   # soft shadow on the wall
        P(x, 97, WLN)
    P(x1 + 1, 75, WLN)
    for y in range(76, 97):
        P(x1 + 1, y, WL)

# ================================================================ DOOR
# lintel with golden transom bar
R(46, 64, 81, 68, OUT)
R(47, 65, 80, 65, GOLDH)
R(47, 66, 80, 66, GOLD)
R(47, 67, 80, 67, GOLD2)
# jambs
for y in range(69, 103):
    for i, col in enumerate((TDD, TM, TD)):
        P(46 + i, y, col)
    for i, col in enumerate((TD, TH, TDD)):
        P(79 + i, y, col)
# glass leaves
for (lx0, lx1) in ((49, 62), (65, 78)):
    for y in range(69, 102):
        for x in range(lx0, lx1 + 1):
            if y == 69 or x in (lx0, lx1):
                c = TM
            elif y < 80:
                c = GL
            elif y < 86:
                c = GLD
            elif y < 92:
                c = WLN
            else:
                c = C("a5644b")
            P(x, y, c)
    for x in range(lx0 + 1, lx1):
        P(x, 86, WL)
        P(x, 92, TM)
        P(x, 101, TD)
    # kick-panel inset
    R(lx0 + 2, 94, lx1 - 2, 99, TH)
    R(lx0 + 2, 94, lx1 - 2, 94, C("a5644b"))
    R(lx0 + 2, 99, lx1 - 2, 99, TD)
    R(lx0 + 2, 94, lx0 + 2, 99, TD)
# glass reflections
for k in range(5):
    P(52 + k, 71 + k, GLH); P(53 + k, 71 + k, GLH)
    P(68 + k, 71 + k, GLH); P(69 + k, 71 + k, GLH)
# centre mullion
R(63, 69, 64, 101, TD)
P(64, 70, TM)
for y in range(70, 102):
    P(63, y, TM)
# handles
for hx in (60, 66):
    R(hx, 79, hx + 1, 86, GOLD)
    R(hx + 1, 79, hx + 1, 86, GOLD2)
    P(hx, 79, GOLDH)
# threshold
R(46, 102, 81, 102, TDD)

# ================================================================ FOUNDATION + STEP
for y in range(103, 112):
    t = y - 103
    for x in range(3, 125):
        if t == 0:
            c = SH
        elif t == 8:
            c = OUT
        else:
            course = 0 if t <= 4 else 1
            lt = (t - 1) if course == 0 else (t - 5)
            off = 0 if course == 0 else 7
            jx = (x + off) % 14
            c = SM
            if lt == 0: c = SH
            if lt == 3 or t == 7: c = SD
            if jx == 0: c = SDD
            if lt in (1, 2) and hs(x, y) % 17 == 0: c = SD
        P(x, y, c)
    P(3, y, OUT if t else OUT)
    P(124, y, OUT)
# door step slab (walkable tiles are x48-79) in lighter flagstone with red mat
R(46, 103, 81, 111, SH)
R(46, 103, 81, 103, C("c9bb8a"))
for x in range(46, 82):
    if (x - 46) % 12 == 5:
        R(x, 104, x, 110, SM)
R(46, 111, 81, 111, OUT)
R(46, 110, 81, 110, SM)
R(46, 103, 46, 111, OUT); R(81, 103, 81, 111, OUT)
R(51, 105, 76, 109, ARD)
R(52, 106, 75, 108, AR)
R(52, 106, 75, 106, ARH)
for x in range(54, 75, 4):
    P(x, 107, ACH); P(x + 1, 107, ACH)
R(52, 108, 75, 108, ARS)

# ================================================================ SAFETY: unused tiles stay empty
for (x0, y0) in ((0, 0), (112, 0)):
    for y in range(y0, y0 + 16):
        for x in range(x0, x0 + 16):
            px[x, y] = (0, 0, 0, 0)

img.save(DST, optimize=True)
print("wrote", DST)
