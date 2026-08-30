from pydantic import BaseModel, Field


class Gum(BaseModel):
    """
    Represents a consumable Gum (Pac-Dot or Power Pellet) in the maze.

    This model tracks the grid coordinates, point value, and current state
    (whether it is a super gum and whether it has been eaten) of a gum
    entity.

    Attributes:
        grid_x (int): The X coordinate of the gum on the maze grid.
        grid_y (int): The Y coordinate of the gum on the maze grid.
        points (int): The score awarded when this gum is eaten.
        is_super (bool): True if this is a Power Pellet (scares ghosts).
        is_eaten (bool): True if Pacman has already consumed this gum.
    """
    grid_x: int
    grid_y: int
    points: int = Field(default=10)

    is_super: bool = Field(default=False)
    is_eaten: bool = Field(default=False)
