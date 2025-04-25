# pyqt_drawing_app/views/element_properties_dock.py
from PyQt5.QtWidgets import (
    QDockWidget, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QDoubleSpinBox, QSpacerItem, QSizePolicy, QColorDialog, QComboBox, QFrame,
    QToolButton, QSpinBox, QCheckBox, QGroupBox, QGridLayout
)
from PyQt5.QtGui import QColor, QPalette, QBrush, QIcon
from PyQt5.QtCore import Qt, pyqtSignal, QSize
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

class ColorWheelButton(QPushButton):
    colorChanged = pyqtSignal(QColor)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(24, 24)
        self.setText("🎨")
        self.setStyleSheet("""
            QPushButton {
                background-color: #24283b;
                border: 1px solid #414868;
                border-radius: 3px;
                color: #c0caf5;
            }
            QPushButton:hover {
                border: 1px solid #7aa2f7;
                background-color: #414868;
            }
        """)
        self.clicked.connect(self._on_click)
        
    def _on_click(self):
        color = QColorDialog.getColor(QColor("black"), self, "Select Color")
        if color.isValid():
            self.colorChanged.emit(color)

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
        
        # Color wheel button
        wheel_layout = QHBoxLayout()
        wheel_layout.addStretch()
        self.color_wheel = ColorWheelButton()
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
                border: 1px solid #414868;
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
        """Updates the dock controls based on the selected elements."""
        if not elements:
            self.setEnabled(False)
            return

        self.setEnabled(True)

        # Get properties from the first element
        first = elements[0]
        initial_color = first.color
        initial_thickness = first.line_thickness
        initial_dash = first.dash_pattern_key
        initial_start_arrow = first.start_arrowhead
        initial_end_arrow = first.end_arrowhead

        # Check for multiple values and element type compatibility
        multi_colors = False
        multi_thicknesses = False
        multi_dash = False
        multi_start_arrow = False
        multi_end_arrow = False
        supports_styles = True # Assume support initially

        for el in elements[1:]:
            if el.color != initial_color: multi_colors = True
            if el.line_thickness != initial_thickness: multi_thicknesses = True
            # Check if element supports line styles (e.g., not LaTeX)
            if not hasattr(el, 'dash_pattern_key'):
                 supports_styles = False
                 continue # Skip style checks for this element
            if el.dash_pattern_key != initial_dash: multi_dash = True
            if el.start_arrowhead != initial_start_arrow: multi_start_arrow = True
            if el.end_arrowhead != initial_end_arrow: multi_end_arrow = True

        # Also check the first element for style support
        if not hasattr(first, 'dash_pattern_key'):
            supports_styles = False

        # Block signals
        self.color_buttons[0].blockSignals(True)
        self.color_buttons[1].blockSignals(True)
        self.color_buttons[2].blockSignals(True)
        self.color_buttons[3].blockSignals(True)
        self.color_buttons[4].blockSignals(True)
        self.color_buttons[5].blockSignals(True)
        self.color_buttons[6].blockSignals(True)
        self.color_buttons[7].blockSignals(True)
        self.color_buttons[8].blockSignals(True)
        self.color_buttons[9].blockSignals(True)
        self.color_buttons[10].blockSignals(True)
        self.color_buttons[11].blockSignals(True)
        self.thickness_spinbox.blockSignals(True)
        self.dash_combo.blockSignals(True)
        self.start_checkbox.blockSignals(True)
        self.end_checkbox.blockSignals(True)

        # Update controls
        for btn in self.color_buttons:
            btn.set_color(QColor() if multi_colors else initial_color)

        self.thickness_spinbox.setValue(initial_thickness)
        self.thickness_spinbox.setStyleSheet("background-color: lightyellow;" if multi_thicknesses else "")
        self.thickness_spinbox.setEnabled(supports_styles) # Disable for incompatible types

        self.dash_combo.setCurrentText(initial_dash if not multi_dash else "") # Empty string if multi
        self.dash_combo.setEnabled(supports_styles)
            
        # Set checkboxes based on arrow presence
        self.start_checkbox.setChecked(initial_start_arrow != "None")
        self.end_checkbox.setChecked(initial_end_arrow != "None")

        # Unblock signals
        self.color_buttons[0].blockSignals(False)
        self.color_buttons[1].blockSignals(False)
        self.color_buttons[2].blockSignals(False)
        self.color_buttons[3].blockSignals(False)
        self.color_buttons[4].blockSignals(False)
        self.color_buttons[5].blockSignals(False)
        self.color_buttons[6].blockSignals(False)
        self.color_buttons[7].blockSignals(False)
        self.color_buttons[8].blockSignals(False)
        self.color_buttons[9].blockSignals(False)
        self.color_buttons[10].blockSignals(False)
        self.color_buttons[11].blockSignals(False)
        self.thickness_spinbox.blockSignals(False)
        self.dash_combo.blockSignals(False)
        self.start_checkbox.blockSignals(False)
        self.end_checkbox.blockSignals(False)

    def _on_checkbox_changed(self, side, state):
        # Emit signals for checkbox changes
        if side == "start":
            self.propertyStartArrowChanged.emit("Arrow" if state == Qt.Checked else "None")
        else:  # end
            self.propertyEndArrowChanged.emit("Arrow" if state == Qt.Checked else "None")

