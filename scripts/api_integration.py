import requests

# API_KEY = "c968c19d5c4da554e1e5d5ea4ce7b778"
# BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city):

    API_KEY = "c968c19d5c4da554e1e5d5ea4ce7b778"
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"

    complete_url = f"{BASE_URL}q={city}&appid={API_KEY}&units=metric"

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

def get_news():
    api_key = "4986bc0fe00e43cfb823aed7422c257e"
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"

    response = requests.get(url)
    data = response.json()
    if data["status"] == "ok":
        aritcles = data['articles']
        news_list = [f"{article['title'] - {article['source']['name']}}" for article in aritcles[:5]]
        return "Here are top news headlines:\\\\n" + "\\\n".join(news_list)
    else:
        return "Unable to fetch news at the moment"

news_update = get_news()
print(f"News Update: {news_update}")
