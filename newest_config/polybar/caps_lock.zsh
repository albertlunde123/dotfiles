#!/usr/bin/zsh

CAPS=$(xset -q | awk '/00:/{print $4}')
if [[ $CAPS = "on" ]]
then
     echo "%{F#0f0} CAPS%{F-}"
else
     echo ""
fi
