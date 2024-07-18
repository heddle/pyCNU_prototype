
from PyQt6.QtWidgets import (
    QToolButton, QToolBar,
    QButtonGroup
)

from constants import POINTER, BOX_ZOOM, PAN
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from managers.imagemanager import ImageManager

class Toolbar(QToolBar):
    def __init__(self, view, attributes):
        super().__init__()
        self.view = view
        self.attributes = attributes

        # Button group for radio button-like behavior
        self.radio_button_group = QButtonGroup()
        self.radio_button_group.setExclusive(True)

        self.pointer_button = self.createRadioButton(self.radio_button_group, self.radio_button_callback, POINTER)
        self.box_zoom_button = self.createRadioButton(self.radio_button_group, self.radio_button_callback, BOX_ZOOM)
        self.pan_button = self.createRadioButton(self.radio_button_group, self.radio_button_callback, PAN)
        self.pointer_button.setChecked(True)
        self.active_button = self.pointer_button.text()

        self.center_button = self.createPushButton(self.center_callback, "center")
        self.zoom_in_button = self.createPushButton(self.zoom_in_callback, "zoom_in")
        self.zoom_out_button = self.createPushButton(self.zoom_out_callback, "zoom_out")
        self.undo_zoom_button = self.createPushButton(self.undo_zoom_callback, "undo_zoom")
        self.world_button = self.createPushButton(self.world_callback, "world")

    def createPushButton(self, callback, name):
        pixmap = ImageManager.getInstance().get_image(name)
        button = QToolButton()
        button.setIcon(QIcon(pixmap))
        button.setCheckable(True)
        button.setFixedSize(24, 24)  # Fixed size
        button.setText(name)
        self.addWidget(button)

        button.clicked.connect(lambda: callback(name))
        return button
    def createRadioButton(self, buttonGroup, callback, name):
        button = self.createPushButton(callback, name)
        buttonGroup.addButton(button)
        return button

    def radio_button_callback(self, name):
        self.active_button = name
        print(self.active_button + " is activated ")

    def center_callback(self, name):
        print(name + " is clicked")

    def zoom_in_callback(self, name):
        print(name + " is clicked")

    def zoom_out_callback(self, name):
        print(name + " is clicked")

    def undo_zoom_callback(self, name):
        print(name + " is clicked")

    def world_callback(self, name):
        print(name + " is clicked")

    def get_cursor(self):
        if self.active_button == POINTER:
            return Qt.CursorShape.ArrowCursor
        elif self.active_button == BOX_ZOOM:
            return Qt.CursorShape.CrossCursor
        elif self.active_button == PAN:
            return Qt.CursorShape.ClosedHandCursor
        else:
            return Qt.CursorShape.ArrowCursor

    def set_default_cursor(self):
        self.view.setCursor(Qt.CursorShape.ArrowCursor)

    def get_active_radiobutton(self):
        for button in self.radio_button_group.buttons():
            if button.isChecked():
                return button.text()
        return None

