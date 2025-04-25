# pyqt_drawing_app/tools/base_tool.py
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget

class BaseTool:
    def __init__(self):
        self.canvas = None
    
    def activate(self, canvas):
        """Called when the tool is activated"""
        self.canvas = canvas
        # Make sure the canvas can receive keyboard events
        canvas.setFocusPolicy(Qt.StrongFocus)
        canvas.setFocus()
    
    def deactivate(self):
        """Called when the tool is deactivated"""
        self.canvas = None
    
    def mousePressEvent(self, event):
        """Handle mouse press events"""
        pass
    
    def mouseMoveEvent(self, event):
        """Handle mouse move events"""
        pass
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release events"""
        pass
    
    def keyPressEvent(self, event):
        """Placeholder for keyboard event handling"""
        event.ignore()  # Default behavior is to ignore the event
    
    def draw(self, painter):
        """Draw any temporary elements while the tool is active"""
        pass
