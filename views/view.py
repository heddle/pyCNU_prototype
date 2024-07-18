from PyQt6.QtWidgets import QMdiSubWindow, QVBoxLayout, QStatusBar, QWidget
from PyQt6.QtGui import QFontMetrics, QFont
from views.layer import Layer

from views.viewcanvas import ViewCanvas
from constants import LEFT, TOP, TITLE, TOOL_BAR, GLASS_LAYER, ANNOTATION_LAYER
from views.toolbar import Toolbar

class View(QMdiSubWindow):

    def __init__(self, attributes: dict):
        super().__init__()
        self.attributes = attributes
        self.layers = []

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
            self.createStatusBar()

        self.glassLayer = self.add_layer(GLASS_LAYER)  # Add the glass layer on init
        self.annotation_layer = self.add_layer(ANNOTATION_LAYER)  # Add the glass layer on init

        # Set the position of the view
        left = attributes.get(LEFT, 20)
        top = attributes.get(TOP, 20)
        self.move(left, top)

     #check if there is a staus bar
    def hasStatusBar(self):
        return self.status_bar is not None

    #create the status bar
    def createStatusBar(self):
        self.status_bar = QStatusBar()

        # Create a QFont object
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.status_bar.setFont(font)

        # Get the height of one line of text
        font_metrics = QFontMetrics(font)
        text_height = font_metrics.height()

        # Set the fixed height of the status bar to match one line of text
        self.status_bar.setFixedHeight(text_height + 4)  # Add some padding for better appearance
        self.status_bar.setStyleSheet("QStatusBar { background-color: #111111; \
        color: cyan; border: 1px solid black; }")
        self.layout.addWidget(self.status_bar)


    def get_attributes(self):
        return self.attributes

    def add_layer(self, name: str):
        if any(layer.name == name for layer in self.layers):
            raise ValueError(f"Layer with name {name} already exists.")
        layer = Layer(view=self, name=name)
        self.layers.append(layer)
        return layer

    def remove_layer(self, name: str):
        if name == GLASS_LAYER or name == ANNOTATION_LAYER:
            raise ValueError(f"Cannot remove the {name}.")
        self.layers = [layer for layer in self.layers if layer.name != name]
