from ase import Atoms
from ase.visualize import view
import random
import os

# Number of gold atoms

import numpy as np
import itertools

x_min, x_max = 0, 10
y_min, y_max = 0, 10
spacing = 1  # Grid spacing

x_points = np.arange(x_min, x_max + spacing, spacing)
y_points = np.arange(y_min, y_max + spacing, spacing)
grid_points = list(itertools.product(x_points, y_points))

# Define a minimum distance between atoms
min_distance = 2.0

# Filter grid points based on minimum distance
filtered_grid_points = []
for point in grid_points:
    if all(np.linalg.norm(np.array(point) - np.array(existing_point)) >= min_distance for existing_point in filtered_grid_points):
        filtered_grid_points.append(point)
from ase import Atoms
import random
import os

# Create a directory to save the configurations
if not os.path.exists('sampled_configs'):
    os.makedirs('sampled_configs')

# Function to sample a configuration of 10 atoms
def sample_config(grid_points, n_atoms=10):
    return random.sample(grid_points, n_atoms)

# Sample 10 random configurations
sampled_configs = [sample_config(filtered_grid_points) for _ in range(10)]

# Create and save Atoms objects
for i, config in enumerate(sampled_configs):
    positions = np.array(config).reshape(-1, 2)
    positions = np.hstack([positions, np.zeros((positions.shape[0], 1))])  # Add zero z-coordinates
    atoms = Atoms('Au' * len(config), positions=positions)
    atoms.write(f'sampled_configs/config_{i+1}.xyz')

