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

        self.font_title = pygame.font.Font(None, 60)
        self.font_text = pygame.font.Font(None, 36)
        self.font_footer = pygame.font.Font(None, 40)

        self.TEXT_COLOR = (255, 255, 255)
        self.HEADER_COLOR = (246, 135, 20)
        self.NEON_PINK = (255, 60, 170)
        self.FOOTER_COLOR = (0, 255, 220)
        self.BOX_BG = (28, 18, 48, 180)

        self.instructions = [
            "1. Eat all Pac-Gums to complete the level.",
            "2. Avoid Ghosts, or you lose a life.",
            "3. Eat Super Pac-Gums to make Ghosts edible.",
            "4. Ghosts in Hard Mode will chase you!",
            "5. Survive, get the highest score, and win."
        ]

    def handle_event(self, event: pygame.event.Event) -> str | None:
        """Handle ESC key to exit."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "back_to_menu"
        return None

    def _draw_arrow(self, x: int, y: int, direction: str) -> None:
        """Draw a directional arrow."""
        color = self.TEXT_COLOR
        width = 3

        if direction == "UP":
            pygame.draw.line(
                self.surface, color, (x, y + 10), (x, y - 10), width
            )      # الخط العمودي
            pygame.draw.line(
                self.surface, color, (x, y - 10), (x - 8, y - 2), width
            )   # رأس السهم الأيسر
            pygame.draw.line(
                self.surface, color, (x, y - 10), (x + 8, y - 2), width
            )   # رأس السهم الأيمن

        elif direction == "DOWN":
            pygame.draw.line(
                self.surface, color, (x, y - 10), (x, y + 10), width
            )
            pygame.draw.line(
                self.surface, color, (x, y + 10), (x - 8, y + 2), width
            )
            pygame.draw.line(
                self.surface, color, (x, y + 10), (x + 8, y + 2), width
            )

        elif direction == "LEFT":
            pygame.draw.line(
                self.surface, color, (x + 10, y), (x - 10, y), width
            )
            pygame.draw.line(
                self.surface, color, (x - 10, y), (x - 2, y - 8), width
            )
            pygame.draw.line(
                self.surface, color, (x - 10, y), (x - 2, y + 8), width
            )

        elif direction == "RIGHT":
            pygame.draw.line(
                self.surface, color, (x - 10, y), (x + 10, y), width
            )
            pygame.draw.line(
                self.surface, color, (x + 10, y), (x + 2, y - 8), width
            )
            pygame.draw.line(
                self.surface, color, (x + 10, y), (x + 2, y + 8), width
            )

    def _draw_keys_panel(self) -> None:
        """Draw the WASD/Arrow keys panel."""

        # 1. Draw the transparent panel frame
        panel_rect = pygame.Rect(750, 200, 350, 300)
        panel_surface = pygame.Surface(
            (panel_rect.width, panel_rect.height), pygame.SRCALPHA
        )
        pygame.draw.rect(
            panel_surface, self.BOX_BG, panel_surface.get_rect(),
            border_radius=15
        )
        self.surface.blit(panel_surface, panel_rect.topleft)
        pygame.draw.rect(
            self.surface, self.NEON_PINK, panel_rect, width=3,
            border_radius=15
        )

        # 2. Panel title
        ctrl_title = self.font_text.render(
            "MOVEMENT", True, self.HEADER_COLOR
        )
        self.surface.blit(
            ctrl_title,
            (
                panel_rect.centerx - ctrl_title.get_width() // 2,
                panel_rect.y + 20)
            )

        # 3. Define the positions of the four keys (Center X, Center Y)
        cx, cy = panel_rect.centerx, panel_rect.centery + 15
        keys = [
            (cx - 30, cy - 80, "UP"),
            (cx - 30, cy - 10, "DOWN"),
            (cx - 100, cy - 10, "LEFT"),
            (cx + 40, cy - 10, "RIGHT")
        ]

        # 4. Draw the key boxes and arrows inside them
        for x, y, direction in keys:
            key_rect = pygame.Rect(x, y, 60, 60)
            # key background
            pygame.draw.rect(
                self.surface, (50, 40, 70), key_rect, border_radius=8
            )
            # key border
            pygame.draw.rect(
                self.surface, self.TEXT_COLOR, key_rect, width=2,
                border_radius=8
            )
            # Draw the arrow in the center of the key
            self._draw_arrow(x + 30, y + 30, direction)

        wasd_text = self.font_text.render(
            "OR USE W A S D", True, (200, 200, 220)
        )
        self.surface.blit(
            wasd_text, (panel_rect.centerx - wasd_text.get_width() // 2,
                        panel_rect.bottom - 45)
                    )

    def draw(self) -> None:
        """Render the background, title, rules, and controls panel."""

        if self.bg:
            self.surface.blit(self.bg, (0, 0))
        else:
            self.surface.fill((20, 10, 40))

        title_surf = self.font_title.render(
            "HOW TO PLAY", True, self.HEADER_COLOR
        )
        self.surface.blit(title_surf, (80, 80))

        start_y = 200
        for line in self.instructions:
            text_surf = self.font_text.render(line, True, self.TEXT_COLOR)
            self.surface.blit(text_surf, (80, start_y))
            start_y += 60

        self._draw_keys_panel()

        esc_surf = self.font_footer.render(
            "[ PRESS ESC TO RETURN ]", True, self.FOOTER_COLOR
        )
        self.surface.blit(
            esc_surf,
            (
                self.surface.get_width() // 2 - esc_surf.get_width() // 2, 700
            ))
