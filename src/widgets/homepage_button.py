import webbrowser

from PySide6.QtCore import QSize, QUrl, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton


class Homepage(QPushButton):
    def __init__(self, parent=None, url=None):
        super().__init__(parent)
        self.default_icon = QIcon("assets/buttons/HOMEPAGE1U.png")
        self.hover_icon = QIcon("assets/buttons/HOMEPAGE1R.png")
        self.pressed_icon = QIcon("assets/buttons/HOMEPAGE1D.png")
        self.disabled_icon = QIcon("assets/buttons/HOMEPAGE1G.png")
        self.setIcon(self.default_icon)
        self.setIconSize(QSize(122, 38))
        self.setFixedSize(122, 38)
        self.move(253, 460)
        self.url = url
        self.clicked.connect(self.open_url)
        # TODO: Disable buttons without variables set.
        self.is_enabled = True
        self.setMouseTracking(True)

    def enterEvent(self, event):
        if self.is_enabled:
            self.setIcon(self.hover_icon)

    def leaveEvent(self, event):
        if self.is_enabled:
            self.setIcon(self.default_icon)

    def mousePressEvent(self, event):
        if self.is_enabled:
            if event.button() == Qt.LeftButton:
                self.setIcon(self.pressed_icon)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self.is_enabled:
            self.setIcon(self.hover_icon)
        super().mouseReleaseEvent(event)

    def is_disabled(self):
        self.setIcon(self.disabled_icon)

    def open_url(self):
        webbrowser.open(self.url)
