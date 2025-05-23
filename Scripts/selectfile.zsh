#!/usr/bin/env bash

# selectfile
# Use rofi to select file or folder until file is selected, then print it.

# Arguments
#   $1=directory to start, defaults to "." (specified in variable default_dir)

# Source directory with systems folders.
default_dir="."
# Filter modes: normal, regex, glob, fuzzy, prefix
rofi_filter_mode="regex"
# Prompt in rofi, defaults to scriptname.
prompt="${0##*/}"

dir1="$HOME/.config/rofi/launchers/text"
themes=($(ls -p --hide="launcher.sh" --hide="styles" $dir))
theme1="${themes[$((1))]}"
# rofi command to run for each selection.
rofi="rofi -dmenu -p "$prompt" -lines 15 -matching $rofi_filter_mode -i -theme $dir1/"$theme1""

if [[ -z $1 ]]
then
    dir=`readlink -f "$default_dir"`
else
    dir=`readlink -f "$1"`
fi

# selected will be set to empty string, if user cancels in rofi.  This should
# start out with any value, as the until loop stops if its empty.  
# ! Attention: Be careful with modifying these things, otherwise you could end
# up in an infinite loop.
selected="x"
file=""
until [[ -f "$file" || "$selected" == "" ]]
do
    # List all folders in the directory and add ".." as top entry.
    filelist=`ls --color=never -1N "$dir"`
    selected=`echo -e "..\n$filelist" | $rofi -mesg "$dir"`
    
    if [[ "$selected" == "" ]]
    then
        file=""
    elif [[ "$selected" == ".." ]]
    then
        # ".." will be translated to go up one folder level and run rofi again.
        dir=${dir%/*}
    else
        file="$dir/$selected"
        dir="$file"
    fi
done

# Extract folder portion, if its a file.  This is needed, because the dir
# variable is overwritten previously.
# if [[ -f "$file" ]]
# then
#     dir=${dir%/*}
# fi
# echo "$dir"

# Finally print the fullpath of selected file.
if [[ ! "$file" == "" ]]
then
    echo "$file"
fi
