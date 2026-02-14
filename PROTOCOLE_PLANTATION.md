# 🌱 PROTOCOLE DE PLANTATION — Winter Tree

> Ce document est un PROMPT pour Claude.
> Quand Sky décrit une idée de projet, Claude exécute ce protocole AVANT d'écrire du code.

---

## DÉCLENCHEUR

Sky dit quelque chose comme :
- "Je veux faire un [truc]"
- "J'ai une idée pour [truc]"
- "On commence [truc]"
- "Nouveau projet : [truc]"

→ Claude exécute le protocole AVANT TOUTE LIGNE DE CODE.

---

## ÉTAPE 1 : GRAINE 🌰

Extraire de la description :
- **Quoi** : qu'est-ce que ça fait en une phrase
- **Input** : qu'est-ce qui rentre
- **Output** : qu'est-ce qui sort
- **Domaine** : audio, web, mobile, trading, hardware, outil, API, jeu

## ÉTAPE 2 : FAMILLE 🌳

Classifier automatiquement :

| Signal | Famille |
|--------|---------|
| Un flux linéaire input→process→output | 🌲 Conifère |
| Plusieurs modules qui rivalisent en taille | 🍁 Feuillu |
| Un seul chemin critique, output riche | 🌴 Palmier |
| Un gros moteur avec une petite interface | 🌳 Baobab |
| Collection d'outils/fichiers indépendants | 🌿 Buisson |
| Extension d'un système existant | 🌿 Liane |

## ÉTAPE 3 : LES 10 NIVEAUX 🌍

Remplir CHAQUE niveau. Si Claude ne sait pas, mettre `❓ À DÉTERMINER`.
Ne JAMAIS laisser un niveau vide sans raison.

### SOUS LE SOL (ce que Sky ne voit pas — le job de Claude)

```
-5 MYCORHIZES (lois physiques, math, hardware immuable)
   Question : "Quelles lois de la physique/math gouvernent ce projet ?"
   Exemples : FFT, gravité, trigonométrie, limites mémoire, latence réseau

-4 POILS ABSORBANTS (légal, réglementaire)
   Question : "Qu'est-ce qui est interdit ou obligatoire par la loi ?"
   Exemples : GDPR, licences, permissions micro/caméra, normes EN 71

-3 RADICELLES (business, marché, users)
   Question : "Pour qui ? Avec quel budget ? Quelle deadline ?"
   Exemples : App Store rules, public cible, monétisation, deadline

-2 RACINES PIVOTANTES (décisions d'architecture)
   Question : "Quels choix structurants faut-il faire maintenant ?"
   Exemples : natif vs cross-platform, SQL vs NoSQL, monolith vs micro

-1 RACINES STRUCTURELLES (frameworks, libs, APIs)
   Question : "Avec quoi on construit ?"
   Exemples : Flutter, Python, React, NumPy, Firebase
```

### LE SOL (l'interface Sky ↔ Claude)

```
 0 SOL (comment on communique)
   Question : "Comment Sky et Claude vont collaborer sur ce projet ?"
   Exemples : CLI, repo GitHub, fichier de config, API
```

### AU-DESSUS DU SOL (ce que Sky voit — la structure visible)

```
+1 TRONC (core engine, pipeline principal)
   Question : "Quel est le chemin critique ? Le truc sans lequel rien ne marche ?"
   Exemples : main.py, pipeline signal→exec, moteur de matching

+2 BRANCHES (modules majeurs)
   Question : "Quels sont les 3-7 gros blocs fonctionnels ?"
   Exemples : capture, analyse, affichage, export, config

+3 RAMEAUX (sous-features, composants)
   Question : "Quels sous-éléments composent chaque branche ?"
   Exemples : bouton record, graphe fréquences, settings page

+4 FEUILLES (outputs visibles, UI)
   Question : "Qu'est-ce que l'utilisateur voit et touche ?"
   Exemples : écran principal, résultat affiché, fichier exporté

+5 CIME (tests, CI, déploiement)
   Question : "Comment on sait que ça marche ? Comment on le livre ?"
   Exemples : tests unitaires, CI GitHub, build APK, publication
```

## ÉTAPE 4 : ORDRE DE CONSTRUCTION 🔨

La famille dicte l'ordre. PAS de négociation.

