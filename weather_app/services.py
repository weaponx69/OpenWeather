import requests
import logging
from django.conf import settings

# Set up logging to help debug API issues
logger = logging.getLogger(__name__)

class AccuWeatherService:
    """
    Handles all interactions with the AccuWeather API.
    Requirement: Third-party API with Authentication (Bearer Token).
    """
    BASE_URL = "https://dataservice.accuweather.com"

    @classmethod
    def get_auth_headers(cls):
        """Returns the headers required for AccuWeather authentication."""
        return {
            "Authorization": f"Bearer {settings.ACCUWEATHER_API_KEY}",
            "Accept-Encoding": "gzip,deflate",  # Recommended for performance
            "Content-Type": "application/json"
        }

    @classmethod
    def get_location_by_ip(cls, ip_address):
        endpoint = f"{cls.BASE_URL}/locations/v1/cities/ipaddress"
        params = {"q": ip_address}
        
        # FIX: Initialize response as None
        response = None 
        
        try:
            response = requests.get(
                endpoint, 
                headers=cls.get_auth_headers(), 
                params=params,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.HTTPError as http_err:
            # Now 'response' is guaranteed to exist (either as None or an object)
            status = response.status_code if response else "No Response"
            logger.error(f"HTTP error: {http_err} - Status: {status}")
        except Exception as err:
            logger.error(f"An error occurred: {err}")
            
        return None

    @classmethod
    def get_current_conditions(cls, location_key):
        """
        Calls the /currentconditions/v1/ endpoint using a Location Key.
        This allows you to get the actual temperature and weather text.
        """
        endpoint = f"{cls.BASE_URL}/currentconditions/v1/{location_key}"
        
        try:
            response = requests.get(
                endpoint, 
                headers=cls.get_auth_headers(),
                timeout=10
            )
            response.raise_for_status()
            
            # Current conditions usually returns a list; we want the first item
            data = response.json()
            return data[0] if data else None
            
        except Exception as err:
            logger.error(f"Error fetching conditions: {err}")
            return None