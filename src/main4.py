import webview
import asyncio
import os
import json

from _config_ import _config_
from auth import Auth
from client import WebSocketClient
from utils import Utils

__VERSION__ = 0.1


class Api():
  def __init__(self):
    self.loop = asyncio.get_event_loop()
    self.auth = Auth()
    self.webs = WebSocketClient()
    self.uts = Utils()


  def close(self):
    window.destroy()

  def minimize(self):
    window.minimize()

  def openGameFolder(self, folder):
    self.uts.open_game_folder(f'{_config_.UPDATES_DIR}/{folder}')


  def tryToLogin(self, username, token):
    return self.loop.run_until_complete(
      self.auth.login(username, token) 
    )
  
  def getMainData(self):
    username = self.auth.get_username()
    modpacks = self.loop.run_until_complete( self.webs.get_modpacks() )

    data = { 
      "username": username,
      "modpacks": modpacks
    }

    return data
  
  def getLastedOptions(self):
    with open(_config_.CONFIG_FILE, 'r', encoding='utf-8') as config:
      data = json.load(config)
      return [data.get('login', None), data.get('token', None)]


class Main():
  def check_config_file(self) -> None:
    def create_config_file():
      with open(_config_.CONFIG_FILE, "w", encoding="utf-8") as config:
        json.dump({}, config, indent=None, ensure_ascii=False)
        print('[Hyperbox] Configuration file created')

    os.makedirs(_config_.UPDATES_DIR, exist_ok=True)

    if os.path.exists(_config_.CONFIG_FILE):
      try: 
        with open(_config_.CONFIG_FILE, "r", encoding="utf-8") as config:
          json.load(config)

      except (json.JSONDecodeError, ValueError):
        print('[Hyperbox] Configuration file is corrupted / missing')
        create_config_file()

    else: 
      create_config_file()
    
    print('[Hyperbox] Configuration file checked')

  def run(self) -> None:
    self.check_config_file()

    global window

    window = webview.create_window(
      title = "HyperBox Launcher",
      url = "./gui/index.html",

      frameless = True,
      easy_drag = True,
      width = 910,
      height = 520,
      background_color = "#1a1a1a",
      js_api = Api()
    )

    webview.start(debug=True)


if __name__ == '__main__':
  Main().run()

