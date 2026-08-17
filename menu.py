import sys
import shutil
import random
from impacman import pacman_mode
from renderer import render_maze
from mazegen.grid import Cell
from mazegen import MazeGenerator, find_path
from mazegen import MazeUnsolvableError, path_to_coords


COLOR_CHOICES = {"1": "104", "2": "44", "3": "42", "4": "43"}


def run_menu(
        width: int, height: int, entry: tuple[int, int],
        entry2: tuple[int, int], pattern_cells: set[tuple[int, int]],
        seed: int | None, perfect: bool) -> tuple[list[list[Cell]], str]:
    wall_color = "104"
    show_path = True
    configured_seed = seed
    grid = MazeGenerator(width, height, seed, pattern_cells).generate()
    try:
        if not perfect:
            pacman_mode(grid, width, height, pattern_cells)
        path = find_path(grid, entry, entry2, width, height)
        path_coord = path_to_coords(entry, path)
    except MazeUnsolvableError as e:
        print(f"Error: {e}")
        sys.exit(1)

    def check_terminal_size() -> bool:
        t_columns, t_rows = shutil.get_terminal_size()
        return (t_columns < (width * 5 + 1) and t_rows < (height * 2 + 1))
    wrong_size = check_terminal_size()
    if wrong_size:
        print("Error: resize your terminal to display the maze")
        sys.exit(1)
    else:
        render_maze(grid, width, height, entry, entry2, pattern_cells,
                    path_coord, show_path, wall_color)
    while True:
        print("\n=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Rotate maze colors")
        print("4. Quit")
        choice = input("Choose a number champ ;)").strip()
        if choice == "1":
            if configured_seed is None:
                seed = random.randint(0, 2**32 - 1)
            else:
                seed = configured_seed
            grid = MazeGenerator(width, height, seed, pattern_cells).generate()
            try:
                if not perfect:
                    pacman_mode(grid, width, height, pattern_cells)
                path = find_path(grid, entry, entry2, width, height)
                path_coord = path_to_coords(entry, path)
            except MazeUnsolvableError as e:
                print(f"Error: {e}")
                continue
            wrong_size = check_terminal_size()
            if wrong_size:
                print("Error: resize your terminal to display the maze")
                sys.exit(1)
            else:
                render_maze(grid, width, height, entry, entry2,
                            pattern_cells, path_coord, show_path, wall_color)
        elif choice == "2":
            show_path = not show_path
            render_maze(grid, width, height, entry, entry2,
                        pattern_cells, path_coord, show_path, wall_color)
        elif choice == "3":
            options = list(COLOR_CHOICES.values())
            current_index = options.index(wall_color)
            next_index = (current_index + 1) % len(options)
            wall_color = options[next_index]
            render_maze(grid, width, height, entry, entry2,
                        pattern_cells, path_coord, show_path, wall_color)
        elif choice == "4":
            break
        else:
            print("Error, try again with an integer number in the 1-4 range.")
    return grid, path
