import shutil
import hashlib
import httpx
import aiofiles
import tempfile
import asyncio
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from pathlib import Path
from loguru import logger

from _config_ import _config_

class Loader:
  def __init__(self, main_dir: Path, game_dir: Path, window, limit=35):
    self.game_dir = game_dir
    self.main_dir = main_dir
    self.window = window

    self.sem = asyncio.Semaphore(limit)
    self.client = httpx.AsyncClient(
      limits=httpx.Limits(max_connections=60, max_keepalive_connections=20)
    )

  async def _file_matches(self, path: Path, expected_size: int, expected_sha1: str) -> bool:
    """Check if a file exists and matches expected size and SHA-1."""
    if not path.exists():
      return False
    
    if path.stat().st_size != expected_size:
      logger.warning(f"File {path} exists, but size does not match. Re-downloading.")
      return False
    
    file_sha1 = hashlib.sha1(path.read_bytes()).hexdigest()
    if file_sha1 != expected_sha1:
      logger.warning(f"File {path} exists, but SHA-1 does not match. Re-downloading.")
      return False
    
    logger.info(f"File {path} already exists and matches the checksum, skipping.")
    return True
  
  
  @retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(min=1, max=5),
    retry=retry_if_exception_type((httpx.HTTPError, httpx.TimeoutException, OSError))
  )
  async def _download_file(self, file_info: dict, base_dir: Path) -> None:
    """Download a file asynchronously and verify its integrity."""
    path = base_dir / file_info["path"]
    path.parent.mkdir(parents=True, exist_ok=True)

    if await self._file_matches(path, file_info["size"], file_info["sha1"]):
      return

    temp_dir = Path(tempfile.mkdtemp())
    temp_path = temp_dir / path.name

    try:
      logger.info(f"Downloading {file_info['url']} -> {temp_path}")
      
      async with self.client.stream("GET", file_info["url"], timeout=60) as response:
        response.raise_for_status()
          
        async with aiofiles.open(temp_path, "wb") as f:
          async for chunk in response.aiter_bytes(chunk_size=8192):
            await f.write(chunk)

      if temp_path.stat().st_size != file_info["size"]:
        raise ValueError(
          f"File size mismatch: expected {file_info['size']}, got {temp_path.stat().st_size}"
        )
      
      sha1 = hashlib.sha1(temp_path.read_bytes()).hexdigest()
      if sha1 != file_info["sha1"]:
        raise ValueError(
          f"SHA-1 mismatch: expected {file_info['sha1']}, got {sha1}"
        )
      
      shutil.move(str(temp_path), str(path))
      logger.info(f"File successfully downloaded and moved: {path}")
      
    finally:
      if temp_dir.exists():
        shutil.rmtree(temp_dir)


  # * java
  async def download_java(self, java: list, version: str) -> Path:
    self.window.evaluate_js(f'window.GameLog.setMaxProgress({len(java)})')
    java_dir = self.main_dir / "java" / version

    async def wrapper(item):
      async with self.sem:
        self.window.evaluate_js(f'window.GameLog.setCurrentFile("{Path(item["path"]).name}")')
        self.window.evaluate_js('window.GameLog.addProgress(1)')
        await self._download_file(item, java_dir)

    tasks = [wrapper(item) for item in java]
    await asyncio.gather(*tasks)

    self.window.evaluate_js(f'window.GameLog.resetProgress()')
    return java_dir / "bin/java.exe" if _config_.DEBUG else "bin/javaw.exe"

  # * Libraries
  async def download_libraries(self, libraries: list) -> None:
    self.window.evaluate_js(f'window.GameLog.setMaxProgress({len(libraries)})')
    libraries_dir = self.game_dir / "libraries"

    async def wrapper(lib):
      async with self.sem:
        self.window.evaluate_js(f'window.GameLog.setCurrentFile("{Path(lib["path"]).name}")')
        self.window.evaluate_js('window.GameLog.addProgress(1)')
        await self._download_file(lib, libraries_dir)

    tasks = [wrapper(lib) for lib in libraries]
    await asyncio.gather(*tasks)

    self.window.evaluate_js(f'window.GameLog.resetProgress()')

  # * Game resources
  async def download_resources(self, resources: dict) -> None:
    async def wrapper(item):
      async with self.sem:
        self.window.evaluate_js(f'window.GameLog.setCurrentFile("{Path(item["path"]).name}")')
        self.window.evaluate_js('window.GameLog.addProgress(1)')
        await self._download_file(item, self.game_dir)

    # Required
    required_resources = resources["requiredResources"]

    self.window.evaluate_js(f'window.GameLog.setMaxProgress({len(required_resources)})')
    tasks = [wrapper(item) for item in required_resources]
    await asyncio.gather(*tasks)

    # Static
    if not _config_.CONFIG_FILE.exists():
      static_resources = resources["staticResources"]

      self.window.evaluate_js(f'window.GameLog.setMaxProgress({len(static_resources)})')
      tasks = [wrapper(item) for item in static_resources]
      await asyncio.gather(*tasks)

    self.window.evaluate_js(f'window.GameLog.resetProgress()')

  # * Assets
  async def download_assets(self, assets: list) -> None:
    assets_dir = self.main_dir / "assets"

    self.window.evaluate_js(f'window.GameLog.setMaxProgress({len(assets)})')

    async def wrapper(f):
      async with self.sem:
        self.window.evaluate_js(f'window.GameLog.setCurrentFile("{Path(f["path"]).name}")')
        self.window.evaluate_js('window.GameLog.addProgress(1)')
        await self._download_file(f, assets_dir)

    tasks = [wrapper(f) for f in assets]
    await asyncio.gather(*tasks)

    self.window.evaluate_js(f'window.GameLog.resetProgress()')
    return assets_dir
    