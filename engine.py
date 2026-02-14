#!/usr/bin/env python3
"""
WINTER TREE ENGINE v1.0
=======================
Moteur de classification, génération et validation d'arbres de projets.

Basé sur :
- Lindenmayer (1968) — L-Systems
- Prusinkiewicz & Lindenmayer (1990) — Algorithmic Beauty of Plants
- Tomer & Schach (2000) — Evolution Tree
- Fowler (2004) — Strangler Fig Application
- Barnes (2013, CMU) — Software Architecture Evolution

Auteur : Sky — l'architecte de l'architecte
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ============================================================================
# KNOWLEDGE BASE — Les 6 familles et leurs règles
# ============================================================================

FAMILIES = {
    "conifere": {
        "emoji": "🌲",
        "nom": "Conifère",
        "forme": "Pyramide verticale",
        "desc": "Pipeline linéaire avec leader dominant. Le tronc d'abord, les branches subordonnées.",
        "quand": "Pipeline linéaire (signal → analyse → action)",
        "exemples": "Trading algo, ETL, CI/CD pipeline",
        "regles": {
            "TRUNK_FIRST": {
                "desc": "Toujours étendre le tronc (pipeline principal) avant les branches",
                "bio": "Le leader terminal dépasse les latérales grâce au contrôle apical fort",
                "violation": "Développer une feature avant que le pipeline end-to-end fonctionne"
            },
            "BRANCH_SUBORDINATION": {
                "desc": "branch.size < 0.6 × trunk.size",
                "bio": "Les branches restent plus petites que le tronc (contrôle apical)",
                "violation": "Un module secondaire dépasse en complexité le pipeline principal"
            },
            "TOP_DOWN_GROWTH": {
                "desc": "L'énergie/info descend de l'apex",
                "bio": "Flux d'auxine basipétal (apex → base)",
                "violation": "Dépendance circulaire ou bottom-up non planifiée"
            },
            "NO_RECOVERY_ON_OLD_WOOD": {
                "desc": "Si le leader casse, refactoring majeur nécessaire",
                "bio": "La plupart des conifères ne régénèrent pas sur vieux bois",
                "violation": "Ignorer une cassure du pipeline principal"
            },
            "ENVIRONMENTAL_ADAPTATION": {
                "desc": "Forêt dense → plus vertical ; terrain ouvert → plus large",
                "bio": "La compétition façonne la forme même chez les excurrents",
                "violation": "Ignorer les contraintes de l'écosystème (API limits, hardware, etc.)"
            }
        },
        "risques": [
            "Si le tronc (pipeline) casse, tout l'arbre meurt",
            "Pas de redondance naturelle — single point of failure",
            "Les branches ne peuvent pas prendre le relais du leader"
        ],
        "diagnostic_keywords": ["pipeline", "séquentiel", "linéaire", "signal", "étape", "flux", "stream"]
    },

    "feuillu": {
        "emoji": "🍁",
        "nom": "Feuillu",
        "forme": "Canopée large",
        "desc": "Multi-modules en parallèle. Tronc court, branches compétitives.",
        "quand": "Projet multi-modules interdépendants",
        "exemples": "App mobile full-stack, moteur 3D, framework",
        "regles": {
            "TRUNK_THEN_BRANCH": {
                "desc": "Tronc court (architecture de base) puis branches en compétition",
                "bio": "Dominance apicale forte la 1ère année, puis latérales libérées",
                "violation": "Développer des branches sans avoir un tronc stable"
            },
            "LATERAL_COMPETITION": {
                "desc": "Les branches peuvent DÉPASSER le tronc — le module le plus utilisé devient dominant",
                "bio": "Contrôle apical faible — les latérales dépassent le leader",
                "violation": "Forcer un module à rester petit quand l'usage le pousse à grandir"
            },
            "CO_DOMINANCE_RISK": {
                "desc": "Deux branches de même taille = point de rupture structurel",
                "bio": "V-shape avec écorce incluse = défaillance en tempête",
                "violation": "Deux modules rivaux de même taille sans arbitrage"
            },
            "CANOPY_SPREAD": {
                "desc": "L'énergie se distribue en LARGEUR",
                "bio": "Forme décurrente — canopée étalée",
                "violation": "Concentrer tout l'effort sur un seul module au détriment des autres"
            },
            "SEASONAL_CYCLE": {
                "desc": "Build → ship → pause → rebuild",
                "bio": "Alternance croissance/dormance essentielle pour libérer les bourgeons",
                "violation": "Développer sans jamais faire de pause (burnout technique)"
            },
            "ENVIRONMENT_SHAPES_FORM": {
                "desc": "Compétition → vertical (MVP rapide) ; open → spread (features riches)",
                "bio": "Plasticité extrême — même espèce, formes différentes selon l'environnement",
                "violation": "Ignorer le contexte marché/concurrence dans les décisions d'architecture"
            }
        },
        "risques": [
            "Co-dominance : deux modules rivaux créent un point de rupture",
            "Le leader se perd parmi les branches — qui pilote ?",
            "Complexité croissante des inter-dépendances"
        ],
        "diagnostic_keywords": ["modules", "parallel", "composants", "multi", "bricks", "interdépendant", "full-stack"]
    },

    "palmier": {
        "emoji": "🌴",
        "nom": "Palmier",
        "forme": "Colonne + couronne",
        "desc": "Un seul méristème, zéro branche. Pipeline étroit, output riche au sommet.",
        "quand": "Pipeline étroit avec output riche concentré",
        "exemples": "Audio processing, data transformation, traduction",
        "regles": {
            "SINGLE_MERISTEM": {
                "desc": "Tout passe par UN SEUL point de production",
                "bio": "Un seul SAM (Shoot Apical Meristem) par tige",
                "violation": "Créer un deuxième point d'entrée ou de traitement parallèle"
            },
            "DIAMETER_FIRST": {
                "desc": "Fixer l'architecture/scope AVANT de coder",
                "bio": "Establishment growth : diamètre fixé avant la hauteur",
                "violation": "Commencer à coder avant d'avoir fixé le scope et l'API"
            },
            "NO_LATERAL_BRANCHING": {
                "desc": "Zéro module secondaire — tout dans le pipeline",
                "bio": "Pas de branches latérales (extrêmement rare chez les palmiers)",
                "violation": "Ajouter des features hors du pipeline principal"
            },
            "PERMANENT_WOUNDS": {
                "desc": "Bugs et dette technique sont permanents — pas de refactoring du tronc",
                "bio": "Pas de compartimentalisation — blessures permanentes",
                "violation": "Compter sur un refactoring futur du core pour résoudre les problèmes"
            },
            "FLEXIBLE_RESILIENCE": {
                "desc": "Adaptable aux changements externes mais structure interne fixe",
                "bio": "Les palmiers résistent aux tempêtes par flexibilité",
                "violation": "Changer la structure interne au lieu de s'adapter en surface"
            }
        },
        "risques": [
            "Si le méristème (core) meurt, TOUT meurt",
            "Pas de branche de secours — single pipeline",
            "Les blessures au tronc sont permanentes"
        ],
        "diagnostic_keywords": ["audio", "fft", "pipeline", "transform", "conversion", "traduction", "narrow", "processing"]
    },

    "baobab": {
        "emoji": "🌳",
        "nom": "Baobab",
        "forme": "Tronc massif",
        "desc": "Gros moteur, petite interface. Consolider le core avant d'étendre.",
        "quand": "Gros moteur/solveur avec petite interface de sortie",
        "exemples": "Solveur de contraintes, moteur de rendu, compilateur",
        "regles": {
            "TRUNK_IS_STORAGE": {
                "desc": "Le core accumule les ressources — l'interface est petite relative au core",
                "bio": "Tronc massif (10-14m diamètre), canopée petite (5-25m hauteur)",
                "violation": "Interface aussi complexe que le core"
            },
            "CONSOLIDATE_BEFORE_EXPAND": {
                "desc": "Remplir le tronc d'abord, puis faire pousser les branches",
                "bio": "Le bois mou doit être massif pour ne pas s'effondrer",
                "violation": "Ajouter des features avant que le core soit solide"
            },
            "SOFT_WOOD_PARADOX": {
                "desc": "Le code n'a pas besoin d'hyper-optimisation — il a besoin de COUVERTURE",
                "bio": "Densité 0.09-0.17 g/cm³, 69-88% parenchyme, 5% bois solide",
                "violation": "Optimiser prématurément au lieu de couvrir tous les cas"
            },
            "BARK_REGENERATION": {
                "desc": "L'interface peut être endommagée/régénérée ; le core est protégé",
                "bio": "Écorce de 8cm qui régénère même après dommages sévères",
                "violation": "Laisser un bug d'interface corrompre le core"
            },
            "SEASONAL_CYCLE": {
                "desc": "Phase de dev intensive → phase de maintenance minimale",
                "bio": "4 mois de pluie (croissance) → 8 mois secs (survie)",
                "violation": "Développement continu sans phase de stabilisation"
            },
            "EXTREME_LONGEVITY": {
                "desc": "Architecture zéro-dépendance pour survie multi-année",
                "bio": "Longévité 1000+ ans, troncs multi-tiges fusionnés",
                "violation": "Dépendances sur des libs/APIs instables"
            }
        },
        "risques": [
            "Tirer trop de ressources du core trop vite → collapse",
            "Le transport interne est LENT (haute résistance)",
            "Le tronc peut être creux — attention à la dette technique cachée"
        ],
        "diagnostic_keywords": ["moteur", "engine", "solver", "solveur", "constraint", "core", "calcul", "massif"]
    },

    "buisson": {
        "emoji": "🌿",
        "nom": "Buisson",
        "forme": "Multi-tiges",
        "desc": "Pas de tronc dominant. Collection d'outils indépendants.",
        "quand": "Collection d'outils/scripts/templates indépendants",
        "exemples": "Toolkit, dotfiles, collection de prompts, utils",
        "regles": {
            "NO_CENTRAL_TRUNK": {
                "desc": "Pas de module principal — tous les composants sont au même niveau",
                "bio": "Pas de tige dominante — toutes égales depuis la base",
                "violation": "Créer une dépendance centrale dont tout dépend"
            },
            "REDUNDANCY_IS_RESILIENCE": {
                "desc": "Si un outil meurt, les autres continuent — pas de single point of failure",
                "bio": "Si une tige meurt, les autres continuent",
                "violation": "Créer des dépendances entre les outils"
            },
            "HORIZONTAL_EXPANSION": {
                "desc": "Ajouter de nouveaux outils, ne pas approfondir les existants",
                "bio": "Suckering = expansion horizontale par les racines",
                "violation": "Sur-développer un outil au détriment de la collection"
            },
            "REJUVENATION_BY_PRUNING": {
                "desc": "Le refactoring radical est bénéfique, pas destructif",
                "bio": "Taille radicale → regrowth vigoureux en une saison",
                "violation": "Avoir peur de supprimer/réécrire un outil obsolète"
            },
            "LOW_INVESTMENT_PER_STEM": {
                "desc": "Chaque outil petit, simple, jetable",
                "bio": "Investissement faible par tige, remplacement facile",
                "violation": "Un outil qui prend plus de temps que la somme des autres"
            },
            "SUCKERING_CLONAL_SPREAD": {
                "desc": "Les bons patterns se propagent à travers les outils",
                "bio": "Les rejets créent des colonies clonales",
                "violation": "Chaque outil a ses propres conventions, pas de cohérence"
            }
        },
        "risques": [
            "Ne grandit jamais très haut — pas de produit impressionnant unique",
            "Peut devenir un fouillis sans organisation",
            "Manque de direction claire si pas de curation"
        ],
        "diagnostic_keywords": ["toolkit", "outils", "collection", "scripts", "utils", "prompts", "templates", "indépendant"]
    },

    "liane": {
        "emoji": "🌿",
        "nom": "Liane",
        "forme": "Grimpe sur un hôte",
        "desc": "Utilise l'infrastructure existante. Vitesse > structure.",
        "quand": "Plugin, extension, wrapper d'API, migration legacy",
        "exemples": "Chrome extension, Flutter plugin, API wrapper, legacy migration",
        "regles": {
            "HOST_REQUIRED": {
                "desc": "L'hôte (API, framework, système legacy) doit exister d'abord",
                "bio": "Germination dans l'hôte — pas d'existence autonome initiale",
                "violation": "Développer le plugin avant que l'API hôte soit stable"
            },
            "SPEED_OVER_STRUCTURE": {
                "desc": "Pas d'infrastructure propre nécessaire — investir en vitesse de dev",
                "bio": "Tiges pleines de vasculaire (transport) mais pas de bois dur",
                "violation": "Construire une infrastructure lourde pour un simple wrapper"
            },
            "CLIMBING_STRATEGIES": {
                "desc": "Hooks, callbacks, wrappers — multiples points d'accroche",
                "bio": "Vrilles, épines, racines adventives, poils adhésifs, enroulement",
                "violation": "Un seul point d'accroche fragile"
            },
            "STRANGLER_PATTERN": {
                "desc": "Coexister → progressivement remplacer → l'hôte meurt, la liane est autonome",
                "bio": "Figuier étrangleur : coexistence → enveloppement → remplacement",
                "violation": "Big bang rewrite au lieu de migration progressive"
            },
            "CONTAGION_SPREAD": {
                "desc": "Un plugin peut s'étendre à travers plusieurs plateformes",
                "bio": "Une liane peut s'étendre sur 49+ arbres hôtes",
                "violation": "Limiter le plugin à un seul hôte quand il pourrait s'étendre"
            },
            "FRAGILE_WITHOUT_HOST": {
                "desc": "Si l'hôte tombe, la liane tombe — changement d'API = mort",
                "bio": "Si l'arbre hôte tombe, la liane tombe",
                "violation": "Ignorer les risques de dépendance sur l'hôte (API deprecation, etc.)"
            }
        },
        "risques": [
            "Dépendance totale sur l'hôte — breaking changes = mort",
            "Pas d'autonomie avant la phase finale du strangling",
            "L'hôte peut vous couper l'accès à tout moment"
        ],
        "diagnostic_keywords": ["plugin", "extension", "wrapper", "api", "migration", "legacy", "hook", "addon"]
    }
}

# ============================================================================
# ANATOMIE BIOLOGIQUE — Les 10 niveaux de l'arbre
# ============================================================================

ANATOMY = {
    # ── AU-DESSUS DU SOL ──
    "+5": {
        "zone": "Cime",
        "bio": "Terminal buds / apex",
        "bio_detail": "Bourgeons terminaux, méristèmes apicaux — produisent les auxines qui contrôlent TOUTE la croissance",
        "dev": "Tests, CI/CD, release, docs",
        "dev_detail": "Ce qui se 'reproduit' : déploiement = reproduction de l'arbre",
        "lifespan": "Saisonnier",
        "color_logic": "green si tests pass + CI ok, yellow si partiel, red si absent",
        "paradox": None
    },
    "+4": {
        "zone": "Feuilles",
        "bio": "Foliage / leaves",
        "bio_detail": "5% de la masse totale mais produisent 100% de l'énergie via photosynthèse",
        "dev": "UI, endpoints, outputs visibles",
        "dev_detail": "Ce que l'utilisateur voit et touche — petit en code, 100% de la valeur perçue",
        "lifespan": "Saisonnier",
        "color_logic": "green si UI fonctionnelle, yellow si partielle, red si cassée",
        "paradox": "5% mass → 100% energy. UI = small code → all perceived value."
    },
    "+3": {
        "zone": "Rameaux",
        "bio": "Twigs / branchlets",
        "bio_detail": "Subdivisions des branches, <4 ans. Les plus flexibles, se plient au vent, premiers à casser",
        "dev": "Sous-features, sous-modules, composants",
        "dev_detail": "Flexibles, remplaçables, supportent les outputs directs",
        "lifespan": "1-4 ans",
        "color_logic": "green si implémenté, yellow si WIP, red si manquant et bloquant",
        "paradox": None
    },
    "+2": {
        "zone": "Branches",
        "bio": "Scaffold branches / boughs",
        "bio_detail": "Branches principales 4+ ans. DOIVENT être plus petites que le tronc sinon l'attache casse",
        "dev": "Modules majeurs, features principales",
        "dev_detail": "Structural, long-lived. Si une branche dépasse le tronc → co-dominance risk",
        "lifespan": "Décennies",
        "color_logic": "green si stable, yellow si en dev actif, red si conflit co-dominance",
        "paradox": "Branch MUST be smaller than trunk. Module > core = structural failure."
    },
    "+1": {
        "zone": "Tronc",
        "bio": "Trunk / bole",
        "bio_detail": "Duramen (heartwood) = MORT mais supporte 20 tonnes. Transport bidirectionnel eau↑ sucres↓",
        "dev": "Core engine, pipeline principal",
        "dev_detail": "Tout passe par lui — si le tronc casse, l'arbre meurt",
        "lifespan": "Vie de l'arbre",
        "color_logic": "green si core solide, yellow si dette technique, red si cassé",
        "paradox": "Heartwood is DEAD but supports 20 tons. Legacy code = dead but load-bearing."
    },

    # ── LE SOL ──
    "0": {
        "zone": "● SOL ●",
        "bio": "Root collar / trunk flare",
        "bio_detail": "Anneaux de croissance 2x plus larges. 93% des arbres urbains ont un collet enterré → mort lente",
        "dev": "Interface Sky ↔ Claude",
        "dev_detail": "Le point de communication. Doit être VISIBLE sinon le projet meurt lentement",
        "lifespan": "Permanent",
        "color_logic": "green si interface claire, yellow si ambiguë, red si enterrée/cachée",
        "paradox": "93% of urban trees have buried collars → slow death. Hidden interface = slow project death."
    },

    # ── SOUS LE SOL ──
    "-1": {
        "zone": "Racines structurelles",
        "bio": "Structural / lateral roots",
        "bio_detail": "5-15 racines principales, jusqu'à 30cm diamètre. Spread = 2-4x couronne. 80-90% dans top 60cm",
        "dev": "Frameworks, APIs, contraintes techniques évidentes",
        "dev_detail": "Visible quand on creuse un peu. Structurant, changeable avec effort",
        "lifespan": "Décennies",
        "color_logic": "green si documenté, yellow si implicite, red si inconnu",
        "paradox": None
    },
    "-2": {
        "zone": "Racines pivotantes",
        "bio": "Taproot / sinker roots",
        "bio_detail": "Racines verticales ~2cm depuis les latérales. Stockage eau + énergie. Souvent perdues à maturité",
        "dev": "Décisions d'architecture profondes, choix structurants",
        "dev_detail": "Décisions prises tôt qui ancrent le projet — difficiles à changer",
        "lifespan": "Vie de l'arbre",
        "color_logic": "green si explicite, yellow si implicite, red si contradictoire",
        "paradox": "Often lost at maturity. Early architecture decisions get buried but still anchor."
    },
    "-3": {
        "zone": "Radicelles",
        "bio": "Fine / feeder roots",
        "bio_detail": "≤2mm, non-ligneuses, éphémères (turnover = mois). Absorption directe eau + nutriments",
        "dev": "Contraintes business (budget, deadline, marché, users)",
        "dev_detail": "Changent constamment mais nourrissent tout le projet",
        "lifespan": "Mois",
        "color_logic": "green si alimenté, yellow si stress, red si coupé (plus de budget/users)",
        "paradox": "Ephemeral but feed everything. Business constraints change but nourish the project."
    },
    "-4": {
        "zone": "Poils absorbants",
        "bio": "Root hairs",
        "bio_detail": "Extensions microscopiques de l'épiderme. Cuticule très fine. Filtrent TOUT ce qui entre",
        "dev": "Contraintes légales/réglementaires (GDPR, licences, EN 71, normes)",
        "dev_detail": "Invisibles à l'œil nu mais filtrent tout ce qui peut entrer dans le projet",
        "lifespan": "Jours",
        "color_logic": "green si conforme, yellow si pas vérifié, red si violation",
        "paradox": "Microscopic but filter EVERYTHING entering. Laws are invisible but non-negotiable."
    },
    "-5": {
        "zone": "Mycorhizes",
        "bio": "Mycorrhizae",
        "bio_detail": "Champignons symbiotiques. Amplifient absorption x100. 2500+ espèces. SANS ELLES rien ne pousse",
        "dev": "Lois physiques, mathématiques, contraintes hardware immuables",
        "dev_detail": "Invisibles, symbiotiques. Tu ne les vois pas mais elles amplifient tout x100 quand comprises",
        "lifespan": "Permanent",
        "color_logic": "green si respecté, yellow si testé aux limites, red si violé (impossible)",
        "paradox": "Amplify absorption 100x. Physics laws are not limits — they AMPLIFY when understood."
    }
}

# Ratios biologiques réels
BIO_RATIOS = {
    "root_shoot_weight": {
        "value": "0.25-0.38",
        "meaning": "Racines = 20-28% du poids total",
        "source": "Mokany et al. 2006, Global Change Biology"
    },
    "root_surface_vs_leaf": {
        "value": "2.5-4.5x",
        "meaning": "Surface racinaire = 2.5-4.5x surface foliaire",
        "source": "Perry (1989), ISA Arboriculture"
    },
    "root_spread_vs_crown": {
        "value": "2-4x",
        "meaning": "Spread latéral = 2-4x diamètre couronne (jusqu'à 7x)",
        "source": "Colorado State University, Iowa State"
    },
    "roots_in_top_60cm": {
        "value": "80-90%",
        "meaning": "La plupart des racines sont proches de la surface",
        "source": "Biology Insights 2025, ISA Arboriculture"
    },
    "structural_roots_count": {
        "value": "5-15",
        "meaning": "Nombre de racines structurelles par arbre",
        "source": "ISA Arboriculture (Sutton & Tinus 1983)"
    },
    "mycorrhizae_amplification": {
        "value": "100x",
        "meaning": "Les mycorhizes amplifient la surface d'absorption x100",
        "source": "Perry, cité par ISA Arboriculture"
    },
    "leaves_mass_percent": {
        "value": "5%",
        "meaning": "Les feuilles = 5% de la masse mais produisent 100% de l'énergie",
        "source": "richardstreeservice.com"
    },
    "buried_collar_urban": {
        "value": "93%",
        "meaning": "93% des arbres urbains ont un collet enterré → mort lente",
        "source": "Smiley 1991, Bartlett Tree Research"
    }
}

# Root types par famille d'arbre
FAMILY_ROOT_TYPES = {
    "conifere": {
        "root_type": "Taproot + latérales",
        "depth": "1-10m (pin jusqu'à 3.9m documenté)",
        "spread": "2-3x rayon couronne",
        "rs_ratio": "0.25-0.30",
        "detail": "Racine pivotante profonde, latérales modérées. Moins de biomasse racinaire que feuillus."
    },
    "feuillu": {
        "root_type": "Heart (oblique) + latérales massives",
        "depth": "Chêne jusqu'à 9m",
        "spread": "2-4x rayon couronne",
        "rs_ratio": "0.25-0.38",
        "detail": "Plus de biomasse racinaire totale que conifères. Racines en cœur, très plastiques."
    },
    "palmier": {
        "root_type": "Adventives uniformes",
        "depth": "1-2m (peu profondes)",
        "spread": "Dense mais limité",
        "rs_ratio": "N/A (monocot, pas de croissance secondaire)",
        "detail": "PAS de racine pivotante. Toutes adventives, même diamètre. Diamètre tronc ≠ indicateur racines."
    },
    "baobab": {
        "root_type": "Latérales massives, peu profondes",
        "depth": "Peu profond",
        "spread": "Jusqu'à 50m pour arbre de 14m diamètre",
        "rs_ratio": "0.15-0.20 (tronc tellement massif)",
        "detail": "Les racines vont chercher l'eau très loin horizontalement. Transport interne lent."
    },
    "buisson": {
        "root_type": "Réseau large > partie aérienne",
        "depth": "Peu profond (30-60cm)",
        "spread": "2-3x largeur des tiges",
        "rs_ratio": "0.40-0.68",
        "detail": "Racines PLUS LARGES que partie visible. C'est pourquoi un buisson repousse après taille radicale."
    },
    "liane": {
        "root_type": "Minimales → complètes (progression)",
        "depth": "Variable (dépend de l'hôte)",
        "spread": "Le long du tronc hôte puis au sol",
        "rs_ratio": "Progresse de ~0 à normal",
        "detail": "Racines aériennes d'abord, puis terrestres. Le figuier étrangleur développe un système complet seulement au sol."
    }
}


# ============================================================================
# CLASSIFICATEUR — Diagnostic de famille
# ============================================================================

def classify_interactive():
    """Classification interactive par questions."""
    print("\n" + "=" * 60)
    print("  🌲 WINTER TREE — CLASSIFICATEUR DE PROJET")
    print("=" * 60)

    name = input("\nNom du projet : ").strip()
    if not name:
        print("Nom requis.")
        return None

    desc = input("Description courte : ").strip()

    print("\n--- QUESTIONS DE DIAGNOSTIC ---\n")

    # Q1 : Structure
    print("Q1. La structure du projet est principalement :")
    print("  [1] Un pipeline linéaire (A → B → C → résultat)")
    print("  [2] Des modules en parallèle (composant A + B + C)")
    print("  [3] Un gros moteur avec une petite interface")
    print("  [4] Des outils indépendants (pas de lien fort entre eux)")
    print("  [5] Un plugin/extension pour un système existant")
    q1 = input("Réponse (1-5) : ").strip()

    # Q2 : Output
    print("\nQ2. L'output du projet est :")
    print("  [1] Concentré (un seul résultat riche en bout de pipeline)")
    print("  [2] Distribué (plusieurs features/modules accessibles)")
    print("  [3] Minimal (un oui/non, un fichier, une décision)")
    print("  [4] Multiple (chaque outil produit son propre résultat)")
    q2 = input("Réponse (1-4) : ").strip()

    # Q3 : Dépendances
    print("\nQ3. Les parties du projet sont :")
    print("  [1] Séquentielles (chaque étape dépend de la précédente)")
    print("  [2] Interdépendantes (les modules se parlent)")
    print("  [3] Le core est indépendant, l'interface dépend du core")
    print("  [4] Indépendantes (chaque partie fonctionne seule)")
    print("  [5] Dépendantes d'un système externe (API, framework)")
    q3 = input("Réponse (1-5) : ").strip()

    # Scoring
    scores = {f: 0 for f in FAMILIES}

    # Q1 scoring
    q1_map = {"1": ["conifere", "palmier"], "2": ["feuillu"],
              "3": ["baobab"], "4": ["buisson"], "5": ["liane"]}
    for f in q1_map.get(q1, []):
        scores[f] += 3

    # Q2 scoring
    q2_map = {"1": ["palmier", "conifere"], "2": ["feuillu"],
              "3": ["baobab"], "4": ["buisson"]}
    for f in q2_map.get(q2, []):
        scores[f] += 2

    # Q3 scoring
    q3_map = {"1": ["conifere", "palmier"], "2": ["feuillu"],
              "3": ["baobab"], "4": ["buisson"], "5": ["liane"]}
    for f in q3_map.get(q3, []):
        scores[f] += 2

    # Keyword bonus from description
    desc_lower = desc.lower()
    for fam_id, fam in FAMILIES.items():
        for kw in fam["diagnostic_keywords"]:
            if kw.lower() in desc_lower:
                scores[fam_id] += 1

    # Trier par score
    ranked = sorted(scores.items(), key=lambda x: x[-1], reverse=True)
    winner_id = ranked[0][0]
    winner = FAMILIES[winner_id]

    print("\n" + "=" * 60)
    print(f"  DIAGNOSTIC : {winner['emoji']} {winner['nom'].upper()}")
    print("=" * 60)
    print(f"\n  {winner['desc']}")
    print(f"  Quand l'utiliser : {winner['quand']}")
    print(f"\n  Scores : ", end="")
    for fam_id, score in ranked:
        f = FAMILIES[fam_id]
        print(f"{f['emoji']}{score} ", end="")
    print()

    return {"name": name, "desc": desc, "family": winner_id}


def classify_auto(name, desc, structure, output, deps):
    """Classification automatique (pour usage par Claude ou script).

    Args:
        name: nom du projet
        desc: description courte
        structure: 'pipeline' | 'parallel' | 'engine' | 'tools' | 'plugin'
        output: 'concentrated' | 'distributed' | 'minimal' | 'multiple'
        deps: 'sequential' | 'interdependent' | 'core-interface' | 'independent' | 'external'
    """
    scores = {f: 0 for f in FAMILIES}

    struct_map = {
        "pipeline": ["conifere", "palmier"],
        "parallel": ["feuillu"],
        "engine": ["baobab"],
        "tools": ["buisson"],
        "plugin": ["liane"]
    }
    for f in struct_map.get(structure, []):
        scores[f] += 3

    output_map = {
        "concentrated": ["palmier", "conifere"],
        "distributed": ["feuillu"],
        "minimal": ["baobab"],
        "multiple": ["buisson"]
    }
    for f in output_map.get(output, []):
        scores[f] += 2

    deps_map = {
        "sequential": ["conifere", "palmier"],
        "interdependent": ["feuillu"],
        "core-interface": ["baobab"],
        "independent": ["buisson"],
        "external": ["liane"]
    }
    for f in deps_map.get(deps, []):
        scores[f] += 2

    desc_lower = desc.lower()
    for fam_id, fam in FAMILIES.items():
        for kw in fam["diagnostic_keywords"]:
            if kw.lower() in desc_lower:
                scores[fam_id] += 1

    ranked = sorted(scores.items(), key=lambda x: x[-1], reverse=True)
    return {"name": name, "desc": desc, "family": ranked[0][0], "scores": dict(ranked)}


# ============================================================================
# GÉNÉRATEUR DE TEMPLATE
# ============================================================================

def generate_template(project_info):
    """Génère un Winter Tree template v2 pré-rempli."""
    name = project_info["name"]
    family_id = project_info["family"]
    desc = project_info.get("desc", "")
    fam = FAMILIES[family_id]
    now = datetime.now().strftime("%Y-%m-%d")

    # Build growth rules section
    rules_text = ""
    for rule_id, rule in fam["regles"].items():
        rules_text += f"### {rule_id}\n"
        rules_text += f"- **Règle :** {rule['desc']}\n"
        rules_text += f"- **Bio :** {rule['bio']}\n"
        rules_text += f"- **Violation :** {rule['violation']}\n\n"

    # Build risks section
    risks_text = "\n".join(f"- {r}" for r in fam["risques"])

    template = f"""# {fam['emoji']} {name.upper()} — ARBRE HIVER v2

