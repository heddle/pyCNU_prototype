from abc import ABC, abstractmethod
from PyQt6.QtCore import Qt, QRect, QPoint
from PyQt6.QtWidgets import QMenu, QColorDialog
from PyQt6.QtGui import QColor, QBrush, QPainter, QPen, QAction, QMouseEvent
from util.x11colors import X11Colors
from constants import FILL_COLOR, LINE_COLOR, LINE_WIDTH, DELETABLE, \
    DRAGGABLE, SELECTABLE, RESIZABLE, ROTATABLE
from dialogs.customcolordialog import CustomColorDialog


class Item(ABC):
    def __init__(self, layer, attributes):
        self.layer = layer
        self.attributes = attributes
        self._locked = False
        self._selected = False
        layer.add_item(self)

        self._deletable = attributes.get(DELETABLE, True)
        self._draggable = attributes.get(DRAGGABLE, True)
        self._selectable = attributes.get(SELECTABLE, True)
        self._resizable = attributes.get(RESIZABLE, True)
        self._rotatable = attributes.get(ROTATABLE, True)

    @property
    def deletable(self):
        """Return the deletable status of the item"""
        return self._deletable

    @deletable.setter
    def deletable(self, value):
        """Set the deletable status of the item"""
        self._deletable = value

    @property
    def draggable(self):
        """Return the draggable status of the item"""
        return self._draggable

    @draggable.setter
    def draggable(self, value):
        """Set the draggable status of the item"""
        self._draggable = value

    @property
    def selectable(self):
        """Return the selectable status of the item"""
        return self._selectable

    @selectable.setter
    def selectable(self, value):
        """Set the selectable status of the item"""
        self._selectable = value

    @property
    def resizable(self):
        """Return the resizable status of the item"""
        return self._resizable

    @resizable.setter
    def resizable(self, value):
        """Set the resizable status of the item"""
        self._resizable = value

    @property
    def rotatable(self):
        """Return the rotatable status of the item"""
        return self._rotatable

    @rotatable.setter
    def rotatable(self, value):
        """Set the rotatable status of the item"""
        self._rotatable = value

    @property
    def locked(self):
        """Return the locked status of the item"""
        return self._locked

    @locked.setter
    def locked(self, value):
        """Set the locked status of the item"""
        self._locked = value

    @property
    def selected(self):
        """Return the selected status of the item"""
        return self._selected

    @selected.setter
    def selected(self, value):
        """Set the selected status of the item"""
        self._selected = value

    def get_view(self):
        """Return the view of the layer, which is the view this item lives on"""
        return self.layer.view

    def get_fill_color(self) -> QColor:
        color_str = self.attributes.get(FILL_COLOR, None)
        if color_str:
            color = QColor(color_str) if color_str.startswith("#") else X11Colors.get_color(color_str)
        else:
            color = None
        return color

    def get_solid_brush(self) -> QBrush:
        """
        Return a solid brush with the fill color of the item.
        :return:  A solid brush with the fill color of the item.
        """
        color = self.get_fill_color()
        return QBrush(color) if color else QBrush(Qt.BrushStyle.NoBrush)

    def get_line_color(self) -> QColor:
        color_str = self.attributes.get(LINE_COLOR, "black")
        color = QColor(color_str) if color_str.startswith("#") else X11Colors.get_color(color_str)
        return color

    def get_line_width(self) -> int:
        return self.attributes.get(LINE_WIDTH, 1)

    def get_text_color(self) -> QColor:
        color_str = self.attributes.get(LINE_COLOR, "black")
        color = QColor(color_str) if color_str.startswith("#") else X11Colors.get_color(color_str)
        return color

    # abstract methods

    def draw(self, canvas):
        """Draw the item on the canvas"""
        painter = QPainter(canvas)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(self.get_solid_brush())
        painter.setPen(QPen(self.get_line_color(), self.get_line_width(), Qt.PenStyle.SolidLine))
        self.custom_draw(canvas, painter)

        if self.selected:
            self.draw_selection(painter)

    def draw_selection(self, painter):
        print("Drawing selection")
        """Draw the selection points of the item"""
        painter.setPen(QPen(Qt.GlobalColor.black, 1, Qt.PenStyle.SolidLine))
        painter.setBrush(QBrush(Qt.GlobalColor.white, Qt.BrushStyle.SolidPattern))
        for point in self.get_selection_points():
            painter.drawRect(point[0] - 4, point[1] - 4, 8, 8)

    def enclosed_by(self, q_rect: QRect):
        """Return True if the item is enclosed by the local
        pixel rectangle, False otherwise"""
        return q_rect.contains(self.get_bounds())

    def context_menu(self, event: QMouseEvent):
        """Show the context menu for the item"""
        print("Context menu for item")
        menu = QMenu()

        canvas = self.get_view().canvas
        change_line_width_action = QAction("Change Line Width", canvas)
        change_line_style_action = QAction("Change Line Style", canvas)
        change_line_color_action = QAction("Change Line Color", canvas)
        change_fill_color_action = QAction("Change Fill Color", canvas)
        bring_to_front_action = QAction("Bring to Front", canvas)
        bring_forward_action = QAction("Bring Forward", canvas)
        send_to_back_action = QAction("Send to Back", canvas)
        send_backward_action = QAction("Send Backward", canvas)

        change_line_width_action.triggered.connect(self.change_line_width)
        change_line_style_action.triggered.connect(self.change_line_style)
        change_line_color_action.triggered.connect(self.change_line_color)
        change_fill_color_action.triggered.connect(self.change_fill_color)
        bring_to_front_action.triggered.connect(self.bring_to_front)
        bring_forward_action.triggered.connect(self.bring_forward)
        send_to_back_action.triggered.connect(self.send_to_back)
        send_backward_action.triggered.connect(self.send_backward)

        menu.addAction(change_line_width_action)
        menu.addAction(change_line_style_action)
        menu.addAction(change_line_color_action)
        menu.addAction(change_fill_color_action)
        menu.addSeparator()
        menu.addAction(bring_to_front_action)
        menu.addAction(bring_forward_action)
        menu.addAction(send_to_back_action)
        menu.addAction(send_backward_action)
        menu.exec(event.globalPosition().toPoint())

    def change_line_width(self):
        # Implement the logic to change line width
        print("Change Line Width selected")

    def change_line_style(self):
        # Implement the logic to change line style
        print("Change Line Style selected")

    def change_line_color(self):

        canvas = self.get_view().canvas
        initial_color = self.get_line_color()
        ccd = CustomColorDialog(initial_color, canvas)

        color = ccd.getColor()
        if color.isValid():
            self.attributes[LINE_COLOR] = color.name()
            canvas.update()

        print("Change Line Color selected")

    def change_fill_color(self):
        canvas = self.get_view().canvas
        initial_color = self.get_fill_color()
        color = QColorDialog.getColor(initial_color, canvas, "Select Color with Alpha",
                                      QColorDialog.ColorDialogOption.ShowAlphaChannel)

        if color.isValid():
            print(f'Selected color: {color.name()} with alpha: {color.alpha()}')
            hex_color = "#{:02X}{:02X}{:02X}{:02X}".format(color.alpha(), color.red(), color.green(), color.blue())
            self.attributes[FILL_COLOR] = hex_color
            canvas.update()
        print("Change Fill Color selected")

    def bring_to_front(self):
        print("Bring to Front selected")

    def bring_forward(self):
        print("Bring Forward selected")

    def send_to_back(self):
        print("Send to Back selected")

    def send_backward(self):
        print("Send Backward selected")

    @abstractmethod
    def custom_draw(self, canvas, painter):
        """Draw the item on the canvas"""
        pass

    @abstractmethod
    def move(self, dx: float, dy: float):
        """Move the item by the given world deltas"""
        pass

    @abstractmethod
    def get_bounds(self) -> QRect:
        """Return the bounding rectangle (local pixel coordinates) of the item"""
        pass

    def contains(self, q_point: QPoint):
        """Return True if the item contains the world point, False otherwise"""
        pass

    @abstractmethod
    def get_selection_points(self):
        """Return the selection points of the item"""
        pass
