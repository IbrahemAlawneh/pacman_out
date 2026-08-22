import pygame
from pathlib import Path


class InstructionsScreen:

    """Handles the instructions screen,
    showing gameplay rules and controls."""

    def __init__(self, surface: pygame.Surface):
        self.surface = surface

        bg_path = Path(
            "assets/main_menu_images/setting/background_image.jpg"
        )
        try:
            self.bg = pygame.image.load(str(bg_path)).convert()
            self.bg = pygame.transform.scale(
                self.bg, self.surface.get_size()
            )
        except (FileNotFoundError, pygame.error):
            self.bg = None

        # Clean, readable fonts with no external font-file dependency.
        font_name = pygame.font.match_font("segoeui,dejavusans,arial")
        self.font_title = pygame.font.Font(font_name, 58)
        self.font_text = pygame.font.Font(font_name, 27)
        self.font_key = pygame.font.Font(font_name, 25)
        self.font_footer = pygame.font.Font(font_name, 22)

        # Modern dark UI palette.
        self.TEXT_COLOR = (225, 233, 250)
        self.GOLD_COLOR = (255, 207, 92)
        self.HEADER_COLOR = (116, 224, 255)
        self.NEON_PINK = (224, 116, 255)
        self.NEON_CYAN = (91, 224, 255)
        self.FOOTER_COLOR = (151, 169, 211)
        self.GLASS_BG = (19, 27, 57, 225)

        self.instructions = [
            ("GAME RULES", self.HEADER_COLOR, "", None),
            ("Pac-Gum = 10 pts  |  Super Pac-Gum = 50 pts", self.TEXT_COLOR, "", None),
            ("Eat an edible Ghost to score 200 pts", self.TEXT_COLOR, "", None),
            ("Avoid active Ghosts to save your lives", self.TEXT_COLOR, "", None),
            ("", self.TEXT_COLOR, "", None),
            ("CHEAT MODE  /  SETTINGS", self.NEON_PINK, "", None),
            ("Power: Lives are safe from ghosts", self.TEXT_COLOR, "ARMOR", self.GOLD_COLOR),
            ("Next: Instant win for the level", self.TEXT_COLOR, "SKIP", self.GOLD_COLOR),
            ("Freeze: Ghosts stop moving", self.TEXT_COLOR, "ICE", self.GOLD_COLOR),
            ("Extra: Add extra lives to player", self.TEXT_COLOR, "1UP", self.GOLD_COLOR),
            ("Speed: Pac-Man moves much faster", self.TEXT_COLOR, "DASH", self.GOLD_COLOR),
        ]

    def handle_event(self, event: pygame.event.Event) -> str | None:
        """Handle ESC key to exit."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "back_to_menu"
        return None

    def _draw_modern_key(self, x: int, y: int, letter: str, arrow: str) -> None:
        """Draw a modern glass keyboard key with shadow and accent lighting."""
        rect = pygame.Rect(x, y, 65, 65)
        accent = self.NEON_CYAN if letter in ("W", "A", "S", "D") else self.NEON_PINK

        # Soft shadow creates depth without changing the control layout.
        shadow = pygame.Surface((rect.width + 18, rect.height + 18), pygame.SRCALPHA)
        pygame.draw.rect(
            shadow,
            (0, 0, 0, 105),
            shadow.get_rect(),
            border_radius=16,
        )
        self.surface.blit(shadow, (rect.x - 9, rect.y + 6))

        pygame.draw.rect(self.surface, self.GLASS_BG, rect, border_radius=15)
        pygame.draw.rect(self.surface, (67, 84, 137), rect, width=1, border_radius=15)
        pygame.draw.rect(self.surface, accent, rect, width=2, border_radius=15)

        # Thin highlight at the top gives the key a polished glass appearance.
        pygame.draw.line(
            self.surface,
            (220, 245, 255),
            (rect.x + 15, rect.y + 6),
            (rect.right - 15, rect.y + 6),
            1,
        )

        letter_surf = self.font_key.render(letter, True, self.TEXT_COLOR)
        arrow_surf = self.font_key.render(arrow, True, accent)

        self.surface.blit(
            letter_surf,
            letter_surf.get_rect(center=(rect.centerx, rect.y + 25)),
        )
        self.surface.blit(
            arrow_surf,
            arrow_surf.get_rect(center=(rect.centerx, rect.y + 49)),
        )

    def _draw_keys_panel(self) -> None:
        """Draw the WASD/Arrow keys panel."""
        panel_rect = pygame.Rect(750, 200, 350, 320)

        # Panel shadow.
        shadow = pygame.Surface(
            (panel_rect.width + 24, panel_rect.height + 24), pygame.SRCALPHA
        )
        pygame.draw.rect(
            shadow,
            (0, 0, 0, 100),
            shadow.get_rect(),
            border_radius=23,
        )
        self.surface.blit(shadow, (panel_rect.x - 12, panel_rect.y + 8))

        # Glass panel and subtle border.
        panel_surface = pygame.Surface(
            (panel_rect.width, panel_rect.height), pygame.SRCALPHA
        )
        pygame.draw.rect(
            panel_surface,
            self.GLASS_BG,
            panel_surface.get_rect(),
            border_radius=20,
        )
        self.surface.blit(panel_surface, panel_rect.topleft)
        pygame.draw.rect(
            self.surface,
            (67, 84, 137),
            panel_rect,
            width=1,
            border_radius=20,
        )
        pygame.draw.rect(
            self.surface,
            self.NEON_PINK,
            panel_rect,
            width=2,
            border_radius=20,
        )

        # Panel title and decorative divider.
        ctrl_title = self.font_text.render(
            "MOVEMENT", True, self.NEON_CYAN
        )
        self.surface.blit(
            ctrl_title,
            (
                panel_rect.centerx - ctrl_title.get_width() // 2,
                panel_rect.y + 24,
            ),
        )
        pygame.draw.line(
            self.surface,
            (60, 76, 125),
            (panel_rect.x + 30, panel_rect.y + 72),
            (panel_rect.right - 30, panel_rect.y + 72),
            1,
        )

        # Preserve the original key positions and dimensions.
        cx, cy = panel_rect.centerx, panel_rect.centery + 15
        keys = [
            (cx - 32, cy - 80, "W", "^"),
            (cx - 32, cy - 5, "S", "v"),
            (cx - 107, cy - 5, "A", "<"),
            (cx + 43, cy - 5, "D", ">"),
        ]

        for x, y, letter, arrow in keys:
            self._draw_modern_key(x, y, letter, arrow)

        footer_text = self.font_key.render(
            "USE ARROWS OR LETTERS", True, self.FOOTER_COLOR
        )
        self.surface.blit(
            footer_text,
            (
                panel_rect.centerx - footer_text.get_width() // 2,
                panel_rect.bottom - 40,
            ),
        )

    def draw(self) -> None:
        """Render screen elements."""
        if self.bg:
            self.surface.blit(self.bg, (0, 0))
            # Dark overlay makes text readable on any background image.
            overlay = pygame.Surface(self.surface.get_size(), pygame.SRCALPHA)
            overlay.fill((7, 10, 27, 100))
            self.surface.blit(overlay, (0, 0))
        else:
            self.surface.fill((9, 13, 30))

            # Subtle modern background decorations.
            overlay = pygame.Surface(self.surface.get_size(), pygame.SRCALPHA)
            pygame.draw.circle(overlay, (*self.NEON_PINK, 22), (1130, 80), 250)
            pygame.draw.circle(overlay, (*self.NEON_CYAN, 16), (40, 720), 220)
            self.surface.blit(overlay, (0, 0))

        # Header.
        title_surf = self.font_title.render(
            "HOW TO PLAY", True, self.TEXT_COLOR
        )
        title_x = 80
        self.surface.blit(title_surf, (title_x, 65))

        pygame.draw.line(
            self.surface,
            self.NEON_CYAN,
            (title_x, 143),
            (title_x + 100, 143),
            3,
        )
        pygame.draw.line(
            self.surface,
            self.NEON_PINK,
            (title_x + 112, 143),
            (title_x + 145, 143),
            3,
        )

        start_y = 178
        for main_text, main_color, highlight_text, highlight_color in self.instructions:
            x_offset = 80

            # Section headings receive a larger visual separation.
            is_heading = main_color in (self.HEADER_COLOR, self.NEON_PINK)
            if is_heading:
                start_y += 7

            if highlight_text:
                # Highlight tags are rendered first to preserve the original
                # positioning logic while making the tag look like a badge.
                tag_text = f"[{highlight_text}]"
                high_surf = self.font_text.render(tag_text, True, highlight_color)
                tag_rect = pygame.Rect(x_offset, start_y + 3, high_surf.get_width() + 16, 31)
                pygame.draw.rect(
                    self.surface,
                    (57, 46, 76),
                    tag_rect,
                    border_radius=8,
                )
                pygame.draw.rect(
                    self.surface,
                    highlight_color,
                    tag_rect,
                    width=1,
                    border_radius=8,
                )
                self.surface.blit(
                    high_surf,
                    (tag_rect.x + 8, tag_rect.y - 1),
                )
                x_offset += tag_rect.width + 12

            if main_text:
                text_surf = self.font_text.render(main_text, True, main_color)
                self.surface.blit(text_surf, (x_offset, start_y))

            start_y += 39 if not is_heading else 45

        self._draw_keys_panel()

        esc_surf = self.font_footer.render(
            "[ PRESS ESC TO RETURN ]", True, self.FOOTER_COLOR
        )
        self.surface.blit(
            esc_surf,
            (
                self.surface.get_width() // 2 - esc_surf.get_width() // 2,
                self.surface.get_height() - 50,
            ),
        )
