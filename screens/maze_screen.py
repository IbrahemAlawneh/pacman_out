import pygame
from entities import GameEntities


class GameScreen:
    """Handles routing the input and triggering the rendering of the game."""

    def __init__(self, screen: pygame.Surface, config: dict):
        self.screen = screen
        self.config = config
        self.entities = GameEntities(**config)

    def handle_event(self, event: pygame.event.Event) -> str | None:
        if event.type == pygame.KEYDOWN:
            
            if event.key in (pygame.K_ESCAPE, pygame.K_p):
                print("pause screen is open")
                return "back_to_menu"

            elif event.key in (pygame.K_UP, pygame.K_w):
                print("[Action] Move UP")
                # self.pacman.set_direction("UP")
                
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                print("[Action] Move DOWN")
                # self.pacman.set_direction("DOWN")
                
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                print("[Action] Move LEFT")
                # self.pacman.set_direction("LEFT")
                
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                print("[Action] Move RIGHT")
                # self.pacman.set_direction("RIGHT")

            elif event.key in (pygame.K_F1, pygame.K_F2, pygame.K_F3, pygame.K_F4, pygame.K_F5):
                cheats = self.config.get("cheats")
                
                if cheats:
                    enable_all = cheats.get("enable_all", False)
                    
                    if event.key == pygame.K_F1:
                        if enable_all or cheats.get("level_skip", False):
                            print("[Cheat] F1 Activated: Level Skipped!")
                            # self.level_manager.skip()
                            
                    elif event.key == pygame.K_F2:
                        if enable_all or cheats.get("ghost_freeze", False):
                            print("[Cheat] F2 Activated: Ghosts Frozen!")
                            # self.ghost_manager.freeze_all()
                            
                    elif event.key == pygame.K_F3:
                        if enable_all or cheats.get("extra_life", False):
                            print("[Cheat] F3 Activated: Extra Life Added!")
                            # self.config["lives"] += 1
                            
                    elif event.key == pygame.K_F4:
                        if enable_all or cheats.get("speed_boost", False):
                            print("[Cheat] F4 Activated: Speed Boost!")
                            # self.pacman.apply_speed_boost()
                            
                    elif event.key == pygame.K_F5:
                        if enable_all or cheats.get("infinite_lives", False):
                            print("[Cheat] F5 Activated: Pac-Man have infinite_lives")
                            # self.pacman.set_invincible(True)

        return None

    def update(self) -> None:
        self.entities.update_logic()

    def draw(self) -> None:
        self.screen.fill((0, 0, 0))
