from django.db import models

class SensorData(models.Model):
    topic = models.CharField(max_length=255, help_text="MQTT Topic")
    value = models.FloatField(help_text="Sensor Value")
    timestamp = models.DateTimeField(auto_now_add=True, help_text="Time received")

    def __str__(self):
        return f"{self.topic}: {self.value} at {self.timestamp}"

    class Meta:
        ordering = ['-timestamp']
