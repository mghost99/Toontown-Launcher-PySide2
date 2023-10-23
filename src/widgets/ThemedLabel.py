from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QSize

class ThemedLabel(QLabel):
    def __init__(self, theme_data, parent=None):
        super().__init__(parent)
        self.default_icon = None
        self.apply_theme(theme_data)

    def apply_theme(self, theme_data):
        # Setting label size
        size = theme_data.get('size', {})
        self.setFixedSize(size.get('width', 100), size.get('height', 30))
        
        # Setting label position
        position = theme_data.get('position', {})
        self.move(position.get('x', 400), position.get('y', 165))
        
        # Setting label icons
        icons = theme_data.get('icons', {})
        self.default_icon = QPixmap(icons.get('default'))
        self.setPixmap(self.default_icon)