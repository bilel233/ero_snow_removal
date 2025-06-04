import networkx as nx
from carp_mvp import compute_tournees, analyze_solution_quality

def run_pipeline():
    print("📂 Chargement du graphe...")
    G = nx.read_gpickle("data/outremont.gpickle")  # Remplace par un autre .gpickle si besoin

    print("🚜 Calcul des tournées de déneigement...")
    tournees = compute_tournees(G, strategy="mixed")

    print(f"\n📊 Résultats des tournées ({len(tournees)} générées) :")
    for t in tournees:
        print(f"  ▸ Tournée {t['id']}: {t['km']} km | {t['hours']} h | {t['utilization']}%")

    summary = analyze_solution_quality(tournees)

    print("\n📈 Synthèse globale :")
    for key, value in summary.items():
        print(f"  {key}: {value}")

if __name__ == "__main__":
    run_pipeline()

