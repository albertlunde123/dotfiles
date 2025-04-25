from PyQt5.QtWidgets import QToolBar, QPushButton, QWidget, QHBoxLayout, QFrame
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor

class ColorToolbar(QToolBar):
    colorSelected = pyqtSignal(QColor)
    
    def __init__(self, color_controller, parent=None):
        super().__init__("Color Palette", parent)
        self.color_controller = color_controller
        self.setMovable(False)  # Make toolbar immovable
        self.color_buttons = {}  # Store buttons to track selection
        self._setup_color_buttons()
        
        # Connect to color controller to update selection
        self.color_controller.color_changed.connect(self._update_selection)
    
    def _setup_color_buttons(self):
        """Create buttons for each color in the palette"""
        # Create a container widget with a frame
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(3)
        
        # Create a frame to hold the buttons
        frame = QFrame()
        frame.setFrameStyle(QFrame.Box | QFrame.Raised)
        frame.setLineWidth(1)
        frame_layout = QHBoxLayout(frame)
        frame_layout.setContentsMargins(5, 5, 5, 5)
        frame_layout.setSpacing(3)
        
        # Add color buttons to the frame
        for color in self.color_controller.get_color_palette():
            # Create a color button
            colorButton = QPushButton()
            colorButton.setFixedSize(24, 24)
            colorButton.setStyleSheet(f"background-color: {color.name()}; border: 1px solid #888;")
            colorButton.setToolTip(f"Set color to {color.name()}")
            colorButton.clicked.connect(lambda checked, c=color: self._on_color_selected(c))
            frame_layout.addWidget(colorButton)
            self.color_buttons[color.name()] = colorButton
        
        # Add the frame to the container
        layout.addWidget(frame)
        
        # Add the container to the toolbar
        self.addWidget(container)
        
        # Set the toolbar to the bottom left
        self.setAllowedAreas(Qt.BottomToolBarArea)
        
        # Apply custom styling
        self.setStyleSheet("""
            QToolBar {
                border: none;
                background: transparent;
            }
            QFrame {
                background-color: #f5f5f5;
                border-radius: 5px;
            }
            QPushButton {
                border-radius: 3px;
            }
            QPushButton:hover {
                border: 1px solid #000;
            }
        """)
    
    def _on_color_selected(self, color):
        """Handle color selection"""
        self.color_controller.set_active_color(color)
        self._update_selection(color)
        self.colorSelected.emit(color)
    
    def _update_selection(self, color=None):
        """Update the visual selection of the color buttons"""
        if color is None:
            color = self.color_controller.get_active_color()
            
        # Reset all buttons
        for btn in self.color_buttons.values():
            btn.setStyleSheet(btn.styleSheet().replace("border: 2px solid #000;", "border: 1px solid #888;"))
        
        # Highlight the selected color
        if color.name() in self.color_buttons:
            btn = self.color_buttons[color.name()]
            btn.setStyleSheet(btn.styleSheet().replace("border: 1px solid #888;", "border: 2px solid #000;"))
