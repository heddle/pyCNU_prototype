import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QMdiArea, QMdiSubWindow, QToolBar, QButtonGroup, QWidget, QVBoxLayout, QToolButton
)
from PyQt6.QtGui import QIcon, QAction
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

        # Button group for radio button-like behavior
        self.radio_button_group = QButtonGroup()
        self.radio_button_group.setExclusive(True)

        # Create QPixmap instances for the icons

        pointerPixMap = ImageManager.getInstance().get_image("pointer")
        box_zoomPixMap = ImageManager.getInstance().get_image("box_zoom")
        panPixMap = ImageManager.getInstance().get_image("pan")

        centerPixMap = ImageManager.getInstance().get_image("center")
        zoom_inPixMap = ImageManager.getInstance().get_image("zoom_in")
        zoom_outPixMap = ImageManager.getInstance().get_image("zoom_out")
        undo_zoomPixMap = ImageManager.getInstance().get_image("undo_zoom")
        worldPixMap = ImageManager.getInstance().get_image("world")


        # Create QToolButton instances for the radio buttons
        self.pointer_button = QToolButton()
        self.pointer_button.setIcon(QIcon(pointerPixMap))
        self.pointer_button.setCheckable(True)
        self.pointer_button.setText("Pointer")

        self.box_zoom_button = QToolButton()
        self.box_zoom_button.setIcon(QIcon(box_zoomPixMap))
        self.box_zoom_button.setCheckable(True)
        self.box_zoom_button.setText("box_zoom")

        self.pan_button = QToolButton()
        self.pan_button.setIcon(QIcon(panPixMap))
        self.pan_button.setCheckable(True)
        self.pan_button.setText("pan")


        # Add buttons to the button group
        self.radio_button_group.addButton(self.pointer_button)
        self.radio_button_group.addButton(self.box_zoom_button)
        self.radio_button_group.addButton(self.pan_button)

        # Add buttons to the toolbar
        toolbar.addWidget(self.pointer_button)
        toolbar.addWidget(self.box_zoom_button)
        toolbar.addWidget(self.pan_button)


        # Add the toolbar to the layout of the subwindow
        layout = QVBoxLayout(content_widget)
        layout.addWidget(toolbar)

        # Connect radio button actions to the same callback
        # self.pointer_button.click().connect(self.radio_button_callback)
        # self.box_zoom_button.click().connect(self.radio_button_callback)
        # self.pan_button.click().connect(self.radio_button_callback)

        # Create actions for regular buttons
        self.center_action = QAction(QIcon(centerPixMap), "center", self)
        self.world_action = QAction(QIcon(worldPixMap), "world", self)
        self.zoom_in_action = QAction(QIcon(zoom_inPixMap), "zoom_in", self)
        self.zoom_out_action = QAction(QIcon(zoom_outPixMap), "zoom_out", self)
        self.undo_zoom_action = QAction(QIcon(undo_zoomPixMap), "undo_zoom", self)

        # Add regular button actions to the toolbar
        toolbar.addAction(self.center_action)
        toolbar.addAction(self.world_action)
        toolbar.addAction(self.zoom_in_action)
        toolbar.addAction(self.zoom_out_action)
        toolbar.addAction(self.undo_zoom_action)

        # Connect regular button actions to their callbacks
        # self.center_action.triggered.connect(self.pbutton1_callback)
        # self.pbutton2_action.triggered.connect(self.pbutton2_callback)
        # self.pbutton3_action.triggered.connect(self.pbutton3_callback)
        # self.pbutton4_action.triggered.connect(self.pbutton4_callback)

    def radio_button_callback(self):
        sender = self.sender()
   #     print(f"{sender.nam} is activated")

    def pbutton1_callback(self):
        print("PButton1 is clicked")

    def pbutton2_callback(self):
        print("PButton2 is clicked")

    def pbutton3_callback(self):
        print("PButton3 is clicked")

    def pbutton4_callback(self):
        print("PButton4 is clicked")

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
