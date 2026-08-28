import pygame

class DrawHUD:
    def __init__(self, font_path: str):
        self.font = pygame.font.Font(font_path, 28)
        self.font_sec = pygame.font.Font(font_path, 18)

        
        self.text_color = (255, 255, 255)

        self.time_pos = (90, 35)
        self.lives_pos = (90, 90)
        
        self.score_center = (200, 175)
        self.level_center = (190, 253)

    def draw(self, screen: pygame.Surface, score: int, level: int, lives: int, time_left: int) -> None:
        
        time_surface = self.font.render(f"{time_left}", False, self.text_color)
        lives_surface = self.font.render(f"x{lives}", False, self.text_color)
        score_surface = self.font_sec.render(f"{score} PTS", False, self.text_color)
        level_surface = self.font_sec.render(f"{level:02d} LEVEL", False, self.text_color)

        score_rect = score_surface.get_rect(center=self.score_center)
        level_rect = level_surface.get_rect(center=self.level_center)

        screen.blit(time_surface, self.time_pos)
        screen.blit(lives_surface, self.lives_pos)
        screen.blit(score_surface, score_rect)
        screen.blit(level_surface, level_rect)