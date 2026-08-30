import pygame
from typing import Any


class DrawMaze:
    """Handles rendering the maze grid with various visual themes."""
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8

    def __init__(self, screen: pygame.Surface):
        """Initialize the maze drawer with a target screen."""
        self.screen = screen
        self._maze_surface = None
        self._cached_level_id = None
        self.current_theme: str = "classic"

    def _build_maze_surface(
            self, level: Any, cell_size: int
    ) -> pygame.Surface:
        """Build and return a cached surface of the entire maze grid."""
        grid = level.grid
        width_px = len(grid[0]) * cell_size
        height_px = len(grid) * cell_size

        surface = pygame.Surface((width_px, height_px), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 150))
        for row_idx, row in enumerate(grid):
            for col_idx, cell in enumerate(row):
                if cell == 0:
                    continue
                self._draw_cell(surface, cell, row_idx, col_idx, cell_size)
        return surface

    def _draw_cell(
            self, surface: pygame.Surface, cell: int, row_idx:
            int, col_idx: int, cell_size: int
    ) -> None:
        """Draw a single cell according to the current theme style."""
        x = col_idx * cell_size
        y = row_idx * cell_size
        rect = pygame.Rect(x, y, cell_size, cell_size)

        if cell == 15:
            self._draw_special_cell(surface, rect)
            return

        if self.current_theme == "neon":
            self._draw_neon_wall(surface, cell, rect)
        elif self.current_theme == "desert":
            self._draw_desert_wall(surface, cell, rect)
        elif self.current_theme == "classic":
            self._draw_classic_wall(surface, cell, rect)
        else:
            self._draw_default_wall(surface, cell, rect)

    def _draw_special_cell(
            self, surface: pygame.Surface, rect: pygame.Rect
    ) -> None:
        """Render a special decorative golden cell on the surface."""
        outer_color = (218, 165, 32)
        inner_color = (255, 215, 0)
        pygame.draw.rect(
            surface, outer_color, rect.inflate(-2, -2),
            width=3, border_radius=6
        )
        pygame.draw.rect(
            surface, inner_color, rect.inflate(-6, -6), width=1,
            border_radius=4
        )
        pygame.draw.circle(
            surface, (255, 255, 200), rect.center, 1
        )

    def _draw_neon_wall(
            self, surface: pygame.Surface, cell: int,
            rect: pygame.Rect
    ) -> None:
        """Draw a neon-styled wall using layered glowing colors."""
        layers = [
            ((105, 0, 150), 8),
            ((225, 0, 255), 4),
            ((255, 200, 244), 2)
        ]
        for color, thickness in layers:
            if cell & self.NORTH:
                pygame.draw.line(
                    surface, color, rect.topleft, rect.topright, thickness
                )
            if cell & self.EAST:
                pygame.draw.line(
                    surface, color, rect.topright, rect.bottomright,
                    thickness
                )
            if cell & self.SOUTH:
                pygame.draw.line(
                    surface, color, rect.bottomleft, rect.bottomright,
                    thickness
                )
            if cell & self.WEST:
                pygame.draw.line(
                    surface, color, rect.topleft, rect.bottomleft, thickness
                    )

    def _draw_desert_wall(
            self, surface: pygame.Surface, cell: int, rect: pygame.Rect
    ) -> None:
        """Draw a desert-styled wall with dimensional
        shadows and highlights."""
        shadow_color = (139, 69, 19)
        sand_color = (210, 150, 70)
        sun_highlight = (245, 200, 120)

        offset = 2
        thick = 4
        if cell & self.NORTH:
            pygame.draw.line(
                surface, shadow_color, (rect.left, rect.top+offset),
                (rect.right, rect.top+offset), thick
            )
        if cell & self.EAST:
            pygame.draw.line(
                surface, shadow_color, (rect.right-offset, rect.top),
                (rect.right-offset, rect.bottom), thick
            )
        if cell & self.SOUTH:
            pygame.draw.line(
                surface, shadow_color, (rect.left, rect.bottom-offset),
                (rect.right, rect.bottom-offset), thick
            )
        if cell & self.WEST:
            pygame.draw.line(
                surface, shadow_color, (rect.left+offset, rect.top),
                (rect.left+offset, rect.bottom), thick
            )

        core_thick = 3
        if cell & self.NORTH:
            pygame.draw.line(
                surface, sand_color, rect.topleft, rect.topright,
                core_thick
            )
        if cell & self.EAST:
            pygame.draw.line(
                surface, sand_color, rect.topright,
                rect.bottomright, core_thick
            )
        if cell & self.SOUTH:
            pygame.draw.line(
                surface, sand_color, rect.bottomleft,
                rect.bottomright, core_thick
            )
        if cell & self.WEST:
            pygame.draw.line(
                surface, sand_color, rect.topleft,
                rect.bottomleft, core_thick
            )

        corner_size = 5
        if cell & self.NORTH and cell & self.EAST:
            pygame.draw.rect(
                surface, sun_highlight, (
                    rect.right - corner_size//2, rect.top - corner_size//2,
                    corner_size, corner_size
                )
            )
        if cell & self.NORTH and cell & self.WEST:
            pygame.draw.rect(
                surface, sun_highlight, (
                    rect.left - corner_size//2, rect.top - corner_size//2,
                    corner_size, corner_size
                )
            )
        if cell & self.SOUTH and cell & self.EAST:
            pygame.draw.rect(
                surface, sun_highlight, (
                    rect.right - corner_size//2, rect.bottom - corner_size//2,
                    corner_size, corner_size
                )
            )
        if cell & self.SOUTH and cell & self.WEST:
            pygame.draw.rect(
                surface, sun_highlight, (
                    rect.left - corner_size//2, rect.bottom - corner_size//2,
                    corner_size, corner_size
                )
            )

    def _draw_classic_wall(
            self, surface: pygame.Surface, cell: int,
            rect: pygame.Rect
    ) -> None:
        """Draw a classic arcade-styled wall with double inner lines."""
        wall_color = ("#cad318")
        wall_color_2 = ("#78b22b")
        gap = 3
        if cell & self.NORTH:
            pygame.draw.line(
                surface, wall_color, rect.topleft, rect.topright, 2
            )
            pygame.draw.line(
                surface, wall_color_2, (rect.left, rect.top + gap),
                (rect.right, rect.top + gap), 2
            )
        if cell & self.EAST:
            pygame.draw.line(
                surface, wall_color, rect.topright, rect.bottomright, 2
            )
            pygame.draw.line(
                surface, wall_color_2, (rect.right - gap, rect.top),
                (rect.right - gap, rect.bottom), 2
            )
        if cell & self.SOUTH:
            pygame.draw.line(
                surface, wall_color, rect.bottomleft, rect.bottomright, 2
            )
            pygame.draw.line(
                surface, wall_color_2, (rect.left, rect.bottom - gap),
                (rect.right, rect.bottom - gap), 2
            )
        if cell & self.WEST:
            pygame.draw.line(
                surface, wall_color, rect.topleft, rect.bottomleft, 2
            )
            pygame.draw.line(
                surface, wall_color_2, (rect.left + gap, rect.top),
                (rect.left + gap, rect.bottom), 2
            )

    def _draw_default_wall(
            self, surface: pygame.Surface, cell: int,
            rect: pygame.Rect
    ) -> None:
        """Draw a basic flat-colored wall as a fallback theme style."""
        wall_color = (57, 139, 64)
        if cell & self.NORTH:
            pygame.draw.line(
                surface, wall_color, rect.topleft, rect.topright, 2
            )
        if cell & self.EAST:
            pygame.draw.line(
                surface, wall_color, rect.topright, rect.bottomright, 2
            )
        if cell & self.SOUTH:
            pygame.draw.line(
                surface, wall_color, rect.bottomleft, rect.bottomright, 2
            )
        if cell & self.WEST:
            pygame.draw.line(
                surface, wall_color, rect.topleft, rect.bottomleft, 2
            )

    def draw(
            self, level: Any, cell_size: int,
            offset_x: int, offset_y: int,
            theme_name: str
    ) -> None:
        """Render the cached maze onto the screen at the given offsets."""
        if not level.grid:
            return
        if self._cached_level_id != level.level_id:
            self.current_theme = theme_name
            self._maze_surface = self._build_maze_surface(
                level, cell_size
            )
            self._cached_level_id = level.level_id
        self.screen.blit(self._maze_surface, (offset_x, offset_y))
