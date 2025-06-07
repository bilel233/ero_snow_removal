import pickle
import osmnx as ox
import matplotlib.pyplot as plt

# Chemin vers le fichier .pkl du graphe
with open("data/processed/graph_sector_Outremont.pkl", "rb") as f:
    G = pickle.load(f)

# Affichage avec OSMnx
fig, ax = ox.plot_graph(
    G,
    node_size=0,
    edge_color="black",
    edge_linewidth=0.8,
    bgcolor="white",
    show=False,
    close=False
)

# Sauvegarde en image PNG
fig.savefig("outremont_graph.png", dpi=300, bbox_inches="tight")
plt.close()
print("✅ Image sauvegardée : outremont_graph.png")

