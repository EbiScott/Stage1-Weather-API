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
    return city


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


@app.route('/api/hello')
def hello():
    visitor_name = request.args.get('visitor_name', 'Guest')
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()
    city = get_ip(client_ip)
        
    if city:
        temperature, city_new = get_weather(city)
        greeting = f"Hello, {visitor_name}! The temperature is {temperature} degrees Celsius in {city_new}"
    else:
        city_new = "Unknown"
        greeting = f"Hello, {visitor_name}! Unfortunately, I could not determine your location"

    response = {
        "client_ip": client_ip,
        "greeting": greeting,
        "location": city_new
    }
    
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)