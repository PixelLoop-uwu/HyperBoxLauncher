import subprocess
import aiohttp
import asyncio
from tenacity import RetryError
from pathlib import Path
from loguru import logger

from .loader import Loader
from .command import Command
from client import Client
from services import get_launcher_settings
from _config_ import _config_

class Launcher:
  def __init__(self, modpack, window):
    self.modpack = modpack
    self.window = window

    self.client = Client()
    self.settings = get_launcher_settings()

    MAIN_DIR = Path(self.settings["mainDir"])
    UPDATES_DIR = MAIN_DIR / "updates"

    self.loader = Loader(
      MAIN_DIR, UPDATES_DIR / modpack, window
    )
    self.command = Command(
      MAIN_DIR, UPDATES_DIR / modpack
    )


  def is_error(self, data) -> bool:
    if isinstance(data, dict) and data.get("status") == "error":
      self.window.evaluate_js(
        'window.GameLog.setErrorr("Ошибка подключения", "Повторите попытку через некоторое время или обратитесь в тикет")'
      )
      return True
    return False


  async def run(self) -> None:
    async with self.client as api:
      modpack_url = f"{_config_.API}/modpacks/{self.modpack}"
      modpack_manifest = await api.get_from_url(modpack_url)

      if self.is_error(modpack_manifest): return

      java_manifest = await api.get_from_url(
        modpack_manifest["java"]["windowsUrl"]
      )

      if self.is_error(java_manifest): return
    
      assets_manifest = await api.get_from_url(
        modpack_manifest["assets"]["urls"]
      )

      if self.is_error(assets_manifest): return

    try: 
      self.window.evaluate_js(f'window.GameLog.setStage("Загрузка java")')
      executable_java = await self.loader.download_java(
        java_manifest, modpack_manifest["java"]["version"]
      )

      self.window.evaluate_js(f'window.GameLog.setStage("Загрузка ассетов")')
      assets_dir = await self.loader.download_assets(
        assets_manifest, modpack_manifest["assets"]["index"],
        modpack_manifest["assets"]["id"]

      )

      self.window.evaluate_js(f'window.GameLog.setStage("Загрузка библиотек")')
      await self.loader.download_libraries(
        modpack_manifest["libraries"]
      )

      self.window.evaluate_js(f'window.GameLog.setStage("Загрузка ресурсов")')
      await self.loader.download_resources(
        modpack_manifest["resources"]
      )

    except RetryError as e:
      original = e.last_attempt.exception()
      if isinstance(original, (aiohttp.ClientError, asyncio.TimeoutError, OSError)):
        logger.critical(f"Failed after retries: {original}")
      
      else:
        logger.critical(e)

      self.window.evaluate_js(
        'window.GameLog.setErrorr("Ошибка подключения", "Повторите попытку через некоторое время или обратитесь в тикет")'
      ); return


    self.window.evaluate_js(f'window.GameLog.setStage("Запуск...")')
    self.window.evaluate_js(f'window.GameLog.setCurrentFile("Готов")')
    self.window.evaluate_js(f'window.GameLog.setMaxProgress(0)')

    LaunchCommand = self.command.get(
      modpack_manifest["command"], 
      assets_dir, 
      executable_java,
      self.settings["ram"]
    )

    subprocess.Popen(
      LaunchCommand, 
      cwd=_config_.UPDATES_DIR / self.modpack,
      close_fds=True
    )

    self.window.destroy()

