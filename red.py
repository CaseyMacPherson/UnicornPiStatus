#!/usr/bin/env python

import time
import unicornhat as unicorn


unicorn.set_layout(unicorn.AUTO)
unicorn.rotation(0)
unicorn.brightness(1.0)
width,height=unicorn.get_shape()


for y in range(height):
    for x in range(width):
        unicorn.set_pixel(x,y,48,0,0)

unicorn.show()

while True:
    time.sleep(1)
