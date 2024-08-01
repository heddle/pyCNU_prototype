import sys

from PyQt6.QtWidgets import QApplication

from constants import AUTO_CENTER, BACKGROUND_COLOR, BG_IMAGE_PATH, FRACTION, \
    STATUS_BAR, TITLE, TOOL_BAR, LEFT, TOP, WIDTH, HEIGHT, WORLD_RECTANGLE, \
    LINE_WIDTH, LINE_COLOR, FILL_COLOR, VISIBLE

from environment import cwd
from mdiapplication.mainwindow import MainWindow
from views.view import View
from world.worldrect import WorldRectangle
from items.rectangleitem import RectangleItem

if __name__ == '__main__':
    print("Current Directory:", cwd())

    app = QApplication(sys.argv)

    # Define the attributes for the main window.
    attributes = {BG_IMAGE_PATH: "cnu",
                  AUTO_CENTER: True,
                  STATUS_BAR: True,
                  FRACTION: 0.9,
                  TITLE: "My Demo QT6 App"}

    # Create a QMainWindow which will be our window.
    window = MainWindow(attributes)

    # Create a sample view
    attributes = {TITLE: "Demo View 1",
                  VISIBLE: True,
                  STATUS_BAR: True,
                  TOOL_BAR: True,
                  LEFT: 100,
                  TOP: 100,
                  WIDTH: 600,
                  HEIGHT: 600,
                  WORLD_RECTANGLE: WorldRectangle(-100, -100, 250, 250),
                  BACKGROUND_COLOR: "alice blue"}
    view = View(window, attributes)


    layer = view.annotation_layer
    attributes = {LINE_COLOR: "blue",
                  LINE_WIDTH: 2,
                  FILL_COLOR: "yellow",
                  WORLD_RECTANGLE: WorldRectangle(0, 10, 50, 70)}
    RectangleItem(layer, attributes)

    layer = view.top_layer
    attributes = {LINE_COLOR: "wheat",
                  LINE_WIDTH: 1,
                  FILL_COLOR: "#dd4455",
                  WORLD_RECTANGLE: WorldRectangle(20, 30, 80, 80)}
    RectangleItem(layer, attributes)

    # Create another sample view not shown at startup
    attributes = {TITLE: "Demo View 2",
                  VISIBLE: False,
                  STATUS_BAR: True,
                  TOOL_BAR: True,
                  LEFT: 400,
                  TOP: 400,
                  WIDTH: 400,
                  HEIGHT: 400,
                  WORLD_RECTANGLE: WorldRectangle(0, 0, 1, 1),
                  BACKGROUND_COLOR: "peach puff"}
    view = View(window, attributes)

    window.show()  # IMPORTANT!!!!! Windows are hidden by default.

    # Start the event loop.
    sys.exit(app.exec())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
