from PyQt5.QtCore import QThread
import requests

class Authenticator(QThread):

    def __init__(self, urls, username="", password="", callback=None):
        super().__init__()
        self.urls = urls
        self.username = username
        self.password = password
        self.callback = callback

    def run(self):
        endpoint = "https://sunrise.games/api/login/alt/"
        data = {
            "username": self.username,
            "password": self.password,
            "serverType": "Final Toontown",
        }
        webHeaders = {"User-Agent": "PyQt5 - Disney's Toontown Online Launcher"}

        try:
            response = requests.post(
                endpoint, data=data, headers=webHeaders, timeout=10
            ).json()
        except Exception as e:
            response = {"errorCode": 1, "message": str(e)}

        # Call the callback method with the response
        self.callback(response)
