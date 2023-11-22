import json
from urllib.parse import urlencode
import requests
import http.client
from PySide2.QtCore import QThread, Signal


class Authenticator(QThread):
    callback = Signal(dict)

    def __init__(self, urls, credentials):
        super().__init__()
        self.urls = urls
        self.credentials = credentials

    def run(self):
        self.connection = http.client.HTTPSConnection("sunrise.games", 443)
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "User-Agent": "PySide2 - Disney's Toontown Online Launcher"}
        username, password = self.credentials
        params = urlencode({
            "username": username.encode("utf-8"),
            "password": password.encode("utf-8"),
            "serverType": "Final Toontown",
        })
        self.connection.request("POST", "/api/login/alt/", params, headers)
        try:
            response = self.connection.getresponse()
        except http.client.BadStatusLine:
            response = {"errorCode": 1, "message": "API - Bad Status. Try again."}
        else:
            if response.status == http.client.SERVICE_UNAVAILABLE:
                response = {"errorCode": 1, "message": "API is unavailable. Try again later."}
            if response.status != http.client.OK:
                response = {"errorCode": 1, "message": "API - Non-OK response. Try again."}
            try:
                response = json.loads(response.read())
            except ValueError:
                response = {"errorCode": 1, "message": "API - Bad JSON response. Try again."}
        success = response.get("success", 'False')
        self.connection.close()
        self.connection = None
        if success == 'True':
            self.callback.emit(response)
        else:
            self.callback.emit(response)