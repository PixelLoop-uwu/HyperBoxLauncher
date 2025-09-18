import json

from websockets import connect
from _config_ import _config_

data = [
    {
      'id': 0, 
      'title': 'HyperBox: Create',
      'version': '1.20.1',
      'folder': 'create',
      'description': [
        'ljhadsfljnk ljhdfjhl jhjhdjh jh jhsdjhd jjhs jhdjhd jh jhsdjhsfdjh hj jhsdjhdfjhjh jh j',
        'ljhsdfjh hjksjkh kjhsdlkjhgskil ikgyn kgynsdfkgyh skigynsngkyhs gynkgkyhjn kgjh agkhjgkhj'
      ]
    },
    {
      'id': 1, 
      'title': 'HyperBox: Classic',
      'version': '1.20.1',
      'folder': 'vanilla',
      'description': [ 
        'lkjhdfalkjh fkljh s djh kfsdjhk sfhjksjhk sdfjhh fjlhjkncd coiucoiuc xoiuzxo iuzxczmz xczxc',
        'olujih adsojhk lk;jhsd azclkjhcdsavk ljhsdavc lkjsdackljdsc amnbzcv nmbcx nbmcvxnbmvcx bnxcnbv cxjhus'
      ]
    }
]


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
    # return await self._send_and_receive({'type': 'login', 'username': login, 'token': token})
    return True 

  async def get_modpacks(self) -> list:
    # return await self._send_and_receive({'type': 'modpacks'})
    return data
  
  async def get_minecraft_token(self) -> str:
    return await self._send_and_receive({'type': 'token'})

  async def list_files(self, modpack: str) -> dict:
    return await self._send_and_receive({'type': 'list_files', 'modpack': modpack})
