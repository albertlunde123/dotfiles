#!/usr/bin/env python

import pyautogui
import time
from subprocess import call

# Program som finder farvekoden på den givne pixel og sender en notifikation.

icon = "../../usr/share/icons/fontawesome/svgs/solid/palette.svg"

def rgb2hex(r, g, b):
    return "#{:02x}{:02x}{:02x}".format(r, g, b)

print("hello")
x, y = pyautogui.position()
pixelColor = pyautogui.screenshot().getpixel((x, y))

RGBToPrint = f"({pixelColor[0]}, {pixelColor[1]}, {pixelColor[2]})"
call(["dunstify", "RGB", RGBToPrint, "-r", "5"])


hex_icon =  "../../usr/share/icons/fontawesome/svgs/solid/hexagon.svg"

HexToPrint = f"({rgb2hex(pixelColor[0], pixelColor[1], pixelColor[2])})"
call(["dunstify", "Hex", HexToPrint, "-r", "6"])
# except KeyboardInterrupt:
#     print("doneso")
