from dotenv import load_dotenv
from pathlib import Path
import os

class _config_:
  load_dotenv()

  API = os.getenv("API")

  # MAIN_DIR = Path(os.environ.get('APPDATA', Path.home() / 'AppData' / 'Roaming'))
  MAIN_DIR = Path('G:/HyperBox')

  CONFIG_FILE = MAIN_DIR / "config.json"
  UPDATES_DIR = MAIN_DIR / "updates"
  TEMP_DIR = Path(os.environ['TEMP'])