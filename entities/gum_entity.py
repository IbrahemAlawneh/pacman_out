class Gum:
    """
    Represents a consumable Gum (Pac-Dot or Power Pellet) in the maze.

    This model tracks the grid coordinates, point value, and current state
    (whether it is a super gum and whether it has been eaten).
    """
    def __init__(
        self,
        grid_x: int,
        grid_y: int,
        points: int = 10,
        is_super: bool = False,
        is_eaten: bool = False
    ) -> None:
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.points = points
        self.is_super = is_super
        self.is_eaten = is_eaten
