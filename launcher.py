import os
import platform
import sys

from PySide6.QtWidgets import QApplication

from gui import MainWindow, SplashScreen


# os.environ['QT_DEBUG_PLUGINS'] = '1'
os.environ["QT_SCALE_FACTOR"] = "1"
os.environ["QT_FONT_DPI"] = "96"
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "0"
# os.environ["QT_LOGGING_RULES"] = "*.debug=true"

# get the 'IS_OLD' environment variable
# if it is set to '1', then use the old launcher
# otherwise, use the new launcher
USE_GUI = os.environ.get('USE_GUI')
if USE_GUI is None:
    print("USE_GUI environment variable not set. Using '0'.")
    USE_GUI = '0'
if USE_GUI == '1':
    print("Using old launcher gui...")
    use_old = True
elif USE_GUI == '0':
    print("Using new launcher gui...")
    use_old = False
elif USE_GUI is not None and USE_GUI not in ['0', '1']:
    help = f"""
    USE_GUI environment variable is set to an invalid value.
    Valid options:
    0 - Use new launcher gui
    1 - Use old launcher gui

    You chose: {USE_GUI} which is not a valid option.

    Defaulting to new launcher gui...
    """
    print(help)
    use_old = False

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
    main_window = MainWindow(
        launcher_urls=urls,
        use_old=use_old)
    main_window.show()
    app.processEvents()


if __name__ == "__main__":
    main()
