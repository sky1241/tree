# PROMPT MAÎTRE — À donner à n'importe quel Claude
# "L'Architecte de l'Architecte"

---

## QUI JE SUIS

Je m'appelle Sky. Je code pas vraiment — j'orchestre des IA pour construire des systèmes complexes. Je suis l'architecte de l'architecte : je construis les outils qui me permettent de construire plus vite. Mon cerveau fonctionne en parallèle (TDAH), je gère 3-5 projets simultanément, et je perds plus de temps à chercher mes outils qu'à les utiliser. Aujourd'hui ça s'arrête.

## CE QUE JE FAIS AUJOURD'HUI

Je range mon atelier. Je crée un système où :
- Mes outils sont rangés au même endroit (sky-toolkit sur GitHub)
- Mes 2 PC sont synchronisés en permanence (SSH + autopush)
- N'importe quel Claude peut comprendre où j'en suis en 30 secondes (Winter Tree)
- Je perds plus jamais 20 minutes à chercher un prompt, un workflow, ou un framework

Ce n'est pas du code. C'est de l'infrastructure. C'est l'usine qui construit les usines.

---

## LE MODÈLE MENTAL — L'ARBRE D'HIVER (Winter Tree)

### Le principe

Imagine un arbre en hiver. Pas de feuilles. Juste la structure.

```
          ☆  Cime (tests, packaging, docs)
         /|\
        / | \  Branches (modules, features)
       /  |  \
      /   |   \
─────/────|────\───── ← LE SOL = l'interface Sky ↔ Claude
     \    |    /
      \   |   /
       \  |  /  Racines (code interne, maths, physique)
        \ | /
         \|/
          ▼  Racines profondes (contraintes fondamentales)
```

### Les deux directions

**Sky monte.** Il regarde l'arbre au-dessus du sol. Il voit les branches (features), leur taille (avancement), ce qui manque. C'est sa carte de progression. Il veut savoir : "où j'en suis ? qu'est-ce qui pousse ? qu'est-ce qui est mort ?"

**Claude descend.** Il regarde les racines sous le sol. Il voit le code, les fonctions, les lignes, les dépendances. C'est sa porte d'entrée. Il veut savoir : "où je plonge ? quel fichier ? quelle ligne ?"

### La règle fondamentale

**Les racines sont TOUJOURS plus grandes que l'arbre visible.**

20 000 lignes de code (racines) → une tortue qui hoche la tête (arbre visible).
C'est pour ça que Sky a l'impression que "rien avance" — il creuse des racines toute la journée et l'arbre grandit de 2 cm. Mais sans racines, l'arbre tombe.

### Le sol = la collaboration

Le sol c'est là où Sky et Claude se parlent. C'est l'interface. Sky pose un problème (du sol vers le haut : "je veux que la tortue bouge"). Claude plonge dans les racines (du sol vers le bas : "il faut modifier L8871 dans automata_unified_v4.py").

Le Winter Tree DOIT montrer les deux côtés.

---

## FORMAT DU WINTER TREE v2

Chaque nœud a maintenant :

```yaml
- id: B5
  label: "AI Parsing"
  level: B                    # R=racine, T=tronc, B=branche, C=cime
  parent: T2
  status: wip                 # done / wip / todo  ← POUR SKY (monter)
  entry: "automata_unified_v4.py: parse_text_to_figurine_config() L8255"  ← POUR CLAUDE (descendre)
  depends: [T2, T5]           # dépendances ← POUR LES DEUX
  desc: "Convertir texte libre en FigurineConfig"
```

- `status` = Sky ouvre l'arbre, voit vert/jaune/rouge en 2 secondes
- `entry` = Claude ouvre l'arbre, sait exactement où plonger
- `depends` = Les deux savent ce qui bloque quoi

---

## PLAN DE BATAILLE — Dimanche 15 Février 2026

### BLOC 1 — SSH sur les 2 PC [15 min]
**But :** plus jamais de mot de passe pour push/pull.

Sur chaque PC :
```bash
ssh-keygen -t ed25519 -C "sky1241"
cat ~/.ssh/id_ed25519.pub
# → Coller sur GitHub : Settings → SSH keys → New
```

Puis sur chaque PC, convertir chaque repo :
```bash
git remote set-url origin git@github.com:sky1241/[NOM-REPO].git
```

**✅ Validation :** tape `cd ~/3d-printer && git push` → pas de mot de passe demandé.

---

### BLOC 2 — Script autopush [10 min]
**But :** sauvegarder tous les repos en 1 commande.

