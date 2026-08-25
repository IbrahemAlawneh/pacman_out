from typing import Any
from pydantic import BaseModel, Field, model_validator


class Ghost(BaseModel):

    x: int = Field(default=0)
    y: int = Field(default=0)
    spawn_x: int = Field(default=0)
    spawn_y: int = Field(default=0)
    
    direction: str = Field(default="NONE")
    color: tuple[int, int, int] = Field(default=(255, 0, 0))


    is_scared: bool = Field(default=False)
    is_eaten: bool = Field(default=False)
    is_frozen: bool = Field(default=False)

    speed: int = Field(default=50)
    mode: int = Field(default=0)

    @model_validator(mode="before")
    @classmethod
    def validate_input(cls, data: Any) -> dict[str, Any]:
        """
        Validate the configuration passed to a Ghost object.
        mode:
            0 = Random
            1 = Hard
        """
        if not isinstance(data, dict):
            print(
                "[Warning] Ghost configuration is invalid. "
                "Using default values."
            )
            return {}

        safe_data: dict[str, Any] = {}

        speed = data.get("ghost_speed", data.get("speed", 50))

        if speed is None or (isinstance(speed, str) and not speed.strip()):
            print("[Warning] Invalid Ghost speed. Using default value: 50.")
            speed = 50

        try:
            speed = int(speed)
            if speed <= 0:
                print("[Warning] Invalid Ghost speed. Using default value: 50.")
                speed = 50
            elif speed > 100:
                print("[Warning] Invalid Ghost speed. Using Max Speed value: 100.")
                speed = 100
        except (ValueError, TypeError):
            print("[Warning] Invalid Ghost speed. Using default value: 50.")
            speed = 50

        safe_data["speed"] = speed
        mode = data.get("mode", 0)

        if mode is None or (isinstance(mode, str) and not mode.strip()):
            print("[Warning] Invalid Ghost mode. Using default mode: 0 (Random).")
            mode = 0

        try:
            mode = int(mode)
            if mode not in (0, 1):
                print("[Warning] Invalid Ghost mode. Using default mode: 0 (Random).")
                mode = 0
        except (ValueError, TypeError):
            print("[Warning] Invalid Ghost mode. Using default mode: 0 (Random).")
            mode = 0
            
        safe_data["mode"] = mode

        return safe_data

    def set_mode(self, mode: int) -> None:
        """
        Change Ghost mode during the game.
        0 = Random
        1 = Hard
        """
        if mode not in (0, 1):
            print(
                "[Warning] Invalid Ghost mode. "
                "Mode was not changed."
            )
            return
        self.mode = mode

    def is_hard(self) -> bool:
        """Return True if the Ghost is in Hard mode."""
        return self.mode == 1

    def is_random(self) -> bool:
        """Return True if the Ghost is in Random mode."""
        return self.mode == 0

    def get_open_walls(
            self, grid: list[list[int]], check_x: int, check_y: int
    ) -> dict[str, bool]:
        """Return open directions for a specific grid point (True = open)"""
        try:
            cell = grid[check_y][check_x]
            return {
                "up": (cell & 1) == 0,
                "right": (cell & 2) == 0,
                "down": (cell & 4) == 0,
                "left": (cell & 8) == 0
            }
        except IndexError:
            return {
                "up": False, "right": False, "down": False, "left": False
            }

    def reset(self) -> None:
        self.x = self.spawn_x
        self.y = self.spawn_y
        self.direction = "NONE"
        self.is_scared = False
        self.is_eaten = False
        self.is_frozen = False