import os
from langchain_core.tools import tool
from serpapi import GoogleSearch

@tool
def flights_finder(origin: str, destination: str, depart_date: str, return_date: str = "") -> dict:
    """
    Find flights between two cities using SerpAPI.

    Args:
        origin (str): Departure airport/city (e.g., "JFK").
        destination (str): Arrival airport/city (e.g., "LHR").
        depart_date (str): Departure date in YYYY-MM-DD format.
        return_date (str, optional): Return date in YYYY-MM-DD format.

    Returns:
        dict: {
            "origin": str,
            "destination": str,
            "depart_date": str,
            "return_date": str,
            "flights": [
                {"airline": str, "price": str, "duration": str, "link": str}
            ]
        }
    """
    try:
        api_key = os.environ.get("SERPAPI_API_KEY")
        if not api_key:
            return {"error": "❌ SERPAPI_API_KEY not set."}

        query = f"Flights from {origin} to {destination} on {depart_date}"
        if return_date:
            query += f" returning on {return_date}"

        search = GoogleSearch({"q": query, "api_key": api_key})
        results = search.get_dict()

        flights = []
        if "organic_results" in results:
            for r in results["organic_results"][:5]:  # Limit to top 5
                flights.append({
                    "airline": r.get("title", "Unknown airline"),
                    "price": r.get("price", "N/A"),
                    "duration": r.get("duration", "N/A"),
                    "link": r.get("link", "")
                })
        else:
            flights = [{"airline": "No flights found", "price": "N/A", "duration": "N/A", "link": ""}]

        return {
            "origin": origin,
            "destination": destination,
            "depart_date": depart_date,
            "return_date": return_date,
            "flights": flights
        }

    except Exception as e:
        return {"error": f"❌ Error fetching flights: {e}"}
