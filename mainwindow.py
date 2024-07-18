from PyQt6.QtWidgets import QMainWindow, QStatusBar
from custommdi import CustomMdiArea
from constants import AUTO_CENTER, FRACTION, STATUS_BAR, TITLE
from managers.imagemanager import ImageManager

class MainWindow(QMainWindow):
    # singleton pattern
    _instance = None

    #singleton pattern
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(MainWindow, cls).__new__(cls)
        return cls._instance

    def __init__(self, attributes):
        super().__init__()

        # singleton pattern
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True

        # save the attributes
        self.attributes = attributes

        # make mdi capable window
        self.mdi = CustomMdiArea(self.attributes)
        self.setCentralWidget(self.mdi)


        # get the attributes from the attributes dictionary
        # get the title of the window
        title = attributes.get(TITLE, "My App")
        self.setWindowTitle(title)

        # get the screen size
        screen = self.screen()
        screen_size = screen.size()
        screen_width = screen_size.width()
        screen_height = screen_size.height()

        # see if we use fractional sizing or fixed size
        fraction = attributes.get(FRACTION, 0)

        if fraction > 0.01:
            width = int(screen_width * fraction)
            height = int(screen_height * fraction)
        else:
            width = attributes.get("width", 800)
            height = attributes.get("height", 600)

        # auto center the window?
        auto_center = attributes.get(AUTO_CENTER, False)
        if auto_center:
            # center the window
            left = (screen_width - width) // 2
            top = (screen_height - height) // 2
        else:
            left = attributes.get("left", 100)
            top = attributes.get("top", 100)

        # set the size and location of the window
        self.setGeometry(left, top, width, height)

        status_bar = attributes.get(STATUS_BAR, False)
        if status_bar:
            self.statusBar = QStatusBar()
            self.setStatusBar(self.statusBar)
            self.statusBar.setStyleSheet("QStatusBar { background-color: white; }")

            self.statusBar.showMessage("Ready")

    def initManagers(self):
        self.image_manager = ImageManager()