import sys

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QMdiArea, QMdiSubWindow, QToolBar, QButtonGroup, QWidget, QVBoxLayout, QToolButton
)

from managers.imagemanager import ImageManager


class MdiSubWindow(QMdiSubWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MdiSubWindow Example")
        self.initUI()

    def initUI(self):
        # Create the toolbar
        toolbar = QToolBar("Toolbar")
        content_widget = QWidget()  # Set an empty widget to hold the toolbar and layout
        self.setWidget(content_widget)

        # Add the toolbar to the layout
        layout = QVBoxLayout(content_widget)
        layout.addWidget(toolbar)

        # Button group for radio button-like behavior
        self.radio_button_group = QButtonGroup()
        self.radio_button_group.setExclusive(True)

        self.pointer_button = self.createRadioButton(toolbar, self.radio_button_group, self.radio_button_callback,
                                                     "pointer")
        self.box_zoom_button = self.createRadioButton(toolbar, self.radio_button_group, self.radio_button_callback,
                                                      "box_zoom")
        self.pan_button = self.createRadioButton(toolbar, self.radio_button_group, self.radio_button_callback, "pan")

        self.center_button = self.createPushButton(toolbar, self.center_callback, "center")
        self.zoom_in_button = self.createPushButton(toolbar, self.zoom_in_callback, "zoom_in")
        self.zoom_out_button = self.createPushButton(toolbar, self.zoom_out_callback, "zoom_out")
        self.undo_zoom_button = self.createPushButton(toolbar, self.undo_zoom_callback, "undo_zoom")
        self.world_button = self.createPushButton(toolbar, self.world_callback, "world")

    def createPushButton(self, toolbar, callback, name):
        pixmap = ImageManager.getInstance().get_image(name)
        button = QToolButton()
        button.setIcon(QIcon(pixmap))
        button.setCheckable(True)
        button.setFixedSize(24, 24)  # Fixed size
        toolbar.addWidget(button)

        button.clicked.connect(lambda: callback(name))
        return button

    def createRadioButton(self, toolbar, buttonGroup, callback, name):
        pixmap = ImageManager.getInstance().get_image(name)
        button = QToolButton()
        button.setIcon(QIcon(pixmap))
        button.setCheckable(True)
        button.setFixedSize(24, 24)  # Fixed size
        buttonGroup.addButton(button)
        toolbar.addWidget(button)

        button.clicked.connect(lambda: callback(name))
        return button

    def radio_button_callback(self, name):
        print(name + " is activated")

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

    def get_active_radiobutton(self):
        for button in self.radio_button_group.buttons():
            if button.isChecked():
                return button.text()
        return None


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MDI Example")
        self.mdi = QMdiArea()
        self.setCentralWidget(self.mdi)

        sub = MdiSubWindow()
        self.mdi.addSubWindow(sub)
        sub.show()


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
