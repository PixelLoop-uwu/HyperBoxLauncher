import httpx
from loguru import logger

from _config_ import _config_


class Client:
  def __init__(self, host=_config_.API):
    self.client = httpx.AsyncClient(
      base_url=host,
      timeout=10.0,
      follow_redirects=True,
      trust_env=False
    )

  async def __aenter__(self):
    await self.client.__aenter__()
    return self

  async def __aexit__(self, exc_type, exc, tb):
    await self.client.__aexit__(exc_type, exc, tb)

  async def _request(
    self, 
    method: str, 
    url: str = None, 
    endpoint: str = None, 
    params: dict = None, 
    json: dict = None,
    header: str = None
  ):
    target = url or endpoint

    try:
      response = await self.client.request(
        method=method,
        url=target,
        params=params,
        json=json,
        headers=header
      )

      if response.is_error:
        logger.error(
          f"HTTP {response.status_code} error from "
          "{response.url}: {response.text}"
        )
        return {
          "status": "error",
          "error": "http_error",
          "code": response.status_code,
          "text": response.text
        }

      return response.json()

    except httpx.ConnectError as e:
      logger.error(f"Connection error: {e}")
      return {
        "status": "error",
        "error": "connection_error",
        "text": str(e)
      }

    except httpx.TimeoutException:
      logger.error(f"Timeout while requesting {target}")
      return {
        "status": "error",
        "error": "timeout",
        "text": "request_timeout"
      }

    except Exception as e:
      logger.error(f"Unexpected error: {e}")
      return {
        "status": "error",
        "error": "unexpected_error",
        "text": str(e)
      }


  async def try_to_login(self, username: str, token: str) -> dict:
    return await self._request(
      "POST", 
      endpoint="/users/login", 
      json={"minecraft_username": username, "token": token}
    )
  
  async def get_modpack_manifest(self, modpack: str) -> dict:
    return await self._request(
      "GET", 
      endpoint="/modpacks/get", 
      params={"modpack": modpack}
      )
  
  async def upload_skin(self, base64Data: str, username: str, jwt: str) -> dict:
    header = {"Authorization": f"Bearer {jwt}"}

    return await self._request(
      "POST", 
      header=header, 
      endpoint="/skins/upload_skin", 
      json={"base64data": base64Data, "minecraft_username": username}
    )
  
  async def get_from_url(self, url: str) -> dict:
    return await self._request("GET", url=url)