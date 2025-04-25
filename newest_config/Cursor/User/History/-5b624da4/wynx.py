# pyqt_drawing_app/canvas_widget.py
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QBrush, QColor
from pyqt_drawing_app.utils.colors import load_pywal_colors
from pyqt_drawing_app.utils.grid import GridManager
from PyQt5.QtCore import Qt

class CanvasWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(800, 600)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.StrongFocus)  # Allow keyboard focus

        self.grid_manager = GridManager()
        
        # Load Pywal colors
        colors = load_pywal_colors()
        if colors:
            self.bg_color = QColor(colors.get("background", "#ffffff"))
            self.line_color = QColor(colors.get("foreground", "#000000"))
            grid_color = QColor(self.line_color)
            # grid_color.setAlpha(50)
            self.grid_manager.set_color(grid_color)
        else:
            self.bg_color = QColor("#ffffff")
            self.line_color = QColor("#000000")
            grid_color = QColor(self.line_color)
            self.grid_manager.set_color(grid_color)
        
        # Store all drawing elements
        self.elements = []
        
        # Active tool
        self.active_tool = None

        # --- Delegate Grid Methods ---
    def set_grid_visibility(self, visible: bool):
        """Sets the visibility of the grid via GridManager."""
        self.grid_manager.set_visibility(visible)
        self.update() # Trigger repaint

    def set_grid_snap(self, enabled: bool):
        """Sets grid snapping via GridManager."""
        self.grid_manager.set_snap_enabled(enabled)

    def set_grid_spacing(self, spacing: int):
        """Sets grid spacing via GridManager."""
        self.grid_manager.set_spacing(spacing)
        self.update() # Trigger repaint

    def toggle_grid_visibility(self):
        """Toggles the visibility and snapping of the grid."""
        # Get current state and toggle
        self.set_grid_visibility(not self.grid_manager.visible)
    # --- End Delegate Grid Methods ---
    
    def add_element(self, element):
        """Add a drawing element to the canvas"""
        self.elements.append(element)
        self.update()
    
    def clear_selection(self):
        """Clear selection state of all elements"""
        for element in self.elements:
            element.selected = False
        self.update()
    
    def get_selected_elements(self):
        """Get all currently selected elements"""
        return [element for element in self.elements if element.selected]
    
    def set_tool(self, tool):
        """Sets the active drawing tool"""
        if self.active_tool:
            self.active_tool.deactivate()
        self.active_tool = tool
        if self.active_tool:
            self.active_tool.activate(self)
        self.update()
    
    def mousePressEvent(self, event):
        if self.active_tool:
            self.active_tool.mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        if self.active_tool:
            self.active_tool.mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event):
        if self.active_tool:
            self.active_tool.mouseReleaseEvent(event)
    
    def keyPressEvent(self, event):
        if self.active_tool:
            self.active_tool.keyPressEvent(event)
        else:
            event.ignore()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QBrush(self.bg_color))
        
        # Draw all elements
        for element in self.elements:
            element.draw(painter)
        
        # Let the active tool draw any temporary elements
        if self.active_tool:
            self.active_tool.draw(painter)

        self.grid_manager.draw_grid(painter, self.width(), self.height())
