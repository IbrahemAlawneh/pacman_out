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

The required command is:

```bash
python3 pac-man.py config.json
```

The program accepts exactly one configuration file argument.

The configuration filename can be changed, as long as a valid JSON configuration file is supplied.

The game is designed to handle configuration problems without displaying an unhandled Python traceback. Missing files, invalid values, missing keys, and other expected configuration problems should result in warnings and safe defaults instead of crashing.

---

# Project Structure

The current project is organized around separate modules for the main game entities and configuration handling.

```text
.
├── pac-man.py
├── config.json
│
├── game_entities.py
├── pacman.py
├── ghost.py
├── level.py
├── mazegenerator.py
│
├── highscores.json
│
├── Makefile
├── .gitignore
└── README.md
```

Additional modules will be added as the graphical interface, game loop, highscore system, cheat mode, and other game systems are implemented.

## Main Modules

### pac-man.py

The main entry point of the application.

It receives the configuration filename from the command line and starts the game.

Usage:

```bash
python3 pac-man.py config.json
```

### game_entities.py

Contains the main GameEntities class.

GameEntities acts as the central container for the main runtime entities:

```text
GameEntities
│
├── Pacman
├── Ghost x 4
└── Level
```

The class receives the complete configuration dictionary and distributes only the relevant configuration values to each entity.

This keeps the individual entities independent from the complete configuration file.

### pacman.py

Contains the Pacman entity.

The class inherits from Pydantic BaseModel and validates its configuration using Pydantic validators.

The Pac-Man entity contains runtime information such as:

- Lives
- Initial lives
- Current points
- Player name

It also contains configurable values such as:

- Points per Pac-Gum
- Points per Super Pac-Gum
- Points per Ghost
- Pac-Man speed

The player name initially uses:

```text
unknown
```

The score starts at:

```text
0
```

The class provides a reset method that restores the player's runtime statistics when starting a new game or after the game ends.

Configuration values have safe defaults so missing or invalid values do not stop the game.

### ghost.py

Contains the Ghost entity.

There is one Ghost class and four Ghost objects are created from it.

A single class is intentionally used instead of creating separate classes for each Ghost or for each Ghost mode.

Each Ghost has attributes such as:

```text
speed
mode
```

The Ghost mode is represented internally as:

```text
0 = Random
1 = Hard / Chase
```

This allows an individual Ghost to change behavior during runtime without creating another class.

The four Ghosts are represented as four objects:

```text
Ghost 1
Ghost 2
Ghost 3
Ghost 4
```

### level.py

Contains the Level entity.

The Level object represents the current runtime level.

The level starts at:

```text
level_id = 1
```

The level ID is not read from the configuration file.

The Level contains runtime information such as:

```text
level_id
width
height
maze
```

and configuration information such as:

```text
seed
level_max_time
max_level
```

The first level starts at:

```text
20 x 20
```

Subsequent levels are designed to increase by:

```text
+5 width
+5 height
```

For example:

```text
Level 1 -> 20 x 20
Level 2 -> 25 x 25
Level 3 -> 30 x 30
```

The next_level() method is responsible for progressing to the next level.

It:

1. Increments the level ID.
2. Calculates the new width.
3. Calculates the new height.
4. Generates a new maze.
5. Updates the current Level object.

The Level cannot advance beyond max_level.

---

# Configuration

The game uses a JSON configuration file.

In addition to standard JSON, the configuration loader supports comments.

Supported comment styles are:

```text
# comment
// comment
/* comment */
```

Comments inside JSON strings are preserved.

For example:

```json
{
    "highscore_filename": "scores//backup.json",
    # This is a comment
    "lives": 3
}
```

The `//` inside the filename is treated as part of the string and is not removed.

Configuration keys are normalized to lowercase, allowing variations such as:

```text
lives
LIVES
Lives
LiVeS
```

to be treated consistently.

Unknown configuration keys are ignored.

Missing or invalid configuration values are handled using safe defaults.

The configuration system is intentionally designed to continue running instead of terminating the game when a configuration value is invalid.

---

# Current Configuration

The current configuration file is:

