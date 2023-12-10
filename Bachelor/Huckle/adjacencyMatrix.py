from PIL import Image
import random as rnd
import subprocess
import numpy as np
import sympy as sp

def drawCircle(image):
    width, height = image.size
    for x in range(width):
        for y in range(height):
            if (x - width/2)**2 + (y - height/2)**2 <= (width/2)**2:
                image.putpixel((x, y), (0, 0, 0))
    return image

def drawDot(image, x, y, thickness=1):
    width, height = image.size
    for i in range(x-thickness, x+thickness+1):
        for j in range(y-thickness, y+thickness+1):
            if i >= 0 and i < width and j >= 0 and j < height:
                image.putpixel((i, j), (0, 0, 0))
    return image

def find_center(image, size_x=299, size_y=299, rgb=(0, 0, 0)):
    random_x = rnd.randint(0, size_x)  # Adjusted to be within image bounds
    random_y = rnd.randint(0, size_y)  # Adjusted to be within image bounds

    # Check if the random point is inside the circle
    while True:
        if image.getpixel((random_x, random_y)) == rgb:
            break
        else:
            random_x = rnd.randint(0, size_x)
            random_y = rnd.randint(0, size_y)

    x, y = random_x, random_y

    # Find x_max
    while image.getpixel((x, y)) == rgb and x < size_x:
        x += 1
    x_max = x

    x = random_x
    # Find x_min
    while image.getpixel((x, y)) == rgb and x > 0:
        x -= 1
    x_min = x

    x = random_x
    # Find y_max
    while image.getpixel((x, y)) == rgb and y < size_y:
        y += 1
    y_max = y

    y = random_y
    # Find y_min
    while image.getpixel((x, y)) == rgb and y > 0:
        y -= 1
    y_min = y

    center = ((x_max + x_min) // 2, (y_max + y_min) // 2)
    return center

def find_centers(image, size_x, size_y, n, rgb=(0, 0, 0)):
    centers = []
    while len(centers) < n:
        center = find_center(image, size_x, size_y, rgb=rgb)
        keep = True
        for c in centers:
            if (center[0] - c[0])**2 + (center[1] - c[1])**2 < 100:
                keep = False
        if keep:
            centers.append(center)
    for center in centers:        
        image = drawDot(image, center[0], center[1], thickness=5)

    return image, centers
    # return centers

def concatenate_images_side_by_side(image1, image2):
    # Determine the size of the new image
    new_width = image1.width + image2.width
    new_height = max(image1.height, image2.height)

    # Create a new image with the appropriate height and width
    new_image = Image.new('RGB', (new_width, new_height))

    # Paste the first image on the left
    new_image.paste(image1, (0, 0))

    # Paste the second image on the right
    new_image.paste(image2, (image1.width, 0))

    return new_image, new_width-1, new_height-1

def create_adjacency_matrix(centers):

    N = len(centers)

    def distance(center1, center2):
        return ((center1[0] - center2[0])**2 + (center1[1] - center2[1])**2)**0.5

    bond_length = min([distance(centers[i], centers[i+1]) for i in range(N-1)])
    print("bond length: ", bond_length)
    adjMatrix = sp.zeros(N, N)

    for i in range(N):
        for j in range(N):
            print(distance(centers[i], centers[j]))
            if i == j:
                adjMatrix[i, j] = 1
            elif np.abs(distance(centers[i], centers[j]) - bond_length) < 5:
                adjMatrix[i, j] = 1
            else:
                adjMatrix[i, j] = 0

    return adjMatrix



    

image = Image.open('atoms.jpg')
image.save('circle.png')


image1 = Image.new('RGB', (300, 300), (255, 255, 255))
image1 = drawCircle(image1)

image2 = Image.new('RGB', (300, 300), (255, 255, 255))

image3, width, height = concatenate_images_side_by_side(image1, image2)
image3, width, height = concatenate_images_side_by_side(image3, image1)

print(width, height)

# image3.save('circle.png')

image, centerss = find_centers(image, image.width-1, image.height-1, 10, rgb=(255, 209, 35))


centers = []
# sort by y coordinate and then x coordinate
for center in centerss:
    centers.append(center)

centers.sort(key=lambda x: -x[1])

# now sort by x coordinate
for i in range(0, len(centers), 2):
    centers[i:i+2] = sorted(centers[i:i+2], key=lambda x: x[0])

print(centers)


adjMatrix = create_adjacency_matrix(centers)
sp.pprint(adjMatrix)
# image.save('circle.png')
# subprocess.call(['feh', '--scale-down', 'circle.png'])



