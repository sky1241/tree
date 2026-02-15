# 🌿 INFERNAL-WHEEL / UX_RESOURCES — ARBRE HIVER v2

## METADATA
```yaml
project: "infernal-wheel/ux_resources"
family: buisson
forme: "Multi-tiges"
desc: "Collection de règles UX (870+ patterns) — web, mobile, WCAG, gamification"
last_updated: "2026-02-14"
```

## (1) TREE_SILHOUETTE

```
  B1-WEB       B2-MOBILE     B3-DESIGN     B4-PROMPTS     B5-SOURCES
  ~450 règles  ~420 règles   Mind-map       Workflows      7 PDFs
  108 sections 61 sections   Décisions      5 modes        276KB
     |             |             |              |              |
     |    iOS      |  Android    |              |              |
     |    HIG      |  M3         |              |              |
     |      \      |  /          |              |              |
     |       \     | /           |              |              |
─────+────────+────+────────+────+──────+───────+──────+───────+─── ← SOL = Sky ↔ Claude
     |        |         |        |           |         |
     R1       R2        R3       R4          R5        R6
   WCAG AA   Touch    Spacing  Contrast   Dynamic    Platform
   4.5:1    44pt/48dp  4px     3:1 UI     Type       iOS+Android
             min       base              scaling     +Web
```

> STRUCTURE BUISSON : Pas de tronc central.
> Chaque tige (B1-B5) est indépendante.
> Les racines (R1-R6) sont les contraintes UNIVERSELLES partagées.

## (2) NODE_REGISTRY

