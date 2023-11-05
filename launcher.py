import os
import platform
import sys

from PySide6.QtWidgets import QApplication

from src.util import Authenticator, GameLauncher, MainWindow, SplashScreen


# os.environ['QT_DEBUG_PLUGINS'] = '1'
os.environ["QT_SCALE_FACTOR"] = "1"
os.environ["QT_FONT_DPI"] = "96"
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "0"
# os.environ["QT_LOGGING_RULES"] = "*.debug=true"
if platform.system == "Windows":
    import ctypes

    awareness = ctypes.c_int()
    ctypes.windll.shcore.GetProcessDpiAwareness(0, ctypes.byref(awareness))
    ctypes.windll.shcore.SetProcessDpiAwareness(0)
    ctypes.windll.user32.SetProcessDPIAware()



def main():
    app = QApplication(sys.argv)
    splash = SplashScreen()
    splash.show()
    splash.url_loader_thread.finished.connect(lambda urls: setup_main_window(app, urls))
    splash.url_loader_thread.error_occurred.connect(lambda: sys.exit(-1))
    sys.exit(app.exec())


def setup_main_window(app, urls):
    authenticator = Authenticator(urls, "", "")
    main_window = MainWindow(
        launcher_urls=urls, game_launcher=None, authenticator=authenticator
    )
    game_launcher = GameLauncher(urls=urls, main_window=main_window)
    main_window.game_launcher = game_launcher
    main_window.show()
    app.processEvents()


if __name__ == "__main__":
    main()