```json
{
    # General game and highscore configuration
    "highscore_filename": "highscores.json",
    "seed": 42,
    "level_max_time": 90,
    "max_level": 10,

    # Pac-Man / player configuration
    "lives": 3,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200,
    "pacman_speed": 50,

    # Ghost configuration
    "ghost_speed": 50,
    "ghosts_mode": 1
}
```

## Configuration Keys

### highscore_filename

Defines the file used to store persistent highscores.

Default:

```text
highscores.json
```

### seed

Defines the seed used for maze generation.

Default:

```text
42
```

The first level uses the configured seed as part of the maze generation process.

### level_max_time

Defines the maximum amount of time allocated to a level.

Default:

```text
90
```

The exact behavior when the timer reaches zero will be defined by the final game logic.

### max_level

Defines the maximum number of levels in the game.

Default:

```text
10
```

The project validates this value so that:

```text
minimum = 3
maximum = 20
```

Values below 3 are safely adjusted to 3.

Values above 20 are safely adjusted to 20.

The default value of 10 satisfies the intended multi-level game design.

### lives

Defines the number of lives the player starts with.

Default:

```text
3
```

The player loses a life when touched by a ghost.

### points_per_pacgum

Defines how many points are awarded when Pac-Man eats a normal Pac-Gum.

Default:

```text
10
```

### points_per_super_pacgum

Defines how many points are awarded when Pac-Man eats a Super Pac-Gum.

Default:

```text
50
```

The Super Pac-Gum also makes ghosts edible for a short period.

### points_per_ghost

Defines how many points are awarded when Pac-Man eats an edible ghost.

Default:

```text
200
```

### pacman_speed

Defines Pac-Man's movement speed.

Default:

```text
50
```

Pac-Man's speed cannot be lower than the Ghost speed.

If necessary, Pac-Man's speed is adjusted to the Ghost speed.

### ghost_speed

Defines the movement speed of the ghosts.

Default:

```text
50
```

### ghosts_mode

Defines which of the four ghosts start in Hard/Chase mode.

The value is interpreted as a 4-bit mask:

```text
Ghost 1 -> bit 0
Ghost 2 -> bit 1
Ghost 3 -> bit 2
Ghost 4 -> bit 3
```

The Ghost mode itself is:

```text
0 = Random
1 = Hard / Chase
```

Examples:

```text
ghosts_mode = 1

Ghost 1 -> Hard
Ghost 2 -> Random
Ghost 3 -> Random
Ghost 4 -> Random
```

```text
ghosts_mode = 3

Ghost 1 -> Hard
Ghost 2 -> Hard
Ghost 3 -> Random
Ghost 4 -> Random
```

```text
ghosts_mode = 7

Ghost 1 -> Hard
Ghost 2 -> Hard
Ghost 3 -> Hard
Ghost 4 -> Random
```

```text
ghosts_mode = 15

Ghost 1 -> Hard
Ghost 2 -> Hard
Ghost 3 -> Hard
Ghost 4 -> Hard
```

The minimum valid value is:

```text
1
```

because the game must always have at least one Ghost in Hard/Chase mode.

The maximum valid value is:

```text
15
```

Values outside this range are safely clamped.

---

# Configuration Error Handling

The configuration loader handles cases such as:

- Missing configuration file
- Empty configuration file
- Invalid JSON
- Invalid UTF-8
- Permission errors
- Invalid configuration root
- Missing configuration keys
- Invalid configuration values
- Empty values
- Unknown configuration keys
- Invalid key types

Instead of raising an unhandled exception, the program prints a warning and continues using safe defaults.

Example:

```text
[Warning] Invalid max_level. Using default value: 10.
```

The configuration system is intentionally defensive because the configuration file may be modified during the defense.

---

# Maze Generation

The project uses the assigned external A-Maze-ing package for maze generation.

The package is imported using:

```python
from mazegenerator import MazeGenerator
```

The assigned package is used as provided and is not modified by the project.

The Level entity creates a maze using the MazeGenerator.

The generator provides useful information including:

```python
maze.maze
maze.maze_entry
maze.maze_exit
maze.shortest_path
```

