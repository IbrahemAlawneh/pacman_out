from typing import Any
from pydantic import BaseModel, Field, model_validator
from mazegenerator import MazeGenerator


class Level(BaseModel):
    """
    Represents the game level and maze configuration.

    This model manages the current level state, maze dimensions, time
    limits, and handles the generation of new mazes as the player
    progresses through the game.
    """
    level_id: int = Field(default=1)

    width: int = Field(default=20)
    height: int = Field(default=20)

    max_level: int = Field(default=10)
    max_time: int = Field(default=90)
    seed: int = Field(default=-1)

    initial_width: int = Field(default=20)
    initial_height: int = Field(default=20)

    maze: Any = Field(default=None)
    size_increment: int = Field(default=1)

    @model_validator(mode="before")
    @classmethod
    def validate_input(cls, data: Any) -> dict[str, Any]:
        """
        Safely validates the Level configuration before instantiation.

        Ensures constraints like max_level, max_time, seed, width, and
        height are valid integers. Invalid or missing values are caught,
        warnings are printed to the terminal, and safe defaults are applied.

        Args:
            data (Any): The raw configuration dictionary for the level.

        Returns:
            dict[str, Any]: A sanitized dictionary with valid values.
        """
        if not isinstance(data, dict):
            print(
                "[Warning] Level configuration is invalid. "
                "Using default values."
            )
            return {}

        safe_data: dict[str, Any] = {}

        max_level = data.get("max_level", 10)
        try:
            max_level = int(max_level)
            if max_level < 3:
                print(
                    "[Warning] max_level cannot be less than 3. "
                    "Using minimum value: 3."
                )
                max_level = 3
            elif max_level > 10:
                print(
                    "[Warning] max_level cannot be greater than 10. "
                    "Using maximum value: 10."
                )
                max_level = 10
        except (ValueError, TypeError):
            print(
                "[Warning] Invalid max_level. "
                "Using default value: 10."
                )
            max_level = 10

        safe_data["max_level"] = max_level

        max_time = data.get("max_time", 90)
        try:
            max_time = int(max_time)
            if max_time < 20:
                print(
                    "[Warning] max_time cannot be less than 20. "
                    "Using minimum value: 20."
                    )
                max_time = 20

            elif max_time > 100:
                print(
                    "[Warning] max_time cannot be greater than 100. "
                    "Using maximum value: 100."
                    )
                max_time = 100
        except (ValueError, TypeError):
            print(
                "[Warning] Invalid max_time. "
                "Using default value: 40."
                )
            max_time = 90
        safe_data["max_time"] = max_time

        seed = data.get("seed", 42)
        try:
            seed = int(seed)
        except (ValueError, TypeError):
            print(
                "[Warning] Invalid seed. "
                "Using default value: 42."
            )
            seed = 42
        safe_data["seed"] = seed
        try:
            safe_data["width"] = int(data.get("width", 15))
            safe_data["height"] = int(data.get("height", 12))

        except (ValueError, TypeError):
            safe_data["width"] = 15
            safe_data["height"] = 12
        return safe_data

    @model_validator(mode="after")
    def validate_game_logic(self) -> "Level":
        """
        Validates relationships between Level attributes and initializes
        the first maze layout.

        Clamps the initial width and height to safe boundaries for rendering,
        and invokes the MazeGenerator to build the level grid.

        Returns:
            Level: The fully initialized Level instance.
        """
        if self.width > 18 or self.width < 9:
            print("[Warning] Invalid width maze. Using default value: 15.")
            self.width = 15
        if self.height > 15 or self.height < 8:
            print("[Warning] Invalid height maze. Using default value: 12.")
            self.height = 12

        self.initial_width = self.width
        self.initial_height = self.height

        self.size_increment = 1

        self.maze: MazeGenerator = MazeGenerator(
            size=(self.width, self.height),
            seed=self.seed
            )

        return self

    def next_level(self) -> bool:
        """
        Advances the game state to the next level.

        Increments the level ID, expands the maze dimensions based on the
        current level progression, and generates a new, larger maze.

        Returns:
            bool: True if the next level was successfully created.
                  False if the current level is already the maximum level.
        """
        if self.level_id >= self.max_level:
            print(
                "[Warning] Maximum level reached. "
                "There is no next level."
            )
            return False

        self.level_id += 1

        self.width = (
            self.initial_width
            + (self.level_id - 1)
        )
        self.height = (
            self.initial_height
            + (self.level_id - 1) - 1
        )
        self.maze = MazeGenerator(
            size=(self.width, self.height),
            seed=self.seed
        )
        return True

    @property
    def grid(self) -> list[list[int]]:
        """
        Retrieves the 2D array representation of the generated maze.

        Returns:
            list[list[int]]: The matrix containing maze wall and path data,
                             or an empty list if the maze is not initialized.
        """
        return self.maze.maze if self.maze else []
