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

## Structure du repo

```
tree/
├── README.md                          ← Tu es ici
├── GROWTH_PATTERNS_6_FAMILIES.md      ← Recherche complète sur les 6 familles
├── MASTER_PROMPT_SKY.md               ← Prompt maître à donner à tout Claude
├── HANDOFF_SESSION_2026-02-14.md      ← Résumé pour passer le relais
├── prompts/
│   ├── MICR_DEEP_RESEARCH_v2_SURGICAL.md
│   └── code-audit-template.md
├── workflows/
│   ├── radar-sniper.md
│   ├── BATTLE_PLAN_2026-02-15_DEFINITIF.md
│   └── LISTE_DE_COURSES_DIMANCHE.md
└── winter-trees/
    └── TEMPLATE_v2.md
```

## Références

- **Lindenmayer (1968)** — L-Systems : grammaire de croissance des plantes
- **Prusinkiewicz & Lindenmayer** — "The Algorithmic Beauty of Plants"
- **Tomer & Schach (2000)** — "Evolution Tree" pour le cycle de vie logiciel
- **Martin Fowler** — "Strangler Fig Application"
- **Barnes (2013, CMU)** — "Software Architecture Evolution"

## Auteur

Sky — l'architecte de l'architecte.
