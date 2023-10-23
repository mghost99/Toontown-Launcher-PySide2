import os
import platform
import subprocess
from PyQt5.QtCore import QObject, QThread, pyqtSignal

class GameLauncher(QObject):
    game_exit_signal = pyqtSignal(int, str)
    game_closed_signal = pyqtSignal()

    def __init__(self, urls, main_window):
        super().__init__()
        self.urls = urls
        self.main_window = main_window
        self.launcher_thread = None
        self.launcher_worker = None

    def launch_game(self):
        self.launcher_thread = QThread()
        self.launcher_worker = LauncherWorker(self.urls)
        self.launcher_worker.moveToThread(self.launcher_thread)
        self.launcher_worker.launch_signal.connect(self.launch)
        self.launcher_thread.started.connect(self.iconify_launcher)
        self.launcher_thread.started.connect(self.launcher_worker.run)
        self.launcher_worker.finished.connect(self.launcher_thread.quit)
        self.launcher_worker.finished.connect(self.launcher_worker.deleteLater)
        self.launcher_thread.finished.connect(self.launcher_thread.deleteLater)
        self.launcher_thread.start()

    def iconify_launcher(self):
        self.main_window.showMinimized()

    def launch(self, cmd):
        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.monitor_game_exit(process)
        except Exception as e:
            error_message = f"An error has occurred launching Toontown: {e}"
            self.game_exit_signal.emit(-1, error_message)

    def monitor_game_exit(self, process):
        while True:
            retcode = process.poll()
            if retcode is not None:
                stdout, stderr = process.communicate()
                if retcode != 0:
                    error_message = stderr.decode('utf-8')
                    self.game_exit_signal.emit(retcode, error_message)
                else:
                    self.game_exit_signal.emit(retcode, "Thanks for playing Toontown!")
                self.game_closed_signal.emit()
                break


class LauncherWorker(QObject):
    launch_signal = pyqtSignal(list)
    finished = pyqtSignal()

    def __init__(self, urls):
        super().__init__()
        self.urls = urls

    def run(self):
        system = platform.system()
        cwd = os.getcwd()

        tt_exe = os.path.join(cwd, 'Toontown.exe')
        os.environ['DOWNLOAD_SERVER'] = self.urls['PATCHER_BASE_URL_HEAVY_LIFTING']
        os.environ['PANDA_DOWNLOAD_URL'] = self.urls['PANDA_DOWNLOAD_URL']
        os.environ['GAME_WHITELIST_URL'] = self.urls['GAME_WHITELIST_URL']
        os.environ['ACCOUNT_SERVER'] = self.urls['ACCOUNT_SERVER']

        cmd = None
        if system == "Linux":
            cmd = ["wine", tt_exe]
        elif system == "Windows":
            cmd = tt_exe
        elif system == "Darwin":
            pass  # TODO

        if cmd:
            self.launch_signal.emit(cmd)
        self.finished.emit()
