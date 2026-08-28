from pathlib import Path
import pygame


class InstructionsScreen:
    """Draw the instructions screen and handle the return key."""

    def __init__(self, surface: pygame.Surface, config: dict) -> None:
        self.surface = surface
        self.config = config
        self._init_assets()

        p_pacgum = max(
            10, min(self.config.get("points_per_pacgum", 10), 100)
        )
        p_super = max(
            50, min(self.config.get("points_per_super_pacgum", 50), 200)
        )
        p_ghost = max(
            200, min(self.config.get("points_per_ghost", 200), 200)
        )

        self.instructions = [
            ("GAME RULES", self.HEADER_COLOR, None),
            (
                f"Pac-Gum = {p_pacgum} pts  |  Super Pac-Gum = {p_super} pts",
                self.TEXT_COLOR, None
            ),
            (
                f"Eat a frightened Ghost to score {p_ghost} pts",
                self.TEXT_COLOR, None
            ),
            (
                "Avoid active Ghosts to protect your lives",
                self.TEXT_COLOR, None
            ),
            (
                "CHEAT MODE (Enable in Settings first)",
                self.NEON_PINK, None
            ),
            ("Skip the current level", self.TEXT_COLOR, "F1"),
            ("Stop all Ghosts from moving", self.TEXT_COLOR, "F2"),
            ("Give Pac-Man one extra life", self.TEXT_COLOR, "F3"),
            ("Move Pac-Man faster", self.TEXT_COLOR, "F4"),
            ("Protect Pac-Man from Ghosts", self.TEXT_COLOR, "F5"),
        ]

    def _init_assets(self) -> None:
        """Load the optional background, fonts, and interface colors."""
        try:
            image = pygame.image.load(
                str(
                    Path(
                        "assets/images/setting/without_logo_bk.jpg")
                    )
                ).convert()
            self.bg = pygame.transform.scale(
                image, self.surface.get_size()
            )
        except (FileNotFoundError, pygame.error):
            self.bg = None

        font = pygame.font.match_font("segoeui,dejavusans,arial")
        self.font_title = pygame.font.Font(font, 58)
        self.font_text = pygame.font.Font(font, 27)
        self.font_key = pygame.font.Font(font, 25)
        self.font_footer = pygame.font.Font(font, 22)

        self.TEXT_COLOR = (240, 245, 255)
        self.GOLD_COLOR = (255, 220, 40)
        self.HEADER_COLOR = (0, 255, 255)
        self.FOOTER_COLOR = (120, 140, 180)
        self.NEON_PINK = (255, 60, 170)
        self.NEON_CYAN = (0, 255, 255)
        self.GLASS_BG = (15, 20, 45, 200)

    def handle_event(self, event: pygame.event.Event) -> str | None:
        """Return to the menu when Escape is pressed."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "back_to_menu"
        return None

    def _draw_glass_panel(
        self, rect: pygame.Rect, color: tuple[int, int, int],
        radius: int = 16
    ) -> None:
        """Draw a compact panel with a shadow and neon border."""

        shadow = pygame.Surface(
            (rect.width + 18, rect.height + 18), pygame.SRCALPHA
        )
        pygame.draw.rect(
            shadow, (0, 0, 0, 100), shadow.get_rect(),
            border_radius=radius
        )
        self.surface.blit(shadow, (rect.x - 9, rect.y + 6))
        pygame.draw.rect(
            self.surface, self.GLASS_BG, rect, border_radius=radius
        )
        pygame.draw.rect(
            self.surface, color, rect, width=2, border_radius=radius
        )

    def _draw_modern_key(
            self, x: int, y: int,
            letter: str, arrow: str
    ) -> None:
        """Draw one movement key."""

        rect = pygame.Rect(x, y, 65, 65)
        self._draw_glass_panel(rect, self.NEON_CYAN, 14)
        self.surface.blit(
            self.font_key.render(letter, True, self.TEXT_COLOR),
            (rect.centerx - 8, rect.y + 10),
        )
        self.surface.blit(
            self.font_key.render(arrow, True, self.NEON_CYAN),
            (rect.centerx - 7, rect.y + 36),
        )

    def _draw_keys_panel(self) -> None:
        """Draw the movement panel on the right."""

        panel = pygame.Rect(750, 200, 350, 320)
        self._draw_glass_panel(panel, self.NEON_PINK, 20)
        title = self.font_text.render("MOVEMENT", True, self.NEON_CYAN)
        self.surface.blit(
            title, title.get_rect(
                center=(panel.centerx, panel.y + 42)
            )
        )
        pygame.draw.line(
            self.surface, (60, 76, 125),
            (panel.x + 30, panel.y + 72),
            (panel.right - 30, panel.y + 72),
        )

        cx, cy = panel.centerx, panel.centery + 15
        keys = (
            (cx - 32, cy - 80, "W", "^"),
            (cx - 107, cy - 5, "A", "<"),
            (cx - 32, cy - 5, "S", "v"),
            (cx + 43, cy - 5, "D", ">")
        )
        for key in keys:
            self._draw_modern_key(*key)

        footer = self.font_key.render(
            "USE ARROWS OR WASD", True, self.FOOTER_COLOR
        )
        self.surface.blit(
            footer, footer.get_rect(
                center=(panel.centerx, panel.bottom - 32)
            )
        )

    def _draw_instruction(
            self, text: str,
            color: tuple[int, int, int], key: str | None, y: int
    ) -> None:
        """Draw one rule or one cheat command."""
        x = 80
        if key:
            tag = self.font_text.render(key, True, self.GOLD_COLOR)
            box = pygame.Rect(x, y - 2, tag.get_width() + 24, 36)
            shadow_rect = box.copy()
            shadow_rect.y += 3
            pygame.draw.rect(
                self.surface, (0, 0, 0, 150), shadow_rect, border_radius=8
            )
            tag_bg = (40, 35, 10)
            pygame.draw.rect(self.surface, tag_bg, box, border_radius=8)
            pygame.draw.rect(
                self.surface, self.GOLD_COLOR, box, width=2, border_radius=8
            )
            self.surface.blit(tag, (box.x + 12, box.y + 2))
            x = box.right + 16

        self.surface.blit(
            self.font_text.render(text, True, color), (x, y + 2)
        )

    def draw(self) -> None:
        """Render the complete screen."""
        if self.bg:
            self.surface.blit(self.bg, (0, 0))
            overlay = pygame.Surface(
                self.surface.get_size(), pygame.SRCALPHA
            )
            overlay.fill((7, 10, 27, 125))
            self.surface.blit(overlay, (0, 0))
        else:
            self.surface.fill((9, 13, 30))

        title = self.font_title.render(
            "HOW TO PLAY", True, self.TEXT_COLOR
        )
        self.surface.blit(title, (80, 110))
        pygame.draw.line(
            self.surface, self.NEON_CYAN, (80, 200), (190, 200), 3
        )
        pygame.draw.line(
            self.surface, self.NEON_PINK, (205, 200), (240, 200), 3
        )

        y = 250
        for text, color, key in self.instructions:
            if key is None and color in (
                self.HEADER_COLOR, self.NEON_PINK
            ):
                y += 8
            self._draw_instruction(text, color, key, y)
            y += 45 if key is None and color in (
                self.HEADER_COLOR, self.NEON_PINK
            ) else 39

        self._draw_keys_panel()
        footer = self.font_footer.render(
            "[ PRESS ESC TO RETURN ]", True, self.FOOTER_COLOR
        )
        self.surface.blit(
            footer, footer.get_rect(
                center=(
                    self.surface.get_width() // 2,
                    self.surface.get_height() - 50
                )
            )
        )
