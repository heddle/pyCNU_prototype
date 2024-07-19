from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QMouseEvent, QPalette, QColor, QPainter, QPen
from PyQt6.QtWidgets import QWidget

from constants import BOX_ZOOM, CENTER, PAN, POINTER, ZOOM_FACTOR, BACKGROUND_COLOR, WIDTH, HEIGHT, WORLD_RECTANGLE
from util.x11colors import X11Colors
from world.worldrect import WorldRectangle


class ViewCanvas(QWidget):
    def __init__(self, view, attributes):
        super().__init__()
        self.view = view

        self.setMouseTracking(True)  # Enable mouse tracking by default

        # Set the style of the canvas
        self.__set_style(attributes)

        self.is_dragging = False
        self.last_mouse_position = None

        #for rubber-banding
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

        # Enable auto-fill background
        self.setAutoFillBackground(True)

    def enterEvent(self, event):
        if self.view.toolbar:
            self.setCursor(self.view.toolbar.get_cursor())
        self.setMouseTracking(True)  # Enable mouse tracking when the mouse enters the canvas

    def leaveEvent(self, event):
        if self.view.toolbar:
            self.view.toolbar.set_default_cursor()
        self.setMouseTracking(False)  # Disable mouse tracking when the mouse leaves the canvas

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_dragging = True
            local_point = self.mapFromGlobal(event.globalPosition().toPoint())
            self.last_mouse_position = local_point
            self.rubber_band_origin = local_point
            world_point = self.local_to_world((local_point.x(), local_point.y()))
            self.view.statusBar.showMessage(f"Mouse Pressed at Local: {local_point}, World: {world_point}")

            if self.view.toolbar:
                current = self.view.toolbar.get_active_radiobutton()
                if current == CENTER:
                    self.center(world_point)
                    self.view.toolbar.set_default_button()
                    self.setCursor(self.view.toolbar.get_cursor())


    def mouseMoveEvent(self, event: QMouseEvent):
        local_point = self.mapFromGlobal(event.globalPosition().toPoint())
        world_point = self.local_to_world((local_point.x(), local_point.y()))
        self.view.statusBar.showMessage(f"Mouse Moved at Local: {local_point}, World: {world_point}")

        # are we dragging?
        if self.is_dragging:
            current_position = local_point
            delta = current_position - self.last_mouse_position
            self.last_mouse_position = current_position
            self.view.statusBar.showMessage(f"Dragging with delta: ({delta.x()}, {delta.y()})")

            if self.view.toolbar:
                current = self.view.toolbar.get_active_radiobutton()
                if current == PAN:
                    self.pan(delta.x(), delta.y())
                elif current == BOX_ZOOM:
                    self.rubber_band_rect = QRect(self.rubber_band_origin, current_position).normalized()
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
            world_point = self.local_to_world((local_point.x(), local_point.y()))
            self.view.statusBar.showMessage(f"Mouse Released at Local: {local_point}, World: {world_point}")

            if self.view.toolbar:
                current = self.view.toolbar.get_active_radiobutton()
                if current == BOX_ZOOM:
                    self.zoom_to_rect(self.rubber_band_rect)
                    zoom_rect = self.local_rect_to_world(self.rubber_band_rect)
                    self.rubber_band_rect = None
                    self.rubber_band_origin = None
                elif current == POINTER:
                    # add selection logic here
                    pass


    def zoom_to_rect(self, rect : QRect):
        """
        Zoom to a rectangle.
        :param rect: the rectangle to zoom to.
        :return: None
        """
        if rect.width() < 8 or rect.height() < 8:
            return

        self.__prepare_to_zoom()
        world_rect = self.local_rect_to_world(rect)
        self.world = world_rect
        self.update()

    def local_to_world(self, local_point):
        """
        Convert a point from the local system to the world system.

        :param local_point: A tuple (x, y) in the local coordinate system.
        :return: A tuple (x, y) in the world coordinate system.
        """
        local_x, local_y = local_point
        canvas_size = self.size()
        world_x = (local_x / canvas_size.width()) * self.world.width + self.world.x_min
        world_y = (1 - local_y / canvas_size.height()) * self.world.height + self.world.y_min
        return world_x, world_y

    def pan(self, dx, dy):
        """
        Pan the world by dx and dy.
        :return: None
        """
        xc = self.size().width() / 2
        yc = self.size().height() / 2
        xc -= dx;
        yc -= dy
        x, y = self.local_to_world((xc, yc))
        self.center((x, y))
        self.update()

    def center(self, world_point):
        """
        Center the world.
        :return: None
        """
        x, y = world_point
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

    def world_to_local(self, world_point):
        """
        Convert a point from the world system to the local system.

        :param world_point: A tuple (x, y) in the world coordinate system.
        :return: A tuple (x, y) in the local coordinate system.
        """
        world_x, world_y = world_point
        canvas_size = self.size()
        local_x = (world_x - self.world.x_min) / self.world.width * canvas_size.width()
        local_y = (1 - (world_y - self.world.y_min) / self.world.height) * canvas_size.height()
        return local_x, local_y

    def local_rect_to_world(self, local_rect: QRect) -> WorldRectangle:
        """
        Convert a rectangle from the local system to the world system.

        :param local_rect: A QRect in the local coordinate system.
        :return: A WorldRectangle in the world coordinate system.
        """
        bottom = local_rect.y() + local_rect.height()
        right = local_rect.x() + local_rect.width()
        x_min, y_min = self.local_to_world((local_rect.x(), bottom))
        x_max, y_max = self.local_to_world((right, local_rect.y()))
        return WorldRectangle(x_min, y_min, x_max - x_min, y_max - y_min)

    def world_rect_to_local(self, world_rect : WorldRectangle) -> QRect:
        """
        Convert a rectangle from the world system to the local system.

        :param world_rect: A WorldRectangle in the world coordinate system.
        :return: A QRect in the local coordinate system.
        """
        x_max = world_rect.x_min + world_rect.width
        y_max = world_rect.y_min + world_rect.height

        left, top = self.world_to_local((world_rect.x_min, y_max))
        right, bottom = self.world_to_local((x_max, world_rect.y_min))
        return QRect(int(left), int(top), int(right - left), int(bottom - top))

    def paintEvent(self, event):
        super().paintEvent(event)
        self.draw_layers()

        # Create a painter
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if self.rubber_band_rect:
            painter.setPen(QPen(Qt.GlobalColor.red, 1, Qt.PenStyle.DashLine))
            painter.drawRect(self.rubber_band_rect)

        # Set the pen for the border
        pen = QPen(QColor(0, 0, 0), 1)  # Black color, 1 pixel width
        painter.setPen(pen)

        # Draw the border
        rect = self.rect()
        painter.drawRect(rect.adjusted(0, 0, -1, -1))  # Adjust to draw inside the widget's boundary

    def draw_layers(self):
        for layer in reversed(self.view.layers):
            print(f"Drawing layer {layer.name}")
            for item in reversed(layer.items):
                item.draw(self)
