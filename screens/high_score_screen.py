import json
from pathlib import Path
import pygame

class HighScoreScreen:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        
        # ---------------------------------------------------------
        # Paths & Assets
        # ---------------------------------------------------------
        self.assets_path = Path("assets/main_menu_images/setting")
        self.scores_file = Path("configuration_files/high_score.json")
        
        self.background_image = self._load_image("background_image.jpg")
        self.bar_image = self._load_image("bar_rank.png")
        
        # ---------------------------------------------------------
        # Colors & Fonts
        # ---------------------------------------------------------
        self.HEADER_COLOR = (246, 135, 20) # #f68714
        self.SCROLL_TRACK_COLOR = (20, 10, 40) # لون مسار السكرول الغامق
        self.TEXT_COLOR = (255, 255, 255)
        
        self.font_header = pygame.font.Font(None, 36)
        self.font_data = pygame.font.Font(None, 32)
        self.font_rank = pygame.font.Font(None, 40)
        
        # ---------------------------------------------------------
        # Layout & Dimensions
        # ---------------------------------------------------------
        self.START_X = 307
        self.START_Y = 228
    
    
        self.BAR_WIDTH = 586 
        self.BAR_HEIGHT = 70
        
        if self.bar_image:
            self.bar_image = pygame.transform.smoothscale(self.bar_image, (self.BAR_WIDTH, self.BAR_HEIGHT))
        else:
            self.BAR_WIDTH, self.BAR_HEIGHT = 600, 50
            
        self.HEADER_HEIGHT = 40
        self.GAP_BETWEEN_BARS = 7
        
        # ---------------------------------------------------------
        # Scroll System Variables
        # ---------------------------------------------------------
        self.VISIBLE_ITEMS = 5
        self.scroll_offset = 0
        

        self.SCROLLBAR_WIDTH = 12
        self.SCROLLBAR_X = self.START_X + self.BAR_WIDTH + 15
        self.SCROLLBAR_START_Y = self.START_Y + self.HEADER_HEIGHT
        self.is_dragging = False
        self.drag_mouse_offset_y = 0
    

        self.high_scores: list[dict] = []
        self._load_high_scores()

    def _load_image(self, filename: str) -> pygame.Surface | None:
        filepath = self.assets_path / filename
        try:
            image = pygame.image.load(str(filepath)).convert_alpha()
            if filename == "background_image.jpg" and image.get_size() != self.screen.get_size():
                image = pygame.transform.scale(image, self.screen.get_size())
            return image
        except:
            return None

    def _load_high_scores(self) -> None:
            
        try:
            with open(self.scores_file, "r") as file:
                data = json.load(file)
                self.high_scores = sorted(data, key=lambda x: x.get("score", 0), reverse=True)[:10]
        except:
            self.high_scores = []

    def _draw_empty_state(self) -> None:
        """when the file high socre empty it show message"""
        box_width = self.BAR_WIDTH
        box_height = 150
        box_rect = pygame.Rect(self.START_X, self.START_Y + self.HEADER_HEIGHT + 40, box_width, box_height)
        
        transparent_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        pygame.draw.rect(transparent_surface, (28, 18, 48, 180), transparent_surface.get_rect(), border_radius=12) 
        pygame.draw.rect(transparent_surface, self.HEADER_COLOR, transparent_surface.get_rect(), width=2, border_radius=12) 
        self.screen.blit(transparent_surface, box_rect.topleft)
        

        msg_font = pygame.font.Font(None, 48)
        sub_font = pygame.font.Font(None, 32)
        
        msg_text = msg_font.render("NO RECORDS YET", True, (255, 60, 170)) # لون وردي نيون
        sub_text = sub_font.render("BE THE FIRST TO SET A HIGH SCORE!", True, (200, 200, 220))
        
        msg_rect = msg_text.get_rect(center=(box_rect.centerx, box_rect.centery - 15))
        sub_rect = sub_text.get_rect(center=(box_rect.centerx, box_rect.centery + 25))
        
        self.screen.blit(msg_text, msg_rect)
        self.screen.blit(sub_text, sub_rect)
        

    def handle_event(self, event: pygame.event.Event) -> str | None:
        # 1. الرجوع
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "back_to_menu"
            
        # 2. السكرول بعجلة الماوس
        elif event.type == pygame.MOUSEWHEEL:
            total_items = len(self.high_scores)
            if total_items > self.VISIBLE_ITEMS:
                max_scroll = total_items - self.VISIBLE_ITEMS
                self.scroll_offset -= event.y 
                self.scroll_offset = max(0, min(self.scroll_offset, max_scroll))

        # 3. بداية مسك السكرول بار بالماوس (كليك يسار)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            sb_data = self._get_scrollbar_data()
            if sb_data and sb_data["thumb_rect"].collidepoint(event.pos):
                self.is_dragging = True
                # نحفظ مكان مسكة الماوس لكي لا يقفز السكرول فجأة
                self.drag_mouse_offset_y = event.pos[1] - sb_data["thumb_rect"].y
                return None

        # 4. إفلات الماوس
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.is_dragging = False

        # 5. السحب (تحريك الماوس وهو مضغوط)
        elif event.type == pygame.MOUSEMOTION:
            if self.is_dragging:
                sb_data = self._get_scrollbar_data()
                if sb_data and sb_data["max_thumb_travel"] > 0:
                    # حساب الـ Y الجديد بناءً على حركة الماوس
                    new_thumb_y = event.pos[1] - self.drag_mouse_offset_y
                    
                    # تحويل الـ Y الجديد إلى نسبة مئوية (Scroll Ratio)
                    travel_y = new_thumb_y - self.SCROLLBAR_START_Y
                    travel_y = max(0, min(travel_y, sb_data["max_thumb_travel"])) # Clamp
                    
                    scroll_ratio = travel_y / sb_data["max_thumb_travel"]
                    
                    # تحويل النسبة إلى إزاحة الكروت
                    self.scroll_offset = int(round(scroll_ratio * sb_data["max_scroll_offset"]))

        return None
    
    
    
    def draw(self) -> None:
        if self.background_image:
            self.screen.blit(self.background_image, (0, 0))
        
        self._draw_header()
        
        if not self.high_scores:
            self._draw_empty_state()
        else:
            total_list_height = (self.BAR_HEIGHT + self.GAP_BETWEEN_BARS) * self.VISIBLE_ITEMS
            clip_rect = pygame.Rect(self.START_X, self.START_Y + self.HEADER_HEIGHT, self.BAR_WIDTH, total_list_height)
            
            self.screen.set_clip(clip_rect)
            self._draw_score_bars()
            self.screen.set_clip(None)
            
            self._draw_scrollbar()

    def _draw_scrollbar(self) -> None:
        sb_data = self._get_scrollbar_data()
        if not sb_data:
            return
            
        track_rect = sb_data["track_rect"]
        thumb_rect = sb_data["thumb_rect"]
        
        thumb_color = "#5e17eb" if self.is_dragging else self.HEADER_COLOR
        
        pygame.draw.rect(self.screen, self.SCROLL_TRACK_COLOR, track_rect, border_radius=6)
        pygame.draw.rect(self.screen, thumb_color, thumb_rect, border_radius=6)

    def _draw_header(self) -> None:
        header_rect = pygame.Rect(self.START_X, self.START_Y, self.BAR_WIDTH, self.HEADER_HEIGHT)
        pygame.draw.rect(self.screen, self.HEADER_COLOR, header_rect, border_top_left_radius=8, border_top_right_radius=8)
        
        rank_surface = self.font_header.render("RANK", True, self.TEXT_COLOR)
        name_surface = self.font_header.render("NAME", True, self.TEXT_COLOR)
        score_surface = self.font_header.render("TOTAL POINT", True, self.TEXT_COLOR)
        
        self.screen.blit(rank_surface, (self.START_X + 20, self.START_Y + 10))
        self.screen.blit(name_surface, (self.START_X + 180, self.START_Y + 10))
        self.screen.blit(score_surface, (self.START_X + self.BAR_WIDTH - score_surface.get_width() - 30, self.START_Y + 10))

    def _draw_score_bars(self) -> None:

        start_drawing_y = self.START_Y + self.HEADER_HEIGHT + self.GAP_BETWEEN_BARS
        start_drawing_y -= self.scroll_offset * (self.BAR_HEIGHT + self.GAP_BETWEEN_BARS)
        
        current_y = start_drawing_y
        
        for index, player in enumerate(self.high_scores):
    
            if current_y + self.BAR_HEIGHT < self.START_Y + self.HEADER_HEIGHT:
                current_y += self.BAR_HEIGHT + self.GAP_BETWEEN_BARS
                continue
            if current_y > self.START_Y + self.HEADER_HEIGHT + ((self.BAR_HEIGHT + self.GAP_BETWEEN_BARS) * self.VISIBLE_ITEMS):
                break
            
            if self.bar_image:
                self.screen.blit(self.bar_image, (self.START_X, current_y))
                
            rank_surface = self.font_rank.render(str(index + 1), True, self.TEXT_COLOR)
            name_surface = self.font_data.render(str(player.get("name", "Unknown")), True, self.TEXT_COLOR)
            score_surface = self.font_data.render(str(player.get("score", "0")), True, self.TEXT_COLOR)

            rank_rect = rank_surface.get_rect(center=(self.START_X + 40, current_y + self.BAR_HEIGHT // 2))
            self.screen.blit(rank_surface, rank_rect)

            name_rect = name_surface.get_rect(midleft=(self.START_X + 180, current_y + self.BAR_HEIGHT // 2))
            self.screen.blit(name_surface, name_rect)

            score_rect = score_surface.get_rect(midright=(self.START_X + self.BAR_WIDTH - 40, current_y + self.BAR_HEIGHT // 2))
            self.screen.blit(score_surface, score_rect)

            current_y += self.BAR_HEIGHT + self.GAP_BETWEEN_BARS
            
            
    def _get_scrollbar_data(self) -> dict | None:
        """ترجع إحداثيات وأبعاد السكرول بار إذا كان ظاهراً"""
        total_items = len(self.high_scores)
        if total_items <= self.VISIBLE_ITEMS:
            return None
            
        total_visible_height = (self.BAR_HEIGHT + self.GAP_BETWEEN_BARS) * self.VISIBLE_ITEMS
        track_rect = pygame.Rect(self.SCROLLBAR_X, self.SCROLLBAR_START_Y, self.SCROLLBAR_WIDTH, total_visible_height)
        
        thumb_height_ratio = self.VISIBLE_ITEMS / total_items
        thumb_height = max(30, int(total_visible_height * thumb_height_ratio))
        
        max_scroll_offset = total_items - self.VISIBLE_ITEMS
        max_thumb_travel = total_visible_height - thumb_height
        
        scroll_ratio = self.scroll_offset / max_scroll_offset
        thumb_y = self.SCROLLBAR_START_Y + int(scroll_ratio * max_thumb_travel)
        thumb_rect = pygame.Rect(self.SCROLLBAR_X, thumb_y, self.SCROLLBAR_WIDTH, thumb_height)
        
        return {
            "track_rect": track_rect,
            "thumb_rect": thumb_rect,
            "max_scroll_offset": max_scroll_offset,
            "max_thumb_travel": max_thumb_travel
        }
