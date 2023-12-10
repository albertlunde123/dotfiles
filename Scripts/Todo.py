#!/usr &/bin/env python

import os
import subprocess
import tkinter as tk
import fontawesome as fa

def add_todo():
    # create a temporary file to hold the user's input
    temp_file = "../../../tmp/todo_input.txt"
    # open the temporary file in vim
    kitty_conf = os.environ["HOME"] + "/.config/kitty/kitty_vim.conf"
    source = os.environ["HOME"] + "/.zshrc"
    vim_command = f"kitty --config {kitty_conf} --class 'todo_input' nvim {temp_file}"
    subprocess.run(vim_command.split())

    # read the contents of the temporary file
    with open(temp_file, "r") as f:
        new_todo = f.read()

    open(temp_file, "w")

    # add the new todo item to your list
    open(os.environ['HOME'] + "/todo.txt", "a").write(new_todo)


# Set the options for rofi

theme = os.environ["HOME"] + "/Scripts/todo.rasi"
prompt = fa.icons["book"]
# rofi_command = f"rofi -dmenu -p 'Todo:' -theme {os.environ['HOME']}/.cache/wal/colors-rofi-dark.rasi -format i -selected-row 0"
rofi_command = f"rofi -dmenu -p {prompt} -theme {theme} -format i -window-title todo_liste -selected-row 0"

Add = ". . . . . . Add new todo . . . . . ."
# Set the prompt for the rofi menu
options = "\n".join([" ".join(line.split()) for line in open(os.environ['HOME'] + "/todo.txt").readlines()]) + "\n" + Add
# Show the rofi menu
chosen = subprocess.run(rofi_command.split(),
                        input=options, capture_output=True, text=True)
# Set the options for the rofi menu

# Get the number of the selected item
sel_number = int(chosen.stdout.strip())

# Get the text of the selected item
selected = options.split("\n")[int(chosen.stdout.strip())]

# If an item was selected, delete it from the todo list
if selected and selected != Add:
    lines = open(os.environ['HOME'] + "/todo.txt").readlines()
    del lines[int(sel_number)]
    open(os.environ['HOME'] + "/todo.txt", "w").writelines(lines)


# If the selected item is "Add a new item," prompt the user for the new item and add it to the todo list
if selected == Add:
    add_todo()
