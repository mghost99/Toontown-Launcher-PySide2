from PySide6.QtCore import QSize
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel


class LiPrompt(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPixmap(QPixmap("assets/LIPROMPT.png"))
        self.setFixedSize(QSize(98, 52))
        self.move(400, 165)
