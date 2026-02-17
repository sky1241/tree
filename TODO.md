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

| Brique | Nom | Tests | Source |
|--------|-----|-------|--------|
| 13 | Edelstein growth | 30 | Edelstein 1982, Schnepf 2008, Du 2019 |
| 14 | Oscillatory signaling | 22 | Goryachev 2012, Wernet 2023, Fleissner 2009 |
| 15 | 3D hyphal mechanics | 30 | BMX 2025, Bartnicki-Garcia 1989, Meškauskas 2004 |
| 16 | AM fungi root growth | 42 | Schnepf & Roose 2008, Schnepf 2016 |
| 17 | Spore germination & chemotaxis | 24 | Peleg 2013, Besserer 2006, Chiu 2001 |
| 18 | L-System root architecture | 22 | Leitner 2010, Schnepf 2018 |
| 19 | Nutrient transport & P uptake | 16 | Schnepf & Roose 2006, Leitner 2010 |
| 20 | C↔P symbiosis exchange | 19 | Kiers 2011, Fellbaum 2012, Chevalier 2025 |

## ✅ Complété (v2.1 — phase intraradical + boucle) — 60 tests

| Brique | Nom | Tests | Source |
|--------|-----|-------|--------|
| 21 | Appressorium (Hyphopodium) | 19 | Howard 1991, Genre 2005, Nagahashi 1997 |
| 22 | Arbuscules & Vésicules | 20 | Pimprikar 2018, Floss 2017, Genre 1997 |
| 23 | Sporulation (boucle) | 21 | Kokkoris 2026, Pfeffer 1999, Bago 2002 |

## ✅ Lifecycle chain v1 — 49 tests

Pipeline `full_lifecycle_simulate()` — réseau extraradical complet.

## Cycle de vie COMPLET AM fungi — A à Z

```
                    ┌─────────────────────────────────────────┐
                    │     CYCLE COMPLET AM FUNGI — BOUCLÉ     │
                    └─────────────────────────────────────────┘

SOL (extraradical)                    RACINE (intraradical)
══════════════════                    ═════════════════════

[17] Spore germe ←──────────────────── [23] Sporulation (BOUCLE ✅)
  ↓ chemotaxis SL
[17] Tube germinatif ──────→ [21] Appressorium (hyphopodium) ✅
                                ↓ turgor + pénétration
[18] Racine L-System            [22] Hyphes intraradicaux ✅
                                  ↓
                                [22] ARBUSCULES ✅ (turnover 2-7j)
                                  ↓ échange C↔P réel
                                [22] Vésicules (TAG storage) ✅
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
[23] SPORULATION ──→ nouvelles spores ──→ retour [17] ✅
  ↓
[0-10] Métriques réseau
```

## Compteur final

| Suite | Tests |
|-------|-------|
| v1.0 (analyse statique) | 51 |
| v2.0 (extraradical) | 274 |
| v2.1 (intraradical + boucle) | 60 |
| Lifecycle chain v1 | 49 |
| **TOTAL** | **434** |

**7748 lignes — 24 briques — CYCLE COMPLET BOUCLÉ**

## 🔴 EN COURS — Intégration pipeline lifecycle

### Bataille 1: Intégrer 21-22-23 dans full_lifecycle_simulate()
- [ ] Phase 1.5: appressorium_simulate() après joint 1→2
- [ ] Phase 2a: intraradical_simulate() après phase 1.5
- [ ] Phase 5.5: sporulation_simulate() après phase 4
- [ ] Joint 23→17: boucle retour vers germination
- [ ] Tests lifecycle mis à jour (49 → ??)

### Bataille 2: Vérifier équations avec sources fraîches
- [ ] Turgor van't Hoff: Π = c·R·T → 1.98 MPa
- [ ] Arbuscule turnover: 2-7 jours
- [ ] TAG fraction: 58-80%
- [ ] Sporulation rate: r = r_max × C/(Kc+C) × Kp/(Kp+P)
- [ ] Carbon budget: 38 → 6.3 μg

### Bataille 3: Bug hunting systématique
- [ ] Edge cases (0 spores, 0 tips, empty graphs)
- [ ] Division par zéro
- [ ] Cohérence d'unités entre briques
- [ ] Overflow / underflow
- [ ] Re-run 434+ tests
