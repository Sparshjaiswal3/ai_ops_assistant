import requests
import os
from .base import register_tool

@register_tool("get_weather")
class WeatherTool:
    """Fetches current weather for a city."""
    def execute(self, city):
        api_key = os.getenv("OPENWEATHER_API_KEY")
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        
        try:
            response = requests.get(url)
            if response.status_code == 404:
                return f"City '{city}' not found."
            response.raise_for_status()
            data = response.json()
            return {
                "city": data["name"],
                "temperature": f"{data['main']['temp']}°C",
                "condition": data["weather"][0]["description"]
            }
        except Exception as e:
            return f"Error fetching weather: {str(e)}"