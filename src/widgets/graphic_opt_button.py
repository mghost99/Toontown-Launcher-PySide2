from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize


class GraphicOptions(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setIcon(QIcon("assets/buttons/GRAPHICSOPTIONS1G.png"))
        self.setIconSize(QSize(122, 38))
        self.setFixedSize(122, 38)
        self.move(499, 460)

        self.clicked.connect(self.graphic_options)

    def graphic_options(self):
        print("TODO: Graphics Option Menu")
