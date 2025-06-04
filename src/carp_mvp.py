import networkx as nx
import random
from typing import List, Dict, Tuple, Optional
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CARPSolver:
    
    def __init__(self, capacity_limit: float = 8.0, speed_kmh: float = 10.0):
        self.capacity_limit = capacity_limit
        self.speed_kmh = speed_kmh
        self.depot_node = 0
        
    def compute_tournees(self, G: nx.Graph, strategy: str = "mixed") -> List[Dict]:
        start_time = time.time()
        
        required_edges = self._get_required_edges(G)
        if not required_edges:
            logging.warning("Aucune arête requise trouvée dans le graphe")
            return []
        
        logging.info(f"Traitement de {len(required_edges)} arêtes requises")
        
        shortest_paths = dict(nx.all_pairs_shortest_path_length(G))
        
        tournees = self._path_scanning_algorithm(
            G, required_edges, shortest_paths, strategy
        )
        
        tournees = self._local_optimization(G, tournees, shortest_paths)
        
        total_time = time.time() - start_time
        tournees = self._calculate_final_stats(G, tournees)
        
        logging.info(f"Génération terminée en {total_time:.2f}s - {len(tournees)} tournées créées")
        
        return tournees
    
    def _get_required_edges(self, G: nx.Graph) -> List[Tuple]:
        required = []
        for u, v, data in G.edges(data=True):
            if data.get('required', False):
                required.append((u, v, data))
        return required
    
    def _path_scanning_algorithm(self, G: nx.Graph, required_edges: List[Tuple], 
                                shortest_paths: Dict, strategy: str) -> List[Dict]:
        unvisited_edges = required_edges.copy()
        tournees = []
        
        while unvisited_edges:
            current_tournee = {
                'edges': [],
                'current_node': self.depot_node,
                'total_distance': 0.0,
                'total_time': 0.0,
                'load': 0.0
            }
            
            while unvisited_edges:
                next_edge = self._select_next_edge(
                    current_tournee, unvisited_edges, shortest_paths, strategy, G
                )
                
                if next_edge is None:
                    break
                
                cost_to_edge, service_time, new_node = self._calculate_edge_cost(
                    current_tournee, next_edge, shortest_paths, G
                )
                
                potential_time = current_tournee['total_time'] + cost_to_edge + service_time
                if potential_time > self.capacity_limit:
                    break
                
                current_tournee['edges'].append(next_edge)
                current_tournee['total_time'] = potential_time
                current_tournee['total_distance'] += (cost_to_edge + service_time) * self.speed_kmh
                current_tournee['current_node'] = new_node
                
                unvisited_edges.remove(next_edge)
            
            if current_tournee['current_node'] != self.depot_node:
                return_cost = shortest_paths[current_tournee['current_node']][self.depot_node]
                current_tournee['total_time'] += return_cost / self.speed_kmh
                current_tournee['total_distance'] += return_cost
            
            tournees.append(current_tournee)
        
        return tournees
    
    def _select_next_edge(self, current_tournee: Dict, unvisited_edges: List, 
                         shortest_paths: Dict, strategy: str, G: nx.Graph) -> Optional[Tuple]:
        current_node = current_tournee['current_node']
        candidates = []
        
        for edge in unvisited_edges:
            u, v, data = edge
            dist_to_u = shortest_paths[current_node][u]
            dist_to_v = shortest_paths[current_node][v]
            min_dist = min(dist_to_u, dist_to_v)
            
            demand = data.get('length_m', 1000) / 1000
            service_time = demand / self.speed_kmh
            
            if strategy == "nearest":
                score = -min_dist
            elif strategy == "cheapest":
                score = -service_time
            elif strategy == "mixed":
                efficiency = demand / (min_dist + service_time + 0.01)
                score = efficiency
            else:
                score = random.random()
            
            candidates.append((edge, score, min_dist, service_time))
        
        if not candidates:
            return None
        
        candidates.sort(key=lambda x: x[1], reverse=True)
        return candidates[0][0]
    
    def _calculate_edge_cost(self, current_tournee: Dict, edge: Tuple, 
                           shortest_paths: Dict, G: nx.Graph) -> Tuple[float, float, int]:
        u, v, data = edge
        current_node = current_tournee['current_node']
        
        dist_to_u = shortest_paths[current_node][u]
        dist_to_v = shortest_paths[current_node][v]
        
        if dist_to_u <= dist_to_v:
            travel_cost = dist_to_u / self.speed_kmh
            new_node = v
        else:
            travel_cost = dist_to_v / self.speed_kmh
            new_node = u
        
        edge_length = data.get('length_m', 1000) / 1000
        service_time = edge_length / self.speed_kmh
        
        return travel_cost, service_time, new_node
    
    def _local_optimization(self, G: nx.Graph, tournees: List[Dict], 
                          shortest_paths: Dict) -> List[Dict]:
        improved = True
        iterations = 0
        max_iterations = 100
        
        while improved and iterations < max_iterations:
            improved = False
            iterations += 1
            
            for i in range(len(tournees)):
                for j in range(i + 1, len(tournees)):
                    if self._try_edge_swap(tournees[i], tournees[j], G, shortest_paths):
                        improved = True
        
        logging.info(f"Optimisation locale terminée après {iterations} itérations")
        return tournees
    
    def _try_edge_swap(self, tournee1: Dict, tournee2: Dict, G: nx.Graph, 
                      shortest_paths: Dict) -> bool:
        if not tournee1['edges'] or not tournee2['edges']:
            return False
        
        current_cost = tournee1['total_time'] + tournee2['total_time']
        
        edge1 = tournee1['edges'][-1]
        edge2 = tournee2['edges'][-1]
        
        return False
    
    def _calculate_final_stats(self, G: nx.Graph, tournees: List[Dict]) -> List[Dict]:
        final_tournees = []
        
        for i, tournee in enumerate(tournees):
            final_tournee = {
                'id': i + 1,
                'edges': tournee['edges'],
                'km': round(tournee['total_distance'], 2),
                'hours': round(tournee['total_time'], 2),
                'num_edges': len(tournee['edges']),
                'efficiency': 0.0,
                'utilization': round((tournee['total_time'] / self.capacity_limit) * 100, 1)
            }
            
            service_km = sum(e[2].get('length_m', 1000) / 1000 for e in tournee['edges'])
            if tournee['total_time'] > 0:
                final_tournee['efficiency'] = round(service_km / tournee['total_time'], 2)
            
            final_tournees.append(final_tournee)
        
        return final_tournees


