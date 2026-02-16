# 🌲 GROWTH PATTERNS — 6 Familles d'Arbres × Règles de Croissance
# Données brutes de recherche pour le système Winter Tree
# Compilé le 15 Février 2026

---

## SYNTHÈSE RAPIDE

| Famille | Forme | Règle dominante | Projet type |
|---------|-------|-----------------|-------------|
| Conifère | Pyramide, tronc unique | Dominance apicale forte → pousse en HAUTEUR d'abord | Pipeline vertical (HSBC algo) |
| Feuillu | Canopée large, ronde | Branches rivalisent avec le leader → pousse en LARGEUR | Multi-modules (3d-printer) |
| Palmier | Colonne, couronne au sommet | Un seul méristème, zéro branche, tout passe par le sommet | Pipeline étroit, output riche (data pipeline) |
| Baobab | Tronc massif, petite canopée | Stockage dans le tronc → consolider avant d'étendre | Moteur/core énorme, petite interface (database, solveur) |
| Buisson | Multi-tiges depuis la base | Pas de tronc dominant, expansion latérale | Collection d'outils indépendants (sky-toolkit) |
| Liane | Grimpe sur un hôte | Parasite structurel, utilise l'infrastructure existante | Plugin, extension, wrapper d'API |

---

## 1. CONIFÈRE (Pin, Sapin, Épicéa)

### Biologie réelle
- **Dominance apicale** : le bourgeon terminal sécrète de l'auxine qui INHIBE la croissance des bourgeons latéraux. Résultat : un tronc droit, les branches restent courtes.
- **Forme excurrente** : un leader central clair qui va jusqu'au sommet. Forme pyramidale/conique.
- **Ironie botanique** : les conifères ont en fait une dominance apicale FAIBLE au niveau des bourgeons (beaucoup de latéraux poussent chaque année), mais le leader terminal maintient un CONTRÔLE apical fort sur les années suivantes, ce qui donne la forme pyramidale.
- **Si on coupe le leader** : l'arbre ne récupère PAS facilement. Les conifères ne régénèrent pas sur le vieux bois. Le sommet reste nu.
- **Croissance** : verticale d'abord, branches courtes, auto-élagage des branches basses (pas assez de lumière).

### Règles de croissance algorithmiques
```
RÈGLE C1 : TRUNK_FIRST
  → Toujours allonger le tronc (pipeline principal) avant d'ajouter des branches
  → Le tronc ne se divise JAMAIS

RÈGLE C2 : BRANCH_SUBORDINATION
  → Chaque branche est TOUJOURS plus petite que le tronc
  → Ratio : branche.taille < 0.6 × tronc.taille

RÈGLE C3 : TOP_DOWN_GROWTH
  → L'énergie va du sommet vers le bas
  → Les branches les plus hautes sont les plus jeunes et les plus actives
  → Les branches basses meurent naturellement (auto-élagage)

RÈGLE C4 : NO_RECOVERY_ON_OLD_WOOD
  → Si le leader est coupé (feature principale cassée), l'arbre ne récupère pas
  → Il faut replanter (refactoring majeur)

RÈGLE C5 : ENVIRONMENTAL_ADAPTATION
  → Dans une forêt dense (compétition forte) → encore plus vertical
  → En terrain ouvert → branches un peu plus larges mais toujours pyramidal
```

### Mapping projet
- **Quand utiliser** : projet avec un pipeline clair et linéaire (input → traitement → output)
- **Priorité** : finir le pipeline de bout en bout d'abord, optimiser ensuite
- **Danger** : si le tronc casse (architecture fondamentale), tout l'arbre meurt
- **Exemple** : algo de trading (signal → analyse → décision → exécution)

---

## 2. FEUILLU (Chêne, Érable, Orme)

### Biologie réelle
- **Forme décurrente** : le tronc se divise en plusieurs branches principales de taille similaire. Canopée large et ronde.
- **Dominance apicale forte la première année** : peu de latéraux poussent. MAIS l'année suivante, les latéraux sont libérés et peuvent DÉPASSER le leader.
- **Résultat** : le leader central "se perd" parmi les branches. Pas de tronc unique au sommet.
- **Plasticité** : même espèce → forme différente selon l'environnement. En forêt dense → pousse droit (cherche la lumière). En terrain ouvert → s'étale en largeur.
- **Branches co-dominantes** : risque structurel. Deux branches de même taille au même point = point de faiblesse (écorce incluse, V-shape).
- **Croissance** : commence vertical puis s'étale. Les branches latérales rivalisent avec le tronc.

