import paho.mqtt.client as mqtt import os import threading import logging import time import unicornhat as unicorn

class SharedContext:
  current_color = "green"

shared_context = SharedContext()

def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe("/pistatus/light/color")

def on_message(client, userdata, msg):
  print(msg.topic+" "+str(msg.payload))
  shared_context.current_color = str(msg.payload.decode("utf-8"))


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
  width,height=unicorn.get_shape()

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
    print("shared_context " + context.current_color)

if __name__ == "__main__":

  client = mqtt.Client()
  client.on_connect = on_connect
  client.on_message = on_message

  light_thread = threading.Thread(target=do_light_thing, args=(shared_context,))
  light_thread.start()

  mqtthost = os.environ.get("MQTT_HOST")
  if mqtthost == None:
    raise Exception("Missing Environment Setting","MQTT_HOST")

  client.connect(mqtthost,1883,60)

  client.loop_forever()

