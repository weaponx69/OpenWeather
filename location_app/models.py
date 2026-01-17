from django.db import models
from django.core.validators import MinLengthValidator

class SearchHistory(models.Model):
    ip_address = models.GenericIPAddressField()
    city_name = models.CharField(max_length=100, validators=[MinLengthValidator(2)])
    location_key = models.CharField(max_length=50)
    search_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # REQUIREMENT: Good string method
        return f"{self.city_name} searched by {self.ip_address} at {self.search_time}"