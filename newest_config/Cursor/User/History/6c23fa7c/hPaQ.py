#controllers/tool_controller.py
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QAction
from ..tools.select_move_tool import SelectMoveTool
from ..tools.line_tool import LineTool
from ..tools.rectangle_tool import RectangleTool
from ..tools.circle_tool import CircleTool
from ..tools.polyline_tool import PolylineTool
from ..tools.latex_text_tool import LatexTextTool
from ..tools.s_curve_tool import SCurveTool

class ToolController(QObject):

    tool_changed = pyqtSignal(str)

    def __init__(self, canvas):
        super().__init__()
        self.canvas = canvas
        self.tools = {
            'select': SelectMoveTool(),
            'line': LineTool(),
            'rectangle': RectangleTool(),
            'circle': CircleTool(),
            'polyline': PolylineTool(),
            'latex': LatexTextTool(),
            's_curve': SCurveTool(),
        }
        self.active_tool = None
    
    def _initialize_tools(self):
        from pyqt_drawing_app.tools.select_move_tool import SelectMoveTool
        from pyqt_drawing_app.tools.line_tool import LineTool
        from pyqt_drawing_app.tools.freehand_tool import FreehandTool
        from pyqt_drawing_app.tools.circle_tool import CircleTool
        from pyqt_drawing_app.tools.latex_text_tool import LatexTextTool
        from pyqt_drawing_app.tools.rectangle_tool import RectangleTool

        
        self.tools = {
            'select': SelectMoveTool(),
            'line': LineTool(self.canvas.line_color),
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
        if 'line' in self.tools and hasattr(self.tools['line'], 'toggle_perpendicular_mode'):
            self.tools['line'].toggle_perpendicular_mode()
    
    def setup_menu(self, menu_bar):
        """Set up the tools menu."""
        tools_menu = menu_bar.addMenu('&Tools')
        
        # Add actions for each tool
        for tool_name, tool in self.tools.items():
            action = QAction(tool_name.replace('_', ' ').title(), self.canvas)
            action.setCheckable(True)
            action.setData(tool_name)
            action.triggered.connect(lambda checked, tn=tool_name: self.set_active_tool(tn))
            tools_menu.addAction(action)
            
        # Set the select tool as active by default
        self.set_active_tool('select')

    def merge_selected_elements(self):
        """Merge selected elements if the select tool is active"""
        if self.active_tool == 'select' and hasattr(self.tools['select'], 'merge_selected_elements'):
            self.tools['select'].merge_selected_elements()
    
