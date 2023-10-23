from PyQt5.QtWebEngineWidgets import QWebEngineView

class ThemedWebView(QWebEngineView):
    def __init__(self, theme_data, parent=None):
        super().__init__(parent)
        self.default_icon = None
        self.apply_theme(theme_data)

    def apply_theme(self, theme_data):
        # Setting view size
        size = theme_data.get('size', {})
        self.setFixedSize(size.get('width', 100), size.get('height', 30))
        
        # Setting view position
        position = theme_data.get('position', {})
        self.move(position.get('x', 400), position.get('y', 165))