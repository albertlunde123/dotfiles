# pyqt_drawing_app/elements/polyline_element.py
from PyQt5.QtCore import Qt, QPointF, QRectF
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush
from .base_element import DrawingElement

class PolylineElement(DrawingElement):
    """A polyline element consisting of multiple connected line segments."""
    
    def __init__(self, points, color=None):
        super().__init__(color)
        self.points = [QPointF(p) for p in points]
        
    def _draw_shape(self, painter):
        """Draw the polyline."""
        if len(self.points) < 2:
            return
            
        # Draw the polyline
        for i in range(len(self.points) - 1):
            painter.drawLine(self.points[i], self.points[i + 1])
            
        # Draw arrowheads if needed
        if self.start_arrowhead != DrawingElement.ARROWHEAD_NONE and len(self.points) >= 2:
            self._draw_arrowhead(painter, self.points[0], self.points[1], self.start_arrowhead)
            
        if self.end_arrowhead != DrawingElement.ARROWHEAD_NONE and len(self.points) >= 2:
            self._draw_arrowhead(painter, self.points[-1], self.points[-2], self.end_arrowhead)
            
    def _draw_arrowhead(self, painter, tip, base, arrow_type):
        """Draw an arrowhead at the specified position."""
        # Calculate the direction vector
        dx = base.x() - tip.x()
        dy = base.y() - tip.y()
        length = (dx * dx + dy * dy) ** 0.5
        
        if length < 0.1:  # Avoid division by zero
            return
            
        # Normalize the direction vector
        dx /= length
        dy /= length
        
        # Calculate the perpendicular vector
        px = -dy
        py = dx
        
        # Calculate the arrowhead size based on line thickness
        size = max(5, self.line_thickness * 3)
        
        # Calculate the arrowhead points
        if arrow_type == DrawingElement.ARROWHEAD_TRIANGLE:
            # Triangle arrowhead
            p1 = QPointF(tip.x() + size * dx, tip.y() + size * dy)
            p2 = QPointF(tip.x() + size * 0.5 * px, tip.y() + size * 0.5 * py)
            p3 = QPointF(tip.x() - size * 0.5 * px, tip.y() - size * 0.5 * py)
            
            # Draw the arrowhead
            painter.drawLine(tip, p1)
            painter.drawLine(p1, p2)
            painter.drawLine(p2, p3)
            painter.drawLine(p3, p1)
            
        elif arrow_type == DrawingElement.ARROWHEAD_LINE:
            # Line arrowhead
            p1 = QPointF(tip.x() + size * dx, tip.y() + size * dy)
            p2 = QPointF(tip.x() + size * 0.5 * px, tip.y() + size * 0.5 * py)
            p3 = QPointF(tip.x() - size * 0.5 * px, tip.y() - size * 0.5 * py)
            
            # Draw the arrowhead
            painter.drawLine(tip, p1)
            painter.drawLine(p1, p2)
            painter.drawLine(p2, p3)
            painter.drawLine(p3, p1)
            
    def _draw_handles(self, painter):
        """Draw handles for the polyline."""
        # Draw handles at each point
        for point in self.points:
            self._draw_point_handle(painter, point)
            
    def contains_point(self, point):
        """Check if a point is within the polyline."""
        # Check if the point is near any line segment
        for i in range(len(self.points) - 1):
            p1 = self.points[i]
            p2 = self.points[i + 1]
            
            # Calculate the distance from the point to the line segment
            dx = p2.x() - p1.x()
            dy = p2.y() - p1.y()
            length = (dx * dx + dy * dy) ** 0.5
            
            if length < 0.1:  # Avoid division by zero
                # If the line segment is very short, just check the distance to the point
                if ((point.x() - p1.x()) ** 2 + (point.y() - p1.y()) ** 2) ** 0.5 <= self.line_thickness + 5:
                    return True
                continue
                
            # Calculate the distance from the point to the line segment
            t = max(0, min(1, ((point.x() - p1.x()) * dx + (point.y() - p1.y()) * dy) / (length * length)))
            proj_x = p1.x() + t * dx
            proj_y = p1.y() + t * dy
            dist = ((point.x() - proj_x) ** 2 + (point.y() - proj_y) ** 2) ** 0.5
            
            if dist <= self.line_thickness + 5:
                return True
                
        return False
        
    def move(self, dx, dy):
        """Move the polyline by the specified delta."""
        for i in range(len(self.points)):
            self.points[i] += QPointF(dx, dy)
            
    def get_bounding_rect(self):
        """Get the bounding rectangle of the polyline."""
        if not self.points:
            return QRectF()
            
        # Calculate the bounding rectangle
        min_x = min(p.x() for p in self.points)
        min_y = min(p.y() for p in self.points)
        max_x = max(p.x() for p in self.points)
        max_y = max(p.y() for p in self.points)
        
        # Add padding for line thickness
        padding = self.line_thickness + 5
        return QRectF(min_x - padding, min_y - padding, 
                      max_x - min_x + 2 * padding, max_y - min_y + 2 * padding)
