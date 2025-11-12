import re

from asyncio import TimeoutError
from aiohttp import ClientConnectionError, ClientError

from client import Client
from services import save_last_login_options


class Auth:
  def __init__(self):
    self.client = Client()
    self.username = None

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
    """Returns minecraft username"""
    return self.username


  async def try_to_login(self, username: str, token: str) -> dict:
    """
    Can return:
      {"status": True} 
      {"error": "token_or_username_is_incorrect}
      {"error": "token_or_username_is_invalid"}
      {"error": "connection_error"}
    """

    if not (Auth._is_username_valid(username) and Auth._is_token_valid(token)):
      print("[HyperBox] Token or Username is invalid")
      return {"error": "token_or_username_is_invalid"}

    try:
      # API request
      async with self.client as api:
        print("[HyperBox] Trying to login....")
        ok = await api.try_to_login(username, token)

        self.username = username
        save_last_login_options(username, token)

        print("[HyperBox] Success")

    except (TimeoutError, ClientConnectionError, ClientError) as e:
      print("[HyperBox] Connection error:", e)
      return {"error": "connection_error"}

    return ok
  