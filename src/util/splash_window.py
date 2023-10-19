from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QBitmap
from PyQt5.QtWidgets import QApplication, QSplashScreen, QProgressBar, QLabel, QDesktopWidget
import urllib
import requests

class SplashScreen(QSplashScreen):
    def __init__(self):
        super().__init__(QPixmap("assets/backgrounds/SPLASH.png"))
        qmask = QPixmap("assets/masks/SPLASH.png")
        self.setMask(qmask.mask())
        self.progressBar = QProgressBar(self)
        self.progressBar.setGeometry(130, 200, 250, 25)
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.progressLabel = QLabel('Setting remote variables...', self)
        self.progressLabel.setAlignment(Qt.AlignCenter)
        self.progressLabel.move(180, 180)

        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def update_progress_bar(self, progress):
        self.progressBar.setValue(progress)

    def set_progress(self, value):
        self.progressBar.setValue(value)

    def load_remote_urls(self):
        urls = {}
        default_url = "http://download.sunrise.games/launcher/"
        base_url = default_url
        variables_to_extract = [
        "PATCHER_VERSION_STRING_SERVER",
        "PATCHER_VERSION_STRING_SERVER_OSK",
        "GAME_VERSION_TEXT",
        "DOWNLOAD_PATCHER_CURRENT_VERSION",
        "DOWNLOAD_PATCHER_CURRENT_VERSION_OSX",
        "GAME_WHITELIST_URL",
        "GAME_IN_GAME_NEWS_URL",
        "GAME_SERVER",
        "ADDITIONAL_VERSION_TEXT",
        "ACCOUNT_SERVER",
        "PANDA_DOWNLOAD_URL",
        "PATCHER_BASE_URL_HEAVY_LIFTING",
        "WEB_PAGE_LOGIN_RPC"
    ]
        try:
            with open('parameters.txt', 'r') as file:
                lines = file.readlines()
                for line in lines:
                    key, sep, value = line.partition('=')
                    if key.strip() == 'PATCHER_BASE_URL' and sep:
                        base_url = value.strip()
                        break
        except FileNotFoundError:
            print("parameters.txt file not found. Using default URL.")
        if not base_url.endswith('/'):
            base_url += '/'
        try:
            remote_url = urllib.parse.urljoin(base_url, 'patcher.startshow')
            response = requests.get(remote_url)
            if response.status_code == 200:
                lines = response.text.splitlines()
                for line in lines:
                    line = line.split('#')[0].strip()
                    if line:
                        key, sep, url = line.partition('=')
                        if sep:
                            urls[key.strip()] = url.strip()
            remote_url_ver = urllib.parse.urljoin(base_url, 'patcher.ver')
            response_ver = requests.get(remote_url_ver)
            if response_ver.status_code == 200:
                lines = response_ver.text.splitlines()
                for line in lines:
                    line = line.split('#')[0].strip()
                    key, sep, value = line.partition('=')
                    key = key.strip()
                    if key in variables_to_extract and sep:
                        urls[key] = value.strip()
            else:
                raise requests.exceptions.RequestException("Invalid URL")
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch the remote file: {e}")
            QApplication.quit()
        urls['BASE_URL'] = base_url
        return urls