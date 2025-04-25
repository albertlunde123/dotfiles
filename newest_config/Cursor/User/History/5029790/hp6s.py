from PyQt5.QtCore import Qt, QPointF, QRectF
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush
from .base_element import DrawingElement

class LatexElement(DrawingElement):
    """An element for rendering LaTeX text on the canvas."""
    
    def __init__(self, position, latex_code, svg_renderer, color=None):
        super().__init__(color)
        self.position = QPointF(position)
        self.latex_code = latex_code
        self.svg_renderer = svg_renderer
        self.scale_factor = 1.0
        
    def _draw_shape(self, painter):
        """Draw the LaTeX text."""
        # Render the LaTeX text
        self.svg_renderer.render_latex(self.latex_code, self.color)
        
        # Get the size of the rendered SVG
        size = self.svg_renderer.defaultSize() * self.scale_factor
        
        # Draw the SVG at the specified position
        self.svg_renderer.render(painter, QRectF(self.position, size))
        
    def _draw_handles(self, painter):
        """Draw handles for the LaTeX text."""
        # Draw a handle at the position
        self._draw_point_handle(painter, self.position)
        
    def contains_point(self, point):
        """Check if a point is within the LaTeX text."""
        # Get the size of the rendered SVG
        size = self.svg_renderer.defaultSize() * self.scale_factor
        
        # Create a rectangle for the LaTeX text
        rect = QRectF(self.position, size)
        
        # Check if the point is within the rectangle
        return rect.contains(point)
        
    def move(self, dx, dy):
        """Move the LaTeX text by the specified delta."""
        self.position += QPointF(dx, dy)
        
    def get_bounding_rect(self):
        """Get the bounding rectangle of the LaTeX text."""
        # Get the size of the rendered SVG
        size = self.svg_renderer.defaultSize() * self.scale_factor
        
        # Create a rectangle for the LaTeX text
        return QRectF(self.position, size) 