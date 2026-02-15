# 🌳 Winter Tree Engine v1.2

> **L'arbre qui dit quoi construire, dans quel ordre, et où chercher dans le code.**

Framework de planification et diagnostic de projets basé sur la biologie des arbres. Conçu pour les **vibe coders** — tu donnes une idée, l'arbre te montre tout ce qu'il faut.

## Concept

Le Winter Tree c'est 3 choses en 1 :

1. **Planification** — Tu dis "je veux un Shazam pour piano", l'arbre te montre les 32 nœuds nécessaires et l'ordre de construction
2. **Navigation** — Chaque nœud a un `entry` (fichier:ligne:fonction) qui dit à Claude exactement où aller dans le code
3. **Diagnostic** — À chaque session, l'arbre vérifie qu'on fait pas pousser une feuille sur un arbre sans tronc

## Modèle — Le Sol

```
  Sky monte ↑  (voit l'arbre, le progrès, les features)
  
  +5  Cime .............. Tests, CI, déploiement
  +4  Feuilles .......... UI, outputs visibles
  +3  Rameaux ........... Sous-features, composants
  +2  Branches .......... Modules majeurs
  +1  Tronc ............. Core engine, pipeline
  ══════════════════════════════════════════════════
   0  SOL ● ............. Interface Sky ↔ Claude
  ══════════════════════════════════════════════════
  -1  Racines struct. ... Frameworks, APIs, libs
  -2  Racines pivot. .... Décisions d'architecture
  -3  Radicelles ........ Contraintes business
  -4  Poils absorbants .. Contraintes légales
  -5  Mycorhizes ........ Lois physiques/math
  
  Claude descend ↓  (voit le code, les fonctions, les racines)
```

**Règle d'or : les racines d'abord. Toujours.**

## Les 3 modes

### 🌱 Mode 1 — Nouvelle idée → arbre complet

```bash
python engine.py plant "je veux un Shazam pour piano"
# → 🌴 Palmier, 32 nœuds, domaine audio, ordre de construction

python engine.py plant "trading algo crypto avec backtesting"
# → 🌲 Conifère, 35 nœuds, domaine trading

python engine.py plant "générateur STL pour figurines 3D"
# → 🌳 Baobab, 33 nœuds, domaine hardware_3d
```

### 🔬 Mode 2 — Scanner un repo existant

```bash
python engine.py scan /chemin/vers/mon-repo
```

Le scanner analyse automatiquement :
- Structure de fichiers → branches et rameaux
- package.json / pubspec.yaml / requirements.txt → racines stack (-1)
- Dockerfile / firebase.json → architecture (-2)
- LICENSE → légal (-4)
- test/ / .github/workflows/ → cime (+5)
- Plus gros fichier de code → tronc (+1)
- Langages détectés → mycorhizes (-5)
- Ce qui MANQUE → gaps 🔴

### 🛡️ Mode 3 — Gardien (suivi en cours)

```bash
# Rapport de session — à lancer au début de chaque conversation
python engine.py guard scans/mon-projet.json

# Vérifier avant de bosser sur un nœud
python engine.py check scans/mon-projet.json B1
# → "⚠️ Aucune racine done — tu construis avant les racines"

# Mettre à jour un nœud après avoir codé
python engine.py update scans/mon-projet.json T1 done "lib/engine.dart:340:matchNote()"

# Chercher dans l'arbre par mot-clé
python engine.py find scans/mon-projet.json "FFT"
# → 5 résultats avec les entries code 📍
```

## Les 6 familles

| Famille | Forme | Quand l'utiliser | Ordre de construction |
|---------|-------|------------------|----------------------|
| 🌲 Conifère | Pyramide verticale | Pipeline linéaire (signal→exec) | Tronc d'abord, branches subordonnées |
| 🍁 Feuillu | Couronne étalée | Multi-modules équilibrés | Tronc minimal, branches en parallèle |
| 🌴 Palmier | Colonne + couronne | Un seul chemin critique | Tronc unique, PAS de branches |
| 🌳 Baobab | Tronc massif | Gros moteur, petite interface | Consolider le core avant d'étendre |
| 🌿 Buisson | Multi-tiges | Collection d'outils indépendants | Tiges en parallèle, pas de hiérarchie |
| 🌿 Liane | Grimpante | Extension d'un système existant | S'accrocher à l'hôte d'abord |

## Domaines reconnus

