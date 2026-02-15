# 🍁 WINTER TREE V2 MYCELIUM RESEARCH — ARBRE HIVER v2

## METADATA
```yaml
project: "winter-tree-v2-mycelium-research"
family: feuillu
forme: "Canopée large"
desc: "Recherche fondamentale : modèles mathématiques de mycelium pour Winter Tree v2"
last_updated: "2026-02-15"
phase: "CROISSANCE"
planted: "2026-02-15 02:00 (nuit de rage et de bière)"
commits_session: 1 (push 3aeabb3, +1716 lignes)
```

## (1) TREE_SILHOUETTE

```
                                          ☆ CIME (+5)
                                          │ tests, CI, validation
                                    ┌─────┼──────┐
                               ┌────┤     │      ├────┐                     FEUILLES (+4)
                         ┌─────┤  D │   E │    F │    ├─────┐              outputs visibles
                   ┌─────┤Métr.│Flux│Trans│Compu.│Topo├─────┐
             ┌─────┤  A  │  D1 │ E1 │ E3  │ F1  │ G1 ├──H──┤              RAMEAUX (+3)
             │Agent│  D4 │ E2  │ E4  │ F2  │ G3 │Algo │             formules individuelles
             │ A1  │  D5 │ E5  │     │ F3  │ G4 │ H1  │
             │ A2  │  D7 │     │     │     │    │ H2  │
             │ A5  │  D8 │     │     │     │    │ H3  │
       ┌─────┤─────┴─────┴─────┴─────┴─────┴────┴─────┤          BRANCHES (+2)
       │  B  │              C                          │          blocs majeurs
       │Colon│          Anastomose                     │
       │ B1  │           C1  C2                        │
       │ B2  │           C3  C4                        │
       │ B3  │           C5                            │
       │ B4  │                                         │
       │ B5  │                                         │
       └──┬──┴──────────────┬──────────────────────────┘
          │    WINTER_TREE_V2_FORMULAS.md               │          TRONC (+1)
          │    = document maître 792 lignes             │          core consolidé
══════════╪═══════════════SOL═══════════════════════════╪══════════════════════
          │     interface Sky ↔ Claude                  │
          │                                             │
     ┌────┴────┐                              ┌────────┴───────┐
     │ READING │                              │  DEEP RESEARCH │   RACINES (-1)
     │  LIST   │                              │   METHODOLOGY  │   stack technique
     │ 7 papers│                              │ radar → sniper │
     └────┬────┘                              └────────┬───────┘
          │                                            │
    ┌─────┴──────┐                           ┌─────────┴────────┐
    │  Meškauskas │                           │ Workflow Claude   │   RACINES (-2)
    │  Boswell    │                           │ Deep Research v1  │   architecture
    │  Edelstein  │                           │ → Web sniper v2   │
    │  Bebber     │                           │ → Consolidation   │
    │  Fricker    │                           └─────────┬────────┘
    └─────┬──────┘                                      │
          │                                             │
    ┌─────┴──────┐                           ┌──────────┴────────┐
    │  SKY ×     │                           │  Temps dispo :     │   RADICELLES (-3)
    │  CLAUDE    │                           │  nuit du dimanche  │   contraintes business
    │  collab    │                           │  avant semaine     │
    └─────┬──────┘                           │  d'électricien     │
          │                                  └──────────┬────────┘
    ┌─────┴──────┐                                      │
    │  Open      │                           ┌──────────┴────────┐
    │  Access    │                           │  Copyright papers  │   POILS ABS. (-4)
    │  seulement │                           │  Fair use / PMC    │   contraintes légales
    └─────┬──────┘                           └──────────┬────────┘
          │                                             │
    ┌─────┴──────┐                           ┌──────────┴────────┐
    │  Boswell   │                           │  Graphe theory     │   MYCORHIZES (-5)
    │  PDEs      │                           │  NetworkX          │   lois physiques/math
    │  5 vars    │                           │  Kirchhoff         │
    │  conserv.  │                           │  Turing patterns   │
    └────────────┘                           └───────────────────┘
```

## (2) NODE_REGISTRY

