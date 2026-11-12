import os
import requests
from dotenv import load_dotenv
from dataclasses import dataclass

@dataclass
class Weather:
    city: str
    country: str
    local_time: str
    temp_c: float
    feels_like_c: float
    humidity: int
    wind_kph: float
    condition: str

    @classmethod
    def from_api(cls, data: dict):
        loc = data["location"]
        cur = data["current"]
        return cls(
            city=loc["name"],
            country=loc["country"],
            local_time=loc["localtime"],
            temp_c=cur["temp_c"],
            feels_like_c=cur["feelslike_c"],
            humidity=cur["humidity"],
            wind_kph=cur["wind_kph"],
            condition=cur["condition"]["text"],
        )

    def summary(self):
        return (
            f"Weather in {self.city}, {self.country}\n"
            f"{'-' * 32}\n"
            f"Local time : {self.local_time}\n"
            f"Condition  : {self.condition}\n"
            f"Temp       : {self.temp_c:.1f} °C\n"
            f"Feels like : {self.feels_like_c:.1f} °C\n"
            f"Humidity   : {self.humidity} %\n"
            f"Wind       : {self.wind_kph:.1f} km/h"
        )

# Read the API key from a .env file; do not hard-code the key.
load_dotenv()
api_key = os.getenv('API_KEY')

url = f'https://api.weatherapi.com/v1/current.json?'
params = {"key": api_key, "q": "Cairo"}

# Call a public REST API using the API key.
try:
    response = requests.get(url, params=params, timeout=10)
    if response.status_code != 200 and response.status_code != 201:
        print(f'Error Occuared: {response}')
    else:

        # Parse the API's JSON response.
        json_obj = response.json()

        # Store the relevant response data in a small class.
        weatherObj = Weather.from_api(json_obj)
        
        # Print a formatted summary of the stored results.
        summary = weatherObj.summary()
        print(summary)

except Exception as ex:
    print(f'Exception Occuared: {ex}')

