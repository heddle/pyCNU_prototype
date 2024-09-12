from items.item import Item
from PyQt6.QtCore import QRect, QPoint, QPointF
from constants import WORLD_RECTANGLE
from world.worldrect import WorldRectangle
from typing_extensions import override

class RectangleItem(Item):
    def __init__(self, layer, attributes):
        super().__init__(layer, attributes)
        self.world_rect = attributes.get(WORLD_RECTANGLE, WorldRectangle(0, 0, 0, 0))


    @override
    def contains_local(self, q_point: QPoint) -> bool:
        local_rect = self.get_view().canvas.world_rect_to_local(self.world_rect)
        return local_rect.contains(q_point)

    @override
    def contains_world(self, q_point: QPointF) -> bool:
        return self.world_rect.contains_local(q_point)

    @override
    def custom_draw(self, canvas, painter):
        local_rect = canvas.world_rect_to_local(self.world_rect)
        painter.drawRect(local_rect)

    @override
    def move(self, dx:float, dy:float):
        self.world_rect.move(dx, dy)

    @override
    def get_bounds(self) -> QRect:
        q_rect = self.get_view().canvas.world_rect_to_local(self.world_rect)
        return q_rect

    @override
    def get_selection_points(self):
        local_rect = self.get_view().canvas.world_rect_to_local(self.world_rect)
        right = local_rect.x() + local_rect.width()
        bottom = local_rect.y() + local_rect.height()
        return [(local_rect.x(), local_rect.y()), (right, local_rect.y()),
                (right, bottom), (local_rect.x(), bottom)]