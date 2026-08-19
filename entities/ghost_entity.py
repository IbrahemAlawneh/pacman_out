from typing import Any

from pydantic import BaseModel, Field, model_validator


class Ghost(BaseModel):
    # Ghost configuration
    speed: int = Field(default=50)
    mode: int = Field(default=0)

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

        safe_data: dict[str, Any] = {}

        # -------------------------
        # Ghost speed
        # -------------------------
        speed = data.get("ghost_speed", data.get("speed", 50))

        if speed is None or (
            isinstance(speed, str) and not speed.strip()
        ):
            print(
                "[Warning] Invalid Ghost speed. "
                "Using default value: 50."
            )
            speed = 50

        try:
            speed = int(speed)

            if speed <= 0:
                print(
                    "[Warning] Invalid Ghost speed. "
                    "Using default value: 50."
                )
                speed = 50

        except (ValueError, TypeError):
            print(
                "[Warning] Invalid Ghost speed. "
                "Using default value: 50."
            )
            speed = 50

        safe_data["speed"] = speed

        # -------------------------
        # Ghost mode
        # -------------------------
        mode = data.get("mode", 0)

        if mode is None or (
            isinstance(mode, str) and not mode.strip()
        ):
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