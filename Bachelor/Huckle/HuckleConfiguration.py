from PIL import Image
import numpy as np
from sympy import Matrix, pretty_print
import random as rnd
import matplotlib.pyplot as plt
import networkx as nx

class HuckleConfiguration:
    def __init__(self, image = None, rgb = (255, 209, 35), size = 10, coords = None, matrix = None):
        self.image = image
        self.size = size
        self.rgb = rgb
        self.coords = coords
        self.adjacency_matrix = matrix
        self.diagram = None
        self.radius = None
        self.fig = None
        self.ax = None

        if self.image != None:
            self.coords = self.find_centers()
            self.adjacency_matrix = self.find_matrix()

        self.ax = None

        # Find the centers of the circles -------------------------------

    def find_centers(self):

        # Find the centers of the circles
        def find_center(self):

            size_x, size_y = self.image.width-1, self.image.height-1

            random_x = rnd.randint(0, size_x)  # Adjusted to be within image bounds
            random_y = rnd.randint(0, size_y)  # Adjusted to be within image bounds

            # Check if the random point is inside the circle
            while True:
                if self.image.getpixel((random_x, random_y)) == self.rgb:
                    break
                else:
                    random_x = rnd.randint(0, size_x)
                    random_y = rnd.randint(0, size_y)

            x, y = random_x, random_y

            # Find x_max
            while self.image.getpixel((x, y)) == self.rgb and x < size_x:
                x += 1
            x_max = x

            x = random_x
            # Find x_min
            while self.image.getpixel((x, y)) == self.rgb and x > 0:
                x -= 1
            x_min = x

            x = random_x
            # Find y_max
            while self.image.getpixel((x, y)) == self.rgb and y < size_y:
                y += 1
            y_max = y

            y = random_y
            # Find y_min
            while self.image.getpixel((x, y)) == self.rgb and y > 0:
                y -= 1
            y_min = y

            center = ((x_max + x_min) // 2, (y_max + y_min) // 2)
            self.radius = ((x_max - x_min) // 2 + (y_max - y_min) // 2) // 2

            return center
        
        centers = []

        while len(centers) < self.size:
            center = find_center(self)
            keep = True
            for c in centers:
                if (center[0] - c[0])**2 + (center[1] - c[1])**2 < self.radius**2:
                    keep = False
            if keep:
                centers.append(center)

        centers = sorted(centers, key=lambda x: x[0])

        return centers

    # -------------------------------
    # Find the matrix of the configuration

    def find_matrix(self):

        matrix = np.zeros((self.size, self.size))
        centers = self.coords

        for i in centers:
            for j in centers:
                if i == j:
                    continue
                else:
                    dist = (i[0] - j[0])**2 + (i[1] - j[1])**2
                    matrix[centers.index(i)][centers.index(j)] = dist
        
        def cutoff(matrix):

            sorted_matrix = np.sort(matrix.flatten(), axis=None)
            sorted_matrix = sorted_matrix[sorted_matrix != 0]
            # print(sorted_matrix)

            init = sorted_matrix[0]
            
            i = 1
            while np.abs(sorted_matrix[i] - init) < init / 2:
                # print(sorted_matrix[i])
                i += 1

            cuttoff = sorted_matrix[i-1]
            # prin
            
            return cuttoff

        minimum = cutoff(matrix)

        for i in range(self.size):
            for j in range(self.size):
                    if matrix[i][j] > minimum or matrix[i][j] == 0:
                        matrix[i][j] = 0
                    elif matrix[i][j] <= minimum:
                        matrix[i][j] = 1
                    else:
                        matrix[i][j] = 0

        return matrix

    def Laplacian(self):

        matrix = self.adjacency_matrix
        rows, cols = matrix.shape
        L = np.zeros((rows, cols))

        for i in range(rows):
            for j in range(cols):
                if i == j:
                    L[i][j] = np.sum(matrix[i]) - matrix[i][j]
                else:
                    L[i][j] = -matrix[i][j]

        return L

    def n_bonds(self):

        matrix = self.adjacency_matrix
        rows, cols = matrix.shape
        bonds = 0

        for i in range(rows):
            for j in range(cols):
                if matrix[i][j] != 0:
                    bonds += 1

        return bonds / 2

    def Diagram(self, directed = False):

        matrix = self.adjacency_matrix
        rows, cols = matrix.shape
 # Create a directed or undirected graph
        G = nx.DiGraph() if directed else nx.Graph()

        # Add nodes
        G.add_nodes_from(range(rows))

        # Add edges based on adjacency matrix
        for i in range(rows):
            for j in range(cols):
                if matrix[i][j] != 0:
                    G.add_edge(i, j, weight=matrix[i][j])

        # Draw the graph
        pos = nx.spring_layout(G)  # positions for all nodes
        nx.draw(G, pos, with_labels=True)
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

        plt.show()

        return self.diagram

    def eigenvalues(self):

        matrix = Matrix(self.adjacency_matrix)
        eigenvalues = matrix.eigenvals()
        ei_list = []

        for key in eigenvalues:
            degen = eigenvalues[key]

            for i in range(degen):
                ei_list.append(key)
        
        ei_list = np.array(ei_list)

        return np.sort(ei_list)

    def eigenvectors(self):
        return Matrix(self.adjacency_matrix).eigenvects()


    def Energy(self):

        energy = 0
        eigenvalues = self.eigenvalues()

        for i in range(self.size):
            if i < 3:
                energy += eigenvalues[0]
            else:
                energy += eigenvalues[1]

        return energy

    def getOrbitals(self):

        orbitals = []
        for e in self.eigenvectors():
            orbitals.append([(self.coords[i], e[2][0][i]) for i in range(len(self.coords))])
        
        return orbitals

        # This function matches coordinates with an eigenvector.


def draw_atoms_and_bonds(conf, ax, circle_size = 27.2):

    coords = conf.coords

    for i in range(conf.size):
        for j in np.arange(i, conf.size):
            if conf.adjacency_matrix[i][j] == 1:
                ax.plot([conf.coords[i][0], conf.coords[j][0]], [conf.coords[i][1], conf.coords[j][1]], c = "black", zorder = 1)

    i = 0

    for coord in coords:
        # print(coord)
        circle = plt.Circle((coord[0], coord[1]), circle_size, edgecolor = "black", facecolor = "gold", linewidth = 1.0, zorder = 2)
        ax.add_artist(circle)

        i += 1


def set_axis(conf, ax, width = 2):

    coords = conf.coords

    x_min = min(coords, key = lambda x: x[0])
    x_max = max(coords, key = lambda x: x[0])
    y_min = min(coords, key = lambda x: x[1])
    y_max = max(coords, key = lambda x: x[1])

    ax.set_xlim(x_min[0] - width, x_max[0] + width)
    ax.set_ylim(y_min[1] - width, y_max[1] + width)

    ax.set_aspect("equal")
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.tick_params(axis='x', colors="white")
    ax.tick_params(axis='y', colors="white")
    ax.yaxis.label.set_color("white")
    ax.xaxis.label.set_color("white")
    
    return

def ConfFigure(conf):

    # conf = HuckleConfiguration(image = Image.open(path))
    
    coords = conf.coords


    fig, ax = plt.subplots(1, 2)
    ax = ax.ravel()

    conf.ax = ax

    ax[0].set_aspect("equal")
    ax[0].spines['top'].set_visible(False)
    ax[0].spines['right'].set_visible(False)
    ax[0].spines['bottom'].set_visible(False)
    ax[0].spines['left'].set_visible(False)
    ax[0].tick_params(axis='x', colors="white")
    ax[0].tick_params(axis='y', colors="white")
    ax[0].yaxis.label.set_color("white")
    ax[0].xaxis.label.set_color("white")

    set_axis(conf, ax[0], width = 28)

    # Draw the atoms.



    draw_atoms_and_bonds(conf, ax[0])


    # plot the eigenvalues on the right.

    for e in conf.eigenvalues():
        ax[1].axhline(y = e, color = "purple", linewidth = 2.0)

    ax[1].set_xlim(0, 1)
    ax[1].spines['top'].set_visible(False)
    ax[1].spines['right'].set_visible(False)
    ax[1].spines['bottom'].set_visible(False)
    ax[1].tick_params(axis='x', colors="white")
    ax[1].tick_params(axis='y', colors="black", labelsize = 12)
    ax[1].xaxis.label.set_color("white")

    ax[1].set_title("Energy Levels", color = "black")


    return fig, ax

    # Draw the bonds.


def plotOrbital(orbital, ax):

    rad_scale = max([np.abs(radius) for center, radius in orbital])

    for c in orbital:

        print(c)

        center = (c[0][0], c[0][1])
        radius = c[1] / rad_scale

        print("center :", center)
        print("radius :", radius)
        
        if radius < 0:
            color = "blue"
        else:
            color = "red"

        circle = plt.Circle(center, radius * 27.2, edgecolor = color, facecolor = color, linewidth = 0, zorder = 3)
        ax.add_artist(circle)

    return ax



# for i in range(1, 5):
#     conf = HuckleConfiguration(image = Image.open(f"conf{i}.png"))
#     eigval = conf.eigenvalues()

#     energy = sum(eigval[:4])*2
#     print(i, energy)

# conf = HuckleConfiguration(image = Image.open("conf1.png"))
# # ConfFigure(conf)

# orbitals = conf.getOrbitals()
# plotOrbital(orbitals[1], conf.ax[0]) 

# plt.show()


# make complete orbitals plot, with list of all orbitals and eigenvalues,

def AllOrbitalPlot(conf):

    fig, ax = plt.subplots(4, 3)
    ax = ax.ravel()

    orbitals = conf.getOrbitals()

    eigval = conf.eigenvalues()

    for i in range(len(ax)):

        set_axis(conf, ax[i], 28)

        if i <= 9:

            ax[i].set_title(f"$\lambda = {np.round(float(eigval[i]), 1)}$")
            draw_atoms_and_bonds(conf, ax[i])
            plotOrbital(orbitals[i], ax[i])

    return fig, ax



colors = ["#24283b", "#9ece6a", "#c0caf5", "#d62728", "#9467bd", "#8c564b",]

from matplotlib.collections import PathCollection
from matplotlib.text import Text

def tokyonight_theme(ax, fig):
    # Define TokyoNight color scheme
    tokyonight_colors = ["#24283b", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]

    # Update plot lines
    for line in ax.get_lines():
        line.set_color(tokyonight_colors[1])

    # Update markers and scatter plots
    for path_collection in ax.collections:
        if isinstance(path_collection, PathCollection):
            path_collection.set_edgecolor(tokyonight_colors[2])
            path_collection.set_facecolor(tokyonight_colors[3])

    # Update spines
    for spine in ax.spines.values():
        spine.set_edgecolor(tokyonight_colors[4])

    # Update tick labels
    for text in ax.get_xticklabels() + ax.get_yticklabels():
        text.set_color(tokyonight_colors[5])

    # Update axis labels and title
    ax.xaxis.label.set_color(tokyonight_colors[6])
    ax.yaxis.label.set_color(tokyonight_colors[7])
    ax.title.set_color(tokyonight_colors[8])

    # Update other text elements
    for text in ax.findobj(match=Text):
        text.set_color(tokyonight_colors[9])

    # Update background colors
    ax.set_facecolor(tokyonight_colors[0])
    fig.patch.set_facecolor(tokyonight_colors[0])

    # Update additional artist elements like circles, polygons, etc.
    for artist in ax.artists:
        artist.set_edgecolor(tokyonight_colors[1])
        artist.set_facecolor(tokyonight_colors[2])

    # Update legend, if present
    legend = ax.get_legend()
    if legend:
        for text in legend.get_texts():
            text.set_color(tokyonight_colors[5])
        legend.get_frame().set_facecolor(tokyonight_colors[0])

    # Update grid, if present
    ax.grid(color=tokyonight_colors[7])

    return ax, fig

# # Example usage
# fig, ax = AllOrbitalPlot(conf)
# # for a in ax:
# #     tokyonight_theme(a, fig)

# plt.show()


# Quick check to see whether they match up.

def test(conf):

    eigenvals = conf.eigenvalues()
    eigenvec = conf.eigenvectors()
    matrix = conf.matrix



    for i in range(len(eigenvec)):
        print(i)
        pretty_print(matrix*eigenvec[2][0])

    return

