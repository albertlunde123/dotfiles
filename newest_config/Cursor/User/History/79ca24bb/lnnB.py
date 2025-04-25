import itertools
import numpy as np

# Assuming 'src' is in the Python path or project root is used for execution
from src.molecule import Cluster, Atom # Also import Atom if needed here
from .base_calculator import EnergyCalculator


class DistanceBasedCalculator(EnergyCalculator):
    """Energy calculator based on pairwise distances between atoms.

    Subclasses should override _energy_contribution.
    """

    def __init__(self, parameters: dict | None = None):
        """Initializes the distance-based calculator."""
        super().__init__(parameters)
        # Add any specific parameter handling for distance-based methods here
        # e.g., cutoff radius
        self.cutoff = self.parameters.get('cutoff', None)
        if self.cutoff is not None:
            self.cutoff = float(self.cutoff)

    # Note: The signature was updated to accept Atom objects directly
    #       as the previous code snippet had inconsistencies.
    def _energy_contribution(self, distance: float, atom1: Atom, atom2: Atom) -> float:
        """Calculate the energy contribution for a single pair of atoms.

        This method should be implemented by the user in a subclass or
        by modifying this class directly to define the specific potential.

        Args:
            distance: The distance between the two atoms.
            atom1: The first Atom object.
            atom2: The second Atom object.

        Returns:
            The energy contribution for this pair (float).
        """

        # Placeholder: User should implement the actual energy calculation here.
        # Example using VdW radii from atom objects:
        vw1 = atom1.vdw_radius
        vw2 = atom2.vdw_radius

        # If the distance is less than the sum of the VdW radii, the atoms repel each other
        # This is a simplified example potential
        if distance < vw1 + vw2:
            # Penalize overlap strongly (example)
            overlap = (vw1 + vw2) - distance
            return 100 * overlap**2 # Example penalty

        # If the distance is greater than the sum of the VdW radii, maybe attract?
        else:
            # Example weak attraction: 1/distance^2
            # Adjust the functional form and parameters as needed!
            return -1.0 / (distance**2) # Example attraction (made negative)

        # return 0.0 # Original placeholder

    def calculate_energy(self, cluster: Cluster) -> float:
        """Calculates the total energy based on pairwise distances.

        Iterates through all unique pairs of atoms, calculates their distance,
        and sums the contributions determined by _energy_contribution.
        Applies a cutoff radius if specified in parameters.

        Args:
            cluster: The Cluster object.

        Returns:
            The total calculated energy.
        """
        total_energy = 0.0
        atoms = cluster.atoms
        num_atoms = len(atoms)

        # Use itertools.combinations for efficient pair iteration
        for i, j in itertools.combinations(range(num_atoms), 2):
            atom1 = atoms[i]
            atom2 = atoms[j]

            distance = atom1.distance_to(atom2)

            # Apply cutoff if specified
            if self.cutoff is None or distance <= self.cutoff:
                # Pass the actual Atom objects
                energy_contrib = self._energy_contribution(distance, atom1, atom2)
                total_energy += energy_contrib

        return total_energy

    def __repr__(self):
        params_str = f"parameters={self.parameters}" if self.parameters else ""
        return f"{self.__class__.__name__}({params_str})" 