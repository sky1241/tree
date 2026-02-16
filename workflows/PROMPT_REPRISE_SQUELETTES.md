# PROMPT DE REPRISE — Squelettes Botaniques Winter Tree Engine

## Contexte

Winter Tree Engine v1.2 — framework bio-inspiré pour cartographier des repos logiciels
en structures d'arbres. Chaque repo scanné est mappé sur une des 6 familles d'arbres,
avec 10 niveaux anatomiques (de +5 Cime à -5 Mycorhizes).

Le travail effectué: on a construit le **squelette parfait du CONIFÈRE** — 28 nœuds idéaux
placés aux points de séparation de l'arbre, avec hiérarchie parent-enfant explicite.
Il faut maintenant faire la même chose pour les 5 autres familles.

## Ce qui est FAIT

### Conifère (🌲) — TERMINÉ
- 28 nœuds idéaux avec positions pixel sur Planche II
- **Hiérarchie corrigée (100% thèse):**
  - Aérien: `trunk → B → b → F` (feuilles via rameaux, PAS directement au tronc)
  - Apex: `trunk → C` (cime = bourgeons terminaux, directement au tronc)
  - Souterrain: `trunk → R-1 → R-2 → R-3 → R-4 → R-5`
- **Pipe Model (Shinozaki):** épaisseur connexions proportionnelle au flux
  - T=4.0px, B/R-1=2.5px, R-2=1.8px, b=1.5px, F/R-3=1.2px, C=1.0px, R-4=0.8px, R-5=0.5px
- **Taille nœuds** proportionnelle à l'importance hiérarchique:
  - T=33px, B/R-1=23px, R-2=18px, b=15px, F/R-3=12px, C=11px, R-4=8px, R-5=6px
- **Désignations techniques** affichées à droite de chaque couche
- Rendu: nœuds blancs, connexions Bézier, tronc central
- Fichier: `templates/interactive_profile.html`
- Image: `assets/winter_tree_planche_II.png` (922×1244px)

### ⚠️ TODO PRIORITAIRE — Lignes de séparation des niveaux
Les lignes horizontales de séparation (CIME, FEUILLES, RAMEAUX, etc.) ne correspondent
plus aux bonnes positions sur l'image. Il faut les recaler sur les vraies zones de l'arbre.
Actuellement les Y dans `LEVELS` sont des valeurs arbitraires, pas calibrées sur la planche.

## Les 6 familles et leurs règles (source: docs/FAMILIES.md)

### 1. CONIFÈRE 🌲 (FAIT)
```
Forme: Pyramidale/excurrente
Règles:
  C1 — TRUNK_FIRST: Le tronc s'étend AVANT les branches. Ne se divise JAMAIS.
  C2 — BRANCH_SUBORDINATION: branche.diamètre < 0.6 × tronc.diamètre
  C3 — TOP_DOWN_GROWTH: Énergie de l'apex vers la base (auxines)
  C4 — NO_RECOVERY_ON_OLD_WOOD: Leader coupé = arbre mort
Biomasse: Tronc 55-65%, Branches 10-15%, Feuilles 5%, Racines 20-23%
Root:Shoot = 0.25-0.30
Branches: Verticillées, 5-7 par verticille, angle 45-60°
Hiérarchie: trunk → B → b → F → C (tout subordonnné au tronc)
Exemple software: Pipeline linéaire (ETL, compilateur, CLI)
```

### 2. FEUILLU 🌳 (À FAIRE)
```
Forme: Arrondie/décurrente
Règles:
  F1 — BRANCH_FIRST: Branches PEUVENT dépasser le tronc (co-dominance OK)
  F2 — LATERAL_FREEDOM: Bourgeons latéraux libérés après dormance
  F3 — DECURRENT_FORM: Perte du leader central, forme arrondie
  F4 — RECOVERY_POSSIBLE: Repousse depuis le bois ancien
Biomasse: Tronc 30-40%, Branches 25-35%, Feuilles 10-15%, Racines 20-25%
Root:Shoot = 0.20-0.25
Branches: PAS de subordination stricte — peuvent rivaliser avec le tronc
Hiérarchie: trunk → B (mais B peut devenir aussi gros que trunk)
           B → b → F → C (chaque branche est quasi-indépendante)
Exemple software: Monorepo multi-modules (React, Django, Spring)
```

