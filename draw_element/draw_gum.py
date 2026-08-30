import pygame
from typing import Any


class DrawGum:
    """Draws normal and super pac-gums onto the screen."""

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.normal_color = (255, 223, 150)
        self.super_color = (255, 175, 50)

    def draw(
        self, gums: list[Any], cell_size: int,
        offset_x: int, offset_y: int
    ) -> None:
        """Draw every non-eaten gum as a normal or super pellet."""
        normal_radius = max(2, cell_size // 8)
        super_radius = max(4, cell_size // 4)
        for gum in gums:
            if gum.is_eaten:
                continue

            center_x = (
                gum.grid_x * cell_size
            ) + offset_x + (cell_size // 2)
            center_y = (
                gum.grid_y * cell_size
            ) + offset_y + (cell_size // 2)

            if gum.is_super:
                pygame.draw.circle(
                    self.screen, self.super_color,
                    (center_x, center_y), super_radius
                )
            else:
                pygame.draw.circle(
                    self.screen, self.normal_color,
                    (center_x, center_y), normal_radius
                )
