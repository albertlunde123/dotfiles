from abc import ABC, abstractmethod

# Assuming 'src' is in the Python path
from src.molecule import Cluster
from src.calculators import EnergyCalculator

class Optimizer(ABC):
    """Abstract base class for all geometry optimizers."""

    def __init__(self, calculator: EnergyCalculator, parameters: dict | None = None):
        """Initializes the optimizer.

        Args:
            calculator: The EnergyCalculator instance to use for energy evaluation.
            parameters: Optional dictionary of optimizer-specific parameters
                        (e.g., step size, convergence criteria, max iterations).
        """
        if not isinstance(calculator, EnergyCalculator):
            raise TypeError("Calculator must be an instance of EnergyCalculator.")
        self.calculator = calculator
        self.parameters = parameters if parameters is not None else {}
        # Example: Extract common parameters
        self.max_iterations = self.parameters.get('max_iterations', 100)
        self.convergence_threshold = self.parameters.get('convergence_threshold', 1e-5)

    @abstractmethod
    def optimize(self, initial_cluster: Cluster) -> Cluster:
        """Runs the optimization algorithm.

        Args:
            initial_cluster: The starting Cluster configuration.

        Returns:
            The optimized Cluster configuration.

        Raises:
            NotImplementedError: If the method is not implemented by a subclass.
        """
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}(calculator={self.calculator!r}, parameters={self.parameters})" 