import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import time
from carp_mvp import CARPSolver, analyze_solution_quality, benchmark_strategies

def create_montreal_like_graph():
    G = nx.Graph()
    np.random.seed(42)

    for i in range(8):
        for j in range(8):
            node = i * 8 + j
            if j < 7:
                right_node = i * 8 + (j + 1)
                length = np.random.normal(800, 200)
                required = np.random.random() > 0.3
                G.add_edge(node, right_node, length_m=max(400, int(length)), required=required)
            if i < 7:
                down_node = (i + 1) * 8 + j
                length = np.random.normal(1000, 300)
                required = np.random.random() > 0.25
                G.add_edge(node, down_node, length_m=max(500, int(length)), required=required)
    
    return G

def visualize_solution(G, tournees, title="Solution CARP"):
    plt.figure(figsize=(12, 8))
    pos = {n: (n % 8, 7 - (n // 8)) for n in G.nodes}
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']

    nx.draw_networkx_nodes(G, pos, node_color='lightgray', node_size=100)

    for u, v in G.edges():
        if not G[u][v].get('required', False):
            nx.draw_networkx_edges(G, pos, [(u, v)], edge_color='lightgray', width=0.5)

    for i, tournee in enumerate(tournees):
        color = colors[i % len(colors)]
        edges = [(u, v) for u, v, _ in tournee['edges']]
        nx.draw_networkx_edges(G, pos, edges, edge_color=color, width=3, alpha=0.7)

    depot_node = 0
    nx.draw_networkx_nodes(G, pos, [depot_node], node_color='red', node_size=200, node_shape='s')

    plt.title(title, fontsize=16)
    plt.axis('off')
    plt.tight_layout()
    plt.show()

def live_demo():
    print("=== DEMONSTRATION LIVE ===")
    print("Création du graphe de Montréal fictif...")
    G = create_montreal_like_graph()

    required = [(u, v, d) for u, v, d in G.edges(data=True) if d.get('required')]
    print(f"{len(required)} routes à déneiger.")

    print("Lancement de l’algorithme...")
    solver = CARPSolver()
    start = time.time()
    tournees = solver.compute_tournees(G, strategy="mixed")
    duration = time.time() - start

    print(f"{len(tournees)} tournées générées en {duration:.2f} secondes")

    for t in tournees:
        print(f"  Tournée {t['id']}: {t['km']} km | {t['hours']} h | {t['utilization']}%")

    print("\nAffichage de la carte...")
    visualize_solution(G, tournees)

if __name__ == "__main__":
    live_demo()

