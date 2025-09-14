import webview
import time

from client import WebSocketClient

__VERSION__ = 0.1

class Api():
  def close(self):
    window.destroy()

  def minimize(self):
    window.minimize()


class main():
  def run(self):
    global window

    window = webview.create_window(
      "HyperBox Launcher",
      "gui/index.html",

      frameless = True,
      easy_drag = True,
      width = 910,
      height = 520,
      background_color = "#1a1a1a",
      js_api = Api()
    )

    webview.start(debug=True)


if __name__ == '__main__':
  main().run()

