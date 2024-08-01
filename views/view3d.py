from PyQt6.QtWidgets import QSizePolicy, QApplication, QMainWindow, QMdiArea, QMdiSubWindow
from PyQt6.QtOpenGLWidgets import QOpenGLWidget

class View3D(QMdiSubWindow):
    def __init__(self, main_window: MainWindow, attributes: dict, parent=None):
        super().__init__(parent)
        self.canvas = OpenGLCanvas()
        self.setWidget(self.canvas)
        self.setWindowTitle("3D View")