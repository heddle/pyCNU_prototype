from items.item import Item
from PyQt6.QtCore import QRect, QPoint, QPointF, Qt
from PyQt6.QtGui import QPolygonF
from constants import WORLD_POLYGON, CLOSED  # Assuming these are defined in the constants module
from typing_extensions import override
class PolygonItem(Item):
    def __init__(self, layer, attributes):
        # Call the parent class constructor
        super().__init__(layer, attributes)

        # Extract the QPolygonF from the attributes dictionary using the WORLD_POLYGON constant
        self.world_polygon = attributes.get(WORLD_POLYGON, QPolygonF())

        # Extract the closed flag from the attributes dictionary using the CLOSED constant
        # Default to True if the CLOSED key is not present
        self.is_closed = attributes.get(CLOSED, True)

    @override
    def contains_local(self, q_point: QPoint) -> bool:
        """
        Check if the given QPoint is contained within the polygon.

        :param q_point: QPoint to check
        :return: True if the point is contained within the polygon, False otherwise
        """
        world_point = self.get_view().canvas.local_to_world(q_point)
        return self.contains_world(world_point)


    @override
    def contains_world(self, q_point: QPointF) -> bool:
        """
        Check if the given QPointF is contained within the polygon.

        :param q_point: QPointF to check
        :return: True if the point is contained within the polygon, False otherwise
        """
        return self.world_polygon.containsPoint(q_point, Qt.FillRule.WindingFill)

    @override
    def get_bounds(self) -> QRect:
        local_polygon = self.get_view().canvas.world_polygon_to_local(self.world_polygon)
        return local_polygon.boundingRect()

    @override
    def custom_draw(self, canvas, painter):
        local_polygon = canvas.world_polygon_to_local(self.world_polygon)

        if (self.is_closed):
            print("Drawing polygon")
            painter.drawPolygon(local_polygon)
        else:
            print("Drawing polyline")
            painter.drawPolyline(local_polygon)

    @override
    def move(self, dx: float, dy: float):
        self.world_polygon.translate(dx, dy)


    @override
    def get_selection_points(self):
        local_polygon = self.get_view().canvas.world_polygon_to_local(self.world_polygon)
        selection_points = []
        for i in range(local_polygon.size()):
            point = local_polygon.at(i)
            selection_points.append((point.x(), point.y()))
        return selection_points

    def __repr__(self):
        return (f"PolygonItem(layer={self.layer}, polyg"
                f"polygon={self.polygon}, is_closed={self.is_closed})")