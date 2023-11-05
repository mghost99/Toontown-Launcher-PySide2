from PySide6.QtCore import QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QFrame, QVBoxLayout


class GameNews(QWebEngineView):
    def __init__(self, parent, url, **kwargs):
        super().__init__(parent)
        self.load(QUrl(url))
        self.setFixedSize(315, 350)
        self.move(35, 75)
