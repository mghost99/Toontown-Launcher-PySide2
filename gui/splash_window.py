from urllib.parse import urljoin

import requests
from PySide2.QtCore import QThread, Qt, Signal, Slot
from PySide2.QtGui import QBitmap, QGuiApplication, QPixmap
from PySide2.QtWidgets import QLabel, QProgressBar, QSplashScreen


class URLLoaderThread(QThread):
    progress_updated = Signal(int)
    finished = Signal(dict)
    error_occurred = Signal(str)

    def __init__(self, base_url, variables_to_extract):
        super().__init__()
        self.base_url = base_url
        self.variables_to_extract = variables_to_extract

    def run(self):
        urls = {}
        progress = 0
        self.progress_updated.emit(progress)

        try:
            remote_url = urljoin(self.base_url, "patcher.startshow")
            response = requests.get(remote_url)
            if response.status_code == 200:
                lines = response.text.splitlines()
                for line in lines:
                    line = line.split("#")[0].strip()
                    if line:
                        key, sep, url = line.partition("=")
                        if sep:
                            urls[key.strip()] = url.strip()
            else:
                raise requests.exceptions.RequestException(
                    "Invalid response from server"
                )

            progress += 50
            self.progress_updated.emit(progress)

            remote_url_ver = urljoin(self.base_url, "patcher.ver")
            response_ver = requests.get(remote_url_ver)
            if response_ver.status_code == 200:
                lines = response_ver.text.splitlines()
                for line in lines:
                    line = line.split("#")[0].strip()
                    key, sep, value = line.partition("=")
                    key = key.strip()
                    if key in self.variables_to_extract and sep:
                        urls[key] = value.strip()
            else:
                raise requests.exceptions.RequestException(
                    "Invalid response from server"
                )

            progress += 50
            self.progress_updated.emit(progress)

            urls["BASE_URL"] = self.base_url
            self.finished.emit(urls)

        except requests.exceptions.RequestException as e:
            self.error_occurred.emit(str(e))


class SplashScreen(QSplashScreen):
    def __init__(self):
        super().__init__(QPixmap("assets/backgrounds/SPLASH.png"))
        qmask = QPixmap("assets/masks/SPLASH.png")
        self.setMask(qmask.mask())
        self.progressBar = QProgressBar(self)
        self.progressBar.setGeometry(130, 200, 250, 25)
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.progressLabel = QLabel("Setting remote variables...", self)
        self.progressLabel.setAlignment(Qt.AlignCenter)
        self.progressLabel.move(180, 180)
        self.center()

        base_url = "http://download.sunrise.games/launcher/"
        variables_to_extract = [
            "PATCHER_VERSION_STRING_SERVER",
            "PATCHER_VERSION_STRING_SERVER_OSX",
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
            "WEB_PAGE_LOGIN_RPC",
        ]

        self.url_loader_thread = URLLoaderThread(base_url, variables_to_extract)
        self.url_loader_thread.progress_updated.connect(self.set_progress)
        self.url_loader_thread.finished.connect(self.on_urls_loaded)
        self.url_loader_thread.error_occurred.connect(self.on_error)
        self.url_loader_thread.start()

    def center(self):
        qr = self.frameGeometry()
        cp = QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    @Slot(int)
    def set_progress(self, value):
        self.progressBar.setValue(value)

    @Slot(dict)
    def on_urls_loaded(self, urls):
        self.close()
        # ... open the main window ...

    @Slot(str)
    def on_error(self, error_message):
        print(f"Failed to fetch the remote file: {error_message}")
        QGuiApplication.quit()
