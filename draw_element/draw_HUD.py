import pygame
import os

class DrawHUD:
    def __init__(self, font_path: str):
        self.font = pygame.font.Font(font_path, 28)
        self.font_sec = pygame.font.Font(font_path, 18)

        self.font_cheat = pygame.font.Font(font_path, 14) 
        self.text_color = (255, 255, 255)
        self.time_pos = (90, 35)
        self.lives_pos = (90, 90)
        self.score_center = (200, 175)
        self.level_center = (190, 253)


        themes_path = os.path.join("assets", "images", "themes")

        # قمت بإضافة تحجيم (Scale) افتراضي 60x30 لتضمن أن الأزرار الثلاثة تتسع أفقياً في القائمة
        raw_on = pygame.image.load(os.path.join(themes_path, "on.png")).convert_alpha()
        raw_off = pygame.image.load(os.path.join(themes_path, "off.png")).convert_alpha()

        self.img_on = pygame.transform.scale(raw_on, (80, 40))
        self.img_off = pygame.transform.scale(raw_off, (80, 40))

        self.cheats_start_x = 400
        self.cheats_start_y = 60
        self.cheats_spacing = 120

    def draw(self, screen: pygame.Surface, score: int, level: int, lives: int, time_left: int, freeze: bool, invisible: bool, speed: bool) -> None:

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

        cheats = [
            ("FREEZE", freeze),
            ("INVIS", invisible),
            ("SPEED", speed)
        ]

        for i, (name, state) in enumerate(cheats):
            current_img = self.img_on if state else self.img_off

            x_pos = self.cheats_start_x + (i * self.cheats_spacing)
            y_pos = self.cheats_start_y

            # طباعة صورة الزر
            screen.blit(current_img, (x_pos, y_pos))

            # تجهيز نص الخاصية وطباعته تحت الزر بالضبط (في المنتصف)
            text_surface = self.font_cheat.render(name, False, self.text_color)
            text_rect = text_surface.get_rect(
                center=(x_pos + (current_img.get_width() // 2), y_pos + current_img.get_height() + 12)
            )
            screen.blit(text_surface, text_rect)
