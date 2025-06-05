# src/drone/model.py
from pathlib import Path
import networkx as nx
from typing import List, Tuple

def chinese_postman(G: nx.MultiDiGraph, weight: str = "length") -> Tuple[List[Tuple[int, int]], float]:
    """
    Résout le Chinese Postman sur un graphe routier orienté en
    le traitant d'abord comme non‐orienté (pour le drone).
    Returns:
      - circuit: liste d'arêtes (u, v) dans l'ordre eulérien (dans G_und)
      - total_dist: distance totale parcourue en mètres
    """
    
    G_und = nx.Graph()
    for u, v, data in G.edges(data=True):
        w = data.get(weight, 1.0)
        if G_und.has_edge(u, v):
            if w < G_und[u][v]["weight"]:
                G_und[u][v]["weight"] = w
        else:
            G_und.add_edge(u, v, weight=w)   
    odds = [v for v, d in G_und.degree() if d % 2 == 1]
    dists = dict(nx.all_pairs_dijkstra_path_length(G_und, weight="weight"))
    K = nx.Graph()
    for i, u in enumerate(odds):
        for v in odds[i + 1:]:
            K.add_edge(u, v, weight=dists[u][v])
    matches = nx.algorithms.matching.min_weight_matching(K, weight="weight")
    G_aug = nx.MultiGraph(G_und)         
    for u, v in matches:
        path = nx.shortest_path(G_und, u, v, weight="weight")
        for a, b in zip(path[:-1], path[1:]):
            w = G_und[a][b]["weight"]
            G_aug.add_edge(a, b, weight=w, added=1)   
    circuit_edges = list(nx.eulerian_circuit(G_aug)) 
    total_dist = 0.0
    nodes_path = []        
    for edge in circuit_edges:
        u, v = edge[0], edge[1]
        k = edge[2] if len(edge) == 3 else 0
        w = G_aug[u][v][k]["weight"] if isinstance(G_aug, nx.MultiGraph) else G_aug[u][v]["weight"]
        total_dist += w
        nodes_path.append(u)
    nodes_path.append(circuit_edges[0][0])

    return nodes_path, total_dist
