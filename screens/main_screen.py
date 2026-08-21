from pathlib import Path
import pygame

class MainScreen:
    """
    Main menu screen.
    """

    # ---------------------------------------------------------
    # Screen configuration
    # ---------------------------------------------------------
    WIDTH = 1200
    HEIGHT = 800

    ANIMATION_FPS = 30
    TOTAL_FRAMES = 120

    FRAME_PREFIX = "ezgif-frame-"
    FRAME_EXTENSION = ".jpg"

    # ---------------------------------------------------------
    # Menu configuration
    # ---------------------------------------------------------
    BUTTON_WIDTH = 280
    BUTTON_HEIGHT = 58
    BUTTON_GAP = 14

    BUTTON_CENTER_X = WIDTH // 2 + 50
    BUTTON_START_Y = 285 + 50

    # ---------------------------------------------------------
    # Colors
    # ---------------------------------------------------------
    TEXT_COLOR = (255, 255, 255)
    BUTTON_COLOR = (38, 15, 75)
    BUTTON_HOVER_COLOR = (90, 35, 145)
    BUTTON_BORDER_COLOR = (255, 196, 0)
    BUTTON_HOVER_BORDER_COLOR = (255, 230, 80)

    # ---------------------------------------------------------
    # Constructor
    # ---------------------------------------------------------
    def __init__(
        self,
        screen: pygame.Surface,
        assets_path: str | Path = "assets/main_menu_images/main",
    ) -> None:
        
        self.screen = screen
        self.assets_path = Path(assets_path)

        # -----------------------------------------------------
        # Animation state
        # -----------------------------------------------------
        self.animation_finished = False
        
        #sound effect
        self.hover_sound = None
        self.click_sound = None
        try:
            
            self.hover_sound = pygame.mixer.Sound("assets/sounds/hover.wav")
            self.click_sound = pygame.mixer.Sound("assets/sounds/click.wav")
            
            
            self.hover_sound.set_volume(0.25)
            self.click_sound.set_volume(0.8)
        except (FileNotFoundError, pygame.error) as e:
            print(f"[Warning] Could not load sound effects: {e}")
        
        #sound effect
        
        if not self.assets_path.exists():
            print(f"[Warning] Directory '{self.assets_path}' not found. Skipping animation.")
            self.animation_finished = True

        self.animation_start_time = pygame.time.get_ticks()
        
        self.current_frame_index = 0
        self.current_frame_surface: pygame.Surface | None = None
        self.final_frame: pygame.Surface | None = None

        # -----------------------------------------------------
        # Fonts & Buttons
        # -----------------------------------------------------
        self.button_font = pygame.font.Font(None, 42)

        self.buttons = [
            {"text": "PLAY", "action": "play", "rect": pygame.Rect(0, self.BUTTON_START_Y, self.BUTTON_WIDTH, self.BUTTON_HEIGHT)},
            {"text": "HIGH SCORES", "action": "highscores", "rect": pygame.Rect(0, self.BUTTON_START_Y + (self.BUTTON_HEIGHT + self.BUTTON_GAP), self.BUTTON_WIDTH, self.BUTTON_HEIGHT)},
            {"text": "SETTINGS", "action": "settings", "rect": pygame.Rect(0, self.BUTTON_START_Y + 2 * (self.BUTTON_HEIGHT + self.BUTTON_GAP), self.BUTTON_WIDTH, self.BUTTON_HEIGHT)},
            {"text": "QUIT", "action": "quit", "rect": pygame.Rect(0, self.BUTTON_START_Y + 3 * (self.BUTTON_HEIGHT + self.BUTTON_GAP), self.BUTTON_WIDTH, self.BUTTON_HEIGHT)},
        ]

        for button in self.buttons:
            button["rect"].centerx = self.BUTTON_CENTER_X

        self.selected_button_index = 0
        
        
    
    #sound effect start
    
    def handle_event(self, event: pygame.event.Event) -> str | None:
        if not self.animation_finished:
            return None

        previous_index = self.selected_button_index

        # -----------------------------------------------------
        # Keyboard
        # -----------------------------------------------------
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self._select_previous_button()
                
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self._select_next_button()
                
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                return self._activate_selected_button()
                
            elif event.key == pygame.K_ESCAPE:
                return "quit"

        # -----------------------------------------------------
        # Mouse
        # -----------------------------------------------------
        
        
        elif event.type == pygame.MOUSEMOTION:
            mouse_position = event.pos
            for index, button in enumerate(self.buttons):
                if button["rect"].collidepoint(mouse_position):
                    self.selected_button_index = index
                    break 

        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_position = event.pos
                for index, button in enumerate(self.buttons):
                    if button["rect"].collidepoint(mouse_position):
                        self.selected_button_index = index
                        return self._activate_selected_button()

        # -----------------------------------------------------
        # Play Hover Sound
        # -----------------------------------------------------
        
        if self.selected_button_index != previous_index and self.hover_sound:
            self.hover_sound.play()

        return None


    
    #sound effect end
    
    # =========================================================
    # Animation (Optimized: Lazy Loading)
    # =========================================================

    def _load_single_frame(self, frame_number: int) -> pygame.Surface | None:

        filename = f"{self.FRAME_PREFIX}{frame_number:03d}{self.FRAME_EXTENSION}"
        frame_path = self.assets_path / filename

        try:
            frame = pygame.image.load(str(frame_path)).convert()
            
            if frame.get_size() != (self.WIDTH, self.HEIGHT):
                frame = pygame.transform.scale(frame, (self.WIDTH, self.HEIGHT))
                
            return frame
            
        except FileNotFoundError:
            print(f"[Warning] Frame '{filename}' not found.")
            return None
        except pygame.error as error:
            print(f"[Warning] Could not load frame '{filename}': {error}")
            return None

    def _update_animation(self) -> None:
        """
        تحديث الأنيميشن وتحميل الإطار المناسب للوقت الحالي فقط.
        """
        if self.animation_finished:
            return

        elapsed_time = pygame.time.get_ticks() - self.animation_start_time
        frame_duration = 1000 / self.ANIMATION_FPS
        
        target_frame_index = int(elapsed_time / frame_duration) + 1

        if target_frame_index >= self.TOTAL_FRAMES:
            if self.final_frame is None:
                self.final_frame = self._load_single_frame(self.TOTAL_FRAMES)
            
            self.current_frame_surface = None  # تفريغ الذاكرة
            self.animation_finished = True
            print("[Info] Main menu animation finished.")
            return

        # تحميل الإطار الجديد فقط إذا تغير الزمن
        if target_frame_index != self.current_frame_index:
            self.current_frame_index = target_frame_index
            new_frame = self._load_single_frame(target_frame_index)
            
            # إذا فشل تحميل إطار معين، نتجاهله ولا نوقف اللعبة
            if new_frame:
                self.current_frame_surface = new_frame

    # =========================================================
    # Drawing
    # =========================================================

    def draw(self) -> None:
        
        self._update_animation()

        if self.animation_finished:
            if self.final_frame is not None:
                self.screen.blit(self.final_frame, (0, 0))
            else:
                self.screen.fill((0, 0, 0))
            
            self._draw_buttons()
        else:
            if self.current_frame_surface is not None:
                self.screen.blit(self.current_frame_surface, (0, 0))
            else:
                self.screen.fill((0, 0, 0))

    def _draw_buttons(self) -> None:
        mouse_position = pygame.mouse.get_pos()

        for index, button in enumerate(self.buttons):
            rect: pygame.Rect = button["rect"]
            is_hovered = rect.collidepoint(mouse_position)
            is_selected = index == self.selected_button_index

            button_color = self.BUTTON_HOVER_COLOR if is_hovered or is_selected else self.BUTTON_COLOR
            border_color = self.BUTTON_HOVER_BORDER_COLOR if is_hovered or is_selected else self.BUTTON_BORDER_COLOR

            pygame.draw.rect(self.screen, button_color, rect, border_radius=14)
            pygame.draw.rect(self.screen, border_color, rect, width=3, border_radius=14)

            text_surface = self.button_font.render(button["text"], True, self.TEXT_COLOR)
            text_rect = text_surface.get_rect(center=rect.center)
            self.screen.blit(text_surface, text_rect)

    # =========================================================
    # Input & Navigation (No Changes needed here)
    # =========================================================


    def _select_next_button(self) -> None:
        self.selected_button_index = (self.selected_button_index + 1) % len(self.buttons)

    def _select_previous_button(self) -> None:
        self.selected_button_index = (self.selected_button_index - 1) % len(self.buttons)

    def _activate_selected_button(self) -> str:
        if self.click_sound:
            self.click_sound.play()
            
        return self.buttons[self.selected_button_index]["action"]

    @property
    def is_animation_finished(self) -> bool:
        return self.animation_finished