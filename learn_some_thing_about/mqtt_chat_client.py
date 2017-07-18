import paho.mqtt.client as mqtt
import json

def on_connect(client, user, data, flags, rc):
    print("Connected with result code" + str(rc))

    client.subscribe("chat")
    client.publish("chat", json.dumps({"user": user, "say": "Hello, anyone!"}))
