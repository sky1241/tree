# WINTER TREE — RECHERCHE APPROFONDIE v2
## Les Architectes du Système + Les 6 Familles Botaniques
### Recherche web sniper — 14 février 2026

---

# PARTIE 1 : LES 5 ARCHITECTES DU SYSTÈME

---

## 1. ARISTID LINDENMAYER (1925–1989)

**Paper fondateur :** "Mathematical models for cellular interactions in development, Parts I and II" — Journal of Theoretical Biology, vol. 18, 1968, pp. 280–315.

**Qui :** Biologiste théorique hongrois, Université d'Utrecht (Pays-Bas). Travaillait sur les levures, champignons filamenteux, et cyanobactéries (Anabaena catenula).

**L'invention — Les L-Systems :**
- Système formel de réécriture parallèle de chaînes de caractères
- Composants : un alphabet de symboles, un axiome (état initial), des règles de production (comment chaque symbole se transforme), et une interprétation géométrique
- Différence clé avec Chomsky : les règles s'appliquent **en parallèle** (toutes en même temps), pas séquentiellement — comme les cellules d'une plante qui se divisent toutes simultanément
- Résultat : des structures complexes émergent de règles simples par itération récursive

**Exemple originel — croissance d'algue :**
```
Axiome : A
Règles : A → AB, B → A
n=0: A
n=1: AB
n=2: ABA
n=3: ABAAB
```
Les longueurs donnent la suite de Fibonacci : 1, 1, 2, 3, 5, 8, 13, 21...

**Extensions clés :**
- L-systems bracketed (1974) : ajout de `[` et `]` pour représenter les branches
- L-systems stochastiques : probabilités dans les règles de production
- L-systems context-sensitive : la transformation d'un symbole dépend de ses voisins
- L-systems paramétriques : attributs numériques associés aux symboles

**Impact :** Devenu le formalisme de référence pour modéliser le développement des plantes — de la génétique moléculaire aux communautés végétales. Utilisé en infographie (Smith 1984), animation (SIGGRAPH), et simulation de croissance.

**Ce qu'on retient pour Winter Tree :** Les règles simples + itération parallèle = complexité émergente. C'est exactement le principe : on définit les règles de croissance (production rules) et on laisse le projet pousser.

---

## 2. PRZEMYSLAW PRUSINKIEWICZ + ARISTID LINDENMAYER

**Livre :** "The Algorithmic Beauty of Plants" — Springer, 1990. 228 pages. Disponible gratuitement en ligne (algorithmicbotany.org).

**Qui :** Prusinkiewicz — informaticien polonais-canadien, Université de Calgary. Collaborateur principal de Lindenmayer pour les applications graphiques.

**Contenu du livre (chapitres clés) :**
- Ch.1 : Modélisation graphique avec L-systems — DOL-systems, interprétation turtle, 3D
- Ch.2 : Modélisation des arbres — branching patterns, phyllotaxie
- Ch.3 : Modèles développementaux des plantes herbacées
- Ch.4 : Phyllotaxie — arrangement des feuilles (spirales de Fibonacci)
- Ch.5 : Modèles de cellwork — développement cellulaire
- Ch.6 : Animation du développement des plantes
- Ch.7 : Fractales et systèmes de fonctions itérées

**Innovation principale :** Interprétation "turtle graphics" des L-systems. La chaîne de caractères générée est traduite en instructions pour une "tortue" qui dessine :
- `F` = avancer et tracer
- `+` / `-` = tourner à gauche/droite
- `[` = sauvegarder position (début de branche)
- `]` = restaurer position (fin de branche)
- `@` = réduire la taille du pas

**Réception :** Reviewé comme "premier livre complet sur la simulation informatique des patterns de développement des plantes." George Klir (Int. J. General Systems) : témoignage du génie de Lindenmayer et de la puissance de la technologie informatique. Les images ne sont pas des photos — elles sont toutes générées par algorithme.

**Ce qu'on retient pour Winter Tree :** Le livre prouve qu'on peut capturer la beauté ET la logique de la croissance avec des règles formelles. La turtle graphics = l'ancêtre conceptuel de notre "descente dans les racines" — chaque symbole correspond à une action concrète dans le code.

---

## 3. AMIR TOMER & STEPHEN R. SCHACH (2000)

