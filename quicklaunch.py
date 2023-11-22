import json
import os
import platform
from urllib.parse import urlencode
import http.client as hc

username = input("Username: ")
import getpass
password = getpass.getpass("Password: ")

os.environ["GAME_WHITELIST_URL"] = "http://download.sunrise.games/launcher/"
os.environ["GAME_IN_GAME_NEWS_URL"] = "http://download.sunrise.games/toontown/en/gamenews/"
os.environ["GAME_SERVER"] = "unite.sunrise.games:6667"
os.environ["ACCOUNT_SERVER"] = "http://unite.sunrise.games:4500"
os.environ["PANDA_DOWNLOAD_URL"] = "http://download.sunrise.games/launcher/"
os.environ["DOWNLOAD_SERVER"] = "http://download.sunrise.games/launcher/"

connection = hc.HTTPSConnection("sunrise.games", 443)
headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "User-Agent": "PySide2 - Disney's Toontown Online Launcher"}
params = urlencode({
            "username": username.encode("utf-8"),
            "password": password.encode("utf-8"),
            "serverType": "Final Toontown",
        })
connection.request("POST", "/api/login/alt/", params, headers)
try:
    response = json.loads(connection.getresponse().read())
    success = response.get("success", 'False')
    if success:
        if response["errorCode"] != 0:
            message = response["message"]
            print(f"message: {message}")
            connection.close()
        else:
            playToken = response["token"]
            message = response["message"]
            print(f"message: {message}")
            os.environ["LOGIN_TOKEN"] = playToken
            connection.close()
            if platform.system() == "Windows":
                # cd the ToontownOnline directory
                os.chdir("ToontownOnline")
                try:
                    os.system("Toontown.exe")
                except:
                    print(f"Toontown.exe not found in {os.getcwd()}")
            elif platform.system() == "Linux":
                os.environ['WINEDEBUG'] = '-all' # Disable wine debug messages
                os.system("wine Toontown.exe")
            else:
                print("Unsupported OS")
except hc.BadStatusLine:
    print("API - Bad Status. Try again.")