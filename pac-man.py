import sys
import pygame
from configuration_files import load_config
from entities import GameEntities



def main() -> None:
    """Program entry point."""
    
    # make surface for all screen
    pygame.init()
    surface = pygame.display.set_mode((800,800))
    pygame.display.set_caption("Pac-Man")

    # The program must receive exactly one argument:
    # the configuration file.
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

    # Load and validate the configuration.
    config = load_config(config_filename)

    # Create the main container of the game entities.
    game = GameEntities(**config)

    # Simple test output for the current development stage.
    print("[Info] GameEntities created successfully.")
    print(f"[Info] Configuration loaded from: {config_filename}")
    print(game.level.maze.maze)
    game.level.next_level()
    print("\n==========================\n")
    print(game.level.maze.maze)
    

if __name__ == "__main__":
    main()
    