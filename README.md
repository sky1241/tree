# 🌲 Tree — Système de croissance de projets

> "Sky monte, Claude descend. Le sol c'est là où on se parle."

## Qu'est-ce que c'est ?

Un framework pour gérer la croissance de projets logiciels en s'inspirant des règles de croissance des arbres dans la nature. Chaque projet est un arbre d'une famille spécifique, et les règles de développement suivent les lois biologiques de cette famille.

## Les 6 familles

| Famille | Forme | Règle dominante | Quand l'utiliser |
|---------|-------|-----------------|------------------|
| 🌲 Conifère | Pyramide verticale | Tronc d'abord, branches subordonnées | Pipeline linéaire |
| 🍁 Feuillu | Canopée large | Branches rivalisent avec le leader | Multi-modules |
| 🌴 Palmier | Colonne + couronne | Un seul méristème, zéro branche | Pipeline étroit, output riche |
| 🌳 Baobab | Tronc massif | Consolider avant d'étendre | Gros moteur, petite interface |
| 🌿 Buisson | Multi-tiges | Pas de tronc dominant | Collection d'outils |
| 🌿 Liane | Grimpe sur un hôte | Utilise l'infrastructure existante | Plugin, wrapper, extension |

## Le modèle Winter Tree

L'Arbre d'Hiver = la carte d'un projet sans les feuilles. Juste la structure.

- **Au-dessus du sol** : ce que Sky voit (progrès, features, statut)
- **En-dessous du sol** : ce que Claude voit (code, fonctions, lignes)
- **Le sol** : l'interface de collaboration Sky ↔ Claude

**Les racines sont TOUJOURS plus grandes que l'arbre visible.**

## Les 10 niveaux biologiques

Chaque nœud d'un projet se place sur un des 10 niveaux anatomiques de l'arbre :

```
+5  Cime .............. Bourgeons terminaux      → Tests, CI/CD, release
+4  Feuilles .......... Photosynthèse            → UI, outputs, endpoints
+3  Rameaux ........... Branchlets flexibles      → Sous-features, composants
+2  Branches .......... Boughs structurels        → Modules majeurs
+1  Tronc ............. Bole + duramen            → Core engine, pipeline
════════════════════════════════════════════════════════════════════
 0  ● SOL ● ........... Collet racinaire          → Interface Sky ↔ Claude
════════════════════════════════════════════════════════════════════
-1  Racines struct. ... Structural/lateral roots  → Frameworks, APIs
-2  Racines pivot. .... Taproot/sinker roots      → Décisions d'architecture
-3  Radicelles ........ Fine/feeder roots         → Contraintes business
-4  Poils absorbants .. Root hairs                → Contraintes légales
-5  Mycorhizes ........ Mycorrhizae               → Lois physiques/math
```

## Le moteur (`engine.py`)

CLI Python, zéro dépendance :

```bash
python engine.py classify          # Classification interactive
python engine.py families          # Liste les 6 familles
python engine.py family baobab     # Détails d'une famille
python engine.py anatomy baobab    # Anatomie 10 niveaux + bio
python engine.py gaps baobab       # Détection de trous 🔴🟡🟢
python engine.py generate conifere # Génère un template v2
python engine.py export            # Exporte en JSON
```

## Structure du repo

```
tree/
├── README.md                          ← Tu es ici
├── engine.py                          ← Moteur Python (1355 lignes)
├── winter_tree_kb.json                ← Knowledge base exportée
├── ANATOMIE_BIOLOGIQUE.md             ← Données biologiques 10 niveaux
├── GROWTH_PATTERNS_6_FAMILIES.md      ← Recherche sur les 6 familles
├── RECHERCHE_APPROFONDIE_v2.md        ← Compilation académique (483 lignes)
├── MASTER_PROMPT_SKY.md               ← Prompt maître pour Claude
├── HANDOFF_SESSION_2026-02-14.md      ← Résumé pour passer le relais
├── prompts/
│   ├── MICR_DEEP_RESEARCH_v2_SURGICAL.md
│   └── code-audit-template.md
├── workflows/
│   ├── radar-sniper.md
│   ├── BATTLE_PLAN_2026-02-15_DEFINITIF.md
│   └── LISTE_DE_COURSES_DIMANCHE.md
└── winter-trees/
    ├── TEMPLATE_v2.md                 ← Template vierge
    └── infernal-wheel-ux_tree.md      ← Exemple réel (buisson)
```

