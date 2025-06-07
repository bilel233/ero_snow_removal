#!/usr/bin/env python3

import argparse
import os
import pickle
import sys
from pathlib import Path
import networkx as nx
import osmnx as ox

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(HERE, ".."))
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from drone.model import chinese_postman
from carp_mvp import CARPSolver, analyze_solution_quality

def load_pickle_graph(path: str):
    with open(path, "rb") as f:
        return pickle.load(f)


def build_route_nodes(G: nx.Graph, depot: int, edges):
  
    route = [depot]
    cur = depot

    for u, v, _ in edges:
       
        if cur not in (u, v):
            sp = nx.shortest_path(G, cur, u, weight="length")
            route.extend(sp[1:])  
            cur = u
       
        nxt = v if cur == u else u
        route.append(nxt)
        cur = nxt

    if cur != depot:
        sp = nx.shortest_path(G, cur, depot, weight="length")
        route.extend(sp[1:])
    return route

def demo_drone(graph_path: str, out_png: str):
    G = load_pickle_graph(graph_path)
    path_nodes, dist_m = chinese_postman(G)
    print(f"Drone tour length : {dist_m/1000:.2f} km")

    fig, _ = ox.plot_graph_route(
        G.to_undirected(), path_nodes,
        node_size=0, route_color="red", route_linewidth=1,
        bgcolor="white", show=False, close=False
    )
    Path(out_png).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png, dpi=200, bbox_inches="tight")
    print("Map written to", out_png)


def demo_vehicle(graph_path: str, capacity_h: float, out_png: str | None):
    G = load_pickle_graph(graph_path)

    if not any(d.get("required", False) for _, _, d in G.edges(data=True)):
        print(" No 'required' edges found – flagging every edge as required for demo.")
        for _, _, d in G.edges(data=True):
            d["required"] = True

    solver = CARPSolver(capacity_limit=capacity_h)
    solver.depot_node = next(iter(G.nodes())) 

    tours = solver.compute_tournees(G, strategy="mixed")
    stats = analyze_solution_quality(tours)

    print("=== CARP stats ===")
    for k, v in stats.items():
        print(f"{k}: {v}")

    if out_png and tours:
        nodes_seq = build_route_nodes(G, solver.depot_node, tours[0]["edges"])
        fig, _ = ox.plot_graph_route(
            G.to_undirected(), nodes_seq,
            node_size=0, route_color="blue", route_linewidth=1,
            bgcolor="white", show=False, close=False
        )
        Path(out_png).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(out_png, dpi=200, bbox_inches="tight")
        print("Map written to", out_png)

def main():
    p = argparse.ArgumentParser(description="Demo ERO Snow Removal")
    sub = p.add_subparsers(dest="cmd", required=True)

    pd = sub.add_parser("drone", help="Run Chinese‑Postman tour on full graph")
    pd.add_argument("--graph", required=True, help="Pickle graph file")
    pd.add_argument("--out", required=True, help="Output PNG path")

    pv = sub.add_parser("vehicle", help="Run CARP solver on sector graph")
    pv.add_argument("--sector", required=True, help="Pickle sector graph file")
    pv.add_argument("--capacity", type=float, default=8.0, help="Vehicle time capacity (h)")
    pv.add_argument("--out", help="Output PNG path for first tour (optional)")

    args = p.parse_args()
    if args.cmd == "drone":
        demo_drone(args.graph, args.out)
    else:
        demo_vehicle(args.sector, args.capacity, args.out)


if __name__ == "__main__":
    main()
