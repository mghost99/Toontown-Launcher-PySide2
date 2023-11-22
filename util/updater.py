import bz2
import hashlib
import json
import os
import platform
import threading
import time

import requests
from panda3d.core import Filename, Multifile, VirtualFileSystem
from PySide2.QtCore import QObject, Signal, Slot, QThread

import logging

class Updater(QObject):
    update_progress_signal = Signal(int)
    update_status_signal = Signal(str)
    update_status_error_signal = Signal(str)
    finished = Signal()
    should_stop = False
    def __init__(
        self, base_url, save_directory=""
    ):
        super().__init__()
        self.update_thread = None
        self.base_url = base_url
        self.version_info_file = "patcher.ver"
        self.save_directory = save_directory
        if save_directory == "":
            self.save_directory = os.path.join(os.getcwd(), "game")
        if not self.save_directory.endswith(os.sep):
            self.save_directory += os.sep
        if not os.path.isdir(self.save_directory):
            os.mkdir(self.save_directory)
        self.env_vars = [
            "GAME_WHITELIST_URL",
            "GAME_IN_GAME_NEWS_URL",
            "GAME_SERVER",
            "ACCOUNT_SERVER",
            "PANDA_DOWNLOAD_URL",
            "PATCHER_BASE_URL_HEAVY_LIFTING",
        ]
        self.file_dict = {}
        self.files_already_updated = False

    def set_environment_variables(self, content_lines):
        for line in content_lines:
            key, sep, value = line.partition("=")
            if key in self.env_vars:
                try:
                    if key == "PATCHER_BASE_URL_HEAVY_LIFTING":
                        key = "DOWNLOAD_SERVER"
                    os.environ[key] = value
                    logging.info(f"Set environment variable: {key} = {value}")
                except OSError as e:
                    logging.error(
                        f"Failed to set environment variable: {key} = {value}. Error: {e}"
                    )


    def extract_multifile(self, multifile_path, extract_to):
        vfs = VirtualFileSystem.getGlobalPtr()
        multifile = Multifile()
        multifile.openRead(Filename.fromOsSpecific(os.path.join(self.save_directory, multifile_path)))
        for i in range(multifile.getNumSubfiles()):
            subfile_name = multifile.getSubfileName(i)
            if platform.system() == "Linux" and subfile_name in ["libpandadx8.dll", "libpandadx9.dll"]:
                continue
            else:
                target_path = os.path.join(extract_to, subfile_name)
                logging.info(f"Extracting: {subfile_name} to {target_path}")
                multifile.extractSubfile(i, Filename.fromOsSpecific(target_path))
    
    def store_file_data(self, content_lines):
        for line in content_lines:
            if line.startswith("REQUIRED_INSTALL_FILES"):
                files_info = line.split("=")[1].split()
                for file_info in files_info:
                    if "OSX" in file_info and platform.system() != "Darwin":
                        continue
                    if "LINUX" in file_info and platform.system() != "Linux":
                        continue
                    decomp_file_name, file_type = file_info.split(":")
                    if file_type == "3":
                        extract_mf = True
                    if file_type == "2":
                        extract_mf = False

                    version_key = f"FILE_{decomp_file_name}.current"
                    version_line = next((l for l in content_lines if l.startswith(version_key)), None)
                    if version_line:
                        version = version_line.split("=")[1]
                        file_url = os.path.join(
                            self.base_url, f"{decomp_file_name}.{version}.bz2")
                        file_hash_info = next(
                            (l for l in content_lines if l.startswith(f"FILE_{decomp_file_name}.{version}")), None)
                        if file_hash_info:
                            _, size_hash = file_hash_info.split("=")
                            expected_size, expected_hash = size_hash.split(" ")
                            expected_size = int(expected_size)
                        
                    self.file_dict[decomp_file_name] = {
                        "version": version,
                        "url": file_url,
                        "size": expected_size,
                        "hash": expected_hash,
                        "extract_mf": extract_mf
                    }

    def is_up_to_date(self, file):
        # check if file exists
        file_path = os.path.join(self.save_directory, file)
        if not os.path.exists(file_path):
            logging.info(f"File {file} does not exist.")
            return False
        # check if file is the correct size
        if os.path.getsize(file_path) != self.file_dict[file]['size']:
            logging.info(f"File {file} does not have the correct size.")
            return False
        # check if file hash matches
        md5_hash = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                md5_hash.update(chunk)
        if md5_hash.hexdigest() != self.file_dict[file]['hash']:
            logging.info(f"File {file} does not have the correct hash.")
            return False
        return True


    def download_and_extract_file(self, file_name):
        logging.info(f"Downloading: {file_name}")
        version = self.file_dict[file_name]['version']
        url = self.file_dict[file_name]['url']
        extract_mf = self.file_dict[file_name]['extract_mf']
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get("content-length", 0))
        bz2_path = os.path.join(self.save_directory, f"{file_name}.{version}.bz2")
        if response.status_code == 200:
            with open(bz2_path, "wb") as file:
                for data in response.iter_content(chunk_size=4096):
                    self.update_progress_signal.emit(file.tell() / total_size * 100)
                    file.write(data)
            logging.info(f"GET - {url} {response.status_code}")      
            with bz2.open(bz2_path, "rb") as f:
                decompressed_content = f.read()
            decompressed_file_path = os.path.join(self.save_directory, f"{file_name}")
            with open(decompressed_file_path, "wb") as f:
                f.write(decompressed_content)
            if extract_mf:
                self.extract_multifile(f"{file_name}", self.save_directory)
            # remove bz2 file
            os.remove(bz2_path)
            logging.info(f"Removed compressed file: {file_name}.{version}.bz2")
        else:
            logging.error(f"GET(FAIL) - {url} {response.status_code}")
            return

    def do_update(self):
        logging.info("Starting updater...")
        current_file = 0
        total_files = len(self.file_dict.keys())
        logging.info(f"Total files to update: {total_files}")
        try:
            if not self.files_already_updated:
                for file_info in self.file_dict.keys():
                    current_file += 1
                    time.sleep(1)
                    self.update_progress_signal.emit(0)
                    if self.is_up_to_date(file_info):
                        self.update_status_signal.emit(f"{file_info} is already up to date.")
                        self.update_progress_signal.emit(100)
                        logging.info(f"{file_info} is already up to date.")
                    else:
                        self.update_status_signal.emit(f"Updating files {current_file}/{total_files}")
                        self.download_and_extract_file(file_info)
                        time.sleep(1)
        except Exception as e:
            logging.error(f"An error occurred during the update process: {e}")
            self.update_status_error_signal.emit(f"An error occurred during the update process.")
            # we want to set to files to up to date if no errors occurred
        else:
            self.update_status_signal.emit("Files are up to date.")
            self.files_already_updated = True
            time.sleep(3)

    @Slot()
    def update(self):
        try:
            if not self.should_stop:
                self.fetch_version_info()
                self.do_update()
                self.cleanup()
            self.update_status_signal.emit("Have fun playing Toontown!")
        except Exception as e:
            self.update_status_error_signal.emit(f"An error occurred during the update process.")
            logging.error(f"An error occurred during the update process: {e}")
        finally:
            self.finished.emit()

    @Slot()
    def stop(self):
        self.should_stop = True

    def fetch_version_info(self):
        response = requests.get(self.base_url + self.version_info_file)
        if response.status_code == 200:
            logging.info("Successfully fetched version info.")
            content_lines = response.text.splitlines()
            self.set_environment_variables(content_lines)
            self.store_file_data(content_lines)
        else:
            logging.error("Failed to connect to the update server.")

    def cleanup(self):
        hash_data = os.path.join(self.save_directory, "hash_data")
        if os.path.exists(hash_data):
            if os.path.isfile(hash_data):
                os.remove(hash_data)
                os.mkdir(hash_data)
                logging.info("Removed hash_data file and created an empty directory.")
        else:
            os.mkdir(hash_data)
            logging.info("hash_data file or folder not found; creating empty directory.")