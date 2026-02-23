#!/usr/bin/env python3
# GEN ALL SKELETONS + OVERLAYS
# Genere les squelettes 1024x1536 et les overlays pour les 6 familles.
# Positions extraites de skeleton_export.html (922x1244 -> scale 1024x1536).
# Usage: python gen_all_skeletons.py

from PIL import Image, ImageDraw, ImageFont
import os, math, json

ROOT = os.path.dirname(os.path.abspath(__file__))
TEMPLATES = os.path.join(ROOT, "templates")

ORIG_W, ORIG_H = 922, 1244
TGT_W, TGT_H = 1024, 1536
SX = TGT_W / ORIG_W
SY = TGT_H / ORIG_H

def sx(x): return round(x * SX)
def sy(y): return round(y * SY)

CENTER_X = sx(461)
SOL_Y = sy(575)

# Bandes
AERIAL_LKS = ["C", "F", "b", "B", "T"]
UNDER_LKS = ["R-1", "R-2", "R-3", "R-4", "R-5"]
AERIAL_TOP, AERIAL_BOT = sy(30), sy(535)
UNDER_TOP, UNDER_BOT = sy(615), sy(1090)

aH = (AERIAL_BOT - AERIAL_TOP) / len(AERIAL_LKS)
uH = (UNDER_BOT - UNDER_TOP) / len(UNDER_LKS)

BAND_Y = {}
for i, lk in enumerate(AERIAL_LKS):
    BAND_Y[lk] = sy(30) + i * aH
for i, lk in enumerate(UNDER_LKS):
    BAND_Y[lk] = sy(615) + i * uH

# Couleurs par niveau
COLORS = {
    "C": (40, 200, 98), "F": (50, 181, 85), "b": (56, 160, 72),
    "B": (61, 138, 58), "T": (90, 154, 53),
    "R-1": (154, 116, 83), "R-2": (138, 99, 68), "R-3": (122, 82, 53),
    "R-4": (107, 66, 38), "R-5": (92, 51, 23),
}

# ══════════════════════════════════════════════════════════════
# POSITIONS PAR FAMILLE (922x1244, seront scalees)
# ══════════════════════════════════════════════════════════════

