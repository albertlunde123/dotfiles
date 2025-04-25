from PyQt5.QtWidgets import QToolBar, QAction, QWidget, QVBoxLayout, QCheckBox, QToolButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor

class ToolToolbar(QToolBar):
    def __init__(self, tool_controller, parent=None):
        super().__init__("Tools", parent)
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
        self.tool_buttons = {}
        
        # Create main tool buttons
        for tool_name in ['select', 'line', 'rectangle', 'circle', 'freehand', 'latex']:
            button = QToolButton()
            button.setText(tool_name.capitalize())
            button.setToolButtonStyle(Qt.ToolButtonTextOnly)
            button.setCheckable(True)
            
            if tool_name == 'line':
                # Create line type buttons
                line_container = QWidget()
                line_layout = QVBoxLayout(line_container)
                line_layout.setContentsMargins(10, 0, 0, 0)  # Add left margin for indentation
                line_layout.setSpacing(1)
                
                # Create straight line button
                straight_button = QToolButton()
                straight_button.setText("Straight Line")
                straight_button.setToolButtonStyle(Qt.ToolButtonTextOnly)
                straight_button.setCheckable(True)
                straight_button.clicked.connect(lambda: self._on_line_type_selected('straight'))
                line_layout.addWidget(straight_button)
                self.tool_buttons['straight_line'] = straight_button
                
                # Create s-curve button
                scurve_button = QToolButton()
                scurve_button.setText("S Curve")
                scurve_button.setToolButtonStyle(Qt.ToolButtonTextOnly)
                scurve_button.setCheckable(True)
                scurve_button.clicked.connect(lambda: self._on_line_type_selected('scurve'))
                line_layout.addWidget(scurve_button)
                self.tool_buttons['s_curve'] = scurve_button
                
                # Add the main line button and container
                layout.addWidget(button)
                layout.addWidget(line_container)
                line_container.setVisible(False)  # Initially hide the line type options
                
                # Connect the main line button to show/hide type options
                button.clicked.connect(lambda checked: line_container.setVisible(checked))
            else:
                # For other tools, just add the button normally
                layout.addWidget(button)
            
            button.clicked.connect(lambda checked, tn=tool_name: self._on_tool_selected(tn))
            self.tool_buttons[tool_name] = button
        
        # Add perpendicular mode toggle for line tool
        self.addSeparator()
        self.perp_mode_action = QToolButton()
        self.perp_mode_action.setText("Perpendicular Mode")
        self.perp_mode_action.setToolButtonStyle(Qt.ToolButtonTextOnly)
        self.perp_mode_action.setCheckable(True)
        self.perp_mode_action.clicked.connect(self._toggle_perpendicular_mode)
        layout.addWidget(self.perp_mode_action)
        
        # Set the container as the toolbar's widget
        self.addWidget(container)
        
        # Apply custom styling
        self.setStyleSheet("""
            QToolBar {
                border: none;
                background: transparent;
            }
            QToolButton {
                border: 1px solid #414868;
                border-radius: 3px;
                padding: 5px;
                margin: 1px;
                text-align: left;
                min-width: 100px;
                background-color: #1a1b26;
                color: #c0caf5;
            }
            QToolButton:hover {
                background-color: #24283b;
                border: 1px solid #7aa2f7;
            }
            QToolButton:checked {
                background-color: #24283b;
                border: 1px solid #7aa2f7;
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
                background-color: #1a1b26;
            }
            QCheckBox::indicator:checked {
                border: 1px solid #7aa2f7;
                background-color: #24283b;
            }
            QCheckBox::indicator:hover {
                border: 1px solid #7aa2f7;
            }
        """)
    
    def _on_tool_selected(self, tool_name):
        """Handle tool selection"""
        # Update checked state
        for name, action in self.tool_buttons.items():
            if name not in ['straight_line', 's_curve']:  # Don't update line type buttons here
                action.setChecked(name == tool_name)
        
        # Activate the tool
        self.tool_controller.set_active_tool(tool_name)
    
    def _on_line_type_selected(self, line_type):
        """Handle line type selection"""
        # Update checked states
        self.tool_buttons['line'].setChecked(True)
        self.tool_buttons['straight_line'].setChecked(line_type == 'straight')
        self.tool_buttons['s_curve'].setChecked(line_type == 'scurve')
        
        # Get the line tool and set its type
        line_tool = self.tool_controller.get_tool('line')
        if line_tool:
            line_tool.set_line_type(
                line_tool.LINE_TYPE_STRAIGHT if line_type == 'straight' else line_tool.LINE_TYPE_SCURVE
            )
            # Activate the line tool
            self.tool_controller.set_active_tool('line')
    
    def _toggle_perpendicular_mode(self):
        """Toggle perpendicular mode on the line tool"""
        self.tool_controller.toggle_perpendicular_mode()
        
        # If perpendicular mode is enabled, make sure line tool is active
        if self.perp_mode_action.isChecked():
            self.tool_controller.set_active_tool('line')
            self._on_tool_selected('line')
