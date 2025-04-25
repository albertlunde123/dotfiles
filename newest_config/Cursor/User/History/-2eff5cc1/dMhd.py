from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPainter, QPen, QColor
from .base_tool import BaseTool
from ..elements.s_curve_element import SCurveElement

class SCurveTool(BaseTool):
    """Tool for drawing S-curves using two connected half-circles."""
    
    def __init__(self):
        super().__init__()
        self.start_point = None
        self.end_point = None
        self.preview_element = None
        self.drawing = False
        
    def activate(self, canvas):
        super().activate(canvas)
        self._reset_state()
        
    def deactivate(self):
        self._reset_state()
        super().deactivate()
        
    def _reset_state(self):
        """Reset the tool's state."""
        self.start_point = None
        self.end_point = None
        self.preview_element = None
        self.drawing = False
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            pos = event.pos()
            
            if not self.drawing:
                # First click - set start point
                self.start_point = QPointF(pos)
                self.drawing = True
                self.canvas.update()
            else:
                # Second click - set end point and create the element
                self.end_point = QPointF(pos)
                self._create_element()
                self._reset_state()
                self.canvas.update()
                
    def mouseMoveEvent(self, event):
        if self.drawing:
            # Update the end point for preview
            self.end_point = QPointF(event.pos())
            self.canvas.update()
            
    def draw(self, painter):
        """Draw the preview of the S-curve."""
        if self.drawing and self.start_point and self.end_point:
            # Create a temporary element for preview
            if not self.preview_element:
                self.preview_element = SCurveElement(self.start_point, self.end_point, self.canvas.current_color)
            else:
                self.preview_element.start_point = self.start_point
                self.preview_element.end_point = self.end_point
                self.preview_element._update_control_points()
                
            # Draw the preview
            self.preview_element.draw(painter)
            
    def _create_element(self):
        """Create the S-curve element and add it to the canvas."""
        if self.start_point and self.end_point:
            element = SCurveElement(self.start_point, self.end_point, self.canvas.current_color)
            element.line_thickness = self.canvas.current_line_thickness
            element.dash_pattern_key = self.canvas.current_dash_pattern
            self.canvas.add_element(element) 