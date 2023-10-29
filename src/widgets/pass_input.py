from PyQt5.QtWidgets import QLineEdit


class PassInput(QLineEdit):
    def __init__(self, parent=None):
        super(PassInput, self).__init__(parent)

        # Setting the size of the password input field
        self.setFixedSize(140, 18)

        # Positioning the password input field
        self.move(499, 195)

        # Set as Password field
        self.setEchoMode(QLineEdit.Password)
