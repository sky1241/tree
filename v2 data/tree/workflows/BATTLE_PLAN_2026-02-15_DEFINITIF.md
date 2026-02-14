# DIMANCHE 15 FÉVRIER 2026 — PLAN D'ATTAQUE DÉFINITIF
# "On range l'atelier une bonne fois pour toutes"

Règle : tu fais CHAQUE étape dans l'ordre. Tu passes à la suivante SEULEMENT quand c'est fait.
Coche au fur et à mesure. Pas de réflexion. Tu exécutes.

---

## BLOC 1 — SSH (ne plus jamais taper de mot de passe) [15 min]

### PC 1 :
```bash
# 1. Ouvre un terminal. Tape ça :
ssh-keygen -t ed25519 -C "sky1241"
# → Tape ENTRÉE 3 fois (pas de passphrase, fichier par défaut)

# 2. Affiche ta clé publique :
cat ~/.ssh/id_ed25519.pub
# → Copie TOUT ce qui s'affiche (commence par ssh-ed25519...)

# 3. Va sur GitHub dans ton navigateur :
#    github.com → Settings → SSH and GPG keys → New SSH key
#    Title : "PC1"
#    Colle la clé → Add SSH key

# 4. Teste :
ssh -T git@github.com
# → Tu dois voir "Hi sky1241! You've been authenticated"
```

### PC 2 :
```bash
# Exactement la même chose, mais Title : "PC2"
ssh-keygen -t ed25519 -C "sky1241"
cat ~/.ssh/id_ed25519.pub
# → GitHub → Settings → SSH keys → New → Title "PC2" → Colle → Add
ssh -T git@github.com
```

### Sur LES DEUX PC — convertir tous les repos en SSH :
```bash
cd ~/3d-printer
git remote set-url origin git@github.com:sky1241/3d-printer.git

cd ~/HSBC-algo-genetic
git remote set-url origin git@github.com:sky1241/HSBC-algo-genetic.git

cd ~/infernal-wheel
git remote set-url origin git@github.com:sky1241/infernal-wheel.git

cd ~/shazam-piano
git remote set-url origin git@github.com:sky1241/shazam-piano.git

cd ~/fck-translation-
git remote set-url origin git@github.com:sky1241/fck-translation-.git
```

### Vérifie que ça marche :
```bash
cd ~/3d-printer && git push
# → Pas de mot de passe demandé = VICTOIRE
```

**FAIT ?** → Passe au bloc 2.

---

## BLOC 2 — Auto-push (backup automatique) [10 min]

### Sur LES DEUX PC, crée ce fichier :

**Windows (PowerShell) :**
```powershell
# Crée le fichier : ~/autopush.ps1
$repos = @(
    "$HOME\3d-printer",
    "$HOME\HSBC-algo-genetic",
    "$HOME\infernal-wheel",
    "$HOME\sky-toolkit"
)

foreach ($repo in $repos) {
    if (Test-Path $repo) {
        Set-Location $repo
        git add -A
        $date = Get-Date -Format "yyyy-MM-dd HH:mm"
        git commit -m "auto-save $date" 2>$null
        git push 2>$null
        Write-Host "OK $repo"
    }
}
```

**Linux/Mac (bash) :**
```bash
# Crée le fichier : ~/autopush.sh
#!/bin/bash
for repo in ~/3d-printer ~/HSBC-algo-genetic ~/infernal-wheel ~/sky-toolkit; do
    if [ -d "$repo" ]; then
        cd "$repo"
        git add -A
        git commit -m "auto-save $(date '+%Y-%m-%d %H:%M')" 2>/dev/null
        git push 2>/dev/null
        echo "OK $repo"
    fi
done
```

```bash
chmod +x ~/autopush.sh
```

### Utilisation :
```bash
# Quand tu veux sauvegarder TOUT d'un coup :
~/autopush.sh        # Linux/Mac
~/autopush.ps1       # Windows PowerShell
```

Tu peux aussi le mettre en tâche planifiée (cron Linux / Task Scheduler Windows)
pour qu'il tourne toutes les heures automatiquement. Mais pour l'instant, le lancer
à la main c'est suffisant.

**FAIT ?** → Passe au bloc 3.

---

## BLOC 3 — Créer sky-toolkit (ta boîte à outils) [30 min]

### 3.1 — Créer le repo sur GitHub
```
1. Va sur github.com/new
2. Nom : sky-toolkit
3. Description : "Outils centralisés — prompts, UX framework, workflows"
4. Public
5. Coche "Add a README file"
6. Create repository
```

### 3.2 — Clone sur les 2 PC
```bash
cd ~
git clone git@github.com:sky1241/sky-toolkit.git
cd sky-toolkit
```

### 3.3 — Créer la structure
```bash
mkdir -p prompts workflows ux-framework templates winter-trees
```

