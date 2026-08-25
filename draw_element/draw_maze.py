import pygame

class DrawMaze:
    """kos omo mn code"""    
    WALL_THICKNESS = 4
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

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self._maze_surface = None
        self._cached_level_id = None

    def _build_maze_surface(self, level, cell_size: int) -> pygame.Surface:
        """Render the full maze once onto an off-screen surface"""
        grid = level.grid
        grid_height_count = len(grid)
        grid_width_count = len(grid[0])


        width_px = grid_width_count * cell_size
        height_px = grid_height_count * cell_size
        
        surface = pygame.Surface((width_px, height_px))
        surface.fill(self.BACKGROUND_COLOR)

        for row_idx, row in enumerate(grid):
            for col_idx, cell in enumerate(row):
                if cell == 0:
                    continue
                self._draw_cell(surface, cell, row_idx, col_idx, cell_size)
                
        return surface

    def _draw_cell(self, surface: pygame.Surface, cell: int, row_idx: int, col_idx: int, cell_size: int) -> None:
        """Draw a single maze cell using the provided cell_size"""
        x = col_idx * cell_size
        y = row_idx * cell_size
        rect = pygame.Rect(x, y, cell_size, cell_size)

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
                pygame.draw.line(surface, color, rect.topleft, rect.topright, thickness)
            if cell & self.EAST:
                pygame.draw.line(surface, color, rect.topright, rect.bottomright, thickness)
            if cell & self.SOUTH:
                pygame.draw.line(surface, color, rect.bottomleft, rect.bottomright, thickness)
            if cell & self.WEST:
                pygame.draw.line(surface, color, rect.topleft, rect.bottomleft, thickness)

    def draw(self, level, cell_size: int, offset_x: int, offset_y: int) -> None:
        """
        يرسم المتاهة على الشاشة بناءً على الإزاحة وحجم الخلية المستلمين من GameScreen
        """
        if not level.grid:
            return

        if self._cached_level_id != level.level_id:
            self._maze_surface = self._build_maze_surface(level, cell_size)
            self._cached_level_id = level.level_id
            

        self.screen.blit(self._maze_surface, (offset_x, offset_y))