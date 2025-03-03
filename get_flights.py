import os
from dotenv import load_dotenv
from serpapi import GoogleSearch
from pydantic import Field
from typing import Optional
import json
from langchain_core.tools import tool


def get_return_flights(
    arrival_id: str = Field(
        ..., description = "The token necessary to fetch return flight data"
    ),
    departure_id: str = Field(
        ..., description = "The token necessary to fetch return flight data"
    ),
    outbound_date: str = Field(
        ..., description = "The token necessary to fetch return flight data"
    )
) -> list:

    params = {
        "engine": "google_flights",
        "departure_id": departure_id,
        "arrival_id": arrival_id,
        "outbound_date": outbound_date,
        "currency": "GBP",
        "type": 2,
        "api_key": os.environ["SERPAPI_KEY"]
    }

    search = GoogleSearch(params)
    results = search.get_dict()["best_flights"][:3]

    info = []
    for flight in results:
        return_info = {}
        return_info["departure_info"] = flight["flights"][0]["departure_airport"]
        if "layovers" in flight:
            return_info["layovers"] = [{"name": layover["name"], "id": layover["id"]} for layover in flight["layovers"]]
        return_info["arrival_info"] = flight["flights"][-1]["arrival_airport"]
        return_info["price"] = flight["price"]
        info.append(return_info)
        
    return info

@tool
def get_flight_tickets(
    city: str = Field(
        ..., description="The name of the city of destination"
    ),
    departure_id: str = Field(
        ..., description="The IATA code e.g. LGW for London Gatwick Airport"
    ), 
    arrival_id: str = Field(
        ..., description="The IATA code e.g. LGW for London Gatwick Airport"
    ), 
    outbound_date: str = Field(
        ..., description="The departure date in YYYY-MM-DD format"
    ), 
    return_date: Optional[str] = Field(
        None, description="The return date in YYYY-MM-DD format"
    ),
) -> dict:
    """
    Fetch flight ticket information from Google Flights using SerpAPI.

    This function searches for the best flight deals based on the provided parameters.
    It returns information about both outbound flights and, if specified, return flights.
    Each flight includes details about departure, arrival, any layovers, and pricing.

    Args:
        city (str): The name of the destination city
        departure_id (str): IATA code of the departure airport (e.g., 'LGW' for London Gatwick)
        arrival_id (str): IATA code of the arrival airport
        outbound_date (str): Departure date in YYYY-MM-DD format
        return_date (Optional[str], optional): Return date in YYYY-MM-DD format. Defaults to None.

    Returns:
        dict: A dictionary containing flight information
    """

    with open('data.json', 'w') as f:
        json.dump({
            "destination": city,
            "start_date": outbound_date,
            "end_date": return_date if isinstance(return_date, str) else outbound_date
            }, f)

    load_dotenv()
    os.environ["SERPAPI_KEY"] = os.getenv("SERPAPI_KEY")
    if not os.environ.get("SERPAPI_KEY"):
            return {
                "error": "SERPAPI_KEY not found in environment variables. Please check your .env file."
            }
    
    if not isinstance(return_date, str):    
        params = {
            "engine": "google_flights",
            "departure_id": departure_id,
            "arrival_id": arrival_id,
            "outbound_date": outbound_date,
            "type": 2,
            "currency": "GBP",
            "hl": "en",
            "api_key": os.environ["SERPAPI_KEY"]
        }
    else:
        params = {
            "engine": "google_flights",
            "departure_id": departure_id,
            "arrival_id": arrival_id,
            "outbound_date": outbound_date,
            "return_date": return_date,
            "currency": "GBP",
            "hl": "en",
            "api_key": os.environ["SERPAPI_KEY"]
        }

    
    search = GoogleSearch(params)
    print(return_date.__annotations__["annotation"])
    results = search.get_dict()["best_flights"][:3]

    info = {"outbound_flights":[], "return_flights":[]}
    for flight in results:
        outbound_info = {}
        outbound_info["departure_info"] = flight["flights"][0]["departure_airport"]
        if "layovers" in flight:
            outbound_info["layovers"] = [{"name": layover["name"], "id": layover["id"]} for layover in flight["layovers"]]
        outbound_info["arrival_info"] = flight["flights"][-1]["arrival_airport"]
        outbound_info["price"] = flight["price"]
        info["outbound_flights"].append(outbound_info)

    if isinstance(return_date, str):
        departure_token = results[0]["departure_token"]
        return_info = get_return_flights(departure_token,departure_id,arrival_id,return_date)
        info["return_flights"].extend(return_info)

    return info
