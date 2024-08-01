from PyQt6.QtCore import QRect
from PyQt6.QtGui import QFontMetrics, QFont
from PyQt6.QtWidgets import QMdiSubWindow, QVBoxLayout, QStatusBar, QWidget
from PyQt6.QtCore import QEvent, Qt

from constants import LEFT, TOP, TITLE, TOOL_BAR, TOP_LAYER, MIDDLE_LAYER,\
    BOTTOM_LAYER, ANNOTATION_LAYER
from views.layer import Layer
from views.toolbar import Toolbar
from views.viewcanvas import ViewCanvas
from mdiapplication.mainwindow import MainWindow


class View(QMdiSubWindow):

    def __init__(self, main_window: MainWindow, attributes: dict, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.attributes = attributes
        self.layers = []

        self.setWindowFlags(Qt.WindowType.Dialog)

        # Create a central widget and set a layout
        central_widget = QWidget()

        self.setWidget(central_widget)
        self.layout = QVBoxLayout(central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        self.layout.setSpacing(0)  # Remove spacing

        # Add a toolbar?
        if attributes.get(TOOL_BAR, False):
            self.toolbar = Toolbar(self, attributes)
            self.layout.addWidget(self.toolbar)

        # Create the canvas and add it to the layout
        self.canvas = ViewCanvas(self, attributes)
        self.layout.addWidget(self.canvas)

        self.setWindowTitle(attributes.get(TITLE, "View"))  # Set the title of the view

        # Create the status bar and add it to the layout
        if attributes.get("status_bar", False):
            self.status_bar = self.create_status_bar()

        # add the default layers
        self.__annotation_layer = self.add_layer(ANNOTATION_LAYER)  # Add the annotation layer on init
        self.__top_layer = self.add_layer(TOP_LAYER)  # Add the top layer on init
        self.__middle_layer = self.add_layer(MIDDLE_LAYER)  # Add the middle layer on init
        self.__bottom_layer = self.add_layer(BOTTOM_LAYER)  # Add the bottom layer on init

        # Set the position of the view
        left = attributes.get(LEFT, 20)
        top = attributes.get(TOP, 20)
        self.move(left, top)

        main_window.mdi.addSubWindow(self)

        # visible?
        visible = attributes.get("visible", True)
        if visible:
            self.show()
        else:
            self.hide()

        main_window.views_manager.add_view(self)

    @property
    def annotation_layer(self):
        return self.__annotation_layer

    @property
    def top_layer(self):
        return self.__top_layer

    @property
    def middle_layer(self):
        return self.__middle_layer

    @property
    def bottom_layer(self):
        return self.__bottom_layer

    # check if there is a status bar
    def has_status_bar(self):
        return self.status_bar is not None

    # create the status bar
    def create_status_bar(self):
        """ Create a status bar for the view.
        :return: The status bar."""
        status_bar = QStatusBar()

        # Create a QFont object
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        status_bar.setFont(font)

        # Get the height of one line of text
        font_metrics = QFontMetrics(font)
        text_height = font_metrics.height()

        # Set the fixed height of the status bar to match one line of text
        status_bar.setFixedHeight(text_height + 4)  # Add some padding for better appearance
        status_bar.setStyleSheet("QStatusBar { background-color: #111111; \
        color: cyan; border: 1px solid black; }")
        self.layout.addWidget(status_bar)
        return status_bar

    def resizeEvent(self, event):
        super().resizeEvent(event)
        new_size = event.size()
        self.canvas.resize(new_size.width(), new_size.height())
        rect = QRect(0, 0, new_size.width(), new_size.height())
        self.canvas.zoom_to_rect(rect)
        print(f"SubWindow resized to: {new_size.width()}x{new_size.height()}")

    def add_layer(self, name: str):
        """ Add a layer to the view.
        :param name: The name of the layer.
        :return: The layer."""

        if any(layer.name == name for layer in self.layers):
            raise ValueError(f"Layer with name {name} already exists.")
        layer = Layer(view=self, name=name)
        self.layers.append(layer)
        return layer

    def remove_layer(self, name: str):
        if name == ANNOTATION_LAYER:
            raise ValueError(f"Cannot remove the {name}.")
        self.layers = [layer for layer in self.layers if layer.name != name]

    def closeEvent(self, event):
        pass

    def showEvent(self, event):
        super().showEvent(event)

    def hideEvent(self, event):
        print("Window is hidden")
        MainWindow.get_instance().views_manager.update_menu()
        super().hideEvent(event)

    def changeEvent(self, event):
        pass
