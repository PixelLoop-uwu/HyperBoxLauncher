import aiohttp

pizdec = [
    {
      "id": 0,
      "title": "Modpack One",
      "version": "1.0.0",
      "description": ["Описание модпака", "Еще строка описания"],
      "folder": "modpack"
    },
    {
      "id": 1,
      "title": "Modpack Two",
      "version": "2.1.0",
      "description": ["Описание второго модпака"],
      "folder": "modpack2"
    }
  ]



class Client:
  def __init__(self, host="127.0.0.1",):
    self.base_url = f"https://{host}"
    self.session = None

  async def __aenter__(self):
    self.session = aiohttp.ClientSession()
    return self

  async def __aexit__(self, exc_type, exc, tb):
    await self.session.close()


  async def _request(self, method, endpoint, params=None, json=None):
    url = f"{self.base_url}/{endpoint}"
    
    async with self.session.request(method=method, url=url, params=params, json=json) as request:
      return await request.json()
    


  async def try_to_login(self, username: str, token: str) -> dict:
    """
    Can return: 
      {"status": True} or {"error": token_or_username_is_incorrect}
    """
    return {"status": True}

    return await self._request("POST", "minecraftlogin", json={
      "username": username,
      "token": token
    })

  async def get_modpacks_data(self) -> list:
    return pizdec

    return await self._request("GET", "modpacks")
  
  async def get_modpack_manifest(self, modpack) -> dict:
    return await self._request("GET", "modpackget", params=(modpack))