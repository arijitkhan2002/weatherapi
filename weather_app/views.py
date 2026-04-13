import requests
from django.conf import settings
from django.shortcuts import render

def home(request):
    city = request.GET.get('city')
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')

    weather_data = {}
    error = None

    # 🌍 URL decide
    if lat and lon:
        url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={settings.API_KEY}&units=metric"
    else:
        city = city or "Kolkata"
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={settings.API_KEY}&units=metric"

    response = requests.get(url)
    data = response.json()

    # ❌ error check
    if data.get("cod") != "200":
        return render(request, "index.html", {
            "weather": {},
            "error": "City not found or API error",
            "labels": [],
            "temp": [],
            "humidity": [],
            "wind": [],
            "forecast": []
        })

    # 📊 chart data
    labels = []
    temp = []
    humidity = []
    wind = []
    forecast = []

    for item in data.get('list', [])[:8]:
        labels.append(item['dt_txt'].split()[1][:5])
        temp.append(item['main']['temp'])
        humidity.append(item['main']['humidity'])
        wind.append(item['wind']['speed'])

    # 🌦 forecast
    days = {}
    for item in data.get('list', []):
        date = item['dt_txt'].split()[0]
        if date not in days:
            days[date] = item

    for d in list(days.values())[:5]:
        forecast.append({
            'date': d['dt_txt'].split()[0],
            'temp': d['main']['temp'],
            'icon': d['weather'][0]['icon']
        })

    # 🌤 CURRENT WEATHER (IMPORTANT FIX)
    current = data['list'][0]

    weather_data = {
        "temperature": current['main']['temp'],
        "city": city or "Kolkata",
        "icon": current['weather'][0]['icon'],
        "description": current['weather'][0]['description']
    }

    return render(request, "index.html", {
        "weather": weather_data,
        "error": None,
        "labels": labels,
        "temp": temp,
        "humidity": humidity,
        "wind": wind,
        "forecast": forecast
    })