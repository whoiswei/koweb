from django.apps import AppConfig
import os

class SensorsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sensors'

    def ready(self):
        # Prevent starting MQTT multiple times in development with auto-reloader
        if os.environ.get('RUN_MAIN') == 'true' or not os.environ.get('SERVER_GATEWAY_INTERFACE'):
            from .mqtt import start_mqtt
            start_mqtt()