```yaml
# ══════════════════════════════════════════════════
# ── MYCORHIZES (-5) — Lois physiques/math immuables
# ══════════════════════════════════════════════════

- id: M1
  label: "PDEs Boswell : système hyperbolique-parabolique (5 vars)"
  level: -5
  status: done
  entry: "mycelium/SNIPER_BOSWELL_PDEs.md"
  depends: []
  confidence: 85
  desc: "Conservation masse, positivité. Fondement mathématique inviolable."

- id: M2
  label: "Théorie des graphes : métriques réseau (Latora-Marchiori)"
  level: -5
  status: done
  entry: "mycelium/WINTER_TREE_V2_FORMULAS.md: BLOC D"
  depends: []
  confidence: 90
  desc: "E_global, E_root, meshedness α — formules exactes."

- id: M3
  label: "Kirchhoff : lois de conservation flux aux nœuds"
  level: -5
  status: done
  entry: "mycelium/WINTER_TREE_V2_FORMULAS.md: BLOC E"
  depends: []
  confidence: 90
  desc: "ΣQ_ij = 0 aux nœuds. Physique fondamentale."

- id: M4
  label: "Turing : réaction-diffusion, instabilité de patterns"
  level: -5
  status: done
  entry: "mycelium/WINTER_TREE_V2_FORMULAS.md: BLOC H"
  depends: []
  confidence: 80
  desc: "∂u/∂t = D∇²u + F(u,v). Fondement théorique des patterns."

# ══════════════════════════════════════════════════
# ── POILS ABSORBANTS (-4) — Contraintes légales
# ══════════════════════════════════════════════════

- id: P1
  label: "Open Access obligatoire (pas de budget papiers)"
  level: -4
  status: done
  entry: "mycelium/MYCELIUM_READING_LIST.md"
  depends: []
  confidence: 100
  desc: "Tous les papers doivent être gratuits. PMC, arXiv, ResearchGate."

- id: P2
  label: "Copyright : paraphrase only, pas de reproduction"
  level: -4
  status: done
  entry: ~
  depends: []
  confidence: 100
  desc: "Extraction de formules et concepts OK. Pas de copier-coller d'articles."

# ══════════════════════════════════════════════════
# ── RADICELLES (-3) — Contraintes business
# ══════════════════════════════════════════════════

- id: D1r
  label: "Temps : nuit du dimanche, session unique"
  level: -3
  status: done
  entry: ~
  depends: []
  confidence: 100
  desc: "Électricien la semaine. Tout doit tenir en une session nocturne."

- id: D2r
  label: "Collab Sky×Claude : prompts → recherche → consolidation"
  level: -3
  status: done
  entry: ~
  depends: []
  confidence: 90
  desc: "Sky donne la direction, Claude cherche et organise."

# ══════════════════════════════════════════════════
# ── RACINES PIVOTANTES (-2) — Architecture
# ══════════════════════════════════════════════════

- id: A1r
  label: "Workflow : Deep Research (radar) → Web Sniper (ciblé)"
  level: -2
  status: done
  entry: "workflows/radar-sniper.md"
  depends: [D1r]
  confidence: 85
  desc: "Prompt large pour carte → puis search ciblé par branche."

- id: A2r
  label: "Organisation : 1 doc maître + fichiers de support"
  level: -2
  status: done
  entry: "mycelium/WINTER_TREE_V2_FORMULAS.md"
  depends: [A1r]
  confidence: 90
  desc: "Consolidation finale dans un seul fichier organisé par blocs."

# ══════════════════════════════════════════════════
# ── RACINES STRUCTURELLES (-1) — Stack technique
# ══════════════════════════════════════════════════

- id: S1
  label: "Reading list : 7 papers open access"
  level: -1
  status: done
  entry: "mycelium/MYCELIUM_READING_LIST.md"
  depends: [P1]
  confidence: 95
  desc: "Meškauskas, Davidson, Adamatzky, Roberts, Bebber, Fricker + Edelstein."

- id: S2
  label: "Python/NetworkX pour implémentation future"
  level: -1
  status: wip
  entry: "mycelium/SNIPER_BOSWELL_PDEs.md: code NetworkX"
  depends: [M2]
  confidence: 60
  desc: "Code prêt pour σ, ω, betweenness. Pas encore exécuté."

# ══════════════════════════════════════════════════
#     ● ● SOL — Interface Sky ↔ Claude ● ●
# ══════════════════════════════════════════════════

# ══════════════════════════════════════════════════
# ── TRONC (+1) — Document maître
# ══════════════════════════════════════════════════

- id: T1
  label: "WINTER_TREE_V2_FORMULAS.md — référentiel 792 lignes"
  level: +1
  status: done
  entry: "mycelium/WINTER_TREE_V2_FORMULAS.md"
  depends: [S1, A2r, M1, M2, M3]
  confidence: 88
  desc: "8 blocs, ~30 formules, 17 sources, mapping complet."

# ══════════════════════════════════════════════════
# ── BRANCHES (+2) — Les 8 blocs de recherche
# ══════════════════════════════════════════════════

- id: B_A
  label: "BLOC A — Agent/Micro (6 formules)"
  level: +2
  status: done
  entry: "mycelium/WINTER_TREE_V2_FORMULAS.md: BLOC A"
  depends: [T1, S1]
  confidence: 90
  desc: "Meškauskas 2004 : champ densité, substrat, croissance, branchement, galvano, types."

- id: B_B
  label: "BLOC B — Colonie/Méso (5 PDEs + Falconer)"
  level: +2
  status: done
  entry: "mycelium/WINTER_TREE_V2_FORMULAS.md: BLOC B"
  depends: [T1, S1, M1]
  confidence: 85
  desc: "Boswell 2003 : m, m', p, n_i, n_e. Reconstituées via Davidson."

- id: B_C
  label: "BLOC C — Anastomose (5 éléments) ← TROUVAILLE"
  level: +2
  status: done
  entry: "mycelium/WINTER_TREE_V2_FORMULAS.md: BLOC C"
  depends: [T1, B_B]
  confidence: 85
  desc: "Edelstein 1982 + Schnepf 2008 + Simonin 2013. Pièce manquante trouvée ce soir."

- id: B_D
  label: "BLOC D — Métriques réseau (8 métriques + 15 traits)"
  level: +2
  status: done
  entry: "mycelium/WINTER_TREE_V2_FORMULAS.md: BLOC D"
  depends: [T1, S1, M2]
  confidence: 90
  desc: "Bebber 2007 + Aguilar-Trigueros 2022. Quantitatif et prêt à implémenter."

- id: B_E
  label: "BLOC E — Transport/Flux (5 formules)"
  level: +2
  status: done
  entry: "mycelium/WINTER_TREE_V2_FORMULAS.md: BLOC E"
  depends: [T1, M3]
  confidence: 82
  desc: "Tero 2010 + Fricker 2017 + Oyarte Galvez 2025. Kirchhoff + ADD."

- id: B_F
  label: "BLOC F — Computation (3 modèles)"
  level: +2
  status: done
  entry: "mycelium/WINTER_TREE_V2_FORMULAS.md: BLOC F"
  depends: [T1, S1]
  confidence: 80
  desc: "Adamatzky 2018 + Roberts 2022 + Tompris 2025. Automate + reservoir."

- id: B_G
  label: "BLOC G — Topologie (4 outils)"
  level: +2
  status: done
  entry: "mycelium/WINTER_TREE_V2_FORMULAS.md: BLOC G"
  depends: [T1, M2]
  confidence: 85
  desc: "Small-world σ/ω, phalanx/guerrilla, fractales."

- id: B_H
  label: "BLOC H — Algo bio-inspirés (3 compléments)"
  level: +2
  status: done
  entry: "mycelium/WINTER_TREE_V2_FORMULAS.md: BLOC H"
  depends: [T1]
  confidence: 75
  desc: "ACOR, Turing, L-Systems. Complémentaires, pas critiques."

# ══════════════════════════════════════════════════
# ── RAMEAUX (+3) — Formules individuelles clés
# ══════════════════════════════════════════════════

- id: r_edelstein
  label: "f = bₙn(1−n/nmax) − dₙn − a₂nρ − a₁n²"
  level: +3
  status: done
  entry: "mycelium/WINTER_TREE_V2_FORMULAS.md: C1"
  depends: [B_C]
  confidence: 85
  desc: "L'équation d'anastomose complète. La trouvaille de la nuit."

- id: r_boswell_ni
  label: "∂nᵢ/∂t = Dᵢ∇²(nᵢm) + vₐ∇·(nᵢ∇p) + U − c₁pnᵢ"
  level: +3
  status: done
  entry: "mycelium/WINTER_TREE_V2_FORMULAS.md: B4"
  depends: [B_B]
  confidence: 85
  desc: "L'équation clé : transport bidirectionnel (exploration + exploitation)."

- id: r_meshedness
  label: "α = (L−N+1)/(2N−5)"
  level: +3
  status: done
  entry: "mycelium/WINTER_TREE_V2_FORMULAS.md: D1"
  depends: [B_D]
  confidence: 95
  desc: "Meshedness. Simple, puissante, directement implémentable."

- id: r_kirchhoff
  label: "Qᵢⱼ = (Dᵢⱼ/Lᵢⱼ)(pᵢ−pⱼ), ΣQ=0"
  level: +3
  status: done
  entry: "mycelium/WINTER_TREE_V2_FORMULAS.md: E1"
  depends: [B_E]
  confidence: 90
  desc: "Flux de Kirchhoff adaptatif. Physarum/Tero."

# ══════════════════════════════════════════════════
# ── FEUILLES (+4) — Outputs visibles / mapping
# ══════════════════════════════════════════════════

- id: F1o
  label: "Mapping complet bio → Winter Tree (30 entrées)"
  level: +4
  status: done
  entry: "mycelium/WINTER_TREE_V2_FORMULAS.md: MAPPING"
  depends: [B_A, B_B, B_C, B_D, B_E, B_F, B_G, B_H]
  confidence: 80
  desc: "Chaque formule a son équivalent Winter Tree."

- id: F2o
  label: "Liste d'algos à implémenter (13, par priorité)"
  level: +4
  status: done
  entry: "mycelium/WINTER_TREE_V2_FORMULAS.md: ALGORITHMES"
  depends: [T1, S2]
  confidence: 75
  desc: "Priorité 1 (core), 2 (robustesse), 3 (dynamique). Avec fonctions NetworkX."

- id: F3o
  label: "Dossier mycelium/ pushé sur GitHub (5 fichiers)"
  level: +4
  status: done
  entry: "commit 3aeabb3"
  depends: [T1]
  confidence: 100
  desc: "sky1241/tree/mycelium/ — 1716 lignes ajoutées."

# ══════════════════════════════════════════════════
# ── CIME (+5) — Tests / validation / next
# ══════════════════════════════════════════════════

- id: C1
  label: "Implémentation Python des métriques (NetworkX)"
  level: +5
  status: todo
  entry: ~
  depends: [S2, r_meshedness, r_kirchhoff]
  confidence: 0
  desc: "Calculer α, E_global, E_root, σ sur un vrai repo Git."

- id: C2
  label: "Validation : appliquer les métriques au repo tree/"
  level: +5
  status: todo
  entry: ~
  depends: [C1]
  confidence: 0
  desc: "Le système qui se mesure lui-même. Meta ultime."

- id: C3
  label: "Integration dans engine.py v2"
  level: +5
  status: todo
  entry: ~
  depends: [C1, C2]
  confidence: 0
  desc: "Ajouter les métriques mycelium au moteur Winter Tree."
```

