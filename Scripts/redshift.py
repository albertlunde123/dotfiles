import subprocess
import os

with open('Scripts/current_temperature.txt') as file:
    temp = int(file.readlines()[0])
    print(temp)
    if temp > 1000:
        temp = temp - 100
        print(temp)
    file.close()

with open('Scripts/current_temperature.txt', "w") as file:
    print(temp)
    file.write(str(temp))
    file.close()

subprocess.run(["redshift", "-P", "-O", str(temp)])

