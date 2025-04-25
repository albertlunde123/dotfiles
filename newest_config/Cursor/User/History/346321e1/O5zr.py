# pyqt_drawing_app/elements/base_element.py
from abc import ABC, abstractmethod
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen
from PyQt5.QtCore import Qt, QPointF, QRectF
from typing import Optional, List # Import Optional and List

class DrawingElement(ABC):
    """Base class for all drawing elements (lines, shapes, etc.)"""
    DEFAULT_LINE_THICKNESS = 2

    # Define constants for styles (can be expanded)
    SOLID_LINE = "Solid"
    DASHED_LINE = "Dashed"
    DOTTED_LINE = "Dotted"
    DASH_PATTERNS = {
        SOLID_LINE: None,
        DASHED_LINE: [4, 2], # 4 pixels on, 2 pixels off
        DOTTED_LINE: [1, 2], # 1 pixel on, 2 pixels off
    }

    ARROWHEAD_NONE = "None"
    ARROWHEAD_STANDARD = "Arrow"
    ARROWHEAD_DOUBLE = "Double Arrow"
    ARROWHEAD_DIAMOND = "Diamond"
    ARROWHEAD_CIRCLE = "Circle"
    ARROWHEAD_TYPES = [
        ARROWHEAD_NONE,
        ARROWHEAD_STANDARD,
        ARROWHEAD_DOUBLE,
        ARROWHEAD_DIAMOND,
        ARROWHEAD_CIRCLE
    ]

    def __init__(self, element_type, color):
        self.element_type = element_type
        self.color = QColor(color)
        self.selected = False
        # --- Style Properties ---
        self.line_thickness: float = self.DEFAULT_LINE_THICKNESS
        self.dash_pattern_key: str = self.SOLID_LINE # Store the key (e.g., "Solid")
        self.start_arrowhead: Optional[str] = self.ARROWHEAD_NONE
        self.end_arrowhead: Optional[str] = self.ARROWHEAD_NONE
        # ---
        self.selected_line_width_increase = 1
        self.handle_size = 3
        self.arrowhead_size = 10 # Default arrowhead size

    def get_pen(self) -> QPen:
        """Returns the appropriate QPen based on selection state and properties."""
        width = self.line_thickness
        style = Qt.SolidLine # Default style for selection dashes
        dash_pattern = self.DASH_PATTERNS.get(self.dash_pattern_key)

        if self.selected:
            width += self.selected_line_width_increase
            style = Qt.DashLine # Selection uses its own dash style
            # Don't apply element's dash pattern when selected for clarity
            dash_pattern = None
        else:
            # Use SolidLine style but apply dash pattern if specified
            style = Qt.SolidLine

        width = max(1, width) # Ensure minimum width
        pen = QPen(self.color, width, style)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)

        # Apply dash pattern if not selected and pattern exists
        if not self.selected and dash_pattern:
            pen.setDashPattern(dash_pattern)

        return pen

    # --- Property Setters ---
    def set_color(self, color: QColor):
        if self.color != color:
            self.color = QColor(color)

    def set_line_thickness(self, thickness: float):
        new_thickness = max(0, thickness)
        if self.line_thickness != new_thickness:
            self.line_thickness = new_thickness

    def set_dash_pattern(self, pattern_key: str):
        """Sets the dash pattern using a key from DASH_PATTERNS."""
        if pattern_key in self.DASH_PATTERNS and self.dash_pattern_key != pattern_key:
            self.dash_pattern_key = pattern_key

    def set_start_arrowhead(self, arrowhead_type: Optional[str]):
        """Sets the start arrowhead type."""
        if arrowhead_type in self.ARROWHEAD_TYPES and self.start_arrowhead != arrowhead_type:
            self.start_arrowhead = arrowhead_type

    def set_end_arrowhead(self, arrowhead_type: Optional[str]):
        """Sets the end arrowhead type."""
        if arrowhead_type in self.ARROWHEAD_TYPES and self.end_arrowhead != arrowhead_type:
            self.end_arrowhead = arrowhead_type

    # --- Abstract Methods & Base Draw ---
    # ... (get_handle_brush, get_handle_pen, _draw_shape, _draw_handles, draw,
    #      contains_point, move remain the same as before) ...
    def get_handle_brush(self) -> QBrush:
        return QBrush(self.color)
    def get_handle_pen(self) -> QPen:
         return QPen(self.color, 1, Qt.SolidLine)
    @abstractmethod
    def _draw_shape(self, painter: QPainter): pass
    @abstractmethod
    def _draw_handles(self, painter: QPainter): pass
    def draw(self, painter: QPainter):
        painter.save()
        try:
            painter.setPen(self.get_pen()) # Pen now includes thickness/dash
            painter.setBrush(Qt.NoBrush)
            self._draw_shape(painter) # Draws lines and potentially arrowheads
            if self.selected:
                 painter.setBrush(self.get_handle_brush())
                 painter.setPen(self.get_handle_pen())
                 self._draw_handles(painter)
        finally:
            painter.restore()
    @abstractmethod
    def contains_point(self, point: QPointF) -> bool: return False
    @abstractmethod
    def move(self, dx: float, dy: float): pass