---

## Références

### A. Fondations académiques (architecture logicielle)

| Auteur | Année | Titre | Source | Concept clé |
|--------|-------|-------|--------|-------------|
| Aristid Lindenmayer | 1968 | "Mathematical models for cellular interactions in development I & II" | J. Theoretical Biology, vol.18, pp.280-315 | **L-Systems** — réécriture parallèle de chaînes pour la croissance |
| Prusinkiewicz & Lindenmayer | 1990 | "The Algorithmic Beauty of Plants" | Springer, 228 pages. Gratuit : [algorithmicbotany.org](http://algorithmicbotany.org) | Interprétation turtle graphics des L-systems |
| Amir Tomer & Stephen R. Schach | 2000 | "The Evolution Tree: A Maintenance-Oriented Software Development Model" | CSMR 2000, IEEE, pp.209-214 | **Evolution Tree** — arbre 2D version × phases |
| Martin Fowler | 2004 | "Strangler Fig Application" | [martinfowler.com/bliki](https://martinfowler.com/bliki/StranglerFigApplication.html) | Migration progressive inspirée du figuier étrangleur |
| Jeffrey M. Barnes | 2013 | "Software Architecture Evolution" | CMU-ISR-13-118, Carnegie Mellon | Évolution = graphe d'états architecturaux |

### B. Biologie des 6 familles d'arbres

Chaque famille a été recherchée individuellement avec des sources scientifiques vérifiées.

#### 🌲 Conifère — Contrôle apical & forme excurrente

| Source | Concept recherché |
|--------|-------------------|
| Brown, C.L. et al. (1967), cité par Cline (1997) | Paradoxe : dominance apicale FAIBLE mais contrôle apical FORT |
| Wilson, B.F. (2000) "Apical control of branch growth and angle in woody plants" | Mécanisme auxine basipétale (apex → base) vs cytokinine acropétale |
| Cline, M.G. (1997) "Concepts and terminology of apical dominance" | Distinction dominance vs contrôle apical chez les conifères |
| University of Minnesota Extension | Norfolk Island Pine : les latérales NE PEUVENT PAS devenir leader |
| Iowa State Extension, "Tree Anatomy 101" | Forme excurrente (pyramidale) vs décurrente (étalée) |

#### 🍁 Feuillu — Compétition latérale & forme décurrente

| Source | Concept recherché |
|--------|-------------------|
| Iowa State Extension, "Tree Anatomy 101" | Décurrence : le leader "se perd" parmi les branches |
| Tree Steward Manual, Virginia Tech, Ch.4 | Risque co-dominance : V-shape + écorce incluse = point de rupture |
| UF/IFAS Extension, University of Florida | Plasticité environnementale : même espèce, formes différentes |
| ISA Arboriculture, "Root-Shoot Ratios" (1992) | Ratio R:S feuillus 0.25-0.38, biomasse racinaire > conifères |

#### 🌴 Palmier — Méristème unique & croissance primaire

| Source | Concept recherché |
|--------|-------------------|
| Tomlinson, P.B. (1990) "The Structural Biology of Palms" | SAM unique, pas de cambium vasculaire, pas de croissance secondaire |
| UF/IFAS Extension, "Biology of Palms" | "Primary gigantism" — diamètre fixé avant la hauteur |
| Purdue Extension | Blessures PERMANENTES — pas de compartimentalisation |
| Hodel, D.R. (2009) "Biology of Palms" | Croissance diffuse secondaire vs vraie croissance secondaire |

#### 🌳 Baobab — Le paradoxe du tronc massif

| Source | Concept recherché |
|--------|-------------------|
| Chapotin, S.M. et al. (2006), American Journal of Botany | Le tronc massif n'est PAS principalement pour le stockage d'eau |
| Chapotin et al. (2006) | Bois nécessaire pour prévenir le FLAMBAGE — densité 0.09-0.17 g/cm³ |
| Wickens & Lowe (2008) "The Baobabs" | Multi-troncs fusionnés, tronc creux naturel, longévité 1000+ ans |
| Patrut et al. (2007) | Datation radiocarbone : 1275±20 BP (Madagascar) |
| Chapotin et al. (2006) | 69-88% parenchyme, 5% bois solide, 79% eau, transport radial lent |

#### 🌿 Buisson — Multi-tiges & résilience par redondance

| Source | Concept recherché |
|--------|-------------------|
| University of Minnesota Extension | Cane-growth habit : tiges multiples depuis la base, pas de dominante |
| Iowa State Extension, "Pruning Shrubs" | Rejuvenation pruning : taille à 15-30cm → regrowth vigoureux en 1 saison |
| Purdue Extension, "Shrub Pruning" | Suckering : rejets depuis les racines, expansion horizontale |
| Multiple Extension Services | Redondance = résilience — si une tige meurt, les autres continuent |

#### 🌿 Liane / Figuier étrangleur — Cycle parasite → autonome

| Source | Concept recherché |
|--------|-------------------|
| Martin Fowler (2004), observation Queensland 2001 | Cycle : germination dans l'hôte → racines au sol → autonomie → hôte meurt |
| Putz, F.E. & Mooney, H.A. (1991) "The Biology of Vines" | 25% des espèces ligneuses tropicales sont des lianes |
| Stevens, G.C. (1987) "Lianas as structural parasites" | Impact sur l'hôte : -50% croissance, 2x mortalité, -60% fruits |
| Various tropical botany sources | Stratégies d'accroche : vrilles, épines, racines adventives, poils adhésifs |

### C. Anatomie de l'arbre — Les 10 niveaux

| Source | Concept recherché |
|--------|-------------------|
| US Forest Service, "Anatomy of a Tree" | Duramen (heartwood) mort mais supporte 20 tonnes. Auxines des bourgeons |
| Arbor Day Foundation, "Anatomy of a Tree" | Racines dans les 3 premiers pieds, spread 2-4x couronne |
| ISA Arboriculture (1992), "Root-Shoot Ratios" | Surface racinaire = 2.5-4.5x surface foliaire (Perry) |
| ISA Arboriculture (2010), "Contemporary Root System Architecture" | 5-15 racines structurelles, spread = 38:1 vs diamètre tronc |
| CSU Extension, GardenNotes #659 | Types de racines : structural, sinker, fine/feeder, root hairs |
| Tree Steward Manual, Virginia Tech, Ch.4 | Collet racinaire = amortisseur, anneaux 2x plus larges |
| Smiley (1991), Bartlett Tree Research | 93% des arbres urbains ont un collet enterré → mort lente |
| Perry (1989), cité par ISA | Mycorhizes amplifient absorption x100, 2500+ espèces |
| Mokany et al. (2006), Global Change Biology | Ratio R:S moyen 0.25-0.38, analyse critique globale |
| Ledo et al. (2018), New Phytologist | Taille et déficit hydrique contrôlent R:S globalement |
| Biology Insights (2025), "Conifer Root System" | 80-90% racines dans top 60cm |
| Leuschner et al. (2025), ScienceDirect | Hêtre/chêne profondeur max 3.8m, biomasse fine racinaire comparée |
| Iowa State Extension, "Tree Root Systems" | Racines rarement > 4 pieds, spread 4-7x rayon couronne |
| A Plus Tree (2024), "3 Types of Root Systems" | Taproot, lateral, heart root — 80% arbres = système latéral |

### D. Ratios biologiques dans le moteur

| Ratio | Valeur | Source |
|-------|--------|--------|
| Racine:Shoot (poids) | 0.25-0.38 | Mokany et al. 2006 |
| Surface racinaire vs foliaire | 2.5-4.5x | Perry (1989) |
| Spread latéral vs couronne | 2-4x (jusqu'à 7x) | Colorado State U. + Iowa State |
| Racines dans top 60cm | 80-90% | ISA + Biology Insights |
| Racines structurelles par arbre | 5-15 | Sutton & Tinus 1983 |
| Amplification mycorhizes | 100x | Perry, cité ISA |
| Feuilles = % masse totale | 5% | richardstreeservice.com |
| Collets enterrés (urbain) | 93% | Smiley 1991 |

---

## Auteur

**Sky** — l'architecte de l'architecte.

> "Les racines sont toujours plus grandes que l'arbre visible."
