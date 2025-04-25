from PyQt5.QtGui import QColor, QIcon, QPixmap
from PyQt5.QtWidgets import QAction
from PyQt5.QtCore import QObject, pyqtSignal

class ColorController(QObject):
    color_changed = pyqtSignal(QColor)
    
    def __init__(self, canvas, tool_controller):
        super().__init__()
        self.canvas = canvas
        self.tool_controller = tool_controller
        self.color_palette = self._load_color_palette()
        self.active_color = self.color_palette[0] if self.color_palette else QColor("#000000")
        
        # Configure initial settings with hardcoded values
        self.preview_opacity = 128
        self._configure_default_settings()
    
    def _configure_default_settings(self):
        """Set default visual settings"""
        from pyqt_drawing_app.utils.snapping import set_snap_colors
        from pyqt_drawing_app.utils.colors import get_snap_colors
        
        # Set default snap colors
        snap_color, fill_color = get_snap_colors()
        set_snap_colors(snap_color, fill_color)
    
    def _load_color_palette(self):
        """Load colors from pywal or use defaults"""
        from pyqt_drawing_app.utils.colors import load_pywal_colors, get_color_palette
        
        colors = load_pywal_colors()
        if colors:
            return get_color_palette(colors)
        else:
            print("pywal colors not found")
            # Fallback colors if pywal isn't available
            return [
                QColor("#000000"),  # Black
                QColor("#ff0000"),  # Red
                QColor("#00ff00"),  # Green
                QColor("#0000ff"),  # Blue
                QColor("#ffff00"),  # Yellow
                QColor("#ff00ff"),  # Magenta
                QColor("#00ffff"),  # Cyan
                QColor("#ffffff"),  # White
            ]
    
    def set_active_color(self, color):
        """Set the active color for drawing"""
        self.active_color = color
        self.canvas.line_color = color
        self.tool_controller.update_tool_colors(color)
        self.canvas.update()
        self.color_changed.emit(color)
    
    def get_color_palette(self):
        """Get the full color palette"""
        return self.color_palette
    
    def _create_color_icon(self, color):
        """Create a colored icon for the menu"""
        from PyQt5.QtGui import QPixmap, QPainter, QIcon
        
        # Create a pixmap
        pixmap = QPixmap(16, 16)
        pixmap.fill(color)
        
        # Create and return a QIcon from the pixmap
        return QIcon(pixmap)
        
    def setup_menu(self, menu_bar):
        """Set up the Colors menu"""
        color_menu = menu_bar.addMenu("Colors")
        
        # Add color selection actions
        for i, color in enumerate(self.color_palette):
            action = QAction(f"Color {i+1}", menu_bar.parent())
            action.setToolTip(f"Set active color to {color.name()}")
            action.setIcon(self._create_color_icon(color))
            action.triggered.connect(lambda checked, c=color: self.set_active_color(c))
            color_menu.addAction(action)
