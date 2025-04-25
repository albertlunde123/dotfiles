# utils/snapping.py
from PyQt5.QtGui import QColor, QPen, QBrush
from PyQt5.QtCore import QPointF
from pyqt_drawing_app.utils.colors import get_snap_colors
from typing import TYPE_CHECKING, Tuple, Optional # <--- ADD THIS IMPORT

if TYPE_CHECKING:
    from pyqt_drawing_app.utils.grid import GridManager
    from pyqt_drawing_app.elements import DrawingElement
    
SNAP_INDICATOR_COLOR, SNAP_INDICATOR_FILL = get_snap_colors()
SNAP_INDICATOR_COLOR, SNAP_INDICATOR_FILL = get_snap_colors()
DEFAULT_ELEMENT_SNAP_THRESHOLD = 10 # Pixels

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
    Returns a QPointF if found, otherwise None. (Renamed for clarity)
    """
    min_dist_sq = threshold ** 2 # Use squared distance for efficiency
    closest_point = None

    for element in elements:
        if hasattr(element, 'snap_points'):
            for point in element.snap_points:
                dist_sq = (pos.x() - point.x())**2 + (pos.y() - point.y())**2
                if dist_sq < min_dist_sq:
                    min_dist_sq = dist_sq
                    closest_point = QPointF(point) # Return a copy

    return closest_point

def get_snap_target(
    original_pos: QPointF,
    elements: list['DrawingElement'],
    grid_manager: 'GridManager',
    element_snap_threshold: float = DEFAULT_ELEMENT_SNAP_THRESHOLD
) -> Tuple[QPointF, Optional[str]]:
    """
    Determines the best snap target, considering grid and elements.
    Returns: (snapped_point, snap_type) where snap_type is 'grid', 'element', or None.
    """
    snapped_point = original_pos
    snap_type = None
    min_dist_sq = float('inf')

    # 1. Check Grid Snap
    grid_snap_point = grid_manager.snap_to_grid(original_pos) # Checks enabled status internally
    if grid_snap_point != original_pos:
        dist_sq = (original_pos.x() - grid_snap_point.x())**2 + (original_pos.y() - grid_snap_point.y())**2
        # Grid snaps if it's within half the grid spacing distance (prevents snapping too far)
        if dist_sq < (grid_manager.spacing / 8) ** 2:
             min_dist_sq = dist_sq
             snapped_point = grid_snap_point
             snap_type = 'grid'

    # 2. Check Element Snap
    element_snap_point = find_element_snap_point(elements, original_pos, element_snap_threshold)
    if element_snap_point:
        dist_sq = (original_pos.x() - element_snap_point.x())**2 + (original_pos.y() - element_snap_point.y())**2
        # Only override grid snap if element snap is closer AND within threshold
        if dist_sq < min_dist_sq:
            # min_dist_sq = dist_sq # No need to update min_dist_sq here
            snapped_point = element_snap_point
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
