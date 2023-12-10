# This program takes a screenshot and sends it to a target folder

import subprocess
import os


print('------ Screenshot app ------\n')
name = input('filename : ') + '.png'
subprocess.run(['gnome-screenshot', '-a'])

Pictures = os.path.expanduser("~/Pictures")

screenshot = Pictures + '/'
path_to_pict = os.listdir(Pictures)
for p in path_to_pict:
    if 'Screenshot' in p:
        screenshot += p

select = os.path.expanduser("~/Scripts/selectfile.zsh")
dest_path = subprocess.check_output(select, shell = True)
dest_path = dest_path.decode()

# Nu skal jeg bygge filnavnet.
# Jeg skal skærer den sidste /foo fra.

fil = ""
for t in dest_path.split('/')[:-1]:
    fil += t + '/'
fil += name

subprocess.run(['mv', screenshot, fil])
