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

        # Validate position input (allow list, tuple, or numpy array)
        is_valid_shape = False
        temp_position = None
        if isinstance(position, (list, tuple)):
            if len(position) == 3:
                try:
                    temp_position = np.array(position, dtype=float)
                    is_valid_shape = True
                except (ValueError, TypeError):
                    pass # Error handled below
        elif isinstance(position, np.ndarray):
            if position.shape == (3,):
                if np.issubdtype(position.dtype, np.number): # Check if numeric type
                    temp_position = np.array(position, dtype=float) # Ensure float dtype
                    is_valid_shape = True
                # else: could raise error for non-numeric numpy array

        if not is_valid_shape or temp_position is None:
            raise ValueError("Position must be a list, tuple, or numpy array of 3 numeric coordinates.")

        # Store position as a numpy array
        self.position = temp_position

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