from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPainter, QPen, QColor
from .base_tool import BaseTool
from ..elements.latex_element import LatexElement
from ..utils.latex_renderer import LatexRenderer

class LatexTool(BaseTool):
    """Tool for adding LaTeX text to the canvas."""
    
    def __init__(self):
        super().__init__()
        self.position = None
        self.latex_code = ""
        self.preview_element = None
        self.drawing = False
        self.latex_renderer = LatexRenderer()
        
    def activate(self, canvas):
        super().activate(canvas)
        self._reset_state()
        
    def deactivate(self):
        self._reset_state()
        super().deactivate()
        
    def _reset_state(self):
        """Reset the tool's state."""
        self.position = None
        self.latex_code = ""
        self.preview_element = None
        self.drawing = False
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            pos = event.pos()
            
            # Set the position
            self.position = QPointF(pos)
            self.drawing = True
            
            # Prompt for LaTeX code
            from PyQt5.QtWidgets import QInputDialog
            latex_code, ok = QInputDialog.getText(
                self.canvas, "LaTeX Text", "Enter LaTeX code:",
                Qt.ImhFormattedTextOnly
            )
            
            if ok and latex_code:
                self.latex_code = latex_code
                self._create_element()
                
            self._reset_state()
            self.canvas.update()
            
    def mouseMoveEvent(self, event):
        if self.drawing and self.position:
            # Update the preview
            self.canvas.update()
            
    def draw(self, painter):
        """Draw the preview of the LaTeX text."""
        if self.drawing and self.position and self.latex_code:
            # Create a temporary element for preview
            if not self.preview_element:
                self.preview_element = LatexElement(
                    self.position, self.latex_code, self.latex_renderer, self.canvas.current_color
                )
            else:
                self.preview_element.position = self.position
                self.preview_element.latex_code = self.latex_code
                
            # Draw the preview
            self.preview_element.draw(painter)
            
    def _create_element(self):
        """Create the LaTeX element and add it to the canvas."""
        if self.position and self.latex_code:
            element = LatexElement(
                self.position, self.latex_code, self.latex_renderer, self.canvas.current_color
            )
            self.canvas.add_element(element) 