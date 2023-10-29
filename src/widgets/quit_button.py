from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize


class Quit(QPushButton):
    def __init__(self, parent=None):
        super(Quit, self).__init__(parent)

        # Setting the size of the button
        self.setFixedSize(122, 38)

        # Positioning the button
        self.move(620, 460)

        # Setting the icons for different button states
        self.default_icon = QIcon("assets/buttons/QUIT1U.png")
        self.hover_icon = QIcon(
            "assets/buttons/QUIT1R.png")  # Rollover (Hover)
        self.pressed_icon = QIcon("assets/buttons/QUIT1D.png")  # Down
        self.disabled_icon = QIcon(
            "assets/buttons/QUIT1G.png")  # Disabled (Greyed)

        # Setting the icon for the button
        self.setIcon(self.default_icon)
        self.setIconSize(QSize(122, 38))  # Setting the size of the icon

        # Connecting the button to the quit_app method
        self.clicked.connect(self.quit_app)

        # Enabling mouse tracking to detect hover events
        self.setMouseTracking(True)

    def enterEvent(self, event):
        self.setIcon(self.hover_icon)

    def leaveEvent(self, event):
        self.setIcon(self.default_icon)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setIcon(self.pressed_icon)
        super(Quit, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.setIcon(self.hover_icon)
        super(Quit, self).mouseReleaseEvent(event)

    def setEnabled(self, enabled):
        super(Quit, self).setEnabled(enabled)
        if not enabled:
            self.setIcon(self.disabled_icon)
        else:
            self.setIcon(self.default_icon)

    def quit_app(self):
        # Define what happens when the quit button is clicked
        exit()
