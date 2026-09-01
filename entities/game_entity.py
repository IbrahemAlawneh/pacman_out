from typing import Any
from pydantic import BaseModel, Field, model_validator, ConfigDict
from .ghost_entity import Ghost
from .level_entity import Level
from .pacman_entity import Pacman
from .gum_entity import Gum


class GameEntities(BaseModel):
    """
    Central configuration and state manager for the game.

    This model parses raw configuration data, validates it strictly against
    types and boundary ranges, and instantiates all primary game entities.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)
    highscore_filename: str = Field(default="highscores.json")

    lives: int = Field(default=3)

    points_per_ghost: int = Field(default=200)
    pacman_speed: int = Field(default=50)
    ghost_speed: int = Field(default=50)
    ghosts_mode: int = Field(default=1)
    seed: int = Field(default=42)
    max_time: int = Field(default=90)
    max_level: int = Field(default=10)

    width: int = Field(default=20)
    height: int = Field(default=20)
    points_per_super_pacgum: int = Field(default=40)
    points_pes_pacgum: int = Field(default=10)

    scared_duration_ms: int = Field(default=10000)
    ghost_respawn_ms: int = Field(default=5000)

    pacman: Pacman = Field(default_factory=Pacman)
    ghosts: list[Ghost] = Field(default_factory=list)
    level: Level = Field(default_factory=Level)
    gums: list[Gum] = Field(default_factory=list)

    @model_validator(mode="before")
    @classmethod
    def validate_config(cls, data: Any) -> dict[str, Any]:
        """
        Pre-validation hook acting as an ultimate shield.
        Validates both data types and boundaries (min/max ranges).
        Out-of-bound values are safely clamped, and invalid types fallback
        to safe defaults with terminal warnings.
        """
        if not isinstance(data, dict):
            print(
                "[Warning] Configuration data is not a valid object. "
                "Using default values for everything."
            )
            return {}

        safe_data: dict[str, Any] = {}
        int_fields = {
            "lives": (3, 1, 10),
            "points_per_ghost": (200, 50, 500),
            "pacman_speed": (50, 40, 100),
            "ghost_speed": (50, 40, 100),
            "ghosts_mode": (1, 1, 15),
            "seed": (42, -1, 1000),
            "points_per_super_pacgum": (40, 20, 200),
            "points_pes_pacgum": (20, 10, 100),
            "scared_duration_ms": (10000, 5000, 12000),
            "ghost_respawn_ms": (5000, 3000, 6000),
            "max_time": (90, 20, 100),
            "max_level": (10, 1, 10),
            "width": (15, 9, 18),
            "height": (12, 8, 15)
        }

        for key, value in data.items():
            if not isinstance(key, str):
                print(
                    f"[Warning] Key '{key}' is not a string. "
                    "The key will be ignored."
                )
                continue

            norm_key = key.strip().lower()

            if norm_key == "highscore_filename":
                if not value or not isinstance(value, str):
                    print(
                        f"[Warning] Invalid {norm_key}: '{value}'. "
                        "Using default: highscores.json"
                    )
                else:
                    safe_data[norm_key] = str(value)

            elif norm_key in int_fields:
                default_val, min_val, max_val = int_fields[norm_key]
                try:
                    if isinstance(value, bool):
                        raise ValueError

                    if isinstance(value, float):
                        print(
                            f"[Warning] {norm_key} is a float ({value}). "
                            f"Truncating to integer: {int(value)}."
                        )

                    parsed_val = int(value)

                    if min_val is not None and max_val is not None:
                        if parsed_val < min_val or parsed_val > max_val:
                            clamped = max(min_val, min(parsed_val, max_val))
                            print(
                                f"[Warning] {norm_key} is out of bounds. "
                                f"Clamping {parsed_val} -> {clamped}."
                            )
                            safe_data[norm_key] = clamped
                        else:
                            safe_data[norm_key] = parsed_val
                    else:
                        safe_data[norm_key] = parsed_val

                except (ValueError, TypeError):
                    print(
                        f"[Warning] Invalid type for {norm_key}: '{value}'. "
                        f"Using default: {default_val}."
                    )

        return safe_data

    @model_validator(mode="after")
    def create_entities(self) -> "GameEntities":
        """
        Post-validation hook that initializes child entities.
        Since all bounding and clamping is guaranteed by the before-validator,
        this method only focuses on safe instantiation and grid processing.
        """
        pacman_config: dict[str, Any] = {
            "lives": self.lives,
            "points_per_ghost": self.points_per_ghost,
            "pacman_speed": self.pacman_speed,
        }
        self.pacman = Pacman(**pacman_config)

        level_config: dict[str, Any] = {
            "seed": self.seed,
            "max_time": self.max_time,
            "max_level": self.max_level,
            "width": self.width,
            "height": self.height,
        }
        self.level = Level(**level_config)

        self.ghosts = []
        max_x = self.level.width - 1
        max_y = self.level.height - 1
        corners = [
            (0, 0),
            (max_x, 0),
            (0, max_y),
            (max_x, max_y)
        ]
        colors = [
            "orange",
            "blue",
            "purple",
            "green"
        ]

        for ghost_index in range(4):
            mode = (self.ghosts_mode >> ghost_index) & 1
            grid_x, grid_y = corners[ghost_index]
            ghost_config: dict[str, Any] = {
                "ghost_speed": self.ghost_speed,
                "mode": mode,
                "color": colors[ghost_index],
                "x": grid_x,
                "y": grid_y,
                "spawn_x": grid_x,
                "spawn_y": grid_y,
                "chase_algorithm": ghost_index % 2
            }
            ghost = Ghost(**ghost_config)
            self.ghosts.append(ghost)

        self.gums = []
        max_row = len(self.level.grid) - 1
        max_col = len(self.level.grid[0]) - 1

        for row_idx, row in enumerate(self.level.grid):
            for col_idx, cell in enumerate(row):
                if cell == 15:
                    continue
                is_corner = (
                    row_idx == 0 or row_idx == max_row
                ) and (col_idx == 0 or col_idx == max_col)

                if is_corner:
                    self.gums.append(
                        Gum(
                            grid_x=col_idx, grid_y=row_idx, is_super=True,
                            points=self.points_per_super_pacgum
                        )
                    )
                else:
                    self.gums.append(
                        Gum(
                            grid_x=col_idx, grid_y=row_idx,
                            points=self.points_pes_pacgum
                        )
                    )
        return self

    def gum_reset(self) -> None:
        """
        Clears the current gums list and respawns standard and super gums
        based on the current maze grid layout.
        """
        self.gums = []
        max_row = len(self.level.grid) - 1
        max_col = len(self.level.grid[0]) - 1

        for row_idx, row in enumerate(self.level.grid):
            for col_idx, cell in enumerate(row):
                if cell == 15:
                    continue
                is_corner = (
                    row_idx == 0 or row_idx == max_row
                ) and (col_idx == 0 or col_idx == max_col)

                if is_corner:
                    self.gums.append(
                        Gum(
                            grid_x=col_idx, grid_y=row_idx, is_super=True,
                            points=self.points_per_super_pacgum
                        )
                    )
                else:
                    self.gums.append(
                        Gum(
                            grid_x=col_idx, grid_y=row_idx,
                            points=self.points_pes_pacgum
                        )
                    )
