import os
import requests
import time
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("WEATHER_API_KEY")

api_url = "https://api.weatherapi.com/v1/forecast.json"

zip_codes = [
    '90045',  # Los Angeles, CA
    '10001',  # New York, NY
    '60601',  # Chicago, IL
    '98101',  # Seattle, WA
    '33101',  # Miami, FL
    '77001',  # Houston, TX
    '85001',  # Phoenix, AZ
    '19101',  # Philadelphia, PA
    '78201',  # San Antonio, TX
    '92101',  # San Diego, CA
    '75201',  # Dallas, TX
    '95101',  # San Jose, CA
    '78701',  # Austin, TX
    '32099',  # Jacksonville, FL
    '76001',  # Fort Worth, TX
    '43085',  # Columbus, OH
    '28201',  # Charlotte, NC
    '46201',  # Indianapolis, IN
    '94102',  # San Francisco, CA
    '98004',  # Seattle (Bellevue), WA
]

results = []

for zip_code in zip_codes:
    params = {
        "key": api_key,
        "q": zip_code,
        "days": 7,
    }
    response = requests.get(api_url, params=params)
    data = response.json()

    city = data["location"]["name"]
    region = data["location"]["region"]

    print(f"{city}, {region}:")
    for day in data["forecast"]["forecastday"]:
        date = day["date"]
        max_temp = day["day"]["maxtemp_f"]
        min_temp = day["day"]["mintemp_f"]
        condition = day["day"]["condition"]["text"]

        results.append({
            "zip_code": zip_code,
            "city": city,
            "region": region,
            "date": date,
            "max_temp_f": max_temp,
            "min_temp_f": min_temp,
            "condition": condition,
        })

        print(f"  {date}: {min_temp}–{max_temp}°F, {condition}")

    time.sleep(1)

df = pd.DataFrame(results)
print(df.to_string(index=False))
print(f"\n{df.shape[0]} rows x {df.shape[1]} columns")

df.to_csv("weather_data.csv", index=False)
print("Saved to weather_data.csv")
