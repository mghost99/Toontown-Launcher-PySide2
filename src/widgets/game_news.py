from PyQt5.QtWidgets import QFrame, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl


class GameNews(QWebEngineView):
    def __init__(self, parent, url, **kwargs):
        super(GameNews, self).__init__(parent)
        self.load(QUrl(url))
        self.setFixedSize(315, 350)
        self.move(35, 75)
