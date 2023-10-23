from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QSize

class ThemedLineEdit(QLineEdit):
    def __init__(self, theme_data, parent=None):
        super().__init__(parent)
        self.password = False
        self.apply_theme(theme_data)

    def apply_theme(self, theme_data):
        # Setting label size
        size = theme_data.get('size', {})
        self.setFixedSize(size.get('width', 100), size.get('height', 30))
        
        # Setting label position
        position = theme_data.get('position', {})
        self.move(position.get('x', 0), position.get('y', 0))

        # Password?
        password = theme_data.get('password', False)
        if password:
            self.setEchoMode(QLineEdit.Password)
