"""
Genere le squelette BUISSON au format natif ChatGPT (1024x1536).
Reprend EXACTEMENT le meme rendu que skeleton_export.html, mais scale a 1024x1536.
Sortie: templates/buisson_skeleton_1024x1536.png
"""
from PIL import Image, ImageDraw, ImageFont
import os, math

# ── Dimensions originales du squelette ──
ORIG_W, ORIG_H = 922, 1244
ORIG_CENTER_X, ORIG_SOL_Y = 461, 575

# ── Dimensions cible (format natif ChatGPT portrait) ──
TGT_W, TGT_H = 1024, 1536
SX = TGT_W / ORIG_W   # 1.1106
SY = TGT_H / ORIG_H   # 1.2348

def sx(x): return round(x * SX)
def sy(y): return round(y * SY)

CENTER_X = sx(ORIG_CENTER_X)  # ~512
SOL_Y = sy(ORIG_SOL_Y)        # ~710

# ── Bandes (calculees dans l'espace original, puis scalees) ──
AERIAL_TOP, AERIAL_BOT = 30, ORIG_SOL_Y - 40   # 30..535
UNDER_TOP, UNDER_BOT   = ORIG_SOL_Y + 40, 1090  # 615..1090
AERIAL_LKS = ["C", "F", "b", "B", "T"]
UNDER_LKS  = ["R-1", "R-2", "R-3", "R-4", "R-5"]

aerialBandH = (AERIAL_BOT - AERIAL_TOP) / len(AERIAL_LKS)
underBandH  = (UNDER_BOT - UNDER_TOP) / len(UNDER_LKS)

band_info = {}
for i, lk in enumerate(AERIAL_LKS):
    top = AERIAL_TOP + i * aerialBandH
    band_info[lk] = {"lineY": top, "centerY": top + aerialBandH / 2}
for i, lk in enumerate(UNDER_LKS):
    top = UNDER_TOP + i * underBandH
    band_info[lk] = {"lineY": top, "centerY": top + underBandH / 2}

# ── Noeuds buisson (positions originales de skeleton_export.html) ──
NODES = [
    {"id":"iC1",  "lk":"C",   "label":"Tests / CI",      "x":380, "y":100, "pid":"iF1"},
    {"id":"iC2",  "lk":"C",   "label":"Release / CD",    "x":540, "y":105, "pid":"iF3"},
    {"id":"iF1",  "lk":"F",   "label":"API endpoints",   "x":310, "y":175, "pid":"ib1"},
    {"id":"iF2",  "lk":"F",   "label":"UI composants",   "x":461, "y":170, "pid":"ib3"},
    {"id":"iF3",  "lk":"F",   "label":"Exports / CLI",   "x":610, "y":175, "pid":"ib4"},
    {"id":"ib1",  "lk":"b",   "label":"Sub-mod 1",       "x":300, "y":250, "pid":"iB1"},
    {"id":"ib2",  "lk":"b",   "label":"Sub-mod 2",       "x":390, "y":255, "pid":"iB2"},
    {"id":"ib3",  "lk":"b",   "label":"Sub-mod 3",       "x":461, "y":245, "pid":"iB3"},
    {"id":"ib4",  "lk":"b",   "label":"Sub-mod 4",       "x":530, "y":250, "pid":"iB4"},
    {"id":"ib5",  "lk":"b",   "label":"Sub-mod 5",       "x":620, "y":255, "pid":"iB5"},
    {"id":"iB1",  "lk":"B",   "label":"Tige A",          "x":310, "y":390, "pid":None},
    {"id":"iB2",  "lk":"B",   "label":"Tige B",          "x":395, "y":385, "pid":None},
    {"id":"iB3",  "lk":"B",   "label":"Tige C",          "x":461, "y":380, "pid":None},
    {"id":"iB4",  "lk":"B",   "label":"Tige D",          "x":527, "y":385, "pid":None},
    {"id":"iB5",  "lk":"B",   "label":"Tige E",          "x":612, "y":390, "pid":None},
    {"id":"iR11", "lk":"R-1", "label":"Dep principale",  "x":461, "y":618, "pid":None},
    {"id":"iR12", "lk":"R-1", "label":"Framework test",  "x":560, "y":632, "pid":None},
    {"id":"iR21", "lk":"R-2", "label":"Archi DB",        "x":540, "y":718, "pid":"iR11"},
    {"id":"iR22", "lk":"R-2", "label":"Archi API",       "x":382, "y":725, "pid":"iR11"},
    {"id":"iR31", "lk":"R-3", "label":"Contrainte 1",    "x":575, "y":808, "pid":"iR21"},
    {"id":"iR32", "lk":"R-3", "label":"Contrainte 2",    "x":348, "y":815, "pid":"iR22"},
    {"id":"iR41", "lk":"R-4", "label":"Licence",         "x":608, "y":900, "pid":"iR31"},
    {"id":"iR42", "lk":"R-4", "label":"Conformite",      "x":315, "y":908, "pid":"iR32"},
    {"id":"iR51", "lk":"R-5", "label":"Algorithmes",     "x":640, "y":992, "pid":"iR41"},
    {"id":"iR52", "lk":"R-5", "label":"Hardware",        "x":282, "y":1000, "pid":"iR42"},
]

