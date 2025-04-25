from PyQt5.QtWidgets import QToolBar, QAction, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor

class ToolToolbar(QToolBar):
    def __init__(self, tool_controller, parent=None):
        super().__init__("Drawing Tools", parent)
        self.tool_controller = tool_controller
        self.setMovable(False)  # Make toolbar immovable
        self._setup_tool_buttons()
        # self.tool_controller.tool_changed.connect(self._on_tool_selected)
    
    def _setup_tool_buttons(self):
        """Create buttons for each tool"""
        # Create a widget to hold the tools vertically
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(2)
        layout.setAlignment(Qt.AlignTop)
        
        # Tool buttons
        tools = self.tool_controller.get_all_tools()
        self.tool_actions = {}
        
        for tool_name in tools:
            action = QAction(tool_name.capitalize(), self)
            action.setCheckable(True)
            action.triggered.connect(lambda checked, tn=tool_name: self._on_tool_selected(tn))
            # Set a fixed width for the action
            action.setProperty("tool_button", True)
            self.addAction(action)
            self.tool_actions[tool_name] = action
        
        # Add perpendicular mode toggle for line tool
        self.addSeparator()
        self.perp_mode_action = QAction("Perpendicular Mode", self)
        self.perp_mode_action.setCheckable(True)
        self.perp_mode_action.triggered.connect(self._toggle_perpendicular_mode)
        self.addAction(self.perp_mode_action)
        
        # Set the container as the toolbar's widget
        self.addWidget(container)
        
        # Apply custom styling
        self.setStyleSheet("""
            QToolBar {
                border: none;
                background: transparent;
            }
            QToolButton {
                border: 1px solid #888;
                border-radius: 3px;
                padding: 5px;
                margin: 1px;
                text-align: left;
                min-width: 100px;
            }
            QToolButton:hover {
                background-color: #f0f0f0;
            }
            QToolButton:checked {
                background-color: #e0e0e0;
                border: 1px solid #666;
            }
        """)
    
    def _on_tool_selected(self, tool_name):
        """Handle tool selection"""
        # Update checked state
        for name, action in self.tool_actions.items():
            action.setChecked(name == tool_name)
        
        # Activate the tool
        self.tool_controller.set_active_tool(tool_name)
    
    def _toggle_perpendicular_mode(self):
        """Toggle perpendicular mode on the line tool"""
        self.tool_controller.toggle_perpendicular_mode()
        
        # If perpendicular mode is enabled, make sure line tool is active
        if self.perp_mode_action.isChecked():
            self.tool_controller.set_active_tool('line')
            self._on_tool_selected('line')
