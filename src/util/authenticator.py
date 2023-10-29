from PyQt5.QtCore import QThread, pyqtSignal
import requests


class Authenticator(QThread):
    progress_signal = pyqtSignal(int)
    authentication_signal = pyqtSignal(dict)

    def __init__(self, urls, username, password):
        super().__init__()
        self.urls = urls
        self.username = username
        self.password = password

    def run(self):
        # self.urls['WEB_PAGE_LOGIN_RPC']
        endpoint = "https://sunrise.games/api/login/alt/"
        data = {
            "username": self.username,
            "password": self.password,
            "serverType": "Final Toontown",
        }
        webHeaders = {"User-Agent": "PyQt5 - Disney's Toontown Online Launcher"}

        request = requests.post(
            endpoint, data=data, headers=webHeaders, timeout=10
        ).json()
        self.authentication_signal.emit(request)
