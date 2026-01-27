import webview
import sys, os
from loguru import logger

import utils
from webview_api import Api
from _config_ import _config_

__VERSION__ = 1


def get_path(file_name: str) -> str:
  here = os.path.dirname(__file__)
  return os.path.join(here, "webUI", file_name)


def run() -> None:
  utils.load_config()
  logger.remove()

  if sys.stderr:
    logger.add(
      sys.stderr,
      level="DEBUG",
      format=
        "<green>{time:HH:mm:ss}</green> | "
        "<level>{level}</level> | "
        "<cyan>{name}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    )

  webview.create_window(
    title="HyperBox Launcher",
    url=get_path("index.html"),
    # url="../webUI/index.html",

    frameless=True,
    easy_drag=False,
    width=910,
    height=520,
    background_color="#1a1a1a",
    js_api=Api(),
  )

  webview.start(debug=_config_.DEBUG, icon=get_path("logo.ico"))


if __name__ == '__main__':
  run()

