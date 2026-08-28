import pygame
import os

class DrawPacman:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen

        img_path = os.path.join("assets", "images", "charater")
        self.img_close = pygame.image.load(os.path.join(img_path, "close.png")).convert_alpha()
        self.img_open = pygame.image.load(os.path.join(img_path, "open.png")).convert_alpha()

        self.last_cell_size = 0
        self.scaled_close = self.img_close
        self.scaled_open = self.img_open

    def draw(self, pacman_entity, cell_size: int, offset_x: int, offset_y: int) -> None:
        if self.last_cell_size != cell_size and cell_size > 0:
            size = int(cell_size * 0.8)
            self.scaled_close = pygame.transform.scale(self.img_close, (size, size))
            self.scaled_open = pygame.transform.scale(self.img_open, (size, size))
            self.last_cell_size = cell_size

        time_now = pygame.time.get_ticks()
        if (time_now // 150) % 2 == 0:
            current_img = self.scaled_open
        else:
            current_img = self.scaled_close


        direction = getattr(pacman_entity, 'direction', 'RIGHT')
        angle = 0
        if direction == "UP": angle = 90
        elif direction == "LEFT": angle = 180
        elif direction == "DOWN": angle = 270

        if angle != 0:
            current_img = pygame.transform.rotate(current_img, angle)

        center_x = pacman_entity.x + offset_x + (cell_size // 2)
        center_y = pacman_entity.y + offset_y + (cell_size // 2)

        img_rect = current_img.get_rect(center=(int(center_x), int(center_y)))
        self.screen.blit(current_img, img_rect)
