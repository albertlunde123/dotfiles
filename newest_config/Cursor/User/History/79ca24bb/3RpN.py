import itertools
import numpy as np

# Potential type hinting issue if src is not in PYTHONPATH
try:
    from src.molecule import Cluster
    from .base_calculator import EnergyCalculator
except ImportError:
    # Allow for potential direct testing or different project structures
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    try:
        from molecule import Cluster
        from calculators.base_calculator import EnergyCalculator
    except ImportError:
        # Define dummies if not found (e.g., during linting)
        class Cluster:
            pass
        class EnergyCalculator:
            def __init__(self, parameters=None): pass
            def calculate_energy(self, cluster): raise NotImplementedError

class DistanceBasedCalculator(EnergyCalculator):
    """Energy calculator based on pairwise distances between atoms.

    Subclasses should override _energy_contribution_from_distance.
    """

    def __init__(self, parameters: dict | None = None):
        """Initializes the distance-based calculator."""
        super().__init__(parameters)
        # Add any specific parameter handling for distance-based methods here
        # e.g., cutoff radius
        self.cutoff = self.parameters.get('cutoff', None)
        if self.cutoff is not None:
            self.cutoff = float(self.cutoff)

    def _energy_contribution(self, distance: float, atom1_symbol: str, atom2_symbol: str) -> float:
        """Calculate the energy contribution for a single pair of atoms.

        This method should be implemented by the user in a subclass or
        by modifying this class directly to define the specific potential.

        Args:
            distance: The distance between the two atoms.
            atom1_symbol: Symbol of the first atom.
            atom2_symbol: Symbol of the second atom.

        Returns:
            The energy contribution for this pair (float).
        """
        # Placeholder: User should implement the actual energy calculation here.
        # Example: return some_function(distance, self.parameters.get(atom1_symbol), self.parameters.get(atom2_symbol))
        # For now, it returns 0.0.
        return 0.0

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
                energy_contrib = self._energy_contribution(distance, atom1.symbol, atom2.symbol)
                total_energy += energy_contrib

        return total_energy

    def __repr__(self):
        params_str = f"parameters={self.parameters}" if self.parameters else ""
        return f"{self.__class__.__name__}({params_str})" 