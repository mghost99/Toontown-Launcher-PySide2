import webbrowser

from PySide6.QtCore import QSize, QUrl, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton


class TopToons(QPushButton):
    def __init__(self, parent=None, url=None):
        super().__init__(parent)
        self.setFixedSize(122, 38)
        self.move(378, 460)
        self.url = url
        self.default_icon = QIcon("assets/buttons/COMMUNITY1U.png")
        self.hover_icon = QIcon("assets/buttons/COMMUNITY1R.png")
        self.pressed_icon = QIcon("assets/buttons/COMMUNITY1D.png")
        self.disabled_icon = QIcon("assets/buttons/COMMUNITY1G.png")
        self.setIcon(self.default_icon)
        self.setIconSize(QSize(122, 38))
        self.clicked.connect(self.open_url)
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

    def open_url(self):
        webbrowser.open(self.url)
