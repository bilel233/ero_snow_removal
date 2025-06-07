import networkx as nx
import pickle
from pathlib import Path
from carp_mvp import compute_tournees, analyze_solution_quality

def run_pipeline():
    print(" Chargement du graphe")
    gpath = Path("data/outremont.gpickle")
    with open(gpath, "rb") as f:
        G = pickle.load(f)

    print(" Calcul des tournées de déneigement")
    tournees = compute_tournees(G, strategy="mixed")

    print(f"\n  Résultats ({len(tournees)} tournées) :")
    for t in tournees:
        print(f"  ▸ Tournée {t['id']}: {t['km']} km | {t['hours']} h | {t['utilization']}%")

    summary = analyze_solution_quality(tournees)
    print("\n Synthèse globale :")
    for k, v in summary.items():
        print(f"  {k}: {v}")

if __name__ == "__main__":
    run_pipeline()
