import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from typing import Literal, Union

# Potential type hinting issue if src is not in PYTHONPATH when running static analysis
# We might need to adjust imports or project structure if this becomes problematic.
try:
    from src.molecule import Cluster, Atom
except ImportError:
    # Allow running script directly for testing, assuming molecule is in parent dir
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from molecule import Cluster, Atom

def plot_cluster(cluster: Cluster, dim: Literal[2, 3] = 3, show_labels: bool = False, ax: Union[plt.Axes, Axes3D, None] = None):
    """Plots the atoms of a cluster in a 2D or 3D scatter plot.

    Args:
        cluster: The Cluster object to plot.
        dim: The number of dimensions to plot (2 or 3). Defaults to 3.
        show_labels: Whether to display atom symbols as labels.
        ax: An optional existing Matplotlib axes object (2D or 3D) to plot on.
    """
    if not isinstance(cluster, Cluster):
        raise TypeError("Input must be a Cluster object.")
    if dim not in [2, 3]:
        raise ValueError("Dimension must be 2 or 3.")

    created_ax = False
    if ax is None:
        fig = plt.figure()
        if dim == 3:
            ax = fig.add_subplot(111, projection='3d')
        else: # dim == 2
            ax = fig.add_subplot(111)
        created_ax = True
    else:
        # Basic check if provided axis dimension matches requested plot dimension
        is_3d_ax = hasattr(ax, 'get_zlim')
        if dim == 3 and not is_3d_ax:
            raise ValueError("Provided 'ax' is 2D, but 3D plot requested.")
        if dim == 2 and is_3d_ax:
            raise ValueError("Provided 'ax' is 3D, but 2D plot requested.")


    xs = [atom.position[0] for atom in cluster.atoms]
    ys = [atom.position[1] for atom in cluster.atoms]
    symbols = [atom.symbol for atom in cluster.atoms]

    if dim == 3:
        zs = [atom.position[2] for atom in cluster.atoms]
        ax.scatter(xs, ys, zs, marker='o')
        if show_labels:
            for x, y, z, label in zip(xs, ys, zs, symbols):
                ax.text(x, y, z, f'{label}', size=10, zorder=1, color='k')
        ax.set_xlabel("X Coordinate")
        ax.set_ylabel("Y Coordinate")
        ax.set_zlabel("Z Coordinate")
        ax.set_title(f"3D Cluster Visualization ({len(cluster.atoms)} atoms)")
    else: # dim == 2
        ax.scatter(xs, ys, marker='o')
        if show_labels:
            for x, y, label in zip(xs, ys, symbols):
                ax.text(x, y, f'{label}', size=10, zorder=1, color='k')
        ax.set_xlabel("X Coordinate")
        ax.set_ylabel("Y Coordinate")
        ax.set_title(f"2D Cluster Visualization (XY Plane) ({len(cluster.atoms)} atoms)")
        ax.set_aspect('equal', adjustable='box') # Often useful for 2D molecular plots

    # Only show the plot if we created the axes within this function
    if created_ax:
        plt.show() 