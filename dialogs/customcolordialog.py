from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QColorDialog, QDialog, QVBoxLayout, QSlider,
    QLabel, QDialogButtonBox)


class CustomColorDialog(QColorDialog):
    def __init__(self, initial_color=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Choose Color")

        # Create a QColorDialog without the dialog buttons
        self.setOptions(QColorDialog.ColorDialogOption.ShowAlphaChannel)

        if initial_color:
            self.setCurrentColor(initial_color)

        self.setFocus()  # Ensure the dialog has focus
