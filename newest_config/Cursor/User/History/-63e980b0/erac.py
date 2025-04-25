# pyqt_drawing_app/tools/select_move_tool.py
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush
from PyQt5.QtCore import Qt, QPointF, QRectF
from .base_tool import BaseTool
# Import snapping functions
from ..utils.snapping import (
    get_snap_target, # We might still use parts of this logic or adapt it
    find_element_snap_point, # Specifically for finding targets
    draw_snap_indicator,
    DEFAULT_ELEMENT_SNAP_THRESHOLD
)
# Import element base class for type hinting if needed
from ..elements import DrawingElement
from typing import List, Tuple, Optional # For type hints
import math

# Helper for squared distance
def dist_sq(p1: QPointF, p2: QPointF) -> float:
    return (p1.x() - p2.x())**2 + (p1.y() - p2.y())**2

class SelectMoveTool(BaseTool):
    # Mode constants
    MODE_NONE = 0
    MODE_MOVE = 1
    MODE_ROTATE = 2

    def __init__(self):
        super().__init__()
        self.dragging = False
        self.area_selecting = False
        self.area_selection_started = False
        self.start_pos = None
        self.last_mouse_pos = None
        self.selection_rect = None
        self.active_snap_indicator_pos = None # For drawing the indicator
        self.snap_threshold = DEFAULT_ELEMENT_SNAP_THRESHOLD
        self.clicked_on_selected = False
        
        # Mode handling
        self.current_mode = self.MODE_NONE
        self.is_moving = False
        self.selected_element = None
        self.drag_threshold = 5  # Pixels to move before considering it a drag
        self.drag_started = False  # Track if we've exceeded drag threshold
        self.just_clicked = False
        
        # Movement tracking
        self.initial_drag_pos = None  # Where the drag started

        # Hold & Release Snap Mechanism
        self.is_currently_snapped = False
        self.current_snap_target_point = None # Point we are snapped TO
        self.unsnap_threshold_sq = 144 # e.g., 3 pixels squared
        self.snap_jump_factor = 1.1 # Jump slightly outside snap radius on release

        # Rotation
        self.rotation_snap_angles = [0, 45, 90, 135, 180, 225, 270, 315]
        self.rotation_snap_threshold = 5  # Degrees
        self.rotation_mode_locked = False  # Flag to maintain rotation mode

    def activate(self, canvas):
        super().activate(canvas)
        self._reset_state()
        self._update_selection_and_notify()
        # Make sure the canvas can receive keyboard events
        canvas.setFocusPolicy(Qt.StrongFocus)
        canvas.setFocus()

    def deactivate(self):
        self._reset_state()
        super().deactivate()

    def _reset_state(self):
        """Resets the tool's internal state."""
        self.dragging = False
        self.area_selecting = False
        self.area_selection_started = False
        self.start_pos = None
        self.last_mouse_pos = None
        self.selection_rect = None
        self.active_snap_indicator_pos = None
        self.clicked_on_selected = False
        if not self.rotation_mode_locked:  # Only reset mode if not locked
            self.current_mode = self.MODE_NONE
        self.selected_element = None
        self.drag_started = False
        self.initial_drag_pos = None
        # Reset snap state
        self.is_currently_snapped = False
        self.current_snap_target_point = None

    def _update_selection_and_notify(self):
        """Helper to update selection state and notify MainWindow."""
        self.selected_elements = self.canvas.get_selected_elements()
        main_window = self.canvas.parent().parent()
        if hasattr(main_window, 'update_properties_panel'):
            main_window.update_properties_panel()
            # Show the properties panel if there are selected elements
            if self.selected_elements and hasattr(main_window, 'properties_dock'):
                main_window.properties_dock.show()
                self.canvas.update()  # Only update if we're showing the properties dock

    def _update_element_rotation_mode(self):
        """Update the rotation mode flag on elements"""
        for element in self.canvas.elements:
            if hasattr(element, '_in_rotation_mode'):
                element._in_rotation_mode = (self.current_mode == self.MODE_ROTATE and element.selected)

    def _set_mode(self, mode):
        """Set the current mode and update UI accordingly"""
        if self.current_mode != mode:
            self.current_mode = mode
            self._update_element_rotation_mode()
            self.canvas.update()  # Only update if mode changed

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            current_pos = QPointF(event.pos())
            self.start_pos = current_pos
            self.last_mouse_pos = current_pos
            self.drag_started = False
            self.initial_drag_pos = current_pos
            # Reset snap state on new press
            self.is_currently_snapped = False
            self.current_snap_target_point = None
            self.just_clicked = True

            # Area Selection Logic
            if event.modifiers() & Qt.ShiftModifier:
                if not self.area_selection_started:
                    self.area_selecting = True
                    self.area_selection_started = True
                    self.selection_rect = QRectF(self.start_pos, self.start_pos)
                    self.dragging = False
                    self.active_snap_indicator_pos = None
                    self.canvas.update()
                return

            # Check if clicking on currently selected element
            clicked_element = None
            for element in self.canvas.get_selected_elements():
                if element.contains_point(current_pos):
                    clicked_element = element
                    break

            if clicked_element:
                # Clicking on already selected element - only change mode if not in locked rotation mode
                self.selected_element = clicked_element
                if not self.rotation_mode_locked:
                    self._set_mode(self.MODE_MOVE)
            else:
                # Clicking on unselected element or empty space
                self.canvas.clear_selection()
                for element in self.canvas.elements:
                    if element.contains_point(current_pos):
                        element.selected = True
                        self.selected_element = element
                        if not self.rotation_mode_locked:
                            self._set_mode(self.MODE_MOVE)
                        break
                else:
                    # Clicked empty space
                    self.selected_element = None
                    if not self.rotation_mode_locked:
                        self._set_mode(self.MODE_NONE)

            self.canvas.update()

        elif event.button() == Qt.RightButton:
            # Right click deselects and unlocks rotation mode
            self.rotation_mode_locked = False
            self.canvas.clear_selection()
            self.selected_element = None
            self._set_mode(self.MODE_NONE)
            self.canvas.update()

    def keyPressEvent(self, event):
        print(f"KeyPressEvent received! Key: {event.key()}, Modifiers: {event.modifiers()}")
        # Check for Ctrl+R to enter rotation mode
        if (event.key() == Qt.Key_R and 
            event.modifiers() & Qt.ControlModifier and 
            len(self.canvas.get_selected_elements()) > 0):
            self.selected_element = self.canvas.get_selected_elements()[0]
            self._set_mode(self.MODE_ROTATE)
            self.rotation_mode_locked = True  # Lock rotation mode
            # Initialize the rotation mode flag on the element
            print("Initializing rotation mode flag on the element")
            if hasattr(self.selected_element, '_in_rotation_mode'):
                self.selected_element._in_rotation_mode = True
            self.canvas.update()
            event.accept()
        else:
            print("Event ignored")
            event.ignore()

    def keyReleaseEvent(self, event):
        event.accept()

    def mouseMoveEvent(self, event):
        if not self.start_pos or not self.last_mouse_pos:
            # Need last_mouse_pos to calculate delta
            # If it's None (e.g., after release), update and exit
            self.last_mouse_pos = QPointF(event.pos())
            return

        current_mouse_pos = QPointF(event.pos())
        selected_elements = self.canvas.get_selected_elements()
        if not selected_elements:
            self.last_mouse_pos = current_mouse_pos
            return # Nothing to move

        final_dx = 0
        final_dy = 0
        jump_offset = QPointF(0, 0)

        # --- Hold & Release Logic ---
        if self.is_currently_snapped and self.current_snap_target_point:
            dist_sq_from_snap = dist_sq(current_mouse_pos, self.current_snap_target_point)

            if dist_sq_from_snap <= self.unsnap_threshold_sq:
                # HOLD phase: Ignore movement
                self.last_mouse_pos = current_mouse_pos # Still update for next delta calc
                self.active_snap_indicator_pos = self.current_snap_target_point # Keep indicator
                self.canvas.update()
                return
            else:
                # RELEASE phase: Calculate jump
                # print("Snap Released")
                self.is_currently_snapped = False
                direction = current_mouse_pos - self.current_snap_target_point
                length = math.sqrt(direction.x()**2 + direction.y()**2)
                if length > 1e-6:
                    direction /= length # Normalize
                    jump_distance = self.snap_threshold * self.snap_jump_factor
                    jump_offset = direction * jump_distance
                self.current_snap_target_point = None # Clear the target we were snapped to
                self.active_snap_indicator_pos = None # Clear indicator immediately on release

        # --- Calculate Movement and Potential New Snap ---
        # Calculate Raw Delta based on the *last* valid mouse position
        dx_raw = current_mouse_pos.x() - self.last_mouse_pos.x()
        dy_raw = current_mouse_pos.y() - self.last_mouse_pos.y()

        best_adjustment = QPointF(0, 0)
        potential_snap_target_pos = None
        min_snap_dist_sq = float('inf')
        snap_found = False

        # Only look for a *new* snap if not currently snapped
        if not self.is_currently_snapped:
            non_selected_elements = [e for e in self.canvas.elements if not e.selected]
            for element in selected_elements:
                if hasattr(element, 'snap_points') and element.snap_points:
                    for point in element.snap_points:
                        # Potential position *after* raw movement
                        potential_pos = point + QPointF(dx_raw, dy_raw)
                        snapped_pos, snap_type = get_snap_target(
                            potential_pos, non_selected_elements, self.canvas.grid_manager, self.snap_threshold
                        )

                        if snap_type:
                            # Calculate adjustment needed from potential_pos to snapped_pos
                            adjustment = snapped_pos - potential_pos
                            adjustment_dist_sq = adjustment.x()**2 + adjustment.y()**2

                            if adjustment_dist_sq < min_snap_dist_sq and adjustment_dist_sq < self.snap_threshold ** 2:
                                min_snap_dist_sq = adjustment_dist_sq
                                best_adjustment = adjustment
                                # Store the target point itself for potential locking
                                potential_snap_target_pos = snapped_pos
                                snap_found = True

        # --- Apply Movement ---
        final_dx = dx_raw + jump_offset.x() # Add jump if we just released
        final_dy = dy_raw + jump_offset.y()

        if snap_found: # Apply snap adjustment if we found a new one
            final_dx += best_adjustment.x()
            final_dy += best_adjustment.y()
            # Lock onto the new snap point
            self.is_currently_snapped = True
            self.current_snap_target_point = current_mouse_pos
            self.active_snap_indicator_pos = self.current_snap_target_point
            # print(f"Snap Locked to {self.current_snap_target_point}")
        else:
            # If no new snap found, ensure we are not marked as snapped
            # (Should be handled by release logic, but double-check)
            self.is_currently_snapped = False
            self.current_snap_target_point = None
            # Keep showing potential target if adjustment was calculated but not best
            self.active_snap_indicator_pos = potential_snap_target_pos

        # Move all selected elements by the final calculated delta
        if abs(final_dx) > 1e-6 or abs(final_dy) > 1e-6:
            for element in selected_elements:
                element.move(final_dx, final_dy)
            # Reset just_clicked flag after movement
            self.just_clicked = False

        # Update last mouse position *after* all calculations for this event
        self.last_mouse_pos = current_mouse_pos
        self.canvas.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Only update selection if we haven't dragged
            if not self.drag_started:
                self._update_selection_and_notify()
            
            # Reset drag state
            self.drag_started = False
            self.start_pos = None
            self.last_mouse_pos = None
            self.active_snap_indicator_pos = None
            self.canvas.update()

    def _finalize_area_selection(self, event):
        # (Keep existing logic)
        if self.selection_rect:
            ctrl_pressed = event.modifiers() & Qt.ControlModifier
            if not ctrl_pressed: self.canvas.clear_selection()
            for element in self.canvas.elements:
                if self._element_in_rect(element, self.selection_rect):
                    element.selected = True
        self.area_selecting = False
        self.area_selection_started = False
        self.selection_rect = None
        self._update_selection_and_notify()

    # Keep your existing helper methods:
    # _element_in_rect, _line_intersects_rect, _line_segments_intersect,
    # _orientation, _on_segment, _point_distance_to_line
    # ... (Paste your existing helper methods here) ...
    def _element_in_rect(self, element, rect):
        """Determines if an element is within or intersects a selection rectangle."""
        # First try to get a bounding rectangle for the element
        element_rect = None
        
        # Try to get the bounding rectangle for the element
        if hasattr(element, 'rect'):
            element_rect = element.rect
        elif hasattr(element, 'boundingRect'):
            element_rect = element.boundingRect()
        elif hasattr(element, 'position') and hasattr(element, 'svg_renderer'):
            # For LaTeX elements
            size = element.svg_renderer.defaultSize() * element.scale_factor
            if not size.isEmpty():
                element_rect = QRectF(element.position, size)
        elif hasattr(element, 'points') and element.points:
            # For polylines and other multi-point elements
            min_x = min(p.x() for p in element.points)
            max_x = max(p.x() for p in element.points)
            min_y = min(p.y() for p in element.points)
            max_y = max(p.y() for p in element.points)
            element_rect = QRectF(min_x, min_y, max_x - min_x, max_y - min_y)
        elif hasattr(element, 'center') and hasattr(element, 'radius'):
            # For circles
            element_rect = QRectF(
                element.center.x() - element.radius,
                element.center.y() - element.radius,
                element.radius * 2,
                element.radius * 2
            )
        elif hasattr(element, 'start_point') and hasattr(element, 'end_point'):
            # For line elements
            min_x = min(element.start_point.x(), element.end_point.x())
            max_x = max(element.start_point.x(), element.end_point.x())
            min_y = min(element.start_point.y(), element.end_point.y())
            max_y = max(element.start_point.y(), element.end_point.y())
            # Add some padding for line thickness
            padding = element.line_thickness if hasattr(element, 'line_thickness') else 2
            element_rect = QRectF(min_x - padding, min_y - padding, 
                                 max_x - min_x + 2*padding, max_y - min_y + 2*padding)
        
        # If we have a bounding rectangle, check if it intersects with the selection rectangle
        if element_rect:
            return rect.intersects(element_rect)
        
        # If we couldn't determine a bounding rectangle, try to check if any point is in the rect
        if hasattr(element, 'points') and element.points:
            for point in element.points:
                if rect.contains(point):
                    return True
        elif hasattr(element, 'start_point') and hasattr(element, 'end_point'):
            if rect.contains(element.start_point) or rect.contains(element.end_point):
                return True
        elif hasattr(element, 'center'):
            if rect.contains(element.center):
                return True
        elif hasattr(element, 'position'):
            if rect.contains(element.position):
                return True
                
        # If we have a circle, check if any part of the circle intersects the rectangle
        if hasattr(element, 'center') and hasattr(element, 'radius'):
            # Check if the center is in the rect
            if rect.contains(element.center):
                return True
                
            # Check if any of the four corners of the rect are within the circle
            corners = [
                QPointF(rect.left(), rect.top()),
                QPointF(rect.right(), rect.top()),
                QPointF(rect.right(), rect.bottom()),
                QPointF(rect.left(), rect.bottom())
            ]
            for corner in corners:
                if (corner.x() - element.center.x())**2 + (corner.y() - element.center.y())**2 <= element.radius**2:
                    return True
                    
            # Check if any of the four sides of the rect intersect the circle
            # This is a simplified check that might miss some edge cases
            for i in range(4):
                p1 = corners[i]
                p2 = corners[(i+1) % 4]
                if self._point_distance_to_line(element.center, p1, p2) <= element.radius:
                    return True
        
        return False
    def _line_intersects_rect(self, p1, p2, rect): # Keep existing
        rect_lines = [(QPointF(rect.left(), rect.top()), QPointF(rect.right(), rect.top())), (QPointF(rect.right(), rect.top()), QPointF(rect.right(), rect.bottom())), (QPointF(rect.right(), rect.bottom()), QPointF(rect.left(), rect.bottom())), (QPointF(rect.left(), rect.bottom()), QPointF(rect.left(), rect.top()))]
        for line in rect_lines:
            if self._line_segments_intersect(p1, p2, line[0], line[1]): return True
        return False
    def _line_segments_intersect(self, p1, p2, p3, p4): # Keep existing
        o1=self._orientation(p1,p2,p3); o2=self._orientation(p1,p2,p4); o3=self._orientation(p3,p4,p1); o4=self._orientation(p3,p4,p2)
        if o1!=o2 and o3!=o4: return True
        if o1==0 and self._on_segment(p1,p3,p2): return True
        if o2==0 and self._on_segment(p1,p4,p2): return True
        if o3==0 and self._on_segment(p3,p1,p4): return True
        if o4==0 and self._on_segment(p3,p2,p4): return True
        return False
    def _orientation(self, p, q, r): # Keep existing
        val = (q.y()-p.y())*(r.x()-q.x()) - (q.x()-p.x())*(r.y()-q.y())
        if abs(val)<1e-9: return 0
        return 1 if val > 0 else 2
    def _on_segment(self, p, q, r): # Keep existing
        return (q.x()<=max(p.x(),r.x())+1e-9 and q.x()>=min(p.x(),r.x())-1e-9 and q.y()<=max(p.y(),r.y())+1e-9 and q.y()>=min(p.y(),r.y())-1e-9)
    def _point_distance_to_line(self, point, line_start, line_end): # Keep existing
        if line_start==line_end: dx=point.x()-line_start.x(); dy=point.y()-line_start.y(); return (dx*dx+dy*dy)**0.5
        line_length_sq=(line_end.x()-line_start.x())**2+(line_end.y()-line_start.y())**2
        if line_length_sq<1e-9: dx=point.x()-line_start.x(); dy=point.y()-line_start.y(); return (dx*dx+dy*dy)**0.5
        t=max(0,min(1,((point.x()-line_start.x())*(line_end.x()-line_start.x())+(point.y()-line_start.y())*(line_end.y()-line_start.y()))/line_length_sq))
        projection_x=line_start.x()+t*(line_end.x()-line_start.x()); projection_y=line_start.y()+t*(line_end.y()-line_start.y())
        dx=point.x()-projection_x; dy=point.y()-projection_y; return (dx*dx+dy*dy)**0.5


    def merge_selected_elements(self):
        # (Keep existing logic)
        selected_elements = self.canvas.get_selected_elements()
        if len(selected_elements) <= 1: return
        all_points = []
        seen_points = set()
        def point_exists(point, tolerance=0.001):
            for existing in seen_points:
                if abs(point.x() - existing[0]) < tolerance and abs(point.y() - existing[1]) < tolerance: return True
            return False
        def add_unique_point(point):
            if not point_exists(point): all_points.append(point); seen_points.add((point.x(), point.y()))
        for element in selected_elements:
            if hasattr(element, 'start_point') and hasattr(element, 'end_point'): add_unique_point(element.start_point); add_unique_point(element.end_point)
            elif hasattr(element, 'points'):
                for point in element.points: add_unique_point(point)
        if not all_points: return
        color = selected_elements[0].color
        from pyqt_drawing_app.elements import PolylineElement
        merged_element = PolylineElement(all_points, color)
        for element in selected_elements:
            if element in self.canvas.elements: self.canvas.elements.remove(element)
        self.canvas.add_element(merged_element)
        self.canvas.clear_selection()
        merged_element.selected = True
        self.canvas.update()


    def draw(self, painter: QPainter):
        # Draw snap indicator if applicable
        if self.active_snap_indicator_pos:
            draw_snap_indicator(painter, self.active_snap_indicator_pos)

        # Draw selection rectangle if in area selection mode
        if self.area_selecting and self.selection_rect:
            painter.save()
            painter.setPen(QPen(QColor(100, 100, 255, 180), 1, Qt.DashLine))
            painter.setBrush(QBrush(QColor(100, 100, 255, 50)))
            painter.drawRect(self.selection_rect)
            painter.restore()