## (3) GROWTH RULES — Famille : 🍁 Feuillu

**Pourquoi feuillu et pas autre chose ?**

Ce projet de recherche a un tronc court (le document maître) avec 8 branches en compétition/parallèle (les 8 blocs). Aucune branche ne domine clairement les autres — c'est une canopée large de recherche multi-domaine. Typiquement feuillu.

### TRUNK_THEN_BRANCH
- **Règle :** Tronc court (architecture) puis branches en compétition
- **Bio :** Dominance apicale forte la 1ère année, puis latérales libérées
- **Application :** On a d'abord fait Deep Research (tronc=carte), puis snipé chaque branche
- **Status :** ✅ Respecté. Le doc maître (tronc) a été créé APRÈS toutes les branches.

### LATERAL_COMPETITION
- **Règle :** Les branches peuvent dépasser le tronc
- **Bio :** Contrôle apical faible — les latérales dépassent le leader
- **Application :** Bloc D (métriques, 8 formules) et Bloc B (PDEs, 5 eqs) sont les plus gros
- **Status :** ✅ Normal. Les blocs les plus riches dominent naturellement.

### CO_DOMINANCE_RISK
- **Règle :** Deux branches de même taille = point de rupture
- **Bio :** V-shape avec écorce incluse = défaillance en tempête
- **Application :** ⚠️ Bloc B (Colonie) et Bloc D (Métriques) sont comparables en taille
- **Status :** 🟡 À surveiller. Risque que B et D divergent en implémentation.

