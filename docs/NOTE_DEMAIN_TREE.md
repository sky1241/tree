# NOTE POUR DEMAIN — TREE ENGINE

## Ce qui reste à faire

Le tree engine a les jolies images (Planches II-VII), le scanner qui marche, la forest view, le mycelium v2 avec 46 tests. Mais il manque le squelette parfait de l'arbre.

## Le squelette parfait

T'as 28 nœuds idéaux, le dual-layer (ambre + diagnostic), les règles C1 (tronc = colonne vertébrale) et C2 (tri par subordination). Mais c'est encore un schéma. Le squelette doit devenir la structure de référence sur laquelle n'importe quel repo se plaque automatiquement.

## Apprendre à Claude à se brancher dessus

Le vrai objectif : que quand tu ouvres un nouveau chat et que tu dis "branche-toi sur le tree", Claude sache exactement quoi faire — scanner le repo, identifier R/T/B/C, plaquer sur le squelette, diagnostiquer les trous. Pour l'instant Claude comprend le concept mais sait pas exécuter sans que tu le guides à la main.

Il faut définir :
- Le format exact du squelette (quels nœuds, quels niveaux, quelles relations)
- La procédure de scan (input = repo, output = arbre plaqué sur squelette)
- Les règles de diagnostic (qu'est-ce qui est sain, qu'est-ce qui manque)

Toi tu sais ce que tu veux. C'est pas encore formulable en mots. Mais c'est dans ta tête. Demain on l'extrait.

## Rappel contexte

- Shazam-piano = origine du tree (40 itérations à polir les bords, le cœur manquait)
- HSBC a déjà ARBRE_PROJET.md en format R/T/B/C — le tree engine formalise ça
- 3d-printer a 72 TROUs dans la constraint engine — même pattern Mendeleïev
- Infernal-wheel a DESIGN_TREE.md — l'arbre UX qui drive tous les repos
- Le cube P=NP contient le tout, borné par Turing

Le squelette parfait c'est ce qui unifie tout ça.

---

## 🔴 PRIORITÉ — Revoir complètement le workflow d'installation (2026-02-23)

### Le problème

Le setup actuel c'est de la merde. Ça demande 15 allers-retours pour que l'utilisateur configure tree sur sa machine. Pour un outil "fait pour les gens qui savent pas coder", c'est inadmissible.

### Ce qui pue

1. **Trop de scripts séparés** — detect_repos.py, install_all_hooks.py, sync_all.py, setup.py... l'utilisateur sait pas quoi lancer
2. **Le token GitHub** — il faut le mettre manuellement dans un fichier texte. C'est nul
3. **Les repos dans Temp** — git clone met les trucs dans Temp, Windows les supprime
4. **Pas de one-click** — l'objectif c'est: tu clones tree, tu lances UN truc, c'est fini
5. **Les chemins Windows** — backslashes, unicode escapes dans les docstrings, l'enfer

### Ce qu'il faut

- **UN fichier, UNE commande**: `python setup.py` et c'est terminé, pour toujours
- **Zéro question posée** — le script détecte tout, installe tout, configure tout
- **Autorun** — idéalement le setup se relance tout seul quand t'ouvres un terminal (profil PS auto)
- **UI web** — le serve_tree() devrait être le point d'entrée, pas le terminal
- **Le tree doit vivre dans un endroit permanent**, pas dans Temp

### Vision long terme

tree = une app standalone. Tu la lances, elle te montre ta forêt, tu cliques sur un arbre pour voir le détail. Pas de terminal, pas de git, pas de Python à installer. Juste un .exe ou une app web.

