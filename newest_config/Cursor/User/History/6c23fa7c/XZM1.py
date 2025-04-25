#controllers/tool_controller.py
from PyQt5.QtCore import QObject, pyqtSignal, Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QAction, QMenu, QToolBar, QWidget, QVBoxLayout, QPushButton, QMainWindow
from ..tools.select_move_tool import SelectMoveTool
from ..tools.line_tool import LineTool
from ..tools.rectangle_tool import RectangleTool
from ..tools.circle_tool import CircleTool
from ..tools.latex_text_tool import LatexTextTool
from ..tools.freehand_tool import FreehandTool

class ToolController(QObject):

    tool_changed = pyqtSignal(str)
    
    # Define tool groups
    TOOL_GROUPS = {
        'line': ['straight_line', 's_curve']
    }

    def __init__(self, canvas):
        super().__init__()
        self.canvas = canvas
        self._initialize_tools()
        self.active_tool = None
        self.tool_buttons = {}  # Store references to tool buttons
        
        # Find the main window
        parent = self.canvas.parent()
        while parent and not isinstance(parent, QMainWindow):
            parent = parent.parent()
        self.main_window = parent
    
    def _initialize_tools(self):
        # Create line tool instance that will be used for both straight and s-curve modes
        line_tool = LineTool(self.canvas.line_color)
        
        self.tools = {
            'select': SelectMoveTool(),
            'straight_line': line_tool,  # Straight line mode
            's_curve': line_tool,  # S-curve mode (same tool instance)
            'rectangle': RectangleTool(self.canvas.line_color),
            'freehand': FreehandTool(self.canvas.line_color),
            'circle': CircleTool(self.canvas.line_color),
            'latex': LatexTextTool(self.canvas.line_color)
        }
    
    def set_active_tool(self, tool_name):
        """Set the active drawing tool"""
        if tool_name in self.tools:
            # Update active tool reference
            self.active_tool = tool_name
            
            # Configure line tool mode if switching to straight line or s-curve
            if tool_name in ['straight_line', 's_curve']:
                line_tool = self.tools[tool_name]
                line_tool.set_line_type(
                    LineTool.LINE_TYPE_STRAIGHT if tool_name == 'straight_line' else LineTool.LINE_TYPE_SCURVE
                )
            
            # Update button states
            self._update_button_states(tool_name)
            
            # Set the tool in the canvas
            self.canvas.set_tool(self.tools[tool_name])
            self.tool_changed.emit(tool_name)
            return True
        return False
    
    def _update_button_states(self, active_tool_name):
        """Update the checked state of all tool buttons"""
        for tool_name, button in self.tool_buttons.items():
            button.setChecked(tool_name == active_tool_name)
            
            # If this is a main tool with subtypes, update its checked state based on subtypes
            if tool_name in self.TOOL_GROUPS:
                subtypes = self.TOOL_GROUPS[tool_name]
                button.setChecked(active_tool_name in subtypes)
    
    def get_active_tool(self):
        """Get the currently active tool name"""
        return self.active_tool
    
    def get_tool(self, tool_name):
        """Get a specific tool by name"""
        return self.tools.get(tool_name)
    
    def get_all_tools(self):
        """Get all available tools"""
        return self.tools
    
    def update_tool_colors(self, color):
        """Update color for all tools"""
        for tool_name, tool in self.tools.items():
            # Handle different tool property names
            if hasattr(tool, 'line_color'):
                tool.line_color = color
            elif hasattr(tool, 'circle_color'):
                tool.circle_color = color
            
            # Update preview color
            if hasattr(tool, 'preview_color'):
                tool.preview_color = QColor(color)
                tool.preview_color.setAlpha(128)
    
    def update_preview_opacity(self, opacity):
        """Update the opacity for all tool previews"""
        for tool in self.tools.values():
            if hasattr(tool, 'preview_color'):
                tool.preview_color.setAlpha(opacity)
    
    def toggle_perpendicular_mode(self):
        """Toggle perpendicular mode for the line tool"""
        active_tool = self.tools.get(self.active_tool)
        if isinstance(active_tool, LineTool):
            active_tool.toggle_perpendicular_mode()
    
    def setup_menu(self, menu_bar):
        """Set up the tools menu."""
        tools_menu = menu_bar.addMenu('&Tools')
        
        # Create a toolbar for the main interface
        toolbar = QToolBar()
        toolbar.setOrientation(Qt.Vertical)
        
        # Create a widget to hold the toolbar and subtype buttons
        tools_widget = QWidget()
        layout = QVBoxLayout(tools_widget)
        layout.setSpacing(2)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Add the main toolbar to the layout
        layout.addWidget(toolbar)
        
        # Create buttons for each tool
        for tool_name in ['select', 'line', 'rectangle', 'circle', 'freehand', 'latex']:
            # Create the main tool button
            button = QPushButton(tool_name.replace('_', ' ').title())
            button.setCheckable(True)
            self.tool_buttons[tool_name] = button
            
            if tool_name in self.TOOL_GROUPS:
                # Create a container for the subtype buttons
                subtype_container = QWidget()
                subtype_layout = QVBoxLayout(subtype_container)
                subtype_layout.setSpacing(1)
                subtype_layout.setContentsMargins(10, 0, 0, 0)  # Add left margin for indentation
                
                # Create buttons for each subtype
                for subtype in self.TOOL_GROUPS[tool_name]:
                    subtype_button = QPushButton(subtype.replace('_', ' ').title())
                    subtype_button.setCheckable(True)
                    subtype_button.setFixedHeight(20)  # Make subtype buttons smaller
                    subtype_button.clicked.connect(
                        lambda checked, st=subtype: self.set_active_tool(st)
                    )
                    self.tool_buttons[subtype] = subtype_button
                    subtype_layout.addWidget(subtype_button)
                
                # Add the main button and its subtypes to the layout
                layout.addWidget(button)
                layout.addWidget(subtype_container)
                
                # Connect the main button to show/hide subtypes
                button.clicked.connect(
                    lambda checked, sc=subtype_container: sc.setVisible(checked)
                )
                # Initially hide the subtypes
                subtype_container.setVisible(False)
            else:
                # For tools without subtypes, just connect directly
                button.clicked.connect(
                    lambda checked, tn=tool_name: self.set_active_tool(tn)
                )
                layout.addWidget(button)
        
        # Add the tools widget to the main window
        if self.main_window:
            self.main_window.addToolBar(Qt.LeftToolBarArea, toolbar)
            toolbar.addWidget(tools_widget)
        
        # Set the select tool as active by default
        self.set_active_tool('select')

    def merge_selected_elements(self):
        """Merge selected elements if the select tool is active"""
        if self.active_tool == 'select' and hasattr(self.tools['select'], 'merge_selected_elements'):
            self.tools['select'].merge_selected_elements()
    
