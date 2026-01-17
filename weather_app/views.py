from django.shortcuts import render
from django.contrib import messages
from .services import OpenWeatherService

# REQUIREMENT: App 2 accessing App 1 models
from location_app.models import SearchHistory

def get_client_ip(request):
    """Utility to handle IP detection through proxies or local dev."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    
    # Mock a public IP if testing on localhost (127.0.0.1)
    if ip == '127.0.0.1' or ip == '::1':
        #return '8.8.8.8'  # Example: Mountain View, CA
        return '66.249.66.1'  # Example: 
    return ip

def weather_dashboard(request):
    """
    Main view that coordinates the API call and data persistence.
    """
    client_ip = get_client_ip(request)
    
    # 1. Use the Service to talk to OpenWeatherMap
    result = OpenWeatherService.get_weather_by_ip(client_ip)
    
    location_data = None
    weather_data = None
    city_name = None
    
    if result:
        location_data = result.get('location')
        weather_data = result.get('weather')
        city_name = location_data.get('EnglishName', 'Unknown City') if location_data else None
        
        # 2. Persistence: Save to location_app (Requirement: Interaction between apps)
        # We wrap this in a try/except to ensure the page loads even if DB write fails
        if city_name:
            try:
                SearchHistory.objects.create(
                    ip_address=client_ip,
                    city_name=city_name,
                    location_key=city_name  # Using city name as location key
                )
            except Exception as e:
                print(f"Database save failed: {e}")

    context = {
        'ip': client_ip,
        'location': location_data,
        'weather': weather_data,
    }
    
    return render(request, 'weather_app/dashboard.html', context)