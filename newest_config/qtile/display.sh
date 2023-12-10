#!/bin/bash

INTERNAL_DISPLAY="eDP1"
EXTERNAL_DISPLAY="DP1"

if xrandr | grep "$EXTERNAL_DISPLAY connected"; then
    xrandr --output $INTERNAL_DISPLAY --off --output $EXTERNAL_DISPLAY --auto --scale 1.4x1.4 --dpi 144
# else
#     xrandr --output $INTERNAL_DISPLAY --auto --dpi 96
# fi