## METADATA
```yaml
project: "{name}"
family: {family_id}
forme: "{fam['forme']}"
desc: "{desc}"
last_updated: "{now}"
```

## (1) TREE_SILHOUETTE

```
          ☆  Cime (tests, CI, packaging, docs)
         /|\\
        / | \\  Branches (modules, features)
       /  |  \\
      /   |   \\
─────/────|────\\───── ← LE SOL = interface Sky ↔ Claude
     \\    |    /
      \\   |   /  Tronc (moteur principal, core)
       \\  |  /
        \\ | /
         \\|/
          ▼  Racines (contraintes fondamentales)
```

> TODO: Personnaliser l'arbre avec les vrais noms de modules.
> Max 9 branches, noms sur les nœuds, max 110 chars de large.

## (2) NODE_REGISTRY

```yaml
# ── RACINES (contraintes fondamentales) ──
- id: R1
  label: "[contrainte #1]"
  level: R
  parent: null
  status: todo
  entry: "fichier.py: fonction() L???"
  depends: []
  desc: "[à remplir]"

# ── TRONC (moteur principal) ──
- id: T1
  label: "[module core]"
  level: T
  parent: R1
  status: todo
  entry: "main.py: __init__() L???"
  depends: [R1]
  desc: "[à remplir]"

# ── BRANCHES (features, modules) ──
- id: B1
  label: "[feature #1]"
  level: B
  parent: T1
  status: todo
  entry: "module.py: func() L???"
  depends: [T1]
  desc: "[à remplir]"

# ── CIME (tests, packaging, docs) ──
- id: C1
  label: "Tests"
  level: C
  parent: T1
  status: todo
  entry: "test_main.py: test_suite() L1"
  depends: [B1]
  desc: "Suite de tests"
```

