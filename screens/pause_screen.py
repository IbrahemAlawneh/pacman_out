import pygame


class PauseScreen:
    """Transparent pause menu and How to Play screen."""

    MENU, HELP = "menu", "help"
    OVERLAY = (4, 7, 22, 145)
    PANEL = (13, 18, 46, 145)
    CYAN, PINK, PURPLE = (70, 220, 255), (220, 100, 255), (190, 140, 255)
    WHITE, MUTED, LINE = (240, 245, 255), (150, 165, 205), (63, 81, 132)
    PURPLE_BTN = ((225, 150, 255), (110, 45, 160), (240, 190, 255))
    STEEL_BTN = ((70, 100, 145), (25, 35, 70), (90, 180, 220))

    def __init__(self, surface: pygame.Surface) -> None:
        """Create the menu and calculate its button positions."""
        self.surface, self.mode, self.selected = surface, self.MENU, 0
        font = pygame.font.match_font("segoeui,dejavusans,arial")
        self.title = pygame.font.Font(font, 48)
        self.button = pygame.font.Font(font, 22)
        self.text = pygame.font.Font(font, 18)
        self.small = pygame.font.Font(font, 15)

        labels = (("RESUME GAME", "resume"), ("HOW TO PLAY", "instructions"),
                  ("MAIN MENU", "back_to_menu"), ("QUIT GAME", "quit"))
        x, y = surface.get_width() // 2 - 170, surface.get_height() // 2 - 64
        self.buttons = [
            {"text": text, "action": action,
             "rect": pygame.Rect(x, y + i * 78, 340, 64)}
            for i, (text, action) in enumerate(labels)
        ]

    def open(self) -> None:
        """Reset the screen to the pause menu."""
        self.mode, self.selected = self.MENU, 0

    def handle_event(self, event: pygame.event.Event) -> str | None:
        """Handle keyboard and mouse input."""
        if self.mode == self.HELP:
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_BACKSPACE):
                self.mode = self.MENU
            return None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "resume"
            if event.key in (pygame.K_UP, pygame.K_w):
                self.selected = (self.selected - 1) % len(self.buttons)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected = (self.selected + 1) % len(self.buttons)
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                return self._activate(self.selected)
        elif event.type == pygame.MOUSEMOTION:
            for i, button in enumerate(self.buttons):
                if button["rect"].collidepoint(event.pos):
                    self.selected = i
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, button in enumerate(self.buttons):
                if button["rect"].collidepoint(event.pos):
                    return self._activate(i)
        return None

    def _activate(self, index: int) -> str | None:
        """Run the selected action."""
        action = self.buttons[index]["action"]
        if action == "instructions":
            self.mode = self.HELP
            return None
        return action

    def _text(self, value: str, pos: tuple[int, int], font: pygame.font.Font,
              color: tuple[int, int, int] = WHITE, center: bool = True) -> None:
        """Draw text centered unless requested otherwise."""
        image = font.render(value, True, color)
        self.surface.blit(image, image.get_rect(center=pos) if center else image.get_rect(topleft=pos))

    def _panel(self, rect: pygame.Rect, border: tuple[int, int, int]) -> None:
        """Draw a transparent rounded panel."""
        layer = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.rect(layer, self.PANEL, layer.get_rect(), border_radius=22)
        self.surface.blit(layer, rect.topleft)
        pygame.draw.rect(self.surface, border, rect, 2, border_radius=22)

    def draw(self) -> None:
        """Draw the overlay and the current page."""
        overlay = pygame.Surface(self.surface.get_size(), pygame.SRCALPHA)
        overlay.fill(self.OVERLAY)
        self.surface.blit(overlay, (0, 0))
        self._draw_help() if self.mode == self.HELP else self._draw_menu()

    def _draw_button(self, rect: pygame.Rect, label: str, active: bool) -> None:
        """Draw the original metallic button with slight transparency."""
        top, bottom, border = self.PURPLE_BTN if active else self.STEEL_BTN
        layer = pygame.Surface(rect.size, pygame.SRCALPHA)
        for y in range(rect.height):
            ratio = y / rect.height
            color = tuple(int(top[i] + (bottom[i] - top[i]) * ratio) for i in range(3))
            pygame.draw.line(layer, (*color, 150), (0, y), (rect.width, y))

        mask = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.rect(mask, (255, 255, 255, 255), mask.get_rect(), border_radius=32)
        layer.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        self.surface.blit(layer, rect.topleft)

        gloss = pygame.Surface((rect.width - 16, rect.height // 3), pygame.SRCALPHA)
        pygame.draw.rect(gloss, (255, 255, 255, 65), gloss.get_rect(), border_radius=12)
        self.surface.blit(gloss, (rect.x + 8, rect.y + 4))
        pygame.draw.rect(self.surface, border, rect, 3 if active else 2, border_radius=32)

        if active:
            glow = pygame.Surface((rect.width + 16, rect.height + 16), pygame.SRCALPHA)
            pygame.draw.rect(glow, (*border, 45), glow.get_rect(), border_radius=40)
            self.surface.blit(glow, (rect.x - 8, rect.y - 8))
        color = (35, 25, 10) if active else self.WHITE
        self._text(label, rect.center, self.button, color)

    def _draw_menu(self) -> None:
        """Draw the main pause page."""
        panel = pygame.Rect(0, 0, 500, 560)
        panel.center = self.surface.get_rect().center
        self._panel(panel, self.PINK)
        self._text("PAUSED", (panel.centerx, panel.y + 55), self.title)
        self._text("THE GAME IS ON HOLD", (panel.centerx, panel.y + 93), self.small, self.MUTED)
        pygame.draw.line(self.surface, self.LINE, (panel.x + 45, panel.y + 118), (panel.right - 45, panel.y + 118))
        mouse = pygame.mouse.get_pos()
        for i, button in enumerate(self.buttons):
            rect = button["rect"]
            active = i == self.selected or rect.collidepoint(mouse)
            self._draw_button(rect, button["text"], active)
        self._text("UP / DOWN SELECT   ENTER CONFIRM   ESC RESUME",
                   (panel.centerx, panel.bottom - 25), self.small, self.MUTED)

    def _draw_help(self) -> None:
        """Draw How to Play in the same visual style as Pause."""
        panel = pygame.Rect(0, 0, 610, 520)
        panel.center = self.surface.get_rect().center
        self._panel(panel, self.CYAN)
        self._text("HOW TO PLAY", (panel.centerx, panel.y + 45), self.title)
        self._text("CONTROLS & CHEAT COMMANDS", (panel.centerx, panel.y + 82), self.small, self.CYAN)
        self._text("ENABLE IN SETTINGS FIRST", (panel.centerx, panel.y + 104), self.small, self.PURPLE)
        pygame.draw.line(self.surface, self.LINE, (panel.x + 40, panel.y + 125), (panel.right - 40, panel.y + 125))

        rows = (("MOVE", "Arrow keys or WASD", self.CYAN), ("SKIP LEVEL", "F1", self.PURPLE),
                ("FREEZE GHOSTS", "F2", self.PURPLE), ("EXTRA LIFE", "F3", self.PURPLE),
                ("SPEED BOOST", "F4", self.PURPLE), ("GHOST SHIELD", "F5", self.PURPLE))
        for i, (name, key, color) in enumerate(rows):
            y = panel.y + 155 + i * 42
            name_img = self.text.render(name, True, color)
            name_box = pygame.Rect(panel.x + 42, y - 5, name_img.get_width() + 26, 30)
            key_img = self.text.render(key, True, self.WHITE)
            key_box = pygame.Rect(panel.right - key_img.get_width() - 68, y - 5, key_img.get_width() + 26, 30)
            for box, fill, border in ((name_box, (19, 31, 65, 170), color),
                                      (key_box, (19, 31, 65, 200), self.CYAN)):
                layer = pygame.Surface(box.size, pygame.SRCALPHA)
                pygame.draw.rect(layer, fill, layer.get_rect(), border_radius=9)
                self.surface.blit(layer, box.topleft)
                pygame.draw.rect(self.surface, border, box, 1, border_radius=9)
            self.surface.blit(name_img, name_img.get_rect(center=name_box.center))
            self.surface.blit(key_img, key_img.get_rect(center=key_box.center))
            pygame.draw.line(self.surface, self.LINE, (panel.x + 40, y + 31), (panel.right - 40, y + 31))
        self._text("ESC / BACKSPACE  RETURN TO PAUSE MENU",
                   (panel.centerx, panel.bottom - 25), self.small, self.MUTED)