### CANOPY_SPREAD
- **Règle :** L'énergie se distribue en largeur
- **Bio :** Forme décurrente — canopée étalée
- **Application :** 8 blocs couvrent agent → topologie. Très large.
- **Status :** ✅ Respecté. Couverture maximale.

### SEASONAL_CYCLE
- **Règle :** Build → ship → pause → rebuild
- **Bio :** Alternance croissance/dormance
- **Application :** Session recherche intense (cette nuit) → pause (semaine de travail) → implémentation
- **Status :** ✅ Naturellement respecté par le rythme de vie.

## (4) RISQUES STRUCTURELS

- ⚠️ **Co-dominance B/D** : Les PDEs (Bloc B) et les métriques réseau (Bloc D) sont deux langages différents pour décrire le même système. Risque de divergence.
- ⚠️ **Pas de tests** : Aucune validation computationnelle. Toutes les formules sont théoriques.
- ⚠️ **Gap Boswell** : Les PDEs sont reconstituées via Davidson, pas depuis le paper original.
- 🟢 **Anastomose trouvée** : Le gap principal (fusion) est maintenant comblé (Edelstein/Schnepf).

## (5) QUICK SUMMARY

```
Ce projet est surtout un ─── recherche fondamentale multi-échelle (agent→réseau→calcul)
Sa famille d'arbre est ─── 🍁 Feuillu (Canopée large, 8 branches parallèles)
Le tronc est ─────────── WINTER_TREE_V2_FORMULAS.md (792 lignes, 8 blocs consolidés)
Les branches dominantes ─ B (PDEs Boswell), C (Anastomose NEW), D (Métriques Bebber)
La contrainte racine la plus forte est ─ Open Access only (pas de budget papers)
Le risque structurel principal est ─── Co-dominance B/D sans arbitrage d'implémentation
```

