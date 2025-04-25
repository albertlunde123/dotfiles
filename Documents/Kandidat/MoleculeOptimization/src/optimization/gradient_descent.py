import numpy as np
import copy

from src.molecule import Cluster, Atom
from src.calculators import EnergyCalculator
from .base_optimizer import Optimizer

class GradientDescentOptimizer(Optimizer):
    """Simple gradient descent optimizer.

    Moves atoms proportional to the negative gradient (force).
    """

    def __init__(self, calculator: EnergyCalculator, parameters: dict | None = None):
        """Initializes the Gradient Descent optimizer.

        Required parameters:
            step_size (float): The scaling factor for the force vector.

        Optional parameters:
            max_iterations (int): Maximum number of steps (default: 100).
            convergence_threshold (float): Convergence criterion based on max force
                                         component (default: 1e-5).
        """
        super().__init__(calculator, parameters)
        self.step_size = self.parameters.get('step_size')
        if self.step_size is None:
            raise ValueError("'step_size' parameter is required for GradientDescentOptimizer")
        self.step_size = float(self.step_size)

        # Override defaults if specified in parameters
        self.max_iterations = int(self.parameters.get('max_iterations', 100))
        self.convergence_threshold = float(self.parameters.get('convergence_threshold', 1e-5))


    def optimize(self, initial_cluster: Cluster) -> Cluster:
        """Runs the gradient descent optimization.

        Args:
            initial_cluster: The starting Cluster configuration.

        Returns:
            The optimized Cluster configuration.
        """
        current_cluster = copy.deepcopy(initial_cluster) # Work on a copy

        print(f"Starting Gradient Descent Optimization:")
        print(f"  Max Iterations: {self.max_iterations}")
        print(f"  Step Size: {self.step_size}")
        print(f"  Convergence Threshold (Max Force Component): {self.convergence_threshold}")

        for iteration in range(self.max_iterations):
            # Calculate energy and forces
            try:
                energy, forces = self.calculator.calculate(current_cluster)
            except Exception as e:
                print(f"ERROR: Energy/Force calculation failed on iteration {iteration}: {e}")
                # Return the last valid cluster state before the error
                # Or handle more gracefully depending on expected errors
                return current_cluster

            # Check for convergence: max absolute force component
            max_force_component = np.max(np.abs(forces))
            print(f"Iter: {iteration:4d}, Energy: {energy:12.6f}, Max Force: {max_force_component:10.6e}")

            if max_force_component < self.convergence_threshold:
                print(f"Converged after {iteration} iterations.")
                break

            # Update positions: X_new = X_old + step_size * F
            current_positions = np.array([atom.position for atom in current_cluster.atoms])
            new_positions = current_positions + self.step_size * forces

            # Create the next cluster configuration
            # Keep atom symbols and IDs, just update positions
            new_atoms = []
            for i, atom in enumerate(current_cluster.atoms):
                # Create new Atom object with updated position
                # Note: This creates new Atom instances each step.
                # Could potentially update positions in-place if Atom.position was mutable
                # and Cluster structure allowed, but creating new ones is safer.
                new_atoms.append(Atom(symbol=atom.symbol, position=new_positions[i], id=atom.id))

            # Assume bonds are defined by indices/topology and don't change here
            current_cluster = Cluster(atoms=new_atoms, bonds=current_cluster.bonds)

        else: # Loop finished without break (convergence)
            print(f"Warning: Maximum number of iterations ({self.max_iterations}) reached without convergence.")

        return current_cluster

    def __repr__(self):
        # Customize representation if needed
        return super().__repr__() 