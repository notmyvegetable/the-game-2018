#!/usr/bin/python3

from PIL import Image
import sys

img = Image.open(sys.argv[1])
img.load()

oimg = Image.open(sys.argv[1])
oimg.load()

width = img.width
height = img.height
inc = int(sys.argv[2])

for x in range(0, width):
    for y in range(0, height):
        pix = img.getpixel((x,y))
        if pix[2] & inc:
            pix = (0, 0, 255)
        else:
            pix = (0, 0, 0)
        oimg.putpixel((x,y), pix)

oimg.show()
