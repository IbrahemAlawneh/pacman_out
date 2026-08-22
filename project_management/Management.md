# Project Management

## Team Organization

```mermaid
flowchart TD
    A[Pac-Man 42 Project] --> B[ialalawn]
    A --> C[abani-am]

    B --> B1[Config parser & validation]
    B --> B2[Highscore system]
    B --> B3[README & documentation]

    C --> C1[Entities: Pacman, Ghost, Level]
    C --> C2[Maze generator integration]
    C --> C3[Packaging & Itch.io deployment]

    B & C --> D[Game loop, UI, Ghost AI]
    D --> E[Joint review & peer testing]
```

Both members review each other's work before merging. Architectural decisions (e.g. entity design, Pydantic validation strategy, packaging approach) were made collaboratively through pair discussion.

## Risk Analysis

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| External `mazegenerator` package fails or has an unstable API | Medium | High | Wrapped all calls in try/except; adapter layer isolates the rest of the codebase from the package's interface |
| Config file is manually edited/broken during defense | High | Medium | Defensive Pydantic validators clamp every field to safe defaults; no unhandled traceback possible |
| `pyinstaller`/`butler` packaging fails on submission day | Medium | High | Packaging tested early via `packaging/publish.sh`; kept as a repeatable one-command script |
| Ghost AI performance issues on larger mazes (levels 5–10) | Low | Medium | Chase logic kept lightweight (distance-based, no full pathfinding) to avoid frame drops |
| Merge conflicts between the two members | Medium | Low | Clear module ownership (see Team Organization) reduces overlapping edits |

## Acceptance Test Plan

| Feature | Test |
|---|---|
| Config loading | Missing file → safe defaults, no crash |
| Config loading | Invalid JSON → safe defaults, no crash |
| Config loading | `#`, `//`, `/* */` comments stripped correctly |
| Maze generation | `PERFECT=False` produces valid Pac-Man-style maze |
| Player movement | Pac-Man cannot pass through walls |
| Ghost behavior | Ghosts switch to edible state after Super Pac-Gum |
| Highscore | Top 10 persist correctly across restarts |
| Cheat mode | Invincibility / level skip work as expected |
| Packaging | `make build` + `publish.sh` produce a working Itch.io build |

## Blocking Points & Conflicts

- **Itch.io project naming mismatch** — initial `butler push` attempts failed with `invalid target (bad user)` due to a mismatch between the `USERNAME` in the publish script and the actual Itch.io account handle. Resolved by aligning the script's `USERNAME`/`GAME` values with the exact Itch.io project URL slug.
- **Poetry package-mode error** — `poetry install` initially failed with *"No file/folder found for package"* since the project is an application, not an importable library. Resolved by setting `package-mode = false` under `[tool.poetry]`.
- No unresolved team conflicts to date; task division has kept overlap minimal.