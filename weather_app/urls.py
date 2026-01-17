from django.urls import path
from . import views  # Import views from the current directory

urlpatterns = [
    # This maps 'http://127.0.0.1:8000/weather/dashboard/' to your view
    path('dashboard/', views.weather_dashboard, name='weather_dashboard'),
]