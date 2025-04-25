# pyqt_drawing_app/views/grid_settings_dock.py
from PyQt5.QtWidgets import (
    QDockWidget, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox,
    QCheckBox, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt, pyqtSignal

class GridSettingsDock(QDockWidget):
    # Signals to emit when settings change
    spacingChanged = pyqtSignal(int)
    visibilityChanged = pyqtSignal(bool)
    snapChanged = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__("Grid Settings", parent)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.setFeatures(QDockWidget.DockWidgetClosable | QDockWidget.DockWidgetMovable)

        # Main widget and layout
        self.main_widget = QWidget()
        self.layout = QVBoxLayout(self.main_widget)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)

        # --- Grid Spacing ---
        spacing_layout = QHBoxLayout()
        spacing_label = QLabel("Spacing (px):")
        self.spacing_spinbox = QSpinBox()
        self.spacing_spinbox.setRange(5, 500) # Example range
        self.spacing_spinbox.setSingleStep(5)
        self.spacing_spinbox.valueChanged.connect(self.spacingChanged.emit) # Emit signal
        spacing_layout.addWidget(spacing_label)
        spacing_layout.addWidget(self.spacing_spinbox)
        self.layout.addLayout(spacing_layout)

        # --- Visibility Checkbox ---
        self.visible_checkbox = QCheckBox("Grid Visible")
        self.visible_checkbox.toggled.connect(self.visibilityChanged.emit) # Emit signal
        self.layout.addWidget(self.visible_checkbox)

        # --- Snapping Checkbox ---
        self.snap_checkbox = QCheckBox("Snap to Grid")
        self.snap_checkbox.toggled.connect(self.snapChanged.emit) # Emit signal
        self.layout.addWidget(self.snap_checkbox)

        # --- Spacer ---
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout.addItem(spacer)

        self.setWidget(self.main_widget)

        # Apply custom styling
        self.setStyleSheet("""
            QDockWidget {
                border: none;
                background: transparent;
            }
            QFrame {
                background-color: #1a1b26;
                border-radius: 5px;
                border: 1px solid #24283b;
            }
            QLabel {
                color: #a9b1d6;
            }
            QCheckBox {
                color: #a9b1d6;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
            }
            QCheckBox::indicator:unchecked {
                border: 1px solid #24283b;
                background-color: #1a1b26;
            }
            QCheckBox::indicator:checked {
                border: 1px solid #7aa2f7;
                background-color: #24283b;
            }
            QCheckBox::indicator:hover {
                border: 1px solid #414868;
            }
            QSpinBox {
                border: 1px solid #24283b;
                border-radius: 3px;
                padding: 3px;
                background-color: #1a1b26;
                color: #a9b1d6;
            }
            QSpinBox:hover {
                border: 1px solid #414868;
                background-color: #24283b;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                background-color: #24283b;
                border: 1px solid #24283b;
            }
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {
                background-color: #414868;
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
        """)

    def set_initial_values(self, spacing: int, visible: bool, snap_enabled: bool):
        """Sets the initial state of the controls without emitting signals."""
        self.spacing_spinbox.blockSignals(True)
        self.visible_checkbox.blockSignals(True)
        self.snap_checkbox.blockSignals(True)

        self.spacing_spinbox.setValue(spacing)
        self.visible_checkbox.setChecked(visible)
        self.snap_checkbox.setChecked(snap_enabled)

        self.spacing_spinbox.blockSignals(False)
        self.visible_checkbox.blockSignals(False)
        self.snap_checkbox.blockSignals(False)

    def update_controls(self, visible: bool, snap_enabled: bool):
        """Updates checkboxes if state changes programmatically (e.g., toggle action)."""
        self.visible_checkbox.blockSignals(True)
        self.snap_checkbox.blockSignals(True)

        self.visible_checkbox.setChecked(visible)
        self.snap_checkbox.setChecked(snap_enabled)

        self.visible_checkbox.blockSignals(False)
        self.snap_checkbox.blockSignals(False)
