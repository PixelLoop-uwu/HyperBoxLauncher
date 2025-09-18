import os

class Utils:

  @staticmethod
  def open_game_folder(path: str) -> None:
    if not os.path.exists(path):
      os.makedirs(path, exist_ok=True)
    os.startfile(path)

    
    