import pygame
import math
from typing import Any
from entities import GameEntities
from draw_element.draw_maze import DrawMaze
from draw_element.draw_pacman import DrawPacman
from draw_element.draw_gum import DrawGum
from draw_element.draw_ghost import DrawGhost
from draw_element.draw_HUD import DrawHUD
from draw_element.theme_manager import GAME_THEMES
from .pause_screen import PauseScreen
from .game_result import GameResult


class GameScreen:
    """Handles routing the input and triggering the rendering of the game."""

    def __init__(self, screen: pygame.Surface, config: dict):
        """Build all game entities, drawers, and initial state."""
        self.screen = screen
        self.config = config
        self.paused = False
        self.high_score = config.get("highscore_filename", "high_score.json")
        self.entities = GameEntities(**config)
        self.last_timer_update = pygame.time.get_ticks()
        self.maze_draw = DrawMaze(self.screen)
        self.pacman_draw = DrawPacman(self.screen)
        self.gum_draw = DrawGum(self.screen)
        self.ghosts_draw = DrawGhost(self.screen)
        self.HUD_draw = DrawHUD("assets/fonts/PressStart2P-Regular.ttf")
        self.pause_screen = PauseScreen(self.screen)
        self.game_result: GameResult | None = None
        self.scared_timer_start = 0
        self.init_time = self.entities.level.max_time
        self.all_gums_eaten = False
        self.speed_on = False
        self.is_infinite = False
        self._calculate_layout()

    def _load_image(
                self, filename: str, scale_to_screen: bool = False
    ) -> pygame.Surface | None:
        """Load an image file, optionally scaled to fill the screen."""
        filepath = filename
        try:
            img = pygame.image.load(str(filepath)).convert_alpha()
            if scale_to_screen:
                img = pygame.transform.scale(
                    img, self.screen.get_size()
                )
            return img
        except Exception as e:
            print(f"[Warning] Could not load {filename}: {e}")
            return None

    def handle_event(self, event: pygame.event.Event) -> str | None:
        """Route input to pause, cheats, or the active result screen."""
        if self.game_result is not None:
            return self.game_result.handle_event(event)

        if self.paused:
            action = self.pause_screen.handle_event(event)
            if action == "resume":
                self.paused = False
            elif action in ("back_to_menu", "quit"):
                return action
            return None

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_p):
                self.paused = True
                self.pause_screen.open()
                return None
            elif event.key in (
                pygame.K_F1, pygame.K_F2, pygame.K_F3,
                pygame.K_F4, pygame.K_F5
            ):
                cheats = self.config.get("cheats")
                if cheats:
                    enable_all = cheats.get("enable_all", False)
                    if event.key == pygame.K_F1:
                        if enable_all or cheats.get("level_skip", False):
                            self.skip_level()
                    elif event.key == pygame.K_F2:
                        if enable_all or cheats.get("ghost_freeze", False):
                            self._cheat_freeze()
                    elif event.key == pygame.K_F3:
                        if enable_all or cheats.get("extra_life", False):
                            self.entities.pacman.lives += 1
                    elif event.key == pygame.K_F4:
                        if enable_all or cheats.get("speed_boost", False):
                            if not self.speed_on:
                                self.entities.pacman.pacman_speed += 20
                                self.speed_on = True
                            else:
                                self.entities.pacman.pacman_speed -= 20
                                self.speed_on = False
                    elif event.key == pygame.K_F5:
                        if enable_all or cheats.get("infinite_lives", False):
                            if not self.is_infinite:
                                self.is_infinite = True
                            else:
                                self.is_infinite = False
        return None

    def update(self) -> str | None:
        """Advance gameplay one frame, or update the result screen."""
        if self.game_result is not None:
            result = self.game_result.update()
            if result == "next_level":
                self.skip_level()
                for ghost in self.entities.ghosts:
                    ghost.reset(self.entities.level, self.cell_size)
                self.game_result = None
            return None

        if self.paused:
            return None
        pac = self.entities.pacman
        keys = pygame.key.get_pressed()

        self._process_input(pac, keys)
        step = self._calculate_speed(pac)
        self._update_pacman_position(pac, step)

        if self.scared_timer_start > 0:
            if (
                pygame.time.get_ticks() - self.scared_timer_start >
                self.entities.scared_duration_ms
            ):
                for ghost in self.entities.ghosts:
                    ghost.is_scared = False
                self.scared_timer_start = 0
        self._update_ghosts_position()
        self._check_gum_collisions(pac)
        self._check_ghost_collisions(pac)
        self._update_level_timer()
        return self._check_game_state()

    def _cheat_freeze(self) -> None:
        """Freeze every ghost in place via the ghost-freeze cheat."""
        for g in self.entities.ghosts:
            g.freeze()
        return

    def _update_ghosts_position(self) -> None:
        """Move each ghost toward its next grid direction."""
        pac = self.entities.pacman
        pac_grid_x = int((pac.x + (self.cell_size // 2)) // self.cell_size)
        pac_grid_y = int((pac.y + (self.cell_size // 2)) // self.cell_size)

        max_physical_speed = self.cell_size / 8.0
        for ghost in self.entities.ghosts:
            if ghost.is_frozen:
                return
            if ghost.is_dead:
                if (
                    pygame.time.get_ticks() - ghost.respawn_timer_start >
                    self.entities.ghost_respawn_ms
                ):
                    ghost.reset(self.entities.level, self.cell_size)
                continue

            speed_ratio = (ghost.speed / 100.0) * 0.85
            if ghost.is_scared:
                speed_ratio *= 0.5
            step = max(1, int(max_physical_speed * speed_ratio))

            center_x = ghost.x + (self.cell_size // 2)
            center_y = ghost.y + (self.cell_size // 2)
            ghost_grid_x = int(center_x // self.cell_size)
            ghost_grid_y = int(center_y // self.cell_size)

            perfect_x = ghost_grid_x * self.cell_size
            perfect_y = ghost_grid_y * self.cell_size
            tolerance = step
            is_centered = abs(
                ghost.x - perfect_x
            ) <= tolerance and abs(ghost.y - perfect_y) <= tolerance
            if (
                is_centered and (
                    ghost.last_grid_x != ghost_grid_x or
                    ghost.last_grid_y != ghost_grid_y
                )
            ) or ghost.direction == "NONE":
                ghost.x = perfect_x
                ghost.y = perfect_y
                ghost.last_grid_x = ghost_grid_x
                ghost.last_grid_y = ghost_grid_y

                ghost.direction = ghost.get_next_direction(
                    ghost_grid_x,
                    ghost_grid_y,
                    self.entities.level.grid,
                    pac_grid_x,
                    pac_grid_y
                )
            if ghost.direction == "UP":
                ghost.y -= step
            elif ghost.direction == "DOWN":
                ghost.y += step
            elif ghost.direction == "LEFT":
                ghost.x -= step
            elif ghost.direction == "RIGHT":
                ghost.x += step

    def _check_ghost_collisions(self, pac: Any) -> None:
        """Handle Pac-Man touching a ghost: eat it, die, or ignore it."""
        if pac.lives <= 0:
            return
        for ghost in self.entities.ghosts:
            if ghost.is_dead:
                continue
            distance = math.sqrt((pac.x - ghost.x)**2 + (pac.y - ghost.y)**2)
            if distance < self.cell_size * 0.8:
                if ghost.is_scared:
                    ghost.is_dead = True
                    ghost.is_scared = False
                    ghost.x = -1000
                    ghost.y = -1000
                    ghost.respawn_timer_start = pygame.time.get_ticks()
                    pac.total_points += pac.points_per_ghost
                elif self.is_infinite:
                    return
                else:
                    pac.lives -= 1
                    self.entities.level_max_time = self.init_time + (
                        (self.entities.level.level_id - 1) * 10
                    )
                    self._reset_positions()
                    return

    def _reset_positions(self) -> None:
        """Reset Pac-Man and every ghost back to their spawn points."""
        self.entities.pacman.reset_position(self.cell_size)
        for ghost in self.entities.ghosts:
            ghost.reset(self.entities.level, self.cell_size)

    def _new_level_increase(self) -> None:
        """Raise speeds and ghost difficulty when a new level starts."""
        if self.entities.pacman.pacman_speed < 65:
            self.entities.pacman.pacman_speed = min(
                65, self.entities.pacman.pacman_speed + 2
            )
        for ghost in self.entities.ghosts:
            if getattr(ghost, 'speed', 40) < 63:
                ghost.speed = min(63, ghost.speed + 2)
        hard_count = sum(
            1 for g in self.entities.ghosts if g.mode == 1 and
            g.chase_algorithm == 0
        )
        for ghost in self.entities.ghosts:
            is_easy = (ghost.mode == 0)
            is_medium = (ghost.mode == 1 and ghost.chase_algorithm == 1)
            if is_easy:
                ghost.mode = 1
                ghost.chase_algorithm = 1
                break
            elif is_medium:
                if hard_count < 2:
                    ghost.mode = 1
                    ghost.chase_algorithm = 0
                    break

    def _check_game_state(self) -> None | str:
        """Trigger the result screen on game over, win, or level clear."""
        if self.entities.pacman.lives <= 0:
            self.game_result = GameResult(
                self.screen, won=False,
                score=self.entities.pacman.total_points,
                file_name=self.high_score
            )
            return None

        self.all_gums_eaten = len(
            self.entities.gums
        ) > 0 and all(gum.is_eaten for gum in self.entities.gums)
        if self.all_gums_eaten:
            if (
                self.entities.level.level_id >=
                self.entities.level.max_level
            ):
                self.game_result = GameResult(
                    self.screen, won=True,
                    score=self.entities.pacman.total_points,
                    file_name=self.high_score
                )
            else:
                self.game_result = GameResult(
                    self.screen, won=False, score=0,
                    next_level=self.entities.level.level_id + 1,
                    file_name=self.high_score
                )
        return None

    def _process_input(self, pac: Any, keys: Any) -> None:
        """Queue Pac-Man's next direction from the pressed movement keys."""
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            pac.next_direction = "UP"
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            pac.next_direction = "DOWN"
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            pac.next_direction = "LEFT"
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            pac.next_direction = "RIGHT"

    def _calculate_speed(self, pac: Any) -> int:
        """Convert Pac-Man's speed stat into a per-frame pixel step."""
        max_physical_speed = self.cell_size / 6.5
        speed_ratio = pac.pacman_speed / 100.0
        return max(1, int(max_physical_speed * speed_ratio))

    def _update_pacman_position(self, pac: Any, step: int) -> None:
        """Move Pac-Man forward, turning and stopping at walls."""
        center_x = pac.x + (self.cell_size // 2)
        center_y = pac.y + (self.cell_size // 2)
        grid_x = int(center_x // self.cell_size)
        grid_y = int(center_y // self.cell_size)

        perfect_x = grid_x * self.cell_size
        perfect_y = grid_y * self.cell_size
        if (
            pac.next_direction != "NONE" and
            pac.next_direction != pac.direction
        ):
            if self._is_path_open(grid_x, grid_y, pac.next_direction):
                tolerance = step * 2
                if abs(
                    pac.x - perfect_x
                ) <= tolerance and abs(pac.y - perfect_y) <= tolerance:
                    pac.x = perfect_x
                    pac.y = perfect_y
                    pac.direction = pac.next_direction
                    pac.next_direction = "NONE"
        can_move = True
        if not self._is_path_open(grid_x, grid_y, pac.direction):
            if pac.direction == "UP" and pac.y <= perfect_y:
                pac.y = perfect_y
                can_move = False
            elif pac.direction == "DOWN" and pac.y >= perfect_y:
                pac.y = perfect_y
                can_move = False
            elif pac.direction == "LEFT" and pac.x <= perfect_x:
                pac.x = perfect_x
                can_move = False
            elif pac.direction == "RIGHT" and pac.x >= perfect_x:
                pac.x = perfect_x
                can_move = False

        if can_move and pac.direction != "NONE":
            if pac.direction == "UP":
                pac.y -= step
            elif pac.direction == "DOWN":
                pac.y += step
            elif pac.direction == "LEFT":
                pac.x -= step
            elif pac.direction == "RIGHT":
                pac.x += step

    def _check_gum_collisions(self, pac: Any) -> None:
        """Mark eaten gums, award points, and trigger scared mode."""
        pac_grid_x = int(
            (pac.x + (self.cell_size // 2)) // self.cell_size
        )
        pac_grid_y = int(
            (pac.y + (self.cell_size // 2)) // self.cell_size
        )
        for gum in self.entities.gums:
            if (
                not gum.is_eaten and gum.grid_x == pac_grid_x and
                gum.grid_y == pac_grid_y
            ):
                gum.is_eaten = True
                pac.total_points += gum.points
                if gum.is_super:
                    self.scared_timer_start = pygame.time.get_ticks()
                    for ghost in self.entities.ghosts:
                        if not ghost.is_dead:
                            ghost.is_scared = True

    def _is_path_open(self, grid_x: int, grid_y: int, direction: str) -> bool:
        """Check whether the given direction is open at a grid cell."""
        try:
            cell = self.entities.level.grid[grid_y][grid_x]
        except IndexError:
            return False

        if direction == "UP":
            return (cell & 1) == 0
        elif direction == "RIGHT":
            return (cell & 2) == 0
        elif direction == "DOWN":
            return (cell & 4) == 0
        elif direction == "LEFT":
            return (cell & 8) == 0
        return False

    def skip_level(self) -> None:
        """Advance to the next level and reset gums, layout, and entities."""
        self.entities.level.next_level()
        self.entities.gum_reset()
        self._new_level_increase()
        self._calculate_layout()
        self._reset_positions()
        self.entities.level_max_time = self.init_time + (
            (self.entities.level.level_id - 1) * 10
        )

    def _load_level_theme(self) -> None:
        """Load the background image and music for the current level."""
        theme_index = (
            self.entities.level.level_id - 1
        ) % len(GAME_THEMES)
        current_theme = GAME_THEMES[theme_index]

        self.theme_name = current_theme.name
        self.bk_image = self._load_image(current_theme.bg_path, True)
        pygame.mixer.music.load(current_theme.music_path)
        pygame.mixer.music.play(-1)

    def _update_level_timer(self) -> None:
        """Count down the level timer and penalize the player on timeout."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_timer_update >= 1000:
            if self.entities.level_max_time > 0:
                self.entities.level_max_time -= 1

            self.last_timer_update = current_time
        if self.entities.level_max_time <= 0:
            self.entities.pacman.lives -= 1
            self.entities.level_max_time = self.init_time + (
                (self.entities.level.level_id - 1) * 10
            )
            self._reset_positions()

    def _calculate_layout(self) -> None:
        """Compute cell size, offsets, and spawn positions for the maze."""
        grid = self.entities.level.grid
        grid_width = len(grid[0])
        grid_height = len(grid)

        MAX_W, MAX_H = 860, 600
        cell_w = MAX_W // grid_width
        cell_h = MAX_H // grid_height

        self.cell_size = min(cell_w, cell_h, 60)

        maze_width_px = grid_width * self.cell_size
        maze_height_px = grid_height * self.cell_size

        MARGIN_RIGHT = 40
        MARGIN_BOTTOM = 60

        self.offset_x = self.screen.get_width() - maze_width_px - MARGIN_RIGHT
        self.offset_y = (
            self.screen.get_height() - maze_height_px - MARGIN_BOTTOM
        )
        center_grid_x = grid_width // 2
        center_grid_y = grid_height // 2

        while grid[center_grid_y][center_grid_x] == 15:
            center_grid_x -= 1
            center_grid_y -= 1

        self.entities.pacman.center = center_grid_x, center_grid_y

        pac = self.entities.pacman
        pac.x = center_grid_x * self.cell_size
        pac.y = center_grid_y * self.cell_size

        pac.direction = "NONE"
        pac.next_direction = "NONE"

        for ghost in self.entities.ghosts:
            sx, sy = ghost.spawn_x, ghost.spawn_y
            while (
                sx >= 0 and sy >= 0 and sx < grid_width and
                sy < grid_height and grid[sy][sx] == 15
            ):
                if sx > grid_width // 2:
                    sx -= 1
                elif sx < grid_width // 2:
                    sx += 1
                if sy > grid_height // 2:
                    sy -= 1
                elif sy < grid_height // 2:
                    sy += 1
            ghost.spawn_x = sx
            ghost.spawn_y = sy
            ghost.x = ghost.spawn_x * self.cell_size
            ghost.y = ghost.spawn_y * self.cell_size
        self._load_level_theme()

    def draw(self) -> None:
        """Draw the maze, entities, HUD, and any active overlay screen."""
        self.screen.blit(self.bk_image, (0, 0))
        self.maze_draw.draw(
            self.entities.level, self.cell_size,
            self.offset_x, self.offset_y,
            self.theme_name
            )
        self.gum_draw.draw(
            self.entities.gums, self.cell_size,
            self.offset_x, self.offset_y
        )
        self.ghosts_draw.draw(
            self.entities.ghosts, self.cell_size,
            self.offset_x, self.offset_y
        )
        self.pacman_draw.draw(
            self.entities.pacman, self.cell_size,
            self.offset_x, self.offset_y
        )
        self.HUD_draw.draw(
            self.screen, self.entities.pacman.total_points,
            self.entities.level.level_id,
            self.entities.pacman.lives,
            self.entities.level_max_time,
            self.entities.ghosts[0].is_frozen,
            self.is_infinite,
            self.speed_on
            )
        if self.game_result is not None:
            self.game_result.draw()
        elif self.paused:
            self.pause_screen.draw()
