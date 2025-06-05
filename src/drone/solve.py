#!/usr/bin/env python
import argparse, pickle
import networkx as nx, osmnx as ox
from .model import chinese_postman
from pathlib import Path

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--graph", required=True, help="pickle .pkl")
    p.add_argument("--out",   required=True, help="PNG à créer")
    args = p.parse_args()
    
    with open(args.graph, "rb") as f:
        G = pickle.load(f)
    nodes_path, dist = chinese_postman(G)
    print(f"Distance minimale : {dist/1000:.2f} km")
    G_plot = G.to_undirected()
    fig, ax = ox.plot_graph_route(
        G_plot, nodes_path,
        node_size=0, bgcolor="white",
        route_color="red", route_linewidth=1
    )

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.out, dpi=200, bbox_inches="tight")

if __name__ == "__main__":
    main()
