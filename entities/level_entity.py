from typing import Any
from mazegenerator import MazeGenerator


class Level:
    """
    Represents the game level and maze configuration.

    This model manages the current level state, maze dimensions, time
    limits, and handles the generation of new mazes as the player
    progresses through the game.
    """
    def __init__(
        self,
        level_id: int = 1,
        width: int = 20,
        height: int = 20,
        max_level: int = 10,
        max_time: int = 90,
        seed: int = -1,
        **kwargs: Any
    ) -> None:
        self.level_id = level_id
        self.max_level = max_level
        self.max_time = max_time
        self.seed = seed
        self.width = width
        self.height = height

        self.initial_width = self.width
        self.initial_height = self.height
        self.size_increment = 1

        self.maze = MazeGenerator(
            size=(self.width, self.height),
            seed=self.seed
        )

    def next_level(self) -> bool:
        """
        Advances the game state to the next level.

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
            list[list[int]]: The matrix containing maze wall and path data.
        """
        return self.maze.maze if self.maze else []
