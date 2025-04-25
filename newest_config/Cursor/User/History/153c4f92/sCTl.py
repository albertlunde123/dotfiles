# pyqt_drawing_app/elements/polyline_element.py
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import QPointF, Qt
from .base_element import DrawingElement
import math

class PolylineElement(DrawingElement):
    """A polyline element defined by a sequence of connected points"""
    def __init__(self, points, color):
        super().__init__("polyline", color)
        self.points = [QPointF(p) for p in points]
        self.snap_points = self.points

    def _draw_arrowhead(self, painter: QPainter, tip: QPointF, base: QPointF):
        """Draws a standard arrowhead at the tip point, pointing from base."""
        if tip == base: return # Cannot draw arrowhead for zero length segment

        # Use a solid pen for the arrowhead regardless of line style
        arrow_pen = QPen(self.color, max(1, self.line_thickness), Qt.SolidLine)
        arrow_pen.setCapStyle(Qt.RoundCap)
        arrow_pen.setJoinStyle(Qt.RoundJoin)
        painter.setPen(arrow_pen)
        painter.setBrush(self.color) # Fill the arrowhead

        vec = base - tip # Vector pointing from tip towards base
        length = math.sqrt(vec.x()**2 + vec.y()**2)
        if length < 1e-6: return # Avoid division by zero

        # Normalize vector
        norm_vec = vec / length

        # Calculate arrowhead wing points by rotating the normalized vector
        angle = math.radians(25) # Arrowhead angle
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)

        # Rotation matrix components for +angle and -angle
        p1_x = norm_vec.x() * cos_a - norm_vec.y() * sin_a
        p1_y = norm_vec.x() * sin_a + norm_vec.y() * cos_a

        p2_x = norm_vec.x() * cos_a + norm_vec.y() * sin_a
        p2_y = -norm_vec.x() * sin_a + norm_vec.y() * cos_a

        # Scale wing vectors by arrowhead size
        wing1 = QPointF(p1_x, p1_y) * self.arrowhead_size
        wing2 = QPointF(p2_x, p2_y) * self.arrowhead_size

        # Arrowhead polygon points (relative to tip)
        arrow_p1 = tip + wing1
        arrow_p2 = tip + wing2

        # Draw filled polygon
        painter.drawPolygon(tip, arrow_p1, arrow_p2)

        # Restore brush for subsequent lines if needed (base draw sets NoBrush)
        painter.setBrush(Qt.NoBrush)


    def _draw_shape(self, painter: QPainter):
        # Pen is already set by the base draw method (includes thickness/dash)
        if len(self.points) < 2: return

        for i in range(len(self.points) - 1):
            p1 = self.points[i]
            p2 = self.points[i+1]
            painter.drawLine(p1, p2)

            # Draw start arrowhead on the first segment
            if i == 0 and self.start_arrowhead == self.ARROWHEAD_STANDARD:
                self._draw_arrowhead(painter, p1, p2) # Tip is p1, pointing from p2

            # Draw end arrowhead on the last segment
            if i == len(self.points) - 2 and self.end_arrowhead == self.ARROWHEAD_STANDARD:
                self._draw_arrowhead(painter, p2, p1) # Tip is p2, pointing from p1

    def _draw_handles(self, painter: QPainter):
        for point in self.points:
            painter.drawEllipse(point, self.handle_size, self.handle_size)

    def contains_point(self, point: QPointF) -> bool:
        # (Keep existing logic)
        if len(self.points) < 2: return False
        for i in range(len(self.points) - 1):
            p1 = self.points[i]
            p2 = self.points[i+1]
            line_vec = p2 - p1
            point_vec = point - p1
            line_len_sq = line_vec.x()**2 + line_vec.y()**2
            if line_len_sq == 0:
                dist_sq = point_vec.x()**2 + point_vec.y()**2
            else:
                t = max(0, min(1, QPointF.dotProduct(point_vec, line_vec) / line_len_sq))
                projection = p1 + t * line_vec
                dist_sq = (point - projection).x()**2 + (point - projection).y()**2
            tolerance = (5 + self.line_thickness / 2) ** 2
            if dist_sq < tolerance:
                return True
        return False

    def move(self, dx: float, dy: float):
        delta = QPointF(dx, dy)
        self.points = [p + delta for p in self.points]
        self.snap_points = self.points