### 3.4 — Copier le framework UX depuis infernal-wheel
```bash
# Adapte les chemins selon où sont tes dossiers UX dans infernal-wheel :
cp -r ~/infernal-wheel/[tes-dossiers-ux]/* ~/sky-toolkit/ux-framework/

# Structure cible dans ux-framework/ :
#   apple-hig/
#   material3/
#   wcag/
#   nielsen/
#   baymard/
#   checklists/
#   anti-patterns/
#   device-compat/
#   components/
#   decision-trees/
```

### 3.5 — Créer le fichier workflow radar/sniper
```bash
cat > ~/sky-toolkit/workflows/radar-sniper.md << 'EOF'
# Workflow Radar / Sniper

## Principe
- Deep Research = RADAR (prompt large, récolte les noms, URLs, termes)
- Claude web search = SNIPER (un par un, extraire les données précises)

## Étape 1 — Radar (Deep Research)
Prompt type :
> "Liste-moi TOUS les papers, outils, libs, blogs, auteurs qui traitent de [SUJET].
> Je veux les NOMS et RÉFÉRENCES uniquement — pas de résumé, pas d'analyse.
> Format : une ligne par référence avec auteur, année, titre, URL si dispo."

## Étape 2 — Triage
Parmi les résultats, marquer :
- ★ = critique (données chiffrées attendues)
- ○ = utile (contexte)
- ✗ = poubelle

## Étape 3 — Sniper (Claude web search)
Pour chaque ★, donner à Claude :
> "Cherche [Auteur Année Titre exact]. Je veux :
> 1. [question précise 1]
> 2. [question précise 2]
> Pas de résumé. Juste les données."

## Règle d'or
- Radar = large, on accepte le bruit
- Sniper = chirurgical, une cible à la fois
- JAMAIS les deux dans le même prompt
EOF
```

### 3.6 — Push
```bash
cd ~/sky-toolkit
git add -A
git commit -m "feat: initial toolkit — workflows + UX framework"
git push
```

### 3.7 — Pull sur le 2ème PC
```bash
cd ~/sky-toolkit && git pull
```

**FAIT ?** → Passe au bloc 4.

---

## BLOC 4 — Sauver le Winter Tree (ta carte de code) [15 min]

L'arbre hiver c'est ton outil pour cartographier un repo en 1 page.
Il vient du 3d-printer. Tu le mets dans sky-toolkit pour le réutiliser partout.

### 4.1 — Copier le template
```bash
cat > ~/sky-toolkit/winter-trees/TEMPLATE.md << 'EOF'
# 🌲 [NOM DU PROJET] — ARBRE HIVER

## (1) TREE_SILHOUETTE
```
Dessiner l'arbre de BAS (racines = contraintes fondamentales)
vers le HAUT (cime = tests, packaging, docs).

Tronc = le fichier/module principal.
Branches = les modules secondaires.
Racines = les contraintes non-négociables.
```

## (2) NODE_REGISTRY
```yaml
- id: R1
  label: "Nom de la contrainte"
  level: R          # R=racine, T=tronc, B=branche, C=cime
  parent: null
  desc: "Description en 1 ligne"
