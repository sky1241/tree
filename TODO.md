# MYCELIUM ENGINE — TODO

## ✅ Complété (v1.0 — analyse statique)

| Brique | Nom | Tests | Source |
|--------|-----|-------|--------|
| 0 | Construction de graphe | 13 | — |
| 1 | Meshedness α | 10 | Haggett-Chorley 1969 |
| 2 | Efficacité globale | 2 | Latora-Marchiori 2001 |
| 3 | Efficacité root | 5 | Latora-Marchiori 2001 |
| 4 | Volume-MST ratio | 4 | Bebber 2007 |
| 5 | Betweenness centrality | 2 | Freeman 1977 / Newman 2003 |
| 6 | Robustesse | 6 | Albert-Barabási 2000 |
| 7 | Small-world σ | 4 | Humphries-Gurney 2008 |
| 8 | Small-world ω | 1 | Telesford 2011 |
| 9 | Stratégie phalanx/guerrilla | 4 | Bebber + Tero composite |
| 10 | Kirchhoff + Physarum | 16 | Tero 2007, Ito 2011, Tero 2010 |
| 11 | Anastomose | 14 | Edelstein 1982, Glass 2006 |
| 12 | Intégration complète | 39 | — |
| **TOTAL v1.0** | | **51** | |

## ✅ Complété (v2.0 — modèles de croissance)

| Brique | Nom | Tests | Source | Status |
|--------|-----|-------|--------|--------|
| 13 | Edelstein growth (branching + death + densité) | 30 | Edelstein 1982, Schnepf 2008, Du 2019 | ✅ DONE |
| 14 | Oscillatory signaling (hyphes qui se cherchent) | 22 | Goryachev 2012, Wernet 2023, Fleissner 2009 | ✅ DONE |
| 15 | 3D hyphal mechanics (croissance filament) | 30 | BMX 2025, Bartnicki-Garcia 1989, Meškauskas 2004 | ✅ DONE |
| 16 | AM fungi root growth (croissance depuis racine) | 42 | Schnepf & Roose 2008, Schnepf 2016 | ✅ DONE |
| 17 | Germination de spores & chemotaxis | 24 | Peleg 2013, Besserer 2006, Chiu 2001 | ✅ DONE |
| 18 | L-System root architecture | 22 | Leitner 2010, Schnepf 2018 (CRootBox) | ✅ DONE |
| 19 | Nutrient transport & P uptake | 16 | Schnepf & Roose 2006, Leitner 2010 | ✅ DONE |
| 20 | C↔P symbiosis exchange | 19 | Kiers 2011, Fellbaum 2012, Chevalier 2025 | ✅ DONE |
| **TOTAL v2.0** | | **274** | | |

## ✅ Complété — LIFECYCLE CHAIN (ordre biologique)

Pipeline `full_lifecycle_simulate()` — toutes les briques dans l'ordre du cycle de vie :

```
PHASE 0: SETUP
  [18] L-System root → racine 3D dans le sol
       ↓ root_tips + positions
PHASE 1: GERMINATION
  [17] Spore germination → chemotaxis vers strigolactone
       ↓ germ tube tips → connectés aux root tips
PHASE 2: COLONISATION + MATURATION
  [16] Root emission → hyphes depuis interface racine
  [13] Edelstein growth → branching, death, densité
  [15] 3D mechanics → Lockhart, Spitzenkörper, gravitropisme
  [14] Oscillatory signaling → FHN, tips se cherchent
  [11] Anastomose → fusion des hyphes synchronisés
       ↓ réseau mature
PHASE 2b: SPATIAL FUSION
  Intra-component fusion for connectivity
PHASE 2c: PRUNING
  Orphan component removal → active graph (1 component)
       ↓ graphe mature connecté
PHASE 3: FONCTION — P UPTAKE
  [19] Michaelis-Menten uptake + diffusion sol + transport vers racine
       ↓ total P delivered
PHASE 4: FONCTION — C↔P EXCHANGE
  [20] Reciprocal rewards (Kiers 2011), obligate biotroph
       ↓ plant P, fungal C, symbiosis stability
PHASE 5: ANALYSE
  [0-10] Toutes métriques v1.0 sur graphe final :
         meshedness, efficiency, root_eff, volume_mst,
         bottlenecks, robustness, strategy, kirchhoff,
         physarum, small_world σ+ω
```

### Joints vérifiés

| Joint | De → Vers | Mécanisme |
|-------|-----------|-----------|
| 0→1 | Root → Spore | root_tip positions = source SL |
| 1→2 | Spore → AM | germ tips connectés aux root tips, fake roots skippés |
| 2→2b | AM → Spatial fusion | intra-component fusion |
| 2b→2c | Fusion → Pruning | remove orphan components |
| 2→3 | AM → Nutrient | graphe mature direct, root nodes = P sinks |
| 3→4 | Nutrient → Symbiosis | real P from phase 3 → soil_p for exchange |
| 4→5 | Exchange → Metrics | v1.0 metrics on pruned active graph |

### Tests lifecycle : 49

## Compteur total

| Suite | Tests |
|-------|-------|
| v1.0 (analyse) | 51 |
| v2.0 (croissance) | 274 |
| Lifecycle chain | 49 |
| **TOTAL** | **374** |

**6790 lignes — 21 briques — 1 pipeline lifecycle complet**

## Notes

v1.0 = moteur d'**analyse** (photo du réseau à un instant t)
v2.0 = moteur de **croissance** (le réseau pousse dans le temps)
Lifecycle = **chaîne complète** spore → réseau mature → P delivery → métriques

Chaque brique v2.0 suit le même workflow:
1. Recherche internet (papiers)
2. Extraction des équations
3. Traduction code discret
4. Tests unitaires
5. Push git
