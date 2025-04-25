from ase.data import atomic_numbers, vdw_radii
import numpy as np # Using numpy for distance calculation is more standard

_vdw_radii_fallback = {symbol: vdw_radii[num] for symbol, num in atomic_numbers.items() if num < len(vdw_radii)}
_max_atomic_number = max(atomic_numbers.values()) # For potential future validation

class Atom:
    """Represents a single atom within a cluster, including its VdW radius."""
    def __init__(self, symbol: str, position: tuple[float, float, float], id: int | None = None):
        """
        Initializes an Atom object.

        Args:
            symbol: The chemical symbol of the atom (e.g., 'H', 'C', 'O').
            position: A tuple or list containing the (x, y, z) coordinates.
            id: An optional unique identifier for the atom.
        """
        if not isinstance(symbol, str) or not symbol:
            raise ValueError("Atom symbol must be a non-empty string.")
        if symbol not in atomic_numbers:
            raise ValueError(f"Unknown atom symbol: {symbol}")

        if not isinstance(position, (list, tuple)) or len(position) != 3:
            raise ValueError("Position must be a list or tuple of 3 coordinates.")
        try:
            # Store position as a numpy array for easier calculations
            self.position = np.array(position, dtype=float)
        except (ValueError, TypeError):
            raise ValueError("Coordinates must be convertible to floats.")

        self.symbol = symbol
        self.id = id
        self.atomic_number = atomic_numbers[symbol]

        # Get Van der Waals radius from ASE data
        # Use the precomputed dictionary as direct access by atomic number can fail for high Z
        # Provide a default (e.g., 1.0 Angstrom) if somehow not found (though unlikely with checks)
        self.vdw_radius = _vdw_radii_fallback.get(symbol, 1.0)

        # Add other potential attributes like charge, mass, etc. later

    def __repr__(self):
        pos_str = np.array2string(self.position, precision=3, separator=', ')
        return f"Atom(id={self.id}, symbol='{self.symbol}', radius={self.vdw_radius:.3f}, position={pos_str})"

    def distance_to(self, other_atom: 'Atom') -> float:
        """Calculates the Euclidean distance to another atom."""
        if not isinstance(other_atom, Atom):
             raise TypeError("Input must be an Atom object.")
        # Use numpy for efficient distance calculation
        return np.linalg.norm(self.position - other_atom.position) 