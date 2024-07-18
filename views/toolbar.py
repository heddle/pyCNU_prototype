
from PyQt6.QtWidgets import (
    QToolButton, QToolBar,
    QButtonGroup
)

from PyQt6.QtGui import QAction, QIcon
from managers.imagemanager import ImageManager

class Toolbar(QToolBar):
    def __init__(self, view, attributes):
        super().__init__()
        self.attributes = attributes
        self.setOrientation(attributes.get("orientation", "horizontal"))
        self.setMovable(attributes.get("movable", True))
        self.setFloatable(attributes.get("floatable", True))
        self.setAllowedAreas(attributes.get("allowed_areas", "all"))
        self.setToolButtonStyle(attributes.get("tool_button_style", "tool_button_icon_only"))
        self.setIconSize(attributes.get("icon_size", "16x16"))

        view.addToolBar(self)

    # Button group for radio button-like behavior

        self.radio_button_group = QButtonGroup()
        self.radio_button_group.setExclusive(True)
      # Create actions for the radio buttons

        pointer = ImageManager.getInstance().get_image("pointer")
        pan = ImageManager.getInstance().get_image("pan")
        box_zoom = ImageManager.getInstance().get_image("box_zoom")

        self.pointer_action = QAction(QIcon(pointer), "Pointer", self)
        self.box_zoom_action = QAction(QIcon(box_zoom), "RButton1", self)
        self.pan_action = QAction(QIcon(pan), "RButton2", self)

        self.pointer_button = self.createToolButton(pointer)
        self.box_zoom_button = self.createToolButton(box_zoom)
        self.pan_button = self.createToolButton(pan)



    def radio_button_callback(self):
        sender = self.sender()
        print(f"{sender.text()} is activated")
    def createToolButton(self, pixmap):
        toolButton = QToolButton()
        toolButton.setIcon(QIcon(pixmap))
        toolButton.setCheckable(True)
        self.radio_button_group.addButton(toolButton)
        self.addWidget(toolButton)
        toolButton.clicked.connect(self.radio_button_callback)
        return toolButton
