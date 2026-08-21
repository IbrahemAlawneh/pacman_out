import sys
import pygame
from configuration_files import load_config
from entities import GameEntities
from screens import MainScreen


def main() -> None:
    """Program entry point."""
    
    # make surface for all screen
    pygame.init()
    pygame.mixer.init()
    surface = pygame.display.set_mode((1200,800))
    pygame.display.set_caption("Pac-Man")
    
    main_screen = MainScreen(surface)
    clock = pygame.time.Clock()
    
    try:
        pygame.mixer.music.load("assets/sounds/background_music.ogg")
        pygame.mixer.music.set_volume(0.3)
        
        # الرقم -1 يعني أن الموسيقى ستتكرر إلى ما لا نهاية (Loop)
        pygame.mixer.music.play(-1)
    
    except pygame.error as e:
        print(f"[Warning] Could not load background music: {e}")
    
    
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
    
    running = True
    while running:
        
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
                continue

            action = main_screen.handle_event(event)
            
            #هذول للتست ورح ينشالن
            if action == "quit":
                running = False

            elif action == "play":
                print("[Info] Play selected.")

            elif action == "highscores":
                print("[Info] High Scores selected.")

            elif action == "settings":
                print("[Info] Settings selected.")

        main_screen.draw()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    
    
    
    
    # Load and validate the configuration.
    config = load_config(config_filename)

    # هاي بدها تعديل مكان استدعائها لبعدين
    game = GameEntities(**config)
    
    

if __name__ == "__main__":
    main()
    