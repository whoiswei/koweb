import paho.mqtt.client as mqtt
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

MQTT_BROKER = "127.0.0.1"
MQTT_PORT = 1883
MQTT_TOPICS = [("escaperoom/pico/sensors", 0)]

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info(f"Connected to MQTT Broker at {MQTT_BROKER}:{MQTT_PORT}")
        client.subscribe(MQTT_TOPICS)
    else:
        logger.error(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    try:
        topic = msg.topic
        payload_str = msg.payload.decode('utf-8')
        
        if topic == "escaperoom/pico/sensors":
            import json
            data = json.loads(payload_str)
            
            from .models import SensorData
            
            # 將每一個 key-value 存入 DB
            for key, val in data.items():
                SensorData.objects.create(topic=key, value=str(val))
                
            logger.info(f"Saved all Pico W sensor data: {data}")
            
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON payload for topic {msg.topic}: {msg.payload}")
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
