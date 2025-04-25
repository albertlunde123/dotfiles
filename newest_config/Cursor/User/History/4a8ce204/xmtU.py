from PyQt5.QtWidgets import QShortcut, QToolBar, QWidget
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt
from ..views.tool_toolbar import ToolToolbar

class HotkeyManager:
    """Manages application hotkeys and keyboard shortcuts"""
    
    def __init__(self, main_window):
        """
        Initialize hotkey manager with the main application window
        
        Args:
            main_window: The main window with controllers and canvas
        """
        self.main_window = main_window
        self.shortcuts = {}
        self._setup_hotkeys()
    
    def _setup_hotkeys(self):
        """Define and register all application hotkeys"""
        # Tool selection - using tool_controller
        self._add_shortcut("V", lambda: self._select_tool('select_move'), "Select Tool")
        self._add_shortcut("L", lambda: self._select_tool('line'), "Line Tool")
        self._add_shortcut("R", lambda: self._select_tool('rectangle'), "Rectangle Tool")
        self._add_shortcut("C", lambda: self._select_tool('circle'), "Circle Tool")
        self._add_shortcut("F", lambda: self._select_tool('freehand'), "Freehand Tool")
        self._add_shortcut("T", lambda: self._select_tool('latex'), "LaTeX Text Tool")
        
        # Remove any existing Shift+R shortcut if it exists
        if "Shift+R" in self.shortcuts:
            self.shortcuts["Shift+R"]["shortcut"].setEnabled(False)
            del self.shortcuts["Shift+R"]
        
    def _select_tool(self, tool_name):
        """Select a tool and update UI without causing recursion"""
        # Find the ToolToolbar instance
        toolbar = None
        for toolbar_obj in self.main_window.findChildren(QToolBar):
            if isinstance(toolbar_obj, ToolToolbar):
                toolbar = toolbar_obj
                break
        
        if toolbar:
            # Update button states
            for name, button in toolbar.tool_buttons.items():
                if name not in ['straight_line', 's_curve']:  # Skip line type buttons
                    button.setChecked(name == tool_name)
            
            # Special handling for line tool subtypes
            if tool_name == 'line':
                toolbar.tool_buttons['line'].setChecked(True)
                toolbar.tool_buttons['straight_line'].setChecked(True)
                # Make line type options visible
                for widget in toolbar.findChildren(QWidget):
                    if isinstance(widget, QWidget) and widget.parent() == toolbar:
                        for child in widget.findChildren(QWidget):
                            if isinstance(child, QWidget) and child.parent() == widget:
                                child.setVisible(True)
        
        # Set the tool without triggering UI updates
        self.main_window.tool_controller.set_active_tool(tool_name)
        
    def _add_shortcut(self, key_sequence, callback, description=""):
        """Add a keyboard shortcut"""
        shortcut = QShortcut(QKeySequence(key_sequence), self.main_window)
        shortcut.activated.connect(callback)
        self.shortcuts[key_sequence] = {
            "shortcut": shortcut,
            "callback": callback,
            "description": description
        }
        return shortcut
    
    def get_shortcut_list(self):
        """Return a list of all registered shortcuts with descriptions"""
        return [(key, self.shortcuts[key]["description"]) 
                for key in self.shortcuts]
    
    def update_tool_specific_shortcuts(self):
        """
        Update shortcuts that are specific to the active tool.
        Call this when the active tool changes.
        """
        # Remove any existing tool-specific shortcuts
        tool_specific_keys = ["Ctrl+M", "Ctrl+G", "Ctrl+U"]
        for key in tool_specific_keys:
            if key in self.shortcuts:
                self.shortcuts[key]["shortcut"].setEnabled(False)
                del self.shortcuts[key]
        
        # Add shortcuts for the new active tool if it supports them
        if hasattr(self.main_window.tool_controller, 'get_active_tool'):
            active_tool = self.main_window.tool_controller.get_active_tool()
            if hasattr(active_tool, 'merge_selected_elements'):
                self._add_shortcut("Ctrl+M", lambda: active_tool.merge_selected_elements(), "Merge Elements")
            if hasattr(active_tool, 'group_selected_elements'):
                self._add_shortcut("Ctrl+G", lambda: active_tool.group_selected_elements(), "Group Elements")
            if hasattr(active_tool, 'ungroup_selected_elements'):
                self._add_shortcut("Ctrl+U", lambda: active_tool.ungroup_selected_elements(), "Ungroup Elements")
