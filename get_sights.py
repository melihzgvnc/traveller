import os
from dotenv import load_dotenv
from serpapi import GoogleSearch
from pydantic import Field

load_dotenv()
os.environ["SERPAPI_KEY"] = os.getenv("SERPAPI_KEY")

def get_top_sights(
    destination: str = Field(
        ..., description = "The city which the top sights of will be fetched"
    ) 
) -> list:

    params = {
        "engine": "google",
        "q": f"Top sights in {destination}",
        "api_key": os.environ["SERPAPI_KEY"]
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    top_sights = [i["title"] for i in results["top_sights"]["sights"][:5]]
    return top_sights