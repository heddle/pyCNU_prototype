from abc import ABC, abstractmethod
from PyQt6.QtCore import Qt, QRect, QPoint, QPointF
from PyQt6.QtGui import QMouseEvent, QPalette, QColor, QPainter, QPen, QPolygonF, QPolygon


class Transform():
    def __init__(self):
        super().__init__()

    @abstractmethod
    def local_to_world(self, local_point: QPoint) -> QPointF:
        """
        Convert a point from the local system to the world system.

        :param local_point: A point in the local pixel coordinate system.
        :return: A point in the world coordinate system.
        """
        pass;

    @abstractmethod
    def world_to_local(self, world_point: QPointF) -> QPoint:
        """
        Convert a point from the world system to the local system.

        :param world_point: A point in the world coordinate system.
        :return: A point in the local pixel coordinate system.
        """
        pass;

    @abstractmethod
    def local_to_world_rect(self, local_rect: QRect) -> QRect:
        """
        Convert a rectangle from the local system to the world system.

        :param local_rect: A rectangle in the local pixel coordinate system.
        :return: A rectangle in the world coordinate system.
        """
        pass;

    @abstractmethod
    def world_to_local_rect(self, world_rect: QRect) -> QRect:
        """
        Convert a rectangle from the world system to the local system.

        :param world_rect: A rectangle in the world coordinate system.
        :return: A rectangle in the local pixel coordinate system.
        """
        pass;

    @abstractmethod
    def local_to_world_polygon(self, local_polygon: QPolygon) -> QPolygon:
        """
        Convert a polygon from the local system to the world system.

        :param local_polygon: A polygon in the local pixel coordinate system.
        :return: A polygon in the world coordinate system.
        """
        pass;

    @abstractmethod
    def world_to_local_polygon(self, world_polygon: QPolygon) -> QPolygon:
        """
        Convert a polygon from the world system to the local system.

        :param world_polygon: A polygon in the world coordinate system.
        :return: A polygon in the local pixel coordinate system.
        """
        pass;