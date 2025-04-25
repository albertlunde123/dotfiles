from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPainter, QPen, QColor
from .base_tool import BaseTool
from ..elements.s_curve_element import SCurveElement

class SCurveTool(BaseTool):
    """Tool for drawing S-curves using two connected half-circles."""
    
    def __init__(self):
        super().__init__()
        self.points = []  # Store all points for the multi-segment S-curve
        self.current_mouse_pos = None
        self.preview_element = None
        
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
        
    def mousePressEvent(self, event):
        pos = event.pos()
        
        if event.button() == Qt.LeftButton:
            # Add point to the list
            self.points.append(QPointF(pos))
            self.canvas.update()
            
        elif event.button() == Qt.RightButton:
            # Finish the curve if we have at least two points
            if len(self.points) >= 2:
                self._create_final_curve()
            self._reset_state()
            self.canvas.update()
                
    def mouseMoveEvent(self, event):
        # Update the preview
        self.current_mouse_pos = QPointF(event.pos())
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
            
    def _create_final_curve(self):
        """Create the final multi-segment S-curve."""
        # Create S-curve elements for each pair of consecutive points
        for i in range(len(self.points) - 1):
            element = SCurveElement(self.points[i], self.points[i + 1], self.canvas.line_color)
            self.canvas.add_element(element) 