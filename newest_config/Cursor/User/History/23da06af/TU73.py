class Atom:
    """Represents a single atom within a cluster."""
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
        if not isinstance(position, (list, tuple)) or len(position) != 3:
            raise ValueError("Position must be a list or tuple of 3 coordinates.")
        try:
            self.position = tuple(float(p) for p in position)
        except (ValueError, TypeError):
            raise ValueError("Coordinates must be convertible to floats.")

        self.symbol = symbol
        self.id = id
        # Add other potential attributes like charge, mass, etc. later

    def __repr__(self):
        pos_str = ", ".join(f"{p:.3f}" for p in self.position)
        return f"Atom(id={self.id}, symbol='{self.symbol}', position=({pos_str}))"

    def distance_to(self, other_atom: 'Atom') -> float:
        """Calculates the Euclidean distance to another atom."""
        # Simple distance calculation, assuming numpy might not be available yet
        dx = self.position[0] - other_atom.position[0]
        dy = self.position[1] - other_atom.position[1]
        dz = self.position[2] - other_atom.position[2]
        return (dx**2 + dy**2 + dz**2)**0.5 