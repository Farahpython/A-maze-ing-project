import random


class Cell(object):
    def __init__(self) -> None:
        self.walls: int = 0xF
        self.visited: bool = False


def draw_4(x: int, y: int) -> set[tuple[int, int]]:
    coords = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 3), (2, 4),]
    return {(x + dx, y + dy) for dx, dy in coords}


def draw_2(x: int, y: int) -> set[tuple[int, int]]:
    coords = [(0, 0), (1, 0), (2, 0), (2, 1), (0, 2), (1, 2), (2, 2),
              (0, 3), (0, 4), (1, 4), (2, 4),]
    return {(x + dx, y + dy) for dx, dy in coords}


def get_pattern_cells(width: int, height: int) -> set[tuple[int, int]]:
    pattern_width = 7
    pattern_height = 5

    if width < pattern_width or height < pattern_height:
        print("Maze too small to display the 42 pattern.\n")
        return set()

    start_x = (width - pattern_width) // 2
    start_y = (height - pattern_height) // 2
    cells = draw_4(start_x, start_y)
    cells |= draw_2(start_x + 4, start_y)
    return cells


class MazeGenerator:
    def __init__(self, width: int, height: int, seed: int | None = None,
                 pattern_cells: set[tuple[int, int]] | None = None) -> None:
        self.width = width
        self.height = height
        self.seed = seed
        self.pattern_cells = pattern_cells
        self.grid: list[list[Cell]] | None = None

    def generate(self) -> list[list[Cell]]:

        if self.seed is not None:
            random.seed(self.seed)

        grid: list[list[Cell]] = [
            [Cell() for _ in range(self.width)]
            for _ in range(self.height)
        ]

        if self.pattern_cells:
            for px, py in self.pattern_cells:
                grid[py][px].visited = True

        x, y = 0, 0
        grid[y][x].visited = True
        stack = [(x, y)]

        way = [
            (0, -1, "N"),
            (0, 1, "S"),
            (-1, 0, "W"),
            (1, 0, "E")
        ]

        while len(stack) > 0:
            x, y = stack[-1]
            neighbors = []

            for wx, wy, w in way:
                nx = x + wx
                ny = y + wy

                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if not grid[ny][nx].visited:
                        neighbors.append((nx, ny, w))

            if neighbors:
                nx, ny, w = random.choice(neighbors)

                if w == "E":
                    grid[y][x].walls -= 2
                    grid[ny][nx].walls -= 8

                elif w == "S":
                    grid[y][x].walls -= 4
                    grid[ny][nx].walls -= 1

                elif w == "W":
                    grid[y][x].walls -= 8
                    grid[ny][nx].walls -= 2

                elif w == "N":
                    grid[y][x].walls -= 1
                    grid[ny][nx].walls -= 4

                grid[ny][nx].visited = True
                stack.append((nx, ny))

            else:
                stack.pop()
        self.grid = grid
        return self.grid
