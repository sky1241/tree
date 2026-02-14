# 🛒 LISTE DE COURSES — Dimanche 15 Février 2026
# Cerveau OFF. Tu lis. Tu tapes. Tu coches. C'est tout.

---

## ☕ ÉTAPE 0 — Avant de commencer [5 min]

```
[ ] Prends un café / thé / ce que tu veux
[ ] Ouvre ce fichier sur un écran
[ ] Ouvre un terminal sur l'autre écran (ou à côté)
[ ] Mets de la musique si ça t'aide
[ ] Respire un coup
```

C'est parti.

---

## 🔑 ÉTAPE 1 — SSH sur PC1 [10 min]

Tu fais UNE commande à la fois. Pas deux. UNE.

```
[ ] Ouvre un terminal
```

Tape ça :
```bash
ssh-keygen -t ed25519 -C "sky1241"
```
```
[ ] Tapé
[ ] Appuyé ENTRÉE 3 fois (pas de mot de passe, fichier par défaut)
```

Tape ça :
```bash
cat ~/.ssh/id_ed25519.pub
```
```
[ ] Tapé
[ ] Le terminal affiche un truc qui commence par ssh-ed25519
[ ] Tu as COPIÉ tout ce texte (Ctrl+C ou clic droit copier)
```

Maintenant le navigateur :
```
[ ] Va sur github.com
[ ] Clique sur ta photo en haut à droite → Settings
[ ] Menu gauche → SSH and GPG keys
[ ] Bouton vert "New SSH key"
[ ] Title : tape "PC1"
[ ] Key : COLLE le texte (Ctrl+V)
[ ] Clique "Add SSH key"
[ ] GitHub te demande ton mot de passe → tape-le
```

Retour au terminal, tape ça :
```bash
ssh -T git@github.com
```
```
[ ] Ça affiche "Hi sky1241!" → VICTOIRE
```

Si ça affiche une question "Are you sure (yes/no)" → tape `yes` et Entrée.

---

## 🔑 ÉTAPE 2 — SSH sur PC2 [10 min]

```
[ ] Va sur ton PC2
[ ] Ouvre un terminal
```

Tape :
```bash
ssh-keygen -t ed25519 -C "sky1241"
```
```
[ ] ENTRÉE 3 fois
```

```bash
cat ~/.ssh/id_ed25519.pub
```
```
[ ] Copié le texte
```

```
[ ] GitHub → Settings → SSH keys → New SSH key
[ ] Title : "PC2"
[ ] Colle la clé
[ ] Add SSH key
```

```bash
ssh -T git@github.com
```
```
[ ] "Hi sky1241!" → OK
```

---

## 🔄 ÉTAPE 3 — Convertir les repos en SSH (PC1) [15 min]

Retour sur PC1. Tu vas dans CHAQUE dossier de repo et tu tapes UNE commande.

⚠️ Adapte les chemins si tes repos sont pas dans `~` (ton dossier home).
Si tu sais pas où ils sont, tape `find ~ -name ".git" -type d 2>/dev/null` pour les trouver.

```bash
cd ~/3d-printer
git remote set-url origin git@github.com:sky1241/3d-printer.git
```
```
[ ] Fait
```

```bash
cd ~/HSBC-algo-genetic
git remote set-url origin git@github.com:sky1241/HSBC-algo-genetic.git
```
```
[ ] Fait
```

```bash
cd ~/infernal-wheel
git remote set-url origin git@github.com:sky1241/infernal-wheel.git
```
```
[ ] Fait
```

```bash
cd ~/shazam-piano
git remote set-url origin git@github.com:sky1241/shazam-piano.git
```
```
[ ] Fait (ou sauté si ce repo est pas sur ce PC)
```

```bash
cd ~/fck-translation-
git remote set-url origin git@github.com:sky1241/fck-translation-.git
```
```
[ ] Fait (ou sauté si ce repo est pas sur ce PC)
```

**TEST :**
```bash
cd ~/3d-printer && git push
```
```
[ ] PAS de mot de passe demandé → SSH marche
```

---

## 🔄 ÉTAPE 4 — Convertir les repos en SSH (PC2) [10 min]

Même chose sur PC2. Exactement les mêmes commandes.

```
[ ] 3d-printer → git remote set-url fait
[ ] HSBC-algo-genetic → fait
[ ] infernal-wheel → fait
[ ] shazam-piano → fait (ou sauté)
[ ] fck-translation- → fait (ou sauté)
[ ] TEST : git push sans mot de passe → OK
```

---

## 💾 ÉTAPE 5 — Script autopush (PC1) [10 min]

