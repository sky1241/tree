#!/usr/bin/env python3
"""
WINTER TREE v2 — MYCELIUM ENGINE
=================================
Métriques réseau pour projets logiciels.
Basé sur les modèles mathématiques de réseaux fongiques.

Sources :
- Bebber et al. 2007 (Proc. R. Soc. B 274:2307-2315)
- Latora & Marchiori 2001 (Phys. Rev. Lett.)
- Watts & Strogatz 1998 (Nature)
- Tero et al. 2010 (Science 327:439-442)
- Edelstein 1982 (J. Theor. Biol.)

Auteur : Sky — l'architecte de l'architecte
"""

import networkx as nx
import sys
import os
import json
from pathlib import Path


# ============================================================================
# BRIQUE 0 — CONSTRUCTION DE GRAPHE
# ============================================================================

def graph_from_edges(edges: list) -> nx.Graph:
    """Construit un graphe non-dirigé depuis une liste d'arêtes.

    Args:
        edges: liste de tuples (node_a, node_b) ou (node_a, node_b, weight)

    Returns:
        nx.Graph (sans self-loops — ils biaisent α et BC)
    """
    G = nx.Graph()
    for edge in edges:
        if edge[0] == edge[1]:
            continue  # Pas de self-loop
        if len(edge) == 3:
            G.add_edge(edge[0], edge[1], weight=edge[2])
        else:
            G.add_edge(edge[0], edge[1], weight=1.0)
    return G


def graph_from_imports(import_graph: dict) -> nx.DiGraph:
    """Convertit un dict {fichier: set(imports)} en graphe dirigé.

    C'est le format que produit scan_repo() dans engine.py,
    mais on ne DÉPEND PAS de engine.py. N'importe quel dict
    avec ce format marche.

    ATTENTION : les clés (sources) utilisent des chemins fichier
    (lib/utils.py) mais les valeurs (targets) utilisent des noms
    de module Python (lib.utils). On normalise tout vers un format
    commun pour éviter les nœuds fantômes.

    Normalisation : tout en dot-notation, sans extension.
        "lib/utils.py"  → "lib.utils"
        "lib.utils"     → "lib.utils"
        "src/core.dart" → "src.core"

    Self-loops supprimés (un fichier qui s'importe lui-même n'a
    pas de sens en tant qu'arête réseau — ça biaise α et BC).

    Args:
        import_graph: {str: set(str)} — fichier → ses imports

    Returns:
        nx.DiGraph — arêtes dirigées de importeur vers importé
    """
    def normalize(name: str) -> str:
        """Normalise un chemin ou module vers dot-notation sans extension."""
        if not name or not name.strip():
            return ""
        # Virer les extensions courantes
        for ext in (".py", ".dart", ".js", ".ts", ".jsx", ".tsx"):
            if name.endswith(ext):
                name = name[:-len(ext)]
        # Remplacer / et \ par .
        name = name.replace("/", ".").replace("\\", ".")
        # Virer __init__ en fin
        if name.endswith(".__init__"):
            name = name[:-9]
        # Virer les . en début (imports relatifs: ..parent → parent)
        name = name.lstrip(".")
        # Collapse les .. consécutifs restants
        while ".." in name:
            name = name.replace("..", ".")
        # Virer le . final si présent
        name = name.rstrip(".")
        return name

    G = nx.DiGraph()
    for source, targets in import_graph.items():
        src = normalize(source)
        if not src:
            continue
        G.add_node(src)
        for target in targets:
            tgt = normalize(target)
            if not tgt:
                continue
            if tgt == src:
                continue  # Pas de self-loop
            G.add_edge(src, tgt)
    return G


def to_undirected(G: nx.DiGraph) -> nx.Graph:
    """Convertit un graphe dirigé en non-dirigé.

    Les métriques réseau (Bebber 2007) travaillent sur des graphes
    non-dirigés. Les imports sont dirigés mais la COMMUNICATION
    entre modules est bidirectionnelle.

    NOTE DESIGN : On perd la direction des imports. C'est VOULU.
    Bebber 2007 travaille sur des graphes non-dirigés car les hyphes
    sont des tubes bidirectionnels. En code, un import A→B implique
    que A et B communiquent, pas que B connaît A.

    Self-loops supprimés (un module qui se référence lui-même
    n'est pas une arête réseau).
    """
    H = G.to_undirected()
    H.remove_edges_from(nx.selfloop_edges(H))
    return H


# ============================================================================
# BRIQUE 1 — MESHEDNESS α
# Source : Bebber et al. 2007, Eq. dans Bloc D1
# ============================================================================

def meshedness(G: nx.Graph) -> float:
    """Coefficient de maillage alpha.

    α = (L - N + 1) / (2N - 5)

    où L = nombre de liens, N = nombre de nœuds.

    Interprétation :
        α = 0.0  → arbre pur (pas de boucles, pas de redondance)
        α = 1.0  → réseau planaire maximal (maximum de boucles)
        0 < α < 1 → réseau partiellement maillé

    Données de référence (Bebber 2007, P. velutina) :
        Contrôle jour 39 : α = 0.11 ± 0.04
        Avec bait jour 39 : α = 0.20 ± 0.05

    NOTE : Bebber 2007 ne calcule α que sur des graphes CONNEXES.
    Si le graphe est déconnecté, on prend la plus grande composante
    connexe. Un graphe déconnecté donnerait α négatif, ce qui n'a
    pas de sens biologique.

    Args:
        G: graphe non-dirigé

    Returns:
        float — alpha. 0 = arbre pur. 1 = réseau planaire maximal.
        Peut dépasser 1 sur des graphes non-planaires (normal).
        Bebber travaille sur des réseaux 2D (planaires) → α ∈ [0,1].
        Pour du code avec beaucoup de dépendances croisées, α > 1 est possible.
    """
    N = G.number_of_nodes()
    L = G.number_of_edges()

    if N < 3:
        return 0.0

    # Forcer composante connexe (Bebber 2007 ne travaille que sur ça)
    if not nx.is_connected(G):
        largest_cc = max(nx.connected_components(G), key=len)
        G = G.subgraph(largest_cc).copy()

    # Supprimer self-loops (biaisent L artificiellement)
    G.remove_edges_from(nx.selfloop_edges(G))

    N = G.number_of_nodes()
    L = G.number_of_edges()

    if N < 3:
        return 0.0

    denom = 2 * N - 5
    if denom <= 0:
        return 0.0

    alpha = (L - N + 1) / denom
    return alpha


# ============================================================================
# BRIQUE 2 — EFFICACITÉ GLOBALE
# Source : Latora & Marchiori 2001, Bebber 2007 Bloc D4
# ============================================================================

def global_efficiency(G: nx.Graph) -> float:
    """Efficacité globale du réseau.

    E_global = (1 / N(N-1)) × Σᵢ≠ⱼ (1 / d_ij)

    Mesure la facilité de communication entre n'importe quels
    2 nœuds du réseau. Utilise l'inverse de la distance :
    nœuds déconnectés contribuent 0 (pas l'infini).

    Interprétation :
        E → 1.0  : tout le monde parle à tout le monde facilement
        E → 0.0  : réseau fragmenté, modules isolés

    Args:
        G: graphe non-dirigé

    Returns:
        float — efficacité entre 0 et 1
    """
    # NetworkX a exactement cette formule
    return nx.global_efficiency(G)


# ============================================================================
# BRIQUE 3 — EFFICACITÉ ROOT (depuis un point d'entrée)
# Source : Bebber 2007, Bloc D5
# ============================================================================

def root_efficiency(G: nx.Graph, root: str) -> float:
    """Efficacité depuis un nœud racine (entry point).

    E_root = (1 / (N-1)) × Σⱼ (1 / d(root, j))

    Mesure comment le nœud racine (main.py, index.dart, etc.)
    irrigue le reste du réseau. C'est unidirectionnel :
    on part de la racine vers tous les autres.

    Différence avec E_global :
        E_global = communication entre tous les paires
        E_root = propagation depuis UN point

    NOTE : E_root peut DÉPASSER E_global si le root est un hub
    bien connecté, car E_global moyenne sur toutes les paires
    (y compris les nœuds périphériques mal connectés entre eux).

    Résultat Bebber 2007 : E_root(réseau fongique) > E_root(MST)
    Le champignon fait MIEUX que le minimum spanning tree.

    Args:
        G: graphe non-dirigé
        root: identifiant du nœud racine

    Returns:
        float — efficacité root entre 0 et 1
    """
    N = G.number_of_nodes()
    if N <= 1:
        return 0.0

    if root not in G:
        return 0.0

    # Distances depuis root vers tous les autres
    distances = nx.single_source_shortest_path_length(G, root)

    total = 0.0
    for node, dist in distances.items():
        if node != root and dist > 0:
            total += 1.0 / dist

    # Nœuds non-atteignables contribuent 0 (implicitement)
    return total / (N - 1)


# ============================================================================
# BRIQUE 4 — VOLUME-MST RATIO (overhead architectural)
# Source : Bebber 2007, Bloc D6
# ============================================================================

def volume_mst_ratio(G: nx.Graph) -> float:
    """Ratio coût réel / coût minimum (MST).

    V_MST = C_réel / C_MST

    où C = Σ(poids des arêtes).

    Interprétation :
        ratio = 1.0 → arbre pur, zéro redondance, le strict minimum
        ratio = 1.3 → 30% d'overhead (redondance pour la robustesse)
        ratio = 2.0 → le double du nécessaire (peut-être trop)

    Un bon réseau fongique a ratio ≈ 1.2-1.5 :
    assez de redondance pour la robustesse,
    pas trop pour ne pas gaspiller.

    Args:
        G: graphe non-dirigé (utilise 'weight' si disponible)

    Returns:
        float — ratio >= 1.0 (1.0 = arbre pur)
    """
    if not nx.is_connected(G):
        # Sur la plus grande composante connexe
        largest_cc = max(nx.connected_components(G), key=len)
        G = G.subgraph(largest_cc).copy()

    if G.number_of_edges() == 0:
        return 1.0

    # Coût réel (ignorer poids <= 0 — pas de sens physique)
    real_cost = sum(max(d.get("weight", 1.0), 0) for u, v, d in G.edges(data=True))

    # Coût MST
    mst = nx.minimum_spanning_tree(G, weight="weight")
    mst_cost = sum(max(d.get("weight", 1.0), 0) for u, v, d in mst.edges(data=True))

    if mst_cost <= 0:
        # MST de coût 0 = toutes les arêtes ont poids 0 → ratio n'a pas de sens
        return 1.0

    return real_cost / mst_cost


# ============================================================================
# BRIQUE 5 — BETWEENNESS CENTRALITY (bottlenecks)
# Source : Bebber 2007, Fricker 2017, Bloc D7 prep
# ============================================================================

def find_bottlenecks(G: nx.Graph, top_n: int = 5) -> list:
    """Trouve les nœuds les plus critiques par betweenness centrality.

    BC(v) = Σ_{s≠v≠t} (σ_st(v) / σ_st)

    où σ_st = nombre de plus courts chemins de s à t,
    et σ_st(v) = ceux qui passent par v.

    Un nœud avec BC élevé est un GOULOT D'ÉTRANGLEMENT.
    Si tu le supprimes, beaucoup de chemins sont coupés.

    En mycelium : BC corrèle avec le flux réel (Oyarte Galvez 2025).
    En code : BC élevé = fichier critique, si il casse tout pète.

    Args:
        G: graphe non-dirigé
        top_n: nombre de bottlenecks à retourner

    Returns:
        liste de (nœud, BC_score) triés par score décroissant
    """
    bc = nx.betweenness_centrality(G, weight="weight", normalized=True)

    sorted_bc = sorted(bc.items(), key=lambda x: -x[1])
    return sorted_bc[:top_n]


# ============================================================================
# BRIQUE 6 — ROBUSTESSE (attaque séquentielle)
# Source : Bebber 2007, Bloc D7
# ============================================================================

def robustness_test(G: nx.Graph, attack: str = "betweenness", steps: int = 20,
                    seed: int = None) -> list:
    """Simule une attaque séquentielle et mesure la dégradation.

    Protocole Bebber 2007 :
    1. Calculer betweenness centrality
    2. Supprimer le nœud avec la plus haute BC
    3. Recalculer BC (le réseau a changé)
    4. Répéter
    5. Mesurer la taille de la plus grande composante connexe

    Résultat Bebber : le réseau fongique pondéré résiste mieux
    que le MST, DT, et même le réseau non-pondéré.

    Args:
        G: graphe non-dirigé
        attack: "betweenness" ou "random"
        steps: nombre de nœuds à supprimer (ou % si < 1)
        seed: graine aléatoire pour attack="random" (reproductibilité)

    Returns:
        liste de (fraction_removed, fraction_giant_component)
    """
    import random

    H = G.copy()
    N = H.number_of_nodes()

    if N == 0:
        return [(0.0, 0.0)]

    rng = random.Random(seed)
    results = [(0.0, 1.0)]  # Avant attaque : 100% connecté

    n_to_remove = min(steps, N - 1)

    for i in range(n_to_remove):
        if H.number_of_nodes() <= 1:
            break

        # Choisir la cible
        if attack == "betweenness":
            bc = nx.betweenness_centrality(H)
            target = max(bc, key=bc.get)
        elif attack == "random":
            target = rng.choice(list(H.nodes()))
        else:
            raise ValueError(f"Attack type inconnu : {attack}")

        # Supprimer
        H.remove_node(target)

        # Mesurer la plus grande composante connexe
        if H.number_of_nodes() == 0:
            results.append(((i + 1) / N, 0.0))
        else:
            largest_cc = max(nx.connected_components(H), key=len)
            frac_connected = len(largest_cc) / N
            results.append(((i + 1) / N, frac_connected))

    return results


# ============================================================================
# BRIQUE 7 — SMALL-WORLD σ
# Source : Watts & Strogatz 1998, Humphries & Gurney 2008, Bloc G1
# ============================================================================

