from typing import Any

from pydantic import BaseModel, Field, model_validator


class Pacman(BaseModel):
    # Runtime attributes
    name: str = Field(default="unknown")
    total_points: int = Field(default=0)

    # Pac-Man configuration
    lives: int = Field(default=3)
    points_per_pacgum: int = Field(default=10)
    points_per_super_pacgum: int = Field(default=50)
    points_per_ghost: int = Field(default=200)
    pacman_speed: int = Field(default=50)

    # Used by reset()
    initial_lives: int = Field(default=3)

    @model_validator(mode="before")
    @classmethod
    def validate_input(cls, data: Any) -> dict[str, Any]:
        if not isinstance(data, dict):
            print(
                "[Warning] Pac-Man configuration is invalid. "
                "Using default values."
            )
            return {}

        safe_data: dict[str, Any] = {}

        defaults = {
            "lives": 3,
            "points_per_pacgum": 10,
            "points_per_super_pacgum": 50,
            "points_per_ghost": 200,
            "pacman_speed": 50,
        }

        for key, default_value in defaults.items():

            if key not in data:
                continue

            value = data[key]

            if value is None or (
                isinstance(value, str) and not value.strip()
            ):
                print(
                    f"[Warning] Invalid value for '{key}'. "
                    f"Using default value: {default_value}."
                )
                continue

            try:
                value = int(value)

                if value <= 0:
                    print(
                        f"[Warning] Invalid value for '{key}'. "
                        f"Using default value: {default_value}."
                    )
                    continue

                safe_data[key] = value

            except (ValueError, TypeError):
                print(
                    f"[Warning] Invalid value for '{key}'. "
                    f"Using default value: {default_value}."
                )

        return safe_data

    @model_validator(mode="after")
    def validate_game_logic(self) -> "Pacman":
        self.initial_lives = self.lives
        return self

    def reset(self) -> None:
        self.lives = self.initial_lives
        self.total_points = 0
        self.name = "unknown"