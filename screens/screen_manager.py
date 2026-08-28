import pygame
from entities import GameEntities
from enum import Enum
from .high_score_screen import HighScoreScreen
from .instructions_screen import InstructionsScreen
from .main_screen import MainScreen
from .maze_screen import GameScreen
from .setting_screen import SettingScreen


class ScreenManager:
    """Central manager for all games screens (State Machine)
    Handles transitions, screen lifecycle, and memory"""
    def __init__(self, surface: pygame.Surface, config: dict):
        self.surface = surface
        self.config = config
        self.current_music_path = None

        self.menus = {
            "main_menu": MainScreen(self.surface),
            "settings": SettingScreen(self.surface, self.config),
            "instructions": InstructionsScreen(self.surface, self.config),
            "high_scores": HighScoreScreen(self.surface),
        }

        self.current_screen_name = "main_menu"
        self.active_screen = self.menus[self.current_screen_name]
        self.clock = pygame.time.Clock()
        self.running = True
        
        
    def play_music(self, music_path: str) -> None:        
        if self.current_music_path == music_path:
            return 

        try:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(-1)
            self.current_music_path = music_path
        except pygame.error as e:
            print(f"Error loading music {music_path}: {e}")


    def run(self) -> None:
        """Main game loop
        Runs continuously until the player closes the game"""
        self.play_music("assets/sounds/background_music.ogg")
        while self.running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    continue

                action = self.active_screen.handle_event(event)

                if action is not None:
                    self._handle_action(action)


            if isinstance(self.active_screen, GameScreen):
                self.active_screen.update()

            self.active_screen.draw()
            pygame.display.flip()
            self.clock.tick(60)

    def _handle_action(self, action: str | None) -> None:

        self.play_music("assets/sounds/background_music.ogg")

        if not action:
            return

        if action == "quit":
            self.running = False
            
        
        elif action == "play":
            self.active_screen = GameScreen(self.surface, self.config)
            self.current_screen_name = "play"
            print(
                "[System] PlayScreen created. "
                "Game is starting with current config."
            )
            self.current_music_path = None

        elif action == "back_to_menu":
            if self.current_screen_name == "play":
                print(
                    "[System] Exiting game. "
                    "PlayScreen & GameEntities destroyed (RAM Freed)."
                )

            self.active_screen = self.menus["main_menu"]
            self.current_screen_name = "main_menu"

        elif action == "settings":
            self.active_screen = self.menus["settings"]
            self.current_screen_name = "settings"

        elif action == "instructions":
            self.active_screen = self.menus["instructions"]
            self.current_screen_name = "instructions"

        elif action == "highscores":
            self.active_screen = self.menus["high_scores"]
            self.current_screen_name = "high_scores"
