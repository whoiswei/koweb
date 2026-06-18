import paho.mqtt.client as mqtt
import time
import random

BROKER = "127.0.0.1"
PORT = 1883
TOPICS = ["sensor/temperature", "sensor/humidity", "sensor/light"]

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

client = mqtt.Client()
client.on_connect = on_connect

client.connect(BROKER, PORT, 60)
client.loop_start()

try:
    print("Starting to publish fake data... Press Ctrl+C to stop.")
    while True:
        temp = round(random.uniform(20.0, 30.0), 2)
        hum = round(random.uniform(40.0, 80.0), 2)
        light = round(random.uniform(100.0, 1000.0), 2)
        
        client.publish(TOPICS[0], str(temp))
        client.publish(TOPICS[1], str(hum))
        client.publish(TOPICS[2], str(light))
        
        print(f"Published - Temp: {temp}, Hum: {hum}, Light: {light}")
        time.sleep(5)
except KeyboardInterrupt:
    print("Stopped.")
    client.loop_stop()
    client.disconnect()
