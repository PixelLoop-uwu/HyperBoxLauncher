import psutil
import base64
from io import BytesIO
from PIL import Image
from pathlib import Path
from loguru import logger

from _config_ import _config_
from utils import load_config, write_config
from client import Client

def get_main_dir() -> Path:
	cfg = load_config()
	options = cfg.get("options", {})
	main_dir = options.get("mainDir")

	return Path(main_dir) if main_dir else _config_.MAIN_DIR


def get_last_login_options() -> tuple[str, str]:
	cfg = load_config()
	auth = cfg.get("auth", {})
    
	return auth.get("username", ""), auth.get("token", "")


def save_last_login_options(username: str, token: str) -> None:
  write_config({
    "auth": {
      "username": username,
      "token": token
  }}) 


def get_launcher_settings() -> dict:
	cfg = load_config()

	options = cfg.setdefault("options", {})

	mem = psutil.virtual_memory()
	maxRam = (mem.total + (1024**3) - 1) // (1024**3) * 1024

	for key, value in _config_.DEFAULT_LAUNCHER_OPTIONS.items():
		options.setdefault(key, value)

	options["maxRam"] = maxRam
	return options


def save_launcher_settings(settings: dict) -> None:
  write_config( {"options": settings} )
  logger.success("Minecraft settings saved")


async def upload_skin(base64Data) -> dict:
	from auth import auth
	try:
		img_bytes = base64.b64decode(base64Data)
		img = Image.open(BytesIO(img_bytes))
	
	except Exception as e:
		logger.error(str(e))
		return {"status": "error", "text": "Файл поврежден"}

	if not img.size in (64, 64):
		logger.error("Incorrect skin format")
		return {"status": "error", "text": "Неверный формат"}

	async with Client() as client:
		return await client.upload_skin(
			base64Data, 
			auth.get_username(), 
			auth.get_assets_token()
		)
 
async def get_skin() -> str:
	async with Client() as client:
		from auth import auth
		return await client.get_skin(auth.get_username())
	
