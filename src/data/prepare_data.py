from pathlib import Path
import osmnx as ox
import geopandas as gpd
import networkx as nx
import pickle
from shapely.geometry import box  

RAW_DIR = Path("data/raw")
PROC_DIR = Path("data/processed")

SECTORS = {
    "Outremont":          {"north": 45.534, "south": 45.511, "east": -73.592, "west": -73.623},
    "Verdun":             {"north": 45.475, "south": 45.450, "east": -73.555, "west": -73.605},
    "Anjou":              {"north": 45.620, "south": 45.575, "east": -73.515, "west": -73.600},
    "RDP-PAT":            {"north": 45.690, "south": 45.610, "east": -73.475, "west": -73.580},
    "Plateau-Mont-Royal": {"north": 45.535, "south": 45.510, "east": -73.560, "west": -73.600},
}


def save_graph_shapefile(G: nx.MultiDiGraph, out_dir: Path) -> None:
    """La fonction exporte un graphe en deux shapefiles (nodes et edges)."""
    
    nodes, edges = ox.graph_to_gdfs(G, nodes=True, edges=True)
    out_dir.mkdir(parents=True, exist_ok=True)
    nodes.to_file(out_dir / "nodes.shp")
    edges.to_file(out_dir / "edges.shp")


def download_and_save_full_graph() -> nx.MultiDiGraph:
    """La fonction télécharge tout Montréal puis sauvegarde shapefile + pickle."""

    print("Téléchargement du réseau routier de Montréal")
    G = ox.graph_from_place("Montréal, Québec, Canada", network_type="drive")
    print("Téléchargement terminé.")

    shp_dir = RAW_DIR / "montreal_roads"
    print(f"▶ Export Shapefile complet dans {shp_dir}/")
    save_graph_shapefile(G, shp_dir)
    print("Shapefile complet et  enregistré.")

    PROC_DIR.mkdir(parents=True, exist_ok=True)
    with open(PROC_DIR / "graph_full.pkl", "wb") as f:
        pickle.dump(G, f)
    print("Graphe complet sérialisé data/processed/graph_full.pkl")
    return G


def extract_sector_graphs(_: nx.MultiDiGraph) -> None:
    """Construit, sérialise et exporte les graphes des 5 secteurs."""
    print("🔎  Extraction des 5 sous-graphes sectoriels…")
    for name, bb in SECTORS.items():
        print(f"  • {name}")
        poly = box(bb["west"], bb["south"], bb["east"], bb["north"])
        G_sub = ox.graph_from_polygon(poly, network_type="drive")
        with open(PROC_DIR / f"graph_sector_{name}.pkl", "wb") as f:
            pickle.dump(G_sub, f)
        shp_out = RAW_DIR / "sectors" / name
        print(f"    ▶ Export Shapefile dans {shp_out}/")
        save_graph_shapefile(G_sub, shp_out)

    print("Sous-graphes sérialisés et shapefiles prêts.")


if __name__ == "__main__":
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROC_DIR.mkdir(parents=True, exist_ok=True)

    full_graph = download_and_save_full_graph()
    extract_sector_graphs(full_graph)
