import pulsectl

pulse = pulsectl.Pulse('qtile-volume-control')

def get_active_sink():
    # Get the list of sinks
    sinks = pulse.sink_list()
    # Find the default sink (or active sink)
    for sink in sinks:
        if sink.state == pulsectl.PulseStateEnum.running:
            return sink
    return None

def change_volume_up(qtile):
    sink = get_active_sink()
    if sink:
        volume = sink.volume
        # Adjust volume for all channels
        for i in range(len(volume.values)):
            volume.values[i] += 0.05
        pulse.volume_set(sink, volume)

def change_volume_down(qtile):
    sink = get_active_sink()
    if sink:
        volume = sink.volume
        # Adjust volume for all channels
        for i in range(len(volume.values)):
            volume.values[i] -= 0.05
        pulse.volume_set(sink, volume)

def toggle_mute(qtile):
    sink = get_active_sink()
    if sink:
        pulse.mute(sink, not sink.mute)

# Example usage
# change_volume(0.05)  # Increase volume by 5%
# change_volume(-0.05) # Decrease volume by 5%
# toggle_mute()        # Toggle mute