FAMILIES = {
    "conifere": {
        "emoji": "🌲", "trunkTopY": 90,
        "nodes": [
            {"id":"iC1","lk":"C","label":"Tests / CI","x":476,"y":112,"pid":None},
            {"id":"iC2","lk":"C","label":"Release / CD","x":446,"y":118,"pid":None},
            {"id":"iF1","lk":"F","label":"API endpoints","x":505,"y":188,"pid":"ib1"},
            {"id":"iF2","lk":"F","label":"UI composants","x":418,"y":193,"pid":"ib3"},
            {"id":"iF3","lk":"F","label":"Exports / CLI","x":538,"y":218,"pid":"ib5"},
            {"id":"iB1","lk":"B","label":"Module A","x":490,"y":392,"pid":None},
            {"id":"iB2","lk":"B","label":"Module B","x":432,"y":397,"pid":None},
            {"id":"iB3","lk":"B","label":"Module C","x":515,"y":450,"pid":None},
            {"id":"iB4","lk":"B","label":"Module D","x":408,"y":455,"pid":None},
            {"id":"ib1","lk":"b","label":"Sub-mod 1","x":520,"y":278,"pid":"iB1"},
            {"id":"ib2","lk":"b","label":"Sub-mod 2","x":555,"y":308,"pid":"iB1"},
            {"id":"ib3","lk":"b","label":"Sub-mod 3","x":400,"y":283,"pid":"iB2"},
            {"id":"ib4","lk":"b","label":"Sub-mod 4","x":368,"y":312,"pid":"iB2"},
            {"id":"ib5","lk":"b","label":"Sub-mod 5","x":580,"y":342,"pid":"iB3"},
            {"id":"ib6","lk":"b","label":"Sub-mod 6","x":345,"y":348,"pid":"iB4"},
            {"id":"iT1","lk":"T","label":"Core pipeline","x":461,"y":530,"pid":None},
            {"id":"iR11","lk":"R-1","label":"Framework web","x":505,"y":612,"pid":None},
            {"id":"iR12","lk":"R-1","label":"Framework data","x":418,"y":618,"pid":None},
            {"id":"iR13","lk":"R-1","label":"Framework test","x":545,"y":638,"pid":None},
            {"id":"iR21","lk":"R-2","label":"Archi DB","x":548,"y":712,"pid":"iR11"},
            {"id":"iR22","lk":"R-2","label":"Archi API","x":375,"y":720,"pid":"iR12"},
            {"id":"iR31","lk":"R-3","label":"Contrainte 1","x":580,"y":800,"pid":"iR21"},
            {"id":"iR32","lk":"R-3","label":"Contrainte 2","x":345,"y":808,"pid":"iR22"},
            {"id":"iR33","lk":"R-3","label":"Contrainte 3","x":628,"y":815,"pid":"iR21"},
            {"id":"iR41","lk":"R-4","label":"Licence","x":612,"y":895,"pid":"iR31"},
            {"id":"iR42","lk":"R-4","label":"Conformite","x":312,"y":902,"pid":"iR32"},
            {"id":"iR51","lk":"R-5","label":"Algorithmes","x":645,"y":988,"pid":"iR41"},
            {"id":"iR52","lk":"R-5","label":"Hardware","x":278,"y":995,"pid":"iR42"},
        ],
        "pw":{"T":4.0,"B":2.5,"b":1.5,"C":1.0,"F":1.2,"R-1":2.5,"R-2":1.8,"R-3":1.2,"R-4":0.8,"R-5":0.5},
    },
    "feuillu": {
        "emoji": "🍁", "trunkTopY": 200,
        "nodes": [
            {"id":"iC1","lk":"C","label":"Tests / CI","x":461,"y":100,"pid":None},
            {"id":"iC2","lk":"C","label":"Release / CD","x":390,"y":120,"pid":None},
            {"id":"iC3","lk":"C","label":"Monitoring","x":530,"y":120,"pid":None},
            {"id":"iF1","lk":"F","label":"API endpoints","x":340,"y":190,"pid":"ib1"},
            {"id":"iF2","lk":"F","label":"UI composants","x":461,"y":180,"pid":"ib3"},
            {"id":"iF3","lk":"F","label":"Exports / CLI","x":580,"y":190,"pid":"ib4"},
            {"id":"iF4","lk":"F","label":"Webhooks","x":280,"y":215,"pid":"ib2"},
            {"id":"ib1","lk":"b","label":"Sub-mod 1","x":330,"y":260,"pid":"iB1"},
            {"id":"ib2","lk":"b","label":"Sub-mod 2","x":255,"y":285,"pid":"iB2"},
            {"id":"ib3","lk":"b","label":"Sub-mod 3","x":461,"y":255,"pid":"iB3"},
            {"id":"ib4","lk":"b","label":"Sub-mod 4","x":595,"y":260,"pid":"iB4"},
            {"id":"ib5","lk":"b","label":"Sub-mod 5","x":665,"y":285,"pid":"iB5"},
            {"id":"ib6","lk":"b","label":"Sub-mod 6","x":385,"y":275,"pid":"iB1"},
            {"id":"iB1","lk":"B","label":"Module A","x":365,"y":385,"pid":None},
            {"id":"iB2","lk":"B","label":"Module B","x":275,"y":415,"pid":"iB1"},
            {"id":"iB3","lk":"B","label":"Module C","x":461,"y":375,"pid":None},
            {"id":"iB4","lk":"B","label":"Module D","x":555,"y":385,"pid":None},
            {"id":"iB5","lk":"B","label":"Module E","x":645,"y":415,"pid":"iB4"},
            {"id":"iT1","lk":"T","label":"Core engine","x":461,"y":500,"pid":None},
            {"id":"iR11","lk":"R-1","label":"Framework web","x":520,"y":618,"pid":None},
            {"id":"iR12","lk":"R-1","label":"Framework data","x":400,"y":622,"pid":None},
            {"id":"iR13","lk":"R-1","label":"Framework test","x":580,"y":640,"pid":None},
            {"id":"iR21","lk":"R-2","label":"Archi DB","x":560,"y":720,"pid":"iR11"},
            {"id":"iR22","lk":"R-2","label":"Archi API","x":355,"y":728,"pid":"iR12"},
            {"id":"iR31","lk":"R-3","label":"Contrainte 1","x":600,"y":810,"pid":"iR21"},
            {"id":"iR32","lk":"R-3","label":"Contrainte 2","x":320,"y":818,"pid":"iR22"},
            {"id":"iR33","lk":"R-3","label":"Contrainte 3","x":648,"y":825,"pid":"iR21"},
            {"id":"iR41","lk":"R-4","label":"Licence","x":635,"y":905,"pid":"iR31"},
            {"id":"iR42","lk":"R-4","label":"Conformite","x":285,"y":912,"pid":"iR32"},
            {"id":"iR51","lk":"R-5","label":"Algorithmes","x":668,"y":995,"pid":"iR41"},
            {"id":"iR52","lk":"R-5","label":"Hardware","x":255,"y":1002,"pid":"iR42"},
        ],
        "pw":{"T":4.0,"B":3.5,"b":2.0,"C":1.0,"F":1.2,"R-1":2.5,"R-2":1.8,"R-3":1.2,"R-4":0.8,"R-5":0.5},
    },
    "baobab": {
        "emoji": "🌳", "trunkTopY": 170,
        "nodes": [
            {"id":"iC1","lk":"C","label":"Tests / CI","x":461,"y":95,"pid":None},
            {"id":"iC2","lk":"C","label":"Release / CD","x":440,"y":105,"pid":None},
            {"id":"iF1","lk":"F","label":"API endpoints","x":500,"y":135,"pid":"ib1"},
            {"id":"iF2","lk":"F","label":"UI composants","x":420,"y":140,"pid":"ib2"},
            {"id":"ib1","lk":"b","label":"Sub-mod 1","x":495,"y":170,"pid":"iB1"},
            {"id":"ib2","lk":"b","label":"Sub-mod 2","x":428,"y":175,"pid":"iB2"},
            {"id":"ib3","lk":"b","label":"Sub-mod 3","x":530,"y":185,"pid":"iB3"},
            {"id":"iB1","lk":"B","label":"Module A","x":490,"y":215,"pid":None},
            {"id":"iB2","lk":"B","label":"Module B","x":432,"y":220,"pid":None},
            {"id":"iB3","lk":"B","label":"Module C","x":525,"y":240,"pid":None},
            {"id":"iT1","lk":"T","label":"Core engine","x":461,"y":400,"pid":None},
            {"id":"iR11","lk":"R-1","label":"Framework web","x":530,"y":615,"pid":None},
            {"id":"iR12","lk":"R-1","label":"Framework data","x":392,"y":620,"pid":None},
            {"id":"iR13","lk":"R-1","label":"Framework test","x":568,"y":635,"pid":None},
            {"id":"iR21","lk":"R-2","label":"Archi DB","x":575,"y":710,"pid":"iR11"},
            {"id":"iR22","lk":"R-2","label":"Archi API","x":350,"y":718,"pid":"iR12"},
            {"id":"iR31","lk":"R-3","label":"Contrainte 1","x":615,"y":805,"pid":"iR21"},
            {"id":"iR32","lk":"R-3","label":"Contrainte 2","x":310,"y":812,"pid":"iR22"},
            {"id":"iR33","lk":"R-3","label":"Contrainte 3","x":655,"y":820,"pid":"iR21"},
            {"id":"iR41","lk":"R-4","label":"Licence","x":650,"y":900,"pid":"iR31"},
            {"id":"iR42","lk":"R-4","label":"Conformite","x":268,"y":908,"pid":"iR32"},
            {"id":"iR51","lk":"R-5","label":"Algorithmes","x":685,"y":992,"pid":"iR41"},
            {"id":"iR52","lk":"R-5","label":"Hardware","x":235,"y":1000,"pid":"iR42"},
        ],
        "pw":{"T":7.0,"B":1.2,"b":0.8,"C":0.5,"F":0.6,"R-1":2.5,"R-2":1.8,"R-3":1.2,"R-4":0.8,"R-5":0.5},
    },
    "palmier": {
        "emoji": "🌴", "trunkTopY": 90,
        "nodes": [
            {"id":"iC1","lk":"C","label":"Tests / CI","x":461,"y":80,"pid":None},
            {"id":"iF1","lk":"F","label":"API endpoints","x":350,"y":130,"pid":None},
            {"id":"iF2","lk":"F","label":"UI composants","x":461,"y":120,"pid":None},
            {"id":"iF3","lk":"F","label":"Exports / CLI","x":572,"y":130,"pid":None},
            {"id":"iF4","lk":"F","label":"Webhooks","x":300,"y":160,"pid":None},
            {"id":"iF5","lk":"F","label":"Events","x":622,"y":160,"pid":None},
            {"id":"iT1","lk":"T","label":"Stipe unique","x":461,"y":420,"pid":None},
            {"id":"iR11","lk":"R-1","label":"Framework web","x":520,"y":615,"pid":None},
            {"id":"iR12","lk":"R-1","label":"Framework data","x":402,"y":620,"pid":None},
            {"id":"iR21","lk":"R-2","label":"Archi DB","x":555,"y":715,"pid":"iR11"},
            {"id":"iR22","lk":"R-2","label":"Archi API","x":368,"y":722,"pid":"iR12"},
            {"id":"iR31","lk":"R-3","label":"Contrainte 1","x":590,"y":808,"pid":"iR21"},
            {"id":"iR32","lk":"R-3","label":"Contrainte 2","x":335,"y":815,"pid":"iR22"},
            {"id":"iR41","lk":"R-4","label":"Licence","x":620,"y":900,"pid":"iR31"},
            {"id":"iR42","lk":"R-4","label":"Conformite","x":305,"y":908,"pid":"iR32"},
            {"id":"iR51","lk":"R-5","label":"Algorithmes","x":650,"y":992,"pid":"iR41"},
            {"id":"iR52","lk":"R-5","label":"Hardware","x":275,"y":1000,"pid":"iR42"},
        ],
        "pw":{"T":5.0,"B":0,"b":0,"C":0.5,"F":1.5,"R-1":2.0,"R-2":1.5,"R-3":1.0,"R-4":0.6,"R-5":0.4},
    },
    "buisson": {
        "emoji": "🌿", "trunkTopY": None,
        "nodes": [
            {"id":"iC1","lk":"C","label":"Tests / CI","x":380,"y":100,"pid":"iF1"},
            {"id":"iC2","lk":"C","label":"Release / CD","x":540,"y":105,"pid":"iF3"},
            {"id":"iF1","lk":"F","label":"API endpoints","x":310,"y":175,"pid":"ib1"},
            {"id":"iF2","lk":"F","label":"UI composants","x":461,"y":170,"pid":"ib3"},
            {"id":"iF3","lk":"F","label":"Exports / CLI","x":610,"y":175,"pid":"ib4"},
            {"id":"ib1","lk":"b","label":"Sub-mod 1","x":300,"y":250,"pid":"iB1"},
            {"id":"ib2","lk":"b","label":"Sub-mod 2","x":390,"y":255,"pid":"iB2"},
            {"id":"ib3","lk":"b","label":"Sub-mod 3","x":461,"y":245,"pid":"iB3"},
            {"id":"ib4","lk":"b","label":"Sub-mod 4","x":530,"y":250,"pid":"iB4"},
            {"id":"ib5","lk":"b","label":"Sub-mod 5","x":620,"y":255,"pid":"iB5"},
            {"id":"iB1","lk":"B","label":"Tige A","x":310,"y":390,"pid":None},
            {"id":"iB2","lk":"B","label":"Tige B","x":395,"y":385,"pid":None},
            {"id":"iB3","lk":"B","label":"Tige C","x":461,"y":380,"pid":None},
            {"id":"iB4","lk":"B","label":"Tige D","x":527,"y":385,"pid":None},
            {"id":"iB5","lk":"B","label":"Tige E","x":612,"y":390,"pid":None},
            {"id":"iR11","lk":"R-1","label":"Dep principale","x":461,"y":618,"pid":None},
            {"id":"iR12","lk":"R-1","label":"Framework test","x":560,"y":632,"pid":None},
            {"id":"iR21","lk":"R-2","label":"Archi DB","x":540,"y":718,"pid":"iR11"},
            {"id":"iR22","lk":"R-2","label":"Archi API","x":382,"y":725,"pid":"iR11"},
            {"id":"iR31","lk":"R-3","label":"Contrainte 1","x":575,"y":808,"pid":"iR21"},
            {"id":"iR32","lk":"R-3","label":"Contrainte 2","x":348,"y":815,"pid":"iR22"},
            {"id":"iR41","lk":"R-4","label":"Licence","x":608,"y":900,"pid":"iR31"},
            {"id":"iR42","lk":"R-4","label":"Conformite","x":315,"y":908,"pid":"iR32"},
            {"id":"iR51","lk":"R-5","label":"Algorithmes","x":640,"y":992,"pid":"iR41"},
            {"id":"iR52","lk":"R-5","label":"Hardware","x":282,"y":1000,"pid":"iR42"},
        ],
        "pw":{"T":0,"B":2.0,"b":1.2,"C":0.8,"F":1.0,"R-1":2.5,"R-2":1.8,"R-3":1.0,"R-4":0.6,"R-5":0.4},
    },
    "liane": {
        "emoji": "🌱", "trunkTopY": 90,
        "nodes": [
            {"id":"iC1","lk":"C","label":"Tests / CI","x":461,"y":100,"pid":None},
            {"id":"iC2","lk":"C","label":"Release / CD","x":430,"y":115,"pid":None},
            {"id":"iF1","lk":"F","label":"API endpoints","x":400,"y":185,"pid":"ib1"},
            {"id":"iF2","lk":"F","label":"UI composants","x":520,"y":190,"pid":"ib2"},
            {"id":"iF3","lk":"F","label":"Exports / CLI","x":360,"y":215,"pid":"ib3"},
            {"id":"ib1","lk":"b","label":"Vrille 1","x":415,"y":275,"pid":"iB1"},
            {"id":"ib2","lk":"b","label":"Vrille 2","x":505,"y":280,"pid":"iB2"},
            {"id":"ib3","lk":"b","label":"Vrille 3","x":380,"y":310,"pid":"iB1"},
            {"id":"iB1","lk":"B","label":"Fork A","x":430,"y":395,"pid":None},
            {"id":"iB2","lk":"B","label":"Fork B","x":490,"y":400,"pid":None},
            {"id":"iT1","lk":"T","label":"Tige principale","x":461,"y":510,"pid":None},
            {"id":"iR11","lk":"R-1","label":"Framework web","x":500,"y":625,"pid":None},
            {"id":"iR12","lk":"R-1","label":"Framework data","x":422,"y":630,"pid":None},
            {"id":"iR21","lk":"R-2","label":"Archi DB","x":530,"y":725,"pid":"iR11"},
            {"id":"iR22","lk":"R-2","label":"Archi API","x":395,"y":732,"pid":"iR12"},
            {"id":"iR31","lk":"R-3","label":"Contrainte 1","x":560,"y":815,"pid":"iR21"},
            {"id":"iR32","lk":"R-3","label":"Contrainte 2","x":365,"y":822,"pid":"iR22"},
            {"id":"iR41","lk":"R-4","label":"Licence","x":590,"y":908,"pid":"iR31"},
            {"id":"iR42","lk":"R-4","label":"Conformite","x":335,"y":915,"pid":"iR32"},
            {"id":"iR51","lk":"R-5","label":"Algorithmes","x":620,"y":998,"pid":"iR41"},
            {"id":"iR52","lk":"R-5","label":"Hardware","x":305,"y":1005,"pid":"iR42"},
        ],
        "pw":{"T":1.5,"B":1.2,"b":1.0,"C":0.6,"F":0.8,"R-1":1.5,"R-2":1.2,"R-3":0.8,"R-4":0.5,"R-5":0.3},
    },
}

