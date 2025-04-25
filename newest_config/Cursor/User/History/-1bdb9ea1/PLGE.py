from PyQt5.QtCore import Qt, QPointF, QRectF
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush
from .base_element import DrawingElement

class SCurveElement(DrawingElement):
    """An S-curve element consisting of two connected half-circles."""
    
    def __init__(self, start_point, end_point, color=None):
        super().__init__("s_curve", color)
        self.start_point = QPointF(start_point)
        self.end_point = QPointF(end_point)
        self.control_points = []
        self._update_control_points()
        
    def _update_control_points(self):
        """Calculate the control points for the S-curve."""
        # Calculate the midpoint
        mid_x = (self.start_point.x() + self.end_point.x()) / 2
        mid_y = (self.start_point.y() + self.end_point.y()) / 2
        
        # Calculate the distance between points
        dx = self.end_point.x() - self.start_point.x()
        dy = self.end_point.y() - self.start_point.y()
        distance = (dx * dx + dy * dy) ** 0.5
        
        # Calculate the radius of each half-circle (half the distance)
        radius = distance / 2
        
        # Calculate the center points for each half-circle
        # For the first half-circle (from start to middle)
        center1_x = mid_x
        center1_y = mid_y
        
        # For the second half-circle (from middle to end)
        center2_x = mid_x
        center2_y = mid_y
        
        # Store the control points
        self.control_points = [
            QPointF(center1_x, center1_y),  # Center of first half-circle
            QPointF(center2_x, center2_y),  # Center of second half-circle
            radius  # Radius of both half-circles
        ]
        
    def _draw_shape(self, painter):
        """Draw the S-curve."""
        if not self.control_points:
            self._update_control_points()
            
        # Get the control points
        center1, center2, radius = self.control_points
        
        # Draw the first half-circle (top)
        painter.drawArc(
            QRectF(center1.x() - radius, center1.y() - radius, 
                   radius * 2, radius * 2),
            0 * 16, 180 * 16  # 0 to 180 degrees (top half)
        )
        
        # Draw the second half-circle (bottom)
        painter.drawArc(
            QRectF(center2.x() - radius, center2.y() - radius, 
                   radius * 2, radius * 2),
            180 * 16, 180 * 16  # 180 to 360 degrees (bottom half)
        )
        
    def _draw_handles(self, painter):
        """Draw handles for the S-curve."""
        # Draw handles at start and end points
        self._draw_point_handle(painter, self.start_point)
        self._draw_point_handle(painter, self.end_point)
        
    def contains_point(self, point):
        """Check if a point is within the S-curve."""
        if not self.control_points:
            self._update_control_points()
            
        # Get the control points
        center1, center2, radius = self.control_points
        
        # Check if the point is within either half-circle
        # For the first half-circle (top)
        dx1 = point.x() - center1.x()
        dy1 = point.y() - center1.y()
        dist1 = (dx1 * dx1 + dy1 * dy1) ** 0.5
        
        # For the second half-circle (bottom)
        dx2 = point.x() - center2.x()
        dy2 = point.y() - center2.y()
        dist2 = (dx2 * dx2 + dy2 * dy2) ** 0.5
        
        # Check if the point is within the radius of either half-circle
        # and in the correct half (top or bottom)
        if dist1 <= radius and point.y() <= center1.y():
            return True
        if dist2 <= radius and point.y() >= center2.y():
            return True
            
        return False
        
    def move(self, dx, dy):
        """Move the S-curve by the specified delta."""
        self.start_point += QPointF(dx, dy)
        self.end_point += QPointF(dx, dy)
        self._update_control_points()
        
    def get_bounding_rect(self):
        """Get the bounding rectangle of the S-curve."""
        if not self.control_points:
            self._update_control_points()
            
        # Get the control points
        center1, center2, radius = self.control_points
        
        # Calculate the bounding rectangle
        left = min(center1.x() - radius, center2.x() - radius)
        top = min(center1.y() - radius, center2.y() - radius)
        right = max(center1.x() + radius, center2.x() + radius)
        bottom = max(center1.y() + radius, center2.y() + radius)
        
        return QRectF(left, top, right - left, bottom - top) 