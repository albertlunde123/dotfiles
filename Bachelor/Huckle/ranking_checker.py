import HuckleConfiguration as hc
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


energies = {"conf1": -21.555,
            "conf2": -21.407,
            "conf3": -21.356,
            "conf4": -21.016,
            "conf5": -21.854,
            "conf6": -22.184}


# for i in range(1, 6):
#     conf = hc.HuckleConfiguration(image = Image.open(f"conf{i}.png"))
#     # conf.adjacency_matrix = conf.Laplacian()

#     n_bonds = conf.n_bonds()
#     print(f"conf{i}", n_bonds, conf.n_bonds())

#     # print(conf.adjacency_matrix)

#     eigval = conf.eigenvalues()
#     energy = sum(eigval[:4])*2 

    # conf.adjacency_matrix = conf.Laplacian()
    # eigval2 = conf.eigenvalues()
    # energy2 = sum(eigval2[:4])*2

    # print(f"conf{i}", energy, energy2, energies[f"conf{i}"])


fig, ax = plt.subplots(3, 2)
ax = ax.ravel()

for i,j in enumerate([1, 2, 3, 4, 5, 6]):
    conf = hc.HuckleConfiguration(image = Image.open(f"conf{j}.png"))
    hc.draw_atoms_and_bonds(conf, ax[i], circle_size = 20)
    hc.set_axis(conf, ax[i], width = 25)

    eigval = conf.eigenvalues()
    energy = np.round(float(sum(eigval[:4])*2), 3)
    n_bonds = conf.n_bonds()


    title = 'DFT energy = ' + str(energies[f"conf{j}"]) + '\n'
    title += 'Huckle energy = ' + str(energy) + '\n'
    title += 'Number of bonds = ' + str(n_bonds) + '\n'
    # title += 'DFT energy = ' + str(energies[f"conf{j}"])

    # title = f"conf{j} - {energy:.3f} eV,\n {n_bonds} bonds"

    ax[i].set_title(title)

    # ax[i].set_title(f"conf{j} - {energy:.3f} eV,\n {n_bonds} bonds")


plt.tight_layout()
plt.savefig("ranking.png", dpi = 300)
# plt.show()


