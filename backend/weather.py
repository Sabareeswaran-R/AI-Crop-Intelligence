import requests


# ==========================================
# WEATHER API SERVICE
# ==========================================

def get_weather(latitude, longitude):

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "rain",
            "wind_speed_10m"
        ],
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
            "rain_sum"
        ],
        "forecast_days": 7,
        "timezone": "auto"
    }

    response = requests.get(
        url,
        params=params,
        timeout=15
    )

    response.raise_for_status()

    return response.json()


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    # Example coordinates
    latitude = 11.0168
    longitude = 76.9558

    weather = get_weather(
        latitude,
        longitude
    )

    print("====================================")
    print("       WEATHER DATA")
    print("====================================")

    print(
        "Temperature:",
        weather["current"]["temperature_2m"],
        "°C"
    )

    print(
        "Humidity:",
        weather["current"]["relative_humidity_2m"],
        "%"
    )

    print(
        "Rain:",
        weather["current"]["rain"],
        "mm"
    )

    print(
        "Wind Speed:",
        weather["current"]["wind_speed_10m"],
        "km/h"
    )

    print("------------------------------------")
    print("7-DAY FORECAST")
    print("------------------------------------")

    dates = weather["daily"]["time"]

    max_temp = weather["daily"]["temperature_2m_max"]

    min_temp = weather["daily"]["temperature_2m_min"]

    rainfall = weather["daily"]["precipitation_sum"]

    for i in range(len(dates)):

        print(
            dates[i],
            "| Max:",
            max_temp[i],
            "°C | Min:",
            min_temp[i],
            "°C | Rain:",
            rainfall[i],
            "mm"
        )