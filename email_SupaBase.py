from email.message import EmailMessage
import ssl
import smtplib
from supabase import create_client, Client
import os
from dotenv import load_dotenv, dotenv_values
from datetime import date, datetime
import time

load_dotenv()

supa_url = os.getenv("SUPABASE_URL")
supa_key = os.getenv("SUPABASE_KEY")
w_api_key = os.getenv("WEATHER_API")
MY_EMAIL=os.getenv("MY_EMAIL")
password=os.getenv("PASSWORD")
TO_list=os.getenv("TO")

supabase: Client = create_client(supa_url, supa_key)

today = date.today().isoformat() 
current_time = datetime.now().time().isoformat(timespec='seconds')

response= (
    supabase.table("weather_data")
    .select("*")
    .eq("city_id","1264527")
    .eq("date", today)
    .eq("record_time", current_time)
    .limit(1)
    .execute()
)

weather_data = response.data[0]

subject=  f"Weather Update for {weather_data['city_name']} (City ID: {weather_data['city_id']})"
body=(f"""
Hello,

Here is the current weather update for {weather_data['city_name']}:

- Temperature: {weather_data['temperature']}°C (Feels like {weather_data['feels_like_temp']}°C)
- Minimum Temperature: {weather_data['temp_min']}°C
- Maximum Temperature: {weather_data['temp_max']}°C
- Humidity: {weather_data['humidity']}%
- Atmospheric Pressure: {weather_data['presasure']}hPa
- Wind Speed: {weather_data['wind_speed']} m/s

Have a great day!

Best regards,
Your Weather Notification System
""")

em=EmailMessage()
em["From"]= MY_EMAIL
em["To"]= TO_list
em["Subject"]= subject
em.set_content(body)

context=ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
    smtp.login(MY_EMAIL,password) 
    smtp.sendmail(MY_EMAIL, TO_list, em.as_string())
