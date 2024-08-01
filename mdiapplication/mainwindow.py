from PyQt6.QtWidgets import QMainWindow, QStatusBar, QMenu
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QAction
from constants import AUTO_CENTER, FRACTION, STATUS_BAR, TITLE
from custommdi import CustomMdiArea
from managers.viewsmenumanager import ViewsMenuManager


class MainWindow(QMainWindow):
    # singleton pattern
    _instance = None
    menu_bar = None
    file_menu = None
    views_menu = None
    views_manager = None

    # singleton pattern
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

        # create a status bar?
        if attributes.get(STATUS_BAR, False):
            self.status_bar = QStatusBar(self)
            self.setStatusBar(self.status_bar)
            self.status_bar.setStyleSheet("QStatusBar { background-color: white; }")

            self.status_bar.showMessage("Ready")

        # create the menus
        self._create_menus()

        # Call the after_init method after the __init__ completes
        QTimer.singleShot(0, self.after_init)

    def after_init(self):
        print("Initialization is complete. This method runs after __init__.")

    def _create_menus(self):
        self.menu_bar = self.menuBar()
        self.menu_bar.setNativeMenuBar(False)
        self.create_file_menu()
        self.create_views_menu()

    def create_file_menu(self):
        self.file_menu = self.menu_bar.addMenu("File")

        # Exit action
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.exit_app)
        quit_action.setShortcut("Ctrl+Q")
        self.file_menu.addAction(quit_action)

    def create_views_menu(self):
        self.views_menu = QMenu('Views')
        self.menu_bar.addMenu(self.views_menu)
        self.views_manager = ViewsMenuManager(self.views_menu, self.mdi)

    def exit_app(self):
        self.close()

    @staticmethod
    def get_instance():
        return MainWindow._instance