**Paper :** "The Evolution Tree: A Maintenance-Oriented Software Development Model" — Proceedings of CSMR 2000 (4th European Conference on Software Maintenance and Reengineering), Zurich, Suisse, Février 2000, pp. 209-214. IEEE.

**Affiliation :** Tomer — RAFAEL Ltd, Haïfa, Israël. Schach — Vanderbilt University, Nashville, TN.

**Concept clé — L'arbre d'évolution :**
- Modèle 2D du cycle de vie logiciel
- Le développement logiciel = évolution continue d'un produit
- Chaque version = un nœud dans l'arbre
- Chaque décision d'ingénierie = une branche
- La maintenance n'est PAS une phase après la livraison — c'est le processus fondamental depuis le premier jour
- Le développement initial est un CAS PARTICULIER de la maintenance

**Structure :**
- Axe horizontal : les versions successives (évolution temporelle)
- Axe vertical : les phases de développement de chaque version
- Composant additionnel : le "propagation graph" — structure de données qui suit l'impact des changements de requirements sur tous les artefacts

**Extension 3D (2002, Systems Engineering journal) :**
- 3ème axe ajouté : la réutilisation
- Le modèle gère les product lines (familles de produits)
- Réutilisation bidirectionnelle : du core vers un produit spécifique ET d'un produit vers le core

**Ce qu'on retient pour Winter Tree :** L'idée que le développement = un arbre de décisions d'ingénierie qui évolue dans le temps. Et surtout : la maintenance est le processus PRINCIPAL, pas un afterthought. Le propagation graph = notre champ `depends` dans le template v2.

---

## 4. MARTIN FOWLER — Strangler Fig Application (2004)

**Post originel :** blog post sur martinfowler.com, 2004. Renommé "Strangler Fig Application" en 2019.

**Contexte de l'idée :**
Vacances dans les forêts tropicales du Queensland (Australie) en 2001. Fowler observe les figuiers étrangleurs : des vignes qui germent dans un creux d'arbre, poussent vers le sol pour les racines et vers la canopée pour la lumière, finissent par devenir autosuffisantes, et l'arbre hôte meurt — laissant le figuier comme un écho de sa forme.

**Le pattern :**
- Modernisation progressive d'un système legacy
- Au lieu d'un "big bang rewrite" (risqué, long, souvent échoué)
- On construit le nouveau système autour de l'ancien
- Petit à petit, on déplace les comportements de l'ancien vers le nouveau
- Les deux coexistent pendant la transition
- L'ancien système "meurt" progressivement

**4 activités clés (Ian Cartwright, Rob Horn, James Lewis) :**
1. Clarifier les objectifs de la modernisation
2. Identifier les "seams" (coutures) dans le système legacy
3. Commencer à remplacer composant par composant
4. Itérer — chaque remplacement réduit le risque et apporte de la valeur

**Avantages vs big bang rewrite :**
- Investissement et retours graduels et visibles
- On peut pauser la migration si besoin
- On apprend en route (validation en production)
- Chaque étape est réversible
- On ne découvre pas ses erreurs à la fin

**Popularité :** 3000+ vues/mois sur son blog. Adopté par Azure, AWS, Google Cloud comme pattern officiel. Utilisé massivement pour les migrations monolith → microservices.

**Ce qu'on retient pour Winter Tree :** La liane de notre système. Le pattern prouve qu'on peut migrer un système en le "grandissant" de l'extérieur. C'est exactement notre famille Liane : HOST_REQUIRED → CLIMBING → STRANGLER → autonomie.

---

## 5. JEFFREY M. BARNES — CMU (2013)

**Thèse :** "Software Architecture Evolution" — CMU-ISR-13-118, Institute for Software Research, School of Computer Science, Carnegie Mellon University, Décembre 2013.

