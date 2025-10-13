import requests 
import pycountry
import os
from supabase import create_client, Client
from dotenv import load_dotenv, dotenv_values

load_dotenv()

supa_url=os.getenv("supabase_url")
supa_key=os.getenv("supabase_key")
w_api_key=os.getenv("weather_api")

supabase: Client = create_client(supa_url, supa_key)

def insert_city(city_id, city, country,lat,long):
    supabase.table("cities").upsert({
        "city_code": city_id,
        "city_name": city,
        "country": country,
        "latitude": lat,
        "longitude": long
    }).execute()

def get_country_name(code):
        country = pycountry.countries.get(alpha_2=code)
        return country.name if country else code
    
cities = [
    "New York", "Chicago", "Los Angeles", "Toronto", "Lima", "Bogota",
    "Santiago", "Buenos Aires", "Rio de Janeiro", "Mexico City",
    "Guangzhou", "Kobe", "Busan", "George Town", "Chiang Mai",
    "Visakhapatnam", "Mangaluru", "Kochi", "Chennai", "Panaji"
] 

def fetch_and_store():
  for city in cities:
                  url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={w_api_key}&units=metric'
                  response = requests.get(url)

                  if response.status_code != 200:
                      print(f"Failed for {city}: {response.status_code} - {response.text}")
                      continue 
                  data = response.json()
                  
                  country_name=get_country_name(data["sys"]["country"])

                  insert_city(data["id"], data["name"], country_name,data["coord"]["lat"],data["coord"]["lon"])
                  print(f"Inserted data for {data['name']}")

if __name__ == "__main__":
    fetch_and_store()              
  
