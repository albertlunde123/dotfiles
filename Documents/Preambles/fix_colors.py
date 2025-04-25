# I get io.UnsupportedOperation: not readable
import os

path = os.environ['HOME'] + "/Documents/Latex/Preambles/colors.tex"

with open(path, 'r') as f:
    colors = f.readlines()
    f.close()

with open(path, 'w') as f:
    for i in range(len(colors)):
        if i == 0 or i == 1:
            f.write(colors[i])
            continue
        c = "".join(colors[i].split("#"))
        f.write(c)

        
