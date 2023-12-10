#!/bin/sh

pidof dunst && killall dunst
dunst &

dunstify "hvad så der"
