import re
from loguru import logger

from client import Client
from services import save_last_login_options


class Auth:
  def __init__(self):
    self.client = Client()
    self.username = None
    self.assets_token = None

  @staticmethod
  def _is_username_valid(username: str) -> bool:
    pattern = r'^[a-zA-Z0-9_]{3,16}$'
    return bool(re.match(pattern, username))
  
  @staticmethod
  def _is_token_valid(token: str) -> bool:
    pattern = r'^[A-Za-z0-9]{7}-[A-Za-z0-9]{5}-([A-Za-z])([0-9]{2})([A-Za-z0-9]{2})-[A-Za-z0-9]{3}$'
    m = re.match(pattern, token)
    if not m:
      return False
    
    try:
      number = int(m.group(2))
    except ValueError:
      return False

    return number % 4 == 0
  

  def get_username(self) -> str:
    """Return minecraft username."""
    return self.username
  
  def get_assets_token(self) -> str:
    """Return assets token."""
    return self.assets_token


  async def try_to_login(self, username: str, token: str) -> dict:

    if not (Auth._is_username_valid(username) and Auth._is_token_valid(token)):
      logger.error("Username or Token is invalid")
      return {"status": "error", "type": "token_or_username_is_invalid"}

    # API request
    async with self.client as api:
      logger.info(f"Trying to login with {username} {token}")
      ok = await api.try_to_login(username, token)

      logger.error(ok)

      if ok.get("status") == True:
        self.assets_token = ok.get("assets_token", None)
        logger.success("Success")

      # if ok.get("status") == "error":
      #   logger.error(f'Authorization error: {ok["error"]}')

      self.username = username
      save_last_login_options(username, token)

    return ok
  

auth = Auth()   