### Règles de croissance algorithmiques
```
RÈGLE F1 : TRUNK_THEN_BRANCH
  → D'abord un tronc court (architecture de base)
  → Puis les branches principales s'élancent et rivalisent

RÈGLE F2 : LATERAL_COMPETITION
  → Les branches peuvent DÉPASSER le tronc
  → Le module le plus nourri (le plus utilisé) devient dominant
  → Pas de hiérarchie fixe : le leader peut changer

RÈGLE F3 : CANOPY_SPREAD
  → L'énergie se distribue en LARGEUR
  → Chaque branche développe ses propres sous-branches
  → La canopée s'étend horizontalement

RÈGLE F4 : CO_DOMINANCE_RISK
  → Si 2 branches ont exactement la même taille → point de rupture structurel
  → Solution : élaguer (refactorer) pour qu'une branche domine

RÈGLE F5 : ENVIRONMENT_SHAPES_FORM
  → Projet en compétition (marché saturé) → pousser vertical (MVP vite)
  → Projet en terrain ouvert (pas de concurrent) → s'étaler (features riches)

RÈGLE F6 : SEASONAL_CYCLE
  → Les feuillus sont décidus : ils perdent leurs feuilles
  → Cycle de releases : build → ship → pause → rebuild
```

### Mapping projet
- **Quand utiliser** : projet multi-modules avec beaucoup de features parallèles
- **Priorité** : tronc court (core), puis développer les branches en parallèle
- **Danger** : branches co-dominantes (deux features de même importance qui entrent en conflit)
- **Exemple** : 3d-printer (8 briques, figurines, constraints, CLI, web — tout pousse en même temps)

---

## 3. PALMIER (Cocotier, Dattier)

### Biologie réelle
- **Un seul méristème apical** : tout — feuilles, fleurs, fruits — sort d'un seul point de croissance au sommet. Zéro branche latérale.
- **Si le méristème meurt → l'arbre meurt.** Pas de plan B. Pas de bourgeon dormant.
- **Pas de croissance secondaire** : le tronc ne grossit pas avec le temps (pas de cernes). Le diamètre est fixé tôt.
- **Monocotylédone** : pas de cambium vasculaire. Faisceaux vasculaires dispersés. Les blessures au tronc sont PERMANENTES (pas de cicatrisation comme chez un chêne).
- **Croissance** : d'abord le diamètre s'établit (phase juvénile), puis l'arbre pousse en hauteur. Les vieilles feuilles tombent, les nouvelles poussent au sommet.
- **Résilience** : le tronc flexible résiste aux tempêtes (plie mais ne casse pas).

### Règles de croissance algorithmiques
```
RÈGLE P1 : SINGLE_MERISTEM
  → Tout passe par UN SEUL point de production
  → Pas de branches parallèles possibles
  → Tuer le méristème = tuer le projet

RÈGLE P2 : DIAMETER_FIRST
  → Le diamètre du tronc est fixé AVANT la croissance en hauteur
  → Fixer l'architecture et le scope AVANT de coder

RÈGLE P3 : NO_LATERAL_BRANCHING
  → Zéro module secondaire
  → Tout est dans le pipeline : input → process → output (couronne)
  → La richesse est au sommet (output), pas dans les branches

RÈGLE P4 : PERMANENT_WOUNDS
  → Les bugs et la dette technique sont PERMANENTS
  → Pas de refactoring possible du tronc (pas de croissance secondaire)
  → Faire bien du premier coup ou accepter le défaut pour toujours

RÈGLE P5 : FLEXIBLE_RESILIENCE
  → Le tronc plie mais ne casse pas
  → Architecture souple, adaptable aux changements externes
  → Mais structure interne figée

RÈGLE P6 : TOP_PRODUCTION
  → Toute la production (feuilles, fruits, fleurs) est au sommet
  → L'output est riche et concentré, le pipeline est étroit
```