```yaml
# ── RACINES (contraintes fondamentales — PARTAGÉES par toutes les tiges) ──
- id: R1
  label: "WCAG AA Contrast"
  level: R
  parent: null
  status: done
  entry: "WEB.md: Section F (WCAG) + MOBILE.md: Section F"
  depends: []
  desc: "Texte 4.5:1, UI 3:1 — non-négociable"

- id: R2
  label: "Touch Targets"
  level: R
  parent: null
  status: done
  entry: "MOBILE.md: Section A.1 (iOS 44pt) + Section B.1 (Android 48dp)"
  depends: []
  desc: "Taille minimale éléments interactifs par plateforme"

- id: R3
  label: "Spacing System 4px"
  level: R
  parent: null
  status: done
  entry: "WEB.md: Section H + _sources/01_spacing.pdf"
  depends: []
  desc: "Base 4px — 0,4,8,12,16,24,32,48"

- id: R4
  label: "UI Contrast 3:1"
  level: R
  parent: null
  status: done
  entry: "WEB.md: Section F.2 + _sources/03_wcag_rules.pdf"
  depends: []
  desc: "Composants UI, bordures, icônes"

- id: R5
  label: "Dynamic Type"
  level: R
  parent: null
  status: done
  entry: "MOBILE.md: Section A.4 (SF Pro) + Section B.3 (Roboto)"
  depends: []
  desc: "Scaling typographique obligatoire iOS + Android"

- id: R6
  label: "Platform Rules"
  level: R
  parent: null
  status: done
  entry: "MOBILE.md: Sections A (iOS HIG) + B (Material 3)"
  depends: []
  desc: "Respect des conventions plateforme"

# ── TIGES (pas de tronc — buisson = toutes les tiges au même niveau) ──
- id: B1
  label: "WEB.md"
  level: B
  parent: null
  status: done
  entry: "ux_resources/WEB.md L1-??? (112KB, ~450 règles)"
  depends: [R1, R3, R4]
  desc: "Règles web : états, flux, interactions, confiance, couleurs, spacing, data-viz, microcopy, i18n, gamification, tables, settings, search, loading, dark mode, modals, animations, onboarding"

- id: B2
  label: "MOBILE.md"
  level: B
  parent: null
  status: done
  entry: "ux_resources/MOBILE.md L1-??? (69KB, ~420 règles)"
  depends: [R1, R2, R5, R6]
  desc: "Règles mobile : iOS HIG, Material 3, patterns, navigation, accessibilité, i18n, gamification, settings, search, animations"

- id: B3
  label: "DESIGN_TREE.md"
  level: B
  parent: null
  status: done
  entry: "ux_resources/DESIGN_TREE.md L1-??? (14KB)"
  depends: [R1, R2, R3, R4, R5]
  desc: "Mind-map / arbres de décision : tokens → layout → composants → feedback → conversion → accessibilité → patterns avancés"

- id: B4
  label: "Prompts (5 modes)"
  level: B
  parent: null
  status: done
  entry: "ux_resources/prompts/ (5 fichiers, 39KB total)"
  depends: [B1, B2]
  desc: "Mode reprise, CSS fix, calendrier créatif, intégration deep research, prompt deep research massive"

- id: B5
  label: "Sources PDF"
  level: B
  parent: null
  status: done
  entry: "ux_resources/_sources/ (7 PDFs, 1.6MB)"
  depends: []
  desc: "01_spacing, 02_colors, 03_wcag_rules, 04_patterns_2024, 05_patterns_2026, 06_mobile_values, 07_premium_feel"

# ── SOUS-TIGES DE B1 (WEB.md — les sections principales) ──
- id: B1.1
  label: "États & Flux (A-E)"
  level: B
  parent: B1
  status: done
  entry: "WEB.md: Sections A-E"
  depends: [R1]
  desc: "States, user flows, interactions de base, info architecture, trust"

- id: B1.2
  label: "WCAG & Tokens (F-H)"
  level: B
  parent: B1
  status: done
  entry: "WEB.md: Sections F-H"
  depends: [R1, R3, R4]
  desc: "Accessibilité, couleurs sémantiques, spacing system"

- id: B1.3
  label: "Data & Copy (K-M)"
  level: B
  parent: B1
  status: done
  entry: "WEB.md: Sections K-M"
  depends: [R1]
  desc: "Data visualization, microcopy, internationalisation"

- id: B1.4
  label: "Patterns avancés (N-V)"
  level: B
  parent: B1
  status: done
  entry: "WEB.md: Sections N-V"
  depends: [R1, R3]
  desc: "Gamification, tables, settings, search, loading, dark mode, modals, animations, onboarding"

# ── SOUS-TIGES DE B2 (MOBILE.md — les sections principales) ──
- id: B2.1
  label: "iOS HIG (A)"
  level: B
  parent: B2
  status: done
  entry: "MOBILE.md: Section A (touch, margins, safe areas, typo, tab bar, navigation)"
  depends: [R2, R5, R6]
  desc: "44pt, SF Pro, safe areas, tab bar 2-5, navigation push"

- id: B2.2
  label: "Material 3 (B)"
  level: B
  parent: B2
  status: done
  entry: "MOBILE.md: Section B (touch, density, typo, nav bar, nav drawer)"
  depends: [R2, R5, R6]
  desc: "48dp, Roboto, density levels, bottom nav, navigation drawer"

- id: B2.3
  label: "Patterns mobile (C-U)"
  level: B
  parent: B2
  status: done
  entry: "MOBILE.md: Sections C-U"
  depends: [R1, R2]
  desc: "Gestures, forms, validation, feedback, haptics, biometrics, etc."

- id: B2.4
  label: "Avancés mobile (V-Z)"
  level: B
  parent: B2
  status: done
  entry: "MOBILE.md: Sections V-Z"
  depends: [R1, R2]
  desc: "i18n mobile, gamification, settings, search, animations"
```

## (3) GROWTH RULES — Famille : 🌿 Buisson

Collection d'outils indépendants (pas de tronc dominant).

### NO_CENTRAL_TRUNK
- **Règle :** Pas de module principal — tous les composants sont au même niveau
- **Bio :** Pas de tige dominante — toutes égales depuis la base
- **Violation :** Créer une dépendance centrale dont tout dépend
- **Statut ux_resources :** ✅ RESPECTÉ — WEB.md, MOBILE.md, DESIGN_TREE.md sont indépendants

### REDUNDANCY_IS_RESILIENCE
- **Règle :** Si un outil meurt, les autres continuent — pas de single point of failure
- **Bio :** Si une tige meurt, les autres continuent
- **Violation :** Créer des dépendances entre les outils
- **Statut ux_resources :** ✅ RESPECTÉ — tu peux supprimer MOBILE.md, WEB.md continue à fonctionner

