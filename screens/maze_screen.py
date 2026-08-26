import pygame
import math
from entities import GameEntities
from draw_element.draw_maze import DrawMaze
from draw_element.draw_pacman import DrawPacman
from draw_element.draw_gum import DrawGum
from draw_element.draw_ghost import DrawGhost
from .pause_screen import PauseScreen


class GameScreen:
    """Handles routing the input and triggering the rendering of the game."""
    
    def __init__(self, screen: pygame.Surface, config: dict):
        self.screen = screen
        self.config = config
        self.paused = False
        self.entities = GameEntities(**config)

        self.maze_draw = DrawMaze(self.screen)
        self.pacman_draw = DrawPacman(self.screen)
        self.gum_draw = DrawGum(self.screen)
        self.ghosts_draw = DrawGhost(self.screen)
        self.pause_screen = PauseScreen(self.screen)
        self.scared_timer_start = 0
        self._calculate_layout()

    def handle_event(self, event: pygame.event.Event) -> str | None:
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

            elif event.key in (pygame.K_F1, pygame.K_F2, pygame.K_F3, pygame.K_F4, pygame.K_F5):
                cheats = self.config.get("cheats")
                if cheats:
                    enable_all = cheats.get("enable_all", False)

                    if event.key == pygame.K_F1:
                        if enable_all or cheats.get("level_skip", False):
                            print("[Cheat] F1 Activated: Level Skipped!")
                            self.entities.level.next_level()
                            self.entities.gum_reset()
                            self._calculate_layout()

                    elif event.key == pygame.K_F2:
                        if enable_all or cheats.get("ghost_freeze", False):
                            print("[Cheat] F2 Activated: Ghosts Frozen!")

                    elif event.key == pygame.K_F3:
                        if enable_all or cheats.get("extra_life", False):
                            print("[Cheat] F3 Activated: Extra Life Added!")

                    elif event.key == pygame.K_F4:
                        if enable_all or cheats.get("speed_boost", False):
                            print("[Cheat] F4 Activated: Speed Boost!")

                    elif event.key == pygame.K_F5:
                        if enable_all or cheats.get("infinite_lives", False):
                            print(
                                "[Cheat] F5 Activated: "
                                "Pac-Man has infinite lives!"
                            )
        return None

    def update(self) -> None:

        if self.paused:
            return None
        pac = self.entities.pacman
        keys = pygame.key.get_pressed()

        self._process_input(pac, keys)
        
        step = self._calculate_speed(pac)
        
        self._update_pacman_position(pac, step)
        
        if self.scared_timer_start > 0:
            if pygame.time.get_ticks() - self.scared_timer_start > self.entities.scared_duration_ms:
                for ghost in self.entities.ghosts:
                    ghost.is_scared = False
                self.scared_timer_start = 0
        
        self._update_ghosts_position()
        self._check_gum_collisions(pac)
        self._check_ghost_collisions(pac)
        return self._check_game_state()

    def _update_ghosts_position(self) -> None:

        pac = self.entities.pacman
        pac_grid_x = int((pac.x + (self.cell_size // 2)) // self.cell_size)
        pac_grid_y = int((pac.y + (self.cell_size // 2)) // self.cell_size)

        max_physical_speed = self.cell_size / 5.0

        for ghost in self.entities.ghosts:
            if ghost.is_dead:
                if pygame.time.get_ticks() - ghost.respawn_timer_start > self.entities.ghost_respawn_ms:
                    ghost.reset(self.entities.level, self.cell_size)
                continue

            speed_ratio = ghost.speed / 100.0
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
            is_centered = abs(ghost.x - perfect_x) <= tolerance and abs(ghost.y - perfect_y) <= tolerance

            if (is_centered and (ghost.last_grid_x != ghost_grid_x or ghost.last_grid_y != ghost_grid_y)) or ghost.direction == "NONE":
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

            # 5. التنفيذ الأعمى: الحركة الفعلية بالبكسلات بناءً على الاتجاه
            if ghost.direction == "UP":
                ghost.y -= step
            elif ghost.direction == "DOWN":
                ghost.y += step
            elif ghost.direction == "LEFT":
                ghost.x -= step
            elif ghost.direction == "RIGHT":
                ghost.x += step

    def _check_ghost_collisions(self, pac) -> None:
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
                    ghost.x = -1000  # Hide it temporarily
                    ghost.y = -1000
                    ghost.respawn_timer_start = pygame.time.get_ticks()
                    pac.total_points += pac.points_per_ghost
                    print(f"[Action] Ghost eaten! Total Points: {pac.total_points}")
                else:
                    pac.lives -= 1
                    print(f"[Action] Pacman died! Lives remaining: {pac.lives}")
                    self._reset_positions()
                    return

    def _reset_positions(self) -> None:
        self._calculate_layout()
        for ghost in self.entities.ghosts:
            ghost.reset(self.entities.level, self.cell_size)

    def _check_game_state(self) -> None | str:
        if self.entities.pacman.lives <= 0:
            return "back_to_menu"

        all_gums_eaten = len(self.entities.gums) > 0 and all(gum.is_eaten for gum in self.entities.gums)
        if all_gums_eaten:
            print(f"Level {self.entities.level.level_id} Complete! Moving to next level...")

            self.entities.level.next_level()
            self.entities.gum_reset()
            self._calculate_layout()
            for ghost in self.entities.ghosts:
                ghost.reset(self.entities.level, self.cell_size)
        return None

    def _process_input(self, pac, keys) -> None:
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            pac.next_direction = "UP"
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            pac.next_direction = "DOWN"
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            pac.next_direction = "LEFT"
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            pac.next_direction = "RIGHT"

    def _calculate_speed(self, pac) -> int:
        max_physical_speed = self.cell_size / 5.0
        speed_ratio = pac.pacman_speed / 100.0 
        return max(1, int(max_physical_speed * speed_ratio))

    def _update_pacman_position(self, pac, step: int) -> None:
        center_x = pac.x + (self.cell_size // 2)
        center_y = pac.y + (self.cell_size // 2)
        grid_x = int(center_x // self.cell_size)
        grid_y = int(center_y // self.cell_size)

        perfect_x = grid_x * self.cell_size
        perfect_y = grid_y * self.cell_size

        if pac.next_direction != "NONE" and pac.next_direction != pac.direction:
            if self._is_path_open(grid_x, grid_y, pac.next_direction):
                tolerance = step * 2 
                if abs(pac.x - perfect_x) <= tolerance and abs(pac.y - perfect_y) <= tolerance:
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
            if pac.direction == "UP": pac.y -= step
            elif pac.direction == "DOWN": pac.y += step
            elif pac.direction == "LEFT": pac.x -= step
            elif pac.direction == "RIGHT": pac.x += step

    def _check_gum_collisions(self, pac) -> None:
        pac_grid_x = int((pac.x + (self.cell_size // 2)) // self.cell_size)
        pac_grid_y = int((pac.y + (self.cell_size // 2)) // self.cell_size)

        for gum in self.entities.gums:
            if not gum.is_eaten and gum.grid_x == pac_grid_x and gum.grid_y == pac_grid_y:

                gum.is_eaten = True
                pac.total_points += gum.points

                if gum.is_super:
                    self.scared_timer_start = pygame.time.get_ticks()
                    for ghost in self.entities.ghosts:
                        if not ghost.is_dead:
                            ghost.is_scared = True

    def _is_path_open(self, grid_x: int, grid_y: int, direction: str) -> bool:
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

    def _calculate_layout(self) -> None:
        grid = self.entities.level.grid
        grid_width = len(grid[0])
        grid_height = len(grid)

        MAX_W, MAX_H = 1000, 700
        cell_w = MAX_W // grid_width
        cell_h = MAX_H // grid_height
        
        self.cell_size = min(cell_w, cell_h, 40) 

        maze_width_px = grid_width * self.cell_size
        maze_height_px = grid_height * self.cell_size

        self.offset_x = (self.screen.get_width() - maze_width_px) // 2
        self.offset_y = (self.screen.get_height() - maze_height_px) // 2

        center_grid_x = grid_width // 2
        center_grid_y = grid_height // 2
        
        while grid[center_grid_y][center_grid_x] == 15:
                center_grid_x -= 1
                center_grid_y -= 1

        pac = self.entities.pacman
        pac.x = center_grid_x * self.cell_size
        pac.y = center_grid_y * self.cell_size

            
    
        pac.direction = "NONE"
        pac.next_direction = "NONE"
        
        for ghost in self.entities.ghosts:
            # Fix spawn position to not be inside a wall
            sx, sy = ghost.spawn_x, ghost.spawn_y
            while sx >= 0 and sy >= 0 and sx < grid_width and sy < grid_height and grid[sy][sx] == 15:
                if sx > grid_width // 2: sx -= 1
                elif sx < grid_width // 2: sx += 1
                if sy > grid_height // 2: sy -= 1
                elif sy < grid_height // 2: sy += 1
            ghost.spawn_x = sx
            ghost.spawn_y = sy
            ghost.x = ghost.spawn_x * self.cell_size
            ghost.y = ghost.spawn_y * self.cell_size
    
    def draw(self) -> None:
        self.screen.fill((0, 0, 0))

        self.maze_draw.draw(
            self.entities.level, self.cell_size,
            self.offset_x, self.offset_y
        )

        self.gum_draw.draw (
            self.entities.gums, self.cell_size,
            self.offset_x, self.offset_y
        )
        
        self.ghosts_draw.draw (
            self.entities.ghosts, self.cell_size,
            self.offset_x, self.offset_y
        )

        self.pacman_draw.draw(
            self.entities.pacman, self.cell_size,
            self.offset_x, self.offset_y
        )

        if self.paused:
            self.pause_screen.draw()
