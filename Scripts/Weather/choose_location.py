import os

path = os.environ["HOME"] + "/Scripts/Weather/locations.txt"

def move_loc_to_top(i):
    
    with open(path, "r") as file:
        lines = file.readlines()
        new_top = lines[i]
        lines = [new_top] + lines[:i] + lines[i+1:]
        file.close()
    
    with open(path, "w") as file:
        file.writelines(lines)
        file.close()

move_loc_to_top(3)
