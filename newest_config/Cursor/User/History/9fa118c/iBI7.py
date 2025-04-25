# pyqt_drawing_app/views/element_properties_dock.py
import math
from PyQt5.QtWidgets import (
    QDockWidget, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QDoubleSpinBox, QSpacerItem, QSizePolicy, QColorDialog, QComboBox, QFrame,
    QToolButton, QSpinBox, QCheckBox, QGroupBox, QGridLayout
)
from PyQt5.QtGui import QColor, QPalette, QBrush, QIcon, QPainter, QPen, QConicalGradient
from PyQt5.QtCore import Qt, pyqtSignal, QSize, QRect, QPoint
# Import base element to access constants
from pyqt_drawing_app.elements import DrawingElement

class ColorSchemeButton(QPushButton):
    colorChanged = pyqtSignal(QColor)
    def __init__(self, color, parent=None):
        super().__init__(parent)
        self._color = QColor(color)
        self.setFixedSize(24, 24)
        self._update_button_color()
        self.clicked.connect(self._on_click)
        
    def _on_click(self):
        self.colorChanged.emit(self._color)
        
    def set_color(self, color: QColor):
        if isinstance(color, QColor) and color.isValid():
            self._color = QColor(color)
            self._update_button_color()
            
    def _update_button_color(self):
        if self._color.isValid():
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {self._color.name()};
                    border: 1px solid #414868;
                    border-radius: 3px;
                }}
                QPushButton:hover {{
                    border: 1px solid #7aa2f7;
                }}
            """)

class ColorWheel(QWidget):
    colorChanged = pyqtSignal(QColor)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(100, 100)
        self.setMinimumSize(100, 100)
        self._current_color = QColor(255, 0, 0)  # Default to red
        self._is_dragging = False
        self._center = QPoint(50, 50)
        self._radius = 40
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw the color wheel
        gradient = QConicalGradient(self._center, 0)
        for i in range(360):
            color = QColor.fromHsv(i, 255, 255)
            gradient.setColorAt(i / 360.0, color)
        
        painter.setBrush(gradient)
        painter.setPen(QPen(QColor("#414868"), 1))
        painter.drawEllipse(self._center, self._radius, self._radius)
        
        # Draw the current color indicator
        painter.setPen(QPen(Qt.black, 1))
        painter.setBrush(self._current_color)
        painter.drawEllipse(self._center, 5, 5)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._is_dragging = True
            self._update_color(event.pos())
            
    def mouseMoveEvent(self, event):
        if self._is_dragging:
            self._update_color(event.pos())
            
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._is_dragging = False
            
    def _update_color(self, pos):
        # Calculate angle and distance from center
        dx = pos.x() - self._center.x()
        dy = pos.y() - self._center.y()
        distance = (dx*dx + dy*dy)**0.5
        
        if distance <= self._radius:
            # Calculate hue based on angle
            angle = (math.atan2(dy, dx) * 180 / math.pi + 180) % 360
            # Calculate saturation based on distance from center
            saturation = min(255, int(255 * distance / self._radius))
            
            self._current_color = QColor.fromHsv(int(angle), saturation, 255)
            self.colorChanged.emit(self._current_color)
            self.update()
            
    def set_color(self, color):
        if color.isValid():
            self._current_color = color
            self.update()

class ElementPropertiesDock(QDockWidget):
    """Dock widget for editing selected element properties."""
    propertyColorChanged = pyqtSignal(QColor)
    propertyThicknessChanged = pyqtSignal(float)
    # --- New Signals ---
    propertyDashPatternChanged = pyqtSignal(str) # Emits the pattern key (e.g., "Solid")
    propertyStartArrowChanged = pyqtSignal(str) # Emits the arrowhead type (e.g., "None")
    propertyEndArrowChanged = pyqtSignal(str) # Emits the arrowhead type
    # ---

    # Tokyo Night color scheme
    COLOR_SCHEME = [
        "#f7768e", "#ff9e64", "#e0af68", "#9ece6a",
        "#73c048", "#41a6b5", "#7aa2f7", "#bb9af7",
        "#ad8ee6", "#c0caf5", "#a9b1d6", "#414868"
    ]

    def __init__(self, parent=None):
        super().__init__("Element Properties", parent)
        # ... (basic setup: setAllowedAreas, setFeatures, setObjectName) ...
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetClosable)
        self.setObjectName("ElementPropertiesDock")
        
        # Create a custom title bar with close button
        self.title_bar = QWidget()
        title_layout = QHBoxLayout(self.title_bar)
        title_layout.setContentsMargins(5, 2, 5, 2)
        
        # Title label
        title_label = QLabel("Element Properties")
        title_label.setStyleSheet("font-weight: bold;")
        title_layout.addWidget(title_label)
        
        # Spacer
        title_layout.addStretch()
        
        # Close button
        close_button = QToolButton()
        close_button.setText("×")
        close_button.setStyleSheet("""
            QToolButton {
                border: none;
                background: transparent;
                font-size: 16px;
                color: #565f89;
            }
            QToolButton:hover {
                color: #7aa2f7;
            }
        """)
        close_button.clicked.connect(self.close)
        title_layout.addWidget(close_button)
        
        # Set the title bar
        self.setTitleBarWidget(self.title_bar)

        # Create a frame to hold the content
        self.frame = QFrame()
        self.frame.setFrameStyle(QFrame.Box | QFrame.Raised)
        self.frame.setLineWidth(1)
        self.frame_layout = QVBoxLayout(self.frame)
        self.frame_layout.setContentsMargins(10, 10, 10, 10)
        self.frame_layout.setSpacing(15)
        
        # --- Color ---
        color_group = QGroupBox("Color")
        color_layout = QVBoxLayout()
        
        # Color scheme grid
        color_grid = QGridLayout()
        color_grid.setSpacing(4)
        self.color_buttons = []
        
        for i, color in enumerate(self.COLOR_SCHEME):
            btn = ColorSchemeButton(color)
            btn.colorChanged.connect(self.propertyColorChanged.emit)
            self.color_buttons.append(btn)
            color_grid.addWidget(btn, i // 4, i % 4)
            
        color_layout.addLayout(color_grid)
        
        # Color wheel
        wheel_layout = QHBoxLayout()
        wheel_layout.addStretch()
        self.color_wheel = ColorWheel()
        self.color_wheel.colorChanged.connect(self.propertyColorChanged.emit)
        wheel_layout.addWidget(self.color_wheel)
        wheel_layout.addStretch()
        
        color_layout.addLayout(wheel_layout)
        color_group.setLayout(color_layout)
        self.frame_layout.addWidget(color_group)

        # --- Line Thickness ---
        thickness_layout = QHBoxLayout()
        thickness_label = QLabel("Thickness:")
        self.thickness_spinbox = QDoubleSpinBox()
        self.thickness_spinbox.setRange(0.0, 50.0)
        self.thickness_spinbox.setDecimals(1)
        self.thickness_spinbox.setSingleStep(0.5)
        self.thickness_spinbox.valueChanged.connect(self.propertyThicknessChanged.emit)
        thickness_layout.addWidget(thickness_label)
        thickness_layout.addWidget(self.thickness_spinbox)
        self.frame_layout.addLayout(thickness_layout)

        # --- Dash Pattern ---
        dash_layout = QHBoxLayout()
        dash_label = QLabel("Line Style:")
        self.dash_combo = QComboBox()
        # Populate with keys from DrawingElement
        self.dash_combo.addItems(DrawingElement.DASH_PATTERNS.keys())
        self.dash_combo.currentTextChanged.connect(self.propertyDashPatternChanged.emit)
        dash_layout.addWidget(dash_label)
        dash_layout.addWidget(self.dash_combo)
        self.frame_layout.addLayout(dash_layout)

        # --- Arrow Controls ---
        arrow_group = QGroupBox("Arrows")
        arrow_group_layout = QHBoxLayout()
        
        # Start/End checkboxes
        self.start_checkbox = QCheckBox("Start")
        self.end_checkbox = QCheckBox("End")
        self.start_checkbox.stateChanged.connect(lambda state: self._on_checkbox_changed("start", state))
        self.end_checkbox.stateChanged.connect(lambda state: self._on_checkbox_changed("end", state))
        arrow_group_layout.addWidget(self.start_checkbox)
        arrow_group_layout.addWidget(self.end_checkbox)
        arrow_group_layout.addStretch()
        
        arrow_group.setLayout(arrow_group_layout)
        self.frame_layout.addWidget(arrow_group)

        # --- Spacer ---
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.frame_layout.addItem(spacer)

        # Set the frame as the dock's widget
        self.setWidget(self.frame)
        self.setEnabled(False)
        
        # Apply custom styling
        self.setStyleSheet("""
            QDockWidget {
                border: none;
                background: transparent;
            }
            QFrame {
                background-color: #1a1b26;
                border-radius: 5px;
                border: 2px solid #414868;
            }
            QLabel {
                color: #c0caf5;
            }
            QPushButton, QComboBox, QDoubleSpinBox {
                border: 1px solid #414868;
                border-radius: 3px;
                padding: 3px;
                background-color: #1a1b26;
                color: #c0caf5;
            }
            QPushButton:hover, QComboBox:hover, QDoubleSpinBox:hover {
                border: 1px solid #7aa2f7;
                background-color: #24283b;
                color: #7aa2f7;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border: none;
            }
            QToolButton {
                border: none;
                background: transparent;
                font-size: 16px;
                color: #565f89;
            }
            QToolButton:hover {
                color: #7aa2f7;
            }
            QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {
                background-color: #24283b;
                border: 1px solid #414868;
            }
            QDoubleSpinBox::up-button:hover, QDoubleSpinBox::down-button:hover {
                background-color: #414868;
                border: 1px solid #7aa2f7;
            }
            QComboBox:focus, QDoubleSpinBox:focus {
                border: 1px solid #7aa2f7;
            }
            QDockWidget:enabled QLabel {
                color: #c0caf5;
            }
            QDockWidget:disabled QLabel {
                color: #c0caf5;
            }
            QCheckBox {
                color: #c0caf5;
                spacing: 5px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
            }
            QCheckBox::indicator:unchecked {
                border: 1px solid #414868;
                background-color: #24283b;
                border-radius: 3px;
            }
            QCheckBox::indicator:checked {
                border: 1px solid #7aa2f7;
                background-color: #7aa2f7;
                border-radius: 3px;
            }
            QCheckBox::indicator:hover {
                border: 1px solid #7aa2f7;
            }
            QGroupBox {
                border: 1px solid #414868;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
                color: #c0caf5;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 5px;
            }
        """)

    def update_properties(self, elements: list):
        """Update the properties panel based on selected elements."""
        if not elements:
            self.setEnabled(False)
            return
            
        self.setEnabled(True)
        
        # Get the first element's properties
        element = elements[0]
        
        # Update color wheel only (not the buttons)
        current_color = element.color
        self.color_wheel.set_color(current_color)
            
        # Update thickness
        self.thickness_spinbox.setValue(element.line_thickness)
        
        # Update dash pattern
        current_pattern = element.dash_pattern
        index = self.dash_combo.findText(current_pattern)
        if index >= 0:
            self.dash_combo.setCurrentIndex(index)
            
        # Update arrow checkboxes
        self.start_checkbox.setChecked(element.start_arrowhead != DrawingElement.ARROWHEAD_NONE)
        self.end_checkbox.setChecked(element.end_arrowhead != DrawingElement.ARROWHEAD_NONE)

    def _on_checkbox_changed(self, side, state):
        # Emit signals for checkbox changes
        if side == "start":
            self.propertyStartArrowChanged.emit("Arrow" if state == Qt.Checked else "None")
        else:  # end
            self.propertyEndArrowChanged.emit("Arrow" if state == Qt.Checked else "None")