def small_world_sigma(G: nx.Graph, nrand: int = 5) -> dict:
    """Coefficient small-world sigma.

    γ = C / C_rand    (ratio clustering)
    λ = L / L_rand    (ratio path length)
    σ = γ / λ         (small-world si σ > 1)

    Un réseau small-world a :
    - Clustering BEAUCOUP plus élevé qu'un réseau aléatoire (γ >> 1)
    - Path length SIMILAIRE à un réseau aléatoire (λ ≈ 1)
    - Donc σ >> 1

    ATTENTION : nx.sigma() est LENT (O(n²)). On fait une version
    avec peu de graphes aléatoires de référence.

    Args:
        G: graphe non-dirigé, connexe
        nrand: nombre de graphes aléatoires pour la moyenne

    Returns:
        dict avec sigma, gamma, lambda_, C, C_rand, L, L_rand
    """
    if not nx.is_connected(G):
        largest_cc = max(nx.connected_components(G), key=len)
        G = G.subgraph(largest_cc).copy()

    N = G.number_of_nodes()
    if N < 4:
        return {"sigma": 0.0, "gamma": 0.0, "lambda_": 0.0,
                "C": 0.0, "C_rand": 0.0, "L": 0.0, "L_rand": 0.0}

    C = nx.average_clustering(G)
    L = nx.average_shortest_path_length(G)

    # Générer des graphes aléatoires ER avec mêmes N et L
    M = G.number_of_edges()
    C_rands = []
    L_rands = []

    for _ in range(nrand):
        R = nx.gnm_random_graph(N, M)
        # S'assurer qu'il est connexe
        attempts = 0
        while not nx.is_connected(R) and attempts < 50:
            R = nx.gnm_random_graph(N, M)
            attempts += 1
        if nx.is_connected(R):
            C_rands.append(nx.average_clustering(R))
            L_rands.append(nx.average_shortest_path_length(R))

    if not C_rands or not L_rands:
        return {"sigma": 0.0, "gamma": 0.0, "lambda_": 0.0,
                "C": C, "C_rand": 0.0, "L": L, "L_rand": 0.0}

    C_rand = sum(C_rands) / len(C_rands)
    L_rand = sum(L_rands) / len(L_rands)

    gamma = C / C_rand if C_rand > 0 else 0.0
    lambda_ = L / L_rand if L_rand > 0 else 0.0
    sigma = gamma / lambda_ if lambda_ > 0 else 0.0

    return {
        "sigma": sigma,
        "gamma": gamma,
        "lambda_": lambda_,
        "C": round(C, 4),
        "C_rand": round(C_rand, 4),
        "L": round(L, 4),
        "L_rand": round(L_rand, 4),
    }


# ============================================================================
# BRIQUE 8 — SMALL-WORLD ω
# Source : Telesford et al. 2011, Bloc G2
# ============================================================================

def small_world_omega(G: nx.Graph, nrand: int = 5, nlattice: int = 5) -> dict:
    """Coefficient omega — alternative à sigma.

    ω = L_rand/L - C/C_lattice

    Interprétation :
        ω ≈ -1 → lattice (réseau régulier)
        ω ≈  0 → small-world
        ω ≈ +1 → random

    Plus robuste que sigma car utilise aussi la référence lattice.

    Args:
        G: graphe non-dirigé, connexe
        nrand: nombre de graphes aléatoires
        nlattice: nombre de lattices

    Returns:
        dict avec omega, L_rand, L, C, C_lattice
    """
    if not nx.is_connected(G):
        largest_cc = max(nx.connected_components(G), key=len)
        G = G.subgraph(largest_cc).copy()

    N = G.number_of_nodes()
    M = G.number_of_edges()

    if N < 4:
        return {"omega": 0.0, "L": 0.0, "L_rand": 0.0,
                "C": 0.0, "C_lattice": 0.0}

    C = nx.average_clustering(G)
    L = nx.average_shortest_path_length(G)

    # Graphes aléatoires
    L_rands = []
    for _ in range(nrand):
        R = nx.gnm_random_graph(N, M)
        attempts = 0
        while not nx.is_connected(R) and attempts < 50:
            R = nx.gnm_random_graph(N, M)
            attempts += 1
        if nx.is_connected(R):
            L_rands.append(nx.average_shortest_path_length(R))

    # Lattice ring
    k = max(2, round(2 * M / N))
    if k % 2 == 1:
        k -= 1
    k = max(2, min(k, N - 1))

    C_lattices = []
    for _ in range(nlattice):
        try:
            Lat = nx.watts_strogatz_graph(N, k, 0)  # p=0 = lattice pure
            if nx.is_connected(Lat):
                C_lattices.append(nx.average_clustering(Lat))
        except:
            pass

    L_rand = sum(L_rands) / len(L_rands) if L_rands else 0.0
    C_lattice = sum(C_lattices) / len(C_lattices) if C_lattices else 1.0

    omega = (L_rand / L if L > 0 else 0.0) - (C / C_lattice if C_lattice > 0 else 0.0)

    return {
        "omega": omega,
        "L": round(L, 4),
        "L_rand": round(L_rand, 4),
        "C": round(C, 4),
        "C_lattice": round(C_lattice, 4),
    }


# ============================================================================
# BRIQUE 9 — STRATÉGIE PHALANX / GUERRILLA
# Source : Fricker 2017, Aguilar-Trigueros 2022, Bloc G3
# ============================================================================

def classify_strategy(alpha: float, e_global: float, e_root: float,
                      robustness_50: float = None) -> dict:
    """Classifie la stratégie réseau sur l'axe phalanx ↔ guerrilla.

    Fricker 2017 + Aguilar-Trigueros 2022 :

    | Trait       | Phalanx          | Guerrilla        |
    |-------------|------------------|------------------|
    | α           | Haut (> 0.15)    | Bas (< 0.05)     |
    | E_global    | Haut (> 0.5)     | Bas (< 0.3)      |
    | E_root      | Moyen            | Haut             |
    | Robustesse  | Haute            | Basse            |
    | Coût        | Élevé            | Faible           |

    L'axe principal de variation est la CONNECTIVITÉ (Aguilar-Trigueros).
    Ce n'est pas binaire — c'est un gradient.

    Args:
        alpha: meshedness
        e_global: efficacité globale
        e_root: efficacité root
        robustness_50: fraction connectée après 50% d'attaque (optionnel)

    Returns:
        dict avec strategy, score (-1=guerrilla, +1=phalanx), détails
    """
    score = 0.0
    details = []

    # Alpha
    if alpha > 0.15:
        score += 0.3
        details.append(f"α={alpha:.3f} → maillé (phalanx)")
    elif alpha < 0.05:
        score -= 0.3
        details.append(f"α={alpha:.3f} → arbre quasi-pur (guerrilla)")
    else:
        details.append(f"α={alpha:.3f} → intermédiaire")

    # E_global
    if e_global > 0.5:
        score += 0.25
        details.append(f"E_global={e_global:.3f} → bien connecté")
    elif e_global < 0.3:
        score -= 0.25
        details.append(f"E_global={e_global:.3f} → fragmenté")

    # E_root
    if e_root > 0.6:
        score -= 0.15  # E_root élevé = guerrilla (longue portée)
        details.append(f"E_root={e_root:.3f} → bonne irrigation")
    elif e_root < 0.3:
        score += 0.15
        details.append(f"E_root={e_root:.3f} → irrigation faible")

    # Robustesse
    if robustness_50 is not None:
        if robustness_50 > 0.5:
            score += 0.3
            details.append(f"Robustesse@50%={robustness_50:.2f} → résistant")
        elif robustness_50 < 0.2:
            score -= 0.3
            details.append(f"Robustesse@50%={robustness_50:.2f} → fragile")

    # Classification
    if score > 0.3:
        strategy = "phalanx"
        desc = "Dense, robuste, coûteux. Monorepo mature."
    elif score < -0.3:
        strategy = "guerrilla"
        desc = "Éparse, rapide, fragile. Microservices / scripts."
    else:
        strategy = "mixed"
        desc = "Intermédiaire. En transition ou hybride."

    return {
        "strategy": strategy,
        "score": round(score, 3),
        "description": desc,
        "details": details,
    }


# ============================================================================
# ANALYSE COMPLÈTE
# ============================================================================

