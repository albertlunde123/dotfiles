#!/bin/sh

# display setup

INTERNAL_DISPLAY="eDP1"
EXTERNAL_DISPLAY="HDMI2"

if xrandr | grep -q -w "$EXTERNAL_DISPLAY connected"; then
    xrandr --output $INTERNAL_DISPLAY --off --output $EXTERNAL_DISPLAY --auto --scale 1.4x1.4 --dpi 144
else
    xrandr --output $INTERNAL_DISPLAY --auto --dpi 96
fi

# feh --bg-fill ~/.config/qtile/Scripts/background.png
wal --theme tokyonight

dunst &
