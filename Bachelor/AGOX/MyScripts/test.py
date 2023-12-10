import os

path = os.getcwd() + "/aqui_relax/"
os.chdir(path)

print(os.listdir())

# get largest number

largest = 0
for file in os.listdir():
    if file.endswith(".db"):
        if int(file[2]) > largest:
            largest = int(file[2])

print(largest)
