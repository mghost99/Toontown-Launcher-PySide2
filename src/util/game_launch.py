import os
import platform
import subprocess
import time
from PyQt5.QtCore import QObject, pyqtSignal


class GameLauncher(QObject):
    game_exit_signal = pyqtSignal(int, str)
    game_closed_signal = pyqtSignal()

    def __init__(self, urls, main_window):
        super().__init__()
        self.urls = urls
        self.main_window = main_window

    def launch_game(self):
        cmd = self.prepare_command()
        if cmd:
            self.main_window.showMinimized()
            game_process = subprocess.Popen(cmd)
            self.monitor_game_exit(game_process)

    def prepare_command(self):
        system = platform.system()
        cwd = os.getcwd()
        tt_exe = os.path.join(cwd, "Toontown.exe")
        if system == "Linux":
            return ["wine", tt_exe]
        elif system == "Windows":
            return [tt_exe]
        elif system == "Darwin":
            return None  # TODO: Add command for macOS

    def monitor_game_exit(self, process):
        while process.poll() is None:
            time.sleep(1)
        retcode = process.returncode
        if retcode != 0:
            error_message = "Game exited with an error."
            self.game_exit_signal.emit(retcode, error_message)
        else:
            self.game_exit_signal.emit(retcode, "Thanks for playing Toontown!")
        self.game_closed_signal.emit()
