from __future__ import annotations


class GameOfLifeModel:
    def __init__(self, cols: int, rows: int) -> None:
        self.cols = cols
        self.rows = rows
        self.grid = [[False for _ in range(rows)] for _ in range(cols)]
        self.generation = 0

    def resize(self, cols: int, rows: int) -> None:
        new_grid = [[False for _ in range(rows)] for _ in range(cols)]
        copy_cols = min(self.cols, cols)
        copy_rows = min(self.rows, rows)
        for x in range(copy_cols):
            for y in range(copy_rows):
                new_grid[x][y] = self.grid[x][y]

        self.cols = cols
        self.rows = rows
        self.grid = new_grid

    def toggle_cell(self, x: int, y: int) -> None:
        if 0 <= x < self.cols and 0 <= y < self.rows:
            self.grid[x][y] = not self.grid[x][y]

    def population_count(self) -> int:
        return sum(1 for column in self.grid for cell in column if cell)

    def step(self) -> None:
        next_grid = [[False for _ in range(self.rows)] for _ in range(self.cols)]
        for x in range(self.cols):
            for y in range(self.rows):
                neighbors = self._count_neighbors(x, y)
                is_alive = self.grid[x][y]
                if is_alive and neighbors in (2, 3):
                    next_grid[x][y] = True
                elif (not is_alive) and neighbors == 3:
                    next_grid[x][y] = True

        self.grid = next_grid
        self.generation += 1

    def _count_neighbors(self, x: int, y: int) -> int:
        count = 0
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                nx = (x + dx) % self.cols
                ny = (y + dy) % self.rows
                if self.grid[nx][ny]:
                    count += 1
        return count