## (3) GROWTH RULES — Famille : {fam['emoji']} {fam['nom']}

{fam['desc']}

{rules_text}
## (4) RISQUES STRUCTURELS

{risks_text}

## (5) QUICK SUMMARY

```
Ce projet est surtout un ─── {desc if desc else '[à remplir]'}
Sa famille d'arbre est ─── {fam['emoji']} {fam['nom']} ({fam['forme']})
Le tronc est ─────────── [fichier principal + ce qu'il fait]
Les branches dominantes ─ [les 2-3 modules les plus importants]
La contrainte racine la plus forte est ─ [la contrainte #1]
Le risque structurel principal est ─── {fam['risques'][0]}
```

## QUALITY CHECK

```
[ ] Famille identifiée et justifiée
[ ] Arbre BAS→HAUT, un tronc, max 110 chars de large
[ ] NODE_REGISTRY contient TOUS les IDs du dessin
[ ] Chaque nœud a : id, label, level, parent, status, entry, depends, desc
[ ] GROWTH RULES copiées depuis {family_id}
[ ] QUICK SUMMARY rempli
```

## RAPPEL

- **Sky monte** : il regarde status → voit le progrès
- **Claude descend** : il regarde entry → plonge dans le code
- **depends** : les deux savent ce qui bloque quoi
- **Les racines sont toujours plus grandes que l'arbre**
"""
    return template


# ============================================================================
# VALIDATEUR DE CROISSANCE
# ============================================================================

def validate_growth(project_info, nodes):
    """Valide la croissance d'un projet selon les règles de sa famille.

    Args:
        project_info: dict avec au minimum 'family'
        nodes: liste de dicts avec au minimum 'id', 'level', 'status', 'depends'

    Returns:
        Liste de warnings/violations
    """
    family_id = project_info["family"]
    fam = FAMILIES[family_id]
    warnings = []

    # Compter les nœuds par niveau
    levels = {"R": [], "T": [], "B": [], "C": []}
    for node in nodes:
        level = node.get("level", "?")
        if level in levels:
            levels[level].append(node)

    done_count = sum(1 for n in nodes if n.get("status") == "done")
    total_count = len(nodes)
    wip_count = sum(1 for n in nodes if n.get("status") == "wip")

    # --- Règles universelles ---
    if not levels["R"]:
        warnings.append("⚠️  CRITIQUE : Aucune racine (contrainte) définie. Les racines sont TOUJOURS plus grandes que l'arbre.")

    if not levels["T"]:
        warnings.append("⚠️  CRITIQUE : Aucun tronc (core) défini.")

    if len(levels["B"]) > 9:
        warnings.append(f"⚠️  Trop de branches ({len(levels['B'])}). Max recommandé : 9.")

    # Vérifier les dépendances
    all_ids = {n["id"] for n in nodes}
    for node in nodes:
        for dep in node.get("depends", []):
            if dep not in all_ids:
                warnings.append(f"⚠️  Nœud {node['id']} dépend de {dep} qui n'existe pas.")

    # Vérifier status cohérence : un nœud 'done' dont les dépendances ne sont pas 'done'
    status_map = {n["id"]: n.get("status", "todo") for n in nodes}
    for node in nodes:
        if node.get("status") == "done":
            for dep in node.get("depends", []):
                if status_map.get(dep) != "done":
                    warnings.append(f"⚠️  {node['id']} est 'done' mais sa dépendance {dep} est '{status_map.get(dep, '?')}'.")

    # --- Règles spécifiques par famille ---

    if family_id == "conifere":
        # TRUNK_FIRST : les branches ne devraient pas être 'done' si le tronc n'est pas 'done'
        trunk_done = all(n.get("status") == "done" for n in levels["T"])
        branch_done = any(n.get("status") == "done" for n in levels["B"])
        if branch_done and not trunk_done:
            warnings.append("🌲 VIOLATION TRUNK_FIRST : Des branches sont terminées mais le tronc n'est pas fini.")

        # BRANCH_SUBORDINATION : alerter si plus de branches que de tronc
        if len(levels["B"]) > 2 * len(levels["T"]) and len(levels["T"]) > 0:
            warnings.append("🌲 ATTENTION BRANCH_SUBORDINATION : Beaucoup de branches pour peu de tronc.")

    elif family_id == "feuillu":
        # CO_DOMINANCE_RISK : deux branches WIP de même profondeur
        wip_branches = [n for n in levels["B"] if n.get("status") == "wip"]
        if len(wip_branches) >= 2:
            warnings.append("🍁 ATTENTION CO_DOMINANCE_RISK : Plusieurs branches en développement simultané. Risque de conflit.")

        # SEASONAL_CYCLE : alerter si tout est WIP et rien n'est done
        if wip_count > 3 and done_count == 0:
            warnings.append("🍁 ATTENTION SEASONAL_CYCLE : Beaucoup de WIP, rien de terminé. Penser à shipper.")

    elif family_id == "palmier":
        # SINGLE_MERISTEM : il ne devrait y avoir qu'UN seul tronc
        if len(levels["T"]) > 1:
            warnings.append("🌴 VIOLATION SINGLE_MERISTEM : Plusieurs troncs détectés. Le palmier n'a qu'un seul méristème.")

        # NO_LATERAL_BRANCHING : alerter si des branches existent
        if len(levels["B"]) > 2:
            warnings.append("🌴 ATTENTION NO_LATERAL_BRANCHING : Trop de branches pour un palmier. Le pipeline devrait être linéaire.")

    elif family_id == "baobab":
        # CONSOLIDATE_BEFORE_EXPAND : branches avant que le tronc soit solide
        trunk_done = all(n.get("status") == "done" for n in levels["T"])
        branch_wip = any(n.get("status") in ("wip", "done") for n in levels["B"])
        if branch_wip and not trunk_done:
            warnings.append("🌳 VIOLATION CONSOLIDATE_BEFORE_EXPAND : Branches en cours mais le core n'est pas consolidé.")

        # TRUNK_IS_STORAGE : le tronc devrait être plus gros que les branches
        if len(levels["B"]) > len(levels["T"]) * 3:
            warnings.append("🌳 ATTENTION TRUNK_IS_STORAGE : L'interface (branches) semble plus grande que le core (tronc).")

    elif family_id == "buisson":
        # NO_CENTRAL_TRUNK : il ne devrait PAS y avoir de tronc dominant
        if len(levels["T"]) > 1:
            pass  # normal pour un buisson
        if len(levels["T"]) == 1 and len(levels["B"]) < 3:
            warnings.append("🌿 ATTENTION NO_CENTRAL_TRUNK : Un buisson devrait avoir plusieurs tiges indépendantes, pas un tronc dominant.")

        # LOW_INVESTMENT_PER_STEM : alerter si une branche a trop de dépendances
        for node in levels["B"]:
            deps = node.get("depends", [])
            if len(deps) > 3:
                warnings.append(f"🌿 ATTENTION LOW_INVESTMENT_PER_STEM : {node['id']} a {len(deps)} dépendances. Garder chaque outil simple.")

    elif family_id == "liane":
        # HOST_REQUIRED : vérifier qu'il y a une racine de type "hôte"
        has_host = any("host" in n.get("label", "").lower() or "api" in n.get("label", "").lower()
                      or "hôte" in n.get("label", "").lower() for n in levels["R"])
        if not has_host:
            warnings.append("🌿 ATTENTION HOST_REQUIRED : Aucune racine de type 'hôte' ou 'API' détectée. La liane a besoin d'un hôte.")

    # --- Résumé ---
    if not warnings:
        warnings.append(f"✅ Aucune violation détectée pour {fam['emoji']} {fam['nom']}. L'arbre pousse sainement.")

    return warnings


# ============================================================================
# EXPORT — JSON pour interop
# ============================================================================

def display_anatomy(family_id=None):
    """Affiche l'anatomie biologique des 10 niveaux avec couleurs."""
    print("\n" + "=" * 80)
    print("  🌳 ANATOMIE BIOLOGIQUE — LES 10 NIVEAUX DE L'ARBRE")
    print("=" * 80)

    levels_order = ["+5", "+4", "+3", "+2", "+1", "0", "-1", "-2", "-3", "-4", "-5"]

    for lvl in levels_order:
        a = ANATOMY[lvl]
        if lvl == "0":
            print("─" * 80)
            print(f"  {'●':>4} {a['zone']:.<28s} {a['bio']:<28s} {a['dev']}")
            print("─" * 80)
        else:
            marker = "▲" if int(lvl) > 0 else "▼"
            print(f"  {lvl:>4} {marker} {a['zone']:.<26s} {a['bio']:<28s} {a['dev']}")

    if family_id and family_id in FAMILY_ROOT_TYPES:
        frt = FAMILY_ROOT_TYPES[family_id]
        fam = FAMILIES[family_id]
        print(f"\n  Famille : {fam['emoji']} {fam['nom']}")
        print(f"  Type racines : {frt['root_type']}")
        print(f"  Profondeur : {frt['depth']}")
        print(f"  Spread : {frt['spread']}")
        print(f"  Ratio R:S : {frt['rs_ratio']}")

    print(f"\n  📊 RATIOS BIOLOGIQUES")
    print(f"  Surface racinaire = {BIO_RATIOS['root_surface_vs_leaf']['value']} surface foliaire")
    print(f"  Spread racines = {BIO_RATIOS['root_spread_vs_crown']['value']} diamètre couronne")
    print(f"  {BIO_RATIOS['roots_in_top_60cm']['value']} des racines dans les premiers 60cm")
    print(f"  Mycorhizes amplifient absorption {BIO_RATIOS['mycorrhizae_amplification']['value']}")


