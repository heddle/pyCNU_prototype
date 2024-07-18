from PyQt6.QtGui import QPainter, QColor, QPen
from PyQt6.QtCore import Qt
class Item:
    def __init__(self, layer, attributes):
        self.layer = layer
        self._attributes = attributes

    @property
    def attributes(self):
        return self._attributes

    def get_view(self):
        return self.layer.view

    def draw(self, painter, canvas):
        painter.setPen(QPen(Qt.GlobalColor.red, 1, Qt.PenStyle.SolidLine))
        painter.drawRect(50, 50, 100, 100)

