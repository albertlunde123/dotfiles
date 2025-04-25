#!/usr/bin/env python
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import copy

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.molecule import Atom, Cluster
from src.calculators import DistanceBasedCalculator
from src.optimization import GradientDescentOptimizer
from src.visualization import plot_cluster

def run_optimization_with_history(optimizer: GradientDescentOptimizer, initial_cluster: Cluster) -> list[np.ndarray]:
    """
    Runs optimization and returns the history of atom positions at each step.

    Args:
        optimizer: The configured Optimizer instance.
        initial_cluster: The starting Cluster configuration.

    Returns:
        A list of numpy arrays, where each array contains the atom positions
        at a specific iteration.
    """
    history = []
    current_cluster = copy.deepcopy(initial_cluster) # Work on a copy

    print(f"Running Optimization for History Tracking:")
    print(f"  Optimizer: {optimizer.__class__.__name__}")
    print(f"  Calculator: {optimizer.calculator.__class__.__name__}")
    print(f"  Max Iterations: {optimizer.max_iterations}")
    print(f"  Step Size: {optimizer.step_size}")
    print(f"  Convergence Threshold: {optimizer.convergence_threshold}")

    for iteration in range(optimizer.max_iterations):
        # Store current positions
        current_positions = np.array([atom.position for atom in current_cluster.atoms])
        history.append(current_positions)

        # Calculate energy and forces
        try:
            energy, forces = optimizer.calculator.calculate(current_cluster)
        except Exception as e:
            print(f"ERROR: Calculation failed on iteration {iteration}: {e}")
            break # Stop if calculation fails

        # Check for convergence
        max_force_component = np.max(np.abs(forces))
        print(f"Iter: {iteration:4d}, Energy: {energy:12.6f}, Max Force: {max_force_component:10.6e}")

        if max_force_component < optimizer.convergence_threshold:
            print(f"Converged after {iteration} iterations.")
            # Add final converged positions to history
            history.append(current_positions + optimizer.step_size * forces) # Store the (almost) final state
            break

        # Update positions
        new_positions = current_positions + optimizer.step_size * forces

        # Create the next cluster state (needed for next calculation)
        new_atoms = [Atom(symbol=atom.symbol, position=new_positions[i], id=atom.id)
                     for i, atom in enumerate(current_cluster.atoms)]
        current_cluster = Cluster(atoms=new_atoms, bonds=current_cluster.bonds) # Bonds aren't used here but kept for structure

    else: # Loop finished without break
        print(f"Warning: Max iterations ({optimizer.max_iterations}) reached without convergence.")
        # Store the final positions after max iterations
        history.append(np.array([atom.position for atom in current_cluster.atoms]))


    print(f"Optimization history recorded with {len(history)} steps.")
    return history


def main():
    """Sets up and runs the 2-atom optimization and animation."""

    # 1. Define Initial Cluster (e.g., two Carbon atoms)
    # Start them slightly apart
    atom1 = Atom(symbol='C', position=(0.0, 0.0, 0.0), id=1)
    atom2 = Atom(symbol='C', position=(3.5, 0.5, 0.0), id=2) # VdW for C is ~1.7A, so sum is ~3.4A
    initial_cluster = Cluster(atoms=[atom1, atom2])
    print(f"Initial Cluster: {initial_cluster}")

    # 2. Instantiate Calculator
    # Using the default example potential in DistanceBasedCalculator
    calculator = DistanceBasedCalculator()

    # 3. Instantiate Optimizer
    optimizer_params = {
        'step_size': 0.01, # Adjust this - crucial parameter!
        'max_iterations': 200,
        'convergence_threshold': 1e-4
    }
    optimizer = GradientDescentOptimizer(calculator=calculator, parameters=optimizer_params)

    # 4. Run optimization and get history
    position_history = run_optimization_with_history(optimizer, initial_cluster)

    if not position_history:
        print("No history recorded, cannot animate.")
        return

    # 5. Setup Animation
    fig, ax = plt.subplots()
    ax.set_aspect('equal', adjustable='box')

    # Determine fixed axis limits based on the whole trajectory
    all_positions = np.concatenate(position_history, axis=0)
    min_coords = np.min(all_positions[:, :2], axis=0) - 1.0 # XY plane, add padding
    max_coords = np.max(all_positions[:, :2], axis=0) + 1.0 # XY plane, add padding
    ax.set_xlim(min_coords[0], max_coords[0])
    ax.set_ylim(min_coords[1], max_coords[1])

    # Keep initial atom info for plotting symbols/radii
    base_atoms_for_plot = initial_cluster.atoms

    def update(frame_num):
        ax.clear() # Clear previous frame
        ax.set_xlim(min_coords[0], max_coords[0]) # Reapply limits
        ax.set_ylim(min_coords[1], max_coords[1]) # Reapply limits

        current_positions = position_history[frame_num]

        # Create a temporary cluster for plotting this frame
        frame_atoms = [Atom(symbol=base_atoms_for_plot[i].symbol,
                            position=current_positions[i],
                            id=base_atoms_for_plot[i].id)
                       for i in range(len(base_atoms_for_plot))]
        frame_cluster = Cluster(atoms=frame_atoms)

        # Plot this frame (in 2D)
        plot_cluster(frame_cluster, dim=2, show_labels=True,
                     use_radii_for_size=True, size_scale_factor=200.0, # Adjust scale factor
                     ax=ax)

        ax.set_title(f"Optimization Step {frame_num}")
        # Return the artists updated, needed for some backends/blit=True
        # For simplicity, returning empty list works often
        return []

    # 6. Create and Save Animation
    ani = animation.FuncAnimation(fig, update, frames=len(position_history),
                                  interval=100, blit=False) # interval in ms, blit=False is often safer

    output_filename = "optimization_2_atoms.gif"
    print(f"\nSaving animation to {output_filename}...")
    try:
        # You might need to install imagemagick or ffmpeg
        # On Ubuntu: sudo apt install imagemagick ffmpeg
        ani.save(output_filename, writer='pillow', fps=10) # Using pillow writer
        print(f"Animation saved successfully.")
    except Exception as e:
        print(f"ERROR saving animation: {e}")
        print("Showing animation interactively instead (if possible).")
        plt.show() # Fallback to showing interactively


if __name__ == "__main__":
    main()