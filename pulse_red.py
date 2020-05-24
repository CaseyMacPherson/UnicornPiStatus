#!/usr/bin/env python

import time
import unicornhat as unicorn


unicorn.set_layout(unicorn.AUTO)
unicorn.rotation(0)
unicorn.brightness(1.0)
width,height=unicorn.get_shape()


for redvalue in range(48,255):
    for y in range(height):
        for x in range(width):
            unicorn.set_pixel(x,y,redvalue,0,0)
    unicorn.show()


while True:
    time.sleep(1)
