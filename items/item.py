from abc import ABC, abstractmethod
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QBrush, QPainter, QPen
from util.x11colors import X11Colors
from constants import FILL_COLOR, LINE_COLOR, LINE_WIDTH, TEXT_COLOR


class Item(ABC):
    def __init__(self, layer, attributes):
        self.layer = layer
        self.attributes = attributes
        self._locked = False
        self._selected = False
        layer.add_item(self)

    @property
    def locked(self):
        """Return the locked status of the item"""
        return self._locked

    @locked.setter
    def locked(self, value):
        """Set the locked status of the item"""
        self._locked = value

    @property
    def selected(self):
        """Return the selected status of the item"""
        return self._selected

    @selected.setter
    def selected(self, value):
        """Set the selected status of the item"""
        self._selected = value

    def get_view(self):
        """Return the view of the layer, which is the view this item lives on"""
        return self.layer.view

    def get_fill_color(self) -> QColor:
        color_str = self.attributes.get(FILL_COLOR, None)
        if color_str:
            color = QColor(color_str) if color_str.startswith("#") else X11Colors.get_color(color_str)
        else:
            color = None
        return color

    def get_solid_brush(self) -> QBrush:
        """
        Return a solid brush with the fill color of the item.
        :return:  A solid brush with the fill color of the item.
        """
        color = self.get_fill_color()
        return QBrush(color) if color else QBrush(Qt.BrushStyle.NoBrush)

    def get_line_color(self) -> QColor:
        color_str = self.attributes.get(LINE_COLOR, "black")
        color = QColor(color_str) if color_str.startswith("#") else X11Colors.get_color(color_str)
        return color

    def get_line_width(self) -> int:
        return self.attributes.get(LINE_WIDTH, 1)

    def get_text_color(self) -> QColor:
        color_str = self.attributes.get(LINE_COLOR, "black")
        color = QColor(color_str) if color_str.startswith("#") else X11Colors.get_color(color_str)
        return color

    # abstract methods

    def draw(self, canvas):
        """Draw the item on the canvas"""
        painter = QPainter(canvas)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(self.get_solid_brush())
        painter.setPen(QPen(self.get_line_color(), self.get_line_width(), Qt.PenStyle.SolidLine))
        self.custom_draw(canvas, painter)

        if self.selected:
            self.draw_selection(canvas, painter)

    def draw_selection(self, canvas, painter):
        """Draw the selection points of the item"""
        painter.setPen(QPen(Qt.GlobalColor.black, 1, Qt.PenStyle.SolidLine))
        painter.setBrush(QBrush(Qt.GlobalColor.black, Qt.BrushStyle.SolidPattern))
        for point in self.get_selection_points():
            painter.drawRect(point[0] - 3, point[1] - 3, 6, 6)

    @abstractmethod
    def custom_draw(self, canvas, painter):
        """Draw the item on the canvas"""
        pass

    @abstractmethod
    def contains(self, world_point):
        """Return True if the item contains the world point, False otherwise"""
        pass

    @abstractmethod
    def get_selection_points(self):
        """Return the selection points of the item"""
        pass