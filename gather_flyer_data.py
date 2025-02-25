import json
from get_sights import get_top_sights
from get_weather import Weather

with open("data.json", "r+") as f:
  data = json.load(f)
  
destination = data["destination"]

#fetching weather data
weather = Weather(**data)
print(weather.calculate_avg())

#fetching sights data
top_sights = get_top_sights(destination)
print(top_sights)
data["attractions"] = top_sights