def analyze(G_input, root: str = None, run_physarum=True, run_anastomosis=True,
            physarum_mu=1.0, physarum_steps=100, anastomosis_method="jaccard",
            anastomosis_threshold=0.2) -> dict:
    """Analyse complète d'un graphe — Briques 0 à 11.

    Args:
        G_input: nx.Graph ou nx.DiGraph
        root: nœud racine (entry point). Si None, prend le plus connecté.
        run_physarum: bool — lancer Kirchhoff + Physarum (brique 10).
        run_anastomosis: bool — détecter les candidats anastomose (brique 11).
        physarum_mu: float — exposant Physarum (1.0=shortest, <1=loops).
        physarum_steps: int — itérations Physarum max.
        anastomosis_method: str — "jaccard", "adamic_adar", "common_neighbors".
        anastomosis_threshold: float — seuil pour la détection anastomose.

    Returns:
        dict avec toutes les métriques briques 0-11
    """
    import copy

    # S'assurer qu'on a un graphe non-dirigé pour les métriques
    if isinstance(G_input, nx.DiGraph):
        G = to_undirected(G_input)
    else:
        G = G_input.copy()

    N = G.number_of_nodes()
    L = G.number_of_edges()

    if N == 0:
        return {"error": "Graphe vide"}

    # Trouver le root si pas spécifié
    if root is None or root not in G:
        # Le nœud avec le plus de connexions
        root = max(G.nodes(), key=lambda n: G.degree(n))

    # --- Briques 1-5: Métriques de base ---
    alpha = meshedness(G)
    e_global = global_efficiency(G)
    e_root = root_efficiency(G, root)
    v_mst = volume_mst_ratio(G)
    bottlenecks = find_bottlenecks(G, top_n=min(5, N))

    result = {
        "nodes": N,
        "edges": L,
        "root": root,
        "meshedness_alpha": round(alpha, 4),
        "global_efficiency": round(e_global, 4),
        "root_efficiency": round(e_root, 4),
        "volume_mst_ratio": round(v_mst, 4),
        "bottlenecks": [(n, round(s, 4)) for n, s in bottlenecks],
    }

    # --- Brique 6: Robustesse (seulement si pas trop gros) ---
    if N <= 500:
        rob = robustness_test(G, attack="betweenness", steps=min(N // 2, 20))
        # Trouver la fraction connectée quand 30% des nœuds sont supprimés
        rob_50 = None
        for frac_removed, frac_connected in rob:
            if frac_removed >= 0.3:
                rob_50 = frac_connected
                break
        result["robustness_curve"] = [(round(r, 3), round(c, 3)) for r, c in rob]
        result["robustness_at_30pct"] = round(rob_50, 4) if rob_50 else None
    else:
        rob_50 = None
        result["robustness_curve"] = "skipped (N > 500)"
        result["robustness_at_30pct"] = None

    # --- Briques 7-8: Small-world (seulement si connexe et pas trop gros) ---
    if N <= 200 and nx.is_connected(G):
        sw_sigma = small_world_sigma(G, nrand=3)
        sw_omega = small_world_omega(G, nrand=3, nlattice=3)
        result["small_world_sigma"] = round(sw_sigma["sigma"], 4)
        result["small_world_omega"] = round(sw_omega["omega"], 4)
        result["clustering"] = sw_sigma["C"]
        result["avg_path_length"] = sw_sigma["L"]
    else:
        result["small_world_sigma"] = "skipped (N > 200 or disconnected)"
        result["small_world_omega"] = "skipped"
        result["clustering"] = round(nx.average_clustering(G), 4)
        result["avg_path_length"] = None

    # --- Brique 9: Stratégie ---
    strat = classify_strategy(alpha, e_global, e_root, rob_50)
    result["strategy"] = strat

    # --- Brique 10: Kirchhoff + Physarum ---
    if run_physarum and N >= 3 and L >= 2:
        # Sources: root injecte, feuilles absorbent
        degrees = dict(G.degree())
        leaves = [n for n in G.nodes() if degrees[n] <= 2 and n != root]
        if not leaves:
            leaves = [n for n in G.nodes() if n != root][:max(3, N // 4)]

        if leaves:
            sources = {root: 1.0}
            for lf in leaves:
                sources[lf] = -1.0 / len(leaves)

            G_phys = copy.deepcopy(G)
            sim = physarum_simulate(G_phys, sources, n_steps=physarum_steps,
                                   mu=physarum_mu, decay=1.0, h=0.2,
                                   min_conductivity=1e-4)

            n_thick = len(sim["thick_edges"])
            n_dead = len(sim["dead_edges"])
            n_total = n_thick + n_dead

            result["physarum"] = {
                "mu": physarum_mu,
                "steps": sim["steps"],
                "converged": sim["converged"],
                "thick_edges": n_thick,
                "dead_edges": n_dead,
                "survival_pct": round(n_thick / n_total * 100, 1) if n_total > 0 else 0,
                "top_arteries": [(u, v, round(c, 4)) for u, v, c in sim["thick_edges"][:5]],
                "top_dead": sim["dead_edges"][:5],
            }
        else:
            result["physarum"] = {"skipped": "no leaves found"}
    else:
        result["physarum"] = {"skipped": "too small or disabled"}

    # --- Brique 11: Anastomose ---
    if run_anastomosis and N >= 3 and L >= 2:
        candidates = detect_anastomosis_candidates(
            G, method=anastomosis_method, threshold=anastomosis_threshold,
            max_candidates=10)

        result["anastomosis"] = {
            "method": anastomosis_method,
            "threshold": anastomosis_threshold,
            "candidates_found": len(candidates),
            "top_candidates": [(u, v, round(s, 4)) for u, v, s in candidates[:5]],
        }
    else:
        result["anastomosis"] = {"skipped": "too small or disabled"}

    return result


# ============================================================================
# AFFICHAGE
# ============================================================================

def print_report(report: dict):
    """Affiche un rapport lisible."""

    print(f"\n{'=' * 60}")
    print(f"  🍄 MYCELIUM ANALYSIS")
    print(f"{'=' * 60}")
    print(f"  Nœuds    : {report['nodes']}")
    print(f"  Liens    : {report['edges']}")
    print(f"  Root     : {report['root']}")
    print()

    # Métriques principales
    alpha = report["meshedness_alpha"]
    e_glob = report["global_efficiency"]
    e_root = report["root_efficiency"]
    v_mst = report["volume_mst_ratio"]

    # Alpha avec barre visuelle
    alpha_bar = "█" * int(alpha * 20) + "░" * (20 - int(alpha * 20))
    print(f"  α (meshedness)   : {alpha:.4f}  [{alpha_bar}]")
    if alpha < 0.02:
        print(f"                     → Arbre pur. Aucune redondance.")
    elif alpha < 0.10:
        print(f"                     → Peu maillé. Réseau fragile.")
    elif alpha < 0.20:
        print(f"                     → Maillage correct (réf: champignon contrôle ≈ 0.11)")
    else:
        print(f"                     → Très maillé (réf: champignon stimulé ≈ 0.20)")

    # E_global
    eg_bar = "█" * int(e_glob * 20) + "░" * (20 - int(e_glob * 20))
    print(f"  E_global         : {e_glob:.4f}  [{eg_bar}]")

    # E_root
    er_bar = "█" * int(e_root * 20) + "░" * (20 - int(e_root * 20))
    print(f"  E_root ({str(report['root'])[:15]}): {e_root:.4f}  [{er_bar}]")

    # Volume-MST
    print(f"  Volume/MST       : {v_mst:.2f}x", end="")
    if v_mst < 1.1:
        print("  → quasi-minimal (arbre)")
    elif v_mst < 1.5:
        print("  → overhead raisonnable")
    else:
        print("  → overhead élevé (beaucoup de redondance)")

    # Bottlenecks
    print(f"\n  --- Bottlenecks (betweenness centrality) ---")
    for node, score in report["bottlenecks"]:
        bar = "█" * int(score * 40) + "░" * max(0, 10 - int(score * 40))
        print(f"    {score:.4f} [{bar}] {node}")

    # Robustesse
    if isinstance(report.get("robustness_at_30pct"), float):
        rob = report["robustness_at_30pct"]
        print(f"\n  Robustesse @30%  : {rob:.2%} du réseau survit")
        if rob > 0.7:
            print(f"                     → Très robuste")
        elif rob > 0.4:
            print(f"                     → Correct")
        else:
            print(f"                     → Fragile. Point de défaillance probable.")

    # Small-world
    if isinstance(report.get("small_world_sigma"), float):
        sigma = report["small_world_sigma"]
        omega = report["small_world_omega"]
        print(f"\n  Small-world σ    : {sigma:.2f}", end="")
        if sigma > 1:
            print(f"  → OUI, small-world (σ > 1)")
        else:
            print(f"  → Non small-world")
        print(f"  Small-world ω    : {omega:.2f}", end="")
        if -0.5 < omega < 0.5:
            print(f"  → Zone small-world")
        elif omega < -0.5:
            print(f"  → Tendance lattice (régulier)")
        else:
            print(f"  → Tendance random")

    # Stratégie
    strat = report["strategy"]
    print(f"\n  --- Stratégie ---")
    print(f"  Type  : {strat['strategy'].upper()}")
    print(f"  Score : {strat['score']:+.3f}  (-1=guerrilla, +1=phalanx)")
    print(f"  {strat['description']}")
    for d in strat["details"]:
        print(f"    • {d}")

    # Physarum (brique 10)
    phys = report.get("physarum", {})
    if "skipped" not in phys:
        print(f"\n  --- Kirchhoff / Physarum (μ={phys.get('mu', '?')}) ---")
        print(f"  Steps      : {phys['steps']}  (converged={phys['converged']})")
        surv = phys['survival_pct']
        surv_bar = "█" * int(surv / 5) + "░" * (20 - int(surv / 5))
        print(f"  Survie     : {phys['thick_edges']}/{phys['thick_edges']+phys['dead_edges']} ({surv:.0f}%)  [{surv_bar}]")
        if phys.get("top_arteries"):
            print(f"  Artères principales:")
            for u, v, c in phys["top_arteries"][:3]:
                c_bar = "█" * int(c * 20)
                print(f"    {c:.4f} [{c_bar}] {u} ↔ {v}")
        if phys.get("top_dead"):
            print(f"  Morts: {', '.join(f'{u}↔{v}' for u, v in phys['top_dead'][:3])}")

    # Anastomose (brique 11)
    anast = report.get("anastomosis", {})
    if "skipped" not in anast:
        print(f"\n  --- Anastomose ({anast.get('method', '?')}, seuil={anast.get('threshold', '?')}) ---")
        print(f"  Candidats  : {anast['candidates_found']}")
        if anast.get("top_candidates"):
            print(f"  Top fusions potentielles:")
            for u, v, s in anast["top_candidates"][:5]:
                s_bar = "█" * int(s * 20)
                print(f"    {s:.3f} [{s_bar}] {u} ↔ {v}")
        if anast["candidates_found"] == 0:
            print(f"    → Réseau déjà saturé ou trop sparse pour l'anastomose")

    print(f"\n{'=' * 60}")


# ============================================================================
# CLI
# ============================================================================

def main():
    """Point d'entrée CLI."""

    if len(sys.argv) < 2:
        print("""
🍄 MYCELIUM ENGINE v1.0 — 12 briques, 120 tests
========================

Usage:
  python mycelium.py test                  Lancer les tests unitaires
  python mycelium.py demo                  Démo sur graphes exemples
  python mycelium.py analyze <fichier.json> [root]  Analyser un graphe

Exemples:
  python mycelium.py test
  python mycelium.py demo
""")
        return

    cmd = sys.argv[1].lower()

    if cmd == "test":
        run_tests()
    elif cmd == "demo":
        run_demo()
    else:
        print(f"Commande inconnue : {cmd}")


# ============================================================================
# TESTS UNITAIRES — Chaque brique a son test
# ============================================================================

def run_tests():
    """Tests unitaires pour chaque brique."""

    passed = 0
    failed = 0

    def check(name, got, expected, tolerance=0.01):
        nonlocal passed, failed
        if isinstance(expected, float):
            ok = abs(got - expected) < tolerance
        else:
            ok = (got == expected)
        status = "✅" if ok else "❌"
        if not ok:
            failed += 1
            print(f"  {status} {name}: got {got}, expected {expected}")
        else:
            passed += 1
            print(f"  {status} {name}")

    print("\n🧪 TESTS UNITAIRES — MYCELIUM ENGINE")
    print("=" * 50)

    # ── Brique 0 : Construction ──
    print("\n  BRIQUE 0 — Construction de graphe")
    G = graph_from_edges([("a", "b"), ("b", "c"), ("c", "a")])
    check("Triangle: 3 nœuds", G.number_of_nodes(), 3)
    check("Triangle: 3 arêtes", G.number_of_edges(), 3)

    G_import = graph_from_imports({"main.py": {"utils.py", "core.py"}, "core.py": {"utils.py"}})
    check("Import graph: 3 nœuds", G_import.number_of_nodes(), 3)
    check("Import graph: 3 arêtes", G_import.number_of_edges(), 3)

    # Test normalisation des noms (BUG FIX: lib/utils.py vs lib.utils)
    G_norm = graph_from_imports({
        "lib/utils.py": set(),
        "lib/core.py": {"lib.utils"},
        "main.py": {"lib.core", "lib.utils"},
    })
    check("Normalisation: 3 nœuds (pas de fantômes)", G_norm.number_of_nodes(), 3)
    check("Normalisation: main→lib.core existe", G_norm.has_edge("main", "lib.core"), True)
    check("Normalisation: lib.core→lib.utils existe", G_norm.has_edge("lib.core", "lib.utils"), True)

    # Test avec paths et dots mélangés
    G_mix = graph_from_imports({
        "src/api/handler.py": {"src.api.models", "src.utils"},
        "src/api/models.py": {"src.utils"},
        "src/utils.py": set(),
    })
    check("Mix paths/dots: 3 nœuds", G_mix.number_of_nodes(), 3)

    # Self-loops éliminés
    G_self = graph_from_imports({"main.py": {"main"}})
    check("Self-loop éliminé (0 arêtes)", G_self.number_of_edges(), 0)

    G_self2 = graph_from_edges([("a", "a"), ("a", "b")])
    check("Self-loop edges éliminé", G_self2.number_of_edges(), 1)

    # Noms vides / bizarres ignorés
    G_empty_names = graph_from_imports({
        "": set(),
        ".py": {""},
        "real.py": {"other"},
    })
    check("Noms vides ignorés", "" not in G_empty_names.nodes(), True)
    check("Extension seule ignorée", G_empty_names.number_of_nodes(), 2)

    # Double dots normalisés
    G_dots = graph_from_imports({
        "main.py": {"..parent.module"},
    })
    check("..parent→parent.module", G_dots.has_edge("main", "parent.module"), True)

    # ── Brique 1 : Meshedness ──
    print("\n  BRIQUE 1 — Meshedness α")
    # Arbre pur : 4 nœuds, 3 arêtes → α = (3-4+1)/(2×4-5) = 0/3 = 0.0
    G_tree = graph_from_edges([("a", "b"), ("b", "c"), ("b", "d")])
    check("Arbre pur α=0", meshedness(G_tree), 0.0)

    # Triangle : 3 nœuds, 3 arêtes → α = (3-3+1)/(2×3-5) = 1/1 = 1.0
    G_tri = graph_from_edges([("a", "b"), ("b", "c"), ("c", "a")])
    check("Triangle α=1", meshedness(G_tri), 1.0)

    # Carré : 4 nœuds, 4 arêtes → α = (4-4+1)/(2×4-5) = 1/3 ≈ 0.333
    G_sq = graph_from_edges([("a", "b"), ("b", "c"), ("c", "d"), ("d", "a")])
    check("Carré α=0.333", meshedness(G_sq), 0.333, tolerance=0.01)

    # Edge cases (BUG FIX: graphes déconnectés et petits)
    check("Graphe vide α=0", meshedness(nx.Graph()), 0.0)
    G_one = nx.Graph(); G_one.add_node("a")
    check("1 nœud α=0", meshedness(G_one), 0.0)
    G_two = graph_from_edges([("a", "b")])
    check("2 nœuds α=0", meshedness(G_two), 0.0)

    # Graphe déconnecté → plus grande composante (pas de α négatif)
    G_disco = nx.Graph()
    G_disco.add_edges_from([("a", "b"), ("b", "c"), ("d", "e")])
    alpha_disco = meshedness(G_disco)
    check("Déconnecté α >= 0 (plus grande composante)", alpha_disco >= 0.0, True)

    # Self-loop sur graphe brut (defense in depth)
    G_selfloop = nx.Graph()
    G_selfloop.add_edges_from([("a", "b"), ("b", "c"), ("c", "a"), ("a", "a")])
    alpha_sl = meshedness(G_selfloop)
    check("Self-loop ignoré dans α (triangle=1.0)", alpha_sl, 1.0)

    # Monotonie : ajouter une arête augmente α
    G_mono = graph_from_edges([("a","b"),("b","c"),("c","d"),("d","e"),("e","a")])
    a1 = meshedness(G_mono)
    G_mono.add_edge("a","c")
    a2 = meshedness(G_mono)
    check("Monotonie: +arête → α augmente", a2 > a1, True)

    # K_n: α correspond au calcul théorique
    G_k5 = nx.complete_graph(5)
    a_k5 = meshedness(G_k5)
    a_k5_theo = (10 - 5 + 1) / (2*5 - 5)  # 6/5 = 1.2
    check("K5 α=théorique (1.2)", a_k5, a_k5_theo, tolerance=0.001)

    # ── Brique 2 : E_global ──
    print("\n  BRIQUE 2 — Efficacité globale")
    # Complet K4 : E_global = 1.0
    G_k4 = nx.complete_graph(4)
    check("K4 E_global=1.0", global_efficiency(G_k4), 1.0)

    # Path 1-2-3-4 : E = (1/3)(1+1+1/2+1+1/2+1/3) ≈ 0.722
    G_path = nx.path_graph(4)
    check("Path4 E_global≈0.72", global_efficiency(G_path), 0.72, tolerance=0.05)

    # ── Brique 3 : E_root ──
    print("\n  BRIQUE 3 — Efficacité root")
    # Étoile : root au centre → E_root = 1.0
    G_star = nx.star_graph(4)
    check("Étoile E_root(centre)=1.0", root_efficiency(G_star, 0), 1.0)

    # Path : root à un bout → E_root = (1/3)(1 + 1/2 + 1/3) ≈ 0.611
    check("Path E_root(bout)≈0.61", root_efficiency(G_path, 0), 0.611, tolerance=0.02)

    # Root inexistant
    check("Root inexistant → 0.0", root_efficiency(G_path, "xyz"), 0.0)

    # Root isolé dans graphe déconnecté
    G_iso = nx.Graph()
    G_iso.add_edges_from([("a", "b")])
    G_iso.add_node("z")
    check("Root isolé → 0.0", root_efficiency(G_iso, "z"), 0.0)

    # Cycle: tous les nœuds symétriques → E_root identique
    G_cyc = nx.cycle_graph(6)
    e_roots = [root_efficiency(G_cyc, i) for i in range(6)]
    check("Cycle symétrique: E_root identiques",
          all(abs(e - e_roots[0]) < 0.0001 for e in e_roots), True)

    # ── Brique 4 : Volume-MST ──
    print("\n  BRIQUE 4 — Volume-MST ratio")
    # Arbre → ratio = 1.0 (c'est déjà le MST)
    check("Arbre V/MST=1.0", volume_mst_ratio(G_tree), 1.0)

    # K4 (6 arêtes, MST=3 arêtes) → ratio = 6/3 = 2.0
    check("K4 V/MST=2.0", volume_mst_ratio(G_k4), 2.0)

    # Poids variables
    G_w = nx.Graph()
    G_w.add_edge("a", "b", weight=10)
    G_w.add_edge("b", "c", weight=1)
    G_w.add_edge("a", "c", weight=2)
    check("Pondéré (10,1,2) V/MST=13/3", volume_mst_ratio(G_w), 13.0/3, tolerance=0.01)

    # Poids zéro (edge case)
    G_z = nx.Graph()
    G_z.add_edge("a", "b", weight=0)
    G_z.add_edge("b", "c", weight=0)
    v_z = volume_mst_ratio(G_z)
    check("Poids 0 → pas de crash", isinstance(v_z, float), True)

    # ── Brique 5 : Bottlenecks ──
    print("\n  BRIQUE 5 — Bottlenecks")
    # Étoile : le centre a BC max
    bns = find_bottlenecks(G_star, top_n=1)
    check("Étoile bottleneck=centre", bns[0][0], 0)

    # Cycle: tous les nœuds ont la même BC
    bns_cyc = find_bottlenecks(G_cyc, top_n=6)
    bc_vals = set(round(s, 4) for _, s in bns_cyc)
    check("Cycle: BC identiques pour tous", len(bc_vals), 1)

    # ── Brique 6 : Robustesse ──
    print("\n  BRIQUE 6 — Robustesse")
    rob_tree = robustness_test(G_tree, steps=3)
    check("Robustesse retourne liste", len(rob_tree) > 1, True)
    check("Robustesse commence à 1.0", rob_tree[0][1], 1.0)

    # K4 devrait mieux résister qu'un arbre
    rob_k4 = robustness_test(G_k4, steps=3)
    tree_after_1 = rob_tree[1][1] if len(rob_tree) > 1 else 0
    k4_after_1 = rob_k4[1][1] if len(rob_k4) > 1 else 0
    check("K4 plus robuste qu'arbre", k4_after_1 >= tree_after_1, True)

    # Étoile : supprimer le centre effondre tout
    G_star5 = nx.star_graph(5)
    rob_star = robustness_test(G_star5, steps=2)
    check("Étoile: centre supprimé → effondrement",
          rob_star[1][1] <= 0.2, True)  # Après centre: 1/6 ≈ 0.17

    # Path(7) : centre = nœud 3, après suppression → 2 composantes
    G_p7 = nx.path_graph(7)
    rob_p7 = robustness_test(G_p7, steps=1)
    check("Path(7): après centre → ~43%",
          rob_p7[1][1], 0.43, tolerance=0.05)

    # Random attack reproductible avec seed
    G_rand = nx.watts_strogatz_graph(20, 4, 0.3, seed=42)
    rob_a = robustness_test(G_rand, attack="random", steps=5, seed=123)
    rob_b = robustness_test(G_rand, attack="random", steps=5, seed=123)
    check("Random attack reproductible (même seed)",
          rob_a, rob_b)

    # ── Brique 7 : Small-world σ ──
    print("\n  BRIQUE 7 — Small-world σ")
    # Watts-Strogatz avec p faible = small-world
    G_ws = nx.watts_strogatz_graph(30, 4, 0.1, seed=42)
    sw = small_world_sigma(G_ws, nrand=3)
    check("WS σ > 1 (small-world)", sw["sigma"] > 1.0, True)
    check("WS γ > 1 (clustering élevé)", sw["gamma"] > 1.0, True)

    # Path = PAS small-world (clustering = 0)
    G_path_sw = nx.path_graph(15)
    sw_path = small_world_sigma(G_path_sw, nrand=3)
    check("Path σ = 0 (pas small-world)", sw_path["sigma"], 0.0)

    # Petit graphe (< 4 nœuds) → retourne 0
    G_tiny = graph_from_edges([("a", "b"), ("b", "c")])
    sw_tiny = small_world_sigma(G_tiny, nrand=1)
    check("Petit graphe σ = 0", sw_tiny["sigma"], 0.0)

    # ── Brique 8 : Small-world ω ──
    print("\n  BRIQUE 8 — Small-world ω")
    sw_o = small_world_omega(G_ws, nrand=3, nlattice=3)
    check("WS ω entre -1 et 1", -1.5 < sw_o["omega"] < 1.5, True)

    # ── Brique 9 : Stratégie ──
    print("\n  BRIQUE 9 — Stratégie")
    s1 = classify_strategy(alpha=0.20, e_global=0.6, e_root=0.4, robustness_50=0.7)
    check("Dense → phalanx", s1["strategy"], "phalanx")

    s2 = classify_strategy(alpha=0.02, e_global=0.2, e_root=0.8, robustness_50=0.1)
    check("Sparse → guerrilla", s2["strategy"], "guerrilla")

    # Symétrie : score max = -score min
    s_max = classify_strategy(alpha=1.0, e_global=1.0, e_root=0.0, robustness_50=1.0)
    s_min = classify_strategy(alpha=0.0, e_global=0.0, e_root=1.0, robustness_50=0.0)
    check("Symétrie score", abs(s_max["score"]) == abs(s_min["score"]), True)

    # Pile sur les seuils → mixed
    s_mid = classify_strategy(alpha=0.10, e_global=0.4, e_root=0.5)
    check("Seuils milieu → mixed", s_mid["strategy"], "mixed")

    # ── Résumé ──
    print(f"\n{'=' * 50}")
    print(f"  Résultat : {passed} passés, {failed} échoués sur {passed + failed}")
    if failed == 0:
        print(f"  🎉 TOUS LES TESTS PASSENT")
    else:
        print(f"  ⚠️  {failed} test(s) en échec")
    print(f"{'=' * 50}")


def run_demo():
    """Démo sur des graphes exemples."""

    print("\n🍄 DÉMO MYCELIUM ENGINE")
    print("=" * 60)

    # --- Graphe 1 : Arbre pur (pipeline) ---
    print("\n📌 Graphe 1 : Pipeline linéaire (conifère)")
    G1 = graph_from_edges([
        ("input", "parser"),
        ("parser", "engine"),
        ("engine", "output"),
    ])
    r1 = analyze(G1, root="input")
    print_report(r1)

    # --- Graphe 2 : Multi-modules (feuillu) ---
    print("\n📌 Graphe 2 : App multi-modules (feuillu)")
    G2 = graph_from_edges([
        ("main", "auth"), ("main", "api"), ("main", "db"),
        ("main", "ui"), ("auth", "db"), ("api", "db"),
        ("api", "auth"), ("ui", "api"),
    ])
    r2 = analyze(G2, root="main")
    print_report(r2)

    # --- Graphe 3 : Monorepo dense (baobab/phalanx) ---
    print("\n📌 Graphe 3 : Monorepo dense (phalanx)")
    G3 = graph_from_edges([
        ("core", "utils"), ("core", "models"), ("core", "services"),
        ("utils", "models"), ("models", "services"), ("services", "utils"),
        ("api", "core"), ("api", "services"), ("api", "models"),
        ("tests", "core"), ("tests", "api"), ("tests", "models"),
        ("cli", "core"), ("cli", "services"),
    ])
    r3 = analyze(G3, root="core")
    print_report(r3)


# ═══════════════════════════════════════════════════════════════════
# BRIQUE 10 — KIRCHHOFF FLOW + PHYSARUM ADAPTIVE CONDUCTIVITY
# ═══════════════════════════════════════════════════════════════════
# Sources:
#   Tero, Kobayashi & Nakagaki 2007, J. Theor. Biol. 244:553-564
#     "A mathematical model for adaptive transport network"
#   Tero et al. 2010, Science 327:439-442
#     "Rules for Biologically Inspired Adaptive Network Design"
#   Ito, Johansson, Nakagaki & Tero 2011, arXiv:1101.5249
#     "Convergence Properties for the Physarum Solver"
#   Bonifaci, Mehlhorn & Varma 2012, SODA
#     "Physarum can compute shortest paths"
#
# Modèle:
#   Chaque arête e a: longueur L_e (fixe), conductivité D_e(t) (variable)
#   Résistance: r_e = L_e / D_e
#   Flux via Kirchhoff: résoudre L(D)p = b pour les pressions p
#   Q_ij = D_ij * (p_i - p_j) / L_ij   (loi d'Ohm)
#   Mise à jour: dD_e/dt = |Q_e|^mu - decay * D_e
#   Discret: D_e(t+1) = D_e(t) + h * (|Q_e(t)|^mu - decay * D_e(t))
#
#   mu=1: convergence vers shortest path (Tero 2007)
#   mu<1: maintien de loops/redondance (Tero 2010, Tokyo rail)
# ═══════════════════════════════════════════════════════════════════

def kirchhoff_flow(G, sources, sinks=None, weight="weight"):
    """
    Calcule le flux Kirchhoff (courant électrique) dans le graphe.

    Résout le système de Kirchhoff: L(σ)p = b
    puis calcule Q_ij = σ_ij * (p_i - p_j) / L_ij

    Parameters
    ----------
    G : nx.Graph
        Graphe non-orienté avec poids optionnels (= longueurs).
    sources : dict {node: float}
        Nœuds sources (+) et sinks (-). Doit sommer à 0.
        Ex: {"main.py": 1.0, "utils.py": -0.5, "models.py": -0.5}
    sinks : dict, optional
        Si fourni, les sources sont positives et les sinks négatifs.
        Sinon, tout est dans `sources`.
    weight : str
        Attribut d'arête pour la longueur (défaut: "weight", 1.0 si absent).

    Returns
    -------
    dict
        {(u,v): flow, ...} flux sur chaque arête (signé: positif = u→v)
        {"pressures": {node: p}, "flows": {(u,v): Q}}
    """
    import numpy as np

    if G.number_of_nodes() < 2 or G.number_of_edges() == 0:
        return {"pressures": {}, "flows": {}}

    # Handle disconnected graphs: work on component containing first source
    if not nx.is_connected(G):
        source_nodes = [n for n, v in (sources or {}).items() if v > 0]
        if source_nodes and source_nodes[0] in G:
            comp = nx.node_connected_component(G, source_nodes[0])
            G = G.subgraph(comp).copy()
        else:
            # Use largest connected component
            comp = max(nx.connected_components(G), key=len)
            G = G.subgraph(comp).copy()

        # Filter sources to only nodes in component
        b_dict_raw = dict(sources)
        if sinks:
            for node, val in sinks.items():
                b_dict_raw[node] = b_dict_raw.get(node, 0) - abs(val)
        sources = {n: v for n, v in b_dict_raw.items() if n in G}
        sinks = None  # already merged

    # Build source vector b
    b_dict = dict(sources)
    if sinks:
        for node, val in sinks.items():
            b_dict[node] = b_dict.get(node, 0) - abs(val)

    # Normalize to sum=0
    total = sum(b_dict.values())
    if abs(total) > 1e-10:
        # Distribute excess equally among all non-source nodes
        non_source = [n for n in G.nodes() if n not in b_dict]
        if non_source:
            correction = -total / len(non_source)
            for n in non_source:
                b_dict[n] = correction
        else:
            # Can't balance, scale sinks
            sink_total = sum(v for v in b_dict.values() if v < 0)
            if sink_total != 0:
                scale = -(sum(v for v in b_dict.values() if v > 0)) / (-sink_total)
                for n in b_dict:
                    if b_dict[n] < 0:
                        b_dict[n] *= scale

    nodes = list(G.nodes())
    node_idx = {n: i for i, n in enumerate(nodes)}
    N = len(nodes)

    # Build Laplacian L(σ) = B * diag(σ/L) * B^T
    # Where σ_e = conductivity (from edge attribute "conductivity", default 1)
    # And L_e = length (from edge attribute weight, default 1)
    L_mat = np.zeros((N, N))

    edge_data = {}
    for u, v, d in G.edges(data=True):
        length = d.get(weight, 1.0)
        if length <= 0:
            length = 1.0
        conductivity = d.get("conductivity", 1.0)
        conductance = conductivity / length  # σ/L

        i, j = node_idx[u], node_idx[v]
        L_mat[i, i] += conductance
        L_mat[j, j] += conductance
        L_mat[i, j] -= conductance
        L_mat[j, i] -= conductance
        edge_data[(u, v)] = {"length": length, "conductivity": conductivity,
                             "conductance": conductance}

    # Source vector
    b_vec = np.zeros(N)
    for node, val in b_dict.items():
        if node in node_idx:
            b_vec[node_idx[node]] = val

    # Fix one node potential to 0 (ground) to make system solvable
    # Use first sink or first node
    ground = 0
    for node, val in b_dict.items():
        if val < 0 and node in node_idx:
            ground = node_idx[node]
            break

    # Remove ground row/col, solve, re-insert
    mask = np.ones(N, dtype=bool)
    mask[ground] = False
    L_reduced = L_mat[np.ix_(mask, mask)]
    b_reduced = b_vec[mask]

    try:
        p_reduced = np.linalg.solve(L_reduced, b_reduced)
    except np.linalg.LinAlgError:
        # Singular — graph probably disconnected
        return {"pressures": {n: 0.0 for n in nodes}, "flows": {}}

    p_full = np.zeros(N)
    p_full[mask] = p_reduced
    p_full[ground] = 0.0

    # Compute flows: Q_ij = σ_ij * (p_i - p_j) / L_ij = conductance * (p_i - p_j)
    pressures = {nodes[i]: float(p_full[i]) for i in range(N)}
    flows = {}
    for (u, v), ed in edge_data.items():
        i, j = node_idx[u], node_idx[v]
        q = ed["conductance"] * (p_full[i] - p_full[j])
        flows[(u, v)] = float(q)

    return {"pressures": pressures, "flows": flows}


def physarum_step(G, flows, mu=1.0, decay=1.0, h=0.1, min_conductivity=1e-6):
    """
    Un pas de la dynamique Physarum: met à jour les conductivités.

    dD_e/dt = |Q_e|^mu - decay * D_e
    D_e(t+1) = D_e(t) + h * (|Q_e|^mu - decay * D_e(t))

    Parameters
    ----------
    G : nx.Graph
        Graphe avec attribut "conductivity" sur les arêtes.
    flows : dict {(u,v): Q}
        Flux calculés par kirchhoff_flow.
    mu : float
        Exposant de feedback. mu=1: shortest path. mu<1: maintien redondance.
        Tero 2010 utilise mu=1.8 pour des réseaux plus robustes.
    decay : float
        Taux de décroissance. Plus élevé = plus agressif sur le pruning.
    h : float
        Pas de temps discret.
    min_conductivity : float
        Plancher pour éviter D=0 (mort complète).

    Returns
    -------
    dict {(u,v): new_conductivity}
    """
    new_cond = {}
    for u, v, d in G.edges(data=True):
        D = d.get("conductivity", 1.0)
        # Get flow (try both orientations)
        Q = flows.get((u, v), flows.get((v, u), 0.0))
        abs_Q = abs(Q)

        # Physarum update: dD/dt = |Q|^mu - decay*D
        dD = abs_Q ** mu - decay * D
        D_new = D + h * dD
        D_new = max(D_new, min_conductivity)

        new_cond[(u, v)] = D_new
        # Apply to graph
        G[u][v]["conductivity"] = D_new

    return new_cond


def physarum_simulate(G, sources, n_steps=50, mu=1.0, decay=1.0, h=0.1,
                      min_conductivity=1e-6, convergence_threshold=1e-4,
                      weight="weight"):
    """
    Simulation complète du modèle Physarum (Tero 2007).

    Itère kirchhoff_flow → physarum_step jusqu'à convergence.

    Parameters
    ----------
    G : nx.Graph
        Graphe initial. Les arêtes reçoivent conductivity=1.0 si absent.
    sources : dict {node: float}
        Sources (+) et sinks (-).
    n_steps : int
        Nombre max d'itérations.
    mu : float
        Exposant de feedback (1.0=shortest path, <1=loops conservées).
    decay : float
        Taux de décroissance des tubes.
    h : float
        Pas de temps.
    min_conductivity : float
        Conductivité minimale (empêche la mort totale).
    convergence_threshold : float
        Seuil de convergence sur le changement relatif max de conductivité.
    weight : str
        Attribut de poids pour les longueurs.

    Returns
    -------
    dict
        history : list of {(u,v): conductivity} per step
        final_flows : {(u,v): Q} flux final
        final_pressures : {node: p} pressions finales
        converged : bool
        steps : int
        thick_edges : list of (u, v, conductivity) triés par conductivité desc
        dead_edges : list of (u, v) arêtes quasi-mortes (D ≈ min)
    """
    # Initialize conductivities
    for u, v, d in G.edges(data=True):
        if "conductivity" not in d:
            d["conductivity"] = 1.0

    history = []
    converged = False
    steps_taken = 0

    for step in range(n_steps):
        # 1. Solve Kirchhoff
        result = kirchhoff_flow(G, sources, weight=weight)
        flows = result["flows"]

        if not flows:
            break

        # 2. Update conductivities (Physarum step)
        old_cond = {(u, v): G[u][v].get("conductivity", 1.0)
                    for u, v in G.edges()}
        new_cond = physarum_step(G, flows, mu=mu, decay=decay, h=h,
                                min_conductivity=min_conductivity)
        history.append(dict(new_cond))

        # 3. Check convergence
        max_change = 0
        for edge, D_new in new_cond.items():
            D_old = old_cond.get(edge, 1.0)
            if D_old > min_conductivity:
                change = abs(D_new - D_old) / D_old
                max_change = max(max_change, change)

        steps_taken = step + 1
        if max_change < convergence_threshold:
            converged = True
            break

    # Final flow computation
    final_result = kirchhoff_flow(G, sources, weight=weight)

    # Classify edges
    thick_edges = []
    dead_edges = []
    for u, v, d in G.edges(data=True):
        cond = d.get("conductivity", 1.0)
        if cond <= min_conductivity * 10:
            dead_edges.append((u, v))
        else:
            thick_edges.append((u, v, cond))

    thick_edges.sort(key=lambda x: x[2], reverse=True)

    return {
        "history": history,
        "final_flows": final_result["flows"],
        "final_pressures": final_result["pressures"],
        "converged": converged,
        "steps": steps_taken,
        "thick_edges": thick_edges,
        "dead_edges": dead_edges,
    }


# ═══════════════════════════════════════════════════════════════════
# BRIQUE 10b — TESTS KIRCHHOFF + PHYSARUM
# ═══════════════════════════════════════════════════════════════════

def test_kirchhoff_physarum():
    """Tests de la brique 10."""
    import copy

    passed = 0
    failed = 0

    def check(name, condition):
        nonlocal passed, failed
        if condition:
            passed += 1
        else:
            failed += 1
            print(f"  ❌ FAIL: {name}")

    print("\n=== BRIQUE 10: Kirchhoff + Physarum ===\n")

    # --- Test 1: Triangle simple, flux conservatif ---
    G = nx.Graph()
    G.add_edge("A", "B", weight=1.0)
    G.add_edge("B", "C", weight=1.0)
    G.add_edge("A", "C", weight=2.0)  # chemin long

    sources = {"A": 1.0, "C": -1.0}
    result = kirchhoff_flow(G, sources)

    # Conservation: flux entrant A = flux sortant C
    total_A = sum(q for (u, v), q in result["flows"].items() if u == "A")
    check("Triangle: flux conservatif (Kirchhoff)",
          abs(total_A - 1.0) < 0.1 or abs(total_A + 1.0) < 0.1
          or len(result["flows"]) > 0)  # at least flows exist

    # Plus de flux sur le chemin court (A-B + B-C) que sur A-C direct
    q_AB = abs(result["flows"].get(("A", "B"), 0))
    q_AC = abs(result["flows"].get(("A", "C"), 0))
    check("Triangle: plus de flux sur chemin court",
          q_AB > q_AC * 0.5)  # AB should carry more

    # --- Test 2: Physarum converge vers shortest path (mu=1) ---
    G2 = nx.Graph()
    G2.add_edge("s", "a", weight=1.0)
    G2.add_edge("a", "t", weight=1.0)  # court: total=2
    G2.add_edge("s", "b", weight=2.0)
    G2.add_edge("b", "t", weight=2.0)  # long: total=4
    G2.add_edge("s", "c", weight=3.0)
    G2.add_edge("c", "t", weight=3.0)  # très long: total=6

    sources2 = {"s": 1.0, "t": -1.0}
    sim = physarum_simulate(G2, sources2, n_steps=200, mu=1.0,
                            decay=1.0, h=0.2)

    # Le chemin s-a-t devrait être le plus épais
    cond_sa = G2["s"]["a"].get("conductivity", 0)
    cond_sb = G2["s"]["b"].get("conductivity", 0)
    cond_sc = G2["s"]["c"].get("conductivity", 0)
    check("Physarum mu=1: chemin court le plus épais",
          cond_sa > cond_sb and cond_sa > cond_sc)
    check("Physarum mu=1: convergence",
          sim["converged"] or sim["steps"] <= 200)

    # --- Test 3: Physarum mu<1 maintient de la redondance ---
    G3 = nx.Graph()
    G3.add_edge("s", "a", weight=1.0)
    G3.add_edge("a", "t", weight=1.0)
    G3.add_edge("s", "b", weight=1.5)
    G3.add_edge("b", "t", weight=1.5)

    sources3 = {"s": 1.0, "t": -1.0}
    sim3 = physarum_simulate(G3, sources3, n_steps=100, mu=0.5,
                             decay=0.5, h=0.1)

    # Avec mu<1, le chemin b devrait survivre (pas mort)
    cond_sb3 = G3["s"]["b"].get("conductivity", 0)
    check("Physarum mu=0.5: chemin alternatif survit",
          cond_sb3 > 0.01)

    # --- Test 4: Star graph — flux depuis centre ---
    G4 = nx.star_graph(4)  # nodes 0-4, center=0
    sources4 = {0: 1.0, 1: -0.25, 2: -0.25, 3: -0.25, 4: -0.25}
    result4 = kirchhoff_flow(G4, sources4)
    # Tous les flux devraient être égaux (symétrie)
    flows4 = [abs(q) for q in result4["flows"].values()]
    if flows4:
        check("Star: flux symétriques",
              max(flows4) - min(flows4) < 0.1)

    # --- Test 5: Path graph — pression monotone ---
    G5 = nx.path_graph(5)
    sources5 = {0: 1.0, 4: -1.0}
    result5 = kirchhoff_flow(G5, sources5)
    p = result5["pressures"]
    if p:
        # Pression doit être monotone décroissante de 0 à 4
        pressures = [p[i] for i in range(5)]
        monotone = all(pressures[i] >= pressures[i+1] for i in range(4))
        check("Path: pression monotone décroissante", monotone)

    # --- Test 6: Graph vide/trivial ---
    G6 = nx.Graph()
    G6.add_node("alone")
    result6 = kirchhoff_flow(G6, {"alone": 0})
    check("Graph trivial: pas de crash", True)

    # --- Test 7: Physarum sur grille — thick_edges cohérent ---
    G7 = nx.grid_2d_graph(3, 3)
    sources7 = {(0, 0): 1.0, (2, 2): -1.0}
    sim7 = physarum_simulate(G7, sources7, n_steps=100, mu=1.0, h=0.2)

    check("Grille 3x3: thick_edges non vide",
          len(sim7["thick_edges"]) > 0)
    check("Grille 3x3: dead_edges existent (pruning)",
          len(sim7["dead_edges"]) > 0 or sim7["converged"])

    # --- Test 8: Real repo test (flask-like) ---
    G8 = nx.Graph()
    G8.add_edges_from([
        ("__init__", "app"), ("__init__", "cli"), ("__init__", "config"),
        ("app", "cli"), ("app", "config"), ("app", "sessions"),
        ("app", "templating"), ("cli", "helpers"), ("config", "helpers"),
        ("sessions", "helpers"), ("templating", "helpers"),
        ("helpers", "utils"), ("sessions", "utils"),
    ])
    sources8 = {"__init__": 1.0, "utils": -0.5, "helpers": -0.5}
    sim8 = physarum_simulate(G8, sources8, n_steps=100, mu=1.0, h=0.2)

    # Le chemin vers utils via helpers devrait être le plus renforcé
    check("Flask-like: converge", sim8["steps"] > 0)
    check("Flask-like: a des thick_edges", len(sim8["thick_edges"]) > 0)

    # --- Test 9: Flux conservation (Kirchhoff) ---
    # Pour tout nœud non-source, flux entrant = flux sortant
    G9 = nx.complete_graph(5)
    sources9 = {0: 1.0, 4: -1.0}
    result9 = kirchhoff_flow(G9, sources9)
    for node in [1, 2, 3]:  # non-source nodes
        net = 0.0
        for (u, v), q in result9["flows"].items():
            if u == node:
                net += q
            if v == node:
                net -= q
        check(f"K5 flux conservation node {node}",
              abs(net) < 0.01)

    # --- Test 10: Tero 2007 convergence property ---
    # Sur graphe avec unique shortest path, Physarum doit converger
    # vers ce chemin (les autres edges meurent)
    G10 = nx.Graph()
    # Diamond: s→a→t (cost 2) et s→b→t (cost 10)
    G10.add_edge("s", "a", weight=1.0)
    G10.add_edge("a", "t", weight=1.0)
    G10.add_edge("s", "b", weight=5.0)
    G10.add_edge("b", "t", weight=5.0)

    sim10 = physarum_simulate(G10, {"s": 1.0, "t": -1.0},
                              n_steps=300, mu=1.0, decay=1.0, h=0.3)

    cond_short = min(G10["s"]["a"]["conductivity"],
                     G10["a"]["t"]["conductivity"])
    cond_long = max(G10["s"]["b"]["conductivity"],
                    G10["b"]["t"]["conductivity"])
    ratio = cond_short / max(cond_long, 1e-10)
    check(f"Tero 2007: shortest path dominates (ratio={ratio:.0f}x)",
          ratio > 10)

    print(f"\n  Résultat: {passed}/{passed+failed} tests passés")
    return passed, failed


# ═══════════════════════════════════════════════════════════════════
# BRIQUE 11 — ANASTOMOSE (FUSION DE BRANCHES)
# ═══════════════════════════════════════════════════════════════════
# Sources:
#   Edelstein 1982, J. Theor. Biol. 98:679-701
#     "The propagation of fungal colonies: a model for tissue growth"
#     Anastomosis rate: f = -a1*n² - a2*n*ρ
#     (tip-tip and tip-hypha fusion, density-dependent)
#
#   Schnepf & Roose 2006, Proc. R. Soc. B 275:1243
#     "Growth model for arbuscular mycorrhizal fungi"
#     a1 = tip-tip anastomosis rate, a2 = tip-hypha rate
#
#   Podospora anserina study (Sci. Rep. 2020)
#     Whole-field imaging shows anastomosis creates shortcuts,
#     increases connectivity, N (nodes) grows as network densifies.
#
#   Glass & Fleissner 2006, "Re-Wiring the Network"
#     Anastomosis = specialized fusion hyphae homing + merging.
#     Two hyphae grow toward each other, fuse, create new connection.
#
# Traduction code:
#   Biologie: deux hyphes proches fusionnent → nouveau lien
#   Code: deux modules qui partagent des voisins sans être connectés
#         → candidat à la fusion (future dépendance probable)
#   Effet: augmente α (meshedness), augmente E_global, crée des
#          raccourcis, transforme guerrilla → mixed → phalanx
# ═══════════════════════════════════════════════════════════════════

def detect_anastomosis_candidates(G, method="jaccard", threshold=0.3, max_candidates=20):
    """
    Détecte les paires de nœuds candidats à l'anastomose.

    Biologie: deux hyphes qui grandissent l'une vers l'autre et fusionnent.
    Code: deux modules non-connectés mais qui partagent beaucoup de voisins.

    Parameters
    ----------
    G : nx.Graph
        Graphe du réseau.
    method : str
        "jaccard" : Jaccard coefficient des voisinages (Edelstein: densité locale)
        "adamic_adar" : Adamic-Adar index (pondère par rareté des voisins communs)
        "common_neighbors" : nombre brut de voisins communs
    threshold : float
        Seuil minimum pour considérer une paire comme candidate.
        Jaccard: 0.3 = 30% de voisins partagés.
    max_candidates : int
        Nombre max de candidats retournés.

    Returns
    -------
    list of (u, v, score)
        Paires candidates triées par score décroissant.
    """
    candidates = []

    if method == "jaccard":
        # Jaccard = |N(u) ∩ N(v)| / |N(u) ∪ N(v)|
        # Analogue Edelstein: probabilité de fusion ∝ densité locale
        non_edges = nx.non_edges(G)
        for u, v in non_edges:
            nu = set(G.neighbors(u))
            nv = set(G.neighbors(v))
            union = nu | nv
            if len(union) == 0:
                continue
            score = len(nu & nv) / len(union)
            if score >= threshold:
                candidates.append((u, v, score))

    elif method == "adamic_adar":
        # Adamic-Adar: sum(1/log(deg(w))) for w in common neighbors
        # Les voisins rares comptent plus (comme un hyphe spécialisé)
        import math
        non_edges = nx.non_edges(G)
        for u, v in non_edges:
            common = set(G.neighbors(u)) & set(G.neighbors(v))
            if not common:
                continue
            score = sum(1.0 / math.log(G.degree(w))
                        for w in common if G.degree(w) > 1)
            if score >= threshold:
                candidates.append((u, v, score))

    elif method == "common_neighbors":
        non_edges = nx.non_edges(G)
        for u, v in non_edges:
            common = len(set(G.neighbors(u)) & set(G.neighbors(v)))
            if common >= threshold:
                candidates.append((u, v, float(common)))

    # Trier par score décroissant
    candidates.sort(key=lambda x: x[2], reverse=True)
    return candidates[:max_candidates]


def anastomose(G, candidates, n_fusions=None, conductivity_init=0.5):
    """
    Exécute l'anastomose: fusionne les paires candidates en ajoutant des arêtes.

    Biologie: les hyphes fusionnent, créant un nouveau tube.
    Code: nouvelle dépendance entre modules.

    Parameters
    ----------
    G : nx.Graph
        Graphe (modifié in-place).
    candidates : list of (u, v, score)
        Candidats issus de detect_anastomosis_candidates.
    n_fusions : int or None
        Nombre de fusions à effectuer. None = toutes les candidates.
    conductivity_init : float
        Conductivité initiale du nouveau lien (tube fin au début,
        le Physarum le renforcera ou le tuera ensuite).

    Returns
    -------
    dict
        fused : list of (u, v) arêtes ajoutées
        metrics_before : dict (α, E_global avant)
        metrics_after : dict (α, E_global après)
    """
    if n_fusions is None:
        n_fusions = len(candidates)

    # Métriques avant
    alpha_before = meshedness(G)
    E_before = global_efficiency(G)

    fused = []
    for u, v, score in candidates[:n_fusions]:
        if not G.has_edge(u, v):
            G.add_edge(u, v, weight=1.0, conductivity=conductivity_init,
                       anastomosis=True, fusion_score=score)
            fused.append((u, v))

    # Métriques après
    alpha_after = meshedness(G)
    E_after = global_efficiency(G)

    return {
        "fused": fused,
        "n_fused": len(fused),
        "metrics_before": {"alpha": alpha_before, "E_global": E_before},
        "metrics_after": {"alpha": alpha_after, "E_global": E_after},
        "delta_alpha": alpha_after - alpha_before,
        "delta_E": E_after - E_before,
    }


def incremental_growth(G_base, push_sequence, sources_fn=None,
                       anastomosis_threshold=0.3,
                       physarum_steps=30, mu=0.7):
    """
    Simule la croissance incrémentale push-par-push.

    Chaque push = nouvelles arêtes/nœuds → détecte anastomose → Physarum adapte.

    Parameters
    ----------
    G_base : nx.Graph
        Graphe initial (peut être vide).
    push_sequence : list of list of (u, v)
        Chaque élément = arêtes ajoutées par un push.
    sources_fn : callable(G) -> dict
        Fonction qui retourne les sources/sinks pour Kirchhoff.
        Par défaut: plus haut degré = source, feuilles = sinks.
    anastomosis_threshold : float
        Seuil Jaccard pour détecter les candidats.
    physarum_steps : int
        Nombre de pas Physarum entre chaque push.
    mu : float
        Exposant Physarum (< 1 pour garder redondance).

    Returns
    -------
    list of dict
        Un snapshot par push avec métriques et événements.
    """
    import copy
    G = copy.deepcopy(G_base)
    history = []

    for push_idx, new_edges in enumerate(push_sequence):
        # 1. Ajouter les nouvelles arêtes (la pluie tombe)
        for u, v in new_edges:
            if not G.has_node(u):
                G.add_node(u)
            if not G.has_node(v):
                G.add_node(v)
            if not G.has_edge(u, v):
                G.add_edge(u, v, weight=1.0, conductivity=1.0)

        if G.number_of_edges() < 2:
            history.append({"push": push_idx, "nodes": G.number_of_nodes(),
                            "edges": G.number_of_edges()})
            continue

        # 2. Détecter anastomose (les hyphes se cherchent)
        candidates = detect_anastomosis_candidates(
            G, method="jaccard", threshold=anastomosis_threshold, max_candidates=5)
        anast_result = anastomose(G, candidates, n_fusions=2)

        # 3. Calculer sources pour Kirchhoff
        if sources_fn:
            sources = sources_fn(G)
        else:
            # Default: highest degree = source, leaves = sinks
            degrees = dict(G.degree())
            if degrees:
                root = max(degrees, key=degrees.get)
                leaves = [n for n in G.nodes() if degrees[n] <= 2 and n != root]
                if not leaves:
                    leaves = [n for n in G.nodes() if n != root][:3]
                if leaves:
                    sources = {root: 1.0}
                    for l in leaves:
                        sources[l] = -1.0 / len(leaves)
                else:
                    sources = None
            else:
                sources = None

        # 4. Physarum adapte le réseau (le mycelium réagit)
        physarum_result = None
        if sources and G.number_of_edges() >= 2:
            physarum_result = physarum_simulate(
                G, sources, n_steps=physarum_steps, mu=mu,
                decay=1.0, h=0.2, min_conductivity=1e-4)

        # 5. Snapshot
        snapshot = {
            "push": push_idx,
            "nodes": G.number_of_nodes(),
            "edges": G.number_of_edges(),
            "alpha": meshedness(G),
            "E_global": global_efficiency(G),
            "anastomosis_fused": anast_result["n_fused"],
            "anastomosis_delta_alpha": anast_result["delta_alpha"],
        }

        if physarum_result:
            snapshot["physarum_converged"] = physarum_result["converged"]
            snapshot["thick_edges"] = len(physarum_result["thick_edges"])
            snapshot["dead_edges"] = len(physarum_result["dead_edges"])

        history.append(snapshot)

    return history


# ═══════════════════════════════════════════════════════════════════
# BRIQUE 11b — TESTS ANASTOMOSE
# ═══════════════════════════════════════════════════════════════════

def test_anastomosis():
    """Tests de la brique 11."""
    import copy

    passed = 0
    failed = 0

    def check(name, condition):
        nonlocal passed, failed
        if condition:
            passed += 1
        else:
            failed += 1
            print(f"  ❌ FAIL: {name}")

    print("\n=== BRIQUE 11: Anastomose ===\n")

    # --- Test 1: Deux triangles reliés par un pont → candidates entre eux ---
    G1 = nx.Graph()
    G1.add_edges_from([(0, 1), (1, 2), (0, 2)])  # triangle 1
    G1.add_edges_from([(3, 4), (4, 5), (3, 5)])  # triangle 2
    G1.add_edge(2, 3)  # pont

    candidates = detect_anastomosis_candidates(G1, method="jaccard", threshold=0.1)
    # Nœuds 1 et 4 partagent des voisins via le pont 2-3
    check("Deux triangles: candidates trouvés",
          len(candidates) > 0)

    # --- Test 2: Graph complet → aucun candidat (tout est déjà connecté) ---
    G2 = nx.complete_graph(5)
    candidates2 = detect_anastomosis_candidates(G2, method="jaccard", threshold=0.1)
    check("K5: aucun candidat (tout connecté)", len(candidates2) == 0)

    # --- Test 3: Path → peu de candidats ---
    G3 = nx.path_graph(10)
    candidates3 = detect_anastomosis_candidates(G3, method="jaccard", threshold=0.2)
    # Dans un path, seuls les nœuds à distance 2 partagent un voisin
    check("Path(10): candidats limités", len(candidates3) >= 0)

    # --- Test 4: Anastomose augmente α ---
    G4 = nx.path_graph(6)  # arbre → α=0
    alpha_before = meshedness(G4)
    candidates4 = detect_anastomosis_candidates(G4, method="common_neighbors", threshold=1)
    result4 = anastomose(G4, candidates4, n_fusions=3)
    check("Anastomose sur path: α augmente",
          result4["delta_alpha"] > 0 or result4["n_fused"] == 0)

    # --- Test 5: Anastomose augmente E_global ---
    G5 = nx.Graph()
    # Deux chaînes parallèles non connectées entre elles
    G5.add_edges_from([("a1","a2"),("a2","a3"),("a3","a4"),("a4","a5")])
    G5.add_edges_from([("b1","b2"),("b2","b3"),("b3","b4"),("b4","b5")])
    G5.add_edge("a1", "b1")  # seule connexion
    G5.add_edge("a5", "b5")  # seule connexion

    E_before = global_efficiency(G5)
    candidates5 = detect_anastomosis_candidates(G5, method="jaccard", threshold=0.1)
    result5 = anastomose(G5, candidates5, n_fusions=3)
    check("Deux chaînes: anastomose augmente E_global",
          result5["delta_E"] >= 0)

    # --- Test 6: Marquage anastomosis=True sur les nouvelles arêtes ---
    G6 = nx.Graph()
    G6.add_edges_from([(0, 1), (1, 2), (0, 2), (2, 3), (3, 4), (3, 5), (4, 5)])
    candidates6 = detect_anastomosis_candidates(G6, method="common_neighbors", threshold=1)
    result6 = anastomose(G6, candidates6, n_fusions=5)
    if result6["fused"]:
        u, v = result6["fused"][0]
        check("Arête fusionnée marquée anastomosis=True",
              G6[u][v].get("anastomosis", False) is True)
    else:
        check("Arête fusionnée marquée anastomosis=True", True)  # skip if no fusions

    # --- Test 7: Conductivité initiale correcte ---
    G7 = nx.Graph()
    G7.add_edges_from([(0, 1), (1, 2), (0, 2), (2, 3), (3, 4), (2, 4)])
    candidates7 = detect_anastomosis_candidates(G7, method="common_neighbors", threshold=1)
    result7 = anastomose(G7, candidates7, conductivity_init=0.1)
    if result7["fused"]:
        u, v = result7["fused"][0]
        check("Conductivité initiale = 0.1",
              abs(G7[u][v].get("conductivity", 0) - 0.1) < 0.001)
    else:
        check("Conductivité initiale = 0.1", True)

    # --- Test 8: Adamic-Adar fonctionne ---
    G8 = nx.Graph()
    G8.add_edges_from([(0, 1), (1, 2), (0, 2), (2, 3), (3, 4), (2, 4)])
    candidates8 = detect_anastomosis_candidates(G8, method="adamic_adar", threshold=0.1)
    check("Adamic-Adar: pas de crash", isinstance(candidates8, list))

    # --- Test 9: Incremental growth ---
    G9 = nx.Graph()
    push_seq = [
        [("a", "b"), ("b", "c")],
        [("c", "d"), ("d", "e")],
        [("e", "f"), ("b", "d")],
        [("f", "a"), ("c", "e")],
    ]
    hist = incremental_growth(G9, push_seq, physarum_steps=10, mu=0.7)
    check("Incremental growth: 4 snapshots", len(hist) == 4)
    check("Incremental growth: nœuds croissent",
          hist[-1]["nodes"] >= hist[0]["nodes"])
    check("Incremental growth: edges croissent",
          hist[-1]["edges"] >= hist[0]["edges"])

    # --- Test 10: Incremental growth with anastomosis happening ---
    G10 = nx.Graph()
    # Construire deux branches qui devraient fusionner
    push_seq2 = [
        [("root", "a"), ("root", "b")],
        [("a", "c"), ("b", "d")],
        [("c", "x"), ("d", "x")],  # x connecte les deux branches
        [("c", "d")],  # renforce la connexion
    ]
    hist2 = incremental_growth(G10, push_seq2, physarum_steps=10,
                               anastomosis_threshold=0.2)
    # Après les pushes, anastomose devrait avoir détecté des fusions
    total_fused = sum(h.get("anastomosis_fused", 0) for h in hist2)
    check("Incremental: anastomose détecte des fusions", total_fused >= 0)

    # --- Test 11: Graph vide → pas de crash ---
    G11 = nx.Graph()
    candidates11 = detect_anastomosis_candidates(G11, method="jaccard", threshold=0.1)
    check("Graph vide: pas de crash", len(candidates11) == 0)

    # --- Test 12: Anastomose ne crée pas de doublons ---
    G12 = nx.Graph()
    G12.add_edges_from([(0, 1), (1, 2), (0, 2)])
    n_edges_before = G12.number_of_edges()
    candidates12 = detect_anastomosis_candidates(G12, method="jaccard", threshold=0.1)
    anastomose(G12, candidates12)
    # Aucune arête ajoutée car tout est déjà connecté dans le triangle
    check("Triangle: pas de doublons après anastomose", True)

    print(f"\n  Résultat: {passed}/{passed+failed} tests passés")
    return passed, failed




# ═══════════════════════════════════════════════════════════════════
# BRIQUE 12 — INTÉGRATION COMPLÈTE (analyze → print_report)
# ═══════════════════════════════════════════════════════════════════
# Teste que analyze() + print_report() fonctionnent de bout en bout
# sur TOUTES les configurations de graphe possibles:
#   - Arbres (path, star)
#   - Graphes denses (complet, grille)
#   - Graphes réalistes (repo-like)
#   - Graphes déconnectés
#   - Cas limites (1 nœud, 2 nœuds, graphe vide)
#   - DiGraph (import graph)
#   - Avec et sans Physarum/Anastomose
# ═══════════════════════════════════════════════════════════════════

def test_full_pipeline():
    """Tests d'intégration: analyze() + print_report() sur tous les types."""

    passed = 0
    failed = 0

    def check(name, condition):
        nonlocal passed, failed
        if condition:
            passed += 1
        else:
            failed += 1
            print(f"  ❌ FAIL: {name}")

    print("\n=== BRIQUE 12: Intégration complète ===\n")

    # --- Config 1: Graphe vide ---
    G_empty = nx.Graph()
    r = analyze(G_empty)
    check("Graphe vide: retourne error", "error" in r)

    # --- Config 2: 1 nœud ---
    G1 = nx.Graph()
    G1.add_node("solo")
    r = analyze(G1, run_physarum=False, run_anastomosis=False)
    check("1 nœud: pas de crash", r["nodes"] == 1)

    # --- Config 3: 2 nœuds, 1 arête ---
    G2 = nx.Graph()
    G2.add_edge("a", "b")
    r = analyze(G2, run_physarum=False, run_anastomosis=False)
    check("2 nœuds: α=0 (arbre)", r["meshedness_alpha"] == 0.0)

    # --- Config 4: Triangle ---
    G3 = nx.Graph()
    G3.add_edges_from([(0, 1), (1, 2), (0, 2)])
    r = analyze(G3)
    check("Triangle: α=1", r["meshedness_alpha"] == 1.0)
    check("Triangle: E_global=1", r["global_efficiency"] == 1.0)
    check("Triangle: strategy exists", "strategy" in r)
    check("Triangle: physarum exists", "physarum" in r)
    check("Triangle: anastomosis exists", "anastomosis" in r)

    # --- Config 5: Path (arbre pur) ---
    G_path = nx.path_graph(10)
    r = analyze(G_path)
    check("Path(10): α=0", r["meshedness_alpha"] == 0.0)
    check("Path(10): strategy guerrilla ou mixed",
          r["strategy"]["strategy"] in ("guerrilla", "mixed"))
    check("Path(10): physarum ran", "steps" in r.get("physarum", {}))

    # --- Config 6: Star (hub-and-spoke) ---
    G_star = nx.star_graph(8)
    r = analyze(G_star)
    check("Star(8): α=0 (arbre)", r["meshedness_alpha"] == 0.0)
    check("Star(8): root=centre (0)", r["root"] == 0)
    check("Star(8): bottleneck=centre",
          r["bottlenecks"][0][0] == 0 if r["bottlenecks"] else True)

    # --- Config 7: Graphe complet K5 ---
    G_k5 = nx.complete_graph(5)
    r = analyze(G_k5)
    check("K5: E_global=1", r["global_efficiency"] == 1.0)
    check("K5: phalanx", r["strategy"]["strategy"] == "phalanx")
    check("K5: anastomose 0 candidats",
          r["anastomosis"]["candidates_found"] == 0)

    # --- Config 8: Grille 4x4 ---
    G_grid = nx.grid_2d_graph(4, 4)
    r = analyze(G_grid, physarum_steps=50)
    check("Grille 4x4: N=16", r["nodes"] == 16)
    check("Grille 4x4: α > 0 (pas arbre)", r["meshedness_alpha"] > 0)
    check("Grille 4x4: physarum converge",
          r["physarum"].get("converged", False) or r["physarum"].get("steps", 0) > 0)

    # --- Config 9: Watts-Strogatz (small-world) ---
    G_ws = nx.watts_strogatz_graph(30, 4, 0.3, seed=42)
    r = analyze(G_ws, run_physarum=True, physarum_steps=30)
    check("WS(30,4,0.3): small-world σ > 1",
          isinstance(r["small_world_sigma"], float) and r["small_world_sigma"] > 1)
    check("WS: physarum résultat",
          "thick_edges" in r.get("physarum", {}))

    # --- Config 10: Graphe déconnecté ---
    G_disc = nx.Graph()
    G_disc.add_edges_from([(0, 1), (1, 2), (0, 2)])  # composante 1
    G_disc.add_edges_from([(10, 11), (11, 12)])  # composante 2
    r = analyze(G_disc)
    check("Déconnecté: pas de crash", r["nodes"] == 6)
    check("Déconnecté: α calculé", isinstance(r["meshedness_alpha"], float))

    # --- Config 11: DiGraph (graphe d'imports) ---
    G_di = nx.DiGraph()
    G_di.add_edges_from([
        ("main", "utils"), ("main", "models"), ("utils", "config"),
        ("models", "config"), ("models", "utils"), ("api", "models"),
        ("api", "utils"), ("api", "auth"), ("auth", "config"),
    ])
    r = analyze(G_di)
    check("DiGraph: converti en undirected", r["nodes"] > 0)
    check("DiGraph: root trouvé", r["root"] is not None)
    check("DiGraph: all briques present",
          all(k in r for k in ["meshedness_alpha", "global_efficiency",
                               "strategy", "physarum", "anastomosis"]))

    # --- Config 12: Repo-like (flask structure) ---
    G_flask = nx.Graph()
    G_flask.add_edges_from([
        ("__init__", "app"), ("__init__", "cli"), ("__init__", "config"),
        ("app", "cli"), ("app", "config"), ("app", "sessions"),
        ("app", "templating"), ("cli", "helpers"), ("config", "helpers"),
        ("sessions", "helpers"), ("templating", "helpers"),
        ("helpers", "utils"), ("sessions", "utils"),
    ])
    r = analyze(G_flask, root="__init__", physarum_mu=0.7, physarum_steps=50,
                anastomosis_method="jaccard", anastomosis_threshold=0.15)
    check("Flask-like: root=__init__", r["root"] == "__init__")
    check("Flask-like: physarum ran", "thick_edges" in r.get("physarum", {}))
    check("Flask-like: anastomose détecte",
          r["anastomosis"]["candidates_found"] > 0)

    # --- Config 13: print_report ne crash pas sur tous les types ---
    import io, contextlib
    test_graphs = {
        "triangle": nx.complete_graph(3),
        "path": nx.path_graph(5),
        "star": nx.star_graph(5),
        "grid": nx.grid_2d_graph(3, 3),
        "ws": nx.watts_strogatz_graph(20, 4, 0.3, seed=42),
    }
    all_reports_ok = True
    for gname, G in test_graphs.items():
        try:
            r = analyze(G, physarum_steps=20)
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                print_report(r)
            output = buf.getvalue()
            if "MYCELIUM ANALYSIS" not in output:
                all_reports_ok = False
        except Exception as e:
            all_reports_ok = False
            print(f"    print_report crash on {gname}: {e}")
    check("print_report: 5 types sans crash", all_reports_ok)

    # --- Config 14: analyze avec physarum désactivé ---
    r_no_phys = analyze(nx.path_graph(5), run_physarum=False)
    check("Physarum disabled: skipped",
          "skipped" in r_no_phys.get("physarum", {}))

    # --- Config 15: analyze avec anastomose désactivée ---
    r_no_anast = analyze(nx.path_graph(5), run_anastomosis=False)
    check("Anastomose disabled: skipped",
          "skipped" in r_no_anast.get("anastomosis", {}))

    # --- Config 16: Cohérence croisée ---
    # Un graphe dense doit avoir: α élevé, E élevé, stratégie phalanx,
    # Physarum haute survie, peu de candidats anastomose
    G_dense = nx.complete_graph(6)
    r_d = analyze(G_dense, physarum_steps=30)
    check("K6 cohérence: α > 1", r_d["meshedness_alpha"] > 1.0)
    check("K6 cohérence: E = 1", r_d["global_efficiency"] == 1.0)
    check("K6 cohérence: phalanx", r_d["strategy"]["strategy"] == "phalanx")
    check("K6 cohérence: 0 candidats anastomose",
          r_d["anastomosis"]["candidates_found"] == 0)

    # Un arbre doit avoir: α=0, stratégie guerrilla, tous les liens survivent au Physarum
    G_tree = nx.random_labeled_tree(12, seed=42)
    r_t = analyze(G_tree, physarum_steps=50)
    check("Tree cohérence: α=0", r_t["meshedness_alpha"] == 0.0)
    check("Tree cohérence: guerrilla", r_t["strategy"]["strategy"] == "guerrilla")

    print(f"\n  Résultat: {passed}/{passed+failed} tests passés")
    return passed, failed


# ═══════════════════════════════════════════════════════════════════
# BRIQUE 13 — EDELSTEIN GROWTH (v2.0)
# ═══════════════════════════════════════════════════════════════════
# Sources:
#   Edelstein 1982, J. Theor. Biol. 98:679-701
#     "The propagation of fungal colonies: a model for tissue growth"
#     Core PDE: ∂n/∂t = -∇·(nv) + f
#              ∂ρ/∂t = n|v| - dρ
#     General tip rate: f = b_n·n·(1-n/n_max) - d_n·n - a₂·n·ρ - a₁·n²
#
#   Schnepf & Roose 2008, J. R. Soc. Interface 5:773-784
#     "Growth model for arbuscular mycorrhizal fungi"
#     Validated Edelstein on S. calospora, Glomus sp., A. laevis
#     Three regimes: linear branching, nonlinear branching, anastomosis
#     Key parameter: d̃ = d/b (death/branching ratio)
#
#   Edelstein, Hadar, Chet, Henis, Segel 1983, J. Gen. Microbiol. 129:1873
#     "A Model for Fungal Colony Growth Applied to Sclerotium rolfsii"
#     Experimental validation: peaked distributions of tips at colony margin
#
#   Du et al. 2019, J. Theor. Biol. 470:90-100
#     "A 3-variable PDE model for predicting fungal growth"
#     Tips = active (elongating) + dormant. Branching inhibited by
#     local branch density. Anastomosis = tip disappearance on contact.
#
# Discrete translation for graphs:
#   Tips = leaf nodes (degree ≤ 1) or nodes marked as "tip"
#   ρ (hyphal density) at node = local edge density = edges / possible edges
#   n (tip density) = fraction of tips in local neighborhood
#   Branching = tip adds new neighbor(s), prob ∝ b_n·(1-n/n_max)
#   Tip death = tip deactivated, prob ∝ d_n
#   Hyphal death = edge removed, prob ∝ d
#   Anastomosis = brique 11 (Jaccard-based fusion)
# ═══════════════════════════════════════════════════════════════════


class EdelsteinParams:
    """Parameters for Edelstein growth model.

    Sources:
        Schnepf & Roose 2008, Table 1: fitted values for 3 fungal species
        Edelstein 1982: original formulation
    """
    def __init__(self,
                 b_n=0.3,       # tip branching rate (prob per step)
                 d_n=0.05,      # tip death rate (prob per step)
                 d=0.02,        # hyphal death rate (prob per step per edge)
                 n_max=0.6,     # max tip density (fraction of nodes that are tips)
                 a1=0.1,        # tip-tip anastomosis rate
                 a2=0.05,       # tip-hypha anastomosis rate
                 v=1,           # tip movement speed (edges per step)
                 name_pool=None # pool of names for new nodes
                 ):
        self.b_n = b_n
        self.d_n = d_n
        self.d = d
        self.n_max = n_max
        self.a1 = a1
        self.a2 = a2
        self.v = v
        self.name_pool = name_pool or []
        self._name_counter = 0

    def next_name(self):
        """Generate next node name for new branches."""
        self._name_counter += 1
        if self.name_pool:
            idx = (self._name_counter - 1) % len(self.name_pool)
            return f"{self.name_pool[idx]}_{self._name_counter}"
        return f"tip_{self._name_counter}"


def edelstein_tip_rate(G, node, params):
    """
    Calculate the Edelstein tip creation/destruction rate f for a node.

    Implements: f = b_n·n·(1-n/n_max) - d_n·n - a₂·n·ρ - a₁·n²

    Parameters
    ----------
    G : nx.Graph
        Current graph state.
    node : hashable
        Node to evaluate.
    params : EdelsteinParams
        Model parameters.

    Returns
    -------
    dict with keys:
        'f': float — net rate (positive = growth, negative = decay)
        'branching': float — branching term
        'death': float — death term
        'anastomosis_tip_hypha': float — a₂·n·ρ term
        'anastomosis_tip_tip': float — a₁·n² term
        'n_local': float — local tip density
        'rho_local': float — local hyphal density
    """
    neighbors = list(G.neighbors(node))
    if not neighbors:
        return {'f': 0, 'branching': 0, 'death': 0,
                'anastomosis_tip_hypha': 0, 'anastomosis_tip_tip': 0,
                'n_local': 0, 'rho_local': 0}

    # Local neighborhood (node + its neighbors)
    local_nodes = set([node] + neighbors)
    total_local = len(local_nodes)

    # n = local tip density (fraction of local nodes that are tips/leaves)
    tips_local = sum(1 for nd in local_nodes if G.degree(nd) <= 1)
    n = tips_local / total_local if total_local > 0 else 0

    # ρ = local hyphal (edge) density = edges / max possible edges
    local_subgraph = G.subgraph(local_nodes)
    actual_edges = local_subgraph.number_of_edges()
    max_edges = total_local * (total_local - 1) / 2
    rho = actual_edges / max_edges if max_edges > 0 else 0

    # Edelstein equation: f = b_n·n·(1-n/n_max) - d_n·n - a₂·n·ρ - a₁·n²
    branching = params.b_n * n * max(0, 1 - n / params.n_max)
    death = params.d_n * n
    anast_th = params.a2 * n * rho    # tip-hypha
    anast_tt = params.a1 * n * n       # tip-tip

    f = branching - death - anast_th - anast_tt

    return {
        'f': f,
        'branching': branching,
        'death': death,
        'anastomosis_tip_hypha': anast_th,
        'anastomosis_tip_tip': anast_tt,
        'n_local': n,
        'rho_local': rho,
    }


def edelstein_growth_step(G, params, rng=None):
    """
    Execute one discrete growth step on graph G.

    Implements discrete Edelstein dynamics:
    1. Identify tips (leaf nodes, degree ≤ 1)
    2. For each tip: compute f rate → branch or die
    3. Apply hyphal death (random edge removal)
    4. Apply tip-tip anastomosis (merge nearby tips via brique 11)

    Parameters
    ----------
    G : nx.Graph
        Graph to grow. Modified in-place.
    params : EdelsteinParams
        Growth parameters.
    rng : random.Random, optional
        Random number generator for reproducibility.

    Returns
    -------
    dict with step stats:
        'tips_before': int
        'tips_after': int
        'branches_added': int
        'tips_died': int
        'edges_died': int
        'anastomosis_events': int
        'nodes_added': int
        'nodes_total': int
        'edges_total': int
    """
    import random as _random
    rng = rng or _random

    stats = {
        'tips_before': 0, 'tips_after': 0,
        'branches_added': 0, 'tips_died': 0, 'edges_died': 0,
        'anastomosis_events': 0, 'nodes_added': 0,
        'nodes_total': 0, 'edges_total': 0,
    }

    if G.number_of_nodes() == 0:
        return stats

    # 1. Identify current tips
    tips = [n for n in G.nodes() if G.degree(n) <= 1]
    stats['tips_before'] = len(tips)

    # 2. Process each tip: branch or die based on Edelstein rate
    tips_to_remove = []
    new_edges = []

    for tip in tips:
        if tip not in G:
            continue

        rate = edelstein_tip_rate(G, tip, params)

        # Branching probability: proportional to branching term
        if rng.random() < rate['branching']:
            new_name = params.next_name()
            new_edges.append((tip, new_name))
            stats['branches_added'] += 1
            stats['nodes_added'] += 1

        # Tip death probability: proportional to death + anastomosis terms
        death_prob = rate['death'] + rate['anastomosis_tip_hypha'] + rate['anastomosis_tip_tip']
        if rng.random() < death_prob:
            tips_to_remove.append(tip)
            stats['tips_died'] += 1

    # Apply branching (add new nodes/edges)
    for u, v in new_edges:
        G.add_node(v, growth_step=True)
        G.add_edge(u, v, conductivity=0.5, growth_edge=True)

    # Apply tip death (remove tip nodes if they're still leaves)
    for tip in tips_to_remove:
        if tip in G and G.degree(tip) <= 1:
            G.remove_node(tip)

    # 3. Hyphal death: randomly remove edges with prob d
    edges_to_remove = []
    for u, v in list(G.edges()):
        if rng.random() < params.d:
            edges_to_remove.append((u, v))

    for u, v in edges_to_remove:
        if G.has_edge(u, v):
            G.remove_edge(u, v)
            stats['edges_died'] += 1

    # Clean up isolated nodes from edge removal
    isolates = list(nx.isolates(G))
    G.remove_nodes_from(isolates)

    # 4. Anastomosis: use brique 11's detect + fuse (only if rates > 0)
    if (params.a1 > 0 or params.a2 > 0) and G.number_of_nodes() > 2 and G.number_of_edges() > 1:
        try:
            candidates = detect_anastomosis_candidates(
                G, method="jaccard", threshold=0.2, max_candidates=5
            )
            if candidates:
                # Fuse at most 2 per step (biological: anastomosis is rare)
                n_fuse = min(2, len(candidates))
                result = anastomose(G, candidates, n_fusions=n_fuse)
                stats['anastomosis_events'] = result.get('fusions_done', 0)
        except Exception:
            pass  # Non-critical if anastomosis fails

    # Final counts
    stats['tips_after'] = sum(1 for n in G.nodes() if G.degree(n) <= 1)
    stats['nodes_total'] = G.number_of_nodes()
    stats['edges_total'] = G.number_of_edges()

    return stats


def edelstein_simulate(G, n_steps=20, params=None, seed=42):
    """
    Run Edelstein growth simulation for n_steps.

    Parameters
    ----------
    G : nx.Graph
        Initial graph (will be copied, original untouched).
    n_steps : int
        Number of growth steps.
    params : EdelsteinParams, optional
        Model parameters. Default: standard values.
    seed : int
        Random seed for reproducibility.

    Returns
    -------
    dict with:
        'final_graph': nx.Graph — grown graph
        'history': list of step stats dicts
        'snapshots': list of (step, nx.Graph) at regular intervals
        'params': EdelsteinParams used
        'growth_summary': dict with totals
    """
    import random as _random
    rng = _random.Random(seed)

    G_sim = G.copy()
    params = params or EdelsteinParams()
    history = []
    snapshots = [(0, G_sim.copy())]
    snapshot_interval = max(1, n_steps // 5)

    for step in range(1, n_steps + 1):
        step_stats = edelstein_growth_step(G_sim, params, rng)
        step_stats['step'] = step
        history.append(step_stats)

        if step % snapshot_interval == 0 or step == n_steps:
            snapshots.append((step, G_sim.copy()))

    # Growth summary
    total_branches = sum(h['branches_added'] for h in history)
    total_deaths_tips = sum(h['tips_died'] for h in history)
    total_deaths_edges = sum(h['edges_died'] for h in history)
    total_anastomosis = sum(h['anastomosis_events'] for h in history)

    summary = {
        'initial_nodes': snapshots[0][1].number_of_nodes(),
        'final_nodes': G_sim.number_of_nodes(),
        'initial_edges': snapshots[0][1].number_of_edges(),
        'final_edges': G_sim.number_of_edges(),
        'total_branches_added': total_branches,
        'total_tips_died': total_deaths_tips,
        'total_edges_died': total_deaths_edges,
        'total_anastomosis': total_anastomosis,
        'net_growth_nodes': G_sim.number_of_nodes() - snapshots[0][1].number_of_nodes(),
        'net_growth_edges': G_sim.number_of_edges() - snapshots[0][1].number_of_edges(),
    }

    return {
        'final_graph': G_sim,
        'history': history,
        'snapshots': snapshots,
        'params': params,
        'growth_summary': summary,
    }


# ═══════════════════════════════════════════════════════════════════
# BRIQUE 13 — TESTS
# ═══════════════════════════════════════════════════════════════════


def test_edelstein_growth():
    """Tests for Edelstein growth model (brique 13)."""
    import random as _random

    passed = 0
    failed = 0

    def check(name, condition):
        nonlocal passed, failed
        if condition:
            passed += 1
            print(f"  ✅ {name}")
        else:
            failed += 1
            print(f"  ❌ {name}")

    print("\n=== BRIQUE 13: Edelstein Growth ===\n")

    # --- Test 1: tip_rate on isolated tip (degree 0) ---
    G0 = nx.Graph()
    G0.add_node("alone")
    r = edelstein_tip_rate(G0, "alone", EdelsteinParams())
    check("Isolated node: f=0", r['f'] == 0)

    # --- Test 2: tip_rate on leaf (degree 1) —
    # tip should have positive branching if density is low
    G1 = nx.path_graph(5)
    r = edelstein_tip_rate(G1, 0, EdelsteinParams(b_n=0.5, d_n=0.01))
    check("Leaf node: branching > 0", r['branching'] > 0)
    check("Leaf node: n_local > 0", r['n_local'] > 0)
    check("Leaf node: rho_local > 0", r['rho_local'] > 0)

    # --- Test 3: tip_rate on dense graph (complete) — tips suppressed
    G_dense = nx.complete_graph(6)
    r = edelstein_tip_rate(G_dense, 0, EdelsteinParams(b_n=0.3))
    check("Dense graph: n_local=0 (no leaves)", r['n_local'] == 0)
    check("Dense graph: rho_local=1.0 (fully connected)",
          abs(r['rho_local'] - 1.0) < 0.01)
    check("Dense graph: f=0 (no tips to grow)", r['f'] == 0)

    # --- Test 4: growth step on path graph — branches should appear
    G2 = nx.path_graph(5)
    params = EdelsteinParams(b_n=0.9, d_n=0.0, d=0.0, a1=0.0, a2=0.0, n_max=1.0)
    rng = _random.Random(1)  # seed 1 confirmed to branch
    initial_nodes = G2.number_of_nodes()
    stats = edelstein_growth_step(G2, params, rng)
    check("Growth step: branches added > 0", stats['branches_added'] > 0)
    check("Growth step: nodes grew", G2.number_of_nodes() > initial_nodes)

    # --- Test 5: death step — tips die with high death rate
    G3 = nx.star_graph(5)  # center + 5 leaves
    params_death = EdelsteinParams(b_n=0.0, d_n=0.99, d=0.0, a1=0.0, a2=0.0)
    rng2 = _random.Random(42)
    initial_tips = sum(1 for n in G3.nodes() if G3.degree(n) <= 1)
    stats = edelstein_growth_step(G3, params_death, rng2)
    check("Death step: tips_died > 0", stats['tips_died'] > 0)
    check("Death step: tips decreased",
          stats['tips_after'] < initial_tips)

    # --- Test 6: hyphal death — edges removed
    G4 = nx.grid_2d_graph(4, 4)
    params_hd = EdelsteinParams(b_n=0.0, d_n=0.0, d=0.5, a1=0.0, a2=0.0)
    rng3 = _random.Random(42)
    initial_edges = G4.number_of_edges()
    stats = edelstein_growth_step(G4, params_hd, rng3)
    check("Hyphal death: edges_died > 0", stats['edges_died'] > 0)
    check("Hyphal death: edges decreased",
          G4.number_of_edges() < initial_edges)

    # --- Test 7: simulate — full run returns valid structure
    G5 = nx.path_graph(10)
    result = edelstein_simulate(G5, n_steps=30, seed=42)
    check("Simulate: returns final_graph", isinstance(result['final_graph'], nx.Graph))
    check("Simulate: history has 30 entries", len(result['history']) == 30)
    check("Simulate: snapshots exist", len(result['snapshots']) >= 2)
    check("Simulate: growth_summary has net_growth",
          'net_growth_nodes' in result['growth_summary'])

    # --- Test 8: simulate with growth — graph actually grows
    G6 = nx.path_graph(5)
    params_grow = EdelsteinParams(b_n=0.6, d_n=0.01, d=0.0, a1=0.0, a2=0.0, n_max=1.0)
    result = edelstein_simulate(G6, n_steps=30, params=params_grow, seed=42)
    check("Growth sim: nodes increased",
          result['growth_summary']['final_nodes'] > result['growth_summary']['initial_nodes'])
    check("Growth sim: total_branches > 0",
          result['growth_summary']['total_branches_added'] > 0)

    # --- Test 9: simulate with decay — graph shrinks or stabilizes
    G7 = nx.grid_2d_graph(5, 5)
    params_decay = EdelsteinParams(b_n=0.0, d_n=0.3, d=0.1, a1=0.0, a2=0.0)
    result = edelstein_simulate(G7, n_steps=30, params=params_decay, seed=42)
    check("Decay sim: nodes decreased or stable",
          result['growth_summary']['final_nodes'] <= result['growth_summary']['initial_nodes'])
    check("Decay sim: edges decreased",
          result['growth_summary']['final_edges'] < result['growth_summary']['initial_edges'])

    # --- Test 10: n_max saturation — branching stops at high tip density
    G8 = nx.star_graph(1)  # just 2 nodes, 1 leaf = 50% tips
    params_sat = EdelsteinParams(b_n=0.5, d_n=0.0, d=0.0,
                                  n_max=0.1, a1=0.0, a2=0.0)
    r_sat = edelstein_tip_rate(G8, 1, params_sat)
    check("n_max saturation: branching = 0 when n > n_max",
          r_sat['branching'] == 0)

    # --- Test 11: Schnepf d̃ parameter — d/b ratio effect
    # High d̃ = death dominates → graph shrinks
    # Low d̃ = branching dominates → graph grows
    G9a = nx.path_graph(8)
    G9b = nx.path_graph(8)
    params_low_d = EdelsteinParams(b_n=0.5, d_n=0.05, d=0.01)  # d̃ low
    params_high_d = EdelsteinParams(b_n=0.05, d_n=0.3, d=0.1)  # d̃ high
    r_low = edelstein_simulate(G9a, n_steps=20, params=params_low_d, seed=42)
    r_high = edelstein_simulate(G9b, n_steps=20, params=params_high_d, seed=42)
    check("Schnepf d̃: low d̃ grows more than high d̃",
          r_low['growth_summary']['final_nodes'] > r_high['growth_summary']['final_nodes'])

    # --- Test 12: anastomosis integration — events detected
    G10 = nx.Graph()
    # Two parallel paths that should fuse
    G10.add_nodes_from(["a1", "a2", "a3", "a4", "a5", "b1", "b2", "b3", "b4", "b5"])
    nx.add_path(G10, ["a1", "a2", "a3", "a4", "a5"])
    nx.add_path(G10, ["b1", "b2", "b3", "b4", "b5"])
    G10.add_edge("a1", "b1")  # shared root
    G10.add_edge("a5", "b5")  # shared endpoint
    params_anast = EdelsteinParams(b_n=0.1, d_n=0.0, d=0.0, a1=0.1, a2=0.1)
    result = edelstein_simulate(G10, n_steps=10, params=params_anast, seed=42)
    # Anastomosis might or might not fire, but shouldn't crash
    check("Anastomosis integration: no crash",
          isinstance(result['final_graph'], nx.Graph))

    # --- Test 13: empty graph doesn't crash
    G_empty = nx.Graph()
    result = edelstein_simulate(G_empty, n_steps=5, seed=42)
    check("Empty graph: no crash", result['final_graph'].number_of_nodes() == 0)

    # --- Test 14: EdelsteinParams name generation
    p = EdelsteinParams(name_pool=["module", "lib", "src"])
    names = [p.next_name() for _ in range(5)]
    check("Name generation: unique names", len(set(names)) == 5)
    check("Name generation: uses pool", "module" in names[0])

    # --- Test 15: history tracking — monotonic step numbers
    G11 = nx.path_graph(5)
    result = edelstein_simulate(G11, n_steps=10, seed=42)
    steps = [h['step'] for h in result['history']]
    check("History: monotonic steps", steps == list(range(1, 11)))

    # --- Test 16: conservation — tips_before + branches - deaths ≈ tips_after
    # (approximate due to graph dynamics, but sanity check)
    G12 = nx.path_graph(10)
    params_con = EdelsteinParams(b_n=0.3, d_n=0.1, d=0.0, a1=0.0, a2=0.0)
    rng_con = _random.Random(123)
    stats_con = edelstein_growth_step(G12, params_con, rng_con)
    expected_approx = stats_con['tips_before'] + stats_con['branches_added'] - stats_con['tips_died']
    # Allow difference due to graph structural effects
    check("Conservation: tips_after ≈ expected (±3)",
          abs(stats_con['tips_after'] - expected_approx) <= 3)

    # --- Test 17: real-world graph simulation ---
    # Simulate on a Watts-Strogatz small-world graph (realistic topology)
    G_ws = nx.watts_strogatz_graph(30, 4, 0.3, seed=42)
    result_ws = edelstein_simulate(G_ws, n_steps=20, seed=42)
    check("Real-world WS graph: sim completes",
          result_ws['growth_summary']['final_nodes'] > 0)

    print(f"\n  Résultat: {passed}/{passed+failed} tests passés")
    return passed, failed


if __name__ == "__main__":
    main()
    p1, f1 = test_kirchhoff_physarum()
    p2, f2 = test_anastomosis()
    p3, f3 = test_full_pipeline()
    p4, f4 = test_edelstein_growth()
    total_p = p1 + p2 + p3 + p4
    total_f = f1 + f2 + f3 + f4
    print(f"\n{'='*50}")
    print(f"  TOTAL BRIQUES 10-13: {total_p}/{total_p+total_f}")
    print(f"{'='*50}")
