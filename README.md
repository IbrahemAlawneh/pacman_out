*This activity has been created as part of the 42 curriculum by ialalawn, abani-am.*

# Pac-Man

## Description

This project is a Python implementation of the classic Pac-Man game, developed as part of the 42 curriculum.

The goal of the activity is to build a complete, playable Pac-Man game using object-oriented programming, a graphical library compatible with the project's requirements, an external A-Maze-ing maze generator, a configurable game system, and a persistent highscore system.

The game follows the classic Pac-Man concept:

- The player controls Pac-Man through a maze.
- Pac-Man moves through corridors and cannot pass through walls.
- Pac-Gums are distributed throughout the maze.
- Super Pac-Gums are placed in the four corners.
- Four ghosts move autonomously through the maze.
- Ghosts can chase the player and can become edible after eating a Super Pac-Gum.
- The player starts with three lives.
- Completing all Pac-Gums completes the current level.
- Completing all configured levels wins the game.
- Losing all lives ends the game.
- The final score can be saved to the persistent highscore system.

The project is designed around a modular and reusable object-oriented architecture so that game entities, configuration, level generation, scoring, and game logic remain separated.

The activity also requires a main menu, gameplay view, game-over/victory handling, a cheat mode for peer review, and deployment of a playable build to a public gaming platform.

---

# Instructions

## Requirements

The project requires:

- Python 3
- Pydantic
- The assigned A-Maze-ing package
- The graphical library used by the final implementation
- flake8
- mypy

## Running the Game

```bash
python3 pac-man.py config.json
```

The program accepts exactly one configuration file argument. The filename can be changed, as long as a valid JSON configuration file is supplied.

The game handles configuration problems without displaying an unhandled Python traceback. Missing files, invalid values, missing keys, and other expected configuration problems result in warnings and safe defaults instead of crashing.

Common commands:

```bash
make install
make run
make debug
make clean
make lint
```

---

# Project Structure

```text
.
├── pac-man.py
├── config.json
├── pyproject.toml
├── Makefile
├── .gitignore
├── README.md
│
├── entities/
│   ├── __init__.py
│   ├── game_entities.py
│   ├── pacman.py
│   └── ghost.py
│
├── configuration_files/
│   ├── __init__.py
│   ├── config_parser.py
│   └── level.py
│
├── libs/
│   └── mazegenerator-2.1.0-py3-none-any.whl
│
├── assets/
│   └── ...
│
└── packaging/
    └── publish.sh
```

Additional modules will be added as the graphical interface, game loop, highscore system, cheat mode, and other game systems are implemented.

---

# Configuration

The game uses a `config.json` file with extended features:

- **Comments:** Supports `#`, `//`, and `/* */` (comments inside strings are preserved).
- **Flexibility:** Keys are case-insensitive and unknown keys are ignored.
- **Failsafe:** Missing or invalid keys are automatically clamped to safe defaults. The game will never crash due to a bad config.

## Available Keys & Defaults

| Key | Default | Description |
|---|---|---|
| `highscore_filename` | `"highscores.json"` | Path to save top scores |
| `seed` | `42` | Maze generation seed |
| `level_max_time` | `90` | Level time limit (seconds) |
| `max_level` | `10` | Total levels (clamped 3–20) |
| `lives` | `3` | Starting lives (min: 1) |
| `points_per_pacgum` | `10` | Points per Pac-Gum |
| `points_per_super_pacgum` | `50` | Points per Super Pac-Gum (must be > pacgum) |
| `points_per_ghost` | `200` | Points per eaten ghost |
| `pacman_speed` | `50` | Player speed (must be ≥ ghost_speed) |
| `ghost_speed` | `50` | Ghosts' speed |
| `ghosts_mode` | `1` | 4-bit mask (1–15) setting Hard/Chase mode |

## Example

```json
{
    # General config
    "highscore_filename": "highscores.json",
    "seed": 42,
    "level_max_time": 90,
    "max_level": 10,

    // Player config
    "lives": 3,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200,
    "pacman_speed": 50,

    /* Ghost config */
    "ghost_speed": 50,
    "ghosts_mode": 1
}
```

