from PyQt5.QtWidgets import QLineEdit


class PassInput(QLineEdit):
    def __init__(self, command, parent=None):
        super(PassInput, self).__init__(parent)
        self.setFixedSize(140, 18)
        self.move(499, 195)
        self.setEchoMode(QLineEdit.Password)
        self.returnPressed.connect(command)
