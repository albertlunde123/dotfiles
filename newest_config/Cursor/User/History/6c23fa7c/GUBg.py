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
from ..views.tool_toolbar import ToolToolbar

class ToolController(QObject):

    tool_changed = pyqtSignal(str)
    
    # Define tool groups
    TOOL_GROUPS = {
        'line': ['straight_line', 's_curve']
    }

    # Button style sheets
    MAIN_BUTTON_STYLE = """
        QPushButton {
            background-color: #f0f0f0;
            border: 1px solid #c0c0c0;
            border-radius: 4px;
            padding: 5px;
            text-align: left;
            margin: 2px;
        }
        QPushButton:checked {
            background-color: #e0e0e0;
            border: 2px solid #808080;
        }
        QPushButton:hover {
            background-color: #e5e5e5;
        }
    """

    SUB_BUTTON_STYLE = """
        QPushButton {
            background-color: #f8f8f8;
            border: 1px solid #d0d0d0;
            border-radius: 3px;
            padding: 3px;
            text-align: left;
            margin: 1px;
        }
        QPushButton:checked {
            background-color: #e8e8e8;
            border: 2px solid #808080;
        }
        QPushButton:hover {
            background-color: #f0f0f0;
        }
    """

    def __init__(self, canvas):
        super().__init__()
        self.canvas = canvas
        self._initialize_tools()
        self.active_tool = None
        
        # Find the main window
        parent = self.canvas.parent()
        while parent and not isinstance(parent, QMainWindow):
            parent = parent.parent()
        self.main_window = parent
        
        # Create and add the tool toolbar
        if self.main_window:
            toolbar = ToolToolbar(self, self.main_window)
            self.main_window.addToolBar(Qt.LeftToolBarArea, toolbar)
    
    def _initialize_tools(self):
        # Create line tool instance that will be used for both straight and s-curve modes
        line_tool = LineTool(self.canvas.line_color)
        
        self.tools = {
            'select': SelectMoveTool(),
            'line': line_tool,  # Will be configured for straight/curve mode as needed
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
            
            # Configure line tool mode if needed
            if tool_name == 'line':
                line_tool = self.tools[tool_name]
                line_tool.set_line_type(LineTool.LINE_TYPE_STRAIGHT)
            
            # Set the tool in the canvas
            self.canvas.set_tool(self.tools[tool_name])
            self.tool_changed.emit(tool_name)
            return True
        return False
    
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
        """Set up the tools interface."""
        # The toolbar is now created in __init__, so we don't need to do anything here
        pass

    def merge_selected_elements(self):
        """Merge selected elements if the select tool is active"""
        if self.active_tool == 'select' and hasattr(self.tools['select'], 'merge_selected_elements'):
            self.tools['select'].merge_selected_elements()
    
