#!/usr/bin/env zsh

# Connect or Disconnect from Powerbeats Pro

device="50:DE:06:E9:28:3E"
notification_id=9999 # Arbitrary ID to update the notification

# Check if the device is already connected
connected=$(bluetoothctl info $device | grep 'Connected: yes')

if [ -z "$connected" ]; then
    # Device is not connected; connect it
    dunstify "Bluetooth connecting"
    bluetoothctl << EOF
    connect $device
EOF
if [ $? -eq 0 ]; then
    # skip the next notification
    i=0
else
    dunstify "Bluetooth failed to connect"
fi
else
    # Device is already connected; disconnect it
    dunstify "Bluetooth disconnecting"
    bluetoothctl << EOF
    disconnect $device
EOF
fi

