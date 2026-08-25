import pygame

class DrawPacman:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.color = (255, 255, 0) 

    def draw(self, pacman_entity, cell_size: int, offset_x: int, offset_y: int) -> None:
        
        radius = int((cell_size * 0.7) / 2)

        center_x = pacman_entity.x + offset_x + (cell_size // 2)
        center_y = pacman_entity.y + offset_y + (cell_size // 2)

        pygame.draw.circle(
            self.screen,
            self.color,
            (int(center_x), int(center_y)),
            radius
        )