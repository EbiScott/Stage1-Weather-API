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
        city_new = f"{weather['location']['name']}, {weather['location']['region']}"
    else:
        city_new = "N/A"
    
    return temperature, city_new


@app.route('/api/hello')
def hello():
    visitor_name = request.args.get('visitor_name', 'Guest')
    client_ip = request.remote_addr

    print(f"client_ip: {client_ip}")

    city = get_ip(client_ip)
    
    print(f"city: {client_ip}")
    
    if city != "Unknown":
        temperature, city_new = get_weather(city)

        print(f"temperature: {temperature}")

        greeting = f"Hello, {visitor_name}! The temperature is {temperature} degrees Celsius in {city_new}"

    else:
        city_new = "Unknown"
        greeting = f"Hello, {visitor_name}! Unfortunately, I could not determine your location"

    response = {
        "client_ip": client_ip,
        "location": city_new,
        "greeting": greeting
    }
    
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)