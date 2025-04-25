# pyqt_drawing_app/elements/latex_text_element.py
import os # Keep necessary imports if used within methods
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor
from PyQt5.QtCore import QPointF, QRectF, Qt
from PyQt5.QtSvg import QSvgRenderer
from .base_element import DrawingElement

class LatexTextElement(DrawingElement):
    """A LaTeX text element displayed on the canvas using SVG"""
    def __init__(self, position, latex_code, svg_renderer, color):
        super().__init__("latex_text", color)
        self.position = QPointF(position)
        self.latex_code = latex_code
        self.svg_renderer = svg_renderer
        self.scale_factor = 2.0
        self.line_width = 0
        self.selected_line_width = 2

    # Override the base draw method completely
    def draw(self, painter: QPainter):
        painter.save()
        try:
            painter.translate(self.position)
            painter.scale(self.scale_factor, self.scale_factor)
            default_size = self.svg_renderer.defaultSize()
            if not default_size.isEmpty():
                self.svg_renderer.render(painter, QRectF(0, 0, default_size.width(), default_size.height()))
            painter.restore() # Restore from translate/scale

            if self.selected:
                painter.save()
                painter.setPen(self.get_pen()) # Use base helper
                painter.setBrush(Qt.NoBrush)
                scaled_size = default_size * self.scale_factor
                rect = QRectF(
                    self.position.x(), self.position.y(),
                    scaled_size.width(), scaled_size.height()
                )
                painter.drawRect(rect)
                painter.restore()
        except Exception as e:
            print(f"Error drawing LaTeX element: {e}")
            # Consider more robust error handling if needed

    def contains_point(self, point: QPointF) -> bool:
        # (Keep existing logic)
        size = self.svg_renderer.defaultSize()
        if size.isEmpty():
            return False
            
        # Add some padding for easier selection
        padding = 5
        rect = QRectF(
            self.position.x() - padding, 
            self.position.y() - padding,
            size.width() * self.scale_factor + 2*padding, 
            size.height() * self.scale_factor + 2*padding
        )
        return rect.contains(point)

    def move(self, dx: float, dy: float):
        self.position += QPointF(dx, dy)

    # Implement abstract methods, even if unused by overridden draw
    def _draw_shape(self, painter: QPainter): pass
    def _draw_handles(self, painter: QPainter): pass
