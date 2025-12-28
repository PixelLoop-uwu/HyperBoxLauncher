from pathlib import Path

from uuid import uuid4
from auth import auth


class Command:
  def __init__(self, main_dir, game_dir):
    self.game_dir = game_dir
    self.main_dir = main_dir

  def get(self, command_template: dict, assets_dir: Path, executable_java: Path, ram_amount: int) -> list:
    command = [str(executable_java).replace('\\', "/"), "-Xms1G", f"-Xmx{ram_amount}M", f"-DUltraSecretKey={auth.get_assets_token()}"]

    placeholders = {
      "natives_path": self.main_dir / "natives",
      "libraries_path": self.game_dir / "libraries",
      "username": auth.get_username(),
      "game_path": self.game_dir,
      "assets_path": assets_dir,
      "uuid": uuid4(),
      "token": uuid4(),
    }

    for arg in command_template:
      command.append(arg.format_map(placeholders))

    return command