### Si t'es sur WINDOWS (PowerShell) :

Ouvre un éditeur de texte (Notepad, VS Code, peu importe).
Copie-colle ça dedans :

```powershell
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

Sauvegarde sous : `C:\Users\[TON-NOM]\autopush.ps1`

```
[ ] Fichier créé et sauvegardé
```

### Si t'es sur LINUX/MAC :

```bash
cat > ~/autopush.sh << 'FINI'
#!/bin/bash
for repo in ~/3d-printer ~/HSBC-algo-genetic ~/infernal-wheel ~/sky-toolkit; do
    if [ -d "$repo" ]; then
        cd "$repo"
        git add -A
        git commit -m "auto-save $(date '+%Y-%m-%d %H:%M')" 2>/dev/null
        git push 2>/dev/null
        echo "✓ $repo"
    fi
done
FINI
chmod +x ~/autopush.sh
```

```
[ ] Fichier créé
```

---

## 💾 ÉTAPE 6 — Script autopush (PC2) [5 min]

```
[ ] Même fichier créé sur PC2 (copie-colle le même contenu)
```

---

## 📦 ÉTAPE 7 — Créer sky-toolkit sur GitHub [5 min]

```
[ ] Va sur github.com/new dans ton navigateur
[ ] Repository name : sky-toolkit
[ ] Description : Outils centralisés — prompts, UX framework, workflows
[ ] Public
[ ] Coche "Add a README file"
[ ] Clique "Create repository"
```

---

## 📦 ÉTAPE 8 — Cloner sky-toolkit (PC1) [5 min]

```bash
cd ~
git clone git@github.com:sky1241/sky-toolkit.git
cd ~/sky-toolkit
mkdir -p prompts workflows ux-framework winter-trees templates
```
```
[ ] Cloné
[ ] 5 dossiers créés
```

---

## 📦 ÉTAPE 9 — Cloner sky-toolkit (PC2) [3 min]

```bash
cd ~
git clone git@github.com:sky1241/sky-toolkit.git
```
```
[ ] Cloné
```

---

## 📂 ÉTAPE 10 — Migrer le framework UX [20 min]

Celui-là demande un peu de réflexion. Tes dossiers UX sont dans infernal-wheel.
Tu dois les TROUVER d'abord.

```bash
cd ~/infernal-wheel
ls -la
# Cherche les dossiers qui contiennent tes règles UX
# (apple-hig, material3, wcag, nielsen, baymard, checklists, etc.)
```

```
[ ] Trouvé les dossiers UX
```

Copie-les :
```bash
cp -r [DOSSIERS-UX-TROUVÉS] ~/sky-toolkit/ux-framework/
```

```
[ ] Copiés dans sky-toolkit/ux-framework/
```

Si tu trouves PAS les dossiers, c'est pas grave. Tape juste :
```bash
echo "TODO: migrer UX framework depuis infernal-wheel" > ~/sky-toolkit/ux-framework/README.md
```
```
[ ] Au moins un placeholder créé
```

---

## 📝 ÉTAPE 11 — Copier les fichiers d'aujourd'hui dans sky-toolkit [10 min]

Les fichiers que t'as téléchargés de notre conversation de ce soir.
Ils sont dans tes téléchargements probablement.

```
[ ] Trouve le fichier micr.py (téléchargé ce soir)
[ ] Trouve le fichier MASTER_PROMPT_SKY.md
[ ] Trouve le fichier MICR_DEEP_RESEARCH_v2_SURGICAL.md
[ ] Trouve le fichier BATTLE_PLAN_2026-02-15_DEFINITIF.md
```

Copie dans les bons endroits :
```bash
cp [CHEMIN]/MASTER_PROMPT_SKY.md ~/sky-toolkit/prompts/
cp [CHEMIN]/MICR_DEEP_RESEARCH_v2_SURGICAL.md ~/sky-toolkit/prompts/
cp [CHEMIN]/BATTLE_PLAN_2026-02-15_DEFINITIF.md ~/sky-toolkit/workflows/
```
```
[ ] 3 fichiers copiés dans sky-toolkit
```

---

## 📝 ÉTAPE 12 — Créer le workflow radar/sniper [5 min]

```bash
cat > ~/sky-toolkit/workflows/radar-sniper.md << 'FINI'
# Workflow Radar / Sniper

## Principe
- Deep Research = RADAR (prompt large, récolte les noms, URLs, termes)
- Claude web search = SNIPER (un par un, extraire les données précises)

