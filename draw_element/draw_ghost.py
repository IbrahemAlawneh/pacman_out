import pygame
import os
from typing import Any


class DrawGhost:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.base_path = os.path.join("assets", "images", "charater")

        self.ghost_colors = ["blue", "orange", "green", "purple"]
        self.directions = ["up", "down", "left", "right"]

        self.raw_images = {}
        for color in self.ghost_colors:
            self.raw_images[color] = {}
            for direction in self.directions:
                filename = f"{color}_{direction}.png"
                self.raw_images[color][
                    direction.upper()
                ] = self._load_image(filename)
        self.raw_scared = self._load_image("scared.png")
        self.scaled_images = {}
        self.scaled_scared = None
        self.current_cell_size = 0

    def _load_image(self, filename: str) -> pygame.Surface:
        full_path = os.path.join(self.base_path, filename)
        try:
            return pygame.image.load(full_path).convert_alpha()
        except FileNotFoundError:
            print(f"[Warning] Missing ghost image: {full_path}")
            fallback = pygame.Surface((30, 30), pygame.SRCALPHA)
            fallback.fill((255, 0, 0, 150))
            return fallback

    def _scale_images(self, cell_size: int) -> None:
        size = int(cell_size * 0.8)
        self.scaled_images = {}
        for color in self.ghost_colors:
            self.scaled_images[color] = {}
            for direction, img in self.raw_images[color].items():
                self.scaled_images[color][
                    direction
                ] = pygame.transform.scale(img, (size, size))

        self.scaled_scared = pygame.transform.scale(
            self.raw_scared, (size, size)
        )
        self.current_cell_size = cell_size

    def draw(
            self, ghosts: list[Any], cell_size: int,
            offset_x: int, offset_y: int
    ) -> None:

        if self.current_cell_size != cell_size:
            self._scale_images(cell_size)

        for ghost in ghosts:
            if getattr(ghost, 'is_eaten', False):
                continue
            if getattr(ghost, 'is_scared', False):
                current_image = self.scaled_scared
            else:
                ghost_name = getattr(ghost, 'color', 'blue').lower()
                direction = getattr(ghost, 'direction', 'RIGHT').upper()
                if ghost_name not in self.scaled_images:
                    ghost_name = "blue"
                if direction not in self.scaled_images[ghost_name]:
                    direction = "RIGHT"
                current_image = self.scaled_images[ghost_name][direction]

            img_width = current_image.get_width()
            img_height = current_image.get_height()

            center_x = ghost.x + offset_x + (cell_size // 2)
            center_y = ghost.y + offset_y + (cell_size // 2)

            draw_x = center_x - (img_width // 2)
            draw_y = center_y - (img_height // 2)
            self.screen.blit(current_image, (draw_x, draw_y))
