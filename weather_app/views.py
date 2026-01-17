from django.shortcuts import render
from django.contrib import messages
from .services import AccuWeatherService

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
    
    # 1. Use the Service to talk to AccuWeather (Requirement: API Access)
    location_data = AccuWeatherService.get_location_by_ip(client_ip)
    weather_data = None
    
    if location_data and 'Key' in location_data:
        location_key = location_data['Key']
        city_name = location_data.get('EnglishName', 'Unknown City')
        
        # 2. Fetch the actual current weather conditions
        weather_data = AccuWeatherService.get_current_conditions(location_key)
        
        # 3. Persistence: Save to location_app (Requirement: Interaction between apps)
        # We wrap this in a try/except to ensure the page loads even if DB write fails
        try:
            SearchHistory.objects.create(
                ip_address=client_ip,
                city_name=city_name,
                location_key=location_key
            )
        except Exception as e:
            print(f"Database save failed: {e}")

    context = {
        'ip': client_ip,
        'location': location_data,
        'weather': weather_data,
    }
    
    return render(request, 'weather_app/dashboard.html', context)