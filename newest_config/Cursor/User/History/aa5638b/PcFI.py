# pyqt_drawing_app/tools/rectangle_tool.py
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush
from PyQt5.QtCore import Qt, QPointF, QRectF
from pyqt_drawing_app.tools.base_tool import BaseTool
from pyqt_drawing_app.elements import RectangleElement # Correct import path
# Import the central snapping function and indicator drawing
from pyqt_drawing_app.utils.snapping import get_snap_target, draw_snap_indicator

class RectangleTool(BaseTool):
    def __init__(self, rect_color):
        super().__init__()
        self.rect_color = rect_color
        self.preview_color = QColor(rect_color)
        self.preview_color.setAlpha(128)

        self.start_corner = None # Stores the snapped starting corner
        self.current_mouse_pos = None # Current raw mouse position for preview
        # Store snap info as a tuple: (snapped_pos: QPointF | None, snap_type: str | None)
        self.current_snap_info = (None, None)

    def activate(self, canvas):
        super().activate(canvas)
        self.start_corner = None
        self.current_mouse_pos = None
        self.current_snap_info = (None, None)

    def deactivate(self):
        # Reset state if deactivated mid-draw
        self.start_corner = None
        self.current_mouse_pos = None
        self.current_snap_info = (None, None)
        super().deactivate()

    def _finalize_rectangle(self, end_corner: QPointF):
        """Create a rectangle element using start and final end corner."""
        # This is called on the second click, end_corner is already snapped
        if self.start_corner:
            # Add rectangle to canvas if it has some size
            # Use a small threshold to avoid zero-size rectangles
            if (abs(end_corner.x() - self.start_corner.x()) > 0.1 or
                abs(end_corner.y() - self.start_corner.y()) > 0.1):
                self.canvas.add_element(RectangleElement(
                    self.start_corner, end_corner, self.rect_color))

            # Reset state after finalizing
            self.start_corner = None
            self.current_mouse_pos = None
            self.current_snap_info = (None, None)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Get the snapped position for this click event
            snapped_click_pos, _ = self.current_snap_info # Use snap info from last move
            # Use snapped position if available, otherwise use raw event position
            point_to_use = snapped_click_pos if snapped_click_pos else event.pos()

            # If we don't have a start corner yet (FIRST CLICK)
            if not self.start_corner:
                self.start_corner = QPointF(point_to_use)
                self.current_mouse_pos = QPointF(event.pos()) # Store raw pos for preview
                # Clear snap info, next move/click relates to the end corner
                self.current_snap_info = (None, None)
            else:
                # We already have a start corner (SECOND CLICK), finalize
                # Use the snapped position from this click as the end corner
                self._finalize_rectangle(QPointF(point_to_use))

            self.canvas.update()

        elif event.button() == Qt.RightButton:
            # Cancel the current rectangle drawing
            self.start_corner = None
            self.current_mouse_pos = None
            self.current_snap_info = (None, None)
            self.canvas.update()

    def mouseMoveEvent(self, event):
        # Always update the raw mouse position for preview
        self.current_mouse_pos = QPointF(event.pos())

        # Find potential snap point for the current cursor position
        # This will be used for the preview and potentially the next click
        snapped_pos, snap_type = get_snap_target(
            event.pos(), self.canvas.elements, self.canvas.grid_manager
        )
        self.current_snap_info = (snapped_pos, snap_type)

        self.canvas.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.dragging:
                self._finalize_rectangle()
            self.dragging = False
            self.canvas.update()

    def keyPressEvent(self, event):
        """Handle keyboard events for the rectangle tool"""
        # Add any rectangle-specific keyboard shortcuts here
        event.ignore()  # Default behavior is to ignore the event

    def draw(self, painter: QPainter):
        snap_point, snap_type = self.current_snap_info

        # Draw the preview rectangle if we have a start corner
        if self.start_corner and self.current_mouse_pos:
            # Use snapped point for the end corner if available, else raw mouse pos
            end_corner = snap_point if snap_type else self.current_mouse_pos

            # Create preview rectangle
            preview_rect = QRectF(self.start_corner, end_corner).normalized()

            # Draw preview outline
            preview_pen = QPen(self.preview_color, 2, Qt.DashLine)
            painter.setPen(preview_pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(preview_rect)

            # Draw corner handles for preview
            painter.setBrush(QBrush(self.rect_color))
            painter.setPen(QPen(self.rect_color))
            painter.drawEllipse(self.start_corner, 3, 3) # Start corner
            painter.drawEllipse(end_corner, 3, 3) # Current end corner

        # Draw snap indicator at the current potential snap target
        if snap_type:
            draw_snap_indicator(painter, snap_point)
