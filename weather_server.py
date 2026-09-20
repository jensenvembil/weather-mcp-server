import os
import httpx
from mcp.server.mcpserver import MCPServer

mcp = MCPServer(name="OpenWeatherMap")

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

print(f"OPENWEATHER_API_KEY: {OPENWEATHER_API_KEY}")

GEO_URL = "http://openweathermap.org"
WEATHER_URL = "https://api.openweathermap.org"



@mcp.tool()
async def get_weather(city: str, country: str ="") -> str:
    """
    Fetch the current real-time weather information for a given city.

    Args:
        city: The name of the city (e.g., "Paris", "Berlin", "Tokyo").
        country: Optional two-letter ISO country code (e.g., "FR", "DE", "JP").
    """
    if not OPENWEATHER_API_KEY:
        return "Error: OPENWEATHER_API_KEY is not set. Please set it as an environment variable."

    params = {
        "q": f"{city},{country}" if country else city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"  # You can change this to "imperial" for Fahrenheit
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{WEATHER_URL}/data/2.5/weather", params=params)
        except httpx.HTTPError as e:
            return f"Error fetching ju weather data: {e}"

    if response.status_code != 200:
        return f"Error fetching weather data: {response.text}"

    data = response.json()
    weather_description = data["weather"][0]["description"]
    temperature = data["main"]["temp"]

    return f"The current weather in {city} is {weather_description} with a temperature of {temperature}°C."


if __name__ == "__main__":
    mcp.run()