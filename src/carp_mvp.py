import networkx as nx

def compute_tournees(G):
    """
    Calcule des tournées de déneigement sur le graphe G.
    Retourne une liste de dictionnaires : {'edges': [...], 'km': x, 'hours': y}
    """
    required_edges = [(u, v, data) for u, v, data in G.edges(data=True) if data.get('required')]

    required_edges.sort(key=lambda x: -x[2]['length_m'])

    tournees = []
    tournee = []
    temps = 0.0 

    vitesse_kmh = 10
    temps_max_h = 8

    for u, v, data in required_edges:
        dist_km = data['length_m'] / 1000
        temps_edge = dist_km / vitesse_kmh

        if temps + temps_edge > temps_max_h:
            tournees.append(tournee)
            tournee = []
            temps = 0.0

        tournee.append((u, v, data))
        temps += temps_edge

    if tournee:
        tournees.append(tournee)

    result = []
    for t in tournees:
        total_km = sum(data['length_m'] for _, _, data in t) / 1000
        total_h = total_km / vitesse_kmh
        result.append({
            'edges': t,
            'km': total_km,
            'hours': total_h
        })

    return result


if __name__ == '__main__':
    print("TEST : Création d'un mini graphe pour test")

    G = nx.Graph()
    G.add_edge(0, 1, length_m=1000, required=True)
    G.add_edge(1, 2, length_m=1500, required=True)
    G.add_edge(2, 3, length_m=2000, required=True)
    G.add_edge(3, 4, length_m=1000, required=False)  # pas requis
    G.add_edge(4, 5, length_m=2500, required=True)

    res = compute_tournees(G)
    for i, t in enumerate(res):
        print(f"Tournée {i+1} : {t['km']:.2f} km, {t['hours']:.2f} h, {len(t['edges'])} routes")

