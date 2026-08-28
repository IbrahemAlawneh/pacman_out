from typing import Any
from pydantic import BaseModel, Field, model_validator
from .ghost_entity import Ghost
from .level_entity import Level
from .pacman_entity import Pacman
from .gum_entity import Gum


class GameEntities(BaseModel):
    highscore_filename: str = Field(default="highscores.json")

    lives: int = Field(default=3)

    points_per_ghost: int = Field(default=200)
    pacman_speed: int = Field(default=50)

    ghost_speed: int = Field(default=50)
    ghosts_mode: int = Field(default=1)

    seed: int= Field(default=-1)
    level_max_time: int = Field(default=90)
    max_level: int = Field(default=10)

    width: int = Field(default=20)
    height: int = Field(default=20)
    points_per_super_pacgum: int = Field(default=40)
    points_pes_pacgum:int = Field(default=20)
    
    scared_duration_ms: int = Field(default=10000)
    ghost_respawn_ms: int = Field(default=5000)

    # Runtime entities
    pacman: Pacman = Field(default_factory=Pacman)
    ghosts: list[Ghost] = Field(default_factory=list)
    level: Level = Field(default_factory=Level)
    gums: list[Gum] = Field(default_factory=list)
    @model_validator(mode="before")
    @classmethod
    def validate_config(cls, data: Any) -> dict[str, Any]:
        if not isinstance(data, dict):
            print(
                "[Warning] Configuration data is not a valid object. "
                "Using default values."
            )
            return {}

        safe_data: dict[str, Any] = {}

        for key, value in data.items():
            if not isinstance(key, str):
                print(
                    "[Warning] A configuration key is not a string. "
                    "The key will be ignored."
                )
                continue

            normalized_key = key.strip().lower()
            safe_data[normalized_key] = value
        return safe_data

    @model_validator(mode="after")
    def create_entities(self) -> "GameEntities":
        
        self.points_per_ghost = max(50, min(self.points_per_ghost, 500))
        pacman_config = {
            "lives": self.lives,
            "points_per_ghost": self.points_per_ghost,
            "pacman_speed": self.pacman_speed,
        }
        self.pacman = Pacman(**pacman_config)


        level_config = {
            "seed": self.seed,
            "level_max_time": self.level_max_time,
            "max_level": self.max_level,
            "width": self.width,
            "height": self.height,
        }
        self.level = Level(**level_config)
        
        
        ghosts_mode = self._validate_ghosts_mode(self.ghosts_mode)
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
            (255, 0, 0),
            (255, 184, 255),
            (0, 255, 255),
            (255, 184, 82)
            ]
        
        for ghost_index in range(4):
            mode = (ghosts_mode >> ghost_index) & 1

            grid_x, grid_y = corners[ghost_index]
            ghost_config = {
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
        
        self.points_per_super_pacgum = max(20, min(self.points_per_super_pacgum , 200))
        self.points_pes_pacgum = max(10, min(self.points_pes_pacgum, 100))
        
        for row_idx, row in enumerate(self.level.grid):
            for col_idx, cell in enumerate(row):

                if cell == 15:
                    continue

                is_corner = (row_idx == 0 or row_idx == max_row) and (col_idx == 0 or col_idx == max_col)

                if is_corner:
                    self.gums.append(Gum(grid_x=col_idx, grid_y=row_idx,is_super=True,points=self.points_per_super_pacgum))
                else:
                    self.gums.append(Gum(grid_x=col_idx, grid_y=row_idx,points=self.points_pes_pacgum))

        return self

    @staticmethod
    def _validate_ghosts_mode(value: Any) -> int:
        try:
            value = int(value)
        except (ValueError, TypeError):
            print(
                "[Warning] Invalid ghosts_mode. "
                "Using default value: 1."
            )
            return 1

        if value < 1:
            print(
                "[Warning] ghosts_mode cannot be less than 1. "
                "Using value: 1."
            )
            return 1

        if value > 15:
            print(
                "[Warning] ghosts_mode cannot be greater than 15. "
                "Using maximum value: 15."
            )
            return 15
        return value
    
    def gum_reset(self) -> None:
        self.gums = []
        
        max_row = len(self.level.grid) - 1
        max_col = len(self.level.grid[0]) - 1

        for row_idx, row in enumerate(self.level.grid):
            for col_idx, cell in enumerate(row):
                
                if cell == 15:
                    continue
                
                is_corner = (row_idx == 0 or row_idx == max_row) and (col_idx == 0 or col_idx == max_col)
                
                if is_corner:
                    self.gums.append(Gum(grid_x=col_idx, grid_y=row_idx, is_super=True, points=self.points_per_super_pacgum))
                else:
                    self.gums.append(Gum(grid_x=col_idx, grid_y=row_idx,points=self.points_pes_pacgum))
