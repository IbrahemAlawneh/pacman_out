import pygame
from typing import Any

class DrawGhost:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen

        self.scared_color = (0, 0, 255)
        self.eaten_color = (255, 255, 255)

    def draw(self, ghosts: list[Any], cell_size: int, offset_x: int, offset_y: int) -> None:

        for ghost in ghosts:

            radius = int((cell_size * 0.8) / 2)
            

            center_x = ghost.x + offset_x + (cell_size // 2)
            center_y = ghost.y + offset_y + (cell_size // 2)


            if ghost.is_scared:
                color = self.scared_color
            else:
                color = ghost.color

            if not ghost.is_eaten:
                rect_width = radius * 2
                rect_height = radius * 2
                ghost_rect = pygame.Rect(
                    center_x - radius, 
                    center_y - radius, 
                    rect_width, 
                    rect_height
                )
                # ميزة رائعة في Pygame: تدوير الزوايا العلوية فقط!
                pygame.draw.rect(
                    self.screen, 
                    color, 
                    ghost_rect, 
                    border_top_left_radius=radius, 
                    border_top_right_radius=radius
                )

            eye_radius = max(2, radius // 3)
            pupil_radius = max(1, eye_radius // 2)
            
            left_eye_pos = (int(center_x - radius // 2), int(center_y - radius // 4))
            right_eye_pos = (int(center_x + radius // 2), int(center_y - radius // 4))
            
            pygame.draw.circle(self.screen, (255, 255, 255), left_eye_pos, eye_radius)
            pygame.draw.circle(self.screen, (255, 255, 255), right_eye_pos, eye_radius)
            
            pupil_offset_x = 0
            pupil_offset_y = 0
            if ghost.direction == "RIGHT": pupil_offset_x = 2
            elif ghost.direction == "LEFT": pupil_offset_x = -2
            elif ghost.direction == "UP": pupil_offset_y = -2
            elif ghost.direction == "DOWN": pupil_offset_y = 2
            
            pygame.draw.circle(self.screen, (0, 0, 0), (left_eye_pos[0] + pupil_offset_x, left_eye_pos[1] + pupil_offset_y), pupil_radius)
            pygame.draw.circle(self.screen, (0, 0, 0), (right_eye_pos[0] + pupil_offset_x, right_eye_pos[1] + pupil_offset_y), pupil_radius)