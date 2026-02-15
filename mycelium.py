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

def analyze(G_input, root: str = None) -> dict:
    """Analyse complète d'un graphe.

    Args:
        G_input: nx.Graph ou nx.DiGraph
        root: nœud racine (entry point). Si None, prend le plus connecté.

    Returns:
        dict avec toutes les métriques
    """
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

    # --- Métriques de base ---
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

    # --- Robustesse (seulement si pas trop gros) ---
    if N <= 500:
        rob = robustness_test(G, attack="betweenness", steps=min(N // 2, 20))
        # Trouver la fraction connectée quand 50% des nœuds sont supprimés
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

    # --- Small-world (seulement si connexe et pas trop gros) ---
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

    # --- Stratégie ---
    strat = classify_strategy(alpha, e_global, e_root, rob_50)
    result["strategy"] = strat

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
    print(f"  E_root ({report['root'][:15]}): {e_root:.4f}  [{er_bar}]")

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

    print(f"\n{'=' * 60}")


# ============================================================================
# CLI
# ============================================================================

def main():
    """Point d'entrée CLI."""

    if len(sys.argv) < 2:
        print("""
🍄 MYCELIUM ENGINE v0.1
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


if __name__ == "__main__":
    main()
