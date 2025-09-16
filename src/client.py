from websockets import connect
from _config_ import _config_

import json

class WebSocketClient:
  def __init__(self, host='0.0.0.0', port=_config_.PORT):
    self.host = host
    self.port = port
    self.base_url = f"ws://{self.host}:{self.port}"

  async def _send_and_receive(self, message: dict) -> dict | str | bool:
    try:
      async with connect(self.base_url) as ws:
        message_json = json.dumps(message)
        await ws.send(message_json)
        response_json = await ws.recv()
        return json.loads(response_json).get('echo')
    except (OSError):
      return 'OSError'

  async def get_version(self) -> str:
    return await self._send_and_receive({'type': 'version'})

  async def try_to_login(self, login: str, token: str) -> bool:
    return await self._send_and_receive({'type': 'login', 'username': login, 'token': token})
    
  async def get_modpacks(self) -> dict:
    return await self._send_and_receive({'type': 'modpacks'})
  
  async def get_minecraft_token(self) -> str:
    return await self._send_and_receive({'type': 'token'})

  async def list_files(self, modpack: str) -> dict:
    return await self._send_and_receive({'type': 'list_files', 'modpack': modpack})
