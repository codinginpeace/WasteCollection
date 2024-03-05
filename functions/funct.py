
from itertools import combinations

def all_subsets_except_depot(V, demands, vehicle_capacity, depot=0):
    """Generate all subsets of V that do not contain the depot and whose total demand is within vehicle capacity."""
    non_depot_nodes = [v for v in V if v != depot]
    all_subsets = []
    for r in range(1, len(non_depot_nodes) + 1):
        for subset in combinations(non_depot_nodes, r):
            total_demand = sum(demands[node] for node in subset)
            if total_demand <= vehicle_capacity:
                all_subsets.append(subset)
    return all_subsets
