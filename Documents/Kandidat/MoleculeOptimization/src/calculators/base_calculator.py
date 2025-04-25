from abc import ABC, abstractmethod
import numpy as np

# Assuming 'src' is in the Python path or project root is used for execution
from src.molecule import Cluster

class EnergyCalculator(ABC):
    """Abstract base class for all energy calculators.

    Subclasses must implement calculate_energy and calculate_forces.
    They can optionally override calculate for efficiency.
    """

    def __init__(self, parameters: dict | None = None):
        """Initializes the calculator, optionally with parameters."""
        self.parameters = parameters if parameters is not None else {}
        # Potentially load/validate parameters here

    @abstractmethod
    def calculate_energy(self, cluster: Cluster) -> float:
        """Calculates the potential energy of a given cluster.

        Args:
            cluster: The Cluster object for which to calculate the energy.

        Returns:
            The calculated potential energy as a float.
        """
        pass

    @abstractmethod
    def calculate_forces(self, cluster: Cluster) -> np.ndarray:
        """Calculates the force on each atom in the cluster.

        Args:
            cluster: The Cluster object.

        Returns:
            A numpy array of shape (num_atoms, 3) containing the Cartesian
            forces (Fx, Fy, Fz) on each atom.
        """
        pass

    def calculate(self, cluster: Cluster) -> tuple[float, np.ndarray]:
        """Calculates both the energy and forces for the cluster.

        Subclasses can override this method if calculating energy and forces
        together is more efficient than calling calculate_energy and
        calculate_forces separately.

        Args:
            cluster: The Cluster object.

        Returns:
            A tuple containing:
                - energy (float)
                - forces (np.ndarray): Shape (num_atoms, 3)
        """
        # Default implementation calls the separate methods
        energy = self.calculate_energy(cluster)
        forces = self.calculate_forces(cluster)
        return energy, forces

    def __repr__(self):
        return f"{self.__class__.__name__}(parameters={self.parameters})" 