### 🌲 Conifère (pipeline)
```
1. Racines (-5 à -1)     → contraintes + stack
2. Tronc (+1)            → pipeline end-to-end minimal
3. Branches (+2)         → modules un par un, SUBORDONNÉS au tronc
4. Rameaux/Feuilles (+3/+4) → détails et UI
5. Cime (+5)             → tests et déploiement
```

### 🌳 Baobab (gros moteur)
```
1. Racines (-5 à -1)     → contraintes physiques d'abord
2. Tronc (+1)            → core engine MASSIF, consolider avant d'étendre
3. Sol (0)               → interface simple (CLI)
4. Branches (+2)         → petites branches, PAS trop tôt
5. Cime (+5)             → tests
```

### 🌴 Palmier (chemin unique)
```
1. Racines (-5 à -1)     → contraintes critiques
2. Tronc (+1)            → LE chemin unique — protéger à tout prix
3. Feuilles (+4)         → output riche au sommet
4. Cime (+5)             → tests du chemin unique
⚠️ JAMAIS de branches (+2) — un palmier n'a PAS de branches
```

### 🍁 Feuillu (multi-modules)
```
1. Racines (-5 à -1)     → contraintes
2. Tronc (+1)            → core minimal
3. Branches (+2)         → modules en PARALLÈLE, surveiller co-dominance
4. Rameaux (+3)          → sous-features
5. Cime (+5)             → tests par module
⚠️ SURVEILLER : si une branche dépasse le tronc → risque co-dominance
```

### 🌿 Buisson (collection)
```
1. Racines (-5 à -1)     → contraintes partagées
2. Tiges (+2)            → lancer plusieurs en parallèle, PAS de tronc
3. Rameaux (+3)          → sous-éléments par tige
4. Cime (+5)             → validation indépendante par tige
⚠️ RÈGLE : chaque tige DOIT rester légère (LOW_INVESTMENT_PER_STEM)
```

### 🌿 Liane (extension)
```
1. Identifier l'hôte     → quel système existant on étend ?
2. Racines (-1)          → API/SDK de l'hôte
3. Point d'attache (+2)  → interface avec l'hôte
4. Croissance (+3/+4)    → features propres
5. Autonomie future ?    → est-ce qu'on tuera l'hôte un jour ?
```

## ÉTAPE 5 : SORTIE 📋

Claude génère :

```yaml
# WINTER TREE — [nom du projet]
# Famille : [emoji] [nom]
# Date plantation : [date]
# Phase : GRAINE

ARBRE:
  -5_mycorhizes:
    - id: M1
      label: "[contenu]"
      status: todo
      entry: ~
      
  -4_poils_absorbants:
    - id: P1
      label: "[contenu]"
      status: todo
      entry: ~

  # ... tous les niveaux ...

  +5_cime:
    - id: C1
      label: "[contenu]"
      status: todo
      entry: ~

ORDRE_CONSTRUCTION:
  phase_1: [ids des nœuds à faire en premier]
  phase_2: [ids suivants]
  phase_3: [ids suivants]

PROCHAIN_PAS: "[la première chose concrète à faire]"
```

## ÉTAPE 6 : PENDANT LE DÉVELOPPEMENT 🔄

À chaque session Claude :
1. Charge l'arbre existant
2. Vérifie : "est-ce que Sky me demande de travailler sur un nœud dont les dépendances sont 🔴 ?"
3. Si oui → ALERTER : "Attends, il manque [racine/tronc] avant de faire [branche/feuille]"
4. Si non → bosser, puis mettre à jour le nœud (status + entry)

### Mise à jour d'un nœud :
```yaml
- id: T1
  label: "Note matching engine"
  status: done          # était: todo
  entry: "lib/mic_engine.dart:340:matchNote()"  # NOUVEAU
  depends: [R1, R3, M1]
  desc: "Moteur de matching fréquence→note, tolérance ±3Hz"
```

Le champ `entry` c'est la BOUSSOLE de Claude dans le code.

---

## RÈGLE D'OR

> **Ne JAMAIS faire pousser une feuille sur un arbre sans tronc.**
> **Ne JAMAIS faire pousser un tronc sur un arbre sans racines.**
> **Les racines d'abord. Toujours.**
