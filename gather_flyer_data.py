import json
from get_sights import get_top_sights

with open("data.json", "r+") as f:
  data = json.load(f)
  
destination = data["destination"]

#fetching sights data
top_sights = get_top_sights(destination)
print(top_sights)
data["attractions"] = top_sights