def compute_tournees(G: nx.Graph, strategy: str = "mixed") -> List[Dict]:
    solver = CARPSolver()
    return solver.compute_tournees(G, strategy)


def analyze_solution_quality(tournees: List[Dict]) -> Dict:
    if not tournees:
        return {'error': 'Aucune tournée générée'}
    
    total_km = sum(t['km'] for t in tournees)
    total_hours = sum(t['hours'] for t in tournees)
    avg_utilization = sum(t['utilization'] for t in tournees) / len(tournees)
    max_time = max(t['hours'] for t in tournees)
    min_time = min(t['hours'] for t in tournees)
    
    return {
        'num_routes': len(tournees),
        'total_distance_km': round(total_km, 2),
        'total_time_hours': round(total_hours, 2),
        'avg_utilization_percent': round(avg_utilization, 1),
        'max_route_time': round(max_time, 2),
        'min_route_time': round(min_time, 2),
        'time_balance': round(max_time - min_time, 2),
        'efficiency_score': round(total_km / total_hours if total_hours > 0 else 0, 2)
    }

def benchmark_strategies(G: nx.Graph) -> Dict:
    strategies = ["nearest", "cheapest", "mixed"]
    results = {}
    
    for strategy in strategies:
        solver = CARPSolver()
        start_time = time.time()
        tournees = solver.compute_tournees(G, strategy)
        exec_time = time.time() - start_time
        
        analysis = analyze_solution_quality(tournees)
        analysis['execution_time'] = round(exec_time, 3)
        results[strategy] = analysis
    
    return results


if __name__ == '__main__':
    print("TEST : Algorithme CARP Path-Scanning Avancé")
    
    G = nx.Graph()
    edges_data = [
        (0, 1, {'length_m': 1500, 'required': True}),
        (1, 2, {'length_m': 2000, 'required': True}),
        (2, 3, {'length_m': 1800, 'required': True}),
        (3, 4, {'length_m': 2200, 'required': True}),
        (4, 0, {'length_m': 1600, 'required': False}),
        (0, 2, {'length_m': 2500, 'required': True}),
        (1, 3, {'length_m': 1900, 'required': True}),
    ]
    
    for u, v, data in edges_data:
        G.add_edge(u, v, **data)
    
    solver = CARPSolver()
    tournees = solver.compute_tournees(G, "mixed")
    
    print(f"\nRESULTATS :")
    print(f"Nombre de tournées générées : {len(tournees)}")
    
    for i, tournee in enumerate(tournees):
        print(f"\nTournée {tournee['id']} :")
        print(f"  Distance : {tournee['km']} km")
        print(f"  Durée : {tournee['hours']} h")
        print(f"  Utilisation : {tournee['utilization']}%")
        print(f"  Efficacité : {tournee['efficiency']} km/h")
        print(f"  Nombre d'arêtes : {tournee['num_edges']}")
    
    analysis = analyze_solution_quality(tournees)
    print(f"\nANALYSE DE QUALITE :")
    for key, value in analysis.items():
        print(f"  {key}: {value}")
    
    print(f"\nBENCHMARK DES STRATEGIES :")
    benchmark = benchmark_strategies(G)
    for strategy, results in benchmark.items():
        print(f"\n{strategy.upper()}:")
        print(f"  Routes: {results['num_routes']}, Temps: {results['execution_time']}s")
        print(f"  Distance totale: {results['total_distance_km']} km")
        print(f"  Efficacité: {results['efficiency_score']} km/h")
