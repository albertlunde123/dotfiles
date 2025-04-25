from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPainter, QPen, QColor
from .base_tool import BaseTool
from ..elements.polyline_element import PolylineElement

class PolylineTool(BaseTool):
    """Tool for drawing polylines with multiple points."""
    
    def __init__(self):
        super().__init__()
        self.points = []
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
        self.points = []
        self.preview_element = None
        self.drawing = False
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            pos = event.pos()
            
            # Add the point to the list
            self.points.append(QPointF(pos))
            self.drawing = True
            self.canvas.update()
            
        elif event.button() == Qt.RightButton and len(self.points) >= 2:
            # Right-click to finish the polyline
            self._create_element()
            self._reset_state()
            self.canvas.update()
            
    def mouseMoveEvent(self, event):
        if self.drawing:
            # Update the preview
            self.canvas.update()
            
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape and len(self.points) >= 2:
            # Escape key to finish the polyline
            self._create_element()
            self._reset_state()
            self.canvas.update()
            
    def draw(self, painter):
        """Draw the preview of the polyline."""
        if self.drawing and len(self.points) > 0:
            # Create a temporary element for preview
            if not self.preview_element:
                self.preview_element = PolylineElement(self.points, self.canvas.current_color)
            else:
                self.preview_element.points = self.points.copy()
                
            # Draw the preview
            self.preview_element.draw(painter)
            
            # Draw a line from the last point to the current mouse position
            if len(self.points) > 0:
                painter.setPen(QPen(self.canvas.current_color, self.canvas.current_line_thickness))
                painter.drawLine(self.points[-1], self.canvas.mapFromGlobal(self.canvas.cursor().pos()))
            
    def _create_element(self):
        """Create the polyline element and add it to the canvas."""
        if len(self.points) >= 2:
            element = PolylineElement(self.points, self.canvas.current_color)
            element.line_thickness = self.canvas.current_line_thickness
            element.dash_pattern_key = self.canvas.current_dash_pattern
            self.canvas.add_element(element) 