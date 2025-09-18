import json
import re

from client import WebSocketClient as ws
from _config_ import _config_

class Auth:
  def __init__(self):
    self.username: str | None = 'Pixel_Loop'

  @staticmethod
  def _is_login_valid(login: str) -> bool:
    return bool(re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]{2,15}', login))
  
  @staticmethod
  def _is_token_valid(token: str) -> bool:
    m = re.match(r'^([A-Za-z0-9]{7})-([A-Za-z0-9]{5})-([A-Za-z])(\d+)([A-Za-z]{2})-([A-Za-z0-9]{3})$', token)
    return bool(m and int(m.group(4)) % 4 == 0)
  
  @staticmethod
  def _save_options(login: str, token: str) -> None: 
    with open(_config_.CONFIG_FILE, "r+", encoding="utf-8") as config_file:
      config_data = json.load(config_file)

      config_data.update({ "login": login, "token": token })
      
      config_file.seek(0)
      json.dump(config_data, config_file, indent=2, ensure_ascii=False)
      config_file.truncate() 

      print('[Hyperbox] Lasted login options saved to configuration file')

  def get_username(self) -> str | None:
    return self.username

  async def login(self, login: str, token: str) -> bool:
    if Auth._is_login_valid(login) and Auth._is_token_valid(token):
      print('[HyperBox] Login and Token are valid\n' + f'[HyperBox] Trying to login with {login}:{token}')

      ok = await ws().try_to_login(login = login, token = token)

      if ok == 'OSError':
        print('[Hyperbox] Failed to establish connection to server')
        return 'OSError'

      if ok:
        print('[Hyperbox] Succesful')

        Auth._save_options(login, token)
        self.username = login
        return True
    
    print('[Hyperbox] Incorrect Login or Password')
    return False
    