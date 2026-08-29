from typing import Any, ClassVar
from pydantic import BaseModel, Field, model_validator
import math
import random


class Ghost(BaseModel):
    x: int = Field(default=0)
    y: int = Field(default=0)
    spawn_x: int = Field(default=0)
    spawn_y: int = Field(default=0)

    direction: str = Field(default="NONE")
    color: str = Field(default="orange")

    is_scared: bool = Field(default=False)
    is_eaten: bool = Field(default=False)
    is_frozen: bool = Field(default=False)
    is_dead: bool = Field(default=False)

    speed: int = Field(default=50)
    mode: int = Field(default=0)

    last_grid_x: int = Field(default=-1)
    last_grid_y: int = Field(default=-1)
    respawn_timer_start: int = Field(default=0)
    chase_algorithm: int = Field(default=0)
    OPPOSITE_DIRECTIONS: ClassVar[dict[str, str]] = {
        "UP": "DOWN",
        "DOWN": "UP",
        "LEFT": "RIGHT",
        "RIGHT": "LEFT",
        "NONE": "NONE"
    }

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

        safe_data: dict[str, Any] = dict(data)

        speed = data.get("ghost_speed", data.get("speed", 40))

        if speed is None or (isinstance(speed, str) and not speed.strip()):
            print("[Warning] Invalid Ghost speed. Using default value: 40.")
            speed = 40
        try:
            speed = int(speed)
            if speed <= 0:
                print(
                    "[Warning] Invalid Ghost speed. Using default value: 40."
                )
                speed = 40
            elif speed > 100:
                print(
                    "[Warning] Invalid Ghost speed. "
                    "Using Max Speed value: 100."
                )
                speed = 100
        except (ValueError, TypeError):
            print("[Warning] Invalid Ghost speed. Using default value: 40.")
            speed = 40

        safe_data["speed"] = speed
        mode = data.get("mode", 0)

        if mode is None or (isinstance(mode, str) and not mode.strip()):
            print(
                "[Warning] Invalid Ghost mode. "
                "Using default mode: 0 (Random)."
            )
            mode = 0
        try:
            mode = int(mode)
            if mode not in (0, 1):
                print(
                    "[Warning] Invalid Ghost mode. "
                    "Using default mode: 0 (Random)."
                )
                mode = 0
        except (ValueError, TypeError):
            print(
                "[Warning] Invalid Ghost mode. "
                "Using default mode: 0 (Random)."
            )
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

    def _get_valid_moves(
            self, grid_x: int, grid_y: int,
            grid: list[list[int]]
    ) -> list[str]:
        valid_moves = []

        try:
            cell = grid[grid_y][grid_x]
        except IndexError:
            return []
        if grid_y > 0 and not (cell & 1):
            valid_moves.append("UP")
        if grid_x < len(grid[0]) - 1 and not (cell & 2):
            valid_moves.append("RIGHT")
        if grid_y < len(grid) - 1 and not (cell & 4):
            valid_moves.append("DOWN")
        if grid_x > 0 and not (cell & 8):
            valid_moves.append("LEFT")

        opposite = self.OPPOSITE_DIRECTIONS.get(self.direction)
        if opposite in valid_moves and len(valid_moves) > 1:
            valid_moves.remove(opposite)
        return valid_moves

    def _get_bfs_chase_direction(
            self, valid_moves: list[str], grid_x: int,
            grid_y: int, pac_x: int, pac_y: int, grid: list[list[int]]
    ) -> str:
        shortest_distance = float('inf')
        best_direction = valid_moves[0]

        for move in valid_moves:
            next_x, next_y = grid_x, grid_y
            if move == "UP":
                next_y -= 1
            elif move == "DOWN":
                next_y += 1
            elif move == "LEFT":
                next_x -= 1
            elif move == "RIGHT":
                next_x += 1
            distance = self._bfs(next_x, next_y, pac_x, pac_y, grid)

            # Fallback to Euclidean if no path is found
            if distance == -1:
                distance = math.sqrt(
                    (next_x - pac_x)**2 + (next_y - pac_y)**2
                )
            if distance < shortest_distance:
                shortest_distance = distance
                best_direction = move
        return best_direction

    def _bfs(
            self, start_x: int, start_y: int, target_x: int,
            target_y: int, grid: list[list[int]]
    ) -> int:
        if start_x == target_x and start_y == target_y:
            return 0

        queue = [(start_x, start_y, 0)]
        visited = set()
        visited.add((start_x, start_y))

        while queue:
            curr_x, curr_y, dist = queue.pop(0)
            if curr_x == target_x and curr_y == target_y:
                return dist
            try:
                cell = grid[curr_y][curr_x]
            except IndexError:
                continue

            neighbors = []
            if curr_y > 0 and not (cell & 1):
                neighbors.append((curr_x, curr_y - 1))
            if curr_x < len(grid[0]) - 1 and not (cell & 2):
                neighbors.append((curr_x + 1, curr_y))
            if curr_y < len(grid) - 1 and not (cell & 4):
                neighbors.append((curr_x, curr_y + 1))
            if curr_x > 0 and not (cell & 8):
                neighbors.append((curr_x - 1, curr_y))

            for nx, ny in neighbors:
                if (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append((nx, ny, dist + 1))
        return -1

    def _get_euclidean_chase_direction(
            self, valid_moves: list[str], grid_x: int, grid_y: int,
            pac_x: int, pac_y: int
    ) -> str:
        shortest_distance = float('inf')
        best_direction = valid_moves[0]

        for move in valid_moves:
            next_x, next_y = grid_x, grid_y
            if move == "UP":
                next_y -= 1
            elif move == "DOWN":
                next_y += 1
            elif move == "LEFT":
                next_x -= 1
            elif move == "RIGHT":
                next_x += 1
            distance = math.sqrt(
                (next_x - pac_x)**2 + (next_y - pac_y)**2
            )
            if distance < shortest_distance:
                shortest_distance = distance
                best_direction = move
        return best_direction

    def _get_escape_direction(
            self, valid_moves: list[str], grid_x: int,
            grid_y: int, pac_x: int, pac_y: int
    ) -> str:
        longest_distance = -1.0
        best_direction = valid_moves[0]

        for move in valid_moves:
            next_x, next_y = grid_x, grid_y
            if move == "UP":
                next_y -= 1
            elif move == "DOWN":
                next_y += 1
            elif move == "LEFT":
                next_x -= 1
            elif move == "RIGHT":
                next_x += 1
            distance = math.sqrt(
                (next_x - pac_x)**2 + (next_y - pac_y)**2
            )

            if distance > longest_distance:
                longest_distance = distance
                best_direction = move
        return best_direction

    def get_next_direction(
            self, grid_x: int, grid_y: int, grid: list[list[int]],
            pac_x: int, pac_y: int
    ) -> str:
        valid_moves = self._get_valid_moves(grid_x, grid_y, grid)

        if not valid_moves:
            return "NONE"
        if self.is_scared:
            return self._get_escape_direction(
                valid_moves, grid_x, grid_y, pac_x, pac_y
            )
        if self.mode == 0:
            return random.choice(valid_moves)

        elif self.mode == 1:
            if self.chase_algorithm == 0:
                return self._get_bfs_chase_direction(
                    valid_moves, grid_x, grid_y, pac_x, pac_y, grid
                )
            else:
                return self._get_euclidean_chase_direction(
                    valid_moves, grid_x, grid_y, pac_x, pac_y
                )
        return random.choice(valid_moves)

    def freeze(self) -> bool:
        self.is_frozen = not self.is_frozen

    def reset(self, level: Any, cell_size: int) -> None:
        max_x = len(level.grid[0]) - 1
        max_y = len(level.grid) - 1

        if self.spawn_x > 0:
            self.spawn_x = max_x
        if self.spawn_y > 0:
            self.spawn_y = max_y

        self.x = self.spawn_x * cell_size
        self.y = self.spawn_y * cell_size

        self.direction = "NONE"
        self.is_scared = False
        self.is_eaten = False
        self.is_frozen = False
        self.is_dead = False
        self.last_grid_x = -1
        self.last_grid_y = -1
        self.respawn_timer_start = 0
