from src.molecule import Atom, Cluster
from src.calculators import DistanceBasedCalculator

def main():
    # Create two atoms
    atom1 = Atom(symbol='H', position=(0.0, 0.0, 0.0))
    atom2 = Atom(symbol='H', position=(1.0, 0.0, 0.0))

    # Create a cluster with the two atoms
    cluster = Cluster(atoms=[atom1, atom2])

    # Create a distance-based calculator
    calculator = DistanceBasedCalculator()

    # Calculate the energy of the cluster
    energy = calculator.calculate_energy(cluster)

    # Print the energy
    print(f"Energy of the cluster: {energy}")

if __name__ == "__main__":
    main()