### Mapping projet
- **Quand utiliser** : pipeline de données, ETL, script de processing
- **Priorité** : fixer le diamètre (scope, architecture) tôt. Ensuite pousser en hauteur (fonctionnalités)
- **Danger** : si le coeur meurt, TOUT meurt. Pas de backup, pas de branche de secours
- **Exemple** : un script de data processing (input fichier → traitement → rapport riche)

---

## 4. BAOBAB (Adansonia)

### Biologie réelle
- **Tronc massif, petite canopée** : diamètre jusqu'à 10-14m. Hauteur modeste (5-25m). "L'arbre à l'envers" — les branches ressemblent à des racines.
- **Stockage d'eau** : le tronc est composé de 80% d'eau. Parenchyme spongieux (pas du bois dense). Un baobab peut stocker 120 000 à 136 400 litres d'eau.
- **Bois mou** : le bois est léger et poreux. 5% de bois solide seulement dans certaines espèces. C'est un SUCCULENT géant.
- **Stratégie de survie** : stocker pendant la saison des pluies (4 mois) → survivre pendant la saison sèche (8 mois). Perd ses feuilles pour économiser l'eau.
- **Écorce régénérative** : l'écorce (jusqu'à 8cm d'épaisseur) se régénère même après des dommages sévères (éléphants qui arrachent l'écorce).
- **Longévité** : certains spécimens ont 2000-3000 ans.
- **Paradoxe structurel** : le tronc massif n'est PAS pour le stockage (contrairement à ce qu'on pensait). C'est pour la stabilité structurelle — sans ce diamètre, le bois mou ferait s'effondrer l'arbre.

### Règles de croissance algorithmiques
```
RÈGLE B1 : TRUNK_IS_STORAGE
  → Le tronc (core engine) accumule des ressources (données, configs, modèles)
  → La canopée (interface) est petite par rapport au tronc
  → Ratio : core_size >> interface_size

RÈGLE B2 : CONSOLIDATE_BEFORE_EXPAND
  → D'abord remplir le tronc (core solide, testé, validé)
  → Ensuite seulement faire pousser des branches (features)
  → L'arbre grandit en LARGEUR de tronc avant en hauteur

RÈGLE B3 : SEASONAL_CYCLE
  → Phase de pluie = développement intense (code, features, tests)
  → Phase sèche = maintenance minimale, pas de nouvelles features
  → L'arbre perd ses feuilles (features non-essentielles) pour survivre

RÈGLE B4 : BARK_REGENERATION
  → L'interface (écorce) peut être endommagée et régénérée
  → Le core (tronc) est protégé par l'écorce
  → Les utilisateurs touchent l'écorce, pas le bois

RÈGLE B5 : SOFT_WOOD_PARADOX
  → Le code n'a pas besoin d'être "dur" (hyper-optimisé)
  → Il a besoin d'être LARGE (couvrir beaucoup de cas)
  → La taille du tronc compense la souplesse du bois

RÈGLE B6 : EXTREME_LONGEVITY
  → Architecture conçue pour durer des ANNÉES
  → Pas de framework à la mode, pas de dépendances fragiles
  → Zero-dependency = survie millénaire
```

### Mapping projet
- **Quand utiliser** : moteur/engine énorme avec une petite interface
- **Priorité** : consolider le core d'abord. L'interface vient après.
- **Danger** : si on tire trop d'eau du tronc (trop de features trop vite) → l'arbre s'effondre
- **Exemple** : un solveur de contraintes (660 lignes de core, le user voit juste "solved: true")

---

## 5. BUISSON (Arbuste)

### Biologie réelle
- **Pas de tronc dominant** : multiple tiges qui partent de la base ou près du sol.
- **Hauteur limitée** : généralement 1-6m. Compact et dense.
- **Branching from base** : pas de hiérarchie claire. Chaque tige est indépendante.
- **Résilience par redondance** : si une tige meurt, les autres continuent. Le buisson survit à la perte de n'importe quelle partie.
- **Suckering** : nouvelles pousses émergent des racines. Expansion horizontale par clonage.
- **Rajeunissement** : la taille drastique (coupe au ras du sol) stimule une nouvelle croissance vigoureuse. Le buisson se régénère complètement.
- **Stratégie** : pas de compétition en hauteur. Couverture au sol, densité, résistance.
- **Throwaway stems** : tiges "jetables", peu d'investissement par tige, haut remplacement.

