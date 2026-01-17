from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.views.generic import RedirectView  # Import the RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 1. ROOT REDIRECT
    # This sends anyone visiting '/' to '/weather/dashboard/'
    path('', RedirectView.as_view(url=reverse_lazy('weather_dashboard'), permanent=False)),
    
    # 2. APP URLS
    path('locations/', include('location_app.urls')),
    path('weather/', include('weather_app.urls')),
]