# pyqt_drawing_app/elements/rectangle_element.py
from PyQt5.QtGui import QPainter, QBrush, QPen, QTransform
from PyQt5.QtCore import QPointF, QRectF, Qt
from .base_element import DrawingElement
import math

class RectangleElement(DrawingElement):
    """A rectangle element defined by two corner points"""
    def __init__(self, corner1, corner2, color):
        super().__init__("rectangle", color)
        self.corner1 = QPointF(corner1)
        self.corner2 = QPointF(corner2)
        self.rotation_angle = 0  # Angle in degrees
        self.rotation_center = None  # Will be calculated in _update_normalized_rect
        self._update_normalized_rect()

    def find_snap_points(self):
        # Get the corners in the rotated coordinate system
        x1, y1 = self.corner1.x(), self.corner1.y()
        x2, y2 = self.corner2.x(), self.corner2.y()
        min_x, max_x = min(x1, x2), max(x1, x2)
        min_y, max_y = min(y1, y2), max(y1, y2)
        corners = [
            QPointF(min_x, min_y), QPointF(max_x, min_y),
            QPointF(min_x, max_y), QPointF(max_x, max_y)
        ]
        
        # Apply rotation transform to corners
        if self.rotation_angle != 0 and self.rotation_center:
            transform = QTransform()
            transform.translate(self.rotation_center.x(), self.rotation_center.y())
            transform.rotate(self.rotation_angle)
            transform.translate(-self.rotation_center.x(), -self.rotation_center.y())
            corners = [transform.map(corner) for corner in corners]
        
        return corners

    def _update_normalized_rect(self):
        x1, y1 = self.corner1.x(), self.corner1.y()
        x2, y2 = self.corner2.x(), self.corner2.y()
        self.rect = QRectF(
            min(x1, x2), min(y1, y2),
            abs(x2 - x1), abs(y2 - y1)
        )
        # Update rotation center to be the center of the rectangle
        self.rotation_center = QPointF(
            self.rect.center().x(),
            self.rect.center().y()
        )
        self.snap_points = self.find_snap_points()

    def _draw_shape(self, painter: QPainter):
        painter.save()
        if self.rotation_angle != 0 and self.rotation_center:
            # Apply rotation transform
            painter.translate(self.rotation_center.x(), self.rotation_center.y())
            painter.rotate(self.rotation_angle)
            painter.translate(-self.rotation_center.x(), -self.rotation_center.y())
        
        painter.drawRect(self.rect)
        painter.restore()

    def _draw_handles(self, painter: QPainter):
        # Draw corner handles
        for point in self.snap_points:
            painter.drawEllipse(point, self.handle_size, self.handle_size)
        
        # Draw rotation handle and circle when selected
        if self.selected and self.rotation_center:
            # Calculate radius based on rectangle size
            radius = math.sqrt(self.rect.width()**2 + self.rect.height()**2) / 2 + 20
            
            # Draw the rotation circle
            painter.save()
            # Clear any brush to avoid filling
            painter.setBrush(Qt.NoBrush)
            rotation_pen = QPen(self.color, 1, Qt.DashLine)
            painter.setPen(rotation_pen)
            painter.drawEllipse(self.rotation_center, radius, radius)
            
            # Draw the rotation handle with solid fill
            handle_angle = math.radians(self.rotation_angle - 90)  # Position handle at top
            handle_x = self.rotation_center.x() + radius * math.cos(handle_angle)
            handle_y = self.rotation_center.y() + radius * math.sin(handle_angle)
            handle_point = QPointF(handle_x, handle_y)
            
            # Draw handle point with solid fill
            painter.setPen(QPen(self.color, 1, Qt.SolidLine))
            painter.setBrush(QBrush(self.color))
            painter.drawEllipse(handle_point, self.handle_size, self.handle_size)
            
            # Draw a line from center to handle for better visibility
            painter.setPen(QPen(self.color, 1, Qt.DashLine))
            painter.drawLine(self.rotation_center, handle_point)
            
            painter.restore()

    def contains_point(self, point: QPointF) -> bool:
        if self.rotation_angle == 0:
            # Use existing logic for unrotated rectangles
            x, y = point.x(), point.y()
            left, right = self.rect.left(), self.rect.right()
            top, bottom = self.rect.top(), self.rect.bottom()
            tolerance = 5 + self.line_thickness / 2
            on_horizontal = (x >= left - tolerance and x <= right + tolerance and
                           (abs(y - top) <= tolerance or abs(y - bottom) <= tolerance))
            on_vertical = (y >= top - tolerance and y <= bottom + tolerance and
                         (abs(x - left) <= tolerance or abs(x - right) <= tolerance))
            return on_horizontal or on_vertical
        else:
            # For rotated rectangles, transform the test point back to unrotated coordinates
            transform = QTransform()
            transform.translate(self.rotation_center.x(), self.rotation_center.y())
            transform.rotate(-self.rotation_angle)  # Note the negative angle
            transform.translate(-self.rotation_center.x(), -self.rotation_center.y())
            unrotated_point = transform.map(point)
            
            # Now test against the unrotated rectangle
            x, y = unrotated_point.x(), unrotated_point.y()
            left, right = self.rect.left(), self.rect.right()
            top, bottom = self.rect.top(), self.rect.bottom()
            tolerance = 5 + self.line_thickness / 2
            on_horizontal = (x >= left - tolerance and x <= right + tolerance and
                           (abs(y - top) <= tolerance or abs(y - bottom) <= tolerance))
            on_vertical = (y >= top - tolerance and y <= bottom + tolerance and
                         (abs(x - left) <= tolerance or abs(x - right) <= tolerance))
            return on_horizontal or on_vertical

    def move(self, dx: float, dy: float):
        delta = QPointF(dx, dy)
        self.corner1 += delta
        self.corner2 += delta
        if self.rotation_center:
            self.rotation_center += delta
        self._update_normalized_rect()

    def rotate(self, angle: float):
        """Rotate the rectangle by the specified angle in degrees."""
        self.rotation_angle = angle % 360
        self.snap_points = self.find_snap_points()

    def get_rotation_handle_point(self) -> QPointF:
        """Get the current position of the rotation handle."""
        if not self.rotation_center:
            return None
        radius = math.sqrt(self.rect.width()**2 + self.rect.height()**2) / 2 + 20
        handle_angle = math.radians(self.rotation_angle - 90)  # Position handle at top
        handle_x = self.rotation_center.x() + radius * math.cos(handle_angle)
        handle_y = self.rotation_center.y() + radius * math.sin(handle_angle)
        return QPointF(handle_x, handle_y)

    def is_rotation_handle(self, point: QPointF) -> bool:
        """Check if the given point is near the rotation handle."""
        if not self.selected or not self.rotation_center:
            return False
        handle_point = self.get_rotation_handle_point()
        if not handle_point:
            return False
        dx = point.x() - handle_point.x()
        dy = point.y() - handle_point.y()
        distance_sq = dx * dx + dy * dy
        return distance_sq <= (self.handle_size + 5) ** 2
