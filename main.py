import sys
from environment import cwd
from mainwindow import MainWindow
from views.view import View
from world.worldrect import WorldRectangle
from constants import AUTO_CENTER, BACKGROUND_COLOR, BG_IMAGE_PATH, FRACTION, STATUS_BAR, \
    TITLE, TOOL_BAR, LEFT, TOP, WIDTH, HEIGHT, WORLD_RECTANGLE
from PyQt6.QtWidgets import QApplication

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
    attributes = {TITLE: "Demo View",
                  STATUS_BAR: True,
                  TOOL_BAR: True,
                  LEFT: 100,
                  TOP: 100,
                  WIDTH: 600,
                  HEIGHT: 600,
                  WORLD_RECTANGLE: WorldRectangle(-100, -100, 200, 200),
                  BACKGROUND_COLOR: "alice blue"}
    view = View(attributes)
    window.mdi.addSubWindow(view)
    window.show()  # IMPORTANT!!!!! Windows are hidden by default.

    layer = view.annotation_layer
    item = layer.add_item(attributes)


    # Start the event loop.
    sys.exit(app.exec())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
