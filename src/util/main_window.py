from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QProgressBar,
    QDesktopWidget, QPushButton, QLineEdit
)
from PyQt5.QtCore import Qt, QTimer, pyqtSlot, QPoint, QUrl
from PyQt5.QtGui import QPixmap, QColor, QFont, QDesktopServices, QIcon
from src.util.updater import Updater
from src.widgets.ThemedButton import ThemedButton
from src.widgets.ThemedLabel import ThemedLabel
from src.widgets.ThemedLineEdit import ThemedLineEdit
from src.widgets.ThemedWebView import ThemedWebView
import json
import os

class MainWindow(QMainWindow):
    def __init__(self, launcher_urls, game_launcher, authenticator):
        super().__init__()
        self.theme_data = {}
        self.is_old = False
        self.urls = launcher_urls if launcher_urls else {}
        self.game_launcher = game_launcher
        self.authenticator = authenticator
        self.setWindowTitle('Toontown Launcher')
        self.setGeometry(100, 100, 750, 500)
        self.setFixedSize(750, 500)
        self.load_theme(self)
        self.setup_widgets()
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

    def setup_background(self):
        self.background = QLabel(self)
        if self.is_old:
            pixmap = QPixmap("assets/old/backgrounds/BACKGROUND1.jpg")
        else:
            self.setWindowFlags(Qt.FramelessWindowHint)
            pixmap = QPixmap("assets/default/backgrounds/BACKGROUND1.png")
            mask_pixmap = QPixmap("assets/default/masks/BACKGROUNDMASK.png")
            mask_image = mask_pixmap.toImage()
            for x in range(mask_image.width()):
                for y in range(mask_image.height()):
                    color = QColor(mask_image.pixel(x, y))
                    if color == Qt.white:
                        mask_image.setPixelColor(x, y, Qt.transparent)
            mask_pixmap = QPixmap.fromImage(mask_image)
            self.setMask(mask_pixmap.mask())
        self.background.setPixmap(pixmap)
        self.background.resize(750, 500)

    @staticmethod
    def load_theme(self, theme_file="old-theme.json"):
        if theme_file == "old-theme.json":
            self.is_old = True
        with open(os.path.join("themes", theme_file), "r") as file:
            self.theme_data = json.load(file)
        self.setup_background()

    def setup_widgets(self):
        self.button_url_keys = {
            "ReportBug": "BUTTON_6",
            "Homepage": "BUTTON_4",
            "PlayersGuide": "BUTTON_3",
            "TopToons": "BUTTON_2",
            "ManageAccount": "BUTTON_5",
            "CreateAccount": "BUTTON_1",
            "ForgotPassword": "BUTTON_7",
            "GameNews": "GLOBAL_URL_1"
        }

        elements = self.theme_data.get('elements', [])
        for element in elements:
            element_data = elements[element]
            if element_data.get('type') == 'QPushButton':
                button = ThemedButton(element_data, parent=self)
                button.setObjectName(element)

                # Set URLs and connect clicked signal
                url_key = self.button_url_keys.get(element)
                if url_key and url_key in self.urls:
                    button.url = self.urls[url_key]
                    button.clicked.connect(self.open_url(button.url))
                else:
                    if element in ["TQuit", "Quit"]:
                        button.clicked.connect(self.close_app)
                    elif element == 'TMin':
                        button.clicked.connect(self.min_app)
                    elif element == 'Play':
                        button.clicked.connect(self.on_play_button_clicked)
                        button.set_disabled(False)
            elif element_data.get('type') == 'QLineEdit':
                lineedit = ThemedLineEdit(element_data, parent=self)
                lineedit.setObjectName(element)
                setattr(self, element, lineedit)
            elif element_data.get('type') == 'QLabel':
                label = ThemedLabel(element_data, parent=self)
                label.setObjectName(element)
            elif element_data.get('type') == "QWebEngineView":
                webview = ThemedWebView(element_data, parent=self)
                webview.setObjectName(element)

                # Set URLs
                url_key = self.button_url_keys.get(element)
                if url_key and url_key in self.urls:
                    webview.url = self.urls[url_key]
                    webview.load(QUrl(webview.url))
        # Disable GraphicOptions
        if self.get_button("GraphicOptions"):
            self.get_button("GraphicOptions").set_disabled(True)
            self.get_button("GraphicOptions").setIcon(QIcon("assets/default/buttons/GRAPHICSOPTIONS1G.png"))


    def open_url(self, url):
        def _open():
            QDesktopServices.openUrl(QUrl(url))
        return _open

    def close_app(self):
        exit()
    
    def min_app(self):
        self.window().showMinimized()

    def setup_login_area(self):
        self.info_label = QLabel('LOG IN', self)
        self.info_label.setGeometry(420, 150, 300, 20)
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label_font = QFont()
        self.info_label_font.setFamily("Arial")
        self.info_label_font.setPointSize(9)
        self.info_label.setFont(self.info_label_font)
        self.input_font = QFont()
        self.input_font.setFamily("Arial")
        self.input_font.setPointSize(9)
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(499, 182, 140, 20)
        self.progress_bar.setVisible(False)

    def restore_window(self):
        print("linux bug: we know we are minimized but we can do nothing to restore!!??")
        if self.windowState() == Qt.WindowMinimized:
            self.showMinimized()
            self.show()
        

    def info_text(self, message, is_error=False):
        if is_error:
            self.info_label.setText(f'<html><head/><body><p style="color:red;">{message}</p></body></html>')
        else:
            self.info_label.setText(message)

    def get_button(self, button_name):
        button = self.findChild(QPushButton, button_name)
        if button:
            return button

    def show_button(self, button_name):
        button = self.findChild(QPushButton, button_name)
        if button:
            button.show()

    def hide_button(self, button_name):
        button = self.findChild(QPushButton, button_name)
        if button:
            button.hide()

    def show_progress_bar(self):
        self.UserInput.hide()
        self.PassInput.hide()
        self.hide_button("Play")
        self.hide_button("ManageAccount")
        self.hide_button("ForgotPassword")
        self.hide_button("CreateAccount")
        self.hide_button("LoginPrompt")
        self.progress_bar.show()

    def hide_progress_bar(self):
        self.UserInput.show()
        self.PassInput.show()
        self.show_button("Play")
        self.show_button("ManageAccount")
        self.show_button("ForgotPassword")
        self.show_button("CreateAccount")
        self.show_button("LoginPrompt")
        self.progress_bar.hide()

    @pyqtSlot(dict)
    def handle_authentication(self, response):
        if response['errorCode'] != 0:
            self.info_label.setText(response['message'])
        else:
            playToken = response['token']
            os.environ['LOGIN_TOKEN'] = playToken
            self.run_updater()
            self.launch_game()
        self.hide_progress_bar()

    def run_updater(self):
        self.updater = Updater(self.urls['BASE_URL'], progress_bar=self.progress_bar, status_label=self.info_label)
        self.updater.update()
        self.game_launcher.game_closed_signal.connect(self.restore_window)

    def launch_game(self):
        self.hide_progress_bar()
#        self.info_text("LOG IN")
        self.game_launcher.launch_game()

    def on_play_button_clicked(self):
        username = self.UserInput.text()
        password = self.PassInput.text()
        if not username:
            self.info_text("A username is required.", is_error=True)
            return
        if not password:
            self.info_text("A password is required", is_error=True)
            return

        self.show_progress_bar()
        self.authenticator.urls = self.urls  # Update urls
        self.authenticator.username = username  # Update username
        self.authenticator.password = password  # Update password
        
        self.authenticator.authentication_signal.connect(self.handle_authentication)
        self.authenticator.start()  # This will trigger the run method in Authenticator

        self.info_text("Authenticating...")