from abc import ABC, abstractmethod

# Potential type hinting issue if src is not in PYTHONPATH
try:
    from src.molecule import Cluster
except ImportError:
    # Allow for potential direct testing or different project structures
    # This might need adjustment based on how tests/scripts are run
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    try:
        from molecule import Cluster
    except ImportError:
        # Define a dummy Cluster if molecule isn't found (e.g., during linting)
        class Cluster:
            pass

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