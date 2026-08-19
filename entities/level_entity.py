from typing import Any

from pydantic import BaseModel, Field, model_validator

from mazegenerator import MazeGenerator


class Level(BaseModel):
    # -------------------------
    # Runtime level information
    # -------------------------
    level_id: int = Field(default=1)

    width: int = Field(default=20)
    height: int = Field(default=20)

    # -------------------------
    # Level configuration
    # -------------------------
    max_level: int = Field(default=10)
    max_time: int = Field(default=90)
    seed: int = Field(default=42)

    # -------------------------
    # Level size configuration
    # -------------------------
    initial_width: int = Field(default=20)
    initial_height: int = Field(default=20)
    size_increment: int = Field(default=5)

    # -------------------------
    # Maze
    # -------------------------
    maze: Any = Field(default=None)

    @model_validator(mode="before")
    @classmethod
    def validate_input(cls, data: Any) -> dict[str, Any]:
        """
        Safely validate Level configuration.

        Invalid or missing values are replaced with safe defaults.
        """

        if not isinstance(data, dict):
            print(
                "[Warning] Level configuration is invalid. "
                "Using default values."
            )
            return {}

        safe_data: dict[str, Any] = {}

        # -------------------------
        # Level ID
        # -------------------------
        level_id = data.get("level_id", 1)

        try:
            level_id = int(level_id)

            if level_id < 1:
                print(
                    "[Warning] Invalid level_id. "
                    "Using default value: 1."
                )
                level_id = 1

        except (ValueError, TypeError):
            print(
                "[Warning] Invalid level_id. "
                "Using default value: 1."
            )
            level_id = 1

        safe_data["level_id"] = level_id

        # -------------------------
        # Maximum level
        # -------------------------
        max_level = data.get("max_level", 10)

        try:
            max_level = int(max_level)

            if max_level < 3:
                print(
                    "[Warning] max_level cannot be less than 3. "
                    "Using minimum value: 3."
                )
                max_level = 3

            elif max_level > 20:
                print(
                    "[Warning] max_level cannot be greater than 20. "
                    "Using maximum value: 20."
                )
                max_level = 20

        except (ValueError, TypeError):
            print(
                "[Warning] Invalid max_level. "
                "Using default value: 10."
            )
            max_level = 10

        safe_data["max_level"] = max_level

        # -------------------------
        # Maximum time
        # -------------------------
        max_time = data.get("level_max_time", 90)

        try:
            max_time = int(max_time)

            if max_time <= 0:
                print(
                    "[Warning] Invalid level_max_time. "
                    "Using default value: 90."
                )
                max_time = 90

        except (ValueError, TypeError):
            print(
                "[Warning] Invalid level_max_time. "
                "Using default value: 90."
            )
            max_time = 90

        safe_data["max_time"] = max_time

        # -------------------------
        # Seed
        # -------------------------
        seed = data.get("seed", 42)

        try:
            seed = int(seed)

            if seed < 0:
                print(
                    "[Warning] Invalid seed. "
                    "Using default value: 42."
                )
                seed = 42

        except (ValueError, TypeError):
            print(
                "[Warning] Invalid seed. "
                "Using default value: 42."
            )
            seed = 42

        safe_data["seed"] = seed

        # -------------------------
        # Initial width
        # -------------------------
        initial_width = data.get("initial_width", 20)

        try:
            initial_width = int(initial_width)

            if initial_width < 3:
                print(
                    "[Warning] Invalid initial_width. "
                    "Using default value: 20."
                )
                initial_width = 20

        except (ValueError, TypeError):
            print(
                "[Warning] Invalid initial_width. "
                "Using default value: 20."
            )
            initial_width = 20

        safe_data["initial_width"] = initial_width

        # -------------------------
        # Initial height
        # -------------------------
        initial_height = data.get("initial_height", 20)

        try:
            initial_height = int(initial_height)

            if initial_height < 3:
                print(
                    "[Warning] Invalid initial_height. "
                    "Using default value: 20."
                )
                initial_height = 20

        except (ValueError, TypeError):
            print(
                "[Warning] Invalid initial_height. "
                "Using default value: 20."
            )
            initial_height = 20

        safe_data["initial_height"] = initial_height

        # -------------------------
        # Size increment
        # -------------------------
        size_increment = data.get("size_increment", 5)

        try:
            size_increment = int(size_increment)

            if size_increment <= 0:
                print(
                    "[Warning] Invalid size_increment. "
                    "Using default value: 5."
                )
                size_increment = 5

        except (ValueError, TypeError):
            print(
                "[Warning] Invalid size_increment. "
                "Using default value: 5."
            )
            size_increment = 5

        safe_data["size_increment"] = size_increment

        return safe_data

    @model_validator(mode="after")
    def validate_game_logic(self) -> "Level":
        """
        Validate relationships between Level attributes
        and initialize the first maze.
        """

        # Level ID cannot be greater than maximum level.
        if self.level_id > self.max_level:
            print(
                "[Warning] level_id is greater than max_level. "
                "Using max_level as current level."
            )
            self.level_id = self.max_level

        # Calculate current level dimensions.
        self.width = (
            self.initial_width
            + (self.level_id - 1) * self.size_increment
        )

        self.height = (
            self.initial_height
            + (self.level_id - 1) * self.size_increment
        )

        # Create the maze for the current level.
        self.maze = MazeGenerator(
            size=(self.width, self.height),
            seed=self.seed
        )

        return self

    def next_level(self) -> bool:
        """
        Move to the next level.

        Returns:
            True  -> next level was successfully created.
            False -> current level is already the maximum level.
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
            + (self.level_id - 1) * self.size_increment
        )

        self.height = (
            self.initial_height
            + (self.level_id - 1) * self.size_increment
        )

        # Generate a new maze for the new level.
        self.maze = MazeGenerator(
            size=(self.width, self.height),
            seed=self.seed
        )

        return True