#!.local/bin/zsh

# get the bluez_sink. ... . part
sinks=$(pactl list short sinks | grep bluez_sink | cut -f 2)
# list all pactl sink names
if [[ $(pactl list sinks | grep Name | cut -d " " -f 2) ]]; then
    pactl set-sink-volume $sinks -5%
else
    pactl set-sink-volume alsa_output.pci-0000_00_1b.0.analog-stereo +5%
fi

pulsemixer --max-volume 100
