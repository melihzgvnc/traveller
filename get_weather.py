import openmeteo_requests
import requests_cache
import pandas as pd
import numpy as np
from retry_requests import retry
from pyowm.owm import OWM
from pyowm.utils import timestamps
from dotenv import load_dotenv
from pydantic import Field
import os
import requests
from datetime import datetime, timezone, timedelta


class Weather:

  def __init__(self, destination, start_date, end_date = None) -> None:
    self.destination = destination
    self.start_date = datetime.date(pd.to_datetime(start_date))
    self.end_date = datetime.date(pd.to_datetime(end_date)) if end_date else self.start_date
    self.geoloc = self.get_geolocation()
    self.weather_data = self.get_weather_data()

  def get_geolocation(self) -> dict:
    
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": self.destination, "format":"json"}  # Dictionary of parameters
    headers = {"Accept": "application/json", "Referer": "https://nominatim.openstreetmap.org/"}
    response = requests.get(url, params=params, headers=headers)

    result = {}
    if response.status_code == 200:
        data = response.json()
        result["lat"] = float(data[0]["lat"])
        result["lon"] = float(data[0]["lon"])
        return result
    else:
        print(f"Error: {response.status_code}")

  def get_weather_data(self):
    
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)
    

    url = "https://historical-forecast-api.open-meteo.com/v1/forecast"
    params = {
    	"latitude": self.geoloc["lat"],
    	"longitude": self.geoloc["lon"],
    	"start_date": "2024-01-01",
    	"end_date": "2024-12-31",
    	"daily": ["temperature_2m_max", "temperature_2m_min"]
    }
    responses = openmeteo.weather_api(url, params=params)
    
    response = responses[0]
    
    daily = response.Daily()
    daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
    daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()
    
    daily_data = {"date": pd.date_range(
    	start = pd.to_datetime(daily.Time(), unit = "s", utc = True).strftime("%Y-%m-%d"),
	    end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True).strftime("%Y-%m-%d"),
	    #freq = pd.Timedelta(seconds = daily.Interval()),
	    inclusive = "left"
    )}
    
    daily_data["temperature_2m_max"] = daily_temperature_2m_max
    daily_data["temperature_2m_min"] = daily_temperature_2m_min
    
    daily_dataframe = pd.DataFrame(data = daily_data)
    return daily_dataframe
  
  def calculate_avg(self):
    
    start_date = pd.to_datetime(self.start_date.replace(year=2024))
    end_date = pd.to_datetime(self.end_date.replace(year=2024))
    # print(start_date)
    # print(self.weather_data[self.weather_data.date == start_date])
    start = self.weather_data[self.weather_data.date == start_date].index[0]
    end = self.weather_data[self.weather_data.date == end_date].index[0]

    if start == end:
       end += 1
    
    pilot_df = self.weather_data.iloc[start:end]
    
    sum_max = pilot_df.temperature_2m_max.sum()/len(pilot_df.temperature_2m_min)
    sum_min = pilot_df.temperature_2m_min.sum()/len(pilot_df.temperature_2m_min)
    avg_temp = (sum_max+sum_min)/2

    return avg_temp    