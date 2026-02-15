# HANDOFF — Winter Tree Visual Renderer v1

> **Date** : 2026-02-15
> **Engine** : 3401 lignes — `engine.py` à la racine
> **Repo** : github.com/sky1241/tree
> **Branche** : main

---

## CONTEXTE PROJET

Winter Tree Engine = framework bio-inspiré de gestion de projets logiciels.
Chaque projet est un arbre avec 10 niveaux anatomiques (5 aériens, 5 souterrains).
Le moteur sait déjà : scanner un repo, classifier la famille (conifère/baobab/feuillu/buisson),
calculer l'échelle (hauteur=code, épaisseur=data), mesurer la confidence par noeud,
générer des prompts de recherche, et suivre l'avancement (guardian).

**Ce qui manque** : la couche visuelle. Transformer le JSON du scanner en rendu graphique.

---

## STRUCTURE REPO (clean, pushé)

```
tree/
├── engine.py                    # Moteur principal (3401L)
├── README.md
├── LICENSE
├── winter_tree_kb.json
├── assets/
│   └── winter_tree_planche_II.png   # Image référence ChatGPT/DALL-E
├── docs/                        # Théorie (ANATOMIE, GROWTH_PATTERNS, PROTOCOLE, RECHERCHE)
├── scans/                       # Arbres scannés (JSON + MD)
├── mycelium/                    # [v2] NE PAS TOUCHER
├── prompts/
└── workflows/
    └── HANDOFF_RENDERER_V1.md   # CE FICHIER
```

---

## IMAGE RÉFÉRENCE — Planche II

Fichier : `assets/winter_tree_planche_II.png` (922×1244px)
Générée par ChatGPT/DALL-E. C'est LE style visuel cible pour tous les arbres.

### Description précise :
- **Fond** : noir texturé, léger grain
- **Split vertical** : gauche = squelette (branches nues blanc/crème), droite = chair (feuillage vert conifère)
- **Canopée** : forme conifère, 4 tiers triangulaires superposés
- **Tronc** : central, blanc côté squelette, brun-vert côté chair
- **SOL** : ligne horizontale dorée/ambrée à ~43% du haut
- **Racines** : s'étalent largement, plus volumineuses que la canopée (ratio 60/40)
- **Mycorhizes** : en bas, petits champignons reliés par des lignes courbes en pointillés
- **Séparateurs** : 9 lignes horizontales blanches en pointillés (entre chaque niveau)
- **Point lumineux vert** : sommet de la cime
- **Texte** : titre "WINTER TREE" en haut, "Anatomie Conifère — Planche II"
- **Footer** : "RACINES > ARBRE — 2026"

### Positions Y des 10 niveaux (approximatif sur 1244px) :
| Niveau | Nom | Y approx | Zone |
|--------|-----|----------|------|
| +5 | CIME | 100 | Aérien |
| +4 | FEUILLES | 215 | Aérien |
| +3 | RAMEAUX | 330 | Aérien |
| +2 | BRANCHES | 440 | Aérien |
| +1 | TRONC | 530 | Aérien |
| — | SOL | 575 | Séparateur |
| -1 | R.STRUCTURELLES | 650 | Souterrain |
| -2 | R.PIVOTANTES | 760 | Souterrain |
| -3 | RADICELLES | 870 | Souterrain |
| -4 | POILS ABSORBANTS | 960 | Souterrain |
| -5 | MYCORHIZES | 1060 | Souterrain |

### Palette couleurs :
- Aérien : #28c862 (cime) → #32b555 → #38a048 → #3d8a3a → #5a9a35 (tronc)
- SOL : #8B6914
- Souterrain : #9a7453 → #8a6344 → #7a5235 → #6b4226 → #5c3317 (mycorhizes)
- Fond : #0a0d08
- Texte labels : même couleur que le niveau, font monospace

---

## CE QUE LE SCANNER PRODUIT DÉJÀ

Quand on fait `python engine.py scan /chemin/repo`, on obtient un JSON avec :

```json
{
  "idea": "[scanned] nom-projet",
  "family": "conifere",
  "family_emoji": "🌲",
  "scale": {
    "factor": 1.5,
    "height_px": 500,
    "density": 2.0,
    "trunk_width": 1.6,
    "category": "grand arbre",
    "label": "🌲 Grand Arbre (18000 lignes)"
  },
  "stats": {
    "total_files": 245,
    "total_code_lines": 18000,
    "data_weight_mb": 417,
    "languages": {"Python": 15000, "JSON": 3000},
    "biggest_file": {"path": "automata.py", "lines": 12000}
  },
  "nodes": [
    {
      "id": "T1", "level": "T", "label": "Core: main.py (500L)",
      "status": "done", "entry": "main.py", "confidence": 80
    },
    {
      "id": "B1", "level": "B", "label": "scripts/ (45 fichiers, 8000L)",
      "status": "done", "entry": "scripts/", "confidence": 80
    },
    ...
  ]
}
```

