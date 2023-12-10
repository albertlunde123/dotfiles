import subprocess

other_names = {"WH-1000XM3": "Daddy's Headphones"}

def get_connected_bluetooth_device_name():
    """Get the name of the connected bluetooth device"""
    try:
        name = subprocess.check_output(["/usr/bin/bluetoothctl", "info"]).decode("utf-8").split("\n")[1].split(" ")[1]
    
        if name in other_names:
            return other_names[name]
    except:
        return None

# print(get_connected_bluetooth_device_name())

# if type("This is a string") == str:
#     print("This is a string")
