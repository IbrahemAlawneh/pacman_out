from typing import Any, ClassVar
import math
import random


class Ghost:
    """
    Represents a Ghost entity within the game.

    This model manages the ghost's physical coordinates, state variables
    (scared, eaten, frozen, dead), movement speed, and its AI mode for
    pathfinding (Random, BFS, or Euclidean distance).
    """
    OPPOSITE_DIRECTIONS: ClassVar[dict[str, str]] = {
        "UP": "DOWN",
        "DOWN": "UP",
        "LEFT": "RIGHT",
        "RIGHT": "LEFT",
        "NONE": "NONE"
    }

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        spawn_x: int = 0,
        spawn_y: int = 0,
        direction: str = "NONE",
        color: str = "orange",
        is_scared: bool = False,
        is_eaten: bool = False,
        is_frozen: bool = False,
        is_dead: bool = False,
        speed: int = 50,
        ghost_speed: int | None = None,
        mode: int = 0,
        last_grid_x: int = -1,
        last_grid_y: int = -1,
        respawn_timer_start: int = 0,
        chase_algorithm: int = 0,
        **kwargs: Any
    ) -> None:
        self.x = x
        self.y = y
        self.spawn_x = spawn_x
        self.spawn_y = spawn_y
        self.direction = direction
        self.color = color
        self.is_scared = is_scared
        self.is_eaten = is_eaten
        self.is_frozen = is_frozen
        self.is_dead = is_dead

        self.speed = ghost_speed if ghost_speed is not None else speed

        self.mode = mode
        self.last_grid_x = last_grid_x
        self.last_grid_y = last_grid_y
        self.respawn_timer_start = respawn_timer_start
        self.chase_algorithm = chase_algorithm

    def set_mode(self, mode: int) -> None:
        """
        Changes the Ghost's AI mode dynamically during the game.

        Args:
            mode (int): The new mode to apply (0 for Random, 1 for Hard).
        """
        if mode not in (0, 1):
            print(
                "[Warning] Invalid Ghost mode. "
                "Mode was not changed."
            )
            return
        self.mode = mode

    def is_hard(self) -> bool:
        """
        Checks if the ghost is currently operating in Hard mode.

        Returns:
            bool: True if the mode is 1 (Hard), False otherwise.
        """
        return self.mode == 1

    def is_random(self) -> bool:
        """
        Checks if the ghost is currently operating in Random mode.

        Returns:
            bool: True if the mode is 0 (Random), False otherwise.
        """
        return self.mode == 0

    def _get_valid_moves(
            self, grid_x: int, grid_y: int,
            grid: list[list[int]]
    ) -> list[str]:
        """
        Calculates all possible movement directions for the ghost based on
        its current grid position and the maze's wall layout.

        Prevents the ghost from moving in the exact opposite direction of its
        current path unless it reaches a dead end.

        Args:
            grid_x (int): The current X grid coordinate of the ghost.
            grid_y (int): The current Y grid coordinate of the ghost.
            grid (list[list[int]]): The 2D array representing the maze walls.

        Returns:
            list[str]: A list of valid directional strings
            (e.g., ["UP", "RIGHT"]).
        """
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
        """
        Determines the optimal chase direction using the Breadth-First Search
        (BFS) algorithm.

        Args:
            valid_moves (list[str]): Valid directions the ghost can move.
            grid_x (int): The current X grid coordinate of the ghost.
            grid_y (int): The current Y grid coordinate of the ghost.
            pac_x (int): Pacman's current X grid coordinate.
            pac_y (int): Pacman's current Y grid coordinate.
            grid (list[list[int]]): The 2D array representing the maze walls.

        Returns:
            str: The chosen direction minimizing the shortest path to Pacman.
        """
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

            if distance == -1:
                distance = int(math.sqrt(
                    (next_x - pac_x)**2 + (next_y - pac_y)**2
                ))
            if distance < shortest_distance:
                shortest_distance = distance
                best_direction = move
        return best_direction

    def _bfs(
            self, start_x: int, start_y: int, target_x: int,
            target_y: int, grid: list[list[int]]
    ) -> int:
        """
        Executes a Breadth-First Search (BFS) to find the shortest path
        distance between the ghost's next potential step and Pacman's position.

        Args:
            start_x (int): The starting X grid coordinate.
            start_y (int): The starting Y grid coordinate.
            target_x (int): The target X grid coordinate (Pacman).
            target_y (int): The target Y grid coordinate (Pacman).
            grid (list[list[int]]): The 2D array representing the maze walls.

        Returns:
            int: The integer distance (number of steps) to the target,
                or -1 if no valid path is found.
        """
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
        """
        Determines the optimal chase direction using direct Euclidean distance.

        Args:
            valid_moves (list[str]): Valid directions the ghost can move.
            grid_x (int): The current X grid coordinate of the ghost.
            grid_y (int): The current Y grid coordinate of the ghost.
            pac_x (int): Pacman's current X grid coordinate.
            pac_y (int): Pacman's current Y grid coordinate.

        Returns:
            str: The chosen direction minimizing straight-line distance.
        """
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
        """
        Determines the optimal escape direction when the ghost is scared,
        maximizing the Euclidean distance from Pacman.

        Args:
            valid_moves (list[str]): Valid directions the ghost can move.
            grid_x (int): The current X grid coordinate of the ghost.
            grid_y (int): The current Y grid coordinate of the ghost.
            pac_x (int): Pacman's current X grid coordinate.
            pac_y (int): Pacman's current Y grid coordinate.

        Returns:
            str: The chosen direction that maximizes the distance from Pacman.
        """
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
        """
        Evaluates the current state (Scared, Random, or Hard) and decides
        the ghost's next movement direction.

        Args:
            grid_x (int): The current X grid coordinate of the ghost.
            grid_y (int): The current Y grid coordinate of the ghost.
            grid (list[list[int]]): The 2D array representing the maze walls.
            pac_x (int): Pacman's current X grid coordinate.
            pac_y (int): Pacman's current Y grid coordinate.

        Returns:
            str: The finalized direction for the ghost's next move.
        """
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

    def freeze(self) -> None:
        """
        Toggles the freeze state of the ghost.
        When frozen, the ghost will not process movement logic.
        """
        self.is_frozen = not self.is_frozen
        return

    def reset(self, level: Any, cell_size: int) -> None:
        """
        Resets the ghost back to its initial spawn point and default state.
        Typically called when Pacman loses a life or a new level begins.

        Args:
            level (Any): The level entity object containing the maze grid.
            cell_size (int): The calculated pixel size of each grid cell.
        """
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
