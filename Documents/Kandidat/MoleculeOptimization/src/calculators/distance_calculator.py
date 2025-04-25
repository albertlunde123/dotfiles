import itertools
import numpy as np

# Assuming 'src' is in the Python path or project root is used for execution
from src.molecule import Cluster, Atom # Also import Atom if needed here
from .base_calculator import EnergyCalculator


class DistanceBasedCalculator(EnergyCalculator):
    """Energy calculator based on pairwise distances between atoms.

    Assumes the energy is a sum of pairwise contributions U(r_ij).
    Subclasses should override _energy_contribution and _force_magnitude.
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
        """Calculate the energy contribution U(r_ij) for a single pair.

        Args:
            distance: The distance r_ij between the two atoms.
            atom1: The first Atom object.
            atom2: The second Atom object.

        Returns:
            The energy contribution U(r_ij) for this pair (float).
        """
        # Placeholder/Example - User should modify or override
        vw_sum = atom1.vdw_radius + atom2.vdw_radius
        if distance < vw_sum:
            overlap = vw_sum - distance
            return 100.0 * overlap**2  # Repulsive penalty
        else:
            # Use distance >= 1e-9 to avoid division by zero if atoms overlap exactly
            safe_distance = max(distance, 1e-9)
            return -1.0 / (safe_distance**2)  # Attractive term

    def _force_magnitude(self, distance: float, atom1: Atom, atom2: Atom) -> float:
        """Calculate the magnitude of the force between a pair, F = -dU/dr.

        Args:
            distance: The distance r_ij between the two atoms.
            atom1: The first Atom object.
            atom2: The second Atom object.

        Returns:
            The force magnitude -dU/dr (float).
            Positive means repulsive, negative means attractive.
        """
        # Placeholder/Example - User should modify or override based on _energy_contribution
        # This must be the negative derivative of the function in _energy_contribution
        vw_sum = atom1.vdw_radius + atom2.vdw_radius
        if distance < vw_sum:
            overlap = vw_sum - distance
            # dU/dr = d/dr [100 * (vw_sum - r)^2] = 100 * 2 * (vw_sum - r) * (-1) = -200 * overlap
            # Force = -dU/dr = 200 * overlap
            return 200.0 * overlap # Repulsive force
        else:
            # dU/dr = d/dr [-1 / r^2] = -(-2 * r^-3) = 2 / r^3
            # Force = -dU/dr = -2 / r^3
            safe_distance = max(distance, 1e-9)
            return -2.0 / (safe_distance**3) # Attractive force

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

    def calculate_forces(self, cluster: Cluster) -> np.ndarray:
        """Calculates the force on each atom based on pairwise distances."""
        # This implementation can be overridden by calculate() if preferred
        _, forces = self.calculate(cluster)
        return forces

    # Override the base calculate method for potentially better efficiency
    def calculate(self, cluster: Cluster) -> tuple[float, np.ndarray]:
        """Calculates both energy and forces efficiently by iterating pairs once."""
        atoms = cluster.atoms
        num_atoms = len(atoms)
        positions = np.array([atom.position for atom in atoms])
        forces = np.zeros_like(positions)
        total_energy = 0.0

        for i, j in itertools.combinations(range(num_atoms), 2):
            atom1 = atoms[i]
            atom2 = atoms[j]

            # Vector from atom j to atom i
            rij_vec = positions[i] - positions[j]
            distance = np.linalg.norm(rij_vec)

            # Avoid division by zero if atoms are exactly coincident
            if distance < 1e-9:
                continue

            # Apply cutoff
            if self.cutoff is None or distance <= self.cutoff:
                # Calculate energy contribution
                energy_contrib = self._energy_contribution(distance, atom1, atom2)
                total_energy += energy_contrib

                # Calculate force magnitude (-dU/dr)
                force_mag = self._force_magnitude(distance, atom1, atom2)

                # Calculate force vector F_ij = (-dU/dr) * (rij_vec / distance)
                force_vec = force_mag * (rij_vec / distance)

                # Add force contribution to both atoms (Newton's 3rd law)
                forces[i] += force_vec
                forces[j] -= force_vec

        return total_energy, forces

    def __repr__(self):
        params_str = f"parameters={self.parameters}" if self.parameters else ""
        return f"{self.__class__.__name__}({params_str})" 