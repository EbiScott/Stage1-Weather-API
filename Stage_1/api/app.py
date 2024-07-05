import os
from flask  import Flask, request, jsonify
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def get_ip(ip):
    try:
        visitor_ip = requests.get(f"https://ip-api.com/json/{ip}")
        return visitor_ip.json()
    except Exception as e:
        return {"city": "Unknown", "temperature": "Unknown"}

def get_weather(city):
    api_key = os.getenv("OPEN_WEATHER_API_KEY")

    try:
        city = get_ip(request.remote_addr)["city"]
        weather_reply = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric")
        weather =  weather_reply.json()
        return weather['main']['temp']
    except Exception as e:
        return "Unknown"



@app.route('/api/hello')
def hello():
    visitor_name = request.args.get('visitor_name', 'Guest')
    client_ip = request.remote_addr

    ip_info = get_ip(client_ip)
    city = ip_info.get('city', 'Unknown')
    temperature = get_weather(city)

    response = {
        "client_ip": client_ip,
        "location": city,
        "greeting": f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {city}"
    }
    
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)