#!/usr/bin/env zsh

# Set the colors for rofi using pywal
# wal -i "$HOME"
# source "$HOME"/.cache/wal/colors.sh

# Set the options for rofi
rofi_command="rofi -theme '$HOME/.cache/wal/colors-rofi-dark.rasi'"

# Set the prompt for the rofi menu
prompt="Todo:"

# Set the options for the rofi menu
# options="$(cat "$HOME/todo.txt")$'\n'Add a new item"
option="$(cat "$HOME/todo.txt")"

# Show the rofi menu
chosen=$(echo -e "$option" | $rofi_command -dmenu -p "$prompt" -format i -selected-row 0)

# Get the number of the selected item
selected=$(echo "$chosen" | awk '{print $1}')

# If an item was selected, delete it from the todo list
if [ -n "$selected" ]; then
    sed -i "${selected}d" "$HOME/todo.txt"
fi

# If the selected item is "Add a new item," prompt the user for the new item and add it to the todo list
if [ "$selected" = "Add a new item" ]; then
    new_item=$(rofi -dmenu -p "Enter a new todo item:")
    echo "$new_item" >> "$HOME/todo.txt"
fi

