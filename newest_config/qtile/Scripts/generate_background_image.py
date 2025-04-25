from PIL import Image
import os

# Create a new image with a specific color
# color: a tuple of 3 integers (0-255) representing the RGB color

def convert_hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def create_image(color):
    image = Image.new("RGB", (800, 600), color)
    image.save(os.path.expanduser("~/.config/qtile/background.png"))

path = os.path.expanduser("~/.cache/wal/background")

if os.path.exists(path):
    with open(path, "r") as f:
        color = f.read().strip()
        color = convert_hex_to_rgb(color)
        create_image(color)
    
print(color)
