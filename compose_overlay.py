"""
Compose le squelette buisson (noeuds + noms + connexions) sur l'image ChatGPT.
Travaille DIRECTEMENT en 1024x1536 — zero resize, zero decalage.
Les positions sont scalees depuis le squelette 922x1244 vers 1024x1536.
Sortie: templates/buisson_final.png
"""
from PIL import Image, ImageDraw, ImageFont
import os

# ── Dimensions (format natif ChatGPT portrait) ──
IMG_W, IMG_H = 1024, 1536
CENTER_X, SOL_Y = 512, 710

ZONES = {
    "C":"aerial","F":"aerial","b":"aerial","B":"aerial","T":"aerial",
    "R-1":"under","R-2":"under","R-3":"under","R-4":"under","R-5":"under",
}

# ── Positions EXACTES scalees depuis le squelette (band-centered, 1024x1536) ──
# Generees par gen_skeleton_1024.py — collent PIXEL pour PIXEL au squelette
NODES = [
    {"id":"iC1",  "lk":"C",   "label":"Tests / CI",      "x":422, "y":96,   "pid":"iF1"},
    {"id":"iC2",  "lk":"C",   "label":"Release / CD",    "x":600, "y":102,  "pid":"iF3"},
    {"id":"iF1",  "lk":"F",   "label":"API endpoints",   "x":344, "y":226,  "pid":"ib1"},
    {"id":"iF2",  "lk":"F",   "label":"UI composants",   "x":512, "y":220,  "pid":"ib3"},
    {"id":"iF3",  "lk":"F",   "label":"Exports / CLI",   "x":677, "y":226,  "pid":"ib4"},
    {"id":"ib1",  "lk":"b",   "label":"Sub-mod 1",       "x":333, "y":348,  "pid":"iB1"},
    {"id":"ib2",  "lk":"b",   "label":"Sub-mod 2",       "x":433, "y":353,  "pid":"iB2"},
    {"id":"ib3",  "lk":"b",   "label":"Sub-mod 3",       "x":512, "y":341,  "pid":"iB3"},
    {"id":"ib4",  "lk":"b",   "label":"Sub-mod 4",       "x":589, "y":348,  "pid":"iB4"},
    {"id":"ib5",  "lk":"b",   "label":"Sub-mod 5",       "x":689, "y":353,  "pid":"iB5"},
    {"id":"iB1",  "lk":"B",   "label":"Tige A",          "x":344, "y":479,  "pid":None},
    {"id":"iB2",  "lk":"B",   "label":"Tige B",          "x":439, "y":472,  "pid":None},
    {"id":"iB3",  "lk":"B",   "label":"Tige C",          "x":512, "y":467,  "pid":None},
    {"id":"iB4",  "lk":"B",   "label":"Tige D",          "x":585, "y":472,  "pid":None},
    {"id":"iB5",  "lk":"B",   "label":"Tige E",          "x":680, "y":479,  "pid":None},
    {"id":"iR11", "lk":"R-1", "label":"Dep principale",  "x":512, "y":810,  "pid":None},
    {"id":"iR12", "lk":"R-1", "label":"Framework test",  "x":622, "y":827,  "pid":None},
    {"id":"iR21", "lk":"R-2", "label":"Archi DB",        "x":600, "y":931,  "pid":"iR11"},
    {"id":"iR22", "lk":"R-2", "label":"Archi API",       "x":424, "y":940,  "pid":"iR11"},
    {"id":"iR31", "lk":"R-3", "label":"Contrainte 1",    "x":639, "y":1048, "pid":"iR21"},
    {"id":"iR32", "lk":"R-3", "label":"Contrainte 2",    "x":386, "y":1057, "pid":"iR22"},
    {"id":"iR41", "lk":"R-4", "label":"Licence",         "x":675, "y":1166, "pid":"iR31"},
    {"id":"iR42", "lk":"R-4", "label":"Conformite",      "x":350, "y":1175, "pid":"iR32"},
    {"id":"iR51", "lk":"R-5", "label":"Algorithmes",     "x":711, "y":1282, "pid":"iR41"},
    {"id":"iR52", "lk":"R-5", "label":"Hardware",        "x":313, "y":1292, "pid":"iR42"},
]

