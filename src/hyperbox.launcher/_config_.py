from dotenv import load_dotenv
from pathlib import Path
import os

class _config_:
  load_dotenv()

  # API = "http://127.0.0.1:8000"
  API = "https://Api.Hyperbox.world"

  MAIN_DIR = Path(os.environ.get('APPDATA', Path.home())) / 'HyperBox'
  # MAIN_DIR = Path('G:/HyperBox')

  CONFIG_FILE = MAIN_DIR / "config.bin"
  UPDATES_DIR = MAIN_DIR / "updates"
  TEMP_DIR = Path(os.environ['TEMP'])

  DEFAULT_LAUNCHER_OPTIONS = {
    "ram": 4096,
    "fullscreen": False,
    "debug": False,
    "mainDir": str(MAIN_DIR)
  }