---

# Maze Generation

The project uses the assigned external A-Maze-ing package for maze generation.

```python
from mazegenerator import MazeGenerator
```

The assigned package is used as provided and is not modified by the project. The Level entity creates a maze using the MazeGenerator, which provides:

```python
maze.maze
maze.maze_entry
maze.maze_exit
maze.shortest_path
```

The maze representation is `list[list[int]]`. The maze generator is used with `PERFECT = False`, as required by the activity. If the external maze generator fails, the game handles the situation without an unhandled crash.

---

# Highscore

The game requires a persistent highscore system, controlled by `highscore_filename` (default `"highscores.json"`).

The highscore system:

- Loads highscores at game start and saves them at game end.
- Keeps the Top 10 scores (player names + scores).
- Accepts player names up to 10 characters, alphanumeric and spaces only. Empty names fall back to `unknown`.
- Stores non-negative integer scores.
- Handles missing or invalid highscore files without crashing.
- Displays the Top 10 highscores in the main menu.

At the end of a game (win or lose), the final score is displayed and the player can enter a name to save it.

---

# Game Rules

Pac-Man moves through corridors in 4 directions and loses a life on ghost contact (starts with `lives`, default 3). Eating a Pac-Gum awards `points_per_pacgum`; a Super Pac-Gum (placed in the 4 maze corners) awards `points_per_super_pacgum` and makes all ghosts edible briefly, worth `points_per_ghost` each. Completing all Pac-Gums finishes the level; completing all levels wins the game. Score never decreases.

