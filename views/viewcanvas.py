from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QMouseEvent, QPalette, QColor, QPainter, QPen
from PyQt6.QtCore import Qt
import sys
from constants import BACKGROUND_COLOR, WIDTH, HEIGHT

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

        width = attributes.get(WIDTH, 800)
        height = attributes.get(HEIGHT, 600)
        self.setMinimumSize(width, height)  # Set a minimum size for the canvas

    def setStyle(self, attributes):
        # Create a palette
        palette = QPalette()

        # Set the background color (with alpha)  using the palette
        color_hex = attributes.get(BACKGROUND_COLOR, "#DDDDDD")
        color = QColor(color_hex)
        palette.setColor(QPalette.ColorRole.Window, color)
        # Apply the palette to the canvas
        self.setPalette(palette)

        # Enable auto-fill background
        self.setAutoFillBackground(True)

    def enterEvent(self, event):
        print("Mouse entered the canvas", file=sys.stderr)
        sys.stderr.flush()
        self.setMouseTracking(True)  # Enable mouse tracking when the mouse enters the canvas

    def leaveEvent(self, event):
        print("Mouse left the canvas", file=sys.stderr)
        sys.stderr.flush()
        self.setMouseTracking(False)  # Disable mouse tracking when the mouse leaves the canvas

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_dragging = True
            local_point = self.mapFromGlobal(event.globalPosition().toPoint())
            self.last_mouse_position = local_point
            world_point = self.view.local_to_world((local_point.x(), local_point.y()))
            self.view.status_bar.showMessage(f"Mouse Pressed at Local: {local_point}, World: {world_point}")
             # Add your custom logic here

    def mouseMoveEvent(self, event: QMouseEvent):
        local_point = self.mapFromGlobal(event.globalPosition().toPoint())
        world_point = self.view.local_to_world((local_point.x(), local_point.y()))
        self.view.status_bar.showMessage(f"Mouse Moved at Local: {local_point}, World: {world_point}")
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
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_dragging = False
            local_point = self.mapFromGlobal(event.globalPosition().toPoint())
            world_point = self.view.local_to_world((local_point.x(), local_point.y()))
            self.view.status_bar.showMessage(f"Mouse Released at Local: {local_point}, World: {world_point}")
            # Add your custom logic here

    def paintEvent(self, event):
        super().paintEvent(event)

        # Create a painter
        painter = QPainter(self)

        # Set the pen for the border
        pen = QPen(QColor(0, 0, 0), 1)  # Black color, 1 pixel width
        painter.setPen(pen)

        # Draw the border
        rect = self.rect()
        painter.drawRect(rect.adjusted(0, 0, -1, -1))  # Adjust to draw inside the widget's boundary
