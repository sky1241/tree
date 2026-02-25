# HANDOFF — SESSION 25 FÉV 2026 (NUIT)

## CE QUI A ÉTÉ FAIT
- **forest.html** : proto UI/UX galerie forêt → detail arbre
  - Grille responsive 5 colonnes avec artwork par famille
  - Click → modal plein écran avec render du repo
  - Stats done/wip/todo, bouton GitHub, Navi qui vole
  - Tout en base64 inline (standalone HTML, ~2.6MB)
  - **PROBLÈME** : hardcodé avec les données de Sky, pas universel

## CE QUI RESTE À FAIRE — VISION PRODUIT

### Le vrai produit = outil universel pour vibe coders

**Flow utilisateur :**
1. User entre son GitHub username (ou URL)
2. Scan repos via GitHub API (public repos)
3. Classification auto → famille (engine.py Q1→Q6)
4. Grille forêt avec artwork FAMILLE (6 templates universels)
5. Click sur un arbre → scan COMPLET du repo
6. Nœuds placés sur le SKELETON de la famille
7. Overlay sur le `{family}_chatgpt_raw.png` du template
8. User voit SON arbre avec SES vrais fichiers

### Assets universels (déjà prêts) :
```
templates/{family}_chatgpt_raw.png    → artwork grille (6 familles)
templates/{family}_skeleton_sky.json  → positions nœuds (6 familles)
templates/{family}_final.png          → fond pour overlay
scripts/engine.py                     → classifieur Q1→Q6
```

### À construire :
1. **GitHub API scanner** — fetch repos + structure via API
   - `GET /users/{username}/repos` → liste
   - `GET /repos/{owner}/{repo}/git/trees/main?recursive=1` → arbre fichiers
   - Pas besoin de clone, juste l'API
   
2. **Classifieur léger** — version JS/browser du Q1→Q6
   - Ou: API endpoint Python qui classifie
   
3. **Renderer dynamique** — placer nœuds scan sur skeleton
   - Le mapping level→position existe déjà (testé cette session)
   - Canvas ou DOM overlay sur l'image famille

4. **UI entrée** — champ username + bouton scan
   - Loading state pendant le scan
   - Cache résultats (localStorage ou similar)

### Architecture possible :
- **Option A** : Full frontend (GitHub API côté client, classif en JS)
- **Option B** : Backend Python (Flask/FastAPI) + frontend
- **Option C** : GitHub Pages + GitHub Actions pour le scan

## COMMITS CETTE SESSION
- `33b7a1c` — 🌳 Classifieur Q1→Q6 — implémentation scientifique
- `e2b9716` — 🌲 Forêt v2 — galerie propre + detail render par repo

## FICHIERS CLÉS
- `forest.html` — proto UI (hardcodé, à remplacer)
- `proto_navi.html` — proto Navi original (single tree view)
- `scripts/engine.py` — classifieur complet (Python)
- `render_tree.py` — renderer overlay (Python, local)
- `templates/` — tous les assets visuels
- `scans/` — données de scan (format de référence)
