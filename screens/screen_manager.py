import pygame
from entities import GameEntities
from enum import Enum
from .high_score_screen import HighScoreScreen
from .instructions_screen import InstructionsScreen
from .main_screen import MainScreen
from .maze_screen import GameScreen
from .setting_screen import SettingScreen
import pygame

class ScreenManager:
    """
    المدير المركزي لجميع شاشات اللعبة (State Machine).
    يتحكم في الانتقالات، ويدير دورة حياة الشاشات، ويوفر الذاكرة.
    """

    def __init__(self, surface: pygame.Surface, config: dict):
        self.surface = surface
        self.config = config  # هذا القاموس هو المرجع الحي (Live Reference) للإعدادات

        self.menus = {
            "main_menu": MainScreen(self.surface),
            # نمرر الـ config لشاشة الإعدادات لتقرأ منه وتعدل عليه مباشرة
            "settings": SettingScreen(self.surface, self.config),
            "instructions": InstructionsScreen(self.surface),
            "high_scores": HighScoreScreen(self.surface),
        }

        self.current_screen_name = "main_menu"
        self.active_screen = self.menus[self.current_screen_name]

        self.clock = pygame.time.Clock()
        self.running = True

    def run(self) -> None:
        """
        الحلقة الرئيسية للعبة (The Main Game Loop).
        هذه الدالة ستبقى تعمل حتى يقرر اللاعب إغلاق اللعبة.
        """
        while self.running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    continue

                action = self.active_screen.handle_event(event)
                
                self._handle_action(action)

            # 2. الرسم وتحديث الشاشة
            self.active_screen.draw()
            
            pygame.display.flip()
            self.clock.tick(60)

    def _handle_action(self, action: str | None) -> None:

        if not action:
            return

        if action == "quit":
            self.running = False

        elif action == "play":
            self.active_screen = GameScreen(self.surface, self.config)
            self.current_screen_name = "play"
            print("[System] PlayScreen created. Game is starting with current config.")


        elif action == "back_to_menu":
            if self.current_screen_name == "play":
                print("[System] Exiting game. PlayScreen & GameEntities destroyed (RAM Freed).")
            
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