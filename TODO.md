# MYCELIUM ENGINE — TODO

## ✅ Complété (v1.0)

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
| **TOTAL** | | **120** | |

## 🔨 À faire (v2.0 — modèles de croissance)

| Brique | Nom | Source | Status |
|--------|-----|--------|--------|
| 13 | Edelstein growth (branching + death + densité) | Edelstein 1982 J. Theor. Biol. 98:679 | TODO |
| 14 | Oscillatory signaling (hyphes qui se cherchent) | eLife 2023 (Fleissner), Goryachev 2006 | TODO |
| 15 | 3D hyphal mechanics (croissance filament) | Phys. Rev. E 2025 (bmx suite) | TODO |
| 16 | AM fungi root growth (croissance depuis racine) | Schnepf & Roose 2006 Proc. R. Soc. B | TODO |

### Notes

v1.0 = moteur d'**analyse** (photo du réseau à un instant t)
v2.0 = moteur de **croissance** (le réseau pousse dans le temps)

Chaque brique v2.0 suit le même workflow:
1. Recherche internet (papiers)
2. Extraction des équations
3. Traduction code discret
4. Tests unitaires
5. Validation repos réels
6. Push git
