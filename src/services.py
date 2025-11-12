import json
import os
import psutil
from pathlib import Path

from _config_ import _config_


def check_config_file() -> None:
  path = _config_.CONFIG_FILE

  try:
    if not path.exists():
      path.write_text(json.dumps({}, indent=2), encoding='utf-8')
      return
    json.loads(path.read_text(encoding='utf-8'))
  except json.JSONDecodeError:
    path.write_text(json.dumps({}, indent=2), encoding='utf-8')


def get_last_login_options() -> tuple[str, str]:
  check_config_file()

  with open(_config_.CONFIG_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

    if "auth" in data:
      return data["auth"].get("username", ""), data["auth"].get("token", "")

    return '', ''

def save_last_login_options(username: str, token: str) -> None:
  check_config_file()

  with open(_config_.CONFIG_FILE, "r+", encoding="utf-8") as f:
    data = json.load(f)

    data.update({"auth": {"username": username, "token": token}})

    f.seek(0)
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.truncate()


def get_launcher_settings() -> dict:
  check_config_file()

  with open(_config_.CONFIG_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)
    mem = psutil.virtual_memory()
    mb_rounded = (mem.total + 512) // 1024 * 1024

    maxRam = mb_rounded // 1024 // 1024

  default_options = {
    "ram": 4096,
    "fullscreen": False,
    "debug": False,
    "mainDir": str(_config_.MAIN_DIR)
  }

  if "options" not in data:
    data["options"] = default_options.copy()
  else:
    for key, value in default_options.items():
      if key not in data["options"]:
        data["options"][key] = value

  data["options"]["maxRam"] = maxRam

  return data["options"]

def save_launcher_settings(settings: dict) -> None:
  check_config_file()

  with open(_config_.CONFIG_FILE, "r+", encoding="utf-8") as f:
    data = json.load(f)

    data.update({"options": settings})

    f.seek(0)
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.truncate()

    print("[Hyperbox] Minecraft settings saved")

  

def open_game_folder(modpack) -> None:
  path = _config_.UPDATES_DIR / modpack
  if not path.exists():
    path.mkdir(parents=True, exist_ok=True)

  os.startfile(path)
