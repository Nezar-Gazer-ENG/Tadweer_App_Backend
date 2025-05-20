from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Tuple
from app.services.routing import (
    calculate_optimal_route,
    get_distance_between_coords,
    generate_route_map,
    optimize_order_groups,
    get_distance_matrix,
    create_route,
    get_optimized_route,
    optimize_load
)
from app.schemas.route import RouteCreate, RouteResponse
from app.utils.dependencies import get_db
from app.models.user import User

routing_router = APIRouter(
    prefix="/routes",
    tags=["Routes"]
)

# Calculate optimal route between locations
@routing_router.post("/optimize", response_model=List[int])
def calculate_route(locations: List[Tuple[float, float]]):
    try:
        return calculate_optimal_route(locations)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Get the distance between two coordinates
@routing_router.get("/distance", response_model=float)
def get_distance(start: Tuple[float, float], end: Tuple[float, float]):
    try:
        return get_distance_between_coords(start, end)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Generate a route map URL using Google Maps API
@routing_router.post("/map", response_model=dict)
def create_route_map(start_coords: Tuple[float, float], end_coords: Tuple[float, float]):
    try:
        return generate_route_map(start_coords, end_coords)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Combine orders into optimal groups based on vehicle capacity
@routing_router.post("/optimize-orders", response_model=List[List[Dict[str, float]]])
def optimize_orders(orders: List[Dict[str, float]], max_capacity: float):
    try:
        return optimize_order_groups(orders, max_capacity)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Generate the distance matrix for multiple locations
@routing_router.post("/distance-matrix", response_model=List[List[float]])
def generate_distance_matrix(locations: List[Tuple[float, float]]):
    try:
        return get_distance_matrix(locations)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Create a new route for a mission
@routing_router.post("/", response_model=RouteResponse, status_code=status.HTTP_201_CREATED)
def create_new_route(route_data: RouteCreate, db: Session = Depends(get_db)):
    return create_route(db=db, route_data=route_data)

# Get the optimized route for a mission
@routing_router.post("/mission/{mission_id}/optimize", response_model=dict)
def get_route_for_mission(mission_id: int, locations: List[Tuple[float, float]], db: Session = Depends(get_db)):
    return get_optimized_route(db=db, mission_id=mission_id, locations=locations)

# Optimize load based on vehicle capacity
@routing_router.post("/optimize-load", response_model=List[Dict[str, float]])
def optimize_vehicle_load(items: List[Dict[str, float]], max_weight: float):
    try:
        return optimize_load(items, max_weight)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
