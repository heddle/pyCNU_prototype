from PyQt6.QtGui import QPainter, QColor, QPen
from PyQt6.QtCore import Qt
from constants import FILL_COLOR, LINE_COLOR, LINE_WIDTH, TEXT_COLOR
class Item:
    def __init__(self, layer, attributes):
        self.layer = layer
        self._attributes = attributes

    @property
    def attributes(self):
        return self._attributes

    def get_view(self):
        """Return the view of the layer, which is the view this item lives on"""
        return self.layer.view

    def draw(self, painter, canvas):
        painter.setPen(QPen(Qt.GlobalColor.red, 1, Qt.PenStyle.SolidLine))
        painter.drawRect(50, 50, 100, 100)

    def get_fill_color(self):
        return self.attributes.get(FILL_COLOR, None)

    def get_line_color(self):
        return self.attributes.get(LINE_COLOR, None)

    def get_line_width(self):
        return self.attributes.get(LINE_WIDTH, 1)

    def get_text_color(self):
        return self.attributes.get(TEXT_COLOR, QColor(Qt.GlobalColor.black))

