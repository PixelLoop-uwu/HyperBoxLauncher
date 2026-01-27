import pickle
import os
import sys
import webview
from pathlib import Path
from loguru import logger

from _config_ import _config_


def load_config() -> dict:
  _config_.CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)

  try:
    with open(_config_.CONFIG_FILE, "rb") as f:
      return pickle.load(f)

  except Exception as e:
    logger.warning(f"Config file is invalid: {e}")

    with open(_config_.CONFIG_FILE, "wb") as f:
      pickle.dump({}, f)
      logger.info("Config file created")

    return {}

def write_config(data: dict) -> None:
  cfg = load_config()
  cfg.update(data)

  with open(_config_.CONFIG_FILE, "wb") as f:
    pickle.dump(cfg, f)


def open_game_folder(path) -> None:
  path = Path(path)
  if not path.exists():
    path.mkdir(parents=True, exist_ok=True)

  os.startfile(path)

def critical_error(error: str) -> None:
  logger.critical(error)
  webview.windows[0].destroy()
