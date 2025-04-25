import subprocess

def toggle_keyboard_layout(qtile):
    current_layout = subprocess.check_output("/usr/bin/setxkbmap -query | grep layout | awk '{print $2}'", shell=True).decode('utf-8').strip()
    if current_layout == 'us':
        subprocess.call(['/usr/bin/setxkbmap', '-layout', 'dk'])
    else:
        subprocess.call(['/usr/bin/setxkbmap', '-layout', 'us'])

# bluetooth functions

other_names = {"WH-1000XM3": "Daddy's Headphones"}

def get_connected_bluetooth_device_name():
    """Get the name of the connected bluetooth device"""
    try:

        prepend =  "  - "
        name = subprocess.check_output(["/usr/bin/bluetoothctl", "info"]).decode("utf-8").split("\n")[1].split(" ")[1]
    
        if name in other_names:
            return prepend + other_names[name]
        return prepend + name

    except:
        return " No device connected"

def launch_pdf_selector():
    """Launch the PDF selector tool"""
    import os
    import subprocess
    script_path = os.path.expanduser("~/.config/qtile/Scripts/pdf_selector.py")
    subprocess.Popen(["python3", script_path])
# print(get_connected_bluetooth_device_name())
