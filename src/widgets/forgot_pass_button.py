from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QUrl, QSize
import webbrowser


class ForgotPassword(QPushButton):
    def __init__(self, parent=None, url=None):
        super(ForgotPassword, self).__init__(parent)
        self.setFixedSize(104, 13)
        self.setGeometry(508, 218, 140, 18)
        self.default_icon = QIcon("assets/buttons/FORGOT1U.png")
        self.hover_icon = QIcon("assets/buttons/FORGOT1D.png")  # Rollover (Hover)
        self.pressed_icon = QIcon("assets/buttons/FORGOT1D.png")  # Down

        # Setting the icon for the button
        self.setIcon(self.default_icon)
        self.setIconSize(QSize(122, 38))  # Setting the size of the icon

        # Connecting the button to the open_url method
        self.url = url
        self.clicked.connect(self.open_url)

        # Enabling mouse tracking to detect hover events
        self.setMouseTracking(True)

    def enterEvent(self, event):
        self.setIcon(self.hover_icon)

    def leaveEvent(self, event):
        self.setIcon(self.default_icon)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setIcon(self.pressed_icon)
        super(ForgotPassword, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.setIcon(self.hover_icon)
        super(ForgotPassword, self).mouseReleaseEvent(event)

    def setEnabled(self, enabled):
        super(ForgotPassword, self).setEnabled(enabled)
        if not enabled:
            self.setIcon(self.disabled_icon)
        else:
            self.hide()

    def open_url(self):
        webbrowser.open(self.url)
