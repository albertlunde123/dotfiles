import unittest
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtTest import QTest
from pyqt_drawing_app.tools.select_move_tool import SelectMoveTool
from pyqt_drawing_app.elements.rectangle_element import RectangleElement

class TestSelectMoveTool(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create QApplication instance if it doesn't exist
        cls.app = QApplication.instance()
        if cls.app is None:
            cls.app = QApplication([])

    def setUp(self):
        # Create a mock canvas with proper parent hierarchy
        class MockMainWindow(QWidget):
            def __init__(self):
                super().__init__()
                self.tool_controller = None

        class MockCanvas(QWidget):
            def __init__(self):
                super().__init__()
                self.elements = []
                self.selected_elements = []
                self.update_called = False
                self.parent_widget = MockMainWindow()
                self.setParent(self.parent_widget)

            def get_selected_elements(self):
                return self.selected_elements

            def update(self):
                self.update_called = True

            def parent(self):
                return self.parent_widget

        self.canvas = MockCanvas()
        self.tool = SelectMoveTool()
        self.tool.activate(self.canvas)

    def test_rotation_hotkey(self):
        # Create a test element and select it
        element = RectangleElement(QPointF(0, 0), QPointF(100, 100), "black")
        self.canvas.elements.append(element)
        self.canvas.selected_elements = [element]

        # Simulate Ctrl+R key press
        event = QTest.keyEvent(QTest.Press, self.tool.canvas, Qt.Key_R, Qt.ControlModifier)
        self.tool.keyPressEvent(event)

        # Verify that rotation mode was activated
        self.assertEqual(self.tool.current_mode, self.tool.MODE_ROTATE)
        self.assertTrue(self.canvas.update_called)
        self.assertTrue(hasattr(element, '_in_rotation_mode'))
        self.assertTrue(element._in_rotation_mode)

    def test_rotation_hotkey_no_selection(self):
        # Simulate Ctrl+R key press with no selected elements
        event = QTest.keyEvent(QTest.Press, self.tool.canvas, Qt.Key_R, Qt.ControlModifier)
        self.tool.keyPressEvent(event)

        # Verify that rotation mode was not activated
        self.assertEqual(self.tool.current_mode, self.tool.MODE_NONE)
        self.assertFalse(self.canvas.update_called)

    def test_rotation_hotkey_wrong_modifier(self):
        # Create a test element and select it
        element = RectangleElement(QPointF(0, 0), QPointF(100, 100), "black")
        self.canvas.elements.append(element)
        self.canvas.selected_elements = [element]

        # Simulate R key press with Shift modifier instead of Ctrl
        event = QTest.keyEvent(QTest.Press, self.tool.canvas, Qt.Key_R, Qt.ShiftModifier)
        self.tool.keyPressEvent(event)

        # Verify that rotation mode was not activated
        self.assertEqual(self.tool.current_mode, self.tool.MODE_NONE)
        self.assertFalse(self.canvas.update_called)

if __name__ == '__main__':
    unittest.main() 