#!/usr/bin/python3

from PIL import Image
import sys, math

def rot(n, a, b, rx, ry):
    if ry == 0:
        if rx == 1:
            a = n - 1 - a
            b = n - 1 - b
        t = a
        a = b
        b = t

def index2pos(n, index):
    a = b = 0
    i = 1
    d = index
    while i < n:
        rx = 1 & int(d/2)
        ry = 1 & (d ^ rx)
        rot(i, a, b, rx, ry)
        a += i * rx
        b += i * ry
        d = int(d/4)
        i *= 2

    return (a, b)

img = Image.open(sys.argv[1])
img.load()

oimg = Image.open(sys.argv[1])
oimg.load()

width = img.width
height = img.height
n = 2 ** int(sys.argv[2])
size = int(width / n)

def remap(dest, src, x, y, a, b, index):
    x *= size
    y *= size
    a *= size
    b *= size
    for i in range(0, size):
        for j in range(0, size):
            oimg.putpixel((x + j, y + i), img.getpixel((a + j, b + i)))

index = 0
for y in range(0, n):
    for x in range(0, n):
        a, b = index2pos(n, index)
        remap(oimg, img, x, y, a, b, index)
        index += 1

oimg.save("qr.png")

from pyzbar.pyzbar import decode
print(decode(Image.open("qr.png")))
