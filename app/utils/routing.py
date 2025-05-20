from typing import List, Dict, Tuple
from scipy.spatial.distance import cdist
import numpy as np
from app.utils.geo_utils import calculate_distance

def a_star_algorithm(locations: List[Tuple[float, float]]) -> List[int]:
    """
    Uses the A* algorithm to find the optimal route between multiple locations.
    Returns the optimal order of indices to visit.
    """
    def heuristic(a: Tuple[float, float], b: Tuple[float, float]) -> float:
        return calculate_distance(a[0], a[1], b[0], b[1])

    start = 0  # Start from the first location
    open_set = {start}
    came_from = {}
    g_score = {i: float('inf') for i in range(len(locations))}
    g_score[start] = 0
    f_score = {i: float('inf') for i in range(len(locations))}
    f_score[start] = heuristic(locations[start], locations[-1])

    while open_set:
        current = min(open_set, key=lambda x: f_score[x])
        open_set.remove(current)

        if current == len(locations) - 1:
            # Reconstruct path
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            return path[::-1]

        for neighbor in range(len(locations)):
            if neighbor == current:
                continue
            tentative_g_score = g_score[current] + heuristic(locations[current], locations[neighbor])
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic(locations[neighbor], locations[-1])
                open_set.add(neighbor)

    return []

def knapsack_capacity(items: List[Dict[str, float]], max_weight: float) -> List[Dict[str, float]]:
    """
    Uses the Knapsack algorithm to maximize load while staying within the capacity.
    Returns the optimal selection of items.
    """
    items = sorted(items, key=lambda x: x['value'] / x['weight'], reverse=True)
    total_weight = 0
    selected_items = []

    for item in items:
        if total_weight + item['weight'] <= max_weight:
            selected_items.append(item)
            total_weight += item['weight']

    return selected_items

def combine_orders(orders: List[Dict[str, float]], max_capacity: float) -> List[List[Dict[str, float]]]:
    """
    Combines orders into optimal groups based on vehicle capacity.
    Returns a list of order groups for efficient pickup.
    """
    order_groups = []
    current_group = []
    current_weight = 0

    for order in orders:
        if current_weight + order['weight'] <= max_capacity:
            current_group.append(order)
            current_weight += order['weight']
        else:
            order_groups.append(current_group)
            current_group = [order]
            current_weight = order['weight']

    if current_group:
        order_groups.append(current_group)

    return order_groups

def calculate_route_matrix(locations: List[Tuple[float, float]]) -> np.ndarray:
    """
    Creates a distance matrix between all locations.
    Returns a 2D numpy array with pairwise distances.
    """
    coords = np.array(locations)
    dist_matrix = cdist(coords, coords, metric='euclidean')
    return dist_matrix
