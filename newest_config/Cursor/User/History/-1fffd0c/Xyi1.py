# pyqt_drawing_app/tools/circle_tool.py
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush
from PyQt5.QtCore import Qt, QPointF, QRectF
from pyqt_drawing_app.tools.base_tool import BaseTool
from pyqt_drawing_app.elements import CircleElement # Correct import path
# Import the central snapping function and indicator drawing
from pyqt_drawing_app.utils.snapping import get_snap_target, draw_snap_indicator
import math

class CircleTool(BaseTool):
    def __init__(self, circle_color):
        super().__init__()
        self.circle_color = circle_color
        self.preview_color = QColor(circle_color)
        self.preview_color.setAlpha(128)

        self.center_point = None # Center of the circle being defined
        self.current_mouse_pos = None # Current raw mouse position for radius preview
        # Store snap info for the CENTER point only: (snapped_pos: QPointF | None, snap_type: str | None)
        self.center_snap_info = (None, None)

    def activate(self, canvas):
        super().activate(canvas)
        self.center_point = None
        self.current_mouse_pos = None
        self.center_snap_info = (None, None)

    def deactivate(self):
        # Reset state if deactivated mid-draw
        self.center_point = None
        self.current_mouse_pos = None
        self.center_snap_info = (None, None)
        super().deactivate()

    def _finalize_circle(self):
        """Create a circle element and add to canvas using current state."""
        # This is called on the second click
        if self.center_point and self.current_mouse_pos:
            # Calculate radius using the raw mouse position for the second click
            dx = self.center_point.x() - self.current_mouse_pos.x()
            dy = self.center_point.y() - self.current_mouse_pos.y()
            radius = math.sqrt(dx**2 + dy**2)

            # Add circle to canvas if radius is valid
            if radius > 0.1: # Use a small threshold
                self.canvas.add_element(CircleElement(
                    self.center_point, radius, self.circle_color))

            # Reset state after finalizing
            self.center_point = None
            self.current_mouse_pos = None
            self.center_snap_info = (None, None)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # If we don't have a center point yet (FIRST CLICK)
            if not self.center_point:
                # Use the snapped point calculated during mouse move
                snapped_center_pos, _ = self.center_snap_info
                # Use snapped position if available, otherwise use raw event position
                point_to_use = snapped_center_pos if snapped_center_pos else event.pos()

                self.center_point = QPointF(point_to_use)
                self.current_mouse_pos = QPointF(event.pos()) # Store raw pos for radius
                self.center_snap_info = (None, None) # Clear snap indicator after placing center
            else:
                # We already have a center (SECOND CLICK), finalize the circle
                # Update mouse pos one last time before finalizing
                self.current_mouse_pos = QPointF(event.pos())
                self._finalize_circle()

            self.canvas.update()

        elif event.button() == Qt.RightButton:
            # Cancel the current circle drawing
            self.center_point = None
            self.current_mouse_pos = None
            self.center_snap_info = (None, None)
            self.canvas.update()

    def mouseMoveEvent(self, event):
        # Always update the raw mouse position for radius preview
        self.current_mouse_pos = QPointF(event.pos())

        # Find potential snap point ONLY if we haven't set the center yet
        if not self.center_point:
            snapped_pos, snap_type = get_snap_target(
                event.pos(), self.canvas.elements, self.canvas.grid_manager
                # We can use the default snap threshold from the snapping module
            )
            self.center_snap_info = (snapped_pos, snap_type)
        else:
            # If center is already set, don't look for snaps for the radius endpoint
            self.center_snap_info = (None, None)

        self.canvas.update()

    def mouseReleaseEvent(self, event):
        pass  # No action needed on release for this tool

    def keyPressEvent(self, event):
        """Handle keyboard events for the circle tool"""
        # Add any circle-specific keyboard shortcuts here
        event.ignore()  # Default behavior is to ignore the event

    def draw(self, painter: QPainter):
        snap_point, snap_type = self.center_snap_info

        # Draw the preview circle/radius if we have a center point set
        if self.center_point and self.current_mouse_pos:
            # Calculate radius based on raw mouse position
            dx = self.center_point.x() - self.current_mouse_pos.x()
            dy = self.center_point.y() - self.current_mouse_pos.y()
            radius = math.sqrt(dx**2 + dy**2)

            # Draw preview radius line (from center to raw mouse pos)
            preview_pen = QPen(self.preview_color, 1, Qt.DashLine)
            painter.setPen(preview_pen)
            painter.drawLine(self.center_point, self.current_mouse_pos)

            # Draw preview circle outline
            preview_pen = QPen(self.preview_color, 2, Qt.DashLine)
            painter.setPen(preview_pen)
            painter.setBrush(Qt.NoBrush)
            rect = QRectF(
                self.center_point.x() - radius, self.center_point.y() - radius,
                radius * 2, radius * 2
            )
            painter.drawEllipse(rect)

            # Draw center point handle
            painter.setBrush(QBrush(self.circle_color))
            painter.setPen(QPen(self.circle_color))
            painter.drawEllipse(self.center_point, 3, 3)

        # Draw snap indicator ONLY if we haven't placed the center yet
        if not self.center_point and snap_type:
            draw_snap_indicator(painter, snap_point)

