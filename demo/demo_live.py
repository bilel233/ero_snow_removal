#!/usr/bin/env python3
from __future__ import annotations
import argparse
import pathlib
import pickle
from typing import Dict, Tuple, List
import matplotlib
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import networkx as nx

if matplotlib.get_backend() == "Agg":
    print("[INFO] Backend 'Agg' détecté : aucune fenêtre interactive – une vidéo sera exportée.")

NODE_POS_KEYS = ["pos", ("x", "y"), ("lon", "lat"), ("long", "lat")]

def load_graph_pickle(path: str | pathlib.Path) -> nx.Graph:
    with open(path, "rb") as f:
        return pickle.load(f)

def get_node_positions(G: nx.Graph) -> Dict[int, Tuple[float, float]]:
    
    if all("pos" in G.nodes[n] for n in G.nodes):
        return {n: tuple(G.nodes[n]["pos"]) for n in G.nodes}
    
    for pair in NODE_POS_KEYS[1:]:
        kx, ky = pair if isinstance(pair, tuple) else (pair, pair)
        if all(kx in G.nodes[n] and ky in G.nodes[n] for n in G.nodes):
            return {n: (float(G.nodes[n][kx]), float(G.nodes[n][ky])) for n in G.nodes}
 
    print("[WARN] positions manquantes – génération d'un spring_layout…")
    return nx.spring_layout(G, seed=42)

def make_undirected(G: nx.Graph) -> nx.MultiGraph:
    if G.is_directed():
        G = G.to_undirected(as_view=False)
    if not G.is_multigraph():
        G = nx.MultiGraph(G)
    return G

def compute_eulerian_tour(G: nx.Graph):
    H = make_undirected(G)
    if not nx.is_eulerian(H):
        H = nx.eulerize(H)
    return list(nx.eulerian_circuit(H)), H

def animate(
    G: nx.Graph,
    pos: Dict[int, Tuple[float, float]],
    tour: List[Tuple[int, int]],
    *,
    speed: float,
    interval: int,
    outfile: str = "animation_out.mp4",
    blit: bool = False,
) -> None:
    fig, ax = plt.subplots()
    ax.set_aspect("equal")
    ax.axis("off")
    nx.draw_networkx_nodes(G, pos, node_size=8, ax=ax)
    nx.draw_networkx_edges(G, pos, alpha=0.15, ax=ax)

    vehicle, = ax.plot([], [], "ro", markersize=6)

    segments = [(pos[u], pos[v]) for u, v in tour]
    steps_per_segment = 10
    total_frames = len(segments) * steps_per_segment

    def init():
        vehicle.set_data([], [])
        return vehicle,

    def update(frame: int):
        seg_idx, step = divmod(frame, steps_per_segment)
        start, end = segments[seg_idx]
        t = step / steps_per_segment
        x = start[0] + (end[0] - start[0]) * t
        y = start[1] + (end[1] - start[1]) * t
        vehicle.set_data([x], [y])
        if step == 0:
            ax.plot([start[0], end[0]], [start[1], end[1]], color="gray", linewidth=2)
        return vehicle,

    ani = animation.FuncAnimation(
        fig,
        update,
        frames=total_frames,
        init_func=init,
        interval=int(interval / speed),
        repeat=False,
        blit=blit,
    )

    if matplotlib.get_backend() == "Agg":
        ani.save(outfile, writer="ffmpeg", fps=max(1, int(1000 / interval)))
        print(f"[OK] Vidéo enregistrée → {outfile}")
    else:
        plt.show()

def parse_args():
    p = argparse.ArgumentParser(description="Animation d’une tournée de déneigement")
    grp = p.add_mutually_exclusive_group(required=True)
    grp.add_argument("--sector", type=str, help="Nom du secteur pré‑traité (Outremont, Verdun, …)")
    grp.add_argument("--graph", type=str, help="Chemin vers un pickle NetworkX")
    grp.add_argument("--size", type=int, help="Taille n pour générer une grille n×n de test")
    p.add_argument("--speed", type=float, default=1.0, help="Facteur de vitesse (1 = temps réel)")
    p.add_argument("--interval", type=int, default=100, help="Intervalle ms entre frames (≥30 recommandé)")
    p.add_argument("--out", type=str, default="animation_out.mp4", help="Nom du fichier MP4 si export")
    p.add_argument("--blit", action="store_true", help="Active le blitting (plus rapide mais exigeant)")
    return p.parse_args()

def main():
    args = parse_args()

    if args.size:
        G = nx.grid_2d_graph(args.size, args.size)
        G = nx.convert_node_labels_to_integers(G)
    else:
        gpath = pathlib.Path(f"data/processed/graph_sector_{args.sector}.pkl") if args.sector else pathlib.Path(args.graph)
        if not gpath.exists():
            raise FileNotFoundError(f"Fichier graphe introuvable : {gpath}")
        G = load_graph_pickle(gpath)

    pos = get_node_positions(G)
    tour, H = compute_eulerian_tour(G)

    animate(H, pos, tour, speed=args.speed, interval=args.interval, outfile=args.out, blit=args.blit)


if __name__ == "__main__":
    main()
