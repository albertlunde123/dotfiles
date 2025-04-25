#main_window.py
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QAction
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from pyqt_drawing_app.canvas_widget import CanvasWidget
from pyqt_drawing_app.controllers.tool_controller import ToolController
from .controllers.color_controller import ColorController
from pyqt_drawing_app.controllers.file_controller import FileController
from pyqt_drawing_app.views.tool_toolbar import ToolToolbar
from pyqt_drawing_app.views.color_toolbar import ColorToolbar
from pyqt_drawing_app.utils.colors import load_pywal_colors, build_stylesheet
from pyqt_drawing_app.utils.hotkeys import HotkeyManager
from pyqt_drawing_app.views.grid_settings_dock import GridSettingsDock
from pyqt_drawing_app.views.element_properties_dock import ElementPropertiesDock


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt Drawing App")
        self.setGeometry(100, 100, 800, 600)
        
        # Apply stylesheet from colors
        colors = load_pywal_colors()
        if colors:
            stylesheet = build_stylesheet(colors)
            self.setStyleSheet(stylesheet)
        
        # Create canvas
        self.canvas = CanvasWidget(self)
        
        # Initialize controllers
        self.tool_controller = ToolController(self.canvas)
        self.color_controller = ColorController(self.canvas, self.tool_controller)
        self.file_controller = FileController(self.canvas)
        
        # Set up UI components
        self._setup_central_widget()
        
        # Set default tool
        self.tool_controller.set_active_tool('line')
        self._setup_toolbars()
        self._setup_grid_settings_dock()
        self._setup_menus()
        self._setup_element_properties_dock()
        self.hotkey_manager = HotkeyManager(self)
    
    def _setup_central_widget(self):
        """Create and set the central widget with the canvas"""
        self.central_widget = QWidget()
        layout = QVBoxLayout(self.central_widget)
        layout.addWidget(self.canvas)
        self.setCentralWidget(self.central_widget)
    
    def _setup_toolbars(self):
        """Create and add toolbars"""
        # Tool toolbar
        self.tool_toolbar = ToolToolbar(self.tool_controller, self)
        self.addToolBar(Qt.LeftToolBarArea, self.tool_toolbar)
        
        # Color toolbar
        self.color_toolbar = ColorToolbar(self.color_controller, self)
        self.addToolBar(Qt.BottomToolBarArea, self.color_toolbar)
        # Position the color toolbar at the bottom left
        self.color_toolbar.setOrientation(Qt.Horizontal)
        self.color_toolbar.setFloating(False)
        self.color_toolbar.setAllowedAreas(Qt.BottomToolBarArea)
        self.color_toolbar.setMovable(False)
        # Connect to update properties panel when color changes
        self.color_toolbar.colorSelected.connect(self._on_color_selected)
    
    def _on_color_selected(self, color):
        """Handle color selection from the color toolbar"""
        # Update the properties panel if elements are selected
        selected = self.canvas.get_selected_elements()
        if selected:
            self.update_properties_panel()
    
    def _setup_menus(self):
        """Set up the application menus"""
        # Let controllers add their menus
        self.file_controller.setup_menu(self.menuBar())
        self.tool_controller.setup_menu(self.menuBar())
        self.color_controller.setup_menu(self.menuBar())

        menu_bar = self.menuBar()

        view_menu = menu_bar.addMenu("&View")

        # Grid Toggle Action (still useful for quick toggle)
        self.show_grid_action = QAction("Show &Grid", self, checkable=True)
        self.show_grid_action.setChecked(self.canvas.grid_manager.visible)
        self.show_grid_action.triggered.connect(self.toggle_grid_action) # Connect to specific slot
        view_menu.addAction(self.show_grid_action)

        view_menu.addSeparator()


        # Grid Settings Dock Action
        self.grid_settings_action = QAction("Grid Settin&gs...", self)
        self.grid_settings_action.triggered.connect(self.toggle_grid_settings_dock)
        view_menu.addAction(self.grid_settings_action)

        # Element properties
        self.properties_action = QAction("Element Propertie&s", self)
        # Connect its triggered signal to the slot that shows/hides the dock
        self.properties_action.triggered.connect(self.toggle_properties_dock)
        # Add the action to the View menu
        view_menu.addAction(self.properties_action)

    def _setup_element_properties_dock(self):
        self.properties_dock = ElementPropertiesDock(self)
        self.addDockWidget(Qt.RightDockWidgetArea, self.properties_dock)

        # Connect signals from dock to handler slots
        self.properties_dock.propertyColorChanged.connect(self.on_property_color_changed)
        self.properties_dock.propertyThicknessChanged.connect(self.on_property_thickness_changed)
        # --- Connect New Signals ---
        self.properties_dock.propertyDashPatternChanged.connect(self.on_property_dash_pattern_changed)
        self.properties_dock.propertyStartArrowChanged.connect(self.on_property_start_arrow_changed)
        self.properties_dock.propertyEndArrowChanged.connect(self.on_property_end_arrow_changed)
        # ---
        self.properties_dock.hide()

    def _setup_grid_settings_dock(self):
        """Creates and configures the grid settings dock widget."""
        self.grid_dock = GridSettingsDock(self)
        self.grid_dock.setObjectName("GridSettingsDock") # Important for saving state
        # Ensure canvas.grid_manager exists before accessing its attributes
        if hasattr(self.canvas, 'grid_manager'):
            self.grid_dock.set_initial_values(
                self.canvas.grid_manager.spacing,
                self.canvas.grid_manager.visible,
                self.canvas.grid_manager.snap_enabled
            )
            # Connect signals from dock to canvas methods
            self.grid_dock.spacingChanged.connect(self.canvas.set_grid_spacing)
            self.grid_dock.visibilityChanged.connect(self.on_grid_visibility_changed) # Use intermediate slot
            self.grid_dock.snapChanged.connect(self.canvas.set_grid_snap)
        else:
             print("Warning: Canvas grid_manager not found during dock setup.")
             # Optionally disable dock controls here

        self.addDockWidget(Qt.RightDockWidgetArea, self.grid_dock)
        self.grid_dock.hide() # Start hidden

    def toggle_grid_action(self, checked):
        """Slot for the 'Show Grid' menu action."""
        self.canvas.set_grid_visibility(checked)
        # Update dock controls to match
        self.grid_dock.update_controls(self.canvas.grid_manager.visible, self.canvas.grid_manager.snap_enabled)

    def on_grid_visibility_changed(self, visible):
        """Slot for when visibility changes FROM the dock."""
        self.canvas.set_grid_visibility(visible)
        # Update menu action to match
        self.show_grid_action.setChecked(visible)
        # Update snap checkbox in dock as visibility often controls snap
        self.grid_dock.update_controls(visible, self.canvas.grid_manager.snap_enabled)

    def toggle_grid_settings_dock(self):
        """Shows or hides the grid settings dock widget."""
        if self.grid_dock.isVisible():
            self.grid_dock.hide()
        else:
            self.grid_dock.show()

   # --- New Slots for Style Properties ---
    def on_property_color_changed(self, color: QColor):
        """Applies the new color to selected elements."""
        selected = self.canvas.get_selected_elements()
        # Check if the emitted color is valid (it might be invalid if multiple
        # different colors were selected initially)
        if not selected or not color.isValid():
            return

        for element in selected:
            # Check if the element has a 'set_color' method before calling it
            if hasattr(element, 'set_color'):
                element.set_color(color)

        self.canvas.update() # Redraw the canvas to show the changes
        # Optional: If set_color could modify the color (e.g., clamping),
        # you might want to re-read the value and update the dock again.
        # self.update_properties_panel()

    def on_property_thickness_changed(self, thickness: float):
        """Applies the new thickness to selected elements."""
        selected = self.canvas.get_selected_elements()
        if not selected:
            return

        for element in selected:
            # Check if the element has a 'set_line_thickness' method
            if hasattr(element, 'set_line_thickness'):
                 element.set_line_thickness(thickness)

        self.canvas.update() # Redraw the canvas
    def on_property_dash_pattern_changed(self, pattern_key: str):
        """Applies the new dash pattern to selected elements."""
        selected = self.canvas.get_selected_elements()
        if not selected or not pattern_key: return # Ignore empty selection from combo
        for element in selected:
            if hasattr(element, 'set_dash_pattern'):
                 element.set_dash_pattern(pattern_key)
        self.canvas.update()

    def on_property_start_arrow_changed(self, arrow_type: str):
        """Applies the new start arrowhead type to selected elements."""
        selected = self.canvas.get_selected_elements()
        if not selected or not arrow_type: return
        for element in selected:
            if hasattr(element, 'set_start_arrowhead'):
                 element.set_start_arrowhead(arrow_type)
        self.canvas.update()

    def on_property_end_arrow_changed(self, arrow_type: str):
        """Applies the new end arrowhead type to selected elements."""
        selected = self.canvas.get_selected_elements()
        if not selected or not arrow_type: return
        for element in selected:
            if hasattr(element, 'set_end_arrowhead'):
                 element.set_end_arrowhead(arrow_type)
        self.canvas.update()

    def update_properties_panel(self): # Keep existing
        selected = self.canvas.get_selected_elements()
        if selected:
            self.properties_dock.update_properties(selected)
            self.properties_dock.setEnabled(True)
        else:
            self.properties_dock.update_properties([])
            self.properties_dock.setEnabled(False)

    def toggle_properties_dock(self): # Keep existing
        if self.properties_dock.isVisible(): self.properties_dock.hide()
        else: self.properties_dock.show(); self.update_properties_panel()
