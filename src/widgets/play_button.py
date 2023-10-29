from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize


class Play(QPushButton):
    def __init__(self, command, parent=None):
        super(Play, self).__init__(parent)
        self.default_icon = QIcon("assets/buttons/PLAY1U.png")
        self.hover_icon = QIcon(
            "assets/buttons/PLAY1R.png")  # Rollover (Hover)
        self.pressed_icon = QIcon("assets/buttons/PLAY1D.png")  # Down
        self.disabled_icon = QIcon(
            "assets/buttons/PLAY1G.png")  # Disabled (Greyed)

        # Set the default button icon
        self.setIcon(self.default_icon)

        # Define the desired icon size
        # You can adjust the width and height values as needed
        icon_size = QSize(85, 36)

        # Set the icon size
        self.setIconSize(self.icon().actualSize(icon_size))

        # Set button geometry
        self.setGeometry(653, 170, 85, 36)

        # Connecting the button to the command
        self.clicked.connect(command)

        # Enabling mouse tracking to detect hover events
        self.setMouseTracking(True)

    def enterEvent(self, event):
        self.setIcon(self.hover_icon)

    def leaveEvent(self, event):
        """Revert the icon when the mouse leaves the button."""
        self.setIcon(self.default_icon)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setIcon(self.pressed_icon)
        super(Play, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        """Revert the icon when the button is released."""
        self.setIcon(self.hover_icon)
        super(Play, self).mouseReleaseEvent(event)

    def setEnabled(self, enabled):
        super(Play, self).setEnabled(enabled)
        if not enabled:
            self.setIcon(self.disabled_icon)
        else:
            self.setIcon(self.default_icon)