```

## (3) REFERENCES
Chaque nœud peut avoir max 6 références :
- (code) fichier.py: fonction() — L123 — description
- (doc) README.md — description

## (4) QUICK SUMMARY
```
Ce projet est surtout un ─── [1 phrase]
Le tronc est ─────────── [fichier principal + ce qu'il fait]
Les branches dominantes ─ [les 2-3 plus importants]
La contrainte racine la plus forte est ─ [la contrainte #1]
Le risque structurel principal est ─── [le danger #1]
```
EOF
```

### 4.2 — Copier l'arbre hiver du 3d-printer comme exemple
```bash
cp ~/3d-printer/WINTER_TREE_TESTS.md ~/sky-toolkit/winter-trees/3d-printer.md
```

### 4.3 — Push
```bash
cd ~/sky-toolkit && git add -A && git commit -m "feat: winter tree template + 3d-printer example" && git push
```

**FAIT ?** → Passe au bloc 5.

---

## BLOC 5 — Sauver les prompts qui marchent [15 min]

### 5.1 — Le prompt MICR chirurgical (celui d'aujourd'hui)
```bash
cp ~/[là-où-tu-l'as]/MICR_DEEP_RESEARCH_v2_SURGICAL.md ~/sky-toolkit/prompts/
```

### 5.2 — Créer le template de prompt code-audit
```bash
cat > ~/sky-toolkit/prompts/code-audit-template.md << 'EOF'
# Prompt d'audit de code

## Utilisation
Coller ce prompt à Claude avec le code source ou le nom du repo.

## Prompt
> Audite ce code. Pour CHAQUE problème trouvé :
> 1. Ligne exacte
> 2. Sévérité (CRITIQUE / MOYEN / FAIBLE)
> 3. Fix proposé (code, pas de blabla)
>
> Je ne veux pas :
> - "Le code est bien structuré" → je m'en fous
> - "Vous pourriez considérer" → dis-moi quoi faire
>
> Je veux :
> - L1234: BUG — variable non initialisée → fix: ajouter `x = 0`
> - L5678: PERF — boucle O(n²) → fix: utiliser dict lookup
EOF
```

### 5.3 — Push
```bash
cd ~/sky-toolkit && git add -A && git commit -m "feat: prompts — MICR + code-audit template" && git push
```

**FAIT ?** → Passe au bloc 6.

---

## BLOC 6 — Intégrer MICR dans 3d-printer [30 min]

### 6.1 — Copier micr.py
```bash
cp ~/[là-où-tu-l'as]/micr.py ~/3d-printer/micr.py
```

### 6.2 — Tester que micr.py tourne seul
```bash
cd ~/3d-printer
python3 micr.py
# Doit afficher "MICR self-test complete" sans erreur
```

### 6.3 — Push
```bash
cd ~/3d-printer
git add micr.py
git commit -m "feat: MICR — Moteur Inverse de Contraintes Réelles"
git push
```

### 6.4 — L'intégration dans generate() = PAS AUJOURD'HUI
Aujourd'hui c'est RANGEMENT. L'intégration dans le pipeline c'est lundi.
Tu poses la brique, tu la soudes pas encore.

**FAIT ?** → Passe au bloc 7.

---

## BLOC 7 — Vérification finale [10 min]

### Sur les 2 PC, dans un terminal :
```bash
echo "=== VÉRIFICATION ==="

echo "--- sky-toolkit ---"
cd ~/sky-toolkit && git pull && ls -la

echo "--- 3d-printer ---"
cd ~/3d-printer && git pull && git log --oneline -3

echo "--- HSBC ---"
cd ~/HSBC-algo-genetic && git pull && git log --oneline -3

echo "--- infernal-wheel ---"
cd ~/infernal-wheel && git pull && git log --oneline -3

echo "--- SSH test ---"
ssh -T git@github.com

echo "--- autopush test ---"
~/autopush.sh   # ou autopush.ps1 sur Windows
```

### Checklist finale :
```
[ ] SSH fonctionne sur PC1 (pas de mot de passe)
[ ] SSH fonctionne sur PC2 (pas de mot de passe)
[ ] autopush.sh/ps1 existe sur les 2 PC
[ ] sky-toolkit cloné sur les 2 PC
[ ] sky-toolkit contient : prompts/ workflows/ ux-framework/ winter-trees/
[ ] micr.py dans 3d-printer (self-test OK)
[ ] git pull = même état sur les 2 PC
[ ] TOUS les repos en SSH (pas HTTPS)
```

---

## STRUCTURE FINALE DE SKY-TOOLKIT

```
sky-toolkit/
├── README.md
├── prompts/
│   ├── MICR_DEEP_RESEARCH_v2_SURGICAL.md
│   ├── code-audit-template.md
│   └── (futurs prompts qui marchent)
├── workflows/
│   ├── radar-sniper.md
│   └── (futurs process)
├── ux-framework/
│   ├── apple-hig/
│   ├── material3/
│   ├── wcag/
│   ├── nielsen/
│   ├── baymard/
│   ├── checklists/
│   ├── anti-patterns/
│   ├── device-compat/
│   ├── components/
│   └── decision-trees/
├── winter-trees/
│   ├── TEMPLATE.md
│   └── 3d-printer.md
└── templates/
    └── (futurs templates réutilisables)
```

---

## RÉSUMÉ EN 7 BLOCS

| # | Quoi | Temps | Résultat |
|---|------|-------|----------|
| 1 | SSH keys 2 PC | 15 min | Plus jamais de mot de passe |
| 2 | autopush.sh | 10 min | Backup en 1 commande |
| 3 | sky-toolkit repo | 30 min | Boîte à outils centralisée |
| 4 | Winter Tree template | 15 min | Carte de code réutilisable |
| 5 | Prompts sauvegardés | 15 min | Munitions sniper stockées |
| 6 | MICR dans 3d-printer | 30 min | Brique posée (pas soudée) |
| 7 | Vérification 2 PC | 10 min | Tout synchro partout |

**TOTAL : ~2h.** Le reste de la journée tu fais ce que tu veux.

---

## MOT D'ORDRE

Demain tu ouvres ce fichier. Tu fais bloc 1. Puis bloc 2. Puis 3.
Tu réfléchis pas. Tu tapes les commandes. Tu coches.
À la fin t'as un atelier propre et des outils affûtés.

Après ça, chaque fois que tu polis un outil → `sky-toolkit`.
Chaque fois que tu changes de PC → `git pull`.
Chaque fois que tu finis une session → `autopush.sh`.

C'est fini le bordel.