def detect_gaps(nodes, family_id):
    """Détecte les trous dans l'arbre — niveaux manquants, racines absentes.

    Returns list of gap descriptions with severity (red/yellow/green).
    """
    gaps = []
    fam = FAMILIES.get(family_id, {})

    # Mapper les nœuds aux niveaux biologiques
    level_map = {
        "C": "+5",   # Cime = tests/CI
        "F": "+4",   # Feuilles = UI/outputs
        "b": "+3",   # Rameaux = sous-features
        "B": "+2",   # Branches = modules
        "T": "+1",   # Tronc = core
        "R": "-1",   # Racines structurelles par défaut
    }

    # Compter les nœuds par niveau projet
    node_levels = {"C": [], "F": [], "b": [], "B": [], "T": [], "R": []}
    for node in nodes:
        level = node.get("level", "?")
        if level in node_levels:
            node_levels[level].append(node)

    # Compter les racines par profondeur (utiliser le label ou un champ 'depth')
    root_depths = {"-1": 0, "-2": 0, "-3": 0, "-4": 0, "-5": 0}
    for node in nodes:
        if node.get("level") == "R":
            depth = node.get("depth", "-1")
            if depth in root_depths:
                root_depths[depth] += 1
            else:
                root_depths["-1"] += 1  # default

    # ── GAPS AU-DESSUS DU SOL ──

    # +5 Cime : tests/CI manquants
    if not node_levels["C"]:
        gaps.append({
            "level": "+5",
            "zone": "Cime",
            "severity": "red",
            "msg": "AUCUN test/CI/release défini. L'arbre ne peut pas se reproduire (déployer).",
            "action": "Ajouter des nœuds de niveau C (tests, CI pipeline, docs)"
        })

    # +4 Feuilles : pas de nœud UI/output
    if not node_levels["F"]:
        # Pas critique pour tous les projets (moteur sans UI)
        if family_id not in ("baobab",):
            gaps.append({
                "level": "+4",
                "zone": "Feuilles",
                "severity": "yellow",
                "msg": "Aucun output/UI défini. L'arbre ne fait pas de photosynthèse (pas de valeur visible).",
                "action": "Définir les outputs visibles du projet (UI, API endpoints, fichiers générés)"
            })

    # +2 Branches : vérifier le nombre
    if len(node_levels["B"]) > 9:
        gaps.append({
            "level": "+2",
            "zone": "Branches",
            "severity": "yellow",
            "msg": f"{len(node_levels['B'])} branches. Trop dense — difficulté de maintenance.",
            "action": "Regrouper les modules ou créer des sous-niveaux (+3 rameaux)"
        })

    # +1 Tronc : manquant
    if not node_levels["T"] and family_id != "buisson":
        gaps.append({
            "level": "+1",
            "zone": "Tronc",
            "severity": "red",
            "msg": "AUCUN core/tronc défini. L'arbre n'a pas de structure porteuse.",
            "action": "Définir le module central (main.py, core engine, pipeline)"
        })

    # ── LE SOL ──
    # Vérifier si l'interface est documentée
    has_interface = any(
        "interface" in n.get("label", "").lower() or
        "sol" in n.get("label", "").lower() or
        "api" in n.get("label", "").lower()
        for n in nodes
    )
    if not has_interface:
        gaps.append({
            "level": "0",
            "zone": "SOL",
            "severity": "yellow",
            "msg": "Interface (collet racinaire) pas explicitement définie. 93% des projets meurent d'interfaces enterrées.",
            "action": "Documenter explicitement le point d'interaction Sky ↔ Claude"
        })

    # ── GAPS SOUS LE SOL ──

    if not node_levels["R"]:
        gaps.append({
            "level": "-1",
            "zone": "Racines structurelles",
            "severity": "red",
            "msg": "AUCUNE racine/contrainte définie. L'arbre n'est pas ancré.",
            "action": "Identifier les contraintes fondamentales (frameworks, APIs, limites techniques)"
        })
    else:
        # Vérifier la couverture des 5 niveaux de racines
        root_labels = " ".join(n.get("label", "").lower() for n in node_levels["R"])

        # -3 Business
        biz_keywords = ["budget", "deadline", "marché", "market", "user", "client", "revenue", "cost"]
        has_business = any(kw in root_labels for kw in biz_keywords)
        if not has_business:
            gaps.append({
                "level": "-3",
                "zone": "Radicelles",
                "severity": "yellow",
                "msg": "Aucune contrainte business identifiée (budget, deadline, marché, users).",
                "action": "Définir les contraintes business qui alimentent le projet"
            })

        # -4 Legal
        legal_keywords = ["gdpr", "licence", "license", "legal", "norme", "standard", "en 71",
                         "rgpd", "copyright", "compliance", "regulation"]
        has_legal = any(kw in root_labels for kw in legal_keywords)
        if not has_legal:
            gaps.append({
                "level": "-4",
                "zone": "Poils absorbants",
                "severity": "yellow",
                "msg": "Aucune contrainte légale/réglementaire identifiée.",
                "action": "Vérifier GDPR, licences, normes applicables au projet"
            })

        # -5 Physics
        phys_keywords = ["physique", "physics", "hardware", "math", "limite", "fdm", "pla",
                        "bandwidth", "latency", "memory", "cpu", "gpu"]
        has_physics = any(kw in root_labels for kw in phys_keywords)
        if not has_physics and family_id in ("baobab", "conifere", "palmier"):
            gaps.append({
                "level": "-5",
                "zone": "Mycorhizes",
                "severity": "yellow",
                "msg": "Aucune contrainte physique/hardware identifiée pour un projet technique.",
                "action": "Identifier les limites physiques (mémoire, CPU, tolérance FDM, etc.)"
            })

    return gaps


