import os
import requests
import bz2
import hashlib
import logging
import platform
from panda3d.core import Multifile, VirtualFileSystem, Filename

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Updater:
    def __init__(self, base_url, save_directory=".", progress_bar=None, status_label=None):
        self.base_url = base_url
        self.version_info_file = "patcher.ver"
        self.save_directory = save_directory
        self.env_vars = ["GAME_WHITELIST_URL", "GAME_IN_GAME_NEWS_URL", "GAME_SERVER", "ACCOUNT_SERVER", "PANDA_DOWNLOAD_URL", "PATCHER_BASE_URL_HEAVY_LIFTING"]
        self.progress_bar = progress_bar
        self.status_label = status_label

    def update_progress_bar(self, value):
        if self.progress_bar:
            self.progress_bar.setValue(value)

    def update_status_label(self, text):
        if self.status_label:
            self.status_label.setText(text)
            self.status_label.repaint()

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
                    logging.error(f"Failed to set environment variable: {key} = {value}. Error: {e}")

    def verify_file_hash(self, file_path, expected_hash, expected_size):
        if not os.path.exists(file_path) or os.path.getsize(file_path) != expected_size:
            return False
        md5_hash = hashlib.md5()
        with open(file_path, "rb") as file:
            for chunk in iter(lambda: file.read(4096), b""):
                md5_hash.update(chunk)
        return md5_hash.hexdigest() == expected_hash

    def extract_multifile(self, multifile_path, extract_to_directory):
            vfs = VirtualFileSystem.getGlobalPtr()
            multifile = Multifile()
            multifile.openRead(Filename.fromOsSpecific(multifile_path))
            for i in range(multifile.getNumSubfiles()):
                subfile_name = multifile.getSubfileName(i)
                if platform.system() == "Linux" and subfile_name in ['libpandadx8.dll','libpandadx9.dll']:
                    continue
                else:
                    print(f"Extracting: {subfile_name}")
                    multifile.extractSubfile(i, Filename(subfile_name))

    def download_and_extract_files(self, content_lines):
        total_files = len([line for line in content_lines if line.startswith("REQUIRED_INSTALL_FILES")])
        current_file = 0
        for line in content_lines:
            if line.startswith("REQUIRED_INSTALL_FILES"):
                files_info = line.split('=')[1].split()
                for file_info in files_info:
                    file_name, file_type = file_info.split(':')
                    if 'OSX' in file_name and platform.system() != 'Darwin':
                        continue
                    if 'LINUX' in file_name and platform.system() != 'Linux':
                        continue
                    current_file += 1
                    version_key = f"FILE_{file_name}.current"
                    version_line = next((l for l in content_lines if l.startswith(version_key)), None)
                    if version_line:
                        version = version_line.split('=')[1]
                        file_url = os.path.join(self.base_url, f"{file_name}.{version}.bz2")
                        file_hash_info = next((l for l in content_lines if l.startswith(f"FILE_{file_name}.{version}")), None)
                        if file_hash_info:
                            _, size_and_hash = file_hash_info.split("=")
                            expected_size, expected_hash = size_and_hash.split(" ")

                            expected_size = int(expected_size)
                            decompressed_file_path = os.path.join(f"{file_name}")
                            if self.verify_file_hash(decompressed_file_path, expected_hash, expected_size):
                                logging.info(f"File {file_name} already exists and has the correct hash.")
                                continue
                        response = requests.get(file_url, stream=True)
                        total_size = int(response.headers.get('content-length', 0))
                        self.update_status_label(f"Updating files {current_file}/13")
                        if response.status_code == 200:
                            logging.info(f"Downloading file: {file_name}.{version}.bz2")
                            file_path = os.path.join(f"{file_name}.{version}.bz2")
                            with open(file_path, 'wb') as file:
                                downloaded_size = 0
                                for data in response.iter_content(chunk_size=4096):
                                    downloaded_size += len(data)
                                    file.write(data)
                                    self.update_progress_bar(int(downloaded_size * 100 / total_size))
                            with bz2.open(file_path, 'rb') as f:
                                decompressed_content = f.read()
                            decompressed_file_path = os.path.join(f"{file_name}")
                            with open(decompressed_file_path, 'wb') as f:
                                f.write(decompressed_content)
                                logging.info(f"Decompressed file: {file_name}")
                                if file_name in ["phase_1.mf", "phase_2.mf"]:
                                    self.extract_multifile(f"{file_name}", ".")
                            os.remove(file_path)
                            logging.info(f"Removed compressed file: {file_name}.{version}.bz2")
                        else:
                            logging.error(f"Failed to download {file_name}")

    def update(self):
        content_lines = self.fetch_version_info()
        self.set_environment_variables(content_lines)
        self.download_and_extract_files(content_lines)
        self.update_status_label("Files are up to date.")

    def fetch_version_info(self):
        response = requests.get(self.base_url + self.version_info_file)
        if response.status_code == 200:
            logging.info("Successfully fetched version info.")
            return response.text.splitlines()
        else:
            logging.error("Failed to connect to the update server.")
            return []