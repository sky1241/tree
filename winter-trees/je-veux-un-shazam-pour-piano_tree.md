# WINTER TREE — je veux un Shazam pour piano

- Famille : 🌴 Palmier
- Domaine : audio
- Date plantation : 2026-02-14T15:12:52.575434
- Phase : GRAINE

## ARBRE

### [-5] mycorhizes — Lois physiques / math / hardware

```yaml
- id: M1
  label: "FFT (transformée de Fourier rapide)"
  status: todo
  entry: ~
  depends: []
```

```yaml
- id: M2
  label: "Fréquences harmoniques & physique du son"
  status: todo
  entry: ~
  depends: []
```

```yaml
- id: M3
  label: "Latence audio hardware (~10ms incompressible)"
  status: todo
  entry: ~
  depends: []
```

### [-4] poils_absorbants — Contraintes légales

```yaml
- id: P1
  label: "Permission microphone (iOS/Android)"
  status: todo
  entry: ~
  depends: []
```

```yaml
- id: P2
  label: "Licences audio (si samples)"
  status: todo
  entry: ~
  depends: []
```

```yaml
- id: P3
  label: "Privacy policy (enregistrement audio)"
  status: todo
  entry: ~
  depends: []
```

### [-3] radicelles — Contraintes business

```yaml
- id: D1
  label: "Public cible (musiciens débutants/pro)"
  status: todo
  entry: ~
  depends: []
```

```yaml
- id: D2
  label: "App Store / Play Store rules"
  status: todo
  entry: ~
  depends: []
```

```yaml
- id: D3
  label: "Modèle gratuit/premium"
  status: todo
  entry: ~
  depends: []
```

### [-2] pivotantes — Décisions d'architecture

```yaml
- id: A1
  label: "Architecture audio pipeline (capture→FFT→matching→display)"
  status: todo
  entry: ~
  depends: []
```

```yaml
- id: A2
  label: "Choix : traitement on-device vs cloud"
  status: todo
  entry: ~
  depends: []
```

### [-1] structurelles — Stack technique

```yaml
- id: R1
  label: "Framework mobile (Flutter/React Native/Swift)"
  status: todo
  entry: ~
  depends: []
```

```yaml
- id: R2
  label: "Lib audio (AudioKit, TarsosDSP, flutter_audio)"
  status: todo
  entry: ~
  depends: []
```

```yaml
- id: R3
  label: "Lib FFT (fftea, dart:typed_data)"
  status: todo
  entry: ~
  depends: []
```

### [+1] tronc — Core engine / pipeline

```yaml
- id: T1
  label: "Pipeline : capture micro → buffer → FFT → détection fréquence → matching note → affichage"
  status: todo
  entry: ~
  depends: []
```

### [+2] branches — Modules majeurs

```yaml
- id: B1
  label: "Module capture micro"
  status: todo
  entry: ~
  depends: []
```

```yaml
- id: B2
  label: "Module analyse FFT"
  status: todo
  entry: ~
  depends: []
```

```yaml
- id: B3
  label: "Module matching note/accord"
  status: todo
  entry: ~
  depends: []
```

```yaml
- id: B4
  label: "Module affichage résultat"
  status: todo
  entry: ~
  depends: []
```

### [+3] rameaux — Sous-features

```yaml
- id: b1
  label: "Bouton record/stop"
  status: todo
  entry: ~
  depends: []
```

```yaml
- id: b2
  label: "Visualisation fréquences"
  status: todo
  entry: ~
  depends: []
```

```yaml
- id: b3
  label: "Historique des détections"
  status: todo
  entry: ~
  depends: []
```

```yaml
- id: b4
  label: "Réglages sensibilité"
  status: todo
  entry: ~
  depends: []
```

```yaml
- id: b5
  label: "Accordeur (tuner mode)"
  status: todo
  entry: ~
  depends: []
```

### [+4] feuilles — Outputs / UI

```yaml
- id: F1
  label: "Écran principal (note détectée)"
  status: todo
  entry: ~
  depends: []
```

```yaml
- id: F2
  label: "Écran historique"
  status: todo
  entry: ~
  depends: []
```

```yaml
- id: F3
  label: "Écran settings"
  status: todo
  entry: ~
  depends: []
```

```yaml
- id: F4
  label: "Feedback visuel temps réel"
  status: todo
  entry: ~
  depends: []
```

### [+5] cime — Tests / déploiement

```yaml
- id: C1
  label: "Tests unitaires matching"
  status: todo
  entry: ~
  depends: []
```

```yaml
- id: C2
  label: "Test micro simulé"
  status: todo
  entry: ~
  depends: []
```

```yaml
- id: C3
  label: "CI/CD build APK/IPA"
  status: todo
  entry: ~
  depends: []
```

```yaml
- id: C4
  label: "Publication store"
  status: todo
  entry: ~
  depends: []
```

## ORDRE DE CONSTRUCTION

- ⬜ **Phase 0** : Mycorhizes — lois physiques
  - Action : Identifier les lois physiques/math immuables du projet
  - Nœuds : M1, M2, M3

- ⬜ **Phase 1** : Poils — contraintes légales
  - Action : Définir les contraintes de niveau -4
  - Nœuds : P1, P2, P3

- ⬜ **Phase 1** : Radicelles — business
  - Action : Définir les contraintes de niveau -3
  - Nœuds : D1, D2, D3

- ⬜ **Phase 1** : Pivot — architecture
  - Action : Définir les contraintes de niveau -2
  - Nœuds : A1, A2

- ⬜ **Phase 1** : Structurelles — stack technique
  - Action : Définir les contraintes de niveau -1
  - Nœuds : R1, R2, R3

- ⬜ **Phase 2** : Tronc — LE chemin unique
  - Action : Construire LE pipeline unique — le protéger à tout prix
  - Nœuds : T1

- ⬜ **Phase 3** : Feuilles — output riche
  - Action : Output riche au sommet du pipeline unique
  - Nœuds : F1, F2, F3, F4

- ⬜ **Phase 4** : Rameaux — sous-features
  - Action : Implémenter rameaux — sous-features
  - Nœuds : b1, b2, b3, b4, b5

- ⬜ **Phase 4** : Feuilles — UI/outputs
  - Action : Implémenter feuilles — ui/outputs
  - Nœuds : F1, F2, F3, F4

- ⬜ **Phase 5** : Cime — tests et déploiement
  - Action : Implémenter cime — tests et déploiement
  - Nœuds : C1, C2, C3, C4

## PROCHAIN PAS

> Identifier les lois physiques/math immuables du projet