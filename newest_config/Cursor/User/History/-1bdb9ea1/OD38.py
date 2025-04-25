from PyQt5.QtCore import Qt, QPointF, QRectF
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush
from .base_element import DrawingElement
import math

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
        # Calculate the distance between points
        dx = self.end_point.x() - self.start_point.x()
        dy = self.end_point.y() - self.start_point.y()
        distance = (dx * dx + dy * dy) ** 0.5
        
        # Calculate the radius of each half-circle (1/4 of the total distance)
        radius = distance / 4
        
        # Calculate the center points for each half-circle
        # For the first half-circle (centered at 1/4 of the distance)
        center1_x = self.start_point.x() + dx / 4
        center1_y = self.start_point.y() + dy / 4
        
        # For the second half-circle (centered at 3/4 of the distance)
        center2_x = self.start_point.x() + 3 * dx / 4
        center2_y = self.start_point.y() + 3 * dy / 4
        
        # Calculate the angle between the line and the horizontal axis
        line_angle = math.atan2(dy, dx)
        
        # Store the control points
        self.control_points = [
            QPointF(center1_x, center1_y),  # Center of first half-circle
            QPointF(center2_x, center2_y),  # Center of second half-circle
            radius,  # Radius of both half-circles
            line_angle  # Angle between line and horizontal axis
        ]
        
    def _draw_shape(self, painter):
        """Draw the S-curve."""
        if not self.control_points:
            self._update_control_points()
            
        # Get the control points
        center1, center2, radius, line_angle = self.control_points
        
        # Convert line_angle from radians to degrees
        line_angle_deg = line_angle * 180 / math.pi
        
        # In Qt, angles are measured clockwise from 3 o'clock position
        # We need to adjust our calculations accordingly
        
        # Convert our mathematical angle to Qt's angle system
        qt_line_angle = 90 - line_angle_deg  # This converts from standard to Qt's system
        
        # Calculate the start and end angles for each arc in Qt's system
        # First half-circle
        start_angle1 = qt_line_angle - 90
        span_angle1 = 180  # Always positive for counterclockwise in Qt
        
        # Second half-circle
        start_angle2 = qt_line_angle + 90
        span_angle2 = 180  # Always positive for counterclockwise in Qt
        
        # Draw the first half-circle
        rect1 = QRectF(
            center1.x() - radius, 
            center1.y() - radius, 
            radius * 2, 
            radius * 2
        )
        painter.drawArc(rect1, int(start_angle1 * 16), int(span_angle1 * 16))
        
        # Draw the second half-circle
        rect2 = QRectF(
            center2.x() - radius, 
            center2.y() - radius, 
            radius * 2, 
            radius * 2
        )
        painter.drawArc(rect2, int(start_angle2 * 16), int(span_angle2 * 16))
        
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
        center1, center2, radius, line_angle = self.control_points
        
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
        center1, center2, radius, line_angle = self.control_points
        
        # Calculate the bounding rectangle
        left = min(center1.x() - radius, center2.x() - radius)
        top = min(center1.y() - radius, center2.y() - radius)
        right = max(center1.x() + radius, center2.x() + radius)
        bottom = max(center1.y() + radius, center2.y() + radius)
        
        return QRectF(left, top, right - left, bottom - top) 