The maze representation is:

```python
list[list[int]]
```

The project does not replace the assigned maze-generation algorithm.

The maze generator is expected to be used with:

```text
PERFECT = False
```

as required by the activity.

If the external maze generator fails, the final game must handle the situation without an unhandled crash.

---

# Level Generation Strategy

The current architecture represents only the current level in a Level object.

The first level starts with:

```text
level_id = 1
width = 20
height = 20
```

Subsequent levels increase the dimensions by:

```text
+5 width
+5 height
```

For example:

```text
Level 1 -> 20 x 20
Level 2 -> 25 x 25
Level 3 -> 30 x 30
```

The maximum number of levels is controlled by:

```text
max_level
```

The first level uses the configured fixed seed.

Subsequent levels will use the appropriate random generation strategy required by the subject.

---

# Highscore

The game requires a persistent highscore system.

The selected highscore file is controlled by:

```json
"highscore_filename": "highscores.json"
```

The highscore system will:

- Load highscores when the game starts.
- Save highscores when the game ends.
- Keep the Top 10 scores.
- Store player names and scores.
- Accept player names with a maximum of 10 characters.
- Allow only alphanumeric characters and spaces in player names.
- Store non-negative integer scores.
- Handle missing or invalid highscore files without crashing.
- Display the Top 10 highscores in the main menu.

At the end of a game, whether the player wins or loses, the final score is displayed and the player can enter a name.

If the player submits an empty name, the project uses:

```text
unknown
```

as the fallback player name.

The final highscore implementation will be documented further once the highscore module is completed.

---

# Game Rules

## Pac-Man

Pac-Man:

- Starts with 3 lives by default.
- Moves through corridors only.
- Cannot move through walls.
- Supports four directions.
- Will support arrow keys or WASD in the final implementation.
- Loses a life when touched by a ghost.
- Respawns after losing a life.
- The game ends when all lives are lost.
- Completes a level after all Pac-Gums are eaten.

The player's score does not decrease.

## Ghosts

There are exactly four Ghost objects.

Each Ghost:

- Moves autonomously.
- Occupies one of the four maze corners.
- Has its own speed attribute.
- Has a mode attribute.
- Can operate in Random mode.
- Can operate in Hard/Chase mode.
- Can become edible after a Super Pac-Gum is eaten.
- Respawns at its corner after being eaten.

The exact chase algorithm is part of the game implementation.

## Pac-Gums

Normal Pac-Gums are placed throughout most corridors.

Eating a Pac-Gum increases the player's score by:

```text
points_per_pacgum
```

## Super Pac-Gums

Super Pac-Gums are placed in the four corners of the maze.

Eating a Super Pac-Gum:

1. Increases the player's score.
2. Makes ghosts edible for a short period.

The score awarded is controlled by:

```text
points_per_super_pacgum
```

---

# Game Progression

The final game follows this general progression:

```text
Main Menu
    |
    v
Start Game
    |
    v
Level 1
    |
    v
Level 2
    |
    v
...
    |
    v
Final Level
    |
    v
Victory
    |
    v
Enter Name
    |
    v
Highscore
    |
    v
Main Menu
```

If the player loses all lives:

```text
Gameplay
    |
    v
Game Over
    |
    v
Enter Name
    |
    v
Highscore
    |
    v
Main Menu
```

The player's score and remaining lives are handled by the Pacman entity.

Each level has a time limit.

---

# User Interface

## Main Menu

The main menu will provide:

- Start Game
- View Highscores
- Instructions
- Exit

## In-Game HUD

The HUD will display:

- Current score
- Remaining lives
- Current level
- Remaining level time

## Pause Menu

The pause menu will provide:

- Resume Game
- Return to Main Menu

## Game Over

The Game Over screen will:

- Display the final score.
- Ask the player to enter a name.
- Save the score to the highscore system.

## Victory

The Victory screen will:

- Display the final score.
- Display a congratulatory message.
- Ask the player to enter a name.
- Save the score to the highscore system.

---

# Cheat Mode

A cheat mode is required for peer review.

