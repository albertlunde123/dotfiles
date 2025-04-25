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
    grid_snap_threshold: float = DEFAULT_GRID_SNAP_THRESHOLD
) -> Tuple[QPointF, Optional[str]]:
    """
    Determines the best snap target (grid or element point) within thresholds.
    Returns the exact snap point if found.
    Args:
        original_pos: The original position to snap from
        elements: List of elements to snap to
        grid_manager: Grid manager for grid snapping
        element_snap_threshold: Distance threshold for element snapping
        grid_snap_threshold: Distance threshold for grid snapping (fraction of spacing)
    Returns: (snapped_point, snap_type) where snapped_point is the exact snap target
             or original_pos if no snap occurred. snap_type is 'grid', 'element', or None.
    """
    best_snap_point = original_pos
    best_snap_type = None
    min_dist_sq = float('inf')

    # 1. Check Grid Snap
    if grid_manager.snap_enabled:
        grid_snap_point = grid_manager.snap_to_grid(original_pos)
        if grid_snap_point != original_pos:
            dist_sq = (original_pos.x() - grid_snap_point.x())**2 + (original_pos.y() - grid_snap_point.y())**2
            max_grid_dist_sq = (grid_manager.spacing * grid_snap_threshold) ** 2

            if dist_sq < max_grid_dist_sq:
                # Hard snap: If within threshold, use the exact grid point
                min_dist_sq = dist_sq
                best_snap_point = grid_snap_point # Exact grid point
                best_snap_type = 'grid'

    # 2. Check Element Snap
    element_snap_point = find_element_snap_point(elements, original_pos, element_snap_threshold)
    if element_snap_point:
        dist_sq = (original_pos.x() - element_snap_point.x())**2 + (original_pos.y() - element_snap_point.y())**2
        # Only override grid snap if element snap is closer AND within element threshold
        if dist_sq < min_dist_sq:
            # Hard snap: Use the exact element snap point
            best_snap_point = element_snap_point # Exact element point
            best_snap_type = 'element'
            # No need to update min_dist_sq here, we just take the closer one

    return best_snap_point, best_snap_type

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
