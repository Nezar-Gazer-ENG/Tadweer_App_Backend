from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Dict, Tuple
from app.utils.routing import (
    a_star_algorithm,
    knapsack_capacity,
    combine_orders,
    calculate_route_matrix
)
from app.utils.geo_utils import (
    address_to_coords,
    coords_to_address,
    calculate_distance,
    get_route
)
from app.models.route import Route
from app.schemas.route import RouteCreate, RouteResponse

# Helper function to get the optimal route using A* algorithm
def calculate_optimal_route(locations: List[Tuple[float, float]]) -> List[int]:
    try:
        return a_star_algorithm(locations)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error calculating route: {str(e)}")

# Get the distance between two coordinates
def get_distance_between_coords(start: Tuple[float, float], end: Tuple[float, float]) -> float:
    try:
        return calculate_distance(start[0], start[1], end[0], end[1])
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error calculating distance: {str(e)}")

# Create a route map URL using Google Maps API
def generate_route_map(start_coords: Tuple[float, float], end_coords: Tuple[float, float]) -> dict:
    try:
        return get_route(start_coords, end_coords)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error generating route map: {str(e)}")

# Combine orders into optimal groups based on vehicle capacity
def optimize_order_groups(orders: List[Dict[str, float]], max_capacity: float) -> List[List[Dict[str, float]]]:
    try:
        return combine_orders(orders, max_capacity)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error optimizing order groups: {str(e)}")

# Generate the distance matrix for multiple locations
def get_distance_matrix(locations: List[Tuple[float, float]]) -> List[List[float]]:
    try:
        return calculate_route_matrix(locations).tolist()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error calculating distance matrix: {str(e)}")

# Create a new route
def create_route(db: Session, route_data: RouteCreate) -> Route:
    try:
        start_coords = address_to_coords(route_data.start_location)
        end_coords = address_to_coords(route_data.end_location)
        distance = calculate_distance(start_coords[0], start_coords[1], end_coords[0], end_coords[1])
        
        new_route = Route(
            mission_id=route_data.mission_id,
            start_location=f"{start_coords[0]}, {start_coords[1]}",
            end_location=f"{end_coords[0]}, {end_coords[1]}",
            distance=distance,
            optimized_route=None  # Will be calculated later
        )
        db.add(new_route)
        db.commit()
        db.refresh(new_route)
        return new_route
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error creating route: {str(e)}")

# Get the optimized route for a mission
def get_optimized_route(db: Session, mission_id: int, locations: List[Tuple[float, float]]) -> dict:
    try:
        optimal_order = calculate_optimal_route(locations)
        distance_matrix = get_distance_matrix(locations)
        optimal_route = [locations[i] for i in optimal_order]

        return {
            "optimal_route": optimal_route,
            "distance_matrix": distance_matrix
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error retrieving optimized route: {str(e)}")

# Optimize load based on vehicle capacity
def optimize_load(items: List[Dict[str, float]], max_weight: float) -> List[Dict[str, float]]:
    try:
        return knapsack_capacity(items, max_weight)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error optimizing load: {str(e)}")
