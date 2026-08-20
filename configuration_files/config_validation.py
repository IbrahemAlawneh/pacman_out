import json
import re
from typing import Any

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