import json
from pathlib import Path
from typing import Any, cast
import pygame


class GameResult:
    """Shows level transitions, game over/win, and highscore entry."""

    OVERLAY, PANEL_FILL = (4, 7, 22, 175), (13, 18, 46, 190)
    CYAN, PINK, GOLD, RED = (
        (86, 224, 255), (224, 104, 255),
        (255, 202, 86), (255, 65, 75)
    )
    WHITE, MUTED, DIM = (239, 244, 255), (148, 166, 205), (63, 81, 132)

    def __init__(
            self, screen: pygame.Surface, won: bool,
            score: int, next_level: int | None = None,
            file_name: str = "high_score.json"
    ) -> None:
        """Set up the result screen state, fonts, scores, and buttons."""
        self.source_path = Path("configuration_files") / file_name
        self.screen = screen
        self.won, self.score, self.next_level = won, score, next_level
        self.started_at, self.name_input, self.saved_message = (
            pygame.time.get_ticks(), "", ""
        )

        font = pygame.font.match_font("segoeui,dejavusans,arial")
        self.fonts: dict[int | str, pygame.font.Font] = {
            s: pygame.font.Font(font, s) for s in (56, 30, 24, 20, 16)
        }
        self.fonts["bold"] = pygame.font.Font(font, 56)
        self.fonts["bold"].set_bold(True)

        scores = [s.get("score", 0) for s in self._load_scores()]
        lowest_score = min(scores) if len(scores) >= 10 else -1
        self.qualifies = not next_level and self.score > lowest_score
        self.stage = (
            "transition" if next_level else "enter_name"
            if self.qualifies else "result"
        )
        cx, y0 = screen.get_width() // 2, screen.get_height() // 2 + 35

        self.btns: list[dict[str, Any]] = [
            {
                "text": t, "action": a,
                "rect": pygame.Rect(cx - 170, y0 + i * 70, 340, 58)
            }
            for i, (t, a) in enumerate(
                [
                    ("PLAY AGAIN", "play"),
                    ("MAIN MENU", "back_to_menu")
                ]
            )
        ]
        self.selected = 0

    def _load_scores(self) -> list[dict[str, Any]]:
        """Load saved highscores, returning an empty list on any error."""
        try:
            return cast(
                list[dict[str, Any]],
                json.loads(self.source_path.read_text())
            )
        except Exception:
            return []

    def _save_score(self, name: str) -> None:
        """Append the new score and persist the top 10 to disk."""
        scores = sorted(
            self._load_scores() + [
                {
                    "name": name or "unknown",
                    "score": self.score
                }], key=lambda s: s.get("score", 0), reverse=True)[:10]
        self.source_path.parent.mkdir(parents=True, exist_ok=True)
        self.source_path.write_text(json.dumps(scores, indent=2))

    def handle_event(self, event: pygame.event.Event) -> str | None:
        """Route input to name entry or result-stage button handling."""
        if self.stage == "transition":
            return None
        if self.stage == "enter_name" and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.stage = "result"
            elif event.key == pygame.K_RETURN:
                self._save_score(self.name_input.strip())
                self.saved_message = (
                    f'SAVED AS "{self.name_input.strip() or "unknown"}"'
                )
                self.stage = "result"
            elif event.key == pygame.K_BACKSPACE:
                self.name_input = self.name_input[:-1]
            elif len(
                self.name_input
            ) < 10 and (
                event.unicode.isalnum() or event.unicode == " "
            ):
                self.name_input += event.unicode
            return None

        if self.stage == "result":
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    self.selected = 0
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    self.selected = 1
                elif event.key in (
                    pygame.K_RETURN, pygame.K_KP_ENTER
                ):
                    # تحويل صريح إلى str
                    return str(self.btns[self.selected]["action"])
            elif event.type == pygame.MOUSEMOTION and event.rel != (0, 0):
                for i, b in enumerate(self.btns):
                    if b["rect"].collidepoint(event.pos):
                        self.selected = i
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for b in self.btns:
                    if b["rect"].collidepoint(event.pos):
                        # تحويل صريح إلى str
                        return str(b["action"])
        return None

    def update(self) -> str | None:
        """Advance past the level-complete transition after one second."""
        if (
            self.stage == "transition" and
            pygame.time.get_ticks() - self.started_at >= 1000
        ):
            return "next_level"
        return None

    def _text(
            self, txt: str, pos: tuple[int, int],
            size: int | str, color: tuple[int, int, int] | None = None,
            bold: bool = False
    ) -> None:
        """Render one centered text label at the given position."""
        img = (
            self.fonts["bold"] if bold else self.fonts[size]
        ).render(txt, True, color or self.WHITE)
        self.screen.blit(img, img.get_rect(center=pos))

    def _panel(
            self, w: int, h: int, border: tuple[int, int, int]
    ) -> pygame.Rect:
        """Draw a centered translucent panel with a colored border."""
        r = pygame.Rect(0, 0, w, h)
        r.center = self.screen.get_rect().center
        fill = pygame.Surface(r.size, pygame.SRCALPHA)
        pygame.draw.rect(
            fill, self.PANEL_FILL, fill.get_rect(), border_radius=22
        )
        self.screen.blit(fill, r.topleft)
        pygame.draw.rect(
            self.screen, border, r, width=2, border_radius=22
        )
        return r

    def draw(self) -> None:
        """Draw the overlay and the panel matching the current stage."""
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill(self.OVERLAY)
        self.screen.blit(overlay, (0, 0))
        cx = self.screen.get_rect().centerx

        if self.stage == "transition":
            self._draw_transition(cx)
        elif self.stage == "enter_name":
            self._draw_enter_name(cx)
        else:
            self._draw_result(cx)

    def _draw_transition(self, cx: int) -> None:
        """Draw the level-complete panel with a glowing title."""
        p = self._panel(430, 220, self.CYAN)
        for off, col in ((4, self.DIM), (2, self.PINK), (0, self.WHITE)):
            self._text(
                "★ LEVEL COMPLETE ★", (cx + off, p.y + 62 + off), 30, col
            )
        self._text(f"LEVEL {self.next_level}", (cx, p.y + 130), 56, self.GOLD)

    def _draw_enter_name(self, cx: int) -> None:
        """Draw the new-highscore panel with the name input box."""
        p = self._panel(530, 310, self.GOLD)
        title_y = p.y + 55
        for off, col in (
            (7, self.DIM),
            (3, self.CYAN),
            (0, self.GOLD),
            (0, self.GOLD),
        ):
            self._text(
                "NEW HIGH SCORE!",
                (cx + off, title_y + off), 56, col
            )
        self._text(f"SCORE: {self.score}", (cx, p.y + 105), 30)

        box = pygame.Rect(0, 0, 320, 50)
        box.center = (cx, p.y + 175)
        pygame.draw.rect(
            self.screen, (*self.WHITE, 30), box, border_radius=10
        )
        pygame.draw.rect(
            self.screen, self.CYAN, box, width=2, border_radius=10
        )
        self._text(
            self.name_input or "TYPE YOUR NAME",
            box.center, 20,
            self.PINK if self.name_input else self.MUTED
        )
        self._text(
            "ENTER TO SAVE   ESC TO SKIP",
            (cx, p.bottom - 35), 16, self.MUTED
        )

    def _draw_result(self, cx: int) -> None:
        """Draw the win/lose panel with the final score and buttons."""
        p = self._panel(480, 430, self.PINK if self.won else self.RED)
        self._text(
            "YOU WIN!" if self.won else "GAME OVER",
            (cx, p.y + 60), 56,
            self.GOLD if self.won else self.RED,
            not self.won
        )
        self._text(f"FINAL SCORE: {self.score}", (cx, p.y + 112), 30)

        if self.saved_message:
            self._text(self.saved_message, (cx, p.y + 150), 16, self.CYAN)

        pygame.draw.line(
            self.screen, self.DIM,
            (p.x + 48, p.y + 178), (p.right - 48, p.y + 178)
        )
        for i, b in enumerate(self.btns):
            r, active = b["rect"], (i == self.selected)
            border = self.PINK if active else self.CYAN
            fill = pygame.Surface(r.size, pygame.SRCALPHA)

            fill_color = (
                (*border, 60) if active else (*self.DIM, 130)
            )
            pygame.draw.rect(
                fill, fill_color, fill.get_rect(), border_radius=14
            )
            self.screen.blit(fill, r.topleft)
            pygame.draw.rect(
                self.screen, border, r,
                width=3 if active else 1, border_radius=14
            )
            self._text(
                str(b["text"]), r.center, 24,
                self.WHITE if active else self.MUTED
            )
        self._text(
            "\u2191 \u2193 SELECT   ENTER CONFIRM",
            (cx, p.bottom - 25), 16, self.MUTED
        )