### Règles de croissance algorithmiques
```
RÈGLE S1 : NO_CENTRAL_TRUNK
  → Pas de module principal
  → Chaque outil/composant est indépendant
  → Pas de hiérarchie — tous les composants sont au même niveau

RÈGLE S2 : REDUNDANCY_IS_RESILIENCE
  → Si un composant meurt, les autres continuent
  → Pas de single point of failure
  → La valeur est dans la COLLECTION, pas dans un élément

RÈGLE S3 : HORIZONTAL_EXPANSION
  → Croissance latérale, pas verticale
  → Ajouter de nouveaux outils, pas approfondir un outil existant
  → Le buisson s'étale pour couvrir plus de terrain

RÈGLE S4 : REJUVENATION_BY_PRUNING
  → Coupe drastique = renaissance vigoureuse
  → Un buisson peut être coupé au ras et repousse plus fort
  → Refactoring radical est non seulement possible mais BÉNÉFIQUE

RÈGLE S5 : LOW_INVESTMENT_PER_STEM
  → Chaque outil est petit, simple, jetable
  → Pas de gros investissement dans un seul composant
  → Si ça marche pas → on le jette et on en fait un autre

RÈGLE S6 : SUCKERING_CLONAL_SPREAD
  → Les bons patterns se propagent d'un outil à l'autre
  → Templates, conventions, standards = propagation clonale
  → Un buisson est une colonie, pas un individu
```

### Mapping projet
- **Quand utiliser** : collection d'outils, boîte à outils, utilities
- **Priorité** : ajouter des outils, garder chacun petit et indépendant
- **Danger** : le buisson ne grandit jamais très haut (pas de produit impressionnant isolément)
- **Exemple** : sky-toolkit (prompts, workflows, templates — tous indépendants)

---

## 6. LIANE (Vigne, Figuier Étrangleur)

### Biologie réelle
- **Parasite structurel** : utilise les arbres existants comme support. Ne construit PAS son propre tronc solide.
- **Stratégie** : investir dans la VITESSE de croissance plutôt que la solidité structurelle. Tiges pleines de vaisseaux conducteurs (transport rapide) mais pas de bois dur.
- **Figuier étrangleur** : commence comme épiphyte dans la canopée, envoie des racines vers le sol, enveloppe l'hôte, finit par le tuer et le remplacer.
- **Contagion** : une seule liane peut s'étendre sur 49 arbres (donnée réelle).
- **Stratégies d'accroche** : vrilles, épines, racines adventives, poils adhésifs, enroulement.
- **Représente 25% des espèces ligneuses** des forêts tropicales.
- **Impact sur l'hôte** : réduit la croissance de 50%+ des arbres, double la probabilité de mort de l'hôte, réduit la production de fruits de 60%.
- **Martin Fowler pattern** : "Strangler Fig Application" — remplacer progressivement un système legacy en l'enveloppant.

### Règles de croissance algorithmiques
```
RÈGLE L1 : HOST_REQUIRED
  → L'arbre hôte (système existant, API, framework) DOIT exister d'abord
  → La liane ne pousse pas seule — elle wrappe quelque chose

RÈGLE L2 : SPEED_OVER_STRUCTURE
  → Pas besoin de tronc solide (pas d'infrastructure propre)
  → Investir dans la vitesse de développement
  → Le code de la liane est simple et rapide à écrire

RÈGLE L3 : CLIMBING_STRATEGIES
  → Vrilles = hooks/callbacks sur l'API de l'hôte
  → Enroulement = wrapper autour du système existant
  → Racines adventives = points d'ancrage multiples

RÈGLE L4 : STRANGLER_PATTERN
  → Commencer par coexister avec l'hôte
  → Progressivement remplacer les fonctionnalités de l'hôte
  → À la fin, l'hôte meurt et la liane est autonome
  → C'est le pattern de migration legacy → new system

RÈGLE L5 : CONTAGION_SPREAD
  → Une liane peut s'étendre sur PLUSIEURS hôtes
  → Un plugin/extension qui fonctionne sur plusieurs plateformes
  → La valeur est dans la PORTÉE, pas dans la profondeur

RÈGLE L6 : FRAGILE_WITHOUT_HOST
  → Si l'hôte tombe, la liane tombe avec
  → Dépendance forte sur le système sous-jacent
  → Risque : si l'API change, la liane casse
```

