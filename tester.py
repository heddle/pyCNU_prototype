from PyQt6.QtWidgets import QSizePolicy, QApplication, QMainWindow, QMdiArea, QMdiSubWindow
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtCore import QSize, Qt

class OpenGLCanvas(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Setting size policy to be expandable in both directions
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def minimumSizeHint(self):
        # Provide a sensible minimum size for the widget to ensure it's visible
        return QSize(100, 100)

    def initializeGL(self):
        # Initialize OpenGL stuff here
        pass

    def paintGL(self):
        # Rendering logic here
        pass

    def resizeGL(self, width, height):
        # Handle resizing of the OpenGL context
        pass

class View3D(QMdiSubWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.canvas = OpenGLCanvas()
        self.setWidget(self.canvas)
        self.setWindowTitle("3D View")

# Application setup
app = QApplication([])
window = QMainWindow()
mdi_area = QMdiArea()
window.setCentralWidget(mdi_area)

view_3d = View3D()
mdi_area.addSubWindow(view_3d)
view_3d.show()

window.show()
app.exec()
