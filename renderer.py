from mazegen.cells import is_open
from mazegen.grid import Cell

WALL_COLOR = "104"
ENTRY_COLOR = "43"
EXIT_COLOR = "41"
RESET = "\033[0m"
PATTERN_COLOR = "47"
PATH_COLOR = "46"


def colorize(text: str, color_code: str) -> str:
    return f"\033[{color_code}m{text}{RESET}"


def render_maze(grid: list[list[Cell]], width: int, height: int,
                entry: tuple[int, int], exit_: tuple[int, int],
                pattern_cells: set[tuple[int, int]],
                path_coords: set[tuple[int, int]],
                show_path: bool = True, wall_color: str = WALL_COLOR) -> None:
    wall = colorize(" ", wall_color)
    top_border = wall * (width * 5 + 1)
    print(top_border)
    for y in range(height):
        mid = wall
        bottom = wall
        for x in range(width):
            cell = grid[y][x]
            walls = cell.walls
            if (x, y) == entry:
                inner = colorize("    ", ENTRY_COLOR)
            elif (x, y) == exit_:
                inner = colorize("    ", EXIT_COLOR)
            elif show_path and (x, y) in path_coords:
                inner = colorize("    ", PATH_COLOR)
            elif (x, y) in pattern_cells:
                inner = colorize("    ", PATTERN_COLOR)
            else:
                inner = "    "
            mid += inner
            mid += (colorize(" ", PATH_COLOR) if
                    (show_path and is_open(walls, "E") and
                     (x, y) in path_coords and (x + 1, y) in path_coords)
                    else " " if is_open(walls, "E") else wall)

            bottom += (colorize("    ", PATH_COLOR) if
                       (show_path and is_open(walls, "S")
                        and (x, y) in path_coords and
                        (x, y + 1) in path_coords)
                       else "    " if is_open(walls, "S") else wall * 4)
            bottom += wall
        print(mid)
        print(bottom)
