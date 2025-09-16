from dotenv import load_dotenv
import os

class _config_ ():
  load_dotenv()

  API = os.getenv("API")
  PORT = os.getenv("server-port")

  # MAIN_DIR = os.environ.get('USERPROFILE') + '/AppData/Roaming/.HyperBox'
  MAIN_DIR = 'D:/HyperBox'

  CONFIG_FILE = f"{MAIN_DIR}/config.json"
  UPDATES_DIR = f"{MAIN_DIR}/updates"
  # TEMP_DIR = os.environ['TEMP']