Ghosts (4 total) move autonomously from their maze-corner spawn, operating in either Random or Hard/Chase mode (see [`ghosts_mode`](#configuration)), and respawn at their corner after being eaten.

---

# User Interface

| Screen | Contents |
|---|---|
| **Main Menu** | Start Game, View Highscores, Instructions, Exit |
| **In-Game HUD** | Score, lives, current level, remaining time |
| **Pause Menu** | Resume, Return to Main Menu |
| **Game Over / Victory** | Final score, name entry for highscore, (Victory adds a congratulatory message) |

The game's overall flow moves from the Main Menu through each level to Victory or Game Over, then back to the Main Menu after the highscore is saved.

---

# Cheat Mode

A cheat mode is required for peer review, to make it easier for reviewers to test different game features.

Planned cheat features include:

- Invincibility
- Level skip
- Ghost freeze
- Extra lives
- Increased player speed

---

# Implementation

The project uses object-oriented programming with Pydantic-based entities to keep game state, configuration, and validation cleanly separated.

```text
                         pac-man.py
                             |
                             v
                       Configuration
                             |
                             v
                      GameEntities
                             |
             +---------------+---------------+
             |               |               |
             v               v               v
          Pacman          Ghost x 4        Level
                                             |
                                             v
                                      MazeGenerator
```

- **Pacman** — player state (lives, score, name) and speed/points config.
- **Ghost** — a single class instantiated four times; each ghost holds its own `speed` and `mode` (`0 = Random`, `1 = Hard/Chase`), set initially from the `ghosts_mode` bitmask.
- **Level** — current level state (`level_id`, `width`, `height`, `maze`); `next_level()` increments dimensions and regenerates the maze via the assigned `MazeGenerator`.
- **GameEntities** — top-level container that builds all entities from the loaded configuration.

Validation follows Pydantic's `model_validator` (`before`/`after`) to clamp invalid values to safe defaults instead of raising exceptions — see [Configuration](#configuration) and [Error Handling Philosophy](#error-handling-philosophy).

---

# Error Handling Philosophy

The project follows a "no crash" philosophy for expected runtime and configuration failures.

Expected failures are handled using try/except blocks. Clear warnings are displayed instead of Python tracebacks. Files are opened using context managers:

```python
with open(...) as file:
    ...
```

This ensures resources are properly closed. The project uses type hints throughout the codebase and aims to comply with PEP 8, Flake8, Mypy, and PEP 257 docstrings.

---

## General Software Architecture

The project follows a mature, state-driven Object-Oriented Programming (OOP) architecture. It implements a clear separation of concerns (similar to the MVC pattern), cleanly decoupling game logic, rendering algorithms, UI state management, and data persistence into highly cohesive modules.

                             pac-man.py (Main Entry)
                                       |
                                       v
                                ScreenManager
                                       |
         +-----------------------------+-----------------------------+
         |                             |                             |
         v                             v                             v
    UI/Menu Screens               MazeScreen                Configuration & IO
  (Main, Settings,             (Core Game Loop)            (configuration_files/)
   Results, Pause)                     |
                                       |
         +-----------------------------+-----------------------------+
         |                                                           |
         v                                                           v
   Game Entities (Logic)                                 Draw Elements (Rendering)
     (entities/)                                             (draw_element/)
         |                                                           |
         +-- GameEntity (Rules/State)                                +-- ThemeManager (Audio/Visuals)
         +-- PacmanEntity (Physics)                                  +-- DrawMaze (Surface Caching)
         +-- GhostEntity (AI Algorithms)                             +-- DrawPacman / DrawGhost
         +-- LevelEntity -> [libs/mazegenerator]                     +-- DrawHUD (UI/Cheat Modes)


### Core Systems Breakdown

*   **Screens (`screens/`):** Acts as the central state machine. `screen_manager.py` handles seamless transitions and event routing between UI menus, settings, and the core gameplay loop (`maze_screen.py`), ensuring each game state is isolated and memory-efficient.
*   **Game Entities (`entities/`):** The "Brain" of the game. It contains pure logical data models, handling grid-based physics, collision detection, and Ghost AI (implementing escalating difficulty via BFS and Euclidean algorithms). It interacts with the external `mazegenerator` wheel through `level_entity.py`.
*   **Draw Elements (`draw_element/`):** A dedicated rendering engine completely decoupled from the game logic. It is responsible for `pygame` blitting, sprite animation frames, surface caching for the maze, and rendering the dynamic HUD.
*   **Theme & Asset Management (`assets/` & `theme_manager.py`):** A dynamic system that manages scaling, caching, and swapping of visual themes (Classic, Neon, Desert) alongside a smart audio state tracker that prevents music interruption during UI navigation.
*   **Configuration & Data (`configuration_files/`):** Manages persistent application states, ensuring safe data parsing via validation scripts and handling file I/O for the dynamic Top 10 Highscore JSON system.

---

# Project Management

Developed collaboratively by ialalawn and abani-am. See [`project_management/`](./project_management/) for the timeline, task tracking, and risk analysis.

---

# Deployment

The game is packaged and published via [Itch.io](https://itch.io) using the `butler` CLI tool.

- **Packaging script:** `packaging/publish.sh` (at the project root) builds a clean distributable folder and publishes it in one step.
- **Publishing:**
  ```bash
  butler push packaging/build/ Ahmadalameri-0/pacman:linux
  ```
- **Status:** Published as a free, unlisted build for peer-review access.
- **In-package instructions:** Controls, config usage, and cheat mode are documented in `packaging/build/README.txt`, generated automatically by the publish script.

---

# Resources

- **42 Subject** — primary reference for all requirements.
- **A-Maze-ing Package** — assigned external maze generator (see [Maze Generation](#maze-generation)).
- **[Python Documentation](https://docs.python.org/3/)** — OOP, file handling, JSON, type hints, exceptions.
- **[Pydantic Documentation](https://docs.pydantic.dev/)** — `BaseModel`, `Field`, `model_validator`.

---

# AI Usage

AI tools were used strictly as a development assistant for:

- **Architecture & Design:** Reviewing classes (Pac-Man, Ghosts, etc.) and configuration logic.
- **Concept Explanation:** Clarifying Python concepts, libraries, and Regular Expressions.
- **Project Management:** Assisting with the README and verifying project requirements.

*Disclaimer: All AI suggestions were carefully reviewed and adapted. The project members take full responsibility for understanding, testing, and validating the final code.*

---

# Authors

- ialalawn
- abani-am