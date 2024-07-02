import os
from flask  import Flask, request, jsonify
import requests
from dotenv import load.env


app = Flask(__name__)

def get_ip(ip):
    try:
        visitor_ip = request.get(f"https://ip-api.com/json/{ip}")
        return visitor_ip.json()
    except Exception as e:
        return {"city": "Unknown", "country": "Unknown"}

def get_weather(city):
    api_key = os.getenv("OPEN_WEATHER_API_KEY")
    try:
        city = get_ip(request.remote_addr)["city"]
        weather = request.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric")
        weather =  weather.json()
        return weather['main']['temp']
    except Exception as e:
        return {"weather": "Unknown"}

def user_guest():
    user = {
        "visitor_name": "Mark",
        "city": city,
        "weather": weather
    }


@app.route('/api/hello')
def hello():
    visitor_name = request.args.get()
    visitor_ip = request.remote_addr

    return jsonify(user), 200



if __name__ == "__main__":
    app.run(debug=True)