### HORIZONTAL_EXPANSION
- **Règle :** Ajouter de nouveaux outils, ne pas approfondir les existants
- **Bio :** Suckering = expansion horizontale par les racines
- **Violation :** Sur-développer un outil au détriment de la collection
- **Statut ux_resources :** ⚠️ ATTENTION — WEB.md (112KB) et MOBILE.md (69KB) sont MASSIFS. Risque de sur-développement d'une tige.

### REJUVENATION_BY_PRUNING
- **Règle :** Le refactoring radical est bénéfique, pas destructif
- **Bio :** Taille radicale → regrowth vigoureux en une saison
- **Violation :** Avoir peur de supprimer/réécrire un outil obsolète
- **Statut ux_resources :** ✅ APPLICABLE — 04_patterns_2024.pdf pourrait être prunée si 05_patterns_2026 la remplace

### LOW_INVESTMENT_PER_STEM
- **Règle :** Chaque outil petit, simple, jetable
- **Bio :** Investissement faible par tige, remplacement facile
- **Violation :** Un outil qui prend plus de temps que la somme des autres
- **Statut ux_resources :** ⚠️ VIOLATION — WEB.md (112KB, 450 règles) est un MONSTRE. Ce n'est plus une tige de buisson, c'est un tronc d'arbre. Scinder ?

### SUCKERING_CLONAL_SPREAD
- **Règle :** Les bons patterns se propagent à travers les outils
- **Bio :** Les rejets créent des colonies clonales
- **Violation :** Chaque outil a ses propres conventions, pas de cohérence
- **Statut ux_resources :** ✅ RESPECTÉ — les valeurs clés (4px, 44pt, 4.5:1) se retrouvent dans TOUS les fichiers

## (4) RISQUES STRUCTURELS

- **WEB.md est trop gros** — 112KB, 450 règles. Ce n'est plus une "tige de buisson", c'est un baobab déguisé. Risque de devenir impossible à maintenir.
- **Duplication cross-fichiers** — gamification est dans WEB.md (Section N) ET MOBILE.md (Section W). Les règles sont-elles identiques ? Divergence = risque.
- **Les PDFs sources sont statiques** — si Apple met à jour le HIG, les PDFs sont obsolètes mais WEB.md/MOBILE.md ne le savent pas.
- **Pas de versioning des règles** — une règle modifiée en février n'a pas d'historique. DESIGN_TREE.md pointe vers des valeurs qui pourraient changer.

## (5) QUICK SUMMARY

```
Ce projet est surtout un ─── Collection de 870+ règles UX cross-platform
Sa famille d'arbre est ─── 🌿 Buisson (Multi-tiges indépendantes)
Le tronc est ─────────── PAS DE TRONC (buisson = toutes tiges égales)
Les tiges dominantes ── WEB.md (450 règles) + MOBILE.md (420 règles)
La contrainte racine la plus forte est ─ R1 WCAG AA (non-négociable)
Le risque structurel principal est ─── WEB.md trop massif = LOW_INVESTMENT_PER_STEM violation
```

## QUALITY CHECK

```
[x] Famille identifiée et justifiée (buisson score 10/10)
[x] Arbre BAS→HAUT, PAS de tronc central, max 110 chars
[x] NODE_REGISTRY contient TOUS les IDs du dessin
[x] Chaque nœud a : id, label, level, parent, status, entry, depends, desc
[x] GROWTH RULES avec statut réel du projet
[x] QUICK SUMMARY rempli
```

## RECOMMANDATIONS DU MOTEUR

1. **Scinder WEB.md** — 112KB viole LOW_INVESTMENT_PER_STEM. Découper en sous-fichiers par domaine (tokens, patterns, advanced) = retour au buisson propre.
2. **Factoriser les doublons** — Gamification (WEB Section N / MOBILE Section W) → un fichier GAMIFICATION.md partagé. Même logique pour Search, Settings, Animations.
3. **Ajouter un CHANGELOG** — Quand une règle change, on le sait. Important pour SUCKERING_CLONAL_SPREAD (propagation cohérente).
