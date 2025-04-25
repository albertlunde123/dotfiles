from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPainter, QPen, QColor
from .base_tool import BaseTool
from ..elements.s_curve_element import SCurveElement
# Import the central snapping function and indicator drawing
from ..utils.snapping import get_snap_target, draw_snap_indicator, DEFAULT_ELEMENT_SNAP_THRESHOLD

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
        and the current polyline being drawn.
        """
        # Get snap point from grid and existing elements
        snap_point, snap_type = get_snap_target(
            original_pos,
            self.canvas.elements,
            self.canvas.grid_manager,
            self.snap_threshold
        )
        return snap_point, snap_type
        
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
            if snap_point:
                draw_snap_indicator(painter, snap_point)
            
    def _create_final_curve(self):
        """Create the final multi-segment S-curve."""
        # Create S-curve elements for each pair of consecutive points
        for i in range(len(self.points) - 1):
            element = SCurveElement(self.points[i], self.points[i + 1], self.canvas.line_color)
            self.canvas.add_element(element) 