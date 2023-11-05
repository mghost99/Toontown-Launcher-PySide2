from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt, QSize


class Play(QPushButton):
    def __init__(self, command, parent=None):
        super().__init__(parent)
        self.default_icon = QIcon("assets/buttons/PLAY1U.png")
        self.hover_icon = QIcon("assets/buttons/PLAY1R.png")
        self.pressed_icon = QIcon("assets/buttons/PLAY1D.png")
        self.disabled_icon = QIcon("assets/buttons/PLAY1G.png")
        self.setIcon(self.default_icon)
        icon_size = QSize(85, 36)
        self.setIconSize(self.icon().actualSize(icon_size))
        self.setGeometry(653, 170, 85, 36)
        self.clicked.connect(command)
        self.setMouseTracking(True)

    def enterEvent(self, event):
        self.setIcon(self.hover_icon)

    def leaveEvent(self, event):
        self.setIcon(self.default_icon)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setIcon(self.pressed_icon)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.setIcon(self.hover_icon)
        super().mouseReleaseEvent(event)

    def setEnabled(self, enabled):
        super().setEnabled(enabled)
        if not enabled:
            self.setIcon(self.disabled_icon)
        else:
            self.setIcon(self.default_icon)
