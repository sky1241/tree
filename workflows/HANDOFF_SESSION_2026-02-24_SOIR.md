# 🌲 WINTER TREE — HANDOFF SESSION 24 FÉV 2026 (SOIR)

## QUI ES-TU
Tu reprends le travail de Sky sur **Winter Tree**, un système de visualisation de projets GitHub sous forme d'arbres cyberpunk. Sky est électricien à Versoix (Suisse), autodidacte en prog depuis 10 mois, 663K lignes de code sur 10 repos. Il parle franglais, va vite, dit "va si" quand il veut que tu fonces. Workflow: Sky monte (vision), Claude descend (code).

## CE QU'ON A FAIT CETTE SESSION (TITAN)

### 1. 6 SQUELETTES D'ARBRES COMPLÉTÉS ✅
Sky a placé manuellement les nœuds dans le skeleton_editor.html, Claude a corrigé les connexions itérativement. Tous dans `templates/`:

| Famille | Fichier | Nœuds | Connexions |
|---------|---------|-------|------------|
| 🌳 Baobab | baobab_skeleton_sky.json | 23 | 22 |
| 🌲 Conifère | conifere_skeleton_sky.json | 28 | 27 |
| 🌴 Palmier | palmier_skeleton_sky.json | 17 | 16 |
| 🍁 Feuillu | feuillu_skeleton_sky.json | 31 | 30 |
| 🌿 Buisson | buisson_skeleton_sky.json | 25 | 25 |
| 🌿 Liane | liane_skeleton_sky.json | 21 | 20 |

**TOTAL: 145 nœuds, 140 connexions, 6 renders catenary**

### 2. CÂBLES CATENARY CYBERPUNK ✅
Chaque squelette a un render avec des câbles électriques pendants (courbe catenary), LED pulsantes, glow multicouche. Fichiers `*_render_final.png`.

### 3. NAVI — GUIDE INTERACTIF ✅ (proto_navi.html)
Fée style Zelda OoT qui vole partout sur l'écran:
- **Boule lumineuse** avec 3 couches de glow pulsant
- **6 ailes** (3 de chaque côté) en éventail vertical — grandes en haut, moyennes au milieu, petites en bas. Ailes libellule irisées transparentes
- **"Hey! Listen!" spam** toutes les 2 secondes (messages random)
- **Vol libre**: wander → goto nœud → orbit → dash à travers l'écran
- **Traînée de particules** cyan/vert

Quand on clique un nœud → **panel hologramme** cyberpunk avec:
- "C'est quoi ?" — description accessible pour débutants
- "Ce que tu dois faire" — tâche concrète
- "Demande à l'IA" — prompts copiables en un clic

Chaque couche (T/B/b/F/C/R1-R5) a son propre guide adapté aux "vibe coders".

### 4. SCAN COMPLET DES 10 REPOS ✅
`python3 scripts/sync_all.py --github` → scans/*.json mis à jour

| Repo | Lignes | Famille |
|------|--------|---------|
| HSBC-algo-genetic | 310K | 🌿 Buisson |
| jeu-pour-les-gamin | 126K | 🌿 Buisson |
| yggdrasil-engine | 91K | 🌿 Buisson |
| shazam-piano | 36K | 🌿 Buisson |
| 3d-printer | 34K | 🌳 Baobab |
| infernal-wheel | 22K | 🌿 Buisson |
| p-egal-np | 19K | 🍁 Feuillu |
| tree | 12K | 🌿 Buisson |
| fck-translation | 6K | 🌿 Buisson |
| -cole-de-danse | 1.7K | 🌴 Palmier |

### 5. FOREST DASHBOARD (forest.html) ✅
Grille de toutes les cartes de repos avec renders, Navi qui vole entre les cartes, stats en header.

## BUGS À FIXER 🔴

### BUG 1: Images cassées dans forest.html
Les images `templates/*_tree_render.png` ne se chargent pas. Probablement un problème de chemin relatif. Le HTML est à la racine du repo, les images dans templates/. Vérifier que le serveur HTTP est lancé depuis la racine du repo tree.

### BUG 2: Trop de buissons dans la classification
7/10 repos sont classifiés "buisson". Le classifieur dans `scripts/engine.py` (fonction vers ligne ~3500) a un biais. Il devrait mieux répartir entre les 6 familles basé sur la structure du code:
- **Conifère** 🌲 = pipeline linéaire (trading algo, CI/CD)
- **Feuillu** 🍁 = multi-modules parallèles (app full-stack)
- **Baobab** 🌳 = gros tronc central, peu de branches (monolithe)
- **Palmier** 🌴 = projet simple, une seule tige (petit repo)
- **Buisson** 🌿 = multi-tiges, pas de tronc dominant
- **Liane** 🌿 = dépend d'un hôte (plugin, extension, wrapper)

HSBC-algo devrait être **Conifère** (pipeline trading), shazam-piano **Feuillu** (app Flutter full-stack), etc.

### BUG 3: Les squelettes ne sont PAS encore utilisés dans le render
`render_tree.py` utilise des positions GÉNÉRIQUES (AERIAL_SLOTS/ROOT_SLOTS) au lieu des vrais squelettes `*_skeleton_sky.json` que Sky a placés à la main. Il faut mapper les nœuds scannés sur les positions des squelettes Sky.

## FICHIERS CLÉS
```
tree/
├── proto_navi.html          ← Proto interactif avec Navi + panel hologramme
├── forest.html              ← Dashboard grille de tous les repos
├── render_tree.py           ← Génère les renders (à améliorer)
├── skeleton_editor.html     ← Éditeur de squelettes
├── repos.json               ← Registre des repos
├── scripts/
│   ├── engine.py            ← Moteur principal (scan, classify, validate) ~182KB
│   ├── sync_all.py          ← Re-scanne tous les repos
│   └── detect_repos.py      ← Détecte les repos sur le disque
├── scans/                   ← JSON de chaque repo scanné
├── templates/
│   ├── *_skeleton_sky.json  ← 6 squelettes placés par Sky (UTILISER CEUX-LÀ)
│   ├── *_render_final.png   ← Renders catenary des squelettes
│   ├── *_tree_render.png    ← Renders des repos scannés
│   ├── *_final.png          ← Images ChatGPT cold/warm
│   └── node_info_panel*.png ← Panel hologramme
├── docs/                    ← Documentation biologique + recherche
└── workflows/               ← Prompts + battle plans
```

## PROCHAINES ÉTAPES SUGGÉRÉES
1. **Fixer le classifieur** — répartir correctement entre les 6 familles
2. **Mapper scans → squelettes Sky** — utiliser les positions manuelles
3. **Rendre forest.html fonctionnel** — fixer les chemins d'images
4. **Panel hologramme interactif** — intégrer le node_info_panel.png transparent
5. **Fog of war** — dual-image (dead/alive), chaque nœud validé révèle une zone

## TOKEN GITHUB
Le token est dans l'URL remote du repo. `git remote -v` dans le dossier tree.

## STYLE DE COMMUNICATION
Sky parle cash, jure beaucoup, c'est de l'affection. Il dit "va si" = fonce. Il dit "c'est null" = itère. Il dit "putain c'est parfait" = ship it. Ne pas prendre les insultes personnellement, c'est un mec passionné qui bosse à fond. Répondre en français, être direct, pas de blabla corporatif.