def print_gap_report(gaps):
    """Affiche le rapport de gaps avec couleurs."""
    if not gaps:
        print("  ✅ Aucun trou détecté. L'arbre est complet.")
        return

    severity_icons = {"red": "🔴", "yellow": "🟡", "green": "🟢"}

    print(f"\n{'=' * 70}")
    print(f"  🔍 RAPPORT DE GAPS — {len(gaps)} trou(s) détecté(s)")
    print(f"{'=' * 70}")

    reds = [g for g in gaps if g["severity"] == "red"]
    yellows = [g for g in gaps if g["severity"] == "yellow"]

    if reds:
        print(f"\n  🔴 CRITIQUES ({len(reds)})")
        for g in reds:
            print(f"    [{g['level']:>3}] {g['zone']}: {g['msg']}")
            print(f"         → {g['action']}")

    if yellows:
        print(f"\n  🟡 ATTENTION ({len(yellows)})")
        for g in yellows:
            print(f"    [{g['level']:>3}] {g['zone']}: {g['msg']}")
            print(f"         → {g['action']}")

    # Résumé visuel
    print(f"\n  COUVERTURE :")
    levels_order = ["+5", "+4", "+3", "+2", "+1", "0", "-1", "-2", "-3", "-4", "-5"]
    gap_levels = {g["level"] for g in gaps}
    for lvl in levels_order:
        a = ANATOMY[lvl]
        if lvl in gap_levels:
            sev = next(g["severity"] for g in gaps if g["level"] == lvl)
            icon = severity_icons[sev]
        else:
            icon = "🟢"
        print(f"    {icon} [{lvl:>3}] {a['zone']}")