NR = {"T":0, "B":20, "b":12, "F":10, "C":8, "R-1":20, "R-2":14, "R-3":10, "R-4":6, "R-5":4}
PW = {"T":0, "B":2.0, "b":1.2, "C":0.8, "F":1.0, "R-1":2.5, "R-2":1.8, "R-3":1.0, "R-4":0.6, "R-5":0.4}

LEVEL_LABELS = {
    "C": "CIME", "F": "FEUILLES", "b": "RAMEAUX", "B": "BRANCHES", "T": "TRONC",
    "R-1": "R.STRUCTURELLES", "R-2": "R.PIVOTANTES", "R-3": "RADICELLES",
    "R-4": "POILS ABSORBANTS", "R-5": "MYCORHIZES",
}


def compute_positions():
    """Band centering (meme algo que skeleton_export.html), puis scale vers 1024x1536."""
    all_lks = AERIAL_LKS + UNDER_LKS
    iPos = {}
    for lk in all_lks:
        level_nodes = [n for n in NODES if n["lk"] == lk]
        if not level_nodes:
            continue
        orig_center_y = sum(n["y"] for n in level_nodes) / len(level_nodes)
        dy = band_info[lk]["centerY"] - orig_center_y
        for n in level_nodes:
            # Position band-centered en 922x1244, puis scale en 1024x1536
            iPos[n["id"]] = (sx(n["x"]), sy(round(n["y"] + dy)))
    return iPos


def quadratic_bezier(p0, p1, p2, steps=50):
    pts = []
    for i in range(steps + 1):
        t = i / steps
        x = (1-t)**2 * p0[0] + 2*(1-t)*t * p1[0] + t**2 * p2[0]
        y = (1-t)**2 * p0[1] + 2*(1-t)*t * p1[1] + t**2 * p2[1]
        pts.append((round(x), round(y)))
    return pts


def draw_dashed_line(draw, x1, y1, x2, y2, color, width=1, dash=5, gap=7):
    length = math.hypot(x2-x1, y2-y1)
    if length == 0: return
    dx, dy = (x2-x1)/length, (y2-y1)/length
    pos = 0
    while pos < length:
        end = min(pos + dash, length)
        draw.line([(x1 + dx*pos, y1 + dy*pos), (x1 + dx*end, y1 + dy*end)],
                  fill=color, width=width)
        pos = end + gap


