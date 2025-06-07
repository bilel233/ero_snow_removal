#!/usr/bin/env python3
"""
Demo Snow‑Removal Fleet Simulation
---------------------------------
A minimal live demo for the ERO snow‑removal project.

* Builds a simple grid graph (street network) or loads one from a JSON file.
* Computes a naive Eulerian tour (every edge exactly once) as a proxy for a snow‑clearing route.
* Animates a single vehicle (truck or drone) moving along that tour in real time using Matplotlib.

Usage
-----
$ python demo_simulation.py                  # 5×5 grid, default speed
$ python demo_simulation.py --size 8 --speed 2.0  # larger grid, faster vehicle
$ python demo_simulation.py --graph my_graph.json # load custom graph created by your pipeline

Dependencies: networkx, matplotlib.  Install with:
$ pip install networkx matplotlib

The script is intentionally self‑contained so that reviewers can run a live simulation
without installing OR‑Tools or other heavy solvers.
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
import pathlib
import random
import sys
from dataclasses import dataclass
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.animation import FuncAnimation


@dataclass
class VehicleState:
    """Holds the dynamic state of the vehicle along the route."""

    route_edges: List[Tuple[int, int]]
    speed: float  # edges per second for simplicity

    edge_index: int = 0  # current edge in the route
    distance_on_edge: float = 0.0  # progress 0–1 on current edge

    def step(self, dt: float):
        """Advance the vehicle by *dt* seconds."""
        if self.edge_index >= len(self.route_edges):
            return  # finished

        self.distance_on_edge += self.speed * dt
        while self.distance_on_edge >= 1.0 and self.edge_index < len(self.route_edges):
            self.distance_on_edge -= 1.0
            self.edge_index += 1
            if self.edge_index >= len(self.route_edges):
                break

    @property
    def finished(self) -> bool:
        return self.edge_index >= len(self.route_edges)

    def current_edge(self) -> Tuple[int, int] | None:
        if self.finished:
            return None
        return self.route_edges[self.edge_index]


# -----------------------------------------------------------------------------
# Graph helpers
# -----------------------------------------------------------------------------

def make_grid_graph(n: int) -> nx.Graph:
    """Return an n×n grid graph with (x, y) positions on nodes."""
    G = nx.grid_2d_graph(n, n)  # Cartesian grid of size n
    # Re‑label nodes with simple integer ids while storing positions
    mapping = {}
    pos = {}
    for idx, node in enumerate(G.nodes()):
        mapping[node] = idx
        pos[idx] = node  # node is (x, y)
    G = nx.relabel_nodes(G, mapping)
    nx.set_node_attributes(G, {i: {"pos": tuple(map(float, coord))} for i, coord in pos.items()})
    return G


def load_graph_from_json(path: pathlib.Path) -> nx.Graph:
    """Load a graph saved with nodes 'id', 'x', 'y' and edges 'u', 'v'."""
    data = json.loads(path.read_text())
    G = nx.Graph()
    for node in data["nodes"]:
        G.add_node(node["id"], pos=(node["x"], node["y"]))
    for edge in data["edges"]:
        G.add_edge(edge["u"], edge["v"])
    return G


# -----------------------------------------------------------------------------
# Route planner – naive Eulerian tour
# -----------------------------------------------------------------------------

def compute_euler_tour(G: nx.Graph) -> List[Tuple[int, int]]:
    """Return a list of directed edges forming an Eulerian tour.

    For non‑Eulerian graphs we add duplicate edges (semi‑Eulerisation) so that
    every street is ploughed at least once.
    """
    if not nx.is_eulerian(G):
        G = nx.eulerize(G)  # duplicates some edges to make graph Eulerian
    tour = list(nx.eulerian_circuit(G))  # list of (u, v)
    return tour


# -----------------------------------------------------------------------------
# Animation
# -----------------------------------------------------------------------------

def animate_route(G: nx.Graph, route: List[Tuple[int, int]], speed: float, interval: int):
    pos: Dict[int, Tuple[float, float]] = nx.get_node_attributes(G, "pos")

    # Prepare matplotlib figure
    fig, ax = plt.subplots()
    ax.set_aspect("equal")
    ax.set_title("Snow Removal Route Simulation")
    ax.axis("off")

    # Draw static background (streets)
    nx.draw_networkx_edges(G, pos, ax=ax, width=1, edge_color="#cccccc")
    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=20, node_color="#333333")

    # Vehicle marker
    vehicle_marker, = ax.plot([], [], marker="s", markersize=10, linestyle="none")

    # Keep track of visited edges to recolor them when cleared
    visited = set()
    edge_artists = {}

    for u, v in G.edges():
        line = ax.plot([], [])[0]
        edge_artists[(u, v)] = edge_artists[(v, u)] = line  # undirected

    state = VehicleState(route, speed=speed)

    # Pre‑draw all edge artists (so they are in the right order)
    for (u, v), artist in edge_artists.items():
        x1, y1 = pos[u]
        x2, y2 = pos[v]
        artist.set_data([x1, x2], [y1, y2])
        artist.set_color("#cccccc")
        artist.set_linewidth(2)

    def update(frame_number):
        nonlocal state
        state.step(dt=interval / 1000.0)

        edge = state.current_edge()
        if edge is None:
            vehicle_marker.set_visible(False)
            return

        u, v = edge
        (x1, y1), (x2, y2) = pos[u], pos[v]
        # Linear interpolation along the edge
        x = x1 + (x2 - x1) * state.distance_on_edge
        y = y1 + (y2 - y1) * state.distance_on_edge
        vehicle_marker.set_data([x], [y])
        vehicle_marker.set_color("red")

        # Mark edge as visited (cleared)
        if edge not in visited:
            visited.add(edge)
            edge_artists[edge].set_color("#0080ff")  # blue cleared edge

    ani = FuncAnimation(fig, update, interval=interval)
    plt.show()


# -----------------------------------------------------------------------------
# Main CLI
# -----------------------------------------------------------------------------

def parse_args(argv: List[str] | None = None):
    p = argparse.ArgumentParser(description="Live simulation of a snow‑removal route")
    p.add_argument("--graph", type=pathlib.Path, default=None,
                   help="Path to JSON graph file (default: generate grid)")
    p.add_argument("--size", type=int, default=5,
                   help="Grid size if no graph file supplied (default: 5)")
    p.add_argument("--speed", type=float, default=1.0,
                   help="Vehicle speed in edges per second (default: 1.0)")
    p.add_argument("--interval", type=int, default=100,
                   help="Animation frame interval in milliseconds (default: 100)")
    return p.parse_args(argv)


def main(argv: List[str] | None = None):
    args = parse_args(argv)

    if args.graph is None:
        G = make_grid_graph(args.size)
    else:
        if not args.graph.exists():
            print(f"Graph file {args.graph} not found", file=sys.stderr)
            sys.exit(1)
        G = load_graph_from_json(args.graph)

    route = compute_euler_tour(G)
    print(f"Route length: {len(route)} edges")

    animate_route(G, route, speed=args.speed, interval=args.interval)


if __name__ == "__main__":
    main()
