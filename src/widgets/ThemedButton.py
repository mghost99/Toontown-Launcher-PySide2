from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize, QEvent
from PyQt5.QtGui import QIcon

class ThemedButton(QPushButton):
    def __init__(self, theme_data, parent=None):
        super().__init__(parent)
        self.default_icon = None
        self.hover_icon = None
        self.pressed_icon = None
        self.disabled_icon = None
        self.is_disabled = False
        self.apply_theme(theme_data)
        if not self.is_disabled:
            self.setIcon(self.default_icon)
            self.installEventFilter(self)
        else:
            self.setIcon(self.disabled_icon)

    def apply_theme(self, theme_data):
        # Setting button size
        size = theme_data.get('size', {})
        self.setFixedSize(size.get('width', 100), size.get('height', 30))
        
        # Setting button position
        position = theme_data.get('position', {})
        self.move(position.get('x', 0), position.get('y', 0))
        
        # Setting button icons
        icons = theme_data.get('icons', {})
        self.default_icon = QIcon(icons.get('default'))
        self.hover_icon = QIcon(icons.get('hover', icons.get('disabled')))
        self.pressed_icon = QIcon(icons.get('pressed', icons.get('disabled')))
        self.disabled_icon = QIcon(icons.get('disabled', icons.get('disabled')))
        self.setIconSize(QSize(size.get('width', 100), size.get('height', 30)))


    def set_disabled(self, bool):
        self.is_disabled = bool        

    def eventFilter(self, obj, event):
        if self.is_disabled:
            return False
        else:
            if obj == self:
                if event.type() == QEvent.HoverEnter:
                    self.setIcon(self.hover_icon)
                elif event.type() == QEvent.HoverLeave:
                    self.setIcon(self.default_icon)
                elif event.type() == QEvent.MouseButtonPress:
                    self.setIcon(self.pressed_icon)
                elif event.type() == QEvent.MouseButtonRelease:
                    self.setIcon(self.hover_icon)
            return super().eventFilter(obj, event)
