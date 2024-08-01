from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QMdiArea

from constants import BG_IMAGE_PATH
from managers.imagemanager import ImageManager


class CustomMdiArea(QMdiArea):
    def __init__(self, attributes, parent=None):
        super().__init__(parent)
        # tile a background image?
        bg_image = str(attributes.get(BG_IMAGE_PATH))
        if bg_image:
            image = ImageManager.get_instance().get_image(bg_image)
            if image:
                self.background_image = image

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self.viewport())
        tile_width = self.background_image.width()
        tile_height = self.background_image.height()

        for x in range(0, self.width(), tile_width):
            for y in range(0, self.height(), tile_height):
                painter.drawPixmap(x, y, self.background_image)
