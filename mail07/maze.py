#!/usr/bin/python3

###########################################################
#                                                         #
#  THIS IS ALL INEFFICIENT I KNOW BUT TIME WAS A CONCERN  #
#                                                         #
###########################################################

from PIL import Image
import sys

# haha fun
sys.setrecursionlimit(100000)

img = Image.open(sys.argv[1])
img.load()

class tile():
    Walkable = 0
    Walked = 1
    Wall = 2
    SecurityGuard = 3
    Camera = 4
    WinnerWinnerChickenDinner = 5

def getpoint(x, y):
    if x < 0 or y < 0:
        return tile.Wall
    if x > img.width or y > img.height:
        return tile.Wall

    pix = img.getpixel((x, y))
    if pix == (0, 0, 0, 255):
        return tile.Wall
    if pix == (255, 255, 255, 255):
        return tile.Walked
    if pix == (34, 34, 34, 255):
        return tile.Walkable
    if pix == (255, 0, 0, 255):
        return tile.Camera
    if pix == (0, 0, 255, 255):
        return tile.SecurityGuard
    if pix == (255, 255, 0, 255):
        return tile.WinnerWinnerChickenDinner
    return tile.Wall

def setpoint(x, y, tp):
    if tp == tile.Walked:
        img.putpixel((x,y), (255, 255, 255, 255))
    elif tp == tile.Walkable:
        img.putpixel((x,y), (34, 34, 34, 255))
    elif tp == tile.Camera:
        img.putpixel((x,y), (255, 0, 0, 255))
    elif tp == tile.SecurityGuard:
        img.putpixel((x,y), (0, 0, 255, 255))
    return

positions = ((-1, 0), (0, -1), (0, 1), (1, 0))

def solve(x, y):
    tp = getpoint(x, y)
    if tp == tile.WinnerWinnerChickenDinner:
        return 1

    setpoint(x, y, tile.Walked)
    for i in range(0, 4):
        ret = getpoint(x + positions[i][0], y + positions[i][1])
        if ret == tile.Walkable or ret == tile.SecurityGuard or ret == tile.Camera or ret == tile.WinnerWinnerChickenDinner:
            res = solve(x + positions[i][0], y + positions[i][1])
            if res != 0:
                print(str(res))
                if tp == tile.Walkable or tp == tile.WinnerWinnerChickenDinner:
                    return 1 + res
                if tp == tile.Camera:
                    return 3 + res # Should be 2 but quick hack to make it work
                if tp == tile.SecurityGuard:
                    return 2 + res
    setpoint(x, y, tp)
    return 0
sol = solve(0, 1)

img.show()
print("Previous number")
