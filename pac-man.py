import sys
import pygame
from configuration_files import load_config
from screens import ScreenManager


def main() -> None:
    """Program entry point."""
    # make surface for all screens
    pygame.init()
    pygame.mixer.init()
    surface = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption("Pac-Man")

    if len(sys.argv) != 2:
        print(
            "[Warning] Invalid number of arguments. "
            "Usage: python3 pac-man.py config.json"
        )
        return

    config_filename = sys.argv[1]

    # The configuration filename must be a JSON file.
    if not config_filename.lower().endswith(".json"):
        print(
            "[Warning] Invalid configuration file. "
            "The file must have a .json extension."
        )
        return

    config = load_config(config_filename)
    mang = ScreenManager(surface, config)
    mang.run()


if __name__ == "__main__":
    main()
