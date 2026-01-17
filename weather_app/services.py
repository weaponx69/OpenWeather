import requests
import logging
from django.conf import settings

# Set up logging to help debug API issues
logger = logging.getLogger(__name__)

class OpenWeatherService:
    """
    Handles all interactions with the OpenWeatherMap API.
    Requirement: Third-party API with Authentication (API Key).
    Free tier: 60 calls/min, 1M calls/month
    """
    BASE_URL = "https://api.openweathermap.org/data/2.5"

    @classmethod
    def get_weather_by_ip(cls, ip_address):
        """
        Gets weather data for an IP address using geolocation and current weather.
        Uses the ip-api service (free, no key needed) to convert IP to coordinates,
        then fetches weather from OpenWeatherMap.
        """
        try:
            # Step 1: Get coordinates from IP using ip-api (free, no key needed)
            geo_response = requests.get(
                f"http://ip-api.com/json/{ip_address}",
                timeout=10
            )
            geo_response.raise_for_status()
            geo_data = geo_response.json()
            
            if geo_data.get('status') != 'success':
                logger.error(f"Could not geolocate IP {ip_address}")
                return None
            
            # Step 2: Get weather data using coordinates
            lat = geo_data.get('lat')
            lon = geo_data.get('lon')
            city = geo_data.get('city', 'Unknown')
            country = geo_data.get('countryCode', 'Unknown')
            
            weather_endpoint = f"{cls.BASE_URL}/weather"
            params = {
                "lat": lat,
                "lon": lon,
                "appid": settings.OPENWEATHER_API_KEY,
                "units": "imperial"  # Use Fahrenheit to match original
            }
            
            response = requests.get(
                weather_endpoint,
                params=params,
                timeout=10
            )
            response.raise_for_status()
            weather_data = response.json()
            
            # Format response to match expected structure
            return {
                "location": {
                    "EnglishName": city,
                    "Country": {"ID": country}
                },
                "weather": {
                    "Temperature": {
                        "Imperial": {"Value": round(weather_data['main']['temp'])}
                    },
                    "WeatherText": weather_data['weather'][0]['main'],
                    "WeatherIcon": weather_data['weather'][0].get('icon', '01d')
                }
            }
            
        except requests.exceptions.HTTPError as http_err:
            status = http_err.response.status_code if hasattr(http_err, 'response') else "Unknown"
            error_msg = http_err.response.text if hasattr(http_err, 'response') else "Unknown"
            logger.error(f"HTTP error: {http_err} - Status: {status} - Response: {error_msg}")
        except Exception as err:
            logger.error(f"An error occurred: {err}")
            
        return None