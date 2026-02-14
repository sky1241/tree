# WINTER TREE — [scanned] shazam-piano

- Famille : 🌲 Conifère
- Domaine : audio
- Date plantation : 2026-02-14T15:27:38.537244
- Phase : CROISSANCE

## ARBRE

### [-5] mycorhizes — Lois physiques / math / hardware

```yaml
- id: M1
  label: "Langage principal : Dart (2030 lignes)"
  status: done
  entry: ~
  depends: []
```

### [-4] poils_absorbants — Contraintes légales

```yaml
- id: P1
  label: "Licence projet"
  status: done
  entry: LICENSE
  depends: []
```

### [-3] radicelles — Contraintes business

_Aucun nœud — à remplir_

### [-2] pivotantes — Décisions d'architecture

_Aucun nœud — à remplir_

### [-1] structurelles — Stack technique

```yaml
- id: R1
  label: "Flutter/Dart"
  status: done
  entry: pubspec.yaml
  depends: []
```

### [+1] tronc — Core engine / pipeline

```yaml
- id: T1
  label: "Core : lib/main.dart (800 lignes, Dart)"
  status: done
  entry: lib/main.dart
  depends: []
```

### [+2] branches — Modules majeurs

```yaml
- id: B1
  label: "lib/ (7 fichiers, 1980L, Dart)"
  status: done
  entry: lib/
  depends: []
```

```yaml
- id: B2
  label: "test/ (1 fichiers, 50L, Dart)"
  status: done
  entry: test/
  depends: []
```

### [+3] rameaux — Sous-features

```yaml
- id: b1
  label: "lib/services/ (2f, 600L)"
  status: done
  entry: lib/services/
  depends: []
```

```yaml
- id: b2
  label: "lib/screens/ (2f, 350L)"
  status: done
  entry: lib/screens/
  depends: []
```

```yaml
- id: b3
  label: "lib/models/ (1f, 150L)"
  status: done
  entry: lib/models/
  depends: []
```

```yaml
- id: b4
  label: "lib/widgets/ (1f, 80L)"
  status: done
  entry: lib/widgets/
  depends: []
```

### [+4] feuilles — Outputs / UI

```yaml
- id: F1
  label: "README — ABSENT"
  status: todo
  entry: ~
  depends: []
```

### [+5] cime — Tests / déploiement

```yaml
- id: C1
  label: "Tests (dossier test/)"
  status: done
  entry: test/
  depends: []
```

```yaml
- id: C2
  label: "GitHub Actions CI"
  status: done
  entry: .github/workflows/
  depends: []
```

## ORDRE DE CONSTRUCTION

- ⬜ **Phase 0** : Mycorhizes — lois physiques
  - Action : Identifier les lois physiques/math immuables du projet
  - Nœuds : M1

- ⬜ **Phase 1** : Poils — contraintes légales
  - Action : Définir les contraintes de niveau -4
  - Nœuds : P1

- ⬜ **Phase 1** : Structurelles — stack technique
  - Action : Définir les contraintes de niveau -1
  - Nœuds : R1

- ⬜ **Phase 2** : Tronc — pipeline principal
  - Action : Construire le pipeline end-to-end minimal
  - Nœuds : T1

- ⬜ **Phase 3** : Branches — modules subordonnés
  - Action : Ajouter les modules UN PAR UN, toujours subordonnés au tronc
  - Nœuds : B1, B2

- ⬜ **Phase 4** : Rameaux — sous-features
  - Action : Implémenter rameaux — sous-features
  - Nœuds : b1, b2, b3, b4

- ⬜ **Phase 4** : Feuilles — UI/outputs
  - Action : Implémenter feuilles — ui/outputs
  - Nœuds : F1

- ⬜ **Phase 5** : Cime — tests et déploiement
  - Action : Implémenter cime — tests et déploiement
  - Nœuds : C1, C2

## PROCHAIN PAS

> Vérifier l'arbre scanné et compléter les nœuds manquants