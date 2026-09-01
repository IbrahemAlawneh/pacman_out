from typing import Any


class Pacman:
    """
    Represents the Pacman entity within the game.

    This model manages Pacman's physical coordinates, current and next
    movement directions, scoring, lives, and active states.
    """
    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        direction: str | None = "NONE",
        next_direction: str | None = "NONE",
        is_alive: bool = True,
        is_invincible: bool = False,
        name: str = "unknown",
        total_points: int = 0,
        lives: int = 3,
        points_per_ghost: int = 200,
        pacman_speed: int = 50,
        center: tuple[int, int] | None = None,
        **kwargs: Any
    ) -> None:
        self.x = x
        self.y = y
        self.direction = direction
        self.next_direction = next_direction
        self.is_alive = is_alive
        self.is_invincible = is_invincible
        self.name = name
        self.total_points = total_points
        self.lives = lives
        self.points_per_ghost = points_per_ghost

        if pacman_speed > 100:
            print(
                "[Warning] pacman_speed exceeds maximum of 100. "
                "Capping to 100."
            )
            self.pacman_speed = 100
        else:
            self.pacman_speed = pacman_speed

        self.initial_lives = self.lives
        self.center = center

    def reset_position(self, cell_size: int) -> None:
        """
        Resets Pacman back to the calculated center of the maze.

        Args:
            cell_size (int): The pixel size of a single grid cell.
        """
        if self.center is not None:
            self.x = self.center[0] * cell_size
            self.y = self.center[1] * cell_size

        self.direction = None
        self.next_direction = None