def export_knowledge_base(filepath="winter_tree_kb.json"):
    """Exporte toute la knowledge base en JSON."""
    data = {
        "version": "1.1",
        "date": datetime.now().isoformat(),
        "source": "Winter Tree Engine",
        "references": {
            "lindenmayer_1968": {
                "author": "Aristid Lindenmayer",
                "year": 1968,
                "title": "Mathematical models for cellular interactions in development",
                "journal": "Journal of Theoretical Biology",
                "volume": 18,
                "pages": "280-315",
                "concept": "L-Systems — parallel string rewriting for plant growth"
            },
            "prusinkiewicz_1990": {
                "authors": ["Przemyslaw Prusinkiewicz", "Aristid Lindenmayer"],
                "year": 1990,
                "title": "The Algorithmic Beauty of Plants",
                "publisher": "Springer",
                "concept": "Turtle graphics interpretation of L-systems"
            },
            "tomer_schach_2000": {
                "authors": ["Amir Tomer", "Stephen R. Schach"],
                "year": 2000,
                "title": "The Evolution Tree: A Maintenance-Oriented Software Development Model",
                "venue": "CSMR 2000, Zurich",
                "concept": "Software development as tree of engineering decisions"
            },
            "fowler_2004": {
                "author": "Martin Fowler",
                "year": 2004,
                "title": "Strangler Fig Application",
                "url": "https://martinfowler.com/bliki/StranglerFigApplication.html",
                "concept": "Gradual legacy system replacement inspired by strangler figs"
            },
            "barnes_2013": {
                "author": "Jeffrey M. Barnes",
                "year": 2013,
                "title": "Software Architecture Evolution",
                "institution": "Carnegie Mellon University",
                "ref": "CMU-ISR-13-118",
                "concept": "Evolution paths as graph of architectural states"
            }
        },
        "families": FAMILIES,
        "anatomy": ANATOMY,
        "bio_ratios": BIO_RATIOS,
        "family_root_types": FAMILY_ROOT_TYPES
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return filepath


# ============================================================================
# CLI — Interface en ligne de commande
# ============================================================================

def print_family(family_id):
    """Affiche les détails d'une famille."""
    fam = FAMILIES[family_id]
    print(f"\n{fam['emoji']} {fam['nom'].upper()} — {fam['forme']}")
    print(f"{'=' * 50}")
    print(f"\n{fam['desc']}")
    print(f"\nQuand l'utiliser : {fam['quand']}")
    print(f"Exemples : {fam['exemples']}")
    print(f"\n--- RÈGLES DE CROISSANCE ---")
    for rule_id, rule in fam["regles"].items():
        print(f"\n  {rule_id}")
        print(f"    Règle : {rule['desc']}")
        print(f"    Bio   : {rule['bio']}")
        print(f"    ⚠️     : {rule['violation']}")
    print(f"\n--- RISQUES ---")
    for r in fam["risques"]:
        print(f"  - {r}")


def print_all_families():
    """Affiche un résumé de toutes les familles."""
    print("\n" + "=" * 60)
    print("  🌲 LES 6 FAMILLES D'ARBRES")
    print("=" * 60)
    for fid, fam in FAMILIES.items():
        print(f"\n  {fam['emoji']} {fam['nom']:10s} | {fam['forme']:20s} | {fam['quand']}")


def main():
    """Point d'entrée CLI."""
    if len(sys.argv) < 2:
        print("""
🌲 WINTER TREE ENGINE v1.1
==========================

Usage:
  python engine.py classify          Classification interactive d'un projet
  python engine.py families          Liste toutes les familles
  python engine.py family <id>       Détails d'une famille
  python engine.py anatomy [id]      Anatomie biologique 10 niveaux [+ famille]
  python engine.py gaps <id>         Détecte les trous (demo avec nœuds exemple)
  python engine.py generate <id>     Génère un template pour une famille
  python engine.py export            Exporte la knowledge base en JSON
  python engine.py validate          Validation (TODO: input YAML)

Familles: conifere, feuillu, palmier, baobab, buisson, liane

Exemples:
  python engine.py anatomy baobab
  python engine.py gaps feuillu
  python engine.py generate conifere > mon_projet.md
""")
        return

    cmd = sys.argv[1].lower()

    if cmd == "classify":
        result = classify_interactive()
        if result:
            print(f"\n--- RÉSULTAT ---")
            print(f"Projet : {result['name']}")
            print(f"Famille : {FAMILIES[result['family']]['emoji']} {result['family']}")

            save = input("\nGénérer le template ? (o/n) : ").strip().lower()
            if save == "o":
                template = generate_template(result)
                filename = f"winter-trees/{result['name'].lower().replace(' ', '-')}_tree.md"
                os.makedirs("winter-trees", exist_ok=True)
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(template)
                print(f"\n✅ Template sauvé : {filename}")

    elif cmd == "families":
        print_all_families()

    elif cmd == "family":
        if len(sys.argv) < 3:
            print("Usage: python engine.py family <id>")
            print(f"IDs disponibles : {', '.join(FAMILIES.keys())}")
            return
        fid = sys.argv[2].lower()
        if fid in FAMILIES:
            print_family(fid)
        else:
            print(f"Famille inconnue : {fid}")
            print(f"IDs disponibles : {', '.join(FAMILIES.keys())}")

    elif cmd == "anatomy":
        fid = sys.argv[2].lower() if len(sys.argv) > 2 else None
        if fid and fid not in FAMILIES:
            print(f"Famille inconnue : {fid}")
            print(f"IDs disponibles : {', '.join(FAMILIES.keys())}")
            return
        display_anatomy(fid)

    elif cmd == "gaps":
        if len(sys.argv) < 3:
            print("Usage: python engine.py gaps <family_id>")
            print("Démonstration avec des nœuds exemples.")
            return
        fid = sys.argv[2].lower()
        if fid not in FAMILIES:
            print(f"Famille inconnue : {fid}")
            return

        # Demo : nœuds minimaux pour montrer la détection de gaps
        demo_nodes = [
            {"id": "T1", "level": "T", "status": "wip", "depends": [], "label": "Core engine"},
            {"id": "B1", "level": "B", "status": "wip", "depends": ["T1"], "label": "Module A"},
            {"id": "B2", "level": "B", "status": "todo", "depends": ["T1"], "label": "Module B"},
            {"id": "R1", "level": "R", "status": "done", "depends": [], "label": "Python 3.12"},
        ]
        fam = FAMILIES[fid]
        print(f"\n  Analyse gaps pour {fam['emoji']} {fam['nom']} (nœuds demo)")
        gaps = detect_gaps(demo_nodes, fid)
        print_gap_report(gaps)

    elif cmd == "generate":
        if len(sys.argv) < 3:
            print("Usage: python engine.py generate <family_id> [nom_projet]")
            return
        fid = sys.argv[2].lower()
        name = sys.argv[3] if len(sys.argv) > 3 else "Mon Projet"
        if fid in FAMILIES:
            template = generate_template({"name": name, "family": fid, "desc": ""})
            print(template)
        else:
            print(f"Famille inconnue : {fid}")

    elif cmd == "export":
        path = export_knowledge_base()
        print(f"✅ Knowledge base exportée : {path}")

    elif cmd == "validate":
        print("TODO: Implémenter la lecture de fichiers YAML pour validation.")
        print("En attendant, utiliser validate_growth() en Python directement.")

    else:
        print(f"Commande inconnue : {cmd}")
        print("Utiliser 'python engine.py' sans arguments pour l'aide.")


if __name__ == "__main__":
    main()
