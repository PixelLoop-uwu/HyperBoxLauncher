from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()

class _config_:
  API = "https://Api.Hyperbox.world"
  DEBUG = True

  MAIN_DIR = Path(os.environ.get('APPDATA', Path.home())) / 'HyperBox'
  TEMP_DIR = Path(os.environ.get('TEMP', "/tmp"))

  CONFIG_FILE = MAIN_DIR / "config.bin"
  UPDATES_DIR = MAIN_DIR / "updates"

  DEFAULT_LAUNCHER_OPTIONS = {
    "ram": 4096,
    "fullscreen": False,
    "debug": False,
    "mainDir": str(MAIN_DIR)
  }