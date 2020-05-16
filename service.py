import paho.mqtt.client as mqtt
import os

def on_connect(client, userdata, flags, rc):
    print("Connected with result code"+str(rc))
    client.subscribe("/workstatus")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

mqtthost = os.environ.get("MQTT_HOST")
if mqtthost == None:
  raise Exception("Missing Environment Setting","MQTT_HOST")

client.connect(mqtthost,1883,60)

client.loop_forever()
