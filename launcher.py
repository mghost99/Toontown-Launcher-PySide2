
import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from src.util import SplashScreen, Authenticator, GameLauncher, MainWindow


def main():
    os.environ["QT_SCALE_FACTOR"] = str(1)
    QApplication.setAttribute(Qt.AA_DisableHighDpiScaling)

    app = QApplication(sys.argv)

    splash = SplashScreen()
    splash.show()

    urls = splash.load_remote_urls()
    authenticator = Authenticator(urls, "", "")
    main_window = MainWindow(
        launcher_urls=urls, game_launcher=None, authenticator=authenticator)
    game_launcher = GameLauncher(urls=urls, main_window=main_window)
    main_window.game_launcher = game_launcher
    splash.finish(main_window)
    main_window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
