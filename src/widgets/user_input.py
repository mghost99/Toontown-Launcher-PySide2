from PyQt5.QtWidgets import QLineEdit

class UserInput(QLineEdit):
    def __init__(self, parent=None):
        super(UserInput, self).__init__(parent)
        
        # Setting the size and position of the text box
        self.setGeometry(499, 172, 140, 18)
