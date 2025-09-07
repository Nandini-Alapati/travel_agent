import os
from langchain_core.tools import tool
from serpapi import GoogleSearch

@tool
def hotels_finder(location: str, checkin_date: str, checkout_date: str, stars: int = 3) -> dict:
    """
    Find hotels in a city for given dates.

    Args:
        location (str): City name (e.g., "London").
        checkin_date (str): Check-in date in YYYY-MM-DD format.
        checkout_date (str): Check-out date in YYYY-MM-DD format.
        stars (int, optional): Star rating filter.

    Returns:
        dict: {
            "location": str,
            "checkin_date": str,
            "checkout_date": str,
            "stars": int,
            "hotels": [
                {"name": str, "price": str, "rating": str, "link": str}
            ]
        }
    """
    try:
        api_key = os.environ.get("SERPAPI_API_KEY")
        if not api_key:
            return {"error": "❌ SERPAPI_API_KEY not set."}

        query = f"{stars}-star hotels in {location} from {checkin_date} to {checkout_date}"

        search = GoogleSearch({"q": query, "api_key": api_key})
        results = search.get_dict()

        hotels = []
        if "organic_results" in results:
            for r in results["organic_results"][:5]:  # Limit top 5
                hotels.append({
                    "name": r.get("title", "Unknown hotel"),
                    "price": r.get("price", "N/A"),
                    "rating": r.get("rating", "N/A"),
                    "link": r.get("link", "")
                })
        else:
            hotels = [{"name": "No hotels found", "price": "N/A", "rating": "N/A", "link": ""}]

        return {
            "location": location,
            "checkin_date": checkin_date,
            "checkout_date": checkout_date,
            "stars": stars,
            "hotels": hotels
        }

    except Exception as e:
        return {"error": f"❌ Error fetching hotels: {e}"}
