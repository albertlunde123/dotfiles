# pyqt_drawing_app/elements/rectangle_element.py
from PyQt5.QtGui import QPainter, QBrush
from PyQt5.QtCore import QPointF, QRectF, Qt
from .base_element import DrawingElement

class RectangleElement(DrawingElement):
    """A rectangle element defined by two corner points"""
    def __init__(self, corner1, corner2, color):
        super().__init__("rectangle", color)
        self.corner1 = QPointF(corner1)
        self.corner2 = QPointF(corner2)
        self._update_normalized_rect()

    def find_snap_points(self):
        # (Keep existing logic)
        x1, y1 = self.corner1.x(), self.corner1.y()
        x2, y2 = self.corner2.x(), self.corner2.y()
        min_x, max_x = min(x1, x2), max(x1, x2)
        min_y, max_y = min(y1, y2), max(y1, y2)
        return [
            QPointF(min_x, min_y), QPointF(max_x, min_y),
            QPointF(min_x, max_y), QPointF(max_x, max_y)
        ]

    def _update_normalized_rect(self):
        x1, y1 = self.corner1.x(), self.corner1.y()
        x2, y2 = self.corner2.x(), self.corner2.y()
        self.rect = QRectF(
            min(x1, x2), min(y1, y2),
            abs(x2 - x1), abs(y2 - y1)
        )
        self.snap_points = self.find_snap_points()

    def _draw_shape(self, painter: QPainter):
        painter.drawRect(self.rect)

    def _draw_handles(self, painter: QPainter):
        for point in self.snap_points:
             painter.drawEllipse(point, self.handle_size, self.handle_size)

    def contains_point(self, point: QPointF) -> bool:
        # (Keep existing logic)
        x, y = point.x(), point.y()
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
        self._update_normalized_rect()
