import os
import platform
import subprocess
import time

from PySide6.QtCore import QObject, Signal


class GameLauncher(QObject):
    game_exit_signal = Signal(int, str)
    game_closed_signal = Signal()

    def __init__(self, urls, main_window):
        super().__init__()
        self.urls = urls
        self.main_window = main_window

    def launch_game(self):
        """
        This method will launch the game - in our case Toontown.exe
        """
        cmd = self.prepare_command()
        if cmd and cmd != None:
            self.main_window.showMinimized()
            game_process = subprocess.Popen(cmd)
            self.monitor_game_exit(game_process)

    def prepare_command(self):
        system = platform.system()
        cwd = os.getcwd()
        tt_ = os.path.join(cwd, "Toontown")
        if system == "Linux":
            return ["wine", tt_ + ".exe"]
        elif system == "Windows":
            return [tt_ + ".exe"]
        elif system == "Darwin":
            return [tt_]  # Should run an executable called "Toontown" on macOS

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
