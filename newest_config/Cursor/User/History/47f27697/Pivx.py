from abc import ABC, abstractmethod

# Assuming 'src' is in the Python path or project root is used for execution
from src.molecule import Cluster

class EnergyCalculator(ABC):
    """Abstract base class for all energy calculators."""

    def __init__(self, parameters: dict | None = None):
        """Initializes the calculator, optionally with parameters."""
        self.parameters = parameters if parameters is not None else {}
        # Potentially load/validate parameters here

    @abstractmethod
    def calculate_energy(self, cluster: Cluster) -> float:
        """Calculates the energy of a given cluster.

        Args:
            cluster: The Cluster object for which to calculate the energy.

        Returns:
            The calculated energy as a float.

        Raises:
            NotImplementedError: If the method is not implemented by a subclass.
        """
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}(parameters={self.parameters})" 