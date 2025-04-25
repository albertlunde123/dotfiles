# pyqt_drawing_app/tools/freehand_tool.py
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt, QPoint
from pyqt_drawing_app.tools.base_tool import BaseTool
# from pyqt_drawing_app.canvas_widget import LineElement

class FreehandTool(BaseTool):
    def __init__(self, line_color):
        super().__init__()
        self.line_color = line_color
        self.drawing = False
        self.lastPoint = None
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()
    
    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton and self.drawing:
            currentPoint = event.pos()
            # Add a line element to the canvas
            # self.canvas.add_element(LineElement(self.lastPoint, currentPoint, self.line_color))
            self.lastPoint = currentPoint
            self.canvas.update()
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False
    
    def draw(self, painter):
        # No temporary elements to draw
        pass