### Mapping niveau → level code dans le JSON :
- `"C"` = Cime (+5) — tests, CI, qualité
- `"F"` = Feuilles (+4) — README, docs publiques
- `"b"` = Rameaux (+3) — sous-dossiers, sous-modules
- `"B"` = Branches (+2) — dossiers principaux
- `"T"` = Tronc (+1) — entry point, plus gros fichier
- `"R" depth=-1` = R.Structurelles — config, stack
- `"R" depth=-2` = R.Pivotantes — architecture, Docker, CI/CD
- `"R" depth=-3` = Radicelles — helpers, utils
- `"R" depth=-4` = Poils absorbants — legal, licence
- `"M"` ou `"R" depth=-5` = Mycorhizes — langages, liens inter-projets

---

## ROADMAP RENDERER

### Étape 1 — Vue profil (un seul arbre)
`python engine.py serve scans/hsbc.json`
→ Ouvre localhost sur premier port dispo
→ HTML/SVG : Planche II en fond + overlay des nodes du JSON
→ Axe central avec les nodes positionnés sur le squelette
→ Labels à gauche (noms niveaux), descriptions à droite (ce que le scanner a trouvé)
→ Couleurs par niveau, confidence visible, status (done/wip/todo)

**Technique** : `http.server` Python natif, zéro dépendance.
Le HTML est généré par engine.py avec l'image en base64 inline.

### Étape 2 — Vue forêt (multi-arbres)
`python engine.py serve` (sans argument = tous les scans/)
→ Page d'accueil : tous les arbres côte à côte
→ Taille visuelle = scale (hauteur=code, épaisseur=data)
→ Clic sur un arbre → zoom vue profil (étape 1)
→ Chaque arbre a le style Planche II

**Pour ça il faut** : générer une image par famille (conifère, baobab, feuillu, buisson)
via ChatGPT/DALL-E avec le même style. Sky doit fournir les images.
→ Prompt à adapter : même style Planche II mais forme baobab/feuillu/buisson

### Étape 3 — Connexion GitHub API
`python engine.py serve --github sky1241`
→ Scanne tous les repos du compte GitHub
→ Génère la forêt automatiquement

---

## STYLE VISUEL À RESPECTER

- Police : JetBrains Mono (monospace)
- Fond : noir/très sombre, texturé si possible
- Couleurs : palette botanique (verts aériens, bruns souterrains)
- Nodes : cercles lumineux avec glow, petit point blanc au centre
- Liens nodes→labels : lignes pointillées fines de la couleur du niveau
- SOL : ligne dorée horizontale proéminente
- Ambiance : "planche botanique 18ème siècle × dark mode UI"
- PAS de flat design, PAS de cartoon
- Typographie discrète, letter-spacing large pour les titres

---

## COMMANDES ENGINE.PY EXISTANTES (pour référence)

```bash
# Scanner
python engine.py scan /chemin/vers/repo

# Planter (nouvelle idée)
python engine.py plant "description du projet"

# Gardien
python engine.py guard scans/projet.json
python engine.py check scans/projet.json B1
python engine.py update scans/projet.json T1 done "fichier.py:40"
python engine.py find scans/projet.json "mot-clé"

# Infos
python engine.py confidence scans/projet.json
python engine.py research scans/projet.json "contexte"
python engine.py families
python engine.py anatomy
python engine.py kb
```

### Nouvelle commande à implémenter :
```bash
# Étape 1
python engine.py serve scans/projet.json    # Vue profil un arbre

# Étape 2
python engine.py serve                       # Vue forêt tous les arbres

# Étape 3
python engine.py serve --github username     # Forêt depuis GitHub
```

---

## IMAGES À GÉNÉRER (pour étape 2)

Sky doit fournir une Planche II pour chaque famille, même style DALL-E :
- [x] Conifère (Planche II — déjà en assets/)
- [ ] Baobab (tronc massif, petite canopée)
- [ ] Feuillu (canopée ronde, branches équilibrées)
- [ ] Buisson (large et bas, multi-troncs)
- [ ] Liane (vertical fin, accroché à un support)
- [ ] Champignon (cas spécial — data > code)

Même prompt DALL-E, juste changer la forme de l'arbre.

---

## RÈGLE D'OR

**Sol = interface Sky ↔ Claude.**
Sky monte (arbre visible, progrès). Claude descend (racines, code).
Racines toujours > arbre.

**Workflow** : coder → tester → si OK push → étape suivante.
Ne jamais avancer sans valider l'étape en cours.