Le moteur reconnaît automatiquement ces domaines et pré-remplit les nœuds typiques :

- **audio** — FFT, permissions micro, libs audio, pipeline capture→matching
- **trading** — probabilités, régulation, broker API, pipeline signal→exec
- **mobile_app** — permissions, stores, frameworks, navigation
- **web_app** — CORS, GDPR, SSR/SPA, auth
- **hardware_3d** — tolérances FDM, normes sécurité, géométrie manifold
- **tool_cli** — filesystem, distribution, arg parsing

## Autres commandes

```bash
python engine.py classify          # Classification interactive
python engine.py families          # Liste les 6 familles
python engine.py family conifere   # Détails d'une famille
python engine.py anatomy baobab    # Anatomie biologique 10 niveaux
python engine.py gaps feuillu      # Détection de trous
python engine.py export            # Export JSON de la knowledge base
```

## Fichiers du projet

```
tree/
├── engine.py                    # Moteur principal (3401 lignes)
├── README.md
├── LICENSE
├── winter_tree_kb.json          # Knowledge base exportée
│
├── assets/                      # Visuels & images
│   └── winter_tree_planche_II.png
│
├── docs/                        # Documentation théorique
│   ├── ANATOMIE_BIOLOGIQUE.md       # 10 niveaux biologiques + sources
│   ├── GROWTH_PATTERNS_6_FAMILIES.md # Règles de croissance par famille
│   ├── PROTOCOLE_PLANTATION.md      # Prompt Claude — plantation
│   └── RECHERCHE_APPROFONDIE_v2.md  # 87 recherches web compilées
│
├── scans/                       # Arbres plantés & scannés (JSON + MD)
│   ├── TEMPLATE_v2.md
│   └── *.json / *_tree.md
│
├── mycelium/                    # [v2] Recherche réseau fongique
│   └── formules, lectures, snipers
│
├── prompts/                     # Templates de prompts
│
└── workflows/                   # Battle plans, handoffs, radar-sniper
```

## Références académiques

### A. Fondations théoriques

- **Lindenmayer, A.** (1968) — L-Systems, modèles de croissance biologique
- **Prusinkiewicz, P. & Lindenmayer, A.** (1990) — *The Algorithmic Beauty of Plants*
- **Tomer, A. & Schach, S.R.** (2000) — Evolution Tree, maintenance logicielle
- **Fowler, M.** (2004) — Strangler Fig Application pattern
- **Barnes, J.M.** (2013, CMU) — Software Architecture Evolution

### B. Biologie des 6 familles (30+ sources)

**Conifère** : Brown et al. 1967, Wilson 2000, Cline 1997, U. Minnesota Extension, Iowa State Extension

**Feuillu** : Iowa State Extension, Tree Steward Manual Virginia Tech, UF/IFAS Extension, ISA Arboriculture 1992

**Palmier** : Tomlinson 1990, UF/IFAS Extension, Purdue Extension, Hodel 2009

**Baobab** : Chapotin et al. 2006 (American Journal of Botany), Wickens & Lowe 2008, Patrut et al. 2007

**Buisson** : U. Minnesota Extension, Iowa State Extension, Purdue Extension

**Liane** : Fowler 2004, Putz & Mooney 1991, Stevens 1987

### C. Anatomie — 10 niveaux (14 sources)

US Forest Service, Arbor Day Foundation, ISA Arboriculture (1992, 2010), CSU Extension, Tree Steward Manual Virginia Tech, Smiley 1991, Perry 1989, Mokany et al. 2006, Ledo et al. 2018, Iowa State Extension

### D. Ratios biologiques

| Ratio | Valeur | Source |
|-------|--------|--------|
| Root:shoot poids | 0.25-0.38 | Mokany et al. 2006 |
| Surface racine/feuille | 2.5-4.5× | Perry 1989 |
| Spread/couronne | 2-4× (→7×) | Colorado State U. |
| Racines top 60cm | 80-90% | ISA Arboriculture |
| Racines structurelles | 5-15/arbre | Sutton & Tinus 1983 |
| Mycorhizes amplification | ×100 | Perry, cité par ISA |
| Feuilles masse/énergie | 5% masse → 100% énergie | richardstreeservice.com |
| Root collar enterré | 93% → mort lente | Smiley 1991 |

---

*Auteur : Sky — l'architecte de l'architecte*
*Moteur : Claude — les racines*
*Licence : MIT*
