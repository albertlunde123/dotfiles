#!/usr/bin/env zsh

# Connect or Disconnect from Powerbeats Pro

device="50:DE:06:E9:28:3E"
notification_id=9999 # Arbitrary ID to update the notification

# Check if the device is already connected
connected=$(bluetoothctl info $device | grep 'Connected: yes')

any_connected=$(bluetoothctl paired-devices | grep 'Device' | grep -v $device)

if [ -z "$any_connected" ]; then
    echo "False"
else
    echo "True"
fi
