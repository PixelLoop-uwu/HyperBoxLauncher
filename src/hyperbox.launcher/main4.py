import webview
import sys
from loguru import logger

import utils
from webview_api import Api

__VERSION__ = 1


def run() -> None:
  utils.load_config()
  logger.remove()

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
    url="../webUI/index.html",

    frameless=True,
    easy_drag=False,
    width=910,
    height=520,
    background_color="#1a1a1a",
    js_api=Api()
  )

  webview.start(debug=True)


if __name__ == '__main__':
  run()