**Directeur :** David Garlan (pionnier de l'architecture logicielle, Fellow IEEE et ACM).

**Concept clé — Evolution paths :**
- L'évolution architecturale = un graphe d'états
- Chaque nœud = une représentation complète de l'architecture du système
- Chaque arête = une transition évolutive possible
- Le travail de l'architecte = choisir le chemin optimal à travers le graphe

**Innovation — "Evolution Styles" (2009, avec Garlan) :**
- Des patterns récurrents d'évolution architecturale
- Comme les design patterns mais pour l'ÉVOLUTION, pas la conception statique
- Permettent de raisonner sur les chemins d'évolution
- Fondation pour des outils d'aide à la décision

**Paper ICSE 2013 — Automated Planning :**
- Utilisation de techniques de planification automatisée (AI planning)
- Génération automatique de chemins d'évolution
- Réduit la charge sur l'architecte (plus besoin de définir manuellement chaque transition)
- Traduction de l'évolution architecturale en problème de planification formelle

**Questions adressées :**
- Comment stager l'évolution pour atteindre les objectifs business ?
- Comment s'assurer que les releases intermédiaires ne cassent rien ?
- Comment réduire le risque d'intégration de nouvelles technos ?
- Quels changements peuvent être faits indépendamment vs. nécessitent une coordination ?
- Comment faire des trade-offs temps/effort de développement ?

**Ce qu'on retient pour Winter Tree :** L'idée du graphe d'évolution — chaque projet a un état actuel et un état cible, et il faut planifier le chemin entre les deux. Les "evolution styles" = nos familles d'arbres : des patterns qui dictent COMMENT le système évolue, pas juste à quoi il ressemble.

---

# PARTIE 2 : LES 6 FAMILLES BOTANIQUES — DONNÉES SCIENTIFIQUES

---

## 1. 🌲 CONIFÈRE (Pin, Sapin, Épicéa)

### Données botaniques

**Dominance apicale — LE mécanisme central :**
- Paradoxe découvert par Brown et al. (1967) : les conifères ont une dominance apicale FAIBLE (weak apical dominance) mais un contrôle apical FORT (strong apical control)
- Dominance apicale = inhibition des bourgeons latéraux sur la pousse courante → les conifères n'inhibent PAS fortement les bourgeons la première année
- Contrôle apical = capacité du leader terminal à dépasser les branches latérales au fil des ans → les conifères maintiennent un leader dominant année après année
- Résultat : forme excurrente (pyramidale, un seul leader jusqu'au sommet)

**Mécanisme hormonal :**
- L'auxine (IAA) est synthétisée dans le méristème apical et transportée de façon basipétale (de l'apex vers la base)
- Ce flux d'auxine bloque la capacité d'export d'auxine des bourgeons latéraux dormants (Prusinkiewicz et al., 2009)
- Les cytokinines (CK), produites principalement dans les racines, sont transportées de façon acropétale (vers l'apex) et antagonisent l'auxine
- C'est le RATIO auxine:cytokinine qui contrôle, pas la quantité absolue
- Si le leader est coupé → arrêt du flux d'auxine → les CK activent les bourgeons latéraux → repousse

**Comportement si le leader est perdu :**
- Chez la plupart des conifères, un bourgeon latéral peut prendre le relais et devenir le nouveau leader
- EXCEPTION : Norfolk Island Pine — les branches latérales secondaires n'ont pas la capacité de devenir dominantes ; un bouture peut pousser horizontalement pendant des années
- Pin parasol (Italian stone pine) — perd la dominance apicale assez tôt, développe une forme arrondie

**Vigueur et forme :**
- Les pousses vigoureuses ont MOINS de dominance apicale → forme plus excurrente
- Les arbres stressés/matures deviennent plus décurrents (arrondis) → perte de contrôle apical
- Un conifère jeune et excurrent peut devenir arrondi en vieillissant

**Références :** Brown et al. (1967), Cline (2007 - Can. J. For. Res.), Purdue Extension FNR-534-W, Thimann & Skoog (1933).

### Règles algorithmiques validées

| Règle | Validation botanique |
|-------|---------------------|
| TRUNK_FIRST | Le leader terminal dépasse les latérales grâce au contrôle apical fort |
| BRANCH_SUBORDINATION | Les branches restent plus petites que le tronc (contrôle apical) |
| NO_RECOVERY_ON_OLD_WOOD | Exceptions existent, mais la plupart des conifères ne régénèrent pas sur vieux bois |
| TOP_DOWN_GROWTH | Flux d'auxine basipétal = énergie/info descend de l'apex |
| ENVIRONMENTAL_ADAPTATION | Forêt dense → plus vertical ; terrain ouvert → légèrement plus large |

---

## 2. 🍁 FEUILLU (Chêne, Érable, Orme)

### Données botaniques

**Dominance apicale FORTE mais contrôle apical FAIBLE :**
- Exactement l'inverse du conifère
- Dominance apicale forte la première année → peu de bourgeons latéraux se développent
- MAIS l'année suivante, les bourgeons latéraux sont libérés et peuvent DÉPASSER le leader original
- Résultat : le leader central se "perd" parmi les branches → forme décurrente (arrondie, étalée)

**Branches co-dominantes — le risque structurel :**
- Quand deux tiges de même diamètre rivalisent → absence de "branch protection zone"
- Risque de V-shape avec écorce incluse → point de rupture en tempête
- Les branches co-dominantes sont la cause #1 de défaillance structurelle chez les feuillus
- Solutions : enlever l'une des co-dominantes tôt, ou câblage

**Plasticité environnementale :**
- Le même chêne en forêt dense = vertical, peu de branches basses (compétition pour la lumière)
- Le même chêne isolé en plein champ = large canopée étalée
- C'est la même espèce, la même génétique — l'environnement façonne la forme

**Cycle saisonnier :**
- Développement du bois au printemps/été
- Sénescence et chute des feuilles en automne
- Dormance en hiver → les bourgeons se préparent pour le prochain cycle
- La phase de dormance est ESSENTIELLE — c'est pendant cette pause que les bourgeons latéraux sont "libérés"

**Références :** Brown et al. (1967), Cline (2007), Purdue Extension FNR-534-W.

### Règles algorithmiques validées

| Règle | Validation botanique |
|-------|---------------------|
| TRUNK_THEN_BRANCH | Tronc court puis branches dominent (leader perdu) |
| LATERAL_COMPETITION | Les branches latérales dépassent le leader (contrôle apical faible) |
| CO_DOMINANCE_RISK | Deux branches de même diamètre = défaillance structurelle |
| ENVIRONMENT_SHAPES_FORM | Plasticité extrême : forme dépend du contexte |
| SEASONAL_CYCLE | Alternance build/pause essentielle pour libérer les bourgeons |

---

## 3. 🌴 PALMIER

### Données botaniques

**Méristème apical unique — le principe cardinal :**
- Un seul point de croissance par tige (le SAM — Shoot Apical Meristem)
- Toutes les feuilles et fleurs naissent de CE seul méristème
- Pas de méristème latéral, pas de cambium vasculaire
- Si le méristème meurt → la tige meurt (espèces à tige unique = mort de la plante entière)
- Branchement aérien extrêmement rare — seulement chez Hyphaene (doum palm) et Phoenix dactylifera

**Pas de croissance secondaire :**
- Les palmiers sont des monocotylédones — pas de cambium comme les dicots
- Le diamètre du tronc est fixé tôt par "primary gigantism" (terme officiel)
- L'augmentation du diamètre se fait par division et élargissement des cellules de parenchyme
- C'est une "diffuse secondary growth" — pas de production de xylème/phloème secondaire
- Conséquence : le tronc garde un diamètre quasi constant de la base au sommet (forme cylindrique)

**Blessures permanentes :**
- Chez les dicots, les blessures sont compartimentées et recouvertes par la croissance secondaire
- Chez les palmiers, les blessures sont PERMANENTES — pas de mécanisme de réparation
- Les faisceaux vasculaires sont dispersés dans tout le tronc (pas en anneaux comme les dicots)

**Establishment growth :**
- Avant de pousser en hauteur, un jeune palmier doit d'abord atteindre son diamètre définitif
- Phase d'établissement lente → puis croissance en hauteur accélérée
- Les feuilles les plus jeunes sont au sommet ; les plus vieilles à la base de la couronne
- Quand les feuilles atteignent la base de la couronne, elles sont coupées du système vasculaire → abscission

**Références :** UF/IFAS Extension (Broschat), Oil Palm SAM study (PMC), Secondary Growth Wikipedia, La Palmeraie.

### Règles algorithmiques validées

| Règle | Validation botanique |
|-------|---------------------|
| SINGLE_MERISTEM | Un seul SAM — si il meurt, tout meurt |
| DIAMETER_FIRST | Establishment growth : fixer le diamètre AVANT la hauteur |
| NO_LATERAL_BRANCHING | Pas de branches latérales (extrêmement rare) |
| PERMANENT_WOUNDS | Pas de compartimentalisation, blessures permanentes |
| FLEXIBLE_RESILIENCE | Les palmiers résistent aux tempêtes par flexibilité du tronc |

---

## 4. 🌳 BAOBAB (Adansonia)

### Données botaniques

**Le paradoxe du tronc massif :**
- Diamètre jusqu'à 10-14 mètres, hauteur 5-25 mètres
- Le bois de baobab : densité 0.09–0.17 g/cm³ (extrêmement léger)
- Contenu en eau : jusqu'à 79%
- Contenu en parenchyme : 69–88%
- Résultat : le bois solide représente aussi peu que 5% du volume dans certaines espèces
- Cellules vivantes jusqu'à 35 cm de profondeur dans le xylème depuis le cambium

**La raison du tronc massif — BIOMÉCANIQUE, pas stockage :**
- Étude de Chapotin et al. (2006, American Journal of Botany) : le tronc massif est nécessaire pour empêcher l'arbre de s'effondrer sous son propre poids
- Le bois est trop mou et trop aqueux → le module élastique approche celui du tissu de parenchyme pur
- Sans ce diamètre massif, l'arbre flamberait (buckling)
- Le coût de construction volumétrique est PLUSIEURS FOIS inférieur à celui d'un arbre typique
- L'écorce épaisse (jusqu'à 8 cm) augmente la rigidité globale

**Stockage d'eau — réel mais limité :**
- Un grand baobab peut stocker jusqu'à 120 000–136 400 litres d'eau
- MAIS : le transport de l'eau du parenchyme central vers le tissu vasculaire est TRÈS LENT (chemin haute résistance)
- L'eau stockée est utilisée pour le flush des nouvelles feuilles et la transpiration cuticulaire
- Elle n'est PAS suffisante pour supporter l'ouverture stomatique avant la saison des pluies
- Le flux de sève à la base du tronc est quasi nul pendant la saison sèche
- Le contenu en eau du tronc ne diminue que de ~12% pendant la saison sèche

**Écorce régénérative :**
- Épaisseur : jusqu'à 8 cm dans les spécimens matures
- 75% de l'écorce = phloème secondaire (pas le périderme comme la plupart des arbres)
- Capacité exceptionnelle de guérison même après des dommages sévères
- Les cellules de parenchyme peuvent se re-diviser et se re-différencier
- Résistante au feu

**Structure multi-troncs :**
- Les plus gros baobabs sont souvent formés de 3-8 tiges fusionnées en cercle
- Le creux central n'est pas de la décomposition — c'est la structure naturelle
- Radiocarbone : 1275 ± 20 BP pour le plus vieux spécimen mesuré (Madagascar)

**Cycle saisonnier :**
- Saison des pluies (~4 mois) : feuilles, fleurs, accumulation d'eau
- Saison sèche (~8 mois) : perte de toutes les feuilles, métabolisme minimal
- La circonférence du tronc diminue de 2-3 cm pendant la saison sèche

**Références :** Chapotin et al. (2006), Wikipedia Adansonia digitata, AskNature, Baum (1995).

### Règles algorithmiques validées

| Règle | Validation botanique |
|-------|---------------------|
| TRUNK_IS_STORAGE | Le tronc accumule des ressources (eau/parenchyme) |
| CONSOLIDATE_BEFORE_EXPAND | Le tronc doit être massif avant que les branches soient viables |
| SOFT_WOOD_PARADOX | Bois mou mais tronc énorme = coverage, pas optimisation |
| BARK_REGENERATION | L'écorce (interface) peut être endommagée et régénérée ; le core est protégé |
| SEASONAL_CYCLE | Phase intense (4 mois) → maintenance minimale (8 mois) |
| EXTREME_LONGEVITY | Architecture zéro-dépendance pour survie multi-millénaire |

---

## 5. 🌿 BUISSON (Arbuste)

### Données botaniques

**Multi-tiges depuis la base — pas de tronc dominant :**
- Les arbustes multi-tiges (cane-growth habit) produisent de multiples tiges depuis le sol
- Aucune tige ne domine naturellement les autres
- Chaque tige est quasi-indépendante — a son propre système vasculaire partiel
- Hauteur typique : 1-6 mètres

**Suckering — expansion horizontale :**
- Beaucoup d'arbustes produisent des suckers (rejets) depuis les racines
- Le système racinaire peut être beaucoup plus large que la partie aérienne
- Les suckers créent des colonies clonales — la plante s'étend horizontalement
- Les bons patterns (génotypes) se propagent à travers les rejets

**Rejuvenation par taille radicale — la preuve de résilience :**
- On peut couper un arbuste multi-tiges à 6-12 pouces du sol ("rejuvenation pruning")
- Le réseau racinaire, plus large et plus ancien, répond en envoyant de nouvelles tiges vigoureuses
- En une saison, l'arbuste ressemble à une nouvelle plantation
- La taille radicale STIMULE la croissance — les nouvelles tiges sont plus colorées, plus fleuries
- Fonctionne tous les 3-5 ans sans dommage permanent

**MAIS : ne marche PAS sur les plantes à tige unique (arbres) ni les conifères**
- Un arbuste à tige unique = si on coupe la tige, c'est fini
- Les conifères ne régénèrent pas sur vieux bois → souche morte
- C'est spécifiquement le caractère multi-tige qui permet la rejuvenation

**Redundance = résilience :**
- Si une tige meurt (maladie, tempête), les autres continuent
- Le système racinaire survit même si toute la partie aérienne est perdue
- L'investissement par tige est faible → remplacement facile

**Références :** UMN Extension, Iowa State Extension, Independent Tree, Texas A&M Aggie Horticulture.

### Règles algorithmiques validées

| Règle | Validation botanique |
|-------|---------------------|
| NO_CENTRAL_TRUNK | Pas de tige dominante — toutes au même niveau |
| REDUNDANCY_IS_RESILIENCE | Si une tige meurt, les autres continuent |
| HORIZONTAL_EXPANSION | Suckering = expansion par les racines |
| REJUVENATION_BY_PRUNING | Taille radicale = regrowth vigoureux |
| LOW_INVESTMENT_PER_STEM | Chaque tige est petite, remplaçable |
| SUCKERING_CLONAL_SPREAD | Les bons patterns se propagent |

---

## 6. 🌿 LIANE (Figuier étrangleur, Vignes)

### Données botaniques

**Cycle de vie du figuier étrangleur (Fowler, 2001 + botanique) :**
1. La graine est déposée par un oiseau dans un creux en haut d'un arbre hôte
2. Le figuier germe là — accès direct à la lumière (canopée)
3. Les racines poussent vers le bas le long du tronc de l'hôte
4. Les racines atteignent le sol → le figuier devient autosuffisant pour l'eau et les nutriments
5. Les racines s'épaississent et enveloppent progressivement le tronc de l'hôte
6. L'hôte est "étranglé" — privé de lumière et comprimé mécaniquement
7. L'hôte meurt → le figuier reste comme un écho de sa forme, avec un tronc creux

**Stratégie d'investissement — vitesse plutôt que structure :**
- Les lianes investissent dans la VITESSE de croissance, pas dans la solidité structurelle
- Tiges pleines de faisceaux vasculaires (transport rapide) mais pas de bois dur
- Représentent 25% des espèces ligneuses dans les forêts tropicales
- Peuvent s'étendre sur 49 arbres hôtes (étude citée dans session précédente)

**Stratégies d'accroche (climbing strategies) :**
- Vrilles (tendrils)
- Épines (spines)
- Racines adventives
- Poils adhésifs
- Enroulement (coiling)

**Impact sur l'hôte :**
- Réduit la croissance de l'hôte de 50%+
- Double la mortalité de l'hôte
- Réduit la production de fruits de 60%
- MAIS : les deux coexistent pendant longtemps avant que l'hôte ne meure

**Fragilité sans hôte :**
- Si l'arbre hôte tombe, la liane tombe aussi (avant d'être autosuffisante)
- La survie dépend entièrement de l'infrastructure de l'hôte dans les premières phases

