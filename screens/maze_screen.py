import pygame
from entities import GameEntities
from draw_element.draw_maze import DrawMaze
from draw_element.draw_pacman import DrawPacman
from draw_element.draw_gum import DrawGum

class GameScreen:
    """Handles routing the input and triggering the rendering of the game."""
    
    def __init__(self, screen: pygame.Surface, config: dict):
        self.screen = screen
        self.config = config
        self.entities = GameEntities(**config)

        self.maze_draw = DrawMaze(self.screen)
        self.pacman_draw = DrawPacman(self.screen)
        self.gum_draw = DrawGum(self.screen)
        self._calculate_layout()

    def handle_event(self, event: pygame.event.Event) -> str | None:
        if event.type == pygame.KEYDOWN:


            if event.key in (pygame.K_ESCAPE, pygame.K_p):
                print("pause screen is open")
                return "back_to_menu"

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
                            print("[Cheat] F5 Activated: Pac-Man has infinite lives!")

        return None

    def update(self) -> None:
        pac = self.entities.pacman
        keys = pygame.key.get_pressed()

        self._process_input(pac, keys)
        
        step = self._calculate_speed(pac)
        
        self._update_pacman_position(pac, step)
        
        self._check_gum_collisions(pac)
        self._check_game_state()
        
    
    def _check_game_state(self) -> None:
        if self.entities.pacman.lives <= 0:
            print("Game Over! All lives lost.")
            return "back_to_menu"

        all_gums_eaten = len(self.entities.gums) > 0 and all(gum.is_eaten for gum in self.entities.gums)
        
        if all_gums_eaten:
            print(f"Level {self.entities.level.level_id} Complete! Moving to next level...")
            
            self.entities.level.next_level()
            
            self.entities.gum_reset()
            
            self._calculate_layout()
            
            # د. (مستقبلاً) إعادة الأشباح لنقطة البداية
            # for ghost in self.entities.ghosts:
            #     ghost.reset()

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
                
                print(f"[Action] Gum eaten! Total Points: {pac.total_points}")

                    

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
    
    def draw(self) -> None:
        self.screen.fill((0, 0, 0))

        self.maze_draw.draw(
            self.entities.level, self.cell_size, self.offset_x, self.offset_y
        )
        
        self.gum_draw.draw (
                    self.entities.gums, self.cell_size, self.offset_x, self.offset_y
                )
        
        self.pacman_draw.draw(
            self.entities.pacman, self.cell_size, self.offset_x, self.offset_y
        )