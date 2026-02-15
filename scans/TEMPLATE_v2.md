# 🌲 [NOM DU PROJET] — ARBRE HIVER v2

## METADATA
```yaml
project: "[nom]"
family: conifere | feuillu | palmier | baobab | buisson | liane
repo: "github.com/sky1241/[nom]"
last_updated: "YYYY-MM-DD"
```

## (1) TREE_SILHOUETTE

Dessiner l'arbre de BAS (racines = contraintes fondamentales)
vers le HAUT (cime = tests, packaging, docs).

```
          ☆  Cime (tests, CI, packaging, docs)
         /|\
        / | \  Branches (modules, features)
       /  |  \
      /   |   \
─────/────|────\───── ← LE SOL = interface Sky ↔ Claude
     \    |    /
      \   |   /  Tronc (moteur principal, core)
       \  |  /
        \ | /
         \|/
          ▼  Racines (contraintes fondamentales : physique, hardware, specs)
```

Règles de l'arbre :
- Max 9 branches principales
- Noms sur les nœuds (pas de légende séparée)
- Max 110 caractères de large
- Pas de valeurs/détails dans le dessin
- Les racines sont TOUJOURS plus grandes que l'arbre visible

## (2) NODE_REGISTRY

```yaml
# ── RACINES (contraintes fondamentales) ──
- id: R1
  label: "Nom de la contrainte"
  level: R                              # R=racine, T=tronc, B=branche, C=cime
  parent: null
  status: done                          # done / wip / todo  ← POUR SKY (monter)
  entry: "fichier.py: fonction() L123"  # ← POUR CLAUDE (descendre)
  depends: []                           # ← POUR LES DEUX
  desc: "Description en 1 ligne"

# ── TRONC (moteur principal) ──
- id: T1
  label: "Nom du module core"
  level: T
  parent: R1
  status: wip
  entry: "main.py: Engine.__init__() L45"
  depends: [R1, R2]
  desc: "Description en 1 ligne"

# ── BRANCHES (features, modules) ──
- id: B1
  label: "Nom de la feature"
  level: B
  parent: T1
  status: todo
  entry: "module.py: feature_x() L890"
  depends: [T1]
  desc: "Description en 1 ligne"

# ── CIME (tests, packaging, docs) ──
- id: C1
  label: "Tests"
  level: C
  parent: T1
  status: todo
  entry: "test_main.py: test_suite() L1"
  depends: [B1, B2, B3]
  desc: "Suite de tests complète"
```

## (3) REFERENCES (max 6 par nœud)

```yaml
# Rattacher chaque référence à un nœud par son ID
R1:
  - (code) fichier.py: fonction() — L123 — description
  - (doc) README.md — description
  - (test) test_fichier.py: test_x() — L456

T1:
  - (code) main.py: Engine.run() — L789 — pipeline principal
```

## (4) QUICK SUMMARY

```
Ce projet est surtout un ─── [1 phrase]
Sa famille d'arbre est ─── [conifère/feuillu/palmier/baobab/buisson/liane]
Le tronc est ─────────── [fichier principal + ce qu'il fait]
Les branches dominantes ─ [les 2-3 modules les plus importants]
La contrainte racine la plus forte est ─ [la contrainte #1]
Le risque structurel principal est ─── [le danger #1]
```

## (5) GROWTH RULES (basées sur la famille)

Copier les règles de la famille depuis GROWTH_PATTERNS_6_FAMILIES.md.
Ces règles dictent COMMENT faire pousser l'arbre :
- Conifère → trunk first, branches subordonnées
- Feuillu → branches en parallèle, attention co-dominance
- Palmier → diamètre d'abord, un seul pipeline
- Baobab → consolider le core avant d'étendre
- Buisson → ajouter des tiges indépendantes
- Liane → s'accrocher à l'hôte d'abord

## QUALITY CHECK

```
[ ] Arbre BAS→HAUT, un tronc, max 110 chars de large
[ ] Noms sur nœuds (pas de légende séparée)
[ ] Max 9 branches principales
[ ] NODE_REGISTRY contient TOUS les IDs du dessin
[ ] Chaque nœud a : id, label, level, parent, status, entry, depends, desc
[ ] REFERENCES : max 6 refs/nœud, rattachées à un ID
[ ] QUICK SUMMARY rempli
[ ] GROWTH RULES copiées depuis la bonne famille
[ ] Famille d'arbre identifiée et justifiée
```

## RAPPEL

- **Sky monte** : il regarde status → voit le progrès
- **Claude descend** : il regarde entry → plonge dans le code
- **depends** : les deux savent ce qui bloque quoi
- **Les racines sont toujours plus grandes que l'arbre**