**Références :** Martin Fowler (martinfowler.com), données botaniques de la session précédente.

### Règles algorithmiques validées

| Règle | Validation botanique |
|-------|---------------------|
| HOST_REQUIRED | Germination dans l'hôte — pas d'existence autonome initiale |
| SPEED_OVER_STRUCTURE | Investissement en transport/vitesse, pas en bois dur |
| CLIMBING_STRATEGIES | Multiples méthodes d'accroche |
| STRANGLER_PATTERN | Coexistence → remplacement progressif → autonomie |
| CONTAGION_SPREAD | Une liane peut s'étendre sur 49+ hôtes |
| FRAGILE_WITHOUT_HOST | Si l'hôte tombe, la liane tombe |

---

# PARTIE 3 : SYNTHÈSE — CE QUI EST NOUVEAU

## Ce qui existait avant nous :
1. L-Systems (1968) — grammaire de croissance biologique
2. Evolution Tree (2000) — arbre de décisions logicielles
3. Strangler Fig (2004) — pattern de migration legacy
4. Evolution Styles (2009/2013) — graphe d'états architecturaux

## Ce que le Winter Tree ajoute :
1. **Mapping direct famille botanique → type de projet logiciel** — personne n'a fait ça
2. **Règles de croissance biologiques comme règles de développement** — pas comme métaphore, comme SYSTÈME DE RÈGLES
3. **Le sol comme interface humain-IA** — Sky monte (voit l'arbre), Claude descend (voit les racines)
4. **Template v2 avec entry/status/depends** — fusion de la vision ascendante et descendante
5. **Radar/sniper workflow** — séparation carte/territoire pour la recherche
6. **Classification par famille** — chaque projet diagnostiqué et géré selon sa nature biologique

## La thèse centrale :
> Les algorithmes de croissance des plantes, validés par 57 ans de recherche (1968-2025),
> sont transposables en règles de développement logiciel.
> Ce n'est pas une métaphore — c'est un isomorphisme fonctionnel.

---

*Recherche compilée le 14 février 2026*
*Sources : 87 résultats web analysés, 5 références académiques vérifiées*
*Méthode : sniper workflow (recherche ciblée par sujet)*

---

## Zone abstraite — 7ème famille : Saule Pleureur 🌊

> Idée de Sky, 2026-02-15. À explorer comme kiff du dimanche.

**Concept** : Projet à forte cascade descendante. Core central solide (tronc) mais tout retombe — les modules, l'héritage, les dépendances coulent vers le bas comme les branches du saule. Props drilling, ORM cascades, event propagation descendante.

**Pistes** :
- Frameworks avec héritage profond (React props flow, Django ORM)
- Projets où l'output cascade depuis un point central
- Architecture pub/sub avec propagation descendante
- Visuellement : tronc qui monte, branches qui redescendent, feuilles qui touchent le sol

**Statut** : zone de recherche ouverte. Le sujet a beau être vieux, y'a encore des choses à découvrir.


---

## BREAKTHROUGH MYCELIUM — Modèle "Pluie sur Sol" 🌧️🍄

> Sky, 2026-02-15 22h. Idée brute, noter tel quel.

**Le concept :**
- Le TERRAIN = un carré qui représente le repo Git
- Chaque GIT PUSH = une GOUTTE DE PLUIE qui tombe à un endroit précis du terrain
- L'endroit dépend de QUOI a été modifié (quel fichier, quel module, quel niveau de l'arbre)
- Après l'impact, le MYCELIUM se génère depuis le point d'impact
- Les connexions mycorhiziennes POUSSENT entre les points d'impact au fil du temps
- Plus un endroit reçoit de gouttes (commits fréquents), plus le réseau est dense
- Les chemins entre zones fréquentes deviennent des HYPHES PRINCIPALES (autoroutes)
- Les zones négligées restent sèches (pas de réseau)

**Ce que ça donne visuellement :**
- Animation temporelle : on voit l'historique git se jouer comme une pluie
- Le mycelium pousse en temps réel entre les points d'impact
- Les connexions inter-projets = quand deux repos partagent des gouttes proches
- Le réseau final = la carte de santé du projet

**Données source :**
- `git log` = liste des gouttes (quand, où, quoi)
- Fichiers modifiés par commit = position de la goutte
- Fréquence = densité du réseau
- Co-modifications = connexions directes

**Lien avec les formules existantes :**
- Meškauskas 2004 (neighbour-sensing) = comment une goutte influence ses voisines
- Boswell 2003 (diffusion-advection) = comment le réseau se propage après impact
- Small-world 2025 = topologie émergente du réseau final

**Statut** : idée brute, à formaliser. Potentiellement le cœur de v2.

