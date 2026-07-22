import requests

# API_KEY = "c968c19d5c4da554e1e5d5ea4ce7b778"
# BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city):

    API_KEY = "c968c19d5c4da554e1e5d5ea4ce7b778"
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"

    complete_url = BASE_URL + "q=" + city + "&appid="+API_KEY+"&units=metric"

    response = requests.get(complete_url)
    data = response.json()
    print(data)
    if data['cod'] != "404":
        main = data["main"]
        weather = data["weather"][0]
        temperature = main['temp']
        weather_description = weather['description']
        return f"The temperature in {city} is {temperature} celisus with {weather_description}"
    else:
        return "city not found"

city = "New York"
weather_update = get_weather(city)
print(F"weather Update: {weather_update}")

#     params = {
#         "q": city,
#         "appid": API_KEY,
#         "units": "metric"
#     }

#     try:
#         response = requests.get(BASE_URL, params=params)
#         response.raise_for_status()

#         data = response.json()

#         temperature = data["main"]["temp"]
#         humidity = data["main"]["humidity"]
#         description = data["weather"][0]["description"]

#         return (
#             f"Weather in {city}\n"
#             f"Temperature: {temperature}°C\n"
#             f"Humidity: {humidity}%\n"
#             f"Condition: {description.capitalize()}"
#         )

#     except requests.exceptions.HTTPError:
#         return "City not found."

#     except Exception as e:
#         return f"Error: {e}"


# if __name__ == "__main__":
#     city = input("Enter city name: ")
#     print(get_weather(city))