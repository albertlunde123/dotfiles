import sys
import unittest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt

from pyqt_drawing_app.views.element_properties_dock import ElementPropertiesDock
from pyqt_drawing_app.elements import DrawingElement, RectangleElement, CircleElement, PolylineElement

# Create a QApplication instance for testing
app = QApplication(sys.argv)

class TestElementPropertiesDock(unittest.TestCase):
    def setUp(self):
        self.dock = ElementPropertiesDock()
        
    def test_initial_state(self):
        """Test the initial state of the dock"""
        self.assertFalse(self.dock.isEnabled())
        self.assertEqual(self.dock.color_button.get_color(), QColor())
        self.assertEqual(self.dock.thickness_spinbox.value(), 0)
        self.assertEqual(self.dock.dash_combo.currentIndex(), -1)
        self.assertFalse(self.dock.start_checkbox.isChecked())
        self.assertFalse(self.dock.end_checkbox.isChecked())
        
    def test_update_with_rectangle(self):
        """Test updating the dock with a rectangle element"""
        # Create a rectangle element
        rect = RectangleElement(QPointF(0, 0), QPointF(100, 100), QColor("red"))
        rect.line_thickness = 3.0
        rect.dash_pattern_key = DrawingElement.DASHED_LINE
        rect.start_arrowhead = DrawingElement.ARROWHEAD_STANDARD
        rect.end_arrowhead = DrawingElement.ARROWHEAD_NONE
        
        # Update the dock
        self.dock.update_properties([rect])
        
        # Check that the dock is enabled
        self.assertTrue(self.dock.isEnabled())
        
        # Check that the properties are set correctly
        self.assertEqual(self.dock.color_button.get_color(), QColor("red"))
        self.assertEqual(self.dock.thickness_spinbox.value(), 3.0)
        self.assertEqual(self.dock.dash_combo.currentText(), DrawingElement.DASHED_LINE)
        self.assertTrue(self.dock.start_checkbox.isChecked())
        self.assertFalse(self.dock.end_checkbox.isChecked())
        
    def test_update_with_multiple_elements(self):
        """Test updating the dock with multiple elements with different properties"""
        # Create elements with different properties
        rect1 = RectangleElement(QPointF(0, 0), QPointF(100, 100), QColor("red"))
        rect1.line_thickness = 3.0
        rect1.dash_pattern_key = DrawingElement.DASHED_LINE
        rect1.start_arrowhead = DrawingElement.ARROWHEAD_STANDARD
        rect1.end_arrowhead = DrawingElement.ARROWHEAD_NONE
        
        rect2 = RectangleElement(QPointF(0, 0), QPointF(100, 100), QColor("blue"))
        rect2.line_thickness = 5.0
        rect2.dash_pattern_key = DrawingElement.SOLID_LINE
        rect2.start_arrowhead = DrawingElement.ARROWHEAD_NONE
        rect2.end_arrowhead = DrawingElement.ARROWHEAD_STANDARD
        
        # Update the dock
        self.dock.update_properties([rect1, rect2])
        
        # Check that the dock is enabled
        self.assertTrue(self.dock.isEnabled())
        
        # Check that the properties show multiple values
        self.assertEqual(self.dock.color_button.get_color(), QColor())  # Should be invalid color
        self.assertEqual(self.dock.thickness_spinbox.value(), 3.0)  # Should show first element's value
        self.assertEqual(self.dock.dash_combo.currentText(), "")  # Should be empty for multiple values
        self.assertTrue(self.dock.start_checkbox.isChecked())  # Should show first element's value
        self.assertFalse(self.dock.end_checkbox.isChecked())  # Should show first element's value
        
    def test_checkbox_signals(self):
        """Test that the checkbox signals are emitted correctly"""
        # Create a rectangle element
        rect = RectangleElement(QPointF(0, 0), QPointF(100, 100), QColor("red"))
        self.dock.update_properties([rect])
        
        # Connect to signals
        start_arrow_changed = False
        end_arrow_changed = False
        
        def on_start_arrow_changed(arrow_type):
            nonlocal start_arrow_changed
            start_arrow_changed = True
            self.assertEqual(arrow_type, "Arrow")
            
        def on_end_arrow_changed(arrow_type):
            nonlocal end_arrow_changed
            end_arrow_changed = True
            self.assertEqual(arrow_type, "Arrow")
            
        self.dock.propertyStartArrowChanged.connect(on_start_arrow_changed)
        self.dock.propertyEndArrowChanged.connect(on_end_arrow_changed)
        
        # Check the checkboxes
        self.dock.start_checkbox.setChecked(True)
        self.dock.end_checkbox.setChecked(True)
        
        # Check that the signals were emitted
        self.assertTrue(start_arrow_changed)
        self.assertTrue(end_arrow_changed)
        
        # Reset
        start_arrow_changed = False
        end_arrow_changed = False
        
        # Uncheck the checkboxes
        self.dock.start_checkbox.setChecked(False)
        self.dock.end_checkbox.setChecked(False)
        
        # Check that the signals were emitted with "None"
        self.assertTrue(start_arrow_changed)
        self.assertTrue(end_arrow_changed)
        
    def test_close_button(self):
        """Test that the close button works correctly"""
        # Show the dock
        self.dock.show()
        self.assertTrue(self.dock.isVisible())
        
        # Click the close button
        self.dock.close()
        
        # Check that the dock is hidden
        self.assertFalse(self.dock.isVisible())

if __name__ == '__main__':
    unittest.main() 