### Mapping projet
- **Quand utiliser** : plugin, extension, wrapper d'API, migration legacy
- **Priorité** : s'accrocher à l'hôte d'abord, étendre ensuite
- **Danger** : dépendance totale à l'hôte. Si l'API change = mort
- **Exemple** : une extension Chrome, un plugin Flutter, un wrapper d'API tierce

---

## RÉFÉRENCES ACADÉMIQUES CLÉS

### Botanique / Croissance
- **Lindenmayer (1968)** — L-Systems : grammaire formelle de croissance des plantes
- **Prusinkiewicz & Lindenmayer** — "The Algorithmic Beauty of Plants" (livre de référence L-Systems)
- **Fourcaud et al. (1997)** — Modèle fonctionnel de croissance d'arbre (AMAPpara)
- **Brown (1971)** — "Apical Dominance and Form in Woody Plants: A Reappraisal"
- **Chapotin et al. (2006)** — Étude structurelle du baobab (tronc = stabilité, pas stockage)

### Software Architecture / Évolution
- **Tomer & Schach (2000)** — "Evolution Tree" : cycle de vie logiciel comme arbre de décisions
- **Martin Fowler** — "Strangler Fig Application" : migration legacy progressive
- **Barnes (2013, CMU)** — "Software Architecture Evolution" : chemins d'évolution comme graphe
- **Özdemir & Arslan Selçuk (2016)** — "Tree Metaphor in Architectural Design"

### L-Systems / Fractales
- **Wikipedia L-Systems** — Axiome + règles de production + interprétation géométrique
- **Houdini L-System** — Implémentation pratique avec paramètres

---

## TABLEAU DE DÉCISION — "Quel arbre est mon projet ?"

```
Q1: Le projet a-t-il un pipeline linéaire clair ?
    OUI → Q2
    NON → Q3

Q2: Le pipeline est-il étroit (peu de code) avec un output riche ?
    OUI → 🌴 PALMIER
    NON → 🌲 CONIFÈRE

Q3: Le projet a-t-il un core énorme et une petite interface ?
    OUI → 🌳 BAOBAB
    NON → Q4

Q4: Le projet a-t-il plusieurs modules parallèles ?
    OUI → Q5
    NON → Q6

Q5: Les modules sont-ils interdépendants ?
    OUI → 🍁 FEUILLU
    NON → 🌿 BUISSON

Q6: Le projet wrappe-t-il un système existant ?
    OUI → 🌿 LIANE
    NON → 🍁 FEUILLU (par défaut)
```

---

## APPLICATION AUX PROJETS DE SKY

| Projet | Famille | Justification |
|--------|---------|---------------|
| HSBC-algo-genetic | 🌲 Conifère | Pipeline linéaire : signal → analyse → trade. Tronc = le moteur de décision. |
| 3d-printer | 🍁 Feuillu | 8 briques parallèles, branches co-dominantes, canopée large. |
| 3d-printer (MICR) | 🌳 Baobab | Solveur inverse de contraintes intégré au 3d-printer. Tronc massif, output = "solved: true". |
| sky-toolkit | 🌿 Buisson | Collection d'outils indépendants, pas de hiérarchie, expansion horizontale. |
| shazam-piano | 🌴 Palmier | Pipeline audio étroit : micro → FFT → pitch detection → affichage. |
| infernal-wheel | 🍁 Feuillu | Dashboard + UX framework + mobile app → branches multiples. |
| fck-translation | 🌴 Palmier | Audio in → traduction → text out. Pipeline étroit, output riche. |

---

## PROCHAINE ÉTAPE

Transformer ces règles en un système utilisable :
1. Template Winter Tree v2 avec champ `family:` (conifère/feuillu/palmier/baobab/buisson/liane)
2. Règles de croissance automatiques basées sur la famille
3. Quand Sky dit "fais pousser l'arbre", Claude sait s'il faut aller en hauteur, en largeur, ou consolider le tronc
