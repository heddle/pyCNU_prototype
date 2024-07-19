from __future__ import annotations
class WorldRectangle:
    def __init__(self, x_min, y_min, width, height):
        self.x_min = float(x_min)
        self.y_min = float(y_min)
        self.width = float(width)
        self.height = float(height)

    def copy(self) -> WorldRectangle:
        """
        Create a copy of the rectangle.
        :return: a new WorldRectangle object.
        """
        return WorldRectangle(self.x_min, self.y_min, self.width, self.height)

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

    def contains(self, point):
        px, py = point
        return (self.x_min <= px <= self.x_min + self.width) and (self.y_min <= py <= self.y_min + self.height)

    def move(self, dx, dy):
        self.x_min += float(dx)
        self.y_min += float(dy)

    def resize(self, new_width, new_height):
        self.width = float(new_width)
        self.height = float(new_height)

    def center(self):
        return self.x_min + self.width / 2, self.y_min + self.height / 2

    def scale(self, factor):
        """
        Scale the rectangle by a factor. Keep the center of the rectangle the same.
        :param factor: the factor to scale the rectangle by.
        :return: None
        """
        xc, yc = self.center()
        self.width *= factor
        self.height *= factor
        self.x_min = xc - self.width / 2
        self.y_min = yc - self.height / 2

    def intersects(self, other):
        return not (self.x_min > other.x_min + other.width or
                    self.x_min + self.width < other.x_min or
                    self.y_min > other.y_min + other.height or
                    self.y_min + self.height < other.y_min)

    def __eq__(self, other):
        if isinstance(other, WorldRectangle):
            return (self.x_min == other.x_min and self.y_min == other.y_min and
                    self.width == other.width and self.height == other.height)
        return False

    def __repr__(self):
        return f"Rectangle(x={self.x_min}, y={self.y_min}, width={self.width}, height={self.height})"