### 3. PALMIER 🌴 (À FAIRE)
```
Forme: Colonnaire (un seul méristème)
Règles:
  P1 — SINGLE_MERISTEM: Un seul point de croissance. Meurt = arbre meurt.
  P2 — NO_BRANCHES: Pas de vraies branches. Les "palmes" sont des feuilles.
  P3 — NO_SECONDARY_GROWTH: Le tronc ne s'épaissit PAS avec le temps.
  P4 — CROWN_SHAFT: Toutes les feuilles sortent du même point terminal.
Biomasse: Tronc 70-80%, Feuilles 10-15%, Racines 10-15%
Branches: AUCUNE (les palmes ne sont pas des branches)
Hiérarchie: trunk linéaire → F sort du sommet → C au bout des palmes
Exemple software: Single binary, microservice unique, script monolithique
```

### 4. BAOBAB 🫚 (À FAIRE)
```
Forme: Tronc massif, couronne petite
Règles:
  B1 — TRUNK_DOMINANT: 60-80% de la biomasse dans le tronc (stockage)
  B2 — SMALL_CROWN: Très peu de branches, courtes
  B3 — SLOW_GROWTH: Croissance très lente mais très robuste
  B4 — BARK_REGENERATION: Le tronc peut se régénérer (résilience)
Biomasse: Tronc 60-80%, Branches 5-10%, Feuilles 2-5%, Racines 15-20%
Branches: Peu nombreuses, courtes, émergeant tardivement
Hiérarchie: trunk MASSIF → peu de B → encore moins de b
Exemple software: Base de données, OS kernel, infrastructure critique
```

### 5. BUISSON 🌿 (À FAIRE)
```
Forme: Multi-tiges depuis la base
Règles:
  Bu1 — NO_CENTRAL_TRUNK: Pas de tronc dominant. Tiges parallèles.
  Bu2 — BASAL_SPROUTING: Nouvelles tiges depuis les racines
  Bu3 — REJUVENATION: Coupe rase → repousse vigoureuse
  Bu4 — REDUNDANCY: Chaque tige est indépendante (résilience)
Biomasse: Répartie uniformément entre les tiges
Branches: Chaque "tige" EST une branche indépendante
Hiérarchie: racines → tige1, tige2, tige3... (pas de hiérarchie centrale)
Exemple software: Microservices, plugins indépendants, collection de scripts
```

### 6. LIANE 🌱 (À FAIRE)
```
Forme: Grimpante, dépend d'un hôte
Règles:
  L1 — HOST_DEPENDENT: Ne peut pas se soutenir seul
  L2 — NO_STRUCTURAL_COST: Pas de bois structural → croissance rapide
  L3 — PARASITIC_OR_SYMBIOTIC: Utilise la structure de l'hôte
  L4 — DIES_WITH_HOST: Si l'hôte meurt, la liane meurt
Biomasse: Quasi tout dans les tiges et feuilles, pas de tronc
Branches: Vrilles, s'enroulent autour de l'hôte
Hiérarchie: hôte → liane.trunk → tendrils → F → C
Exemple software: Plugin/extension, wrapper, middleware, fork
```

## Données botaniques clés (thèses PhD)

### Sources
- **ISA Arboriculture Standards** — règle branch < trunk diameter
- **Bebber et al. 2007** — "Biological solutions to transport network design"
  - Réseau optimise SIMULTANÉMENT: efficacité, robustesse, coût
- **Boswell 2003/2007** — PDEs de croissance mycélienne (5 variables)
  - m (biomasse active), m' (inactive), p (tips), n_i (ressources internes), n_e (externes)
- **Lindenmayer 1968** — L-Systems (recursive rewriting → plant structures)
- **Aguilar-Trigueros 2022** — 15 traits de réseau
- **Fricker 2017** — transport networks in fungi

### Ratios universels
```
Branch subordination: branche < 0.6 × tronc (conifère STRICT, feuillu SOUPLE)
Root spread: 2-4× diamètre couronne (toutes espèces)
Root depth: 80-90% dans les premiers 60cm (toutes espèces)
Root surface: 2.5-4.5× surface foliaire
Foliage: 5% biomasse mais 100% énergie (photosynthèse)
```

### Pipe Model — Épaisseur des connexions (Shinozaki et al.)
```
RÈGLE: L'épaisseur d'une connexion = proportionnelle au flux qu'elle transporte.
Le tronc transporte TOUT → le plus épais.
Chaque branche transporte MOINS → plus fin.
Chaque rameau encore moins → encore plus fin.

Conifère — stroke-width par niveau:
  Tronc (T):     4.0px  — 100% du flux (colonne vertébrale)
  T → B:         2.5px  — ~50% (règle C2: branche < 0.6× tronc)
  T → C/F:       1.2px  — twigs apicaux, fins
  B → b:         1.5px  — ~30% (rameau subordonné à la branche)
  T → R-1:       2.5px  — racines structurelles (même calibre que branches)
  R-1 → R-2:     1.8px  — pivotantes
  R-2 → R-3:     1.2px  — radicelles (fines)
  R-3 → R-4:     0.8px  — poils absorbants (microscopiques)
  R-4 → R-5:     0.5px  — mycorhizes (les plus fins)

Feuillu — épaisseurs DIFFÉRENTES:
  T → B:         3.5px  — branches presque aussi grosses que le tronc (co-dominance)
  B → b:         2.0px  — rameaux plus robustes que chez le conifère

Palmier: Pas de branches → une seule ligne épaisse (tronc) + fines palmes au sommet
Baobab: Tronc TRÈS épais (6-8px), branches très fines (1px)
Buisson: Pas de tronc → toutes les tiges de même épaisseur (~2px)
Liane: Tout fin (~1-1.5px), pas de structure porteuse
```