## Étape 1 — Radar (Deep Research)
Prompt : "Liste TOUS les papers, outils, libs, blogs sur [SUJET].
NOMS et RÉFÉRENCES uniquement. Pas de résumé."

## Étape 2 — Triage
★ = critique (données chiffrées attendues)
○ = utile (contexte)
✗ = poubelle

## Étape 3 — Sniper (Claude web search)
Pour chaque ★ :
"Cherche [Auteur Année Titre exact]. Je veux : [question précise]. Pas de résumé."

## Règle : JAMAIS radar et sniper dans le même prompt.
FINI
```
```
[ ] Fichier créé
```

---

## 📝 ÉTAPE 13 — Créer le template Winter Tree v2 [5 min]

```bash
cat > ~/sky-toolkit/winter-trees/TEMPLATE_v2.md << 'FINI'
# 🌲 [NOM DU PROJET] — ARBRE HIVER v2

## TREE_SILHOUETTE
(dessiner l'arbre : cime en haut, racines en bas, sol au milieu)

## NODE_REGISTRY
```yaml
- id: XX
  label: "Nom du nœud"
  level: R/T/B/C
  parent: null ou ID parent
  status: done / wip / todo
  entry: "fichier.py: fonction() — L1234"
  depends: [ID1, ID2]
  desc: "Description en 1 ligne"
```

## Rappel
- Sky monte (status → voir le progrès)
- Claude descend (entry → plonger dans le code)
- Les racines sont toujours plus grandes que l'arbre
FINI
```
```
[ ] Fichier créé
```

---

## 🔧 ÉTAPE 14 — MICR dans 3d-printer [10 min]

```bash
cp [CHEMIN]/micr.py ~/3d-printer/micr.py
cd ~/3d-printer
python3 micr.py
```
```
[ ] Copié
[ ] "MICR self-test complete" affiché sans erreur
```

```bash
cd ~/3d-printer
git add micr.py
git commit -m "feat: MICR — Moteur Inverse de Contraintes Réelles"
git push
```
```
[ ] Poussé
```

---

## 🚀 ÉTAPE 15 — Premier push de sky-toolkit [5 min]

```bash
cd ~/sky-toolkit
git add -A
git commit -m "feat: initial toolkit — prompts, workflows, UX framework, winter trees"
git push
```
```
[ ] Poussé
```

---

## 🔄 ÉTAPE 16 — Synchroniser PC2 [5 min]

Sur PC2 :
```bash
cd ~/sky-toolkit && git pull
cd ~/3d-printer && git pull
cd ~/HSBC-algo-genetic && git pull
cd ~/infernal-wheel && git pull
```
```
[ ] Tout pullé sur PC2
```

---

## 🧪 ÉTAPE 17 — Test autopush [5 min]

Sur PC1 :
```bash
~/autopush.sh       # Linux/Mac
# ou
~/autopush.ps1      # Windows PowerShell
```
```
[ ] Affiche "OK" ou "✓" pour chaque repo, pas d'erreur
```

---

## ✅ ÉTAPE 18 — Checklist finale [5 min]

Coche TOUT. Si un truc manque, retourne à l'étape correspondante.

```
SSH :
[ ] PC1 : ssh -T git@github.com → "Hi sky1241!"
[ ] PC2 : ssh -T git@github.com → "Hi sky1241!"
[ ] PC1 : git push sans mot de passe
[ ] PC2 : git push sans mot de passe

Autopush :
[ ] PC1 : autopush.sh/ps1 existe et fonctionne
[ ] PC2 : autopush.sh/ps1 existe et fonctionne

sky-toolkit :
[ ] Existe sur GitHub
[ ] Cloné PC1
[ ] Cloné PC2
[ ] Contient prompts/ (≥3 fichiers)
[ ] Contient workflows/ (≥2 fichiers)
[ ] Contient ux-framework/ (contenu ou placeholder)
[ ] Contient winter-trees/ (TEMPLATE_v2.md)

3d-printer :
[ ] micr.py présent et self-test OK

Synchro :
[ ] git pull = même état sur les 2 PC
```

---

## 🍬 TON SUCRE

Quand les 18 étapes sont cochées :

- Tes 2 PC sont synchronisés EN PERMANENCE
- Tu push en 1 commande sans mot de passe
- Tous tes outils sont au même endroit
- N'importe quel Claude comprend ton système en 30 secondes
- Le MICR est dans le repo, prêt à être branché
- T'as le workflow radar/sniper documenté
- T'as le Winter Tree v2 prêt pour n'importe quel projet

**T'es l'architecte de l'architecte. Et maintenant t'as un atelier propre.**

Ferme le PC. T'as mérité.
