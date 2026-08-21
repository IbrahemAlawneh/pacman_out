import pygame
from entities import Level

class GameScreen:
    """Handles rendering the gameplay grid and entities."""

    def __init__(self, screen: pygame.Surface, cell_size: int = 24):
        self.screen = screen
        self.cell_size = cell_size
        self.wall_color = (0, 255, 220)

    def draw_grid(self, level: Level) -> None:
        """Draw the maze grid and highlight the '42' pattern."""
        grid = level.grid
        if not grid:
            return

        offset_x = (
            self.screen.get_width() - (len(grid[0]) * self.cell_size)
        ) // 2
        offset_y = (
            self.screen.get_height() - (len(grid) * self.cell_size)
        ) // 2

        self.screen.fill((0, 0, 0))

        for row_idx, row in enumerate(grid):
            for col_idx, cell in enumerate(row):
                if cell == 0:
                    continue

                x = offset_x + col_idx * self.cell_size
                y = offset_y + row_idx * self.cell_size
                rect = pygame.Rect(x, y, self.cell_size, self.cell_size)

                # 15 represents the cells forming the '42' pattern
                if cell == 15:
                    pygame.draw.rect(self.screen, (255, 60, 170), rect, border_radius=4)
                else:
                    # Draw standard maze walls using bitwise logic

                    glow_color = (0, 100, 150)

                    for color, thickness in [(glow_color, 8), (self.wall_color, 2)]:
                        if cell & 1:  # North (Top)
                            pygame.draw.line(self.screen, color, rect.topleft, rect.topright, thickness)
                        if cell & 2:  # East (Right)
                            pygame.draw.line(self.screen, color, rect.topright, rect.bottomright, thickness)
                        if cell & 4:  # South (Bottom)
                            pygame.draw.line(self.screen, color, rect.bottomleft, rect.bottomright, thickness)
                        if cell & 8:  # West (Left)
                            pygame.draw.line(self.screen, color, rect.topleft, rect.bottomleft, thickness)