# ChatGPT raw image filenames
RAW_IMAGES = {
    "conifere": "conifere_chatgpt_raw.png",
    "feuillu": "feuillu_chatgpt_raw.png",
    "baobab": "baobab_chatgpt_raw.png",
    "palmier": "palmier_chatgpt_raw.png",
    "buisson": "buisson_chatgpt_raw.png",
    "liane": "liane_chatgpt_raw.png",
}


def quadratic_bezier(p0, p1, p2, steps=50):
    pts = []
    for i in range(steps + 1):
        t = i / steps
        x = (1-t)**2*p0[0] + 2*(1-t)*t*p1[0] + t**2*p2[0]
        y = (1-t)**2*p0[1] + 2*(1-t)*t*p1[1] + t**2*p2[1]
        pts.append((x, y))
    return pts


def gen_skeleton(family_name, fam):
    """Genere le squelette sur fond noir."""
    img = Image.new("RGBA", (TGT_W, TGT_H), (5, 8, 5, 255))
    draw = ImageDraw.Draw(img)

    # Scale nodes
    nodes = []
    for n in fam["nodes"]:
        nodes.append({**n, "x": sx(n["x"]), "y": sy(n["y"])})

    iPos = {n["id"]: (n["x"], n["y"]) for n in nodes}
    pw = fam["pw"]

    # Ligne de sol
    draw.line([(0, SOL_Y), (TGT_W, SOL_Y)], fill=(180, 140, 20, 180), width=2)

    # Axe central
    draw.line([(CENTER_X, 0), (CENTER_X, TGT_H)], fill=(180, 140, 20, 60), width=1)

    # Bandes horizontales
    all_lks = AERIAL_LKS + UNDER_LKS
    for lk in all_lks:
        by = BAND_Y[lk]
        draw.line([(0, by), (TGT_W, by)], fill=(255, 255, 255, 30), width=1)

    # Tronc
    trunkTopY = fam.get("trunkTopY")
    if trunkTopY is not None:
        trunkW = pw.get("T", 0)
        if trunkW > 0:
            tw = int(trunkW * 2.5)
            draw.line(
                [(CENTER_X, sy(trunkTopY)), (CENTER_X, SOL_Y)],
                fill=(255, 255, 255, 120), width=tw
            )

    # Connexions: branches vers tronc ou sol
    for n in nodes:
        nid = n["id"]
        nx, ny = n["x"], n["y"]
        lk = n["lk"]
        pid = n.get("pid")

        # Connexion vers parent
        if pid and pid in iPos:
            px, py = iPos[pid]
            # Courbe bezier
            midx = (nx + px) / 2
            midy = (ny + py) / 2
            cp = (midx + (CENTER_X - midx) * 0.3, midy)
            pts = quadratic_bezier((nx, ny), cp, (px, py), steps=40)
            w = max(1, int(pw.get(lk, 1) * 1.2))
            for i in range(len(pts)-1):
                draw.line([pts[i], pts[i+1]], fill=(255, 255, 255, 80), width=w)
        else:
            # Branches/tiges vers le centre (sol ou tronc)
            if lk in ("B", "T") or (lk.startswith("R") and not pid):
                target_y = SOL_Y
                target_x = CENTER_X
                cp = ((nx + target_x) / 2, (ny + target_y) / 2)
                pts = quadratic_bezier((nx, ny), cp, (target_x, target_y), steps=40)
                w = max(1, int(pw.get(lk, 1) * 1.5))
                for i in range(len(pts)-1):
                    draw.line([pts[i], pts[i+1]], fill=(255, 255, 255, 60), width=w)

    # Noeuds
    for n in nodes:
        nx, ny = n["x"], n["y"]
        lk = n["lk"]
        r = max(4, int(pw.get(lk, 1) * 5))
        col = COLORS.get(lk.split("-")[0] if "-" in lk else lk, (255, 255, 255))
        draw.ellipse([(nx-r, ny-r), (nx+r, ny+r)], fill=(255, 255, 255, 220))

    return img, nodes


