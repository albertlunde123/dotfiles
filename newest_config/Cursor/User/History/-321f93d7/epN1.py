#!/usr/bin/env python
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.molecule import Atom, Cluster
from src.visualization import plot_cluster

def main():
    """Creates a sample cluster and plots it."""
    # Create some sample atoms
    atom1 = Atom(symbol='C', position=(0.0, 0.0, 0.0), id=1)
    atom2 = Atom(symbol='H', position=(1.0, 0.0, 0.0), id=2)
    atom3 = Atom(symbol='H', position=(0.0, 1.0, 0.0), id=3)
 

    # Create a cluster
    sample_cluster = Cluster(atoms=[atom1, atom2, atom3, atom4])

    print(f"Plotting cluster: {sample_cluster}")

    # Plot the cluster with labels in 3D (default)
    print("\nDisplaying 3D plot...")
    plot_cluster(sample_cluster, show_labels=True)

    # Plot the cluster with labels in 2D
    print("\nDisplaying 2D plot (XY projection)...")
    plot_cluster(sample_cluster, dim=2, show_labels=True)

    print("\nTwo plot windows should have opened. Close them to exit the script.")

if __name__ == "__main__":
    main() 