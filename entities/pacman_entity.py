from typing import Any
from pydantic import BaseModel, Field, model_validator


class Pacman(BaseModel):
    """
    Represents the Pacman entity within the game.

    This model manages Pacman's physical coordinates, current and next
    movement directions, scoring, lives, and active states (e.g., alive,
    invincible).
    """
    x: int = Field(default=0)
    y: int = Field(default=0)
    direction: str | None = Field(default="NONE")
    next_direction: str | None = Field(default="NONE")

    is_alive: bool = Field(default=True)
    is_invincible: bool = Field(default=False)

    name: str = Field(default="unknown")
    total_points: int = Field(default=0)

    lives: int = Field(default=3)
    initial_lives: int = Field(default=3)

    points_per_ghost: int = Field(default=200)
    pacman_speed: int = Field(default=50)
    center: tuple | None = Field(default=None)

    @model_validator(mode="before")
    @classmethod
    def validate_input(cls, data: Any) -> dict[str, Any]:
        """
        Validates the configuration passed to a Pacman object before
        instantiation.

        Ensures that core integer fields (lives, points, speed) are valid
        and greater than zero. Invalid values trigger a warning and are
        replaced with safe defaults.

        Args:
            data (Any): The raw configuration dictionary for Pacman.

        Returns:
            dict[str, Any]: A sanitized dictionary with valid values.
        """
        if not isinstance(data, dict):
            print(
                "[Warning] Pacman configuration is invalid. "
                "Using default values."
            )
            return {}

        safe_data: dict[str, Any] = {}
        defaults = {
            "lives": 4,
            "points_per_ghost": 200,
            "pacman_speed": 50,
        }

        for key, default_value in defaults.items():
            if key not in data:
                continue
            value = data[key]
            try:
                value = int(value)
                if value <= 0:
                    print(
                        f"[Warning] Invalid {key} (<= 0). "
                        f"Using default: {default_value}."
                    )
                    safe_data[key] = default_value
                else:
                    safe_data[key] = value
            except (ValueError, TypeError):
                print(
                    f"[Warning] Invalid type for {key}. "
                    f"Using default: {default_value}."
                )
                safe_data[key] = default_value
        return safe_data

    @model_validator(mode="after")
    def validate_game_logic(self) -> "Pacman":
        """
        Validates game logic boundaries and initializes relationships after
        the model has been populated.

        Caps the maximum speed at 100 to prevent physics issues and stores
        the initial lives count for potential resets.

        Returns:
            Pacman: The fully validated and initialized Pacman instance.
        """
        if self.pacman_speed > 100:
            print(
                "[Warning] pacman_speed exceeds maximum of 100. "
                "Capping to 100."
            )
            self.pacman_speed = 100
        self.initial_lives = self.lives
        return self

    def reset_position(self, cell_size: int) -> None:
        """
        Resets Pacman back to the calculated center of the maze.

        This is typically called when a new level starts or when Pacman
        loses a life, halting all current movement directions.

        Args:
            cell_size (int): The pixel size of a single grid cell.
        """
        if self.center is not None:
            self.x = self.center[0] * cell_size
            self.y = self.center[1] * cell_size

        self.direction = None
        self.next_direction = None