def gen_overlay(family_name, fam, nodes):
    """Plaque le squelette semi-transparent sur l'image ChatGPT."""
    raw_path = os.path.join(TEMPLATES, RAW_IMAGES.get(family_name, ""))
    if not os.path.exists(raw_path):
        print(f"    !! Image raw manquante: {raw_path}")
        return None

    bg = Image.open(raw_path).convert("RGBA")
    if bg.size != (TGT_W, TGT_H):
        bg = bg.resize((TGT_W, TGT_H), Image.LANCZOS)

    overlay = Image.new("RGBA", (TGT_W, TGT_H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    pw = fam["pw"]
    iPos = {n["id"]: (n["x"], n["y"]) for n in nodes}

    # Bandes
    all_lks = AERIAL_LKS + UNDER_LKS
    for lk in all_lks:
        by = BAND_Y[lk]
        draw.line([(0, by), (TGT_W, by)], fill=(255, 180, 50, 40), width=1)

    # Ligne de sol
    draw.line([(0, SOL_Y), (TGT_W, SOL_Y)], fill=(200, 160, 30, 100), width=2)

    # Axe central
    draw.line([(CENTER_X, 0), (CENTER_X, TGT_H)], fill=(200, 160, 30, 40), width=1)

    # Connexions
    for n in nodes:
        pid = n.get("pid")
        if pid and pid in iPos:
            nx, ny = n["x"], n["y"]
            px, py = iPos[pid]
            midx = (nx + px) / 2
            midy = (ny + py) / 2
            cp = (midx + (CENTER_X - midx) * 0.3, midy)
            pts = quadratic_bezier((nx, ny), cp, (px, py), steps=40)
            w = max(1, int(pw.get(n["lk"], 1) * 1.0))
            for i in range(len(pts)-1):
                draw.line([pts[i], pts[i+1]], fill=(255, 255, 255, 50), width=w)

    # Noeuds + labels
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 11)
    except:
        font = ImageFont.load_default()

    for n in nodes:
        nx, ny = n["x"], n["y"]
        lk = n["lk"]
        r = max(3, int(pw.get(lk, 1) * 4))

        # Noeud ambre
        draw.ellipse(
            [(nx-r, ny-r), (nx+r, ny+r)],
            fill=(220, 170, 40, 180),
            outline=(255, 200, 50, 220),
            width=1
        )

        # Label
        label = n["label"]
        tw = draw.textlength(label, font=font) if hasattr(draw, 'textlength') else len(label) * 7
        tx = nx - tw / 2
        ty = ny - r - 14

        # Fond label
        draw.rectangle(
            [(tx - 2, ty - 1), (tx + tw + 2, ty + 13)],
            fill=(0, 0, 0, 140)
        )
        draw.text((tx, ty), label, fill=(220, 200, 160, 220), font=font)

    # Compositer
    result = Image.alpha_composite(bg, overlay)
    return result


def gen_positions_file(family_name, nodes):
    """Genere le fichier de positions (comme buisson_positions_1024.txt)."""
    lines = [f"# Positions {family_name} scalees 1024x1536"]
    lines.append(f"# CENTER_X={CENTER_X}, SOL_Y={SOL_Y}")
    for n in nodes:
        lines.append(f"{n['id']:<8s} {n['label']:<22s} x={n['x']:>4d}  y={n['y']:>4d}")
    return "\n".join(lines)


def main():
    print(f"\n  GENERATION DES SQUELETTES + OVERLAYS")
    print(f"  {'=' * 50}")

    for fname, fam in FAMILIES.items():
        print(f"\n  {fam['emoji']} {fname.upper()}")

        # 1. Squelette
        skel_img, scaled_nodes = gen_skeleton(fname, fam)
        skel_path = os.path.join(TEMPLATES, f"{fname}_skeleton_1024x1536.png")
        skel_img.save(skel_path)
        print(f"    skeleton: {skel_path}")

        # 2. Positions
        pos_text = gen_positions_file(fname, scaled_nodes)
        pos_path = os.path.join(TEMPLATES, f"{fname}_positions_1024.txt")
        with open(pos_path, "w", encoding="utf-8") as f:
            f.write(pos_text)
        print(f"    positions: {pos_path}")

        # 3. Overlay
        overlay_img = gen_overlay(fname, fam, scaled_nodes)
        if overlay_img:
            final_path = os.path.join(TEMPLATES, f"{fname}_final.png")
            overlay_img.save(final_path)
            print(f"    final: {final_path}")
        else:
            print(f"    final: SKIP (image raw manquante)")

    print(f"\n  {'=' * 50}")
    print(f"  TERMINE — 6 squelettes + 6 overlays + 6 positions")


if __name__ == "__main__":
    main()
