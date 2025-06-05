import osmnx as ox, pickle, pathlib
center_latlon = (45.560, -73.552)      
radius = 500                            
G_mini = ox.graph_from_point(center_latlon, dist=radius, network_type="drive")
out = pathlib.Path("data/processed/graph_sector_mini.pkl")
out.parent.mkdir(parents=True, exist_ok=True)
with open(out, "wb") as f:
    pickle.dump(G_mini, f)

print("Pickle créé :", out, "(nœuds:", G_mini.number_of_nodes(), ")")
