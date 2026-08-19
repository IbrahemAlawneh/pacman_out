import json
import re

from typing import Any
from pydantic import BaseModel, Field, model_validator

from entities.pacman_entity import Pacman
from entities.ghost_entity import Ghost
from entities.level_entity import Level


class GameEntities(BaseModel):

    # =========================================================
    # Configuration values
    # =========================================================

    highscore_filename: str = Field(default="highscores.json")

    lives: int = Field(default=3)
    points_per_pacgum: int = Field(default=10)
    points_per_super_pacgum: int = Field(default=50)
    points_per_ghost: int = Field(default=200)
    pacman_speed: int = Field(default=50)

    ghost_speed: int = Field(default=50)
    ghosts_mode: int = Field(default=1)

    seed: int = Field(default=42)
    level_max_time: int = Field(default=90)
    max_level: int = Field(default=10)

    # =========================================================
    # Runtime entities
    # =========================================================

    pacman: Pacman = Field(default_factory=Pacman)

    ghosts: list[Ghost] = Field(default_factory=list)

    level: Level = Field(default_factory=Level)

    # =========================================================
    # Configuration validation
    # =========================================================

    @model_validator(mode="before")
    @classmethod
    def validate_config(cls, data: Any) -> dict[str, Any]:

        if not isinstance(data, dict):
            print(
                "[Warning] Configuration data is not a valid object. "
                "Using default values."
            )
            return {}

        safe_data: dict[str, Any] = {}

        for key, value in data.items():

            if not isinstance(key, str):
                print(
                    "[Warning] A configuration key is not a string. "
                    "The key will be ignored."
                )
                continue

            normalized_key = key.strip().lower()

            safe_data[normalized_key] = value

        return safe_data

    # =========================================================
    # Create game entities
    # =========================================================

    @model_validator(mode="after")
    def create_entities(self) -> "GameEntities":

        # -----------------------------------------------------
        # Pac-Man
        # -----------------------------------------------------

        pacman_config = {
            "lives": self.lives,
            "points_per_pacgum": self.points_per_pacgum,
            "points_per_super_pacgum": self.points_per_super_pacgum,
            "points_per_ghost": self.points_per_ghost,
            "pacman_speed": self.pacman_speed,
        }

        self.pacman = Pacman(**pacman_config)

        # -----------------------------------------------------
        # Ghosts
        # -----------------------------------------------------

        ghosts_mode = self._validate_ghosts_mode(
            self.ghosts_mode
        )

        self.ghosts = []

        for ghost_index in range(4):

            mode = (ghosts_mode >> ghost_index) & 1

            ghost_config = {
                "ghost_speed": self.ghost_speed,
                "mode": mode,
            }

            ghost = Ghost(**ghost_config)

            self.ghosts.append(ghost)

        # -----------------------------------------------------
        # Level
        # -----------------------------------------------------

        level_config = {
            "seed": self.seed,
            "level_max_time": self.level_max_time,
            "max_level": self.max_level,
        }

        self.level = Level(**level_config)
        
        for g in self.ghosts:
            if g.speed > self.pacman.pacman_speed:
                g.speed = self.pacman.pacman_speed

        return self

    # =========================================================
    # Ghost mode validation
    # =========================================================

    @staticmethod
    def _validate_ghosts_mode(value: Any) -> int:

        try:
            value = int(value)

        except (ValueError, TypeError):

            print(
                "[Warning] Invalid ghosts_mode. "
                "Using default value: 1."
            )

            return 1

        if value < 1:

            print(
                "[Warning] ghosts_mode cannot be less than 1. "
                "Using value: 1."
            )

            return 1

        if value > 15:

            print(
                "[Warning] ghosts_mode cannot be greater than 15. "
                "Using maximum value: 15."
            )

            return 15

        return value

# ============================================================
# Configuration file helpers
# ============================================================

def _remove_comments(content: str) -> str:
    """Remove supported comments without modifying content inside strings."""

    pattern = re.compile(
        r"""
        (?P<string>
            "(?:\\.|[^"\\])*"
        )
        |
        (?P<comment>
            /\*.*?\*/
            |
            //[^\r\n]*
            |
            \#[^\r\n]*
        )
        """,
        re.DOTALL | re.VERBOSE,
    )

    def replace(match: re.Match[str]) -> str:
        if match.group("string") is not None:
            return match.group("string")

        return ""

    return pattern.sub(replace, content)


def _normalize_keys(data: dict[str, Any]) -> dict[str, Any]:
    """Normalize configuration keys to lowercase."""

    normalized: dict[str, Any] = {}

    for key, value in data.items():
        if not isinstance(key, str):
            print(
                "[Warning] A configuration key is not a string. "
                "The key will be ignored."
            )
            continue

        normalized_key = key.strip().lower()
        normalized[normalized_key] = value

    return normalized


def load_config(filename: str) -> dict[str, Any]:
    """Load, clean, parse, and normalize a configuration file."""

    try:
        with open(filename, "r", encoding="utf-8") as file:
            content = file.read()

        if not content.strip():
            print(
                "[Warning] Configuration file is empty. "
                "Using default values."
            )
            return {}

        content = _remove_comments(content)

        if not content.strip():
            print(
                "[Warning] Configuration file contains no configuration "
                "data. Using default values."
            )
            return {}

        parsed_data = json.loads(content)

        if not isinstance(parsed_data, dict):
            print(
                "[Warning] Configuration root must be a JSON object. "
                "Using default values."
            )
            return {}

        return _normalize_keys(parsed_data)

    except FileNotFoundError:
        print(
            f"[Warning] Configuration file '{filename}' was not found. "
            "Using default values."
        )
        return {}

    except PermissionError:
        print(
            f"[Warning] Permission denied while reading '{filename}'. "
            "Using default values."
        )
        return {}

    except UnicodeDecodeError:
        print(
            f"[Warning] Configuration file '{filename}' is not valid UTF-8. "
            "Using default values."
        )
        return {}

    except json.JSONDecodeError as error:
        print(
            f"[Warning] Invalid JSON configuration: {error}. "
            "Using default values."
        )
        return {}

    except OSError as error:
        print(
            f"[Warning] Could not read configuration file: {error}. "
            "Using default values."
        )
        return {}

    except Exception as error:
        print(
            f"[Warning] Unexpected configuration issue: {error}. "
            "Using default values."
        )
        return {}