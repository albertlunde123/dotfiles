from sympy import *

# Define the matrix

b = Symbol('b')

A = Matrix([[0, -1, -1], [-1, 0, -1], [-1, -1, 0]])
eigenvalues = A.eigenvals()

print(eigenvalues)
