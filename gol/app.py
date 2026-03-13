from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import pygame

from .config import (
    ALIVE_COLOR,
    BACKGROUND_COLOR,
    BUTTON_COLOR,
    BUTTON_HOVER_COLOR,
    BUTTON_TEXT_COLOR,
    DEAD_COLOR,
    DEFAULT_TARGET_COLS,
    GRID_BG_COLOR,
    GRID_LINE_COLOR,
    MIN_WINDOW_WIDTH,
    SLIDER_MAX_COLS,
    SLIDER_MIN_COLS,
    TEXT_COLOR,
    TOOLBAR_COLOR,
    TOOLBAR_HEIGHT,
)
from .model import GameOfLifeModel


@dataclass
class Button:
    rect: pygame.Rect
    label: str
    on_click: Callable[[], None]


class Slider:
    """Horizontal value slider widget."""

    TRACK_H: int = 8
    THUMB_R: int = 9

    def __init__(
        self,
        rect: pygame.Rect,
        min_val: int,
        max_val: int,
        value: int,
        label: str,
        on_change: Callable[[int], None],
    ) -> None:
        self.rect = rect
        self.min_val = min_val
        self.max_val = max_val
        self.value = value
        self.label = label
        self.on_change = on_change
        self._dragging: bool = False

    @property
    def thumb_x(self) -> int:
        ratio = (self.value - self.min_val) / (self.max_val - self.min_val)
        return int(self.rect.left + round(ratio * self.rect.width))

    def _apply_x(self, x: int) -> None:
        ratio = (x - self.rect.left) / max(1, self.rect.width)
        ratio = max(0.0, min(1.0, ratio))
        new_val = round(self.min_val + ratio * (self.max_val - self.min_val))
        if new_val != self.value:
            self.value = new_val
            self.on_change(new_val)

    def handle_mousedown(self, pos: tuple[int, int]) -> bool:
        tx, ty = self.thumb_x, self.rect.centery
        hit_thumb = abs(pos[0] - tx) <= self.THUMB_R + 4 and abs(pos[1] - ty) <= self.THUMB_R + 4
        hit_track = self.rect.inflate(0, 14).collidepoint(pos)
        if hit_thumb or hit_track:
            self._dragging = True
            self._apply_x(pos[0])
            return True
        return False

    def handle_mouseup(self) -> None:
        self._dragging = False

    def handle_mousemove(self, pos: tuple[int, int]) -> None:
        if self._dragging:
            self._apply_x(pos[0])

    def draw(self, surface: pygame.Surface, font: pygame.font.Font) -> None:
        cy = self.rect.centery
        label_surf = font.render(f"{self.label}: {self.value}", True, TEXT_COLOR)
        surface.blit(label_surf, label_surf.get_rect(midright=(self.rect.left - 8, cy)))

        track_rect = pygame.Rect(self.rect.left, cy - self.TRACK_H // 2, self.rect.width, self.TRACK_H)
        pygame.draw.rect(surface, GRID_LINE_COLOR, track_rect, border_radius=4)

        filled_w = max(0, self.thumb_x - self.rect.left)
        if filled_w > 0:
            pygame.draw.rect(
                surface,
                BUTTON_COLOR,
                pygame.Rect(self.rect.left, cy - self.TRACK_H // 2, filled_w, self.TRACK_H),
                border_radius=4,
            )

        pygame.draw.circle(surface, BUTTON_COLOR, (self.thumb_x, cy), self.THUMB_R)
        pygame.draw.circle(surface, BUTTON_TEXT_COLOR, (self.thumb_x, cy), self.THUMB_R - 3)


class GameOfLifeApp:
    SPEED_STEPS = [1, 2, 3, 5, 8, 12, 18, 25, 35, 50]

    def __init__(self, target_cols: int = DEFAULT_TARGET_COLS) -> None:
        pygame.init()
        pygame.display.set_caption("Conway Game of Life")

        self.target_cols = target_cols
        self.cell_size: int = 10  # updated every frame by _layout_from_size
        self.font = pygame.font.SysFont("consolas", 18)
        self.small_font = pygame.font.SysFont("consolas", 14)

        initial_width, initial_height = 720, 650
        self.window = pygame.display.set_mode((initial_width, initial_height), pygame.RESIZABLE)

        self.running = False
        self.speed_level = 5
        self._time_accumulator = 0.0
        self._last_grid_rect = pygame.Rect(0, 0, 0, 0)

        cols, rows, _ = self._layout_from_size(initial_width, initial_height)
        self.model = GameOfLifeModel(cols, rows)

        self.buttons: list[Button] = []
        self.slider: Slider | None = None
        self._rebuild_controls(initial_width, initial_height)

    def run(self) -> None:
        clock = pygame.time.Clock()
        is_active = True

        while is_active:
            dt = clock.tick(60) / 1000.0
            is_active = self._handle_events()
            if self.running:
                self._advance_simulation(dt)
            self._draw()
            pygame.display.flip()

        pygame.quit()

    def _handle_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type in (pygame.VIDEORESIZE, pygame.WINDOWRESIZED):
                self._on_window_resized()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self._toggle_running()
                elif event.key in (pygame.K_PLUS, pygame.K_KP_PLUS, pygame.K_EQUALS):
                    self._increase_speed()
                elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                    self._decrease_speed()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not (self.slider and self.slider.handle_mousedown(event.pos)):
                    self._handle_left_click(event.pos)

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.slider:
                    self.slider.handle_mouseup()

            if event.type == pygame.MOUSEMOTION:
                if self.slider:
                    self.slider.handle_mousemove(event.pos)
                if event.buttons[0] and not self.running and not (
                    self.slider and self.slider._dragging
                ):
                    self._paint_cell(event.pos)

        return True

    def _on_window_resized(self) -> None:
        w, h = self.window.get_size()
        min_h = TOOLBAR_HEIGHT + self.cell_size + 20
        ew = max(w, MIN_WINDOW_WIDTH)
        eh = max(h, min_h)
        if ew != w or eh != h:
            self.window = pygame.display.set_mode((ew, eh), pygame.RESIZABLE)
            w, h = ew, eh
        self._handle_resize(w, h)

    def _handle_resize(self, width: int, height: int) -> None:
        cols, rows, _ = self._layout_from_size(width, height)
        self.model.resize(cols, rows)
        self._rebuild_controls(width, height)

    def _layout_from_size(self, width: int, height: int) -> tuple[int, int, pygame.Rect]:
        margin = 10
        avail_w = max(1, width - 2 * margin)
        avail_h = max(1, height - TOOLBAR_HEIGHT - 2 * margin)

        self.cell_size = max(1, avail_w // self.target_cols)

        cols = min(SLIDER_MAX_COLS, max(1, avail_w // self.cell_size))
        rows = min(SLIDER_MAX_COLS, max(1, avail_h // self.cell_size))

        grid_pixel_width = cols * self.cell_size
        grid_pixel_height = rows * self.cell_size

        grid_x = margin + (avail_w - grid_pixel_width) // 2
        grid_y = margin
        grid_rect = pygame.Rect(grid_x, grid_y, grid_pixel_width, grid_pixel_height)
        return cols, rows, grid_rect

    def _rebuild_controls(self, width: int, height: int) -> None:
        toolbar_top = height - TOOLBAR_HEIGHT
        button_w, button_h, gap = 110, 38, 10
        btn_x, btn_y = 12, toolbar_top + 10

        self.buttons = [
            Button(
                pygame.Rect(btn_x, btn_y, button_w, button_h),
                "Start/Pause",
                self._toggle_running,
            ),
            Button(
                pygame.Rect(btn_x + button_w + gap, btn_y, button_w, button_h),
                "Schneller +",
                self._increase_speed,
            ),
            Button(
                pygame.Rect(btn_x + (button_w + gap) * 2, btn_y, button_w, button_h),
                "Langsamer -",
                self._decrease_speed,
            ),
        ]

        # Slider: second toolbar row (reserve ~130 px left for "Zellen: XXX" label)
        slider_y = toolbar_top + 62
        track_x = 12 + 130
        track_w = max(50, width - track_x - 12)
        self.slider = Slider(
            pygame.Rect(track_x, slider_y, track_w, 20),
            SLIDER_MIN_COLS,
            SLIDER_MAX_COLS,
            self.target_cols,
            "Zellen",
            self._on_cols_change,
        )

    def _on_cols_change(self, new_cols: int) -> None:
        """Called by the slider; updates grid without rebuilding controls."""
        self.target_cols = new_cols
        w, h = self.window.get_size()
        cols, rows, _ = self._layout_from_size(w, h)
        self.model.resize(cols, rows)

    def _advance_simulation(self, dt: float) -> None:
        steps_per_second = self.SPEED_STEPS[self.speed_level - 1]
        seconds_per_step = 1.0 / steps_per_second
        self._time_accumulator += dt

        while self._time_accumulator >= seconds_per_step:
            self.model.step()
            self._time_accumulator -= seconds_per_step

    def _position_to_cell(self, position: tuple[int, int]) -> tuple[int, int] | None:
        if not self._last_grid_rect.collidepoint(position):
            return None

        local_x = position[0] - self._last_grid_rect.left
        local_y = position[1] - self._last_grid_rect.top
        return local_x // self.cell_size, local_y // self.cell_size

    def _paint_cell(self, position: tuple[int, int]) -> None:
        cell = self._position_to_cell(position)
        if cell is None:
            return

        cell_x, cell_y = cell
        if 0 <= cell_x < self.model.cols and 0 <= cell_y < self.model.rows:
            self.model.grid[cell_x][cell_y] = True

    def _handle_left_click(self, position: tuple[int, int]) -> None:
        for button in self.buttons:
            if button.rect.collidepoint(position):
                button.on_click()
                return

        if self.running:
            return

        cell = self._position_to_cell(position)
        if cell is not None:
            self.model.toggle_cell(*cell)

    def _toggle_running(self) -> None:
        self.running = not self.running

    def _increase_speed(self) -> None:
        self.speed_level = min(10, self.speed_level + 1)

    def _decrease_speed(self) -> None:
        self.speed_level = max(1, self.speed_level - 1)

    def _draw(self) -> None:
        width, height = self.window.get_size()
        cols, rows, grid_rect = self._layout_from_size(width, height)
        self._last_grid_rect = grid_rect

        if cols != self.model.cols or rows != self.model.rows:
            self.model.resize(cols, rows)

        self.window.fill(BACKGROUND_COLOR)
        pygame.draw.rect(self.window, GRID_BG_COLOR, grid_rect)

        for x in range(self.model.cols):
            for y in range(self.model.rows):
                cell_rect = pygame.Rect(
                    grid_rect.left + x * self.cell_size,
                    grid_rect.top + y * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )
                color = ALIVE_COLOR if self.model.grid[x][y] else DEAD_COLOR
                pygame.draw.rect(self.window, color, cell_rect)
                if self.cell_size >= 3:
                    pygame.draw.rect(self.window, GRID_LINE_COLOR, cell_rect, 1)

        # Toolbar background
        toolbar_rect = pygame.Rect(0, height - TOOLBAR_HEIGHT, width, TOOLBAR_HEIGHT)
        pygame.draw.rect(self.window, TOOLBAR_COLOR, toolbar_rect)

        # Buttons
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            color = BUTTON_HOVER_COLOR if button.rect.collidepoint(mouse_pos) else BUTTON_COLOR
            pygame.draw.rect(self.window, color, button.rect, border_radius=6)
            lbl = self.small_font.render(button.label, True, BUTTON_TEXT_COLOR)
            self.window.blit(lbl, lbl.get_rect(center=button.rect.center))

        # Status text clipped to the space right of the buttons
        btn_area_right = 12 + 3 * 110 + 2 * 10 + 16
        status = "RUNNING" if self.running else "PAUSE"
        stat_text = (
            f"Gen:{self.model.generation}  "
            f"Pop:{self.model.population_count()}  "
            f"Speed:{self.speed_level}/10  "
            f"{status}"
        )
        stat_surf = self.small_font.render(stat_text, True, TEXT_COLOR)
        stat_y = height - TOOLBAR_HEIGHT + 29  # vertical center of button row
        stat_rect = stat_surf.get_rect(midleft=(btn_area_right, stat_y))
        clip = pygame.Rect(btn_area_right, 0, max(0, width - btn_area_right - 8), height)
        self.window.set_clip(clip)
        self.window.blit(stat_surf, stat_rect)
        self.window.set_clip(None)

        # Slider
        if self.slider:
            self.slider.draw(self.window, self.small_font)