Its purpose is to make it easier for reviewers to test different game features.

Planned cheat features include:

- Invincibility
- Level skip
- Ghost freeze
- Extra lives
- Increased player speed

The cheat mode will be designed specifically to help reviewers test the game efficiently.

---

# Implementation

The project uses object-oriented programming and separates the main game entities into dedicated classes.

Pydantic is used for data validation and safe configuration handling.

The current entity architecture is:

```text
                  GameEntities
                       |
          +------------+------------+
          |            |            |
          v            v            v
       Pacman       Ghost x 4      Level
                                    |
                                    v
                              MazeGenerator
```

## Pacman

```python
class Pacman(BaseModel):
    ...
```

Responsible for player-related state and configuration.

Important runtime values include:

```text
name
points
lives
initial_lives
```

Configuration values include:

```text
points_per_pacgum
points_per_super_pacgum
points_per_ghost
pacman_speed
```

## Ghost

```python
class Ghost(BaseModel):
    ...
```

One class represents all ghosts.

Four objects are created from the class.

Each object has its own:

```text
speed
mode
```

The mode is:

```text
0 = Random
1 = Hard
```

The configuration's `ghosts_mode` value is interpreted as a bitmask to determine the initial mode of each Ghost.

## Level

```python
class Level(BaseModel):
    ...
```

Represents the current level at runtime.

It contains:

```text
level_id
width
height
maze
```

and level configuration:

```text
seed
max_time
max_level
```

The Level object starts at:

```text
level_id = 1
```

and uses:

```python
next_level()
```

to progress to the next level.

## GameEntities

GameEntities is the main entity container.

Its responsibility is to receive the complete configuration and construct:

```text
Pacman
Ghost 1
Ghost 2
Ghost 3
Ghost 4
Level
```

Each entity receives only the configuration relevant to it.

---

# Configuration Flow

The configuration flow is:

```text
config.json
     |
     v
load_config()
     |
     +-- remove comments
     +-- parse JSON
     +-- normalize keys
     +-- handle file/JSON problems
     |
     v
GameEntities
     |
     +----------> Pacman
     |
     +----------> Ghost 1
     |
     +----------> Ghost 2
     |
     +----------> Ghost 3
     |
     +----------> Ghost 4
     |
     +----------> Level
```

This architecture makes the configuration easy to modify during the defense.

---

# Validation Strategy

Pydantic BaseModel is used as the base for the main entities.

The project uses:

```python
Field(...)
```

for defaults and:

```python
model_validator(mode="before")
```

for safe input handling.

Where appropriate, post-validation can be performed using:

```python
model_validator(mode="after")
```

The main goal is that invalid configuration values should never cause an unhandled crash.

Examples:

```text
Invalid lives
    |
    v
Warning
    |
    v
Safe default
    |
    v
Game continues
```

Unknown keys are ignored.

Missing keys use defaults.

Invalid values are replaced with safe values.

---

# Error Handling Philosophy

The project follows a "no crash" philosophy for expected runtime and configuration failures.

Expected failures are handled using try/except blocks.

Clear warnings are displayed instead of Python tracebacks.

Files are opened using context managers:

```python
with open(...) as file:
    ...
```

This ensures resources are properly closed.

The project uses type hints throughout the codebase and aims to comply with:

- PEP 8
- Flake8
- Mypy
- PEP 257 docstrings

---

# General Software Architecture

The project follows a modular object-oriented architecture.

At a high level:

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

Additional systems will be connected to this architecture:

```text
                         Game
                          |
       +------------------+------------------+
       |                  |                  |
       v                  v                  v
 GameEntities          UI/Menu          Highscore
       |
       +-- Pacman
       +-- Ghosts
       +-- Level
              |
              v
        MazeGenerator
```

Additional systems will include:

- Game loop
- Input handling
- Collision detection
- Pac-Gum management
- Super Pac-Gum management
- Ghost AI
- Timer
- Pause handling
- Cheat mode
- Rendering
- Highscores

---

# Project Management

The project is developed collaboratively by:

- ialalawn
- abani-am

Development is performed incrementally:

