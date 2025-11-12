import webview
import asyncio
import os
import json

import services
from authentication import Auth
from client import Client


__VERSION__ = 1


class Api:

  def __init__(self):
    self.auth = Auth()
    self.client = Client()


  # Window actions
  def close(self):
    webview.windows[0].destroy()

  def minimize(self):
    webview.windows[0].minimize()


  # Login screen
  def tryToLogin(self, username: str, token: str) -> dict:
    return asyncio.run(self.auth.try_to_login(username, token))

  def getLastOptions(self) -> list:
    return services.get_last_login_options()


  # Main screen
  async def _async_get_modpacks_data(self):
    async with self.client as api:
      return await api.get_modpacks_data()

  def getMainData(self) -> dict:
    return {
      "username": self.auth.get_username(),
      "modpacks": asyncio.run(self._async_get_modpacks_data())
    }
  
  def getLauncherSettings(self) -> dict:
    return services.get_launcher_settings()
  
  def saveLauncherSettings(self, settings: dict) -> None:
    services.save_launcher_settings(settings)
  
  def openGameFolder(self, modpack) -> None:
    services.open_game_folder(modpack)
  
  def chooseGameFolder(self) -> str:
    folder = webview.windows[0].create_file_dialog(
      webview.FileDialog.FOLDER
    ); return folder[0]

  def play(self, modpack) -> bool:
    ...


def run() -> None:
  services.check_config_file()
    
  global window

  window = webview.create_window(
    title = "HyperBox Launcher",
    url = "./gui/index.html",

    frameless = True,
    easy_drag = False,
    width = 910,
    height = 520,
    background_color = "#1a1a1a",
    js_api = Api()
  )

  webview.start(debug=True)


if __name__ == '__main__':
  run()

