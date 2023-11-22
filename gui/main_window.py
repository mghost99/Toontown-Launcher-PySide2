import json
import os
import platform
import subprocess
import sys
import threading
import time
import stat

from PySide2.QtCore import QMutex, QObject, QMetaObject, QPoint, QTimer, Qt, Signal, Slot, QThread, QUrl, QSize
from PySide2.QtGui import QColor, QFont, QGuiApplication, QPixmap
from PySide2.QtWidgets import QLabel, QMainWindow, QProgressBar, QLineEdit, QGraphicsView, QGraphicsScene, QGraphicsScene
from PySide2.QtWebEngineWidgets import QWebEngineView

from util import Updater, Authenticator
from gui.buttons import *

import logging

def resource_path(filename):
    #Intended for local installs and snap applications
    if os.getenv("LAUNCHER_RESOURCES") is not None:
        # check if the file exists
        _path = os.path.join(os.getenv("LAUNCHER_RESOURCES"), filename)
        if os.path.exists(_path):
            return _path
    _path = os.path.join(".", filename)
    return _path


class ConfigManager:
    def __init__(self, config_file, default_config=None):
        self.config_file = config_file
        self.default_config = default_config or {}

    def save_config(self, _data):
        with open(self.config_file, "w") as f:
            json.dump(_data, f, indent=4)

    def load_config(self):
        if os.path.exists(self.config_file):
            logging.info("Loading configuration...")
            with open(self.config_file, "r") as f:
                return json.load(f)
        else:
            logging.info("Configuration file not found, creating with default...")
            self.save_config(self.default_config)
            return self.default_config

    def update_config(self, _key, _value):
        config = self.load_config()
        config[_key] = _value
        self.save_config(config)

    def get_config_value(self, _key, default=None):
        config = self.load_config()
        return config.get(_key, default)

