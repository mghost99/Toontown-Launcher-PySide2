import webbrowser

from PySide6.QtCore import QSize, QUrl, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton


class ForgotPassword(QPushButton):
    def __init__(self, parent=None, url=None):
        super().__init__(parent)
        self.setFixedSize(104, 13)
        self.setGeometry(508, 218, 140, 18)
        self.default_icon = QIcon("assets/buttons/FORGOT1U.png")
        self.hover_icon = QIcon("assets/buttons/FORGOT1D.png")
        self.pressed_icon = QIcon("assets/buttons/FORGOT1D.png")
        self.setIcon(self.default_icon)
        self.setIconSize(QSize(122, 38))
        self.url = url
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
            self.hide()

    def open_url(self):
        webbrowser.open(self.url)
