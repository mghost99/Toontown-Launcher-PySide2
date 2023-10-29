from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize


class TMin(QPushButton):
    def __init__(self, parent=None):
        super(TMin, self).__init__(parent)

        # Setting the size of the button
        self.setFixedSize(19, 19)

        # Positioning the button
        self.move(685, 1)

        # Setting the icons for different button states
        self.default_icon = QIcon("assets/buttons/TMIN1U.png")
        self.hover_icon = QIcon(
            "assets/buttons/TMIN1D.png")  # Rollover (Hover)
        self.pressed_icon = QIcon("assets/buttons/TMIN1D.png")  # Down

        # Setting the icon for the button
        self.setIcon(self.default_icon)
        self.setIconSize(QSize(122, 38))  # Setting the size of the icon

        # Connecting the button to the open_url method
        self.clicked.connect(self.minimize)

        # Enabling mouse tracking to detect hover events
        self.setMouseTracking(True)

    def enterEvent(self, event):
        self.setIcon(self.hover_icon)

    def leaveEvent(self, event):
        self.setIcon(self.default_icon)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setIcon(self.pressed_icon)
        super(TMin, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.setIcon(self.hover_icon)
        super(TMin, self).mouseReleaseEvent(event)

    def setEnabled(self, enabled):
        super(TMin, self).setEnabled(enabled)
        if not enabled:
            self.setIcon(self.disabled_icon)
        else:
            self.hide()

    def minimize(self):
        # Define what happens when the minimize button is clicked
        self.window().showMinimized()