## Les 10 niveaux anatomiques

```
+5  CIME        Tests, CI/CD, release      (bourgeons terminaux — auxines)
+4  FEUILLES    UI, endpoints, outputs     (5% masse, 100% énergie)
+3  RAMEAUX     Sub-features, sub-modules  (<4 ans, flexibles)
+2  BRANCHES    Modules principaux         (scaffold, décennies)
+1  TRONC       Core engine/pipeline       (55-65% biomasse conifère)
 0  SOL         Interface humain↔machine   ────────────────────────
-1  R.STRUCT.   Frameworks, APIs, deps     (5-15 racines, ∅30cm)
-2  R.PIVOT.    Architecture, décisions    (ancrage 60cm-2m)
-3  RADICELLES  Contraintes métier         (éphémères, mois)
-4  POILS       Licence, conformité        (microscopiques, filtrent tout)
-5  MYCORHIZES  Algo fondamentaux, hardware (symbiose ×100)
```

## Architecture technique

### Fichiers clés
- `engine.py` (~4700 lignes) — Scanner + serveur HTTP
  - `FAMILY_IMAGE_MAP` (ligne ~3188): famille → image PNG
  - `LEVEL_Y_MAP` (ligne ~3198): niveau → {y, label, color, zone}
  - `serve_tree()`: Serveur HTTP port 8420
  - `_build_interactive()`: Injecte JSON dans le template
  - Template chargé AU DÉMARRAGE → restart pour chaque changement

- `templates/interactive_profile.html` — Page profil arbre
  - Layout: sidebar (300px) + canvas (image + SVG overlay) + detail panel
  - Constantes: IMG_W=922, IMG_H=1244, CENTER_X=461, SOL_Y=575
  - SVG overlay avec nœuds, connexions, squelette
  - Zoom/pan/click interactif

- `scans/*.json` — Données de repos scannés
- `assets/winter_tree_planche_*.png` — Images botaniques (6 planches)
- `docs/FAMILIES.md`, `docs/LEVEL_SYSTEM.md`, `docs/MYCELIUM_V2.md` — Documentation

### Comment lancer
```bash
PYTHONIOENCODING=utf-8 python engine.py serve scans/HSBC-algo-genetic.json
# → http://localhost:8420
```

### Pour chaque nouvelle famille, il faut:
1. Lire l'image de la planche correspondante
2. Définir les positions pixel des nœuds aux points de séparation
3. Définir la hiérarchie parent-enfant selon les règles de la famille
4. Adapter le nombre de nœuds par niveau (ex: palmier = 0 branches)
5. Implémenter dans le template (switch sur `TREE_DATA.family`)

## Ce qui reste à faire

1. ☑ ~~Rendre le squelette conifère 100% conforme aux thèses~~ FAIT
2. ☐ **RECALER LES LIGNES DE SÉPARATION** — les Y des niveaux dans `LEVELS` ne matchent
   plus les vraies zones de la planche. À refaire pour chaque famille.
3. ☐ Implémenter le switch par famille dans le template
4. ☐ Squelette FEUILLU (branches co-dominantes, forme arrondie)
5. ☐ Squelette PALMIER (pas de branches, tronc colonnaire)
6. ☐ Squelette BAOBAB (tronc massif, petite couronne)
7. ☐ Squelette BUISSON (multi-tiges, pas de tronc central)
8. ☐ Squelette LIANE (grimpante, dépend d'un hôte)
9. ☐ Overlay du repo réel sur le squelette parfait (diagnostic)
10. ☐ Animations de croissance (graine → arbre)

## Conventions

- Windows 10, shell bash, PYTHONIOENCODING=utf-8
- Git: push sur main (github.com/sky1241/tree.git)
- Template reloadé au restart serveur (pas de hot reload)
- Nœuds actuellement en BLANC (temporaire, couleurs à définir)
- Positions pixel hardcodées par famille (pas de calcul dynamique)
