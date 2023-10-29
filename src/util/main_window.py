import platform
import subprocess
from PyQt5.QtWidgets import QMainWindow, QLabel, QProgressBar, QDesktopWidget
from PyQt5.QtCore import Qt, QTimer, pyqtSlot, QPoint
from PyQt5.QtGui import QPixmap, QColor, QFont
from src.util.updater import Updater

from src.widgets import (
    TQuit,
    TMin,
    ReportBug,
    Homepage,
    PlayersGuide,
    TopToons,
    GraphicOptions,
    Quit,
    LiPrompt,
    UserInput,
    PassInput,
    ForgotPassword,
    ManageAccount,
    CreateAccount,
    Play,
    GameNews,
)

import os


class MainWindow(QMainWindow):
    def __init__(self, launcher_urls, game_launcher, authenticator):
        super().__init__()
        self.urls = launcher_urls if launcher_urls else {}
        self.game_launcher = game_launcher
        self.authenticator = authenticator
        self.winTitle = "Toontown Launcher"
        self.setWindowTitle(self.winTitle)
        self.setGeometry(100, 100, 750, 500)
        self.setFixedSize(750, 500)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.background = QLabel(self)
        pixmap = QPixmap("assets/backgrounds/BACKGROUND1.png")
        self.background.setPixmap(pixmap)
        self.background.resize(750, 500)
        mask_pixmap = QPixmap("assets/masks/BACKGROUNDMASK.png")
        mask_image = mask_pixmap.toImage()
        for x in range(mask_image.width()):
            for y in range(mask_image.height()):
                color = QColor(mask_image.pixel(x, y))
                if color == Qt.white:
                    mask_image.setPixelColor(x, y, Qt.transparent)
        mask_pixmap = QPixmap.fromImage(mask_image)
        self.setMask(mask_pixmap.mask())
        self.setup_top_buttons()
        self.setup_bottom_buttons()
        self.setup_login_area()
        self.m_drag = False
        self.m_DragPosition = QPoint()
        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
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
        self.tquit_button = TQuit(self)
        self.tquit_button.clicked.connect(self.close)
        self.tmin_button = TMin(self)
        self.tmin_button.clicked.connect(self.showMinimized)

    def setup_bottom_buttons(self):
        self.report_bug = ReportBug(
            self, url=self.urls.get("BUTTON_6", "http://example.com")
        )
        self.homepage = Homepage(
            self, url=self.urls.get("BUTTON_4", "http://example.com")
        )
        self.players_guide = PlayersGuide(
            self, url=self.urls.get("BUTTON_3", "http://example.com")
        )
        self.top_toons = TopToons(
            self, url=self.urls.get("BUTTON_2", "http://example.com")
        )
        self.graphic_options = GraphicOptions(self)
        self.quit_button = Quit(self)

    def setup_login_area(self):
        self.info_label = QLabel("LOG IN", self)
        self.info_label.setGeometry(420, 150, 300, 20)
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label_font = QFont()
        self.info_label_font.setFamily("Arial")
        self.info_label_font.setPointSize(9)
        self.info_label.setFont(self.info_label_font)
        self.liprompt = LiPrompt(self)
        self.input_font = QFont()
        self.input_font.setFamily("Arial")
        self.input_font.setPointSize(9)
        self.username_input = UserInput(self)
        self.username_input.setFont(self.input_font)
        self.password_input = PassInput(self)
        self.password_input.setFont(self.input_font)
        self.forgot_password = ForgotPassword(
            self, url=self.urls.get("BUTTON_7", "http://example.com")
        )
        self.manage_account = ManageAccount(
            self, url=self.urls.get("BUTTON_5", "http://example.com")
        )
        self.create_account = CreateAccount(
            self, url=self.urls.get("BUTTON_1", "http://example.com")
        )
        self.play_button = Play(self.on_play_button_clicked, self)
        self.game_news = GameNews(
            self, url=self.urls.get("GLOBAL_URL_1", "http://example.com")
        )
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(499, 182, 140, 20)
        self.progress_bar.setVisible(False)

    def restore_window(self):
        system = platform.system()
        if system == "Linux":
            try:
                subprocess.run(["wmctrl", "-a", self.winTitle])
            except Exception as e:
                print(f"An error occurred while trying to restore the window: {e}")
        self.showNormal()
        self.activateWindow()
        self.raise_()

    def info_text(self, message, is_error=False):
        if is_error:
            self.info_label.setText(
                f'<html><head/><body><p style="color:red;">{message}</p></body></html>'
            )
        else:
            self.info_label.setText(message)

    def show_progress_bar(self):
        self.username_input.hide()
        self.password_input.hide()
        self.play_button.hide()
        self.manage_account.hide()
        self.forgot_password.hide()
        self.create_account.hide()
        self.liprompt.hide()
        self.progress_bar.show()

    def hide_progress_bar(self):
        self.username_input.show()
        self.password_input.show()
        self.play_button.show()
        self.manage_account.show()
        self.forgot_password.show()
        self.create_account.show()
        self.liprompt.show()
        self.progress_bar.hide()

    @pyqtSlot(dict)
    def handle_authentication(self, response):
        if response["errorCode"] != 0:
            self.info_label.setText(response["message"])
            self.play_button.setEnabled(True)
        else:
            playToken = response["token"]
            os.environ["LOGIN_TOKEN"] = playToken
            self.run_updater()
            self.launch_game()
        self.hide_progress_bar()

    def run_updater(self):
        self.updater = Updater(
            self.urls["BASE_URL"],
            progress_bar=self.progress_bar,
            status_label=self.info_label,
        )
        self.updater.update()
        self.game_launcher.game_closed_signal.connect(self.restore_window)

    def launch_game(self):
        self.hide_progress_bar()
        self.info_text("LOG IN")
        self.game_launcher.launch_game()
        self.play_button.setEnabled(True)

    def on_play_button_clicked(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if not username:
            self.info_text("A username is required.", is_error=True)
            return
        if not password:
            self.info_text("A password is required", is_error=True)
            return

        self.play_button.setEnabled(False)
        self.show_progress_bar()
        self.authenticator.urls = self.urls  # Update urls
        self.authenticator.username = username  # Update username
        self.authenticator.password = password  # Update password

        self.authenticator.authentication_signal.connect(self.handle_authentication)
        self.authenticator.start()  # This will trigger the run method in Authenticator

        self.info_text("Authenticating...")
