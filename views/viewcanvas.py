from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QMouseEvent, QPalette, QColor, QPainter, QPen
from PyQt6.QtCore import Qt

from constants import BACKGROUND_COLOR, WIDTH, HEIGHT, WORLD_RECTANGLE
from util.x11colors import X11Colors
from world.worldrect import WorldRectangle
class ViewCanvas(QWidget):
    def __init__(self, view, attributes):
        super().__init__()
        self.view = view

        self.setMouseTracking(True)  # Enable mouse tracking by default
        # Create a palette
        palette = QPalette()

        # Set the style of the canvas
        self.setStyle(attributes)

        self.is_dragging = False
        self.last_mouse_position = None

        width = int(attributes.get(WIDTH, 800))
        height = int(attributes.get(HEIGHT, 600))
        self.world_rect = attributes.get(WORLD_RECTANGLE, WorldRectangle(0, 0, width, height))
        self.setMinimumSize(width, height)  # Set a minimum size for the canvas

    def setStyle(self, attributes):
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
        if (self.view.toolbar):
            self.setCursor(self.view.toolbar.get_cursor())
        self.setMouseTracking(True)  # Enable mouse tracking when the mouse enters the canvas

    def leaveEvent(self, event):
        if (self.view.toolbar):
            self.view.toolbar.set_default_cursor()
        self.setMouseTracking(False)  # Disable mouse tracking when the mouse leaves the canvas

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_dragging = True
            local_point = self.mapFromGlobal(event.globalPosition().toPoint())
            self.last_mouse_position = local_point
            world_point = self.local_to_world((local_point.x(), local_point.y()))
            self.view.status_bar.showMessage(f"Mouse Pressed at Local: {local_point}, World: {world_point}")
             # Add your custom logic here

    def mouseMoveEvent(self, event: QMouseEvent):
        local_point = self.mapFromGlobal(event.globalPosition().toPoint())
        world_point = self.local_to_world((local_point.x(), local_point.y()))
        self.view.status_bar.showMessage(f"Mouse Moved at Local: {local_point}, World: {world_point}")

        #are we dragging?
        if self.is_dragging:
            current_position = local_point
            delta = current_position - self.last_mouse_position
            self.last_mouse_position = current_position
            self.view.status_bar.showMessage(f"Dragging with delta: ({delta.x()}, {delta.y()})")
            # Add your custom logic here
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
            self.view.status_bar.showMessage(f"Mouse Released at Local: {local_point}, World: {world_point}")
            # Add your custom logic here


    def local_to_world(self, local_point):
        """
        Convert a point from the local system to the world system.

        :param local_point: A tuple (x, y) in the local coordinate system.
        :return: A tuple (x, y) in the world coordinate system.
        """
        local_x, local_y = local_point
        canvas_size = self.size()
        world_x = (local_x / canvas_size.width()) * self.world_rect.width + self.world_rect.x_min
        world_y = (1 - local_y / canvas_size.height()) * self.world_rect.height + self.world_rect.y_min
        return world_x, world_y

    def world_to_local(self, world_point):
        """
        Convert a point from the world system to the local system.

        :param world_point: A tuple (x, y) in the world coordinate system.
        :return: A tuple (x, y) in the local coordinate system.
        """
        world_x, world_y = world_point
        canvas_size = self.size()
        local_x = (world_x - self.world_rect.x_min) / self.world_rect.width * canvas_size.width()
        local_y = (1 - (world_y - self.world_rect.y_min) / self.world_rect.height) * canvas_size.height()
        return local_x, local_y

    def local_rect_to_world(self, local_rect):
        """
        Convert a rectangle from the local system to the world system.

        :param local_rect: A WorldRectangle in the local coordinate system.
        :return: A WorldRectangle in the world coordinate system.
        """
        x_min, y_min = self.local_to_world((local_rect.x_min, local_rect.y_min))
        x_max, y_max = self.local_to_world((local_rect.x_min + local_rect.width, local_rect.y_min + local_rect.height))
        return WorldRectangle(x_min, y_min, x_max - x_min, y_max - y_min)

    def world_rect_to_local(self, world_rect):
        """
        Convert a rectangle from the world system to the local system.

        :param world_rect: A WorldRectangle in the world coordinate system.
        :return: A WorldRectangle in the local coordinate system.
        """
        x_min, y_min = self.world_to_local((world_rect.x_min, world_rect.y_min))
        x_max, y_max = self.world_to_local((world_rect.x_min + world_rect.width, world_rect.y_min + world_rect.height))
        return WorldRectangle(x_min, y_min, x_max - x_min, y_max - y_min)

    def paintEvent(self, event):
        super().paintEvent(event)

        # Create a painter
        painter = QPainter(self)

        self.draw_layers(painter)

        # Set the pen for the border
        pen = QPen(QColor(0, 0, 0), 1)  # Black color, 1 pixel width
        painter.setPen(pen)

        # Draw the border
        rect = self.rect()
        painter.drawRect(rect.adjusted(0, 0, -1, -1))  # Adjust to draw inside the widget's boundary


    def draw_layers(self, painter):
        for layer in reversed(self.view.layers):
            print(f"Drawing layer {layer.name}")
            for item in reversed(layer.items):
                item.draw(painter, self)