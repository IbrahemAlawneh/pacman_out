import os
import sys
import pygame
from configuration_files import load_config
from screens import ScreenManager


def main() -> None:
    """Program entry point."""

    # --- PYINSTALLER PATH FIX ---
    if getattr(sys, 'frozen', False):
        os.chdir(getattr(sys, '_MEIPASS'))
    else:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # make surface for all screens
    pygame.init()
    pygame.mixer.init()
    surface = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption("Pac-Man")

    if len(sys.argv) < 2:
        config_path = "config.json"
    else:
        config_path = sys.argv[1]

    # The configuration filename must be a JSON file.
    if not config_path.lower().endswith(".json"):
        print(
            "[Warning] Invalid configuration file. "
            "The file must have a .json extension."
        )
        return

    config = load_config(config_path)
    mang = ScreenManager(surface, config)
    mang.run()


if __name__ == "__main__":
    main()
