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

homeassistant_advertisement_topic = "homeassistant/light/pistatus/config"
state_topic = "homeassistant/pistatus/light/status"
command_topic = "homeassistant/pistatus/light/switch"
brightness_state_topic = "homeassistant/pistatus/light/brightness"
brightness_command_topic = "homeassistant/pistatus/light/brightness/set"
rgb_state_topic = "homeassistant/pistatus/light/rgb/status"
rgb_command_topic = "homeassistant/pistatus/light/rgb/set"



def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))

  if rc == 0:
    client.subscribe(state_topic)
    client.subscribe(command_topic)
    client.subscribe(brightness_state_topic)
    client.subscribe(brightness_command_topic)
    client.subscribe(rgb_state_topic)
    client.subscribe(rgb_command_topic)

    do_mqtt_advertisement(client)

def on_message(client, userdata, msg):
  print(msg.topic+" "+str(msg.payload))
  shared_context.current_color = str(msg.payload.decode("utf-8"))

def do_mqtt_advertisement(client):
  config = {
    "name" : "Work Light",
    "payload_on" : "ON",
    "payload_off" : "OFF",
    "qos" : 0,
    "optimistic" : False,
    "state_topic" : state_topic,
    "command_topic" : command_topic,
    "brightness_state_topic" : brightness_state_topic,
    "brightness_command_topic" : brightness_command_topic,
    "rgb_state_topic" : rgb_state_topic,
    "rgb_command_topic" : rgb_command_topic,
    "rgb_value_template" : "{{ value_json.rgb | join (',') }}",
    "brightness_value_template" : "{{ value_json.brightness }}",
    "state_value_template" : "{{ value_json.state }}"
  }

  client.publish(homeassistant_advertisement_topic,json.dumps(config))

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


