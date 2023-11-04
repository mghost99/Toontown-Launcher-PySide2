from PyQt5.QtWidgets import QLineEdit


class UserInput(QLineEdit):
    def __init__(self, parent=None):
        super(UserInput, self).__init__(parent)
        self.setGeometry(499, 172, 140, 18)