class MainWindow(QMainWindow):
    auth_signal = Signal(dict)

    def __init__(self, launcher_urls, use_old=False):
        super().__init__()
        self.credentials = {}
        self.original_cwd = os.getcwd()
        self.config_file = os.path.join(self.original_cwd, "launcher.json")
        self.default_config = {"username": None}
        self.config_manager = ConfigManager(self.config_file, self.default_config)
        self.urls = launcher_urls if launcher_urls else {}
        self.authenticator = Authenticator(urls=self.urls, credentials=self.credentials)
        self.authenticator.callback.connect(self.handle_authentication)
        self.auth_signal.connect(self.update_authentication_status)
        self.update_thread = None
        self.winTitle = "Toontown Online"
        self.setWindowTitle(self.winTitle)
        self.setGeometry(100, 100, 750, 500)
        self.setFixedSize(750, 500)
        self.background = QLabel(self)
        self.use_old = use_old
        if self.use_old:
            pixmap = QPixmap(resource_path("resources/old/backgrounds/background.jpg"))
        else:
            self.setWindowFlags(Qt.FramelessWindowHint)
            pixmap = QPixmap(resource_path("resources/backgrounds/background.png"))
        self.background.setPixmap(pixmap)
        self.background.resize(750, 500)
        if not self.use_old:
            mask_pixmap = QPixmap(resource_path("resources/masks/background_mask.png"))
            mask_image = mask_pixmap.toImage()
            for x in range(mask_image.width()):
                for y in range(mask_image.height()):
                    color = QColor(mask_image.pixel(x, y))
                    if color == Qt.white:
                        mask_image.setPixelColor(x, y, Qt.transparent)
            mask_pixmap = QPixmap.fromImage(mask_image)
            self.setMask(mask_pixmap.mask())
        self.news = None
        self.news_url = QUrl(self.urls.get("GLOBAL_URL_1", "http://example.com"))
        self.setup_top_buttons()
        self.setup_bottom_buttons()
        self.setup_login_area()
        self.status_label = QLabel("LOG IN", self)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label_font = QFont()
        self.status_label_font.setFamily("Arial")
        self.status_label_font.setPointSize(9)
        self.status_label.setFont(self.status_label_font)
        self.status_label.setGeometry(420, 150, 300, 20)

        self.liprompt = QLabel(self)

        self.input_font = QFont()
        self.input_font.setFamily("Arial")
        self.input_font.setPointSize(9)

        self.ubox = QLineEdit(self)
        self.ubox.setFont(self.input_font)
        self.ubox.move(499, 172)
        self.ubox.setFixedSize(QSize(140, 18))

        self.pbox = QLineEdit(self)
        self.pbox.setEchoMode(QLineEdit.Password)
        self.pbox.setFont(self.input_font)
        self.pbox.move(499, 195)
        self.pbox.setFixedSize(QSize(140, 18))
        if self.use_old:
            liprompt = QPixmap(resource_path("resources/old/loginprompt.jpg"))
            self.liprompt.setGeometry(400, 166, 98, 52)
        else:
            liprompt = QPixmap(resource_path("resources/loginprompt.png"))
            self.liprompt.setGeometry(400, 165, 98, 52)
        self.liprompt.setPixmap(liprompt)
        self.ubox.setFocus()
        if self.config_manager:
            self.ubox.setText(
                self.config_manager.get_config_value("username", "placeholder")
            )
        self.ubox.returnPressed.connect(self.pbox.setFocus)
        self.pbox.returnPressed.connect(self.on_play_button_clicked)
        self.m_drag = False
        self.m_DragPosition = QPoint()
        self.center()

        self.updater = Updater(
            self.urls["BASE_URL"]
        )
        self.updater.finished.connect(self.on_update_finished)
        self.updater.update_progress_signal.connect(self.update_progress_bar)
        self.updater.update_status_signal.connect(self.update_status)
        self.updater.update_status_error_signal.connect(self.update_status_error)

    def closeEvent(self, event):
        # Stop the update thread before closing the application
        event.accept()

    @Slot(int)
    def update_progress_bar(self, value):
        self.progress_bar.setValue(value)

    @Slot(str)
    def update_status(self, text):
        self.status_label.setText(text)
        self.status_label.repaint()

    @Slot(str)
    def update_status_error(self, error_message):
        self.status_label.setText(
                f'<html><head/><body><p style="color:red;">{error_message}</p></body></html>'
            )
        self.status_label.repaint()

    def center(self):
        qr = self.frameGeometry()
        cp = QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_drag = True
            self.m_DragPosition = event.globalPos() - self.pos()
            event.accept()

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_drag:
            self.move(QMouseEvent.globalPos() - self.m_DragPosition)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_drag = False

    def setup_top_buttons(self):
        if not self.use_old:
            self.tquit_button = TQuit(self)
            self.tmin_button = TMin(self)

    def setup_bottom_buttons(self):
        self.report_bug = ReportBug(self)
        self.report_bug.url = self.urls.get("BUTTON_6", "http://example.com")
        self.homepage = Homepage(self)
        self.homepage.url = self.urls.get("BUTTON_4", "http://example.com")
        self.players_guide = PlayersGuide(self)
        self.players_guide.url = self.urls.get("BUTTON_3", "http://example.com")
        self.top_toons = TopToons(self)
        self.top_toons.url = self.urls.get("BUTTON_2", "http://example.com")
        if not self.use_old:
            self.graphic_options = GraphicOptions(self)
        self.quit_button = Quit(self)

    def setup_login_area(self):
        self.forgot_password = ForgotPassword(self)
        self.forgot_password.url = self.urls.get("BUTTON_7", "http://example.com")
        self.manage_account = ManageAccount(self)
        self.manage_account.url = self.urls.get("BUTTON_5", "http://example.com")
        self.create_account = CreateAccount(self)
        self.create_account.url = self.urls.get("BUTTON_1", "http://example.com")
        self.play_button = Play(self)
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(499, 182, 140, 20)
        self.progress_bar.setVisible(False)
        self.news = QWebEngineView(self)
        self.news.setFixedSize(315, 350)
        self.news.move(35, 75)
        self.news.load(self.news_url)
        self.news.show()

    def restore_window(self):
        system = platform.system()
        if not self.use_old:
            # set frameless window hint again if using new gui
            self.setWindowFlags(Qt.FramelessWindowHint)
        else:
            # show minimize and close buttons
            self.setWindowFlags(self.windowFlags() | Qt.WindowMinMaxButtonsHint)
        if system == "Linux":
            try:
                subprocess.run(["wmctrl", "-a", self.winTitle])
            except Exception as e:
                logging.error(f"An error occurred while trying to restore the window: {e}")
        self.showNormal()
        self.activateWindow()
        self.raise_()
        #QTBUG: ensure when restoring the window, game news is loaded again
        self.news.load(self.news_url)
        # reset window flags

    def show_progress_bar(self):
        self.ubox.hide()
        self.pbox.hide()
        self.play_button.hide()
        if not self.use_old:
            self.manage_account.hide()
        self.forgot_password.hide()
        self.create_account.hide()
        self.liprompt.hide()
        self.progress_bar.show()

    def hide_progress_bar(self):
        self.ubox.show()
        self.pbox.show()
        self.play_button.show()
        if not self.use_old:
            self.manage_account.show()
        self.forgot_password.show()
        self.create_account.show()
        self.liprompt.show()
        self.progress_bar.hide()

    def handle_authentication(self, response):
        self.auth_signal.emit(response)

    @Slot(dict)
    def update_authentication_status(self, response):
        if response["errorCode"] != 0:
            logging.error(response["message"])
            self.update_status_error(response["message"])
        else:
            playToken = response["token"]
            message = response["message"]
            self.update_status(message)
            os.environ["LOGIN_TOKEN"] = playToken
            self.launch_game()
        self.hide_progress_bar()

    def run_update(self):
        self.update_thread = threading.Thread(target=self.updater.update)
        self.update_thread.start()

    @Slot()
    def on_update_finished(self):
        logging.info("Update finished!")
        self.update_thread.join()
        self.do_authenticate()

    def launch_game(self):
        self.hide_progress_bar()
        # ensure we are in the 'game' directory
        game_dir = os.path.join(self.original_cwd, "game")
        if not os.path.isdir(game_dir):
            logging.warning(f"The directory {game_dir} does not exist.")
            return
        os.chdir(game_dir)
        # ensure the directory isn't empty
        if not os.listdir(game_dir):
            logging.warning(f"The directory {game_dir} is empty.")
            return

        # launch the game
        if sys.platform in ["win32", "win64"]:
            game = subprocess.Popen('Toontown', creationflags=134217728)
        elif sys.platform == "darwin":
            modes = os.stat('Toontown').st_mode
            if not modes & stat.S_IXUSR:
                os.chmod('Toontown', modes | stat.S_IXUSR)
            game = subprocess.Popen('Toontown')
        elif sys.platform in ["linux", "linux2"]:
            # set WINEDEBUG to -all to hide the annoying wine debug messages
            os.environ["WINEDEBUG"] = "-all"
            game = subprocess.Popen(['wine', 'Toontown.exe'])
        else:
            logging.warning("Unsupported platform")
            return
        time.sleep(1.5)
        self.showMinimized()
        self.setWindowFlags(self.windowFlags() & Qt.CustomizeWindowHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMinMaxButtonsHint)
        while game.poll() is None:
            time.sleep(1.5)
        if game.returncode == 0:
            self.restore_window()
            self.update_status("Thanks for playing Toontown!")

    def on_play_button_clicked(self):
        username = self.ubox.text()
        password = self.pbox.text()
        self.credentials = (username, password)
        if not username:
            self.update_status_error("A username is required.")
            return
        if not password:
            self.update_status_error("A password is required")
            return

        self.config_manager.update_config("username", username)
        self.show_progress_bar()
        self.run_update()

    def do_authenticate(self):
        self.hide_progress_bar()
        self.authenticator.urls = self.urls
        self.authenticator.credentials = self.credentials
        self.authenticator.start()

        self.update_status("Authenticating...")