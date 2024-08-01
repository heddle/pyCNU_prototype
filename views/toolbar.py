from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QToolButton, QToolBar,
    QButtonGroup
)

from constants import POINTER, BOX_ZOOM, PAN, CENTER, ZOOM_IN, ZOOM_OUT, UNDO, WORLD
from managers.imagemanager import ImageManager


class Toolbar(QToolBar):
    def __init__(self, view, attributes):
        super().__init__()
        self.view = view
        self.attributes = attributes

        # Button group for radio button-like behavior
        self.radio_button_group = QButtonGroup()
        self.radio_button_group.setExclusive(True)

        self.pointer_button = self.create_radio_button(self.radio_button_group, self.radio_button_callback,
                                                       POINTER, "Selector tool")
        self.box_zoom_button = self.create_radio_button(self.radio_button_group, self.radio_button_callback, BOX_ZOOM,
                                                        "Rubber-band zoom")
        self.pan_button = self.create_radio_button(self.radio_button_group, self.radio_button_callback,
                                                   PAN, "Pan the view")
        self.center_button = self.create_radio_button(self.radio_button_group, self.radio_button_callback, CENTER,
                                                      "Recenter the view")
        self.pointer_button.setChecked(True)

        self.zoom_in_button = self.create_push_button(self.zoom_in_callback, ZOOM_IN, "Zoom in by a fixed factor")
        self.zoom_out_button = self.create_push_button(self.zoom_out_callback, ZOOM_OUT, "Zoom out by a fixed factor")
        self.undo_button = self.create_push_button(self.undo_callback, UNDO, "Undo the last world operation")
        self.world_button = self.create_push_button(self.world_callback, WORLD, "Restore the default world")

    def create_push_button(self, callback, name, tooltip=None):
        pixmap = ImageManager.get_instance().get_image(name)
        button = QToolButton()
        button.setIcon(QIcon(pixmap))
        button.setCheckable(False)
        button.setFixedSize(24, 24)  # Fixed size
        button.setText(name)

        if tooltip:
            button.setToolTip(tooltip)
        self.addWidget(button)

        button.clicked.connect(lambda: callback(name))
        return button

    def create_radio_button(self, button_group, callback, name, tooltip=None):
        button = self.create_push_button(callback, name, tooltip)
        button.setCheckable(True)
        button_group.addButton(button)
        return button

    def radio_button_callback(self, name):
        pass

    def zoom_in_callback(self, name):
        self.view.canvas.zoom_in()
        self.set_default_button()

    def zoom_out_callback(self, name):
        self.view.canvas.zoom_out()
        self.set_default_button()

    def undo_callback(self, name):
        self.view.canvas.undo_zoom()
        self.set_default_button()

    def world_callback(self, name):
        self.view.canvas.restore_default_world()
        self.set_default_button()

    def get_cursor(self):
        active_button = self.get_active_radiobutton()
        if active_button == POINTER:
            return Qt.CursorShape.ArrowCursor
        elif active_button == BOX_ZOOM:
            return Qt.CursorShape.CrossCursor
        elif active_button == PAN:
            return Qt.CursorShape.OpenHandCursor
        elif active_button == CENTER:
            return Qt.CursorShape.PointingHandCursor
        else:
            return Qt.CursorShape.ArrowCursor

    def set_default_button(self):
        self.pointer_button.setChecked(True)
        self.set_default_cursor()

    def set_default_cursor(self):
        self.view.setCursor(Qt.CursorShape.ArrowCursor)

    def get_active_radiobutton(self):
        for button in self.radio_button_group.buttons():
            if button.isChecked():
                return button.text()
        return None
