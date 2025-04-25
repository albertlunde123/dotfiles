from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPainter, QPen, QColor
from .base_tool import BaseTool
from ..elements.s_curve_element import SCurveElement
# Import the central snapping function and indicator drawing
from ..utils.snapping import get_snap_target, draw_snap_indicator, DEFAULT_ELEMENT_SNAP_THRESHOLD

# Helper for squared distance
def dist_sq(p1: QPointF, p2: QPointF) -> float:
    return (p1.x() - p2.x())**2 + (p1.y() - p2.y())**2

class SCurveTool(BaseTool):
    """Tool for drawing S-curves using two connected half-circles."""
    
    def __init__(self):
        super().__init__()
        self.points = []  # Store all points for the multi-segment S-curve
        self.current_mouse_pos = None
        self.preview_element = None
        self.current_snap_info = (None, None)  # (snap_point, snap_type)
        self.snap_threshold = DEFAULT_ELEMENT_SNAP_THRESHOLD
        
    def activate(self, canvas):
        super().activate(canvas)
        self._reset_state()
        
    def deactivate(self):
        self._reset_state()
        super().deactivate()
        
    def _reset_state(self):
        """Reset the tool's state."""
        self.points = []
        self.current_mouse_pos = None
        self.preview_element = None
        self.current_snap_info = (None, None)
        
    def _find_best_snap_point(self, original_pos: QPointF):
        """
        Finds the best snap point considering grid, existing elements,
        and the current curve being drawn.
        Returns: tuple (snapped_point: QPointF, snap_type: str | None)
        """
        best_snap_point = original_pos
        best_snap_type = None
        min_snap_dist_sq = float('inf')

        # 1. Check Grid and Existing Elements using central function
        grid_element_snap, ge_snap_type = get_snap_target(
            original_pos, self.canvas.elements, self.canvas.grid_manager, self.snap_threshold
        )
        if ge_snap_type:  # Found a grid or element snap
            dist = dist_sq(original_pos, grid_element_snap)
            if dist < min_snap_dist_sq:
                min_snap_dist_sq = dist
                best_snap_point = grid_element_snap
                best_snap_type = ge_snap_type

        # 2. Check Self-Snapping (points in current curve)
        self_snap_point = None
        if len(self.points) > 0:
            threshold_sq = self.snap_threshold ** 2
            # Check all points except the very last one (where we are drawing from)
            for i in range(len(self.points) - 1):
                point = self.points[i]
                d_sq = dist_sq(original_pos, point)
                if d_sq < threshold_sq and d_sq < min_snap_dist_sq:
                    min_snap_dist_sq = d_sq
                    self_snap_point = QPointF(point)  # Found a closer self-snap

        # If self-snap was closer, it becomes the best snap
        if self_snap_point:
            best_snap_point = self_snap_point
            best_snap_type = 'self'  # Use a specific type for self-snapping

        # If no snap found better than original pos, reset type
        if best_snap_point == original_pos:
            best_snap_type = None

        return best_snap_point, best_snap_type
        
    def mousePressEvent(self, event):
        pos = event.pos()
        snap_point, _ = self._find_best_snap_point(QPointF(pos))
        
        if event.button() == Qt.LeftButton:
            # Add point to the list (use snap point if available)
            self.points.append(snap_point if snap_point else QPointF(pos))
            self.canvas.update()
            
        elif event.button() == Qt.RightButton:
            # Finish the curve if we have at least two points
            if len(self.points) >= 2:
                self._create_final_curve()
            self._reset_state()
            self.canvas.update()
                
    def mouseMoveEvent(self, event):
        # Find snap point
        original_pos = QPointF(event.pos())
        snap_point, snap_type = self._find_best_snap_point(original_pos)
        
        # Update the preview position and snap info
        self.current_mouse_pos = snap_point if snap_point else original_pos
        self.current_snap_info = (snap_point, snap_type)
        self.canvas.update()
            
    def draw(self, painter):
        """Draw the preview of the S-curves."""
        # Draw completed segments
        for i in range(len(self.points) - 1):
            element = SCurveElement(self.points[i], self.points[i + 1], self.canvas.line_color)
            element.draw(painter)
        
        # Draw preview segment if we have at least one point and current mouse position
        if self.points and self.current_mouse_pos:
            preview = SCurveElement(self.points[-1], self.current_mouse_pos, self.canvas.line_color)
            preview.draw(painter)
            
            # Draw snap indicator if we have a snap point
            snap_point, snap_type = self.current_snap_info
            if snap_type:  # Draw indicator if type is not None
                draw_snap_indicator(painter, snap_point)
            
    def _create_final_curve(self):
        """Create the final multi-segment S-curve."""
        # Create S-curve elements for each pair of consecutive points
        for i in range(len(self.points) - 1):
            element = SCurveElement(self.points[i], self.points[i + 1], self.canvas.line_color)
            self.canvas.add_element(element) 