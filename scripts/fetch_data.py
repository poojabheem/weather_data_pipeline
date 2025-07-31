import sys
import os
import requests
import pandas as pd
from datetime import datetime
import logging
import concurrent.futures

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def fetch_city_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city.strip()}&appid={config.API_KEY}&units=metric"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return {
            "city": city.strip(),
            "temperature": data['main']['temp'],
            "humidity": data['main']['humidity'],
            "pressure": data['main']['pressure'],
            "weather": data['weather'][0]['description'],
            "wind_speed": data['wind']['speed'],
            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        logging.error(f"Failed to fetch data for {city}: {e}")
        return None

def fetch_weather():
    cities = config.CITY_LIST
    logging.info(f"Fetching weather for cities: {cities}")

    # Parallel fetch
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(fetch_city_weather, cities))

    # Remove failed responses
    results = [r for r in results if r is not None]
    df = pd.DataFrame(results)

    os.makedirs("data", exist_ok=True)
    file_path = f"data/weather_{datetime.now().strftime('%Y%m%d%H%M')}.csv"
    df.to_csv(file_path, index=False)
    logging.info(f"Data saved to {file_path}")

if __name__ == "__main__":
    fetch_weather()
