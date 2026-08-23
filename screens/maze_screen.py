import pygame
from entities import GameEntities


class GameScreen:
    """Handles routing the input and triggering the rendering of the game."""

    def __init__(self, screen: pygame.Surface, config: dict):
        self.screen = screen
        self.entities = GameEntities(**config)

    def handle_event(self, event: pygame.event.Event) -> str | None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "back_to_menu"
        return None

    def update(self) -> None:
        self.entities.update_logic()

    def draw(self) -> None:
        self.screen.fill((0, 0, 0))
        self.entities.level.draw(self.screen)
