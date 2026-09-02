# Project Timeline

## Gantt Chart

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {
    'primaryColor': '#1a2a6c',
    'primaryTextColor': '#fff',
    'primaryBorderColor': '#f6c90e',
    'lineColor': '#f6c90e',
    'secondaryColor': '#b21f1f',
    'tertiaryColor': '#2c3e50',
    'sectionBkgColor': '#1a2a6c',
    'altSectionBkgColor': '#2c3e50',
    'gridColor': '#556677',
    'doneTaskBkgColor': '#27ae60',
    'doneTaskBorderColor': '#1e8449',
    'activeTaskBkgColor': '#f6c90e',
    'activeTaskBorderColor': '#b7950b',
    'taskTextColor': '#ffffff',
    'taskTextOutsideColor': '#ffffff',
    'taskTextDarkColor': '#000000'
}}}%%
gantt
    title Pac-Man 42 — Development Timeline (2026-08-07 to 2026-09-03)
    dateFormat  YYYY-MM-DD
    axisFormat  %d/%m

    section Setup
    Study subject & design architecture   :done,    setup1, 2026-08-07, 2d
    Poetry / pyproject / Makefile setup   :done,    setup2, after setup1, 1d

    section Core
    Config parser (Pydantic + comments)   :done,    core1, after setup2, 2d
    Entities (Pacman, Ghost, Level)       :done,    core2, after core1, 3d
    Maze generator integration            :done,    core3, after core1, 2d

    section Gameplay
    Game loop & rendering                 :done,    gp1, after core2, 4d
    Player movement & collisions          :done,    gp2, after gp1, 2d
    Ghost AI (Random / Chase)             :done,    gp3, after gp2, 3d
    Pac-Gum / Super Pac-Gum logic         :done,    gp4, after gp2, 2d

    section Systems
    Highscore system                      :done,    sys1, after gp4, 2d
    Cheat mode                            :done,    sys2, after gp3, 1d
    UI (menu, HUD, pause, game over)      :done,    sys3, after gp4, 3d

    section Wrap-up
    Linting & type checking               :done,    wrap1, after sys3, 1d
    Packaging & Itch.io deployment        :done,    wrap2, after wrap1, 1d
    README & documentation review         :done,    wrap3, 2026-09-02, 1d
```

## Progress Tracking

Total duration: **4 weeks**, from **Friday, August 7, 2026** to **Thursday, September 3, 2026** (deadline).

| Milestone | Planned |
|---|---|
| Architecture & config parser | Week 1 (Aug 7–13) |
| Core entities (Pacman/Ghost/Level) | Week 1–2 (Aug 11–18) |
| Maze generator integration | Week 1–2 (Aug 11–18) |
| Game loop & rendering | Week 2 (Aug 18–22) |
| Ghost AI & collisions | Week 3 (Aug 22–28) |
| Highscore + UI + Cheat mode | Week 3 (Aug 22–28) |
| Lint/type-check pass | Week 4 (Aug 28–Sep 2) |
| Packaging & deployment | Week 4 (Aug 28–Sep 2) |
| README & final review | Sep 2–3 |

*This table is updated as development progresses; deviations from the planned schedule are discussed in `management.md`.*