from items.item import Item
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPen, QPainter
from constants import WORLD_RECTANGLE
from world.worldrect import WorldRectangle

class RectangleItem(Item):
    def __init__(self, layer, attributes):
        super().__init__(layer, attributes)
        self.world_rect = attributes.get(WORLD_RECTANGLE, WorldRectangle(0, 0, 0, 0))

    def contains(self, world_point):
        return self.world_rect.contains(world_point)

    def custom_draw(self, canvas, painter):
        local_rect = canvas.world_rect_to_local(self.world_rect)
        painter.drawRect(local_rect)

    def get_selection_points(self):
        local_rect = self.get_view().canvas.world_rect_to_local(self.world_rect)
        right = local_rect.x() + local_rect.width()
        bottom = local_rect.y() + local_rect.height()
        return [(local_rect.x(), local_rect.y()), (right, local_rect.y()),
                (right, bottom), (local_rect.x(), bottom)]