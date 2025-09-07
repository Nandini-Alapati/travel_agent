import requests
import os
from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()

# Load Geoapify API key
GEOAPIFY_API_KEY = os.getenv("GEOAPIFY_API_KEY")


# -------------------------------
# Helper: Get city coordinates
# -------------------------------
def get_city_coordinates(city_name):
    """
    Uses Geoapify Geocoding API to fetch coordinates for a city name.
    Returns (lat, lon) tuple or None if not found.
    """
    url = "https://api.geoapify.com/v1/geocode/search"
    params = {
        "text": city_name,
        "apiKey": GEOAPIFY_API_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        features = data.get("features", [])
        if features:
            coords = features[0]["geometry"]["coordinates"]  # [lon, lat]
            return (coords[1], coords[0])  # (lat, lon)
    return None


# -------------------------------
# Tool: Find Attractions
# -------------------------------
@tool
def attractions_finder(location: str, radius: int = 5000, limit: int = 10) -> dict:
    """
    Find tourist attractions for a given location using Geoapify.

    Args:
        location (str): City name or coordinates in "lat,lon" format.
        radius (int): Search radius in meters (default: 5000m).
        limit (int): Number of results to return (default: 10).

    Returns:
        dict: A list of attractions with name, address, lat, lon.
    """
    # Handle input: string city or "lat,lon"
    if "," in location:  # coordinates provided
        lat, lon = location.split(",")
        coords = (float(lat.strip()), float(lon.strip()))
    else:  # assume it's a city name
        coords = get_city_coordinates(location)
        if not coords:
            return {"error": f"Could not find coordinates for {location}"}

    url = "https://api.geoapify.com/v2/places"
    params = {
        "categories": "tourism.sights",
        "filter": f"circle:{coords[1]},{coords[0]},{radius}",  # lon,lat,radius
        "limit": limit,
        "apiKey": GEOAPIFY_API_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        attractions = []
        for feature in data.get("features", []):
            props = feature.get("properties", {})
            attractions.append({
                "name": props.get("name", "Unknown"),
                "address": props.get("formatted", ""),
                "lat": feature["geometry"]["coordinates"][1],
                "lon": feature["geometry"]["coordinates"][0]
            })
        return {"location": location, "attractions": attractions}
    else:
        return {"error": response.text}


# -------------------------------
# Quick Test
# -------------------------------
if __name__ == "__main__":
    print("Attractions in Paris:")
    print(attractions_finder("Paris", limit=5))

    print("\nAttractions in Delhi (coords):")
    print(attractions_finder("28.6139,77.2090", limit=5))
