#!/usr/bin/env python3
"""Patch interactive_profile.html with 6 family skeletons."""
import sys

REPLACEMENT = r'''  // ═══════════════════════════════════════════════════════════
  //  SQUELETTES PARFAITS — 6 FAMILLES BOTANIQUES
  //  Basé sur thèses PhD (ISA, Bebber, Boswell, Lindenmayer)
  //  Chaque nœud a un parent explicite → zéro croisement.
  // ═══════════════════════════════════════════════════════════

  const _F = {
    // ─────────────────── CONIFÈRE 🌲 ───────────────────
    // Pyramidal, tronc dominant, subordination stricte
    // C1:TRUNK_FIRST C2:BRANCH_SUB<0.6 C3:TOP_DOWN C4:NO_RECOVERY
    conifere: {
      trunkTopY: 90,
      nodes: [
        { id:"iC1", lk:"C", label:"Tests / CI",       x:476, y:112, pid:null },
        { id:"iC2", lk:"C", label:"Release / CD",     x:446, y:118, pid:null },
        { id:"iF1", lk:"F", label:"API endpoints",    x:505, y:188, pid:"ib1" },
        { id:"iF2", lk:"F", label:"UI composants",    x:418, y:193, pid:"ib3" },
        { id:"iF3", lk:"F", label:"Exports / CLI",    x:538, y:218, pid:"ib5" },
        { id:"iB1", lk:"B", label:"Module A",         x:490, y:392, pid:null },
        { id:"iB2", lk:"B", label:"Module B",         x:432, y:397, pid:null },
        { id:"iB3", lk:"B", label:"Module C",         x:515, y:450, pid:null },
        { id:"iB4", lk:"B", label:"Module D",         x:408, y:455, pid:null },
        { id:"ib1", lk:"b", label:"Sub-mod 1",        x:520, y:278, pid:"iB1" },
        { id:"ib2", lk:"b", label:"Sub-mod 2",        x:555, y:308, pid:"iB1" },
        { id:"ib3", lk:"b", label:"Sub-mod 3",        x:400, y:283, pid:"iB2" },
        { id:"ib4", lk:"b", label:"Sub-mod 4",        x:368, y:312, pid:"iB2" },
        { id:"ib5", lk:"b", label:"Sub-mod 5",        x:580, y:342, pid:"iB3" },
        { id:"ib6", lk:"b", label:"Sub-mod 6",        x:345, y:348, pid:"iB4" },
        { id:"iT1", lk:"T", label:"Core pipeline",    x:461, y:530, pid:null },
        { id:"iR11", lk:"R-1", label:"Framework web",   x:505, y:612, pid:null },
        { id:"iR12", lk:"R-1", label:"Framework data",  x:418, y:618, pid:null },
        { id:"iR13", lk:"R-1", label:"Framework test",  x:545, y:638, pid:null },
        { id:"iR21", lk:"R-2", label:"Archi DB",        x:548, y:712, pid:"iR11" },
        { id:"iR22", lk:"R-2", label:"Archi API",       x:375, y:720, pid:"iR12" },
        { id:"iR31", lk:"R-3", label:"Contrainte 1",    x:580, y:800, pid:"iR21" },
        { id:"iR32", lk:"R-3", label:"Contrainte 2",    x:345, y:808, pid:"iR22" },
        { id:"iR33", lk:"R-3", label:"Contrainte 3",    x:628, y:815, pid:"iR21" },
        { id:"iR41", lk:"R-4", label:"Licence",         x:612, y:895, pid:"iR31" },
        { id:"iR42", lk:"R-4", label:"Conformite",      x:312, y:902, pid:"iR32" },
        { id:"iR51", lk:"R-5", label:"Algorithmes",     x:645, y:988, pid:"iR41" },
        { id:"iR52", lk:"R-5", label:"Hardware",        x:278, y:995, pid:"iR42" },
      ],
      pw: { "T":4.0,"B":2.5,"b":1.5,"C":1.0,"F":1.2,"R-1":2.5,"R-2":1.8,"R-3":1.2,"R-4":0.8,"R-5":0.5 },
      nr: { "T":33,"B":23,"b":15,"F":12,"C":11,"R-1":23,"R-2":18,"R-3":12,"R-4":8,"R-5":6 },
    },

    // ─────────────────── FEUILLU 🌳 ───────────────────
    // Arrondi/décurrent, branches co-dominantes, tronc COURT
    // F1:BRANCH_FIRST F2:LATERAL_FREEDOM F3:DECURRENT F4:RECOVERY
    feuillu: {
      trunkTopY: 200,
      nodes: [
        { id:"iC1", lk:"C", label:"Tests / CI",       x:461, y:100, pid:null },
        { id:"iC2", lk:"C", label:"Release / CD",     x:390, y:120, pid:null },
        { id:"iC3", lk:"C", label:"Monitoring",        x:530, y:120, pid:null },
        { id:"iF1", lk:"F", label:"API endpoints",    x:340, y:190, pid:"ib1" },
        { id:"iF2", lk:"F", label:"UI composants",    x:461, y:180, pid:"ib3" },
        { id:"iF3", lk:"F", label:"Exports / CLI",    x:580, y:190, pid:"ib4" },
        { id:"iF4", lk:"F", label:"Webhooks",          x:280, y:215, pid:"ib2" },
        { id:"ib1", lk:"b", label:"Sub-mod 1",        x:330, y:260, pid:"iB1" },
        { id:"ib2", lk:"b", label:"Sub-mod 2",        x:255, y:285, pid:"iB2" },
        { id:"ib3", lk:"b", label:"Sub-mod 3",        x:461, y:255, pid:"iB3" },
        { id:"ib4", lk:"b", label:"Sub-mod 4",        x:595, y:260, pid:"iB4" },
        { id:"ib5", lk:"b", label:"Sub-mod 5",        x:665, y:285, pid:"iB5" },
        { id:"ib6", lk:"b", label:"Sub-mod 6",        x:385, y:275, pid:"iB1" },
        { id:"iB1", lk:"B", label:"Module A",         x:365, y:385, pid:null },
        { id:"iB2", lk:"B", label:"Module B",         x:275, y:415, pid:"iB1" },
        { id:"iB3", lk:"B", label:"Module C",         x:461, y:375, pid:null },
        { id:"iB4", lk:"B", label:"Module D",         x:555, y:385, pid:null },
        { id:"iB5", lk:"B", label:"Module E",         x:645, y:415, pid:"iB4" },
        { id:"iT1", lk:"T", label:"Core engine",      x:461, y:500, pid:null },
        { id:"iR11", lk:"R-1", label:"Framework web",   x:520, y:618, pid:null },
        { id:"iR12", lk:"R-1", label:"Framework data",  x:400, y:622, pid:null },
        { id:"iR13", lk:"R-1", label:"Framework test",  x:580, y:640, pid:null },
        { id:"iR21", lk:"R-2", label:"Archi DB",        x:560, y:720, pid:"iR11" },
        { id:"iR22", lk:"R-2", label:"Archi API",       x:355, y:728, pid:"iR12" },
        { id:"iR31", lk:"R-3", label:"Contrainte 1",    x:600, y:810, pid:"iR21" },
        { id:"iR32", lk:"R-3", label:"Contrainte 2",    x:320, y:818, pid:"iR22" },
        { id:"iR33", lk:"R-3", label:"Contrainte 3",    x:648, y:825, pid:"iR21" },
        { id:"iR41", lk:"R-4", label:"Licence",         x:635, y:905, pid:"iR31" },
        { id:"iR42", lk:"R-4", label:"Conformite",      x:285, y:912, pid:"iR32" },
        { id:"iR51", lk:"R-5", label:"Algorithmes",     x:668, y:995, pid:"iR41" },
        { id:"iR52", lk:"R-5", label:"Hardware",        x:255, y:1002, pid:"iR42" },
      ],
      pw: { "T":4.0,"B":3.5,"b":2.0,"C":1.0,"F":1.2,"R-1":2.5,"R-2":1.8,"R-3":1.2,"R-4":0.8,"R-5":0.5 },
      nr: { "T":30,"B":26,"b":15,"F":12,"C":10,"R-1":22,"R-2":16,"R-3":12,"R-4":7,"R-5":5 },
    },

    // ─────────────────── BAOBAB 🫚 ───────────────────
    // Tronc MASSIF (60-80% biomasse), couronne minuscule
    // B1:TRUNK_DOMINANT B2:SMALL_CROWN B3:SLOW_GROWTH B4:BARK_REGEN
    baobab: {
      trunkTopY: 170,
      nodes: [
        { id:"iC1", lk:"C", label:"Tests / CI",       x:461, y:95,  pid:null },
        { id:"iC2", lk:"C", label:"Release / CD",     x:440, y:105, pid:null },
        { id:"iF1", lk:"F", label:"API endpoints",    x:500, y:135, pid:"ib1" },
        { id:"iF2", lk:"F", label:"UI composants",    x:420, y:140, pid:"ib2" },
        { id:"ib1", lk:"b", label:"Sub-mod 1",        x:495, y:170, pid:"iB1" },
        { id:"ib2", lk:"b", label:"Sub-mod 2",        x:428, y:175, pid:"iB2" },
        { id:"ib3", lk:"b", label:"Sub-mod 3",        x:530, y:185, pid:"iB3" },
        { id:"iB1", lk:"B", label:"Module A",         x:490, y:215, pid:null },
        { id:"iB2", lk:"B", label:"Module B",         x:432, y:220, pid:null },
        { id:"iB3", lk:"B", label:"Module C",         x:525, y:240, pid:null },
        { id:"iT1", lk:"T", label:"Core engine",      x:461, y:400, pid:null },
        { id:"iR11", lk:"R-1", label:"Framework web",   x:530, y:615, pid:null },
        { id:"iR12", lk:"R-1", label:"Framework data",  x:392, y:620, pid:null },
        { id:"iR13", lk:"R-1", label:"Framework test",  x:568, y:635, pid:null },
        { id:"iR21", lk:"R-2", label:"Archi DB",        x:575, y:710, pid:"iR11" },
        { id:"iR22", lk:"R-2", label:"Archi API",       x:350, y:718, pid:"iR12" },
        { id:"iR31", lk:"R-3", label:"Contrainte 1",    x:615, y:805, pid:"iR21" },
        { id:"iR32", lk:"R-3", label:"Contrainte 2",    x:310, y:812, pid:"iR22" },
        { id:"iR33", lk:"R-3", label:"Contrainte 3",    x:655, y:820, pid:"iR21" },
        { id:"iR41", lk:"R-4", label:"Licence",         x:650, y:900, pid:"iR31" },
        { id:"iR42", lk:"R-4", label:"Conformite",      x:268, y:908, pid:"iR32" },
        { id:"iR51", lk:"R-5", label:"Algorithmes",     x:685, y:992, pid:"iR41" },
        { id:"iR52", lk:"R-5", label:"Hardware",        x:235, y:1000, pid:"iR42" },
      ],
      pw: { "T":7.0,"B":1.2,"b":0.8,"C":0.5,"F":0.6,"R-1":2.5,"R-2":1.8,"R-3":1.2,"R-4":0.8,"R-5":0.5 },
      nr: { "T":45,"B":12,"b":8,"F":6,"C":5,"R-1":20,"R-2":15,"R-3":10,"R-4":6,"R-5":4 },
    },

    // ─────────────────── PALMIER 🌴 ───────────────────
    // Colonnaire, UN méristème, ZÉRO branche
    // P1:SINGLE_MERISTEM P2:NO_BRANCHES P3:NO_SECONDARY P4:CROWN_SHAFT
    palmier: {
      trunkTopY: 150,
      nodes: [
        { id:"iC1", lk:"C", label:"Tests / CI",       x:461, y:98,  pid:null },
        { id:"iF1", lk:"F", label:"Crown shaft",      x:461, y:135, pid:"iC1" },
        { id:"iF2", lk:"F", label:"API endpoints",    x:380, y:160, pid:"iF1" },
        { id:"iF3", lk:"F", label:"UI composants",    x:540, y:160, pid:"iF1" },
        { id:"iF4", lk:"F", label:"Exports / CLI",    x:330, y:185, pid:"iF1" },
        { id:"iF5", lk:"F", label:"Webhooks",          x:590, y:185, pid:"iF1" },
        { id:"iT1", lk:"T", label:"Core engine",      x:461, y:380, pid:null },
        { id:"iR11", lk:"R-1", label:"Framework web",   x:510, y:620, pid:null },
        { id:"iR12", lk:"R-1", label:"Framework data",  x:412, y:625, pid:null },
        { id:"iR13", lk:"R-1", label:"Framework test",  x:548, y:642, pid:null },
        { id:"iR21", lk:"R-2", label:"Archi DB",        x:545, y:718, pid:"iR11" },
        { id:"iR22", lk:"R-2", label:"Archi API",       x:378, y:725, pid:"iR12" },
        { id:"iR31", lk:"R-3", label:"Contrainte 1",    x:585, y:810, pid:"iR21" },
        { id:"iR32", lk:"R-3", label:"Contrainte 2",    x:340, y:818, pid:"iR22" },
        { id:"iR41", lk:"R-4", label:"Licence",         x:620, y:905, pid:"iR31" },
        { id:"iR42", lk:"R-4", label:"Conformite",      x:305, y:912, pid:"iR32" },
        { id:"iR51", lk:"R-5", label:"Algorithmes",     x:655, y:995, pid:"iR41" },
        { id:"iR52", lk:"R-5", label:"Hardware",        x:270, y:1002, pid:"iR42" },
      ],
      pw: { "T":4.0,"B":0,"b":0,"C":1.5,"F":1.0,"R-1":2.0,"R-2":1.5,"R-3":1.0,"R-4":0.7,"R-5":0.4 },
      nr: { "T":35,"B":0,"b":0,"C":15,"F":10,"R-1":18,"R-2":14,"R-3":10,"R-4":7,"R-5":5 },
    },

    // ─────────────────── BUISSON 🌿 ───────────────────
    // Multi-tiges, PAS de tronc central, tiges = branches
    // Bu1:NO_CENTRAL_TRUNK Bu2:BASAL_SPROUTING Bu3:REJUVENATION Bu4:REDUNDANCY
    buisson: {
      trunkTopY: null,
      nodes: [
        { id:"iC1", lk:"C", label:"Tests / CI",       x:350, y:98,  pid:null },
        { id:"iC2", lk:"C", label:"Release / CD",     x:461, y:92,  pid:null },
        { id:"iC3", lk:"C", label:"Monitoring",        x:572, y:98,  pid:null },
        { id:"iF1", lk:"F", label:"API endpoints",    x:310, y:180, pid:"ib1" },
        { id:"iF2", lk:"F", label:"UI composants",    x:461, y:170, pid:"ib2" },
        { id:"iF3", lk:"F", label:"Exports / CLI",    x:610, y:180, pid:"ib4" },
        { id:"ib1", lk:"b", label:"Sub-mod 1",        x:330, y:260, pid:"iB1" },
        { id:"ib2", lk:"b", label:"Sub-mod 2",        x:430, y:255, pid:"iB2" },
        { id:"ib3", lk:"b", label:"Sub-mod 3",        x:490, y:255, pid:"iB3" },
        { id:"ib4", lk:"b", label:"Sub-mod 4",        x:590, y:260, pid:"iB4" },
        { id:"iB1", lk:"B", label:"Tige A",           x:340, y:390, pid:"iT1" },
        { id:"iB2", lk:"B", label:"Tige B",           x:420, y:385, pid:"iT1" },
        { id:"iB3", lk:"B", label:"Tige C",           x:500, y:385, pid:"iT1" },
        { id:"iB4", lk:"B", label:"Tige D",           x:580, y:390, pid:"iT1" },
        { id:"iT1", lk:"T", label:"Base / Collet",    x:461, y:530, pid:null },
        { id:"iR11", lk:"R-1", label:"Framework web",   x:530, y:620, pid:null },
        { id:"iR12", lk:"R-1", label:"Framework data",  x:392, y:625, pid:null },
        { id:"iR13", lk:"R-1", label:"Framework test",  x:570, y:640, pid:null },
        { id:"iR21", lk:"R-2", label:"Archi DB",        x:565, y:720, pid:"iR11" },
        { id:"iR22", lk:"R-2", label:"Archi API",       x:358, y:728, pid:"iR12" },
        { id:"iR31", lk:"R-3", label:"Contrainte 1",    x:605, y:810, pid:"iR21" },
        { id:"iR32", lk:"R-3", label:"Contrainte 2",    x:320, y:818, pid:"iR22" },
        { id:"iR41", lk:"R-4", label:"Licence",         x:640, y:905, pid:"iR31" },
        { id:"iR42", lk:"R-4", label:"Conformite",      x:285, y:912, pid:"iR32" },
        { id:"iR51", lk:"R-5", label:"Algorithmes",     x:675, y:995, pid:"iR41" },
        { id:"iR52", lk:"R-5", label:"Hardware",        x:250, y:1002, pid:"iR42" },
      ],
      pw: { "T":2.0,"B":2.0,"b":1.5,"C":0.8,"F":1.0,"R-1":2.0,"R-2":1.5,"R-3":1.0,"R-4":0.7,"R-5":0.4 },
      nr: { "T":20,"B":20,"b":12,"F":10,"C":8,"R-1":18,"R-2":14,"R-3":10,"R-4":7,"R-5":5 },
    },

    // ─────────────────── LIANE 🌱 ───────────────────
    // Grimpante, mince, dépend de l'hôte, pas de structure porteuse
    // L1:HOST_DEPENDENT L2:NO_STRUCTURAL_COST L3:PARASITIC L4:DIES_WITH_HOST
    liane: {
      trunkTopY: 90,
      nodes: [
        { id:"iC1", lk:"C", label:"Tests / CI",       x:461, y:100, pid:null },
        { id:"iC2", lk:"C", label:"Release / CD",     x:430, y:115, pid:null },
        { id:"iF1", lk:"F", label:"API endpoints",    x:400, y:185, pid:"ib1" },
        { id:"iF2", lk:"F", label:"UI composants",    x:520, y:190, pid:"ib2" },
        { id:"iF3", lk:"F", label:"Exports / CLI",    x:360, y:215, pid:"ib3" },
        { id:"ib1", lk:"b", label:"Vrille 1",         x:415, y:275, pid:"iB1" },
        { id:"ib2", lk:"b", label:"Vrille 2",         x:505, y:280, pid:"iB2" },
        { id:"ib3", lk:"b", label:"Vrille 3",         x:380, y:310, pid:"iB1" },
        { id:"iB1", lk:"B", label:"Fork A",           x:430, y:395, pid:null },
        { id:"iB2", lk:"B", label:"Fork B",           x:490, y:400, pid:null },
        { id:"iT1", lk:"T", label:"Tige principale",  x:461, y:510, pid:null },
        { id:"iR11", lk:"R-1", label:"Framework web",   x:500, y:625, pid:null },
        { id:"iR12", lk:"R-1", label:"Framework data",  x:422, y:630, pid:null },
        { id:"iR21", lk:"R-2", label:"Archi DB",        x:530, y:725, pid:"iR11" },
        { id:"iR22", lk:"R-2", label:"Archi API",       x:395, y:732, pid:"iR12" },
        { id:"iR31", lk:"R-3", label:"Contrainte 1",    x:560, y:815, pid:"iR21" },
        { id:"iR32", lk:"R-3", label:"Contrainte 2",    x:365, y:822, pid:"iR22" },
        { id:"iR41", lk:"R-4", label:"Licence",         x:590, y:908, pid:"iR31" },
        { id:"iR42", lk:"R-4", label:"Conformite",      x:335, y:915, pid:"iR32" },
        { id:"iR51", lk:"R-5", label:"Algorithmes",     x:620, y:998, pid:"iR41" },
        { id:"iR52", lk:"R-5", label:"Hardware",        x:305, y:1005, pid:"iR42" },
      ],
      pw: { "T":1.5,"B":1.2,"b":1.0,"C":0.6,"F":0.8,"R-1":1.5,"R-2":1.2,"R-3":0.8,"R-4":0.5,"R-5":0.3 },
      nr: { "T":15,"B":12,"b":10,"F":8,"C":6,"R-1":12,"R-2":10,"R-3":8,"R-4":5,"R-5":4 },
    },
  };

  // ── Sélection du squelette actif ──
  const skel = _F[family] || _F.conifere;
  const idealTree = skel.nodes;
  const PIPE_WIDTH = skel.pw;
  const NODE_R = skel.nr;

  // Positions = coordonnées pixel directes
  const iPos = {};
  idealTree.forEach(n => { iPos[n.id] = { x: n.x, y: n.y }; });

  // ────── RENDER: TRONC (pipe model, adapté par famille) ──────
  if (skel.trunkTopY !== null) {
    svgHTML += `<line x1="${CENTER_X}" y1="${skel.trunkTopY}" x2="${CENTER_X}" y2="${SOL_Y}"
      stroke="rgba(255,255,255,0.5)" stroke-width="${PIPE_WIDTH['T']}"/>`;
  }
  svgHTML += `<line x1="${CENTER_X}" y1="${SOL_Y}" x2="${CENTER_X}" y2="600"
    stroke="rgba(255,255,255,0.35)" stroke-width="${PIPE_WIDTH['T'] * 0.85}"/>`;

  // ────── RENDER: CONNEXIONS (pipe model — épaisseur proportionnelle) ──────
  idealTree.forEach(n => {
    const pos = iPos[n.id];
    if (!pos || n.lk === "T") return;

    let pp;
    if (n.pid && iPos[n.pid]) { pp = iPos[n.pid]; }
    else if (n.lk === "R-1") { pp = { x: CENTER_X, y: SOL_Y + 15 }; }
    else { pp = { x: CENTER_X, y: n.y - 15 }; }

    const cx = pp.x + (pos.x - pp.x) * 0.55;
    const cy = pp.y + (pos.y - pp.y) * 0.3;
    const sw = PIPE_WIDTH[n.lk] || 1.0;

    svgHTML += `<path d="M${pp.x},${pp.y} Q${cx},${cy} ${pos.x},${pos.y}"
      fill="none" stroke="rgba(255,255,255,0.45)" stroke-width="${sw}"/>`;
  });'''

with open('templates/interactive_profile.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the section to replace
start_marker = '  // \u2550' * 1  # Start of ═══ line
# More precise: find SQUELETTE PARFAIT
idx1 = content.find('SQUELETTE PARFAIT DU CONIF')
if idx1 == -1:
    print("ERROR: start marker not found")
    sys.exit(1)
# Go back to start of that line
idx1 = content.rfind('\n', 0, idx1) + 1

# Find end: the closing of NODE_R
end_marker = '"R-5":  6,   // mycorhizes (les plus petits)\n  };'
idx2 = content.find(end_marker)
if idx2 == -1:
    print("ERROR: end marker not found")
    sys.exit(1)
idx2 += len(end_marker)

print(f"Replacing chars {idx1} to {idx2} ({idx2 - idx1} chars)")

new_content = content[:idx1] + REPLACEMENT + content[idx2:]

with open('templates/interactive_profile.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("OK - 6 family skeletons patched successfully")
