from typing import Any
from pydantic import BaseModel, Field, model_validator


class Pacman(BaseModel):
    x: int = Field(default=0)
    y: int = Field(default=0)
    direction: str = Field(default="NONE")
    next_direction: str = Field(default="NONE")

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
        if not isinstance(data, dict):
            return {}

        safe_data: dict[str, Any] = {}
        defaults = {
            "lives": 3,
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
                    safe_data[key] = default_value
                else:
                    safe_data[key] = value
            except (ValueError, TypeError):
                safe_data[key] = default_value
        return safe_data

    @model_validator(mode="after")
    def validate_game_logic(self) -> "Pacman":
        if self.pacman_speed > 100:
            self.pacman_speed = 100
        self.initial_lives = self.lives
        return self

    def reset_position(self, cell_size: tuple[Any, ...]) -> None:
        self.x = self.center[0] * cell_size
        self.y = self.center[1] * cell_size

        self.direction = None
        self.next_direction = None
