# pyqt_drawing_app/elements/circle_element.py
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import QPointF, QRectF, Qt
from .base_element import DrawingElement

class CircleElement(DrawingElement):
    """A circle element defined by center point and radius"""
    def __init__(self, center, radius, color):
        super().__init__("circle", color)
        self.center = QPointF(center)
        self.radius = radius
        self.snap_points = [self.center]

    def _draw_shape(self, painter: QPainter):
        rect = QRectF(
            self.center.x() - self.radius, self.center.y() - self.radius,
            self.radius * 2, self.radius * 2
        )
        painter.drawEllipse(rect)

    def _draw_handles(self, painter: QPainter):
        painter.drawEllipse(self.center, self.handle_size, self.handle_size)

    def contains_point(self, point: QPointF) -> bool:
        # (Keep existing logic)
        distance = ((point.x() - self.center.x()) ** 2 +
                   (point.y() - self.center.y()) ** 2) ** 0.5
        tolerance = 5 + self.line_thickness / 2
        return abs(distance - self.radius) < tolerance

    def move(self, dx: float, dy: float):
        self.center += QPointF(dx, dy)
        self.snap_points = [self.center]