def main():
    OUT = os.path.join(os.path.dirname(__file__), "templates", "buisson_skeleton_1024x1536.png")

    img = Image.new("RGBA", (TGT_W, TGT_H), (5, 8, 5, 255))
    draw = ImageDraw.Draw(img)

    iPos = compute_positions()

    # ── Police ──
    try:
        font_node = ImageFont.truetype("consola.ttf", 10)
        font_level = ImageFont.truetype("consola.ttf", 9)
    except Exception:
        font_node = ImageFont.load_default()
        font_level = font_node

    # ── Axe central (tirets dores discrets) ──
    draw_dashed_line(draw, CENTER_X, sy(60), CENTER_X, sy(1160),
                     (139, 105, 20, 40), width=1, dash=7, gap=5)

    # ── Lignes de niveaux (tirets blancs) ──
    line_color = (255, 255, 255, 90)
    for lk in AERIAL_LKS + UNDER_LKS:
        bi = band_info[lk]
        y = sy(round(bi["lineY"]))
        draw_dashed_line(draw, sx(40), y, sx(882), y, line_color, width=1, dash=5, gap=7)
    # Bottom boundaries
    for orig_y in [AERIAL_BOT, UNDER_BOT]:
        y = sy(round(orig_y))
        draw_dashed_line(draw, sx(40), y, sx(882), y, line_color, width=1, dash=5, gap=7)

    # ── Ligne SOL (doree pleine) ──
    draw.line([(sx(40), SOL_Y), (sx(882), SOL_Y)], fill=(139, 105, 20, 105), width=3)

    # ── Tige centrale buisson (B nodes avg -> SOL) ──
    b_nodes = [n for n in NODES if n["lk"] == "B"]
    if b_nodes:
        avg_y = sum(iPos[n["id"]][1] for n in b_nodes) / len(b_nodes)
        pw_b = round(PW["B"] * SX * 0.6)
        draw.line([(CENTER_X, round(avg_y)), (CENTER_X, SOL_Y)],
                  fill=(255, 255, 255, 100), width=max(1, pw_b))
    # SOL -> root top
    draw.line([(CENTER_X, SOL_Y), (CENTER_X, sy(UNDER_TOP + 5))],
              fill=(255, 255, 255, 85), width=2)

    # ── Connexions ──
    for n in NODES:
        pos = iPos.get(n["id"])
        if not pos or n["lk"] == "T":
            continue
        if n["pid"] and n["pid"] in iPos:
            pp = iPos[n["pid"]]
        elif n["lk"] == "R-1":
            pp = (CENTER_X, SOL_Y + sy(15))
        elif n["lk"] == "B":
            pp = (CENTER_X, SOL_Y)
        else:
            pp = (CENTER_X, pos[1] - sy(15))

        cx = pp[0] + (pos[0] - pp[0]) * 0.55
        cy = pp[1] + (pos[1] - pp[1]) * 0.3
        pts = quadratic_bezier(pp, (cx, cy), pos, steps=50)
        sw = max(1, round(PW.get(n["lk"], 1.0) * SX))
        for i in range(len(pts) - 1):
            draw.line([pts[i], pts[i+1]], fill=(255, 255, 255, 130), width=sw)

    # ── Noeuds ──
    for n in NODES:
        pos = iPos.get(n["id"])
        if not pos:
            continue
        x, y = pos
        r = round(NR.get(n["lk"], 5) * SX)

        # Halo
        draw.ellipse([(x-r, y-r), (x+r, y+r)],
                     fill=(255, 255, 255, 40),
                     outline=(255, 255, 255, 200),
                     width=2)
        # Point central
        cr = max(2, round(r * 0.25))
        draw.ellipse([(x-cr, y-cr), (x+cr, y+cr)], fill=(255, 255, 255, 255))

    result = img.convert("RGB")
    result.save(OUT, quality=95)
    print(f"OK -> {OUT} ({TGT_W}x{TGT_H})")
    print(f"CENTER_X={CENTER_X}, SOL_Y={SOL_Y}")

    # Aussi sauvegarder les positions pour compose_overlay.py
    POS_FILE = os.path.join(os.path.dirname(__file__), "templates", "buisson_positions_1024.txt")
    with open(POS_FILE, "w") as f:
        f.write(f"# Positions band-centered, scalees 1024x1536\n")
        f.write(f"# CENTER_X={CENTER_X}, SOL_Y={SOL_Y}\n")
        for n in NODES:
            pos = iPos.get(n["id"])
            if pos:
                f.write(f'{n["id"]:6s}  {n["label"]:20s}  x={pos[0]:4d}  y={pos[1]:4d}\n')
    print(f"Positions -> {POS_FILE}")


if __name__ == "__main__":
    main()
