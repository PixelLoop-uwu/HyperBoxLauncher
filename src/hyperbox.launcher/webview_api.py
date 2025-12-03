import asyncio
import webview

import services
from utils import open_game_folder
from auth import auth
from client import Client
from launcher.launcher import Launcher
from _config_ import _config_


class Api:
  def __init__(self):
    self.auth = auth
    self.client = Client()


  # * Window actions
  def close(self):
    webview.windows[0].destroy()

  def minimize(self):
    webview.windows[0].minimize()


  # * Login screen
  def tryToLogin(self, username: str, token: str) -> dict:
    return asyncio.run( self.auth.try_to_login(username, token) )

  def getLastOptions(self) -> list:
    return services.get_last_login_options()
  
  def connectionCheck(self) -> bool:
    return True
    import requests; return requests.get(_config_.API, timeout=2).ok


  # * Main screen
  async def _async_get_modpacks_data(self):
    async with self.client as api:
      return await api.get_modpacks_data()

  def getMainData(self) -> dict:
    return {
      "username": self.auth.get_username(),
      "modpacks": asyncio.run( 
        self._async_get_modpacks_data()
      )
    }
  
  def getLauncherSettings(self) -> dict:
    return services.get_launcher_settings()
  
  def saveLauncherSettings(self, settings: dict) -> None:
    services.save_launcher_settings(settings)
  
  def openGameFolder(self, modpack: str) -> None:
    open_game_folder(modpack)
  
  def chooseGameFolder(self) -> str:
    folder = webview.windows[0].create_file_dialog(
      webview.FileDialog.FOLDER
    ); return folder[0] if folder else ""

  def launchPlay(self, modpack: str) -> None:
    asyncio.run(
      Launcher(modpack, webview.windows[0]).run()
    )

  def uploadSkin(self, base64Data) -> dict:
    print(asyncio.run(
      services.upload_skin(base64Data)
    ))