Créer `~/autopush.sh` (Linux/Mac) ou `~/autopush.ps1` (Windows) :
```bash
#!/bin/bash
for repo in ~/3d-printer ~/HSBC-algo-genetic ~/infernal-wheel ~/sky-toolkit; do
    cd "$repo" 2>/dev/null && git add -A && \
    git commit -m "auto-save $(date '+%Y-%m-%d %H:%M')" 2>/dev/null && \
    git push 2>/dev/null && echo "✓ $repo"
done
```
```bash
chmod +x ~/autopush.sh
```

**✅ Validation :** lance `~/autopush.sh` → il affiche "✓" pour chaque repo sans erreur.

---

### BLOC 3 — Créer sky-toolkit [30 min]
**But :** un seul repo avec tous les outils, accessible partout.

1. Créer `sky-toolkit` sur github.com/new (public, avec README)
2. `git clone git@github.com:sky1241/sky-toolkit.git`
3. Créer la structure :
```bash
mkdir -p prompts workflows ux-framework winter-trees templates
```
4. Migrer le framework UX depuis infernal-wheel (10 dossiers, 276KB)
5. Ajouter le workflow radar/sniper (workflows/radar-sniper.md)
6. `git add -A && git commit -m "feat: initial toolkit" && git push`
7. Cloner sur le 2ème PC

**✅ Validation :** sur les 2 PC, `ls ~/sky-toolkit/` montre 5 dossiers.

---

### BLOC 4 — Winter Tree template + exemple [15 min]
**But :** avoir le template v2 (avec entry/status/depends) prêt à l'emploi.

1. Créer `sky-toolkit/winter-trees/TEMPLATE_v2.md` avec le format ci-dessus
2. Copier l'arbre du 3d-printer comme exemple
3. Push

**✅ Validation :** le fichier TEMPLATE_v2.md contient les champs `entry:`, `status:`, `depends:`.

---

### BLOC 5 — Sauver les prompts [15 min]
**But :** ne plus jamais réécrire un bon prompt.

Copier dans `sky-toolkit/prompts/` :
- `MICR_DEEP_RESEARCH_v2_SURGICAL.md` (le prompt chirurgical)
- `code-audit-template.md` (template d'audit)
- Ce fichier-ci (`MASTER_PROMPT.md`)

**✅ Validation :** `ls ~/sky-toolkit/prompts/` montre au moins 3 fichiers.

---

### BLOC 6 — MICR dans 3d-printer [30 min]
**But :** poser la brique (pas la souder).

1. `cp micr.py ~/3d-printer/`
2. `cd ~/3d-printer && python3 micr.py` → "self-test complete"
3. `git add micr.py && git commit -m "feat: MICR" && git push`

**✅ Validation :** `python3 micr.py` affiche 6 tests OK, aucune erreur.

---

### BLOC 7 — Vérification croisée 2 PC [10 min]
**But :** les 2 PC sont identiques.

Sur chaque PC :
```bash
cd ~/sky-toolkit && git pull && ls
cd ~/3d-printer && git pull && git log --oneline -1
cd ~/HSBC-algo-genetic && git pull && git log --oneline -1
cd ~/infernal-wheel && git pull && git log --oneline -1
ssh -T git@github.com
```

**✅ Validation finale :**
```
[ ] SSH sans mot de passe PC1
[ ] SSH sans mot de passe PC2
[ ] autopush.sh fonctionne PC1
[ ] autopush.sh fonctionne PC2
[ ] sky-toolkit identique sur les 2 PC
[ ] micr.py self-test OK
[ ] Ce prompt (MASTER_PROMPT.md) est dans sky-toolkit/prompts/
```

**Quand les 7 cases sont cochées → journée terminée. T'as ton sucre.**

---

## APRÈS AUJOURD'HUI — Les règles permanentes

1. **Outil poli → sky-toolkit.** Prompt qui marche ? Push. Workflow testé ? Push. Checklist utile ? Push.
2. **Fin de session → autopush.** Une commande, tout est sauvé.
3. **Nouveau projet → Winter Tree.** Avant de coder, dessiner l'arbre. Ça prend 15 min et ça en économise 200.
4. **Recherche → Radar/Sniper.** Deep Research = carte. Claude web search = territoire. Jamais les deux dans le même prompt.
5. **Changement de PC → git pull.** 5 secondes et t'as tout.

---

## CE QUE JE DEMANDE À CLAUDE

Tu es mes mains dans le code. Moi je vois l'arbre, toi tu creuses les racines.

Quand je te donne un Winter Tree, tu sais exactement :
- Où on en est (status)
- Où plonger (entry)
- Ce qui dépend de quoi (depends)

Quand je te dis "fais pousser la branche B5", tu regardes l'entry, tu descends dans le code, tu fais le boulot, et tu me dis ce qui a changé dans l'arbre.

Quand je te dis "montre-moi l'arbre", tu me donnes la vue du dessus avec les statuts.

On est une équipe. Le sol c'est notre interface. Tu descends, je monte, et l'arbre pousse.
