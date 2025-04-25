import pyautogui
import subprocess

def get_pixel_color(x, y):
    return pyautogui.screenshot().getpixel((x, y))

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

def send_notification(message):
    subprocess.run(['dunstify', message])

def main():
    x, y = pyautogui.position()
    color = get_pixel_color(x, y)
    color_hex = rgb_to_hex(color)
    send_notification(f"RGB: {color} \n Hex: {color_hex}")

if __name__ == "__main__":
    main()

