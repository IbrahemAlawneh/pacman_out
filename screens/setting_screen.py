import pygame
from pathlib import Path


class SettingScreen:
    def __init__(self, screen: pygame.Surface, config: dict) -> None:
        self.screen = screen
        self.config = config
        """check if there is this keys and if not
        add it with default values"""
        self.config.setdefault("width", 15)
        self.config.setdefault("height", 15)
        self.config.setdefault("pacman_speed", 50)
        self.config.setdefault("ghost_speed", 50)
        """this dict for cheat mode setting"""
        if "cheats" not in self.config:
            self.config["cheats"] = {
                "enable_all": False,
                "level_skip": False,
                "ghost_freeze": False,
                "extra_life": False,
                "speed_boost": False,
                "infinite_lives": False
            }

        self.music_volume = 0.5
        self.sfx_volume = 0.8
        self.music_tracks = [
            "assets/sounds/background_music.ogg",
            "assets/sounds/background_music2.ogg",
            "assets/sounds/background_music3.ogg"
        ]

        """here the images path so later if we need
        to change or customieze another theme or animations"""
        self.assets_path = Path("assets/images/setting")
        self.bg_image = self._load_image(
            "without_logo_bk.jpg", scale_to_screen=True
        )
        self.logo = self._load_image("logo.png")
        self.arrow_up = self._load_image("arrow_up.png")
        self.arrow_down = self._load_image("arrow_down.png")
        self.toggle_on = self._load_image("toggle_on.png")
        self.toggle_off = self._load_image("toggle_off.png")
        self.speaker_icon = self._load_image("speaker_icon.png")
        self.music_btn = self._load_image("music_play_btn.png")

        self.font_title = pygame.font.Font(None, 60)
        self.font_label = pygame.font.Font(None, 28)
        self.font_value = pygame.font.Font(None, 32)

        self.COLOR_PANEL = (88, 38, 175)
        self.COLOR_TEXT = (255, 255, 255)
        self.COLOR_ACCENT = (246, 135, 20)
        self.COLOR_SLIDER_BG = (200, 200, 200)
        self._setup_hitboxes()

    def _load_image(
            self, filename: str, scale_to_screen: bool = False
    ) -> pygame.Surface | None:
        filepath = self.assets_path / filename
        try:
            img = pygame.image.load(str(filepath)).convert_alpha()
            if scale_to_screen:
                img = pygame.transform.scale(img, self.screen.get_size())
            return img
        except Exception as e:
            print(f"[Warning] Could not load {filename}: {e}")
            return None

    def _setup_hitboxes(self) -> None:
        """"here is the postions of sounds buttons and config setting"""
        self.music_buttons = [
            pygame.Rect(200, 460, 50, 50),
            pygame.Rect(270, 460, 50, 50),
            pygame.Rect(340, 460, 50, 50)
        ]
        self.slider_music_rect = pygame.Rect(180, 280, 250, 10)
        self.slider_sfx_rect = pygame.Rect(180, 380, 250, 10)
        self.is_dragging_music = False
        self.is_dragging_sfx = False
        self.num_buttons = {
            "ghost_speed": (
                pygame.Rect(240, 590, 25, 20),
                pygame.Rect(240, 610, 25, 20)
            ),
            "pacman_speed": (
                pygame.Rect(410, 590, 25, 20),
                pygame.Rect(410, 610, 25, 20)
            ),
            "width": (
                pygame.Rect(240, 690, 25, 20),
                pygame.Rect(240, 710, 25, 20)
            ),
            "height": (
                pygame.Rect(410, 690, 25, 20),
                pygame.Rect(410, 710, 25, 20)
            )
        }
        self.cheat_keys = [
            "enable_all", "level_skip", "ghost_freeze",
            "extra_life", "speed_boost", "infinite_lives"
        ]
        self.cheat_toggles = {}
        start_y = 300
        for key in self.cheat_keys:
            self.cheat_toggles[key] = pygame.Rect(650, start_y, 80, 40)
            start_y += 70

    def handle_event(self, event: pygame.event.Event) -> str | None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "back_to_menu"
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            for i, rect in enumerate(self.music_buttons):
                if rect.collidepoint(pos):
                    self._play_music(i)
            if self.slider_music_rect.inflate(20, 30).collidepoint(pos):
                self.is_dragging_music = True
            elif self.slider_sfx_rect.inflate(20, 30).collidepoint(pos):
                self.is_dragging_sfx = True
            self._handle_number_clicks(pos)
            self._handle_cheat_clicks(pos)

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.is_dragging_music = False
            self.is_dragging_sfx = False

        elif event.type == pygame.MOUSEMOTION:
            if self.is_dragging_music:
                self._update_slider("music", event.pos[0])
            elif self.is_dragging_sfx:
                self._update_slider("sfx", event.pos[0])
        return None

    def _play_music(self, index: int) -> None:
        """Play a music track based on the pressed button"""
        try:
            pygame.mixer.music.load(self.music_tracks[index])
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(-1)
        except Exception as e:
            print(f"[Error] Could not play music track {index}: {e}")

    def _update_slider(self, slider_type: str, mouse_x: int) -> None:
        """Convert mouse position to a volume percentage"""
        rect = (
            self.slider_music_rect
            if slider_type == "music"
            else self.slider_sfx_rect
        )
        clamped_x = max(rect.left, min(mouse_x, rect.right))
        ratio = (clamped_x - rect.left) / rect.width

        if slider_type == "music":
            self.music_volume = ratio
            pygame.mixer.music.set_volume(self.music_volume)
        else:
            self.sfx_volume = ratio

    def _handle_number_clicks(self, pos: tuple) -> None:
        """Handles arrow-key presses to change the numbers
        within the specified constraints"""
        limits = {
            "ghost_speed": (40, 100),
            "pacman_speed": (40, 100),
            "width": (9, 18),
            "height": (8, 15)
        }

        for key, (rect_up, rect_down) in self.num_buttons.items():
            if rect_up.collidepoint(pos):
                self.config[key] = min(limits[key][1], self.config[key] + 1)
            elif rect_down.collidepoint(pos):
                self.config[key] = max(limits[key][0], self.config[key] - 1)

    def _handle_cheat_clicks(self, pos: tuple) -> None:
        """Handles toggling the Cheat buttons
        based on the Master Switch logic"""
        cheats = self.config["cheats"]

        for key, rect in self.cheat_toggles.items():
            if rect.collidepoint(pos):
                if key == "enable_all":
                    cheats["enable_all"] = not cheats["enable_all"]
                    if cheats["enable_all"]:
                        for k in cheats.keys():
                            cheats[k] = True
                else:
                    if not cheats["enable_all"]:
                        cheats[key] = not cheats[key]

    def draw(self) -> None:
        if self.bg_image:
            self.screen.blit(self.bg_image, (0, 0))
        else:
            self.screen.fill((15, 10, 30))

        panel_rect = pygame.Rect(60, 60, 480, 700)
        pygame.draw.rect(
            self.screen, self.COLOR_PANEL, panel_rect, border_radius=20
        )
        pygame.draw.rect(
            self.screen, self.COLOR_ACCENT, panel_rect,
            width=3, border_radius=20
        )
        if self.logo:
            scaled_logo = pygame.transform.smoothscale(
                self.logo, (250, 250)
            )
            self.screen.blit(scaled_logo, (170, 30))
        self._draw_audio_section()
        self._draw_music_buttons()
        self._draw_number_inputs()
        self._draw_cheat_section()

    def _draw_audio_section(self) -> None:
        lbl_music = self.font_label.render(
            "BACKGROUND MUSIC", True, self.COLOR_TEXT
        )
        lbl_sfx = self.font_label.render(
            "SOUND EFFECT", True, self.COLOR_TEXT
        )
        self.screen.blit(lbl_music, (180, 240))
        self.screen.blit(lbl_sfx, (180, 340))
        if self.speaker_icon:
            scaled_speaker = pygame.transform.smoothscale(
                self.speaker_icon, (30, 30)
            )
            self.screen.blit(scaled_speaker, (130, 235))
            self.screen.blit(scaled_speaker, (130, 335))

        pygame.draw.rect(
            self.screen, self.COLOR_SLIDER_BG,
            self.slider_music_rect, border_radius=5
        )
        fill_width = int(
            self.music_volume * self.slider_music_rect.width
        )
        pygame.draw.rect(
            self.screen, self.COLOR_ACCENT,
            (
                self.slider_music_rect.x, self.slider_music_rect.y,
                fill_width, 10), border_radius=5
        )
        pygame.draw.circle(
            self.screen, (255, 220, 180),
            (
                self.slider_music_rect.x + fill_width,
                self.slider_music_rect.centery
            ), 10
        )
        pygame.draw.rect(
            self.screen, self.COLOR_SLIDER_BG,
            self.slider_sfx_rect, border_radius=5
        )
        fill_width_sfx = int(
            self.sfx_volume * self.slider_sfx_rect.width
        )
        pygame.draw.rect(
            self.screen, self.COLOR_ACCENT,
            (
                self.slider_sfx_rect.x, self.slider_sfx_rect.y,
                fill_width_sfx, 10
            ), border_radius=5
        )
        pygame.draw.circle(
            self.screen, (255, 220, 180),
            (
                self.slider_sfx_rect.x + fill_width_sfx,
                self.slider_sfx_rect.centery
            ), 10
        )

    def _draw_music_buttons(self) -> None:
        title = self.font_value.render("CHANGE MUSIC", True, self.COLOR_TEXT)
        self.screen.blit(title, (205, 430))
        if self.music_btn:
            scaled_btn = pygame.transform.smoothscale(self.music_btn, (50, 50))
            for rect in self.music_buttons:
                self.screen.blit(scaled_btn, rect.topleft)

    def _draw_number_inputs(self) -> None:

        settings = [
            ("GHOSTS SPEED", "ghost_speed", 140, 560),
            ("PACMAN SPEED", "pacman_speed", 310, 560),
            ("MAZE WIDTH", "width", 140, 660),
            ("MAZE HEIGHT", "height", 310, 660)
        ]
        for label_text, key, x, y in settings:

            lbl = (
                pygame.font.Font(None, 22).render(
                    label_text, True, self.COLOR_TEXT
                )
            )
            self.screen.blit(lbl, (x, y + 10))
            box_rect = pygame.Rect(x, y + 30, 130, 40)
            pygame.draw.rect(
                self.screen, (255, 255, 255),
                box_rect, border_radius=5
            )
            if key in ("ghost_speed", "pacman_speed"):
                val_text = self.font_value.render(
                    str(max(40, min(self.config[key], 100))), True, (0, 0, 0)
                    )
            else:
                val_text = self.font_value.render(
                    str(max(5, min(self.config[key], 20))), True, (0, 0, 0)
                    )

            self.screen.blit(val_text, (x + 10, y + 38))

            if self.arrow_up and self.arrow_down:
                scaled_up = pygame.transform.smoothscale(
                    self.arrow_up, (20, 15)
                )
                scaled_down = pygame.transform.smoothscale(
                    self.arrow_down, (20, 15)
                )
                self.screen.blit(scaled_up, (x + 100, y + 32))
                self.screen.blit(scaled_down, (x + 100, y + 52))

    def _draw_cheat_section(self) -> None:
        title = self.font_title.render(
            "CHEAT MODE", True, self.COLOR_ACCENT
        )
        self.screen.blit(title, (720, 150))
        subtitle = self.font_label.render(
            "CHEAT CONTROLS CAN BE FOUND IN THE INSTRUCTIONS",
            True, (200, 200, 200)
        )
        self.screen.blit(subtitle, (600, 210))
        cheats = self.config["cheats"]
        for key, rect in self.cheat_toggles.items():
            is_on = cheats[key]
            text_color = self.COLOR_TEXT
            if not is_on and cheats["enable_all"] and key != "enable_all":
                text_color = (100, 100, 100)
            label_text = key.replace("_", " ").upper()
            lbl = self.font_value.render(label_text, True, text_color)
            if is_on and self.toggle_on:
                scaled_toggle = pygame.transform.smoothscale(
                    self.toggle_on, (80, 40)
                )
                self.screen.blit(scaled_toggle, rect.topleft)
            elif not is_on and self.toggle_off:
                scaled_toggle = pygame.transform.smoothscale(
                    self.toggle_off, (80, 40)
                )
                self.screen.blit(scaled_toggle, rect.topleft)
            else:
                pygame.draw.rect(
                    self.screen, self.COLOR_ACCENT if is_on else (
                        100, 100, 100), rect, border_radius=20
                    )
            self.screen.blit(lbl, (rect.right + 20, rect.y + 10))
