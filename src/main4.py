import webview
import time
import asyncio
import os
import json

from auth import auth
from _config_ import _config_

__VERSION__ = 0.1


class Api():
  def __init__(self):
    self.loop = asyncio.get_event_loop()

  def close(self):
    window.destroy()

  def minimize(self):
    window.minimize()

  def tryToLogin(self, username, token):
    sсcs = self.loop.run_until_complete(
      auth().login(username, token) 
    )
    return sсcs
  
  def getLastedOptions(self):
    with open(_config_.CONFIG_FILE, 'r', encoding='utf-8') as config:
      data = json.load(config)
      return [data.get('login', None), data.get('token', None)]



class main():
  def Init(self):

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

    self.run()

  def run(self):
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
  main().Init()

