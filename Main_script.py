import requests
import datetime
import pytz
from supabase import create_client, Client
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()

supa_url = os.getenv("SUPABASE_URL")
supa_key = os.getenv("SUPABASE_KEY")
w_api_key = os.getenv("WEATHER_API")

supabase: Client = create_client(supa_url, supa_key)

cities = [
    "New York", "Chicago", "Los Angeles", "Toronto", "Lima", "Bogota",
    "Santiago", "Buenos Aires", "Rio de Janeiro", "Mexico City",
    "Guangzhou", "Kobe", "Busan", "George Town", "Chiang Mai",
    "Visakhapatnam", "Mangaluru", "Kochi", "Chennai", "Panaji"
]

def insert_weather_condition(weather_id, climate, description, cloud):
   
    res = supabase.table("weather_condition").select("weather_id") \
        .eq("climate", climate) .eq("climate_condition", description) .execute()
    
    if res:
        supabase.table("weather_condition").upsert({
            "weather_id": weather_id,
            "climate": climate,
            "climate_condition": description,
            "cloudiness": cloud
        }).execute()
    else:
        supabase.table("weather_condition").insert({
            "weather_id": weather_id,
            "climate": climate,
            "climate_condition": description,
            "cloudiness": cloud
        }).execute()
                 
ist = pytz.timezone('Asia/Kolkata')

def insert_weather_record(city_id, weather_id, city_name, temp, feels_like, temp_min, temp_max, wind_speed, pressure, humidity):
    supabase.table("weather_data").upsert({
        "record_time": datetime.datetime.now(ist).strftime('%H:%M'),
        "date": datetime.date.today().isoformat(),           
       "city_id": city_id,
       "weather_id": weather_id,
        "city_name": city_name,
        "temperature": temp,
        "feels_like_temp": feels_like,
        "temp_min": temp_min,
        "temp_max": temp_max,
        "wind_speed": wind_speed,
        "presasure": pressure,
        "humidity": humidity,
    }).execute()

def fetch_and_store():
    for city in cities:
                url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={w_api_key}&units=metric'
                response = requests.get(url)

                if response.status_code != 200:
                    print(f"Failed for {city}: {response.status_code} - {response.text}")
                    continue 
                data = response.json()
                
                insert_weather_condition(
                     data["weather"][0]["id"],data["weather"][0]["main"],data["weather"][0]["description"],data["clouds"]["all"]
                     )

                insert_weather_record(
                     data["id"], data["weather"][0]["id"], data["name"],
                     data["main"]["temp"], data["main"]["feels_like"],
                     data["main"]["temp_min"], data["main"]["temp_max"],data["wind"]["speed"],
                     data["main"]["pressure"], data["main"]["humidity"]
                     )

if __name__ == "__main__":
    fetch_and_store()
