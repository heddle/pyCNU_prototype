from PyQt6.QtGui import QAction


class ViewsMenuManager:
    def __init__(self, menu, mdi_area):
        self.menu = menu
        self.mdi_area = mdi_area
        self.view_actions = {}
        self.mdi_area.subWindowActivated.connect(self.update_menu)

    def add_view(self, view):
        action = QAction(view.windowTitle(), self.menu, checkable=True)
        action.setChecked(view.isVisible())
        action.toggled.connect(lambda checked, v=view: v.setVisible(checked))
        self.view_actions[view] = action
        self.menu.addAction(action)

    def remove_view(self, view):
        action = self.view_actions.pop(view, None)
        if action:
            self.menu.removeAction(action)

    def update_menu(self):
        for view, action in self.view_actions.items():
            action.setChecked(view.isVisible())