1. Study the subject requirements.
2. Design the architecture.
3. Implement configuration loading.
4. Implement entity validation.
5. Integrate the assigned maze generator.
6. Implement the game logic.
7. Implement the graphical interface.
8. Implement the highscore system.
9. Implement cheat mode.
10. Test edge cases.
11. Run linting and static type checks.
12. Package and deploy the final game.

Detailed planning, task allocation, progress tracking, and development history will be maintained in the project-management documentation.

---

# Testing

Testing will cover:

- Configuration parsing
- Comment removal
- Key normalization
- Missing configuration values
- Invalid configuration values
- Invalid JSON
- Missing configuration files
- Invalid maze dimensions
- Level progression
- Ghost mode handling
- Pac-Man reset behavior
- Maze generation
- Highscore file handling
- Game-over conditions
- Victory conditions

Unit tests may be written using pytest or unittest.

---

# Code Quality

The project follows the coding requirements of the 42 activity.

The code should:

- Follow Flake8 standards.
- Use type hints.
- Pass Mypy checks.
- Use docstrings for classes and functions.
- Handle exceptions gracefully.
- Avoid unhandled crashes.
- Properly manage resources.
- Keep modules focused and reusable.

The Makefile will provide common commands such as:

```bash
make install
make run
make debug
make clean
make lint
```

The linting commands will include Flake8 and Mypy checks required by the subject.

---

# Deployment

The final project must provide a complete playable build that can be installed and launched from a public gaming platform such as:

- Steam
- Itch.io
- or another appropriate platform

The packaged game must be functional and include minimal instructions covering:

- Controls
- Options
- Configuration

The Git repository will contain the full source code and packaging script/specification at its root.

---

# Resources

## 42 Subject

The official 42 Pac-Man activity subject is the primary reference for the project.

It defines:

- Game requirements
- Configuration requirements
- Maze generator requirements
- Highscore requirements
- Game progression
- UI requirements
- Cheat mode
- Packaging
- README requirements

## A-Maze-ing Package

The assigned A-Maze-ing package is used as the external maze generator.

The project does not implement its own maze-generation algorithm.

The package interface is used by the Level entity.

## Python Documentation

Python documentation is used as a reference for:

- Object-oriented programming
- File handling
- JSON parsing
- Regular expressions
- Type hints
- Exception handling

## Pydantic Documentation

Pydantic is used for:

- BaseModel
- Field
- model_validator

These tools provide structured validation and safe defaults for the game's configuration and runtime entities.

---

# AI Usage

AI tools were used as development assistance during the activity.

AI assistance was used for:

- Discussing software architecture.
- Reviewing the design of the Pac-Man, Ghost, Level, and GameEntities classes.
- Explaining Python concepts and libraries.
- Explaining regular expressions and the re module.
- Designing robust configuration loading and validation.
- Identifying configuration edge cases.
- Reviewing the relationship between configuration data and runtime objects.
- Assisting with README documentation.
- Reviewing implementation decisions against the project requirements.

AI-generated suggestions were reviewed by the project members and adapted to the project's requirements and architecture.

The project members remain responsible for understanding, testing, reviewing, and validating all submitted code.

---

# Current Development Status

The project is currently in the architecture and entity implementation phase.

Implemented/designed so far:

- Configuration file structure
- JSON configuration loading
- Multiple comment styles
- Configuration key normalization
- Safe configuration handling
- Pydantic-based validation
- Pacman entity
- Ghost entity
- Four Ghost object architecture
- Ghost mode bitmask
- Level entity
- Runtime level progression
- Integration design with the assigned MazeGenerator
- Central GameEntities architecture

Still under development:

- Main game loop
- Graphical interface
- Player movement
- Ghost movement and AI
- Collision detection
- Pac-Gum placement and collection
- Super Pac-Gum behavior
- Timer
- Pause system
- Complete game progression
- Highscore implementation
- Cheat mode
- Main menu
- Victory/Game Over screens
- Automated tests
- Final packaging
- Public deployment

---

# Authors

- ialalawn
- abani-am

---

# License

This project was created as part of the 42 curriculum.
