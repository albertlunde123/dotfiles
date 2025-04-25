# utils/snapping.py
from PyQt5.QtGui import QColor, QPen, QBrush
from PyQt5.QtCore import QPointF
from pyqt_drawing_app.utils.colors import get_snap_colors
from typing import TYPE_CHECKING, Tuple, Optional

if TYPE_CHECKING:
    from pyqt_drawing_app.utils.grid import GridManager
    from pyqt_drawing_app.elements import DrawingElement
    
SNAP_INDICATOR_COLOR, SNAP_INDICATOR_FILL = get_snap_colors()
DEFAULT_ELEMENT_SNAP_THRESHOLD = 10  # Pixels
DEFAULT_GRID_SNAP_THRESHOLD = 0.25   # Fraction of grid spacing
MOVE_MODE_SNAP_STRENGTH = 0.3  # Weaker snap when moving elements

def set_snap_colors(indicator_color, fill_color=None):
    """Set the colors used for snap indicators"""
    global SNAP_INDICATOR_COLOR, SNAP_INDICATOR_FILL
    SNAP_INDICATOR_COLOR = indicator_color
    if fill_color:
        SNAP_INDICATOR_FILL = fill_color
    else:
        # Create a semi-transparent version of the indicator color
        SNAP_INDICATOR_FILL = QColor(indicator_color)
        SNAP_INDICATOR_FILL.setAlpha(80)

def find_element_snap_point(elements: list['DrawingElement'], pos: QPointF, threshold: float) -> Optional[QPointF]:
    """
    Find the closest element snap point (vertex/center) within threshold.
    Returns a QPointF if found, otherwise None.
    """
    min_dist_sq = threshold ** 2  # Use squared distance for efficiency
    closest_point = None

    for element in elements:
        if hasattr(element, 'snap_points'):
            for point in element.snap_points:
                dist_sq = (pos.x() - point.x())**2 + (pos.y() - point.y())**2
                if dist_sq < min_dist_sq:
                    min_dist_sq = dist_sq
                    closest_point = QPointF(point)  # Return a copy

    return closest_point

def get_snap_target(
    original_pos: QPointF,
    elements: list['DrawingElement'],
    grid_manager: 'GridManager',
    element_snap_threshold: float = DEFAULT_ELEMENT_SNAP_THRESHOLD,
    grid_snap_threshold: float = DEFAULT_GRID_SNAP_THRESHOLD,
    is_placement_mode: bool = True
) -> Tuple[QPointF, Optional[str]]:
    """
    Determines the best snap target, considering grid and elements.
    Args:
        original_pos: The original position to snap from
        elements: List of elements to snap to
        grid_manager: Grid manager for grid snapping
        element_snap_threshold: Distance threshold for element snapping
        grid_snap_threshold: Distance threshold for grid snapping
        is_placement_mode: Whether we're placing new points (strong snap) or moving existing elements (weak snap)
    Returns: (snapped_point, snap_type) where snap_type is 'grid', 'element', or None.
    """
    snapped_point = original_pos
    snap_type = None
    min_dist_sq = float('inf')

    # Adjust snap strength based on mode
    snap_strength_multiplier = 1.0 if is_placement_mode else MOVE_MODE_SNAP_STRENGTH

    # 1. Check Grid Snap
    if grid_manager.snap_enabled:
        grid_snap_point = grid_manager.snap_to_grid(original_pos)
        if grid_snap_point != original_pos:
            dist_sq = (original_pos.x() - grid_snap_point.x())**2 + (original_pos.y() - grid_snap_point.y())**2
            max_grid_dist_sq = (grid_manager.spacing * grid_snap_threshold) ** 2
            
            if dist_sq < max_grid_dist_sq:
                # Calculate snap strength (0 to 1) based on distance
                snap_strength = (1 - (dist_sq / max_grid_dist_sq)) * snap_strength_multiplier
                # Apply gradual snapping
                snapped_point = QPointF(
                    original_pos.x() + (grid_snap_point.x() - original_pos.x()) * snap_strength,
                    original_pos.y() + (grid_snap_point.y() - original_pos.y()) * snap_strength
                )
                min_dist_sq = dist_sq
                snap_type = 'grid'

    # 2. Check Element Snap
    element_snap_point = find_element_snap_point(elements, original_pos, element_snap_threshold)
    if element_snap_point:
        dist_sq = (original_pos.x() - element_snap_point.x())**2 + (original_pos.y() - element_snap_point.y())**2
        # Only override grid snap if element snap is closer AND within threshold
        if dist_sq < min_dist_sq:
            # Calculate snap strength for element snap
            snap_strength = (1 - (dist_sq / (element_snap_threshold ** 2))) * snap_strength_multiplier
            # Apply gradual snapping
            snapped_point = QPointF(
                original_pos.x() + (element_snap_point.x() - original_pos.x()) * snap_strength,
                original_pos.y() + (element_snap_point.y() - original_pos.y()) * snap_strength
            )
            snap_type = 'element'

    return snapped_point, snap_type

def draw_snap_indicator(painter, point):
    """Draw a visual indicator for snap points"""
    # Save painter state
    painter.save()
    
    # Draw outer circle
    painter.setPen(QPen(SNAP_INDICATOR_COLOR))
    painter.setBrush(QBrush(SNAP_INDICATOR_FILL))
    painter.drawEllipse(point, 8, 8)
    
    # Restore painter state
    painter.restore()
