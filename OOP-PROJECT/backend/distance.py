from geopy.geocoders import Nominatim
from geopy.distance import geodesic

def get_coords_and_distance(start_location, end_location):
    # Get the coordinates (latitude, longitude) for two locations and calculate the distance between them in kilometers
    geolocator = Nominatim(user_agent="ride-booking-map")
    try:
        # Geocode the start and end locations (assume locations are in the Philippines)
        start = geolocator.geocode(start_location + ", Philippines")
        end = geolocator.geocode(end_location + ", Philippines")
        if not start or not end:
            # Return None if either location is invalid
            return None, None, None
        # Calculate the geodesic distance between the two points
        distance = geodesic((start.latitude, start.longitude), (end.latitude, end.longitude)).km
        # Return coordinates and distance
        return (start.latitude, start.longitude), (end.latitude, end.longitude), distance
    except:
        # Return None if any error occurs during geocoding or distance calculation
        return None, None, None