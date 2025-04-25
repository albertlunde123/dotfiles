import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

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

def plot_cluster(cluster: Cluster, show_labels: bool = False, ax: Axes3D | None = None):
    """Plots the atoms of a cluster in a 3D scatter plot.

    Args:
        cluster: The Cluster object to plot.
        show_labels: Whether to display atom symbols as labels.
        ax: An optional existing Matplotlib 3D axes object to plot on.
    """
    if not isinstance(cluster, Cluster):
        raise TypeError("Input must be a Cluster object.")

    created_ax = False
    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        created_ax = True

    xs = [atom.position[0] for atom in cluster.atoms]
    ys = [atom.position[1] for atom in cluster.atoms]
    zs = [atom.position[2] for atom in cluster.atoms]
    symbols = [atom.symbol for atom in cluster.atoms]

    # Basic scatter plot - might need more sophisticated coloring/sizing later
    ax.scatter(xs, ys, zs, marker='o')

    if show_labels:
        for x, y, z, label in zip(xs, ys, zs, symbols):
            ax.text(x, y, z, f'{label}', size=10, zorder=1, color='k')

    ax.set_xlabel("X Coordinate")
    ax.set_ylabel("Y Coordinate")
    ax.set_zlabel("Z Coordinate")
    ax.set_title(f"Cluster Visualization ({len(cluster.atoms)} atoms)")

    # Only show the plot if we created the axes within this function
    if created_ax:
        plt.show() 