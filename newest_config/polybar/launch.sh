killall -q polybar

# while pgrep -x polybar >/dev/null; do sleep 1; done

exec polybar main &
exec polybar middle &
exec polybar right &
exec polybar bottom-right &
exec polybar bottom-middle &
exec polybar bottom &
exec polybar note &

if type "xrandr"; then
  for m in $(xrandr --query | grep " connected" | cut -d" " -f1); do
    MONITOR=$m polybar --reload main &
    MONITOR=$m polybar --reload middle &
    MONITOR=$m polybar --reload right &
    MONITOR=$m polybar --reload bottom-right &
    MONITOR=$m polybar --reload bottom &
    MONITOR=$m polybar --reload note &
  done
else
  polybar --reload main &
  polybar --reload middle &
  polybar --reload right &
  polybar --reload bottom-right &
  polybar --reload bottom &
  polybar --reload note &
fi
