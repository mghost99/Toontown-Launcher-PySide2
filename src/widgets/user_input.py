from PySide6.QtWidgets import QLineEdit


class UserInput(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(499, 172, 140, 18)