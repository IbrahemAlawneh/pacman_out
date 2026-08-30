from dataclasses import dataclass


@dataclass
class ThemeConfig:
    """Holds a theme's name, background image path, and music path."""

    name: str
    bg_path: str
    music_path: str


GAME_THEMES = [
    ThemeConfig(
        name="classic", bg_path="assets/images/themes/classic.jpg",
        music_path="assets/sounds/themes/classic.ogg"
    ),
    ThemeConfig(
        name="neon", bg_path="assets/images/themes/neon.jpg",
        music_path="assets/sounds/themes/neon.ogg"
    ),
    ThemeConfig(
        name="desert", bg_path="assets/images/themes/desert.jpg",
        music_path="assets/sounds/themes/desert.ogg"
    ),
]
