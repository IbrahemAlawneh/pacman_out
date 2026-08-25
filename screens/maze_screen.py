import pygame
from entities import GameEntities


class GameScreen:
    """Handles routing the input and triggering the
    rendering of the game."""
    CELL_SIZE = 24
    WALL_THICKNESS = 2
    GLOW_THICKNESS = 8

    BACKGROUND_COLOR = (0, 0, 0)
    WALL_COLOR = (0, 220, 225)
    WALL_GLOW_COLOR = (0, 100, 150)
    SPECIAL_CELL_COLOR = (255, 60, 170)
    SPECIAL_CELL_RADIUS = 4

    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8

    def __init__(self, screen: pygame.Surface, config: dict):
        self.screen = screen
        self.config = config
        self.entities = GameEntities(**config)

        self._maze_surface = None
        self._cached_level_id = None

    def handle_event(self, event: pygame.event.Event) -> str | None:
        if event.type == pygame.KEYDOWN:

            if event.key in (pygame.K_ESCAPE, pygame.K_p):
                print("pause screen is open")
                return "back_to_menu"

            elif event.key in (pygame.K_UP, pygame.K_w):
                print("[Action] Move UP")
                # self.pacman.set_direction("UP")

            elif event.key in (pygame.K_DOWN, pygame.K_s):
                print("[Action] Move DOWN")
                # self.pacman.set_direction("DOWN")

            elif event.key in (pygame.K_LEFT, pygame.K_a):
                print("[Action] Move LEFT")
                # self.pacman.set_direction("LEFT")

            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                print("[Action] Move RIGHT")
                # self.pacman.set_direction("RIGHT")

            elif event.key in (
                pygame.K_F1, pygame.K_F2, pygame.K_F3,
                pygame.K_F4, pygame.K_F5
            ):
                cheats = self.config.get("cheats")

                if cheats:
                    enable_all = cheats.get("enable_all", False)

                    if event.key == pygame.K_F1:
                        if enable_all or cheats.get("level_skip", False):
                            print("[Cheat] F1 Activated: Level Skipped!")
                            # self.level_manager.skip()

                    elif event.key == pygame.K_F2:
                        if enable_all or cheats.get("ghost_freeze", False):
                            print("[Cheat] F2 Activated: Ghosts Frozen!")
                            # self.ghost_manager.freeze_all()

                    elif event.key == pygame.K_F3:
                        if enable_all or cheats.get("extra_life", False):
                            print("[Cheat] F3 Activated: Extra Life Added!")
                            # self.config["lives"] += 1

                    elif event.key == pygame.K_F4:
                        if enable_all or cheats.get("speed_boost", False):
                            print("[Cheat] F4 Activated: Speed Boost!")
                            # self.pacman.apply_speed_boost()

                    elif event.key == pygame.K_F5:
                        if enable_all or cheats.get("infinite_lives", False):
                            print(
                                "[Cheat] F5 Activated: Pac-Man have "
                                "infinite_lives"
                            )
                            # self.pacman.set_invincible(True)
        return None

    def update(self) -> None:
        self.entities.update_logic()

    def _build_maze_surface(self, level) -> pygame.Surface:
        """Render the full maze once onto an off-screen surface"""
        grid = level.grid
        width = len(grid[0]) * self.CELL_SIZE
        height = len(grid) * self.CELL_SIZE
        surface = pygame.Surface((width, height))
        surface.fill(self.BACKGROUND_COLOR)

        for row_idx, row in enumerate(grid):
            for col_idx, cell in enumerate(row):
                if cell == 0:
                    continue
                self._draw_cell(surface, cell, row_idx, col_idx)
        return surface

    def _draw_cell(
            self, surface: pygame.Surface, cell: int, row_idx: int,
            col_idx: int
    ) -> None:
        """Draw a single maze cell (special title or bitmask walls)"""
        x = col_idx * self.CELL_SIZE
        y = row_idx * self.CELL_SIZE
        rect = pygame.Rect(x, y, self.CELL_SIZE, self.CELL_SIZE)

        if cell == 15:
            pygame.draw.rect(
                surface, self.SPECIAL_CELL_COLOR, rect,
                border_radius=self.SPECIAL_CELL_RADIUS
            )
            return

        for color, thickness in (
            (self.WALL_GLOW_COLOR, self.GLOW_THICKNESS),
            (self.WALL_COLOR, self.WALL_THICKNESS)
        ):
            if cell & self.NORTH:
                pygame.draw.line(
                    surface, color, rect.topleft, rect.topright, thickness
                )
            if cell & self.EAST:
                pygame.draw.line(
                    surface, color, rect.topright, rect.bottomright, thickness
                )
            if cell & self.SOUTH:
                pygame.draw.line(
                    surface, color, rect.bottomleft,
                    rect.bottomright, thickness
                )
            if cell & self.WEST:
                pygame.draw.line(
                    surface, color, rect.topleft, rect.bottomleft, thickness
                )

    def draw_grid(self, level) -> None:
        """Blit the cached maze surface,
        rebuilding only if the level changed"""
        if not level.grid:
            return

        if self._cached_level_id != level.level_id:
            self._maze_surface = self._build_maze_surface(level)
            self._cached_level_id = level.level_id
        offset_x = (
            self.screen.get_width() - self._maze_surface.get_width()
        ) // 2
        offset_y = (
            self.screen.get_height() - self._maze_surface.get_height()
        ) // 2
        self.screen.blit(self._maze_surface, (offset_x, offset_y))

    def draw(self) -> None:
        self.screen.fill((0, 0, 0))
        self.draw_grid(self.entities.level)
