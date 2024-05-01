from django.db import models

class Reading(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    nitrogen_level = models.DecimalField(max_digits=10, decimal_places=2)
    phosphorus_level = models.DecimalField(max_digits=10, decimal_places=2)
    potassium_level = models.DecimalField(max_digits=10, decimal_places=2)
    temperature = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    humidity = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"NPK Sensor Reading - Timestamp: {self.timestamp} - Nitrogen Level: {self.nitrogen_level} - Phosphorus Level: {self.phosphorus_level} - Potassium Level: {self.potassium_level} -  Temperature: {self.temperature} - Humidity: {self.humidity}"