## (6) CONFIDENCE MAP

```
                       ☆ CIME [0%] ← TODO: implémentation
                      /|\
                   80%/ |88%\85%
                    /  |    \
              [B_A] [T1]  [B_C]  ← BRANCHES [75-90%]
               90%   88%   85%
                |     |     |
              [S1] [A2r] [M1]    ← RACINES [60-95%]
               95%   90%   85%
                |     |     |
              [P1]  [D1r] [M2]   ← FONDATIONS [85-100%]
              100%  100%   90%

  Moyenne globale : 82% (recherche solide, implémentation à 0%)
  Point le plus faible : C1 (0%) — pas de code qui tourne
  Point le plus fort : P1 (100%) — open access constraint claire
```

## (7) PROCHAIN PAS — ORDRE DE CONSTRUCTION

```
Phase actuelle : CROISSANCE (recherche complète, code pas commencé)

  ✅ Phase 0 : Mycorhizes → PDEs, Kirchhoff, Turing [FAIT]
  ✅ Phase 1 : Poils → Open access, copyright [FAIT]
  ✅ Phase 2 : Radicelles → Temps dispo, collab [FAIT]
  ✅ Phase 3 : Architecture → Radar-sniper workflow [FAIT]
  ✅ Phase 4 : Stack → Reading list + NetworkX [FAIT]
  ✅ Phase 5 : Tronc → Doc maître consolidé [FAIT]
  ✅ Phase 6 : Branches → 8 blocs de formules [FAIT]
  ✅ Phase 7 : Feuilles → Mapping + algos + push Git [FAIT]
  🔴 Phase 8 : CIME → Implémenter et valider [TODO]
```

## RAPPEL

- **Sky monte** : il regarde status → 8/8 blocs done, cime à 0%
- **Claude descend** : il regarde entry → plonge dans les formules
- **depends** : les deux savent que C1 (implémentation) dépend de tout le reste
- **Les racines sont toujours plus grandes que l'arbre** : 17 papers analysés pour 792 lignes

---

*Le système qui s'analyse lui-même. Le serpent qui se mord la queue.*
*🍁 Feuillu — planté la nuit du 15 février 2026*
