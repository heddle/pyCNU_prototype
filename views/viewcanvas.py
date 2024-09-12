from PyQt6.QtCore import Qt, QRect, QPoint, QPointF
from PyQt6.QtGui import QMouseEvent, QPalette, QColor, QPainter, QPen, QPolygonF, QPolygon
from PyQt6.QtWidgets import QWidget

from constants import BOX_ZOOM, CENTER, PAN, POINTER, ZOOM_FACTOR, BACKGROUND_COLOR, WIDTH, HEIGHT, WORLD_RECTANGLE
from util.x11colors import X11Colors
from world.worldrect import WorldRectangle
from items.item import Item
from typing import Optional


class ViewCanvas(QWidget):
    def __init__(self, view, attributes):
        super().__init__()
        self.view = view

        self.setMouseTracking(True)  # Enable mouse tracking by default

        # Set the style of the canvas
        self.__set_style(attributes)

        self.is_dragging = False
        self.last_mouse_local = None
        self.last_mouse_world = None

        # for rubber-banding
        self.rubber_band_rect = None
        self.rubber_band_origin = None

        width = int(attributes.get(WIDTH, 800))
        height = int(attributes.get(HEIGHT, 600))
        self.world = attributes.get(WORLD_RECTANGLE, WorldRectangle(0, 0, width, height))
        self.default_world = self.world.copy()
        self.previous_world = self.world.copy()

        self.setMinimumSize(width, height)  # Set a minimum size for the canvas

    def __set_style(self, attributes):
        # Create a palette
        palette = QPalette()

        # Set the background color (with alpha)  using the palette
        color_str = attributes.get(BACKGROUND_COLOR, "#DDDDDD")
        color = QColor(color_str) if color_str.startswith("#") else X11Colors.get_color(color_str)

        palette.setColor(QPalette.ColorRole.Window, color)
        # Apply the palette to the canvas
        self.setPalette(palette)

        # Enable autofill background
        self.setAutoFillBackground(True)

    def enterEvent(self, event):
        """ Handle the enter event, where the pointer enters the canvas. """
        if self.view.toolbar:
            self.setCursor(self.view.toolbar.get_cursor())
        self.setMouseTracking(True)  # Enable mouse tracking when the mouse enters the canvas

    def leaveEvent(self, event):
        """ Handle the leave event, where the pointer leaves the canvas. """
        if self.view.toolbar:
            self.view.toolbar.set_default_cursor()
        self.setMouseTracking(False)  # Disable mouse tracking when the mouse leaves the canvas

    def mousePressEvent(self, event: QMouseEvent):
        shifted = event.modifiers() & Qt.KeyboardModifier.ShiftModifier
        control = event.modifiers() & Qt.KeyboardModifier.ControlModifier
        lb = event.button() == Qt.MouseButton.LeftButton
        rb = event.button() == Qt.MouseButton.RightButton
        mb3 = rb or (lb and control)
        mb1 = lb and not mb3

        if mb1:
            self.is_dragging = True
            local_point = self.mapFromGlobal(event.globalPosition().toPoint())
            self.last_mouse_local = local_point
            self.rubber_band_origin = local_point
            world_point = self.local_to_world(QPoint(local_point.x(), local_point.y()))
            self.last_mouse_world = world_point
            self.handle_simple_click(local_point, world_point, shifted)
        elif mb3:
            current = self.view.toolbar.get_active_radiobutton()
            if current == POINTER:
                self.setCursor(Qt.CursorShape.OpenHandCursor)
                item = self.item_at_point(self.mapFromGlobal(event.globalPosition().toPoint()))
                if item:
                    item.context_menu(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        local_point = self.mapFromGlobal(event.globalPosition().toPoint())
        world_point = self.local_to_world(QPoint(local_point.x(), local_point.y()))
        self.view.status_bar.showMessage(f"Mouse Moved at Local: {local_point}, World: {world_point}")

        # are we dragging?
        if self.is_dragging:
            current_pos_loc = local_point
            delta_loc = current_pos_loc - self.last_mouse_local
            self.last_mouse_local = current_pos_loc
            self.view.status_bar.showMessage(f"Dragging with delta: ({delta_loc.x()}, {delta_loc.y()})")

            current_pos_world = world_point
            delta_world = current_pos_world - self.last_mouse_world
            self.last_mouse_world = current_pos_world

            if self.view.toolbar:
                current = self.view.toolbar.get_active_radiobutton()
                if current == PAN:
                    self.pan(delta_loc.x(), delta_loc.y())
                elif current == POINTER:
                    items = self.get_selected_items()
                    if items:
                        print(f"Moving {len(items)} items")
                        for item in items:
                            item.move(delta_world.x(), delta_world.y())
                    else:
                        self.rubber_band_rect = QRect(self.rubber_band_origin, current_pos_loc).normalized()
                    self.update()
                elif current == BOX_ZOOM:
                    self.rubber_band_rect = QRect(self.rubber_band_origin, current_pos_loc).normalized()
                    self.update()

        else:
            # Add your custom logic here
            pass

    def mouseReleaseEvent(self, event: QMouseEvent):
        """
        Handle the mouse release event.
        :param event: the mouse event
        :return: None
        """
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_dragging = False
            local_point = self.mapFromGlobal(event.globalPosition().toPoint())
            world_point = self.local_to_world(QPoint(local_point.x(), local_point.y()))
            self.view.status_bar.showMessage(f"Mouse Released at Local: {local_point}, World: {world_point}")

            if self.view.toolbar:
                shifted = event.modifiers() & Qt.KeyboardModifier.ShiftModifier

                if self.rubber_band_rect:
                    self.handle_rubber_band(shifted)

    def handle_simple_click(self, local_point, world_point, shifted):
        current = self.view.toolbar.get_active_radiobutton()
        if current == CENTER:  # recenter
            self.center(world_point)
            self.view.toolbar.set_default_button()
            self.setCursor(self.view.toolbar.get_cursor())
        elif current == POINTER:
            item = self.item_at_point(local_point)
            if item:
                self.clicked_on_item(item, shifted)
            else:
                self.deselect_all()
                self.update()

    def handle_rubber_band(self, shifted):
        current = self.view.toolbar.get_active_radiobutton()
        if current == BOX_ZOOM:
            self.zoom_to_rect(self.rubber_band_rect)
        elif current == POINTER:
            items = self.items_enclosed_by_rect(self.rubber_band_rect)
            self.clicked_on_items(items, shifted)

        self.rubber_band_rect = None
        self.rubber_band_origin = None

    def zoom_to_rect(self, rect: QRect):
        """
        Zoom to a local rectangle.
        :param rect: the rectangle to zoom to.
        :return: None
        """
        if rect.width() < 8 or rect.height() < 8:
            return

        self.__prepare_to_zoom()
        world_rect = self.local_rect_to_world(rect)
        self.world = world_rect
        self.update()

    def pan(self, dx, dy):
        """
        Pan the world by dx and dy.
        :return: None
        """
        xc = self.size().width() / 2
        yc = self.size().height() / 2
        xc -= dx
        yc -= dy
        wp = self.local_to_world(QPoint(int(xc), int(yc)))
        self.center(wp)
        self.update()

    def center(self, world_point: QPointF):
        """
        Center the world.
        :return: None
        """
        x = world_point.x()
        y = world_point.y()
        xc, yc = self.world.center()
        dx = x - xc
        dy = y - yc
        self.world.move(dx, dy)
        self.update()

    def __prepare_to_zoom(self):
        self.previous_world = self.world.copy()

    def zoom_in(self):
        self.__prepare_to_zoom()
        self.world.scale(ZOOM_FACTOR)
        self.update()

    def zoom_out(self):
        self.__prepare_to_zoom()
        self.world.scale(1 / ZOOM_FACTOR)
        self.update()

    def undo_zoom(self):
        """
        Undo the last zoom operation.
        :return: None
        """
        temp = self.world.copy()
        self.world = self.previous_world.copy()
        self.previous_world = temp
        self.update()

    def restore_default_world(self):
        """
        Restore the default world.
        :return: None
        """
        self.__prepare_to_zoom()
        self.world = self.default_world.copy()
        self.update()

    def local_to_world(self, local_point: QPoint) -> QPointF:
        """
        Convert a point from the local system to the world system.

        :param local_point: A tuple (x, y) in the local coordinate system.
        :return: A tuple (x, y) in the world coordinate system.
        """
        local_x = local_point.x()
        local_y = local_point.y()
        canvas_size = self.size()
        world_x = (local_x / canvas_size.width()) * self.world.width + self.world.x_min
        world_y = (1 - local_y / canvas_size.height()) * self.world.height + self.world.y_min
        return QPointF(world_x, world_y)

    def world_to_local(self, world_point: QPointF) -> QPoint:
        """
        Convert a point from the world system to the local system.

        :param world_point: A tuple (x, y) in the world coordinate system.
        :return: A tuple (x, y) in the local coordinate system.
        """
        world_x = world_point.x()
        world_y = world_point.y()

        canvas_size = self.size()
        local_x = (world_x - self.world.x_min) / self.world.width * canvas_size.width()
        local_y = (1 - (world_y - self.world.y_min) / self.world.height) * canvas_size.height()
        return QPoint(int(local_x), int(local_y))

    def local_rect_to_world(self, local_rect: QRect) -> WorldRectangle:
        """
        Convert a rectangle from the local system to the world system.

        :param local_rect: A QRect in the local coordinate system.
        :return: A WorldRectangle in the world coordinate system.
        """
        bottom = local_rect.y() + local_rect.height()
        right = local_rect.x() + local_rect.width()
        wp_min = self.local_to_world(QPoint(local_rect.x(), bottom))
        wp_max = self.local_to_world(QPoint(right, local_rect.y()))
        x_min = wp_min.x()
        y_min = wp_min.y()
        x_max = wp_max.x()
        y_max = wp_max.y()
        return WorldRectangle(x_min, y_min, x_max - x_min, y_max - y_min)

    def world_rect_to_local(self, world_rect: WorldRectangle) -> QRect:
        """
        Convert a rectangle from the world system to the local system.

        :param world_rect: A WorldRectangle in the world coordinate system.
        :return: A QRect in the local coordinate system.
        """
        x_max = world_rect.x_min + world_rect.width
        y_max = world_rect.y_min + world_rect.height

        p_lt = self.world_to_local(QPointF(world_rect.x_min, y_max))
        p_rb = self.world_to_local(QPointF(x_max, world_rect.y_min))
        left = p_lt.x()
        top = p_lt.y()
        right = p_rb.x()
        bottom = p_rb.y()
        return QRect(int(left), int(top), int(right - left), int(bottom - top))


    """
    Convert a polygon from the world system to the local system.
    :param world_polygon: A QPolygonF in the world coordinate system.
    :return: A QPolygon in the local coordinate system.
    """
    def world_polygon_to_local(self, world_polygon: QPolygonF) -> QPolygon:
        # Convert QPolygonF to QPolygon by applying world_to_local on each point
        local_polygon = QPolygon()
        for world_point in world_polygon:
            local_point = self.world_to_local(world_point)
            local_polygon.append(local_point)
        return local_polygon

    """
    Convert a polygon from the local system to the world system.
    :param local_polygon: A QPolygon in the local coordinate system.
    :return: A QPolygonF in the world coordinate system.
    """
    def local_polygon_to_world(self, local_polygon: QPolygon) -> QPolygonF:
        # Convert QPolygon to QPolygonF by applying local_to_world on each point
        world_polygon = QPolygonF()
        for local_point in local_polygon:
            world_point = self.local_to_world(local_point)
            world_polygon.append(world_point)
        return world_polygon
    def paintEvent(self, event):
        super().paintEvent(event)
        self.draw_layers()

        # Create a painter
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if self.rubber_band_rect:
            current = self.view.toolbar.get_active_radiobutton()
            if current == BOX_ZOOM:
                painter.setPen(QPen(Qt.GlobalColor.red, 1, Qt.PenStyle.DashLine))
                painter.drawRect(self.rubber_band_rect)
            elif current == POINTER:
                painter.setPen(QPen(Qt.GlobalColor.blue, 1, Qt.PenStyle.SolidLine))
                painter.drawRect(self.rubber_band_rect)

        # Set the pen for the border
        pen = QPen(QColor(0, 0, 0), 1)  # Black color, 1 pixel width
        painter.setPen(pen)

        # Draw the border
        rect = self.rect()
        painter.drawRect(rect.adjusted(0, 0, -1, -1))  # Adjust to draw inside the widget's boundary

    def draw_layers(self):
        for layer in reversed(self.view.layers):
            for item in reversed(layer.items):
                item.draw(self)

    def deselect_all(self):
        """Deselect all items in the view"""
        for layer in self.view.layers:
            for item in layer.items:
                item.selected = False

    def item_at_point(self, q_point: QPoint) -> Optional[Item]:
        """Return the item at the given local point or None if no item is found"""
        for layer in self.view.layers:
            for item in layer.items:
                if item.contains_local(q_point):
                    return item
        return None

    def items_enclosed_by_rect(self, q_rect: QRect):
        """Return a list of items enclosed by the local pixel rectangle
        :param q_rect: The local pixel rectangle
        :return: A list of items enclosed by the local pixel rectangle"""
        items = []
        for layer in self.view.layers:
            for item in layer.items:
                if item.enclosed_by(q_rect):
                    items.append(item)
        return items

    def clicked_on_items(self, items, shifted):
        """Handle the selection of multiple items with the same algorithm
        as in PowerPoint
        :param items: The items clicked on
        :param shifted: Whether the shift key is pressed"""

        if not shifted:
            self.deselect_all()
        for item in items:
            item.selected = True

        self.update()

    def get_selected_items(self):
        """Return a list of selected items"""
        selected = []
        for layer in self.view.layers:
            for item in layer.items:
                if item.selected:
                    selected.append(item)
        return selected

    def clicked_on_item(self, item: Item, shifted):
        """Handle the selection of an item with the same algorithm
        as in PowerPoint
        :param item: The item clicked on
        :param shifted: Whether the shift key is pressed"""
        if item.selectable:
            if item.selected:
                if shifted:
                    item.selected = False
                else:
                    item.selected = True
            else:  # not originally selected
                if not shifted:
                    self.deselect_all()
                item.selected = True
            self.update()
