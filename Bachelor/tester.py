from ase import Atoms

gold = Atoms('Au5', positions=[[0, 0, 0],
                              [1, 1, 0],
                              [2, 2, 0],
                              [3, 3, 0],
                              [4, 4, 0]])

gold.write('gold.xyz')
