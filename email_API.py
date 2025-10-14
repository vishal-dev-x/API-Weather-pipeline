from email.message import EmailMessage
import ssl
import smtplib
import requests
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()

MY_EMAIL=os.getenv("MY_EMAIL")
password=os.getenv("PASSWORD")
TO_list=os.getenv("TO")
w_api_key = os.getenv("WEATHER_API")

city="Bangalore"

url =f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={w_api_key}&units=metric'
response = requests.get(url)
data=response.json()

subject=  f"Weather Update for {data['name']} (City ID: {data['id']})"
body=(f"""
Hello,

Here is the current weather update for {data['name']}:

- Weather: {data['weather'][0]['main']} ({data['weather'][0]['description']})
- Temperature: {data['main']['temp']}°C (Feels like {data['main']['feels_like']}°C)
- Minimum Temperature: {data['main']['temp_min']}°C
- Maximum Temperature: {data['main']['temp_max']}°C
- Humidity: {data['main']['humidity']}%
- Atmospheric Pressure: {data['main']['pressure']}hPa
- Wind Speed: {data['wind']['speed']} m/s
- Cloud Coverage: {data['clouds']['all']}%

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
