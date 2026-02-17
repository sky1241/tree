# MYCELIUM ENGINE — TODO

## ✅ Complété (v1.0 — analyse statique) — 51 tests

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

## ✅ Complété (v2.0 — croissance extraradical) — 274 tests

| Brique | Nom | Tests | Source | Status |
|--------|-----|-------|--------|--------|
| 13 | Edelstein growth | 30 | Edelstein 1982, Schnepf 2008, Du 2019 | ✅ |
| 14 | Oscillatory signaling | 22 | Goryachev 2012, Wernet 2023, Fleissner 2009 | ✅ |
| 15 | 3D hyphal mechanics | 30 | BMX 2025, Bartnicki-Garcia 1989, Meškauskas 2004 | ✅ |
| 16 | AM fungi root growth | 42 | Schnepf & Roose 2008, Schnepf 2016 | ✅ |
| 17 | Spore germination & chemotaxis | 24 | Peleg 2013, Besserer 2006, Chiu 2001 | ✅ |
| 18 | L-System root architecture | 22 | Leitner 2010, Schnepf 2018 | ✅ |
| 19 | Nutrient transport & P uptake | 16 | Schnepf & Roose 2006, Leitner 2010 | ✅ |
| 20 | C↔P symbiosis exchange | 19 | Kiers 2011, Fellbaum 2012, Chevalier 2025 | ✅ |

## ✅ Complété — Lifecycle chain v1 — 49 tests

Pipeline `full_lifecycle_simulate()` — réseau extraradical complet.

## 🔨 v2.1 — Phase intraradical (briques 21-23)

Le cycle de vie COMPLET d'un AM fungi :

```
                    ┌─────────────────────────────────────────┐
                    │          CYCLE COMPLET AM FUNGI          │
                    └─────────────────────────────────────────┘

SOL (extraradical)                    RACINE (intraradical)
══════════════════                    ═════════════════════

[17] Spore germe                      
  ↓ chemotaxis SL                    
[17] Tube germinatif ──────→ [21] Appressorium (hyphopodium)
                                ↓ pénétration épiderme
[18] Racine L-System            [22] Hyphes intraradicaux
                                  ↓
                                [22] ARBUSCULES ←──── échange C↔P réel
                                  ↓ (turnover 4-10 jours)
                                [22] Vésicules (stockage lipides)
                                  ↓
[16] Émission depuis racine ←── sortie vers sol
  ↓
[13] Branching Edelstein
[15] Mécanique 3D
[14] Signaling oscillatoire
[11] Anastomose/fusion
  ↓
[19] P uptake sol (MM)
[20] C↔P exchange (système)
  ↓
[23] SPORULATION ──→ nouvelles spores ──→ retour [17]
  ↓
[0-10] Métriques réseau
```

### Brique 21 — Appressorium & pénétration
- Hyphopodium : structure d'ancrage sur épiderme racine
- Turgor pressure buildup (mélanine, glycérol)
- Penetration peg → traverse paroi cellulaire
- Prepenetration apparatus (PPA) côté plante
- Status: 🔍 RECHERCHE

### Brique 22 — Phase intraradical (arbuscules + vésicules)
- Hyphes intercellulaires dans cortex racinaire
- ARBUSCULES : structures arborescentes intracellulaires
  - Formation (branching dichotomique dans cellule)
  - Maturité (surface échange max, membrane périarbusculaire)
  - Sénescence + collapse (turnover 4-10 jours)
  - C'est ICI que P↔C s'échange vraiment
- VÉSICULES : stockage lipides (TAG), pas chez Gigasporales
- Status: 🔍 TODO

### Brique 23 — Sporulation (boucle du cycle)
- Production nouvelles spores depuis ERM
- Accumulation lipides (TAG → réserve énergétique)
- Maturation spore (paroi épaisse, multi-nucléée)
- Ferme le cycle : [23] → [17] germination
- Status: 🔍 TODO

## Compteur

| Suite | Tests |
|-------|-------|
| v1.0 (analyse) | 51 |
| v2.0 (extraradical) | 274 |
| Lifecycle chain v1 | 49 |
| v2.1 (intraradical) | 0 — EN COURS |
| **TOTAL actuel** | **374** |

**6790 lignes — 21 briques done — 3 à faire**
