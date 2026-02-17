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
| **TOTAL v1.0** | | **120** | |

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
| **TOTAL v2.0** | | **205** | | |

### Compteur total: 325 tests (120 v1.0 + 205 v2.0), 6048 lignes

## 🔨 CHANTIER 2 — Audit ordre biologique

### Problème
Les briques ont été codées dans l'ordre de développement (13→14→15→16→17→18→19→20),
pas dans l'ordre du cycle de vie réel du champignon. Le pipeline am_fungi_simulate()
appelle les phases dans un ordre technique, pas biologique.

### Ordre biologique réel (cycle de vie AM fungi)

```
PHASE 0: SETUP
  [18] L-System root → la racine existe dans le sol
  [17] Germination spore → spore détecte strigolactone, germe, tube germinatif

PHASE 1: COLONISATION
  [16] Root emission → hyphes émis depuis l'interface racine-champignon
  [13] Edelstein growth → branching, death, densité du réseau

PHASE 2: MATURATION
  [15] 3D mechanics → orientation, Spitzenkörper, Lockhart elongation
  [14] Oscillatory signaling → tips se cherchent via FHN
  [11] Anastomose → fusion des hyphes synchronisés (14→11)

PHASE 3: FONCTION
  [19] P uptake → le réseau mature absorbe le phosphore du sol
  [20] C↔P exchange → la plante paie en carbone, reçoit du phosphore

PHASE 4: ANALYSE (v1.0)
  [0-10] Métriques → meshedness, efficacité, Physarum, robustesse, etc.
```

### TODO audit
- [ ] Vérifier que chaque brique reçoit les bonnes données d'entrée de la brique précédente
- [ ] Vérifier que le format de sortie de chaque brique est compatible avec l'entrée de la suivante
- [ ] Créer un pipeline full_lifecycle_simulate() qui enchaîne tout dans l'ordre biologique
- [ ] Identifier les "joints" manquants entre briques
- [ ] Test d'intégration end-to-end : spore → réseau mature → P delivery

## Notes

v1.0 = moteur d'**analyse** (photo du réseau à un instant t)
v2.0 = moteur de **croissance** (le réseau pousse dans le temps)

Pipeline actuel am_fungi_simulate() (ordre technique):
- Phase 1: Root emission (brique 16 — Schnepf boundary)
- Phase 2: Edelstein growth/death (brique 13)
- Phase 3: 3D mechanics (brique 15 — Lockhart/VSC/Spitzenkörper)
- Phase 4: Oscillatory signaling (brique 14 — FHN coupling)
- Phase 5: Fusion completion (brique 14 → 11 — anastomose)

Chaque brique v2.0 suit le même workflow:
1. Recherche internet (papiers)
2. Extraction des équations
3. Traduction code discret
4. Tests unitaires
5. Push git
