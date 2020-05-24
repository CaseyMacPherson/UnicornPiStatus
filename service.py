import paho.mqtt.client as mqtt
import os
import threading
import logging
import time
import unicornhat as unicorn
import json

class SharedContext:
  current_color = "off"

shared_context = SharedContext()


def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  
  if rc == 0:
    client.subscribe("homeassistant/pistatus/light/status")
    client.subscribe("homeassistant/pistatus/light/switch")
    client.subscribe("homeassistant/pistatus/light/brightness")
    client.subscribe("homeassistant/pistatus/light/brightness/set")

    do_mqtt_advertisement(client)

def on_message(client, userdata, msg):
  print(msg.topic+" "+str(msg.payload))
  shared_context.current_color = str(msg.payload.decode("utf-8"))

def do_mqtt_advertisement(client):
  config = {
    "name" : "pistatus",
    "payload_on" : "ON",
    "payload_off" : "OFF",
    "qos" : 0,
    "optimistic" : False,
    "state_topic" : "pistatus/light/status",
    "command_topic" : "pistatus/light/switch",
    "brightness_state_topic" : "pistatus/light/brightness",
    "brightness_command_topic" : "pistatus/light/brightness/set"
  }

  client.publish("homeassistant/light/pistatus/config",json.dumps(config))

def set_color(r,g,b):
  width,height=unicorn.get_shape()
  for y in range(height):
    for x in range(width):
        unicorn.set_pixel(x,y,r,g,b)
  unicorn.show()

def do_light_thing(context):
  unicorn.set_layout(unicorn.AUTO)
  unicorn.rotation(0)
  unicorn.brightness(.40)

  while True:
    if context.current_color == "green" :
      set_color(0,255,0)
    elif context.current_color == "red" :
      set_color(255,0,0)
    elif context.current_color == "blue" :
      set_color(0,0,255)
    else:
      unicorn.clear()
      unicorn.show()
    time.sleep(1.0)

if __name__ == "__main__":

  mqtthost = os.environ.get("MQTT_HOST")
  if mqtthost == None:
    raise Exception("Missing Environment Setting","MQTT_HOST")

  client = mqtt.Client()
  client.on_connect = on_connect
  client.on_message = on_message

  light_control_thread = threading.Thread(target=do_light_thing, args=(shared_context,))
  light_control_thread.daemon = True
  light_control_thread.start()
  
  client.connect(mqtthost,1883,60)
  client.loop_forever()


