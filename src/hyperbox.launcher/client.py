import aiohttp
import asyncio
from loguru import logger

from _config_ import _config_


class Client:
  def __init__(self, host=_config_.API):
    self.base_url = host
    self.session = None

  async def __aenter__(self):
    self.session = aiohttp.ClientSession()
    return self

  async def __aexit__(self, exc_type, exc, tb):
    await self.session.close()


  async def _request(self, method, url=None, endpoint=None, params=None, json=None):
    url = url or f"{self.base_url}/{endpoint}"

    try:
      async with self.session.request(
        method=method, 
        url=url, 
        params=params, 
        json=json,
        timeout=10
      ) as response:
        
        if response.status >= 400:
          text = await response.text()
          logger.error(f"HTTP {response.status} error from {url}: {text}")
          return {
            "status": "error",
            "type": "http_error",
            "code": response.status,
            "error": text
          }
        
        return await response.json()

    except aiohttp.ClientConnectionError as e:
      logger.error(f"Connection error: {e}")
      return {
        "status": "error",
        "type": "connection_error",
        "error": str(e)
      }

    except asyncio.TimeoutError:
      logger.error(f"Timeout while requesting {url}")
      return {
        "status": "error",
        "type": "timeout",
        "error": "request_timeout"
      }

    except Exception as e:
      logger.error(f"Unexpected error: {e}")
      return {
        "status": "error",
        "type": "unexpected_error",
        "error": str(e)
      }


  async def try_to_login(self, username: str, token: str) -> dict:
    return await self._request("POST", endpoint="users/login", json={
      "username": username,
      "token": token
    })

  async def get_modpacks_data(self) -> list:
    return await self._request("GET", endpoint="modpacks/getlist")
  
  async def get_modpack_manifest(self, modpack: str) -> dict:
    return await self._request("GET", endpoint="modpacks", params={"modpack": modpack})
  
  async def get_from_url(self, url: str) -> dict:
    return await self._request("GET", url=url)
  
  async def upload_skin(self, base64Data, username, assets_token) -> dict:
    return await self._request("POST", endpoint="skins/upload_skin", json={
      "base64Data": base64Data,
      "username": username,
      "app_token": assets_token
    })
