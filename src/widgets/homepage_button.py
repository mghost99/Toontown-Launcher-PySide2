from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QUrl, QSize
import webbrowser


class Homepage(QPushButton):
    def __init__(self, parent=None, url=None):
        super(Homepage, self).__init__(parent)

        # Setting the icon for the button
        self.setIcon(QIcon("assets/buttons/HOMEPAGE1U.png"))
        self.setIconSize(QSize(122, 38))  # Setting the size of the icon

        # Setting the size of the button
        self.setFixedSize(122, 38)

        # Positioning the button
        self.move(253, 460)

        # Setting the icons for different button states
        self.default_icon = QIcon("assets/buttons/HOMEPAGE1U.png")
        self.hover_icon = QIcon(
            "assets/buttons/HOMEPAGE1R.png")  # Rollover (Hover)
        self.pressed_icon = QIcon("assets/buttons/HOMEPAGE1D.png")  # Down
        self.disabled_icon = QIcon(
            "assets/buttons/HOMEPAGE1G.png")  # Disabled (Greyed)

        # Setting the icon for the button
        self.setIcon(self.default_icon)
        self.setIconSize(QSize(122, 38))  # Setting the size of the icon

        # Setting the URL to be opened
        self.url = url
        self.clicked.connect(self.open_url)

        # TODO: Disable buttons without variables set.
        self.is_enabled = True

        # Enabling mouse tracking to detect hover events
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
        super(Homepage, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self.is_enabled:
            self.setIcon(self.hover_icon)
        super(Homepage, self).mouseReleaseEvent(event)

    def is_disabled(self):
        self.setIcon(self.disabled_icon)

    def open_url(self):
        webbrowser.open(self.url)
