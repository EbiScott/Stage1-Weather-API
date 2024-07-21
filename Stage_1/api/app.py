import os
from flask  import Flask, request, jsonify
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def get_ip(ip):
    visitor_ip = requests.get(f"https://ip-api.com/json/{ip}")
    response =  visitor_ip.json()
    city = response.get("city", "Unknown")
    region = response.get("region", "Unknown")
    country = response.get("country", "Unknown")
    return city, region, country


def get_weather(city):
    api_key = os.getenv("WEATHERAPI_KEY")
    weather_reply = requests.get(f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no")
    weather =  weather_reply.json()

    if "current" in weather:
        temperature = weather['current']['temp_c']
    else:
        temperature = "N/A"

    if "location" in weather:
        city_new = f"{weather['location']['name']}"
    else:
        city_new = "N/A"
    
    return temperature, city_new

def create_greeting(ip):
    city, region, country = get_ip(ip)
    temperature, resolved_city = get_weather(city)
    
    if resolved_city != "N/A" and temperature != "N/A":
        greeting = f"Hello, {city}! The temperature is {temperature} degrees Celsius in {region} {country}"
    else:
        greeting = "Hello, Someone! Unfortunately, I could not determine your location"
    
    result = {
        "client_ip": ip,
        "greeting": greeting,
        "location": f"{region} {country}" if resolved_city != "N/A" else "Unknown"
    }
    
    return result

    
@app.route('/api/hello')
def hello():
    ip = request.remote_addr
    result = create_greeting(ip)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)