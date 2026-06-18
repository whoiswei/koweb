import paho.mqtt.client as mqtt
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

MQTT_BROKER = "127.0.0.1"
MQTT_PORT = 1883
MQTT_TOPICS = [("sensor/temperature", 0), ("sensor/humidity", 0), ("sensor/light", 0)]

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info(f"Connected to MQTT Broker at {MQTT_BROKER}:{MQTT_PORT}")
        client.subscribe(MQTT_TOPICS)
    else:
        logger.error(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    try:
        topic = msg.topic
        payload = msg.payload.decode('utf-8')
        value = float(payload)
        
        from .models import SensorData
        SensorData.objects.create(topic=topic, value=value)
        logger.info(f"Saved {topic}: {value}")
    except ValueError:
        logger.error(f"Invalid payload for topic {msg.topic}: {msg.payload}")
    except Exception as e:
        logger.error(f"Error saving MQTT message: {e}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

def start_mqtt():
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()
    except Exception as e:
        logger.error(f"Failed to start MQTT client: {e}")
