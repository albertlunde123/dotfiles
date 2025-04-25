# pyqt_drawing_app/tools/line_tool.py
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush
from PyQt5.QtCore import Qt, QPoint, QPointF
from pyqt_drawing_app.tools.base_tool import BaseTool
from pyqt_drawing_app.elements.polyline_element import PolylineElement
from pyqt_drawing_app.elements.s_curve_element import SCurveElement
# Import the central snapping function and indicator drawing
from pyqt_drawing_app.utils.snapping import get_snap_target, draw_snap_indicator, DEFAULT_ELEMENT_SNAP_THRESHOLD
import math

# Helper for squared distance
def dist_sq(p1: QPointF, p2: QPointF) -> float:
    return (p1.x() - p2.x())**2 + (p1.y() - p2.y())**2

class LineTool(BaseTool):
    LINE_TYPE_STRAIGHT = "straight"
    LINE_TYPE_SCURVE = "scurve"

    def __init__(self, line_color):
        super().__init__()
        self.line_color = line_color
        self.preview_color = QColor(line_color)
        self.preview_color.setAlpha(128)

        self.current_points = []  # Points for the current line/curve
        self.current_mouse_pos = None
        self.current_snap_info = (None, None)
        self.snap_threshold = DEFAULT_ELEMENT_SNAP_THRESHOLD

        self.perpendicular_mode = False
        self.perp_projected_point = None
        self.line_type = self.LINE_TYPE_STRAIGHT

    def set_line_type(self, line_type):
        """Set the type of line to draw (straight or s-curve)"""
        if line_type not in [self.LINE_TYPE_STRAIGHT, self.LINE_TYPE_SCURVE]:
            raise ValueError(f"Invalid line type: {line_type}")
        self.line_type = line_type
        # Reset state when changing line type
        self._reset_state()

    def toggle_perpendicular_mode(self):
        # Only allow perpendicular mode for straight lines
        if self.line_type == self.LINE_TYPE_STRAIGHT:
            self.perpendicular_mode = not self.perpendicular_mode
            if self.current_mouse_pos:
                self._update_snap_and_projection(self.current_mouse_pos)
            self.canvas.update()

    def activate(self, canvas):
        super().activate(canvas)
        self._reset_state()

    def deactivate(self):
        self._finalize_line()
        super().deactivate()

    def _reset_state(self):
        """Reset the tool's state."""
        self.current_points = []
        self.current_mouse_pos = None
        self.current_snap_info = (None, None)
        self.perp_projected_point = None

    def _create_element(self, start_point, end_point):
        """Create the appropriate element based on line type"""
        if self.line_type == self.LINE_TYPE_STRAIGHT:
            return PolylineElement([start_point, end_point], self.line_color)
        else:  # s-curve
            return SCurveElement(start_point, end_point, self.line_color)

    def _finalize_line(self):
        """Create the final multi-segment line or curve."""
        if len(self.current_points) > 1:
            if self.line_type == self.LINE_TYPE_STRAIGHT:
                # For straight lines, create a single polyline with all points
                self.canvas.add_element(PolylineElement(self.current_points.copy(), self.line_color))
            else:
                # For S-curves, create individual curve segments
                for i in range(len(self.current_points) - 1):
                    element = SCurveElement(
                        self.current_points[i],
                        self.current_points[i + 1],
                        self.line_color
                    )
                    self.canvas.add_element(element)
        self._reset_state()

    def _find_best_snap_point(self, original_pos: QPointF):
        """
        Finds the best snap point considering grid, existing elements,
        and the current line being drawn.
        Returns: tuple (snapped_point: QPointF, snap_type: str | None)
        """
        best_snap_point = original_pos
        best_snap_type = None
        min_snap_dist_sq = float('inf')

        # 1. Check Grid and Existing Elements using central function
        grid_element_snap, ge_snap_type = get_snap_target(
            original_pos, self.canvas.elements, self.canvas.grid_manager, self.snap_threshold
        )
        if ge_snap_type:  # Found a grid or element snap
            dist = dist_sq(original_pos, grid_element_snap)
            if dist < min_snap_dist_sq:
                min_snap_dist_sq = dist
                best_snap_point = grid_element_snap
                best_snap_type = ge_snap_type

        # 2. Check Self-Snapping (points in current line)
        self_snap_point = None
        if len(self.current_points) > 0:
            threshold_sq = self.snap_threshold ** 2
            # Check all points except the very last one
            for i in range(len(self.current_points) - 1):
                point = self.current_points[i]
                d_sq = dist_sq(original_pos, point)
                if d_sq < threshold_sq and d_sq < min_snap_dist_sq:
                    min_snap_dist_sq = d_sq
                    self_snap_point = QPointF(point)

        # If self-snap was closer, it becomes the best snap
        if self_snap_point:
            best_snap_point = self_snap_point
            best_snap_type = 'self'

        # If no snap found better than original pos, reset type
        if best_snap_point == original_pos:
            best_snap_type = None

        return best_snap_point, best_snap_type

    def _calculate_perpendicular_point(self, base_point, mouse_pos):
        if len(self.current_points) < 2: return mouse_pos
        ref_start = self.current_points[-2]
        ref_end = self.current_points[-1]
        ref_vector = QPointF(ref_end.x() - ref_start.x(), ref_end.y() - ref_start.y())
        perp_vector = QPointF(-ref_vector.y(), ref_vector.x())
        length = math.sqrt(perp_vector.x()**2 + perp_vector.y()**2)
        if length < 0.001: return mouse_pos
        perp_vector = QPointF(perp_vector.x() / length, perp_vector.y() / length)
        to_mouse = QPointF(mouse_pos.x() - base_point.x(), mouse_pos.y() - base_point.y())
        dot_product = to_mouse.x() * perp_vector.x() + to_mouse.y() * perp_vector.y()
        end_point = QPointF(
            base_point.x() + perp_vector.x() * dot_product,
            base_point.y() + perp_vector.y() * dot_product
        )
        return end_point

    def _update_snap_and_projection(self, current_pos: QPointF):
        """Helper to update snap point and perpendicular projection."""
        self.current_mouse_pos = current_pos
        # Find potential best snap point (grid, element, or self)
        snapped_point, snap_type = self._find_best_snap_point(current_pos)
        self.current_snap_info = (snapped_point, snap_type)

        # Calculate perpendicular projection if needed (only for straight lines)
        if self.perpendicular_mode and self.line_type == self.LINE_TYPE_STRAIGHT and self.current_points:
            base_point = self.current_points[-1]
            # Project based on the *snapped* position if available, else mouse pos
            point_to_project = snapped_point if snap_type else current_pos
            self.perp_projected_point = self._calculate_perpendicular_point(base_point, point_to_project)
        else:
            self.perp_projected_point = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Recalculate snap based on the exact press position
            snapped_point, snap_type = self._find_best_snap_point(event.pos())

            # If in perpendicular mode and we have a projected point, use that
            if self.perpendicular_mode and self.perp_projected_point and self.line_type == self.LINE_TYPE_STRAIGHT:
                point_to_add = self.perp_projected_point
            else:
                point_to_add = snapped_point if snap_type else QPointF(event.pos())

            # Add the point to our line
            self.current_points.append(point_to_add)
            # Update mouse pos state and recalculate for next preview
            self._update_snap_and_projection(event.pos())
            self.canvas.update()

        elif event.button() == Qt.RightButton:
            self._finalize_line()
            self.canvas.update()

    def mouseMoveEvent(self, event):
        self._update_snap_and_projection(QPointF(event.pos()))
        self.canvas.update()

    def mouseReleaseEvent(self, event):
        pass  # Click-based, no action on release

    def draw(self, painter: QPainter):
        # Draw existing segments
        if len(self.current_points) > 1:
            if self.line_type == self.LINE_TYPE_STRAIGHT:
                # Draw straight line segments
                painter.setPen(QPen(self.line_color, 2, Qt.SolidLine))
                for i in range(len(self.current_points) - 1):
                    painter.drawLine(self.current_points[i], self.current_points[i + 1])
                # Draw points
                painter.setBrush(QBrush(self.line_color))
                for point in self.current_points:
                    painter.drawEllipse(point, 3, 3)
            else:
                # Draw S-curve segments
                for i in range(len(self.current_points) - 1):
                    element = SCurveElement(
                        self.current_points[i],
                        self.current_points[i + 1],
                        self.line_color
                    )
                    element.draw(painter)

        # Draw preview segment
        if self.current_points and self.current_mouse_pos:
            preview_pen = QPen(self.preview_color, 2, Qt.DashLine)
            painter.setPen(preview_pen)

            # Get the preview end point
            if self.perpendicular_mode and self.perp_projected_point and self.line_type == self.LINE_TYPE_STRAIGHT:
                preview_end_point = self.perp_projected_point
                # Draw perpendicular indicator
                if len(self.current_points) >= 2:
                    painter.save()
                    painter.setPen(QPen(Qt.blue, 1, Qt.DashLine))
                    ref_start = self.current_points[-2]
                    ref_end = self.current_points[-1]
                    painter.drawLine(ref_start, ref_end)
                    # Draw right angle symbol
                    angle_size = 8
                    painter.setPen(QPen(Qt.blue, 1, Qt.SolidLine))
                    ref_vector = QPointF(ref_end.x() - ref_start.x(), ref_end.y() - ref_start.y())
                    length = math.sqrt(ref_vector.x()**2 + ref_vector.y()**2)
                    if length > 0.001:
                        ref_vector = QPointF(ref_vector.x() / length, ref_vector.y() / length)
                        perp_vector = QPointF(-ref_vector.y(), ref_vector.x())
                        p1 = self.current_points[-1] + ref_vector * angle_size
                        p2 = p1 + perp_vector * angle_size
                        p3 = self.current_points[-1] + perp_vector * angle_size
                        painter.drawLine(self.current_points[-1], p1)
                        painter.drawLine(p1, p2)
                        painter.drawLine(self.current_points[-1], p3)
                        painter.drawLine(p3, p2)
                    painter.restore()
            else:
                # Use snap point if available, otherwise use raw mouse position
                snap_point, snap_type = self.current_snap_info
                preview_end_point = snap_point if snap_type else self.current_mouse_pos

            # Draw the preview segment
            if self.line_type == self.LINE_TYPE_STRAIGHT:
                painter.drawLine(self.current_points[-1], preview_end_point)
            else:  # s-curve
                preview = SCurveElement(
                    self.current_points[-1],
                    preview_end_point,
                    self.preview_color
                )
                preview.draw(painter)

        # Draw snap indicator if a snap occurred
        snap_point, snap_type = self.current_snap_info
        if snap_type:
            draw_snap_indicator(painter, snap_point)