PW = {"T":0, "B":2.5, "b":1.5, "C":1.0, "F":1.2, "R-1":3.0, "R-2":2.0, "R-3":1.2, "R-4":0.8, "R-5":0.5}


def quadratic_bezier(p0, p1, p2, steps=50):
    pts = []
    for i in range(steps + 1):
        t = i / steps
        x = (1-t)**2 * p0[0] + 2*(1-t)*t * p1[0] + t**2 * p2[0]
        y = (1-t)**2 * p0[1] + 2*(1-t)*t * p1[1] + t**2 * p2[1]
        pts.append((x, y))
    return pts


def main():
    SRC = os.path.join(os.path.dirname(__file__), "templates", "buisson_chatgpt_raw.png")
    OUT = os.path.join(os.path.dirname(__file__), "templates", "buisson_final.png")

    # Charger l'image ChatGPT TELLE QUELLE — PAS de resize
    img = Image.open(SRC).convert("RGBA")
    w, h = img.size
    if w != IMG_W or h != IMG_H:
        print(f"ATTENTION: image {w}x{h}, attendu {IMG_W}x{IMG_H} — resize force")
        img = img.resize((IMG_W, IMG_H), Image.LANCZOS)

    overlay = Image.new("RGBA", (IMG_W, IMG_H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    iPos = {n["id"]: (n["x"], n["y"]) for n in NODES}

    # ── Police ──
    try:
        font = ImageFont.truetype("consola.ttf", 13)
    except Exception:
        try:
            font = ImageFont.truetype("cour.ttf", 13)
        except Exception:
            font = ImageFont.load_default()

    # ── Connexions subtiles ──
    for n in NODES:
        pos = iPos[n["id"]]
        if n["lk"] == "T":
            continue
        if n["pid"] and n["pid"] in iPos:
            pp = iPos[n["pid"]]
        elif n["lk"] == "R-1":
            pp = (CENTER_X, SOL_Y + 18)
        elif n["lk"] == "B":
            pp = (CENTER_X, SOL_Y)
        else:
            pp = (CENTER_X, pos[1] - 18)

        cx = pp[0] + (pos[0] - pp[0]) * 0.55
        cy = pp[1] + (pos[1] - pp[1]) * 0.3
        pts = quadratic_bezier(pp, (cx, cy), pos, steps=50)
        sw = max(1, round(PW.get(n["lk"], 1.0)))
        for i in range(len(pts) - 1):
            draw.line([pts[i], pts[i+1]], fill=(255, 255, 255, 55), width=sw)

    # ── Noeuds + labels ──
    for n in NODES:
        x, y = iPos[n["id"]]
        above = ZONES.get(n["lk"], "aerial") == "aerial"

        # Point blanc
        dot_r = 5
        draw.ellipse(
            [(x - dot_r, y - dot_r), (x + dot_r, y + dot_r)],
            fill=(255, 255, 255, 200),
            outline=(255, 255, 255, 240),
            width=1
        )

        # Label
        label = n["label"]
        bbox = draw.textbbox((0, 0), label, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]

        ly = y - dot_r - th - 6 if above else y + dot_r + 5
        lx = x - tw // 2
        lx = max(4, min(lx, IMG_W - tw - 4))
        ly = max(4, min(ly, IMG_H - th - 4))

        # Fond + texte
        pad = 4
        draw.rectangle(
            [(lx - pad, ly - 2), (lx + tw + pad, ly + th + 2)],
            fill=(0, 0, 0, 175)
        )
        draw.text((lx, ly), label, fill=(255, 255, 255, 245), font=font)

    # ── Composer ──
    result = Image.alpha_composite(img, overlay).convert("RGB")
    result.save(OUT, quality=95)
    print(f"OK -> {OUT}  ({IMG_W}x{IMG_H})")


if __name__ == "__main__":
    main()
