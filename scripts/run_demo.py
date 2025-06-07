import argparse
import pandas as pd
import networkx as nx

def load_graph(path):
    """Charge le CSV des tronçons et crée un graphe orienté avec attribut 'length'."""
    df = pd.read_csv(path)
    G = nx.from_pandas_edgelist(df, source='u', target='v', edge_attr='length', create_using=nx.DiGraph())
    return G


def chinese_postman_cost(G):
    """Calcule la somme des longueurs de tous les arcs (approximation de coût)."""
    return sum(data['length'] for u, v, data in G.edges(data=True))


def main(sector, fleet):
    """Point d'entrée : calcule un coût total basique pour un secteur donné."""
    csv_path = f"data/{sector}_edges.csv"
    G = load_graph(csv_path)
    cost = chinese_postman_cost(G)
    print(f"Total length = {cost:.1f} m")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Démo ERO Snow Removal: coût simplifié.")
    parser.add_argument("--sector", default="outremont", help="Nom du secteur (par défaut: outremont)")
    parser.add_argument("--fleet", default="2:I,1:II", help="Configuration flotte (ex: '2:I,1:II')")
    args = parser.parse_args()
    main(args.sector, args.fleet)

