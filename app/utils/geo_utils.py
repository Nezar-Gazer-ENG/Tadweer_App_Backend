from geopy.distance import geodesic
import googlemaps
from app.utils.config_loader import get_config

# Initialize Google Maps client if API key is available
API_KEY = get_config("GOOGLE_MAPS_API_KEY")
gmaps = None

if API_KEY:
    try:
        gmaps = googlemaps.Client(key=API_KEY)
    except Exception as e:
        print(f"Failed to initialize Google Maps client: {e}")

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the distance between two geographical coordinates.
    Returns the distance in kilometers.
    """
    point1 = (lat1, lon1)
    point2 = (lat2, lon2)
    return geodesic(point1, point2).kilometers

def address_to_coords(address: str) -> tuple:
    """
    Convert a human-readable address to geographical coordinates (latitude, longitude).
    Uses mock data if Google Maps client is not available.
    """
    if not gmaps:
        print(f"Mocking coordinates for address: {address}")
        return (24.7136, 46.6753)  # Riyadh, Saudi Arabia (Mocked)
    try:
        geocode_result = gmaps.geocode(address)
        if geocode_result:
            location = geocode_result[0]['geometry']['location']
            return location['lat'], location['lng']
        else:
            raise ValueError("Address not found")
    except Exception as e:
        raise ValueError(f"Error in geocoding address: {str(e)}")

def coords_to_address(lat: float, lon: float) -> str:
    """
    Convert geographical coordinates to a human-readable address.
    Uses mock data if Google Maps client is not available.
    """
    if not gmaps:
        print(f"Mocking address for coordinates: ({lat}, {lon})")
        return "Mocked Address, Riyadh, Saudi Arabia"
    try:
        reverse_result = gmaps.reverse_geocode((lat, lon))
        if reverse_result:
            return reverse_result[0]['formatted_address']
        else:
            raise ValueError("Coordinates not found")
    except Exception as e:
        raise ValueError(f"Error in reverse geocoding: {str(e)}")

def get_route(start_coords: tuple, end_coords: tuple) -> dict:
    """
    Retrieve an optimized route between two coordinates.
    Uses mock data if Google Maps client is not available.
    """
    if not gmaps:
        print(f"Mocking route from {start_coords} to {end_coords}")
        return {
            "distance": "10 km",
            "duration": "15 mins",
            "start_address": f"Mocked Start ({start_coords})",
            "end_address": f"Mocked End ({end_coords})",
            "steps": ["Head north", "Turn right", "Arrive at destination"]
        }
    try:
        directions = gmaps.directions(
            origin=start_coords,
            destination=end_coords,
            mode="driving",
            alternatives=False
        )
        if directions:
            route = directions[0]['legs'][0]
            distance = route['distance']['text']
            duration = route['duration']['text']
            return {
                "distance": distance,
                "duration": duration,
                "start_address": route['start_address'],
                "end_address": route['end_address'],
                "steps": [step['html_instructions'] for step in route['steps']]
            }
        else:
            raise ValueError("No route found")
    except Exception as e:
        raise ValueError(f"Error in fetching route: {str(e)}")
