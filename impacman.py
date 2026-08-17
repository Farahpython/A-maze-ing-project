from mazegen import cells


def stage_one(grid: list) -> list:

    """
    This function takes a grid of cells and returns a list of
    cells that are possible dead ends. The function iterates through
    each cell in the grid, counts the number of open walls,
    and adds the cell to the list of possible dead ends if it has exactly
    one open wall."""

    possible_dead_ends = []
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            open_count = 0
            if cells.is_open(cell.walls, "N"):
                open_count += 1
            if cells.is_open(cell.walls, "E"):
                open_count += 1
            if cells.is_open(cell.walls, "S"):
                open_count += 1
            if cells.is_open(cell.walls, "W"):
                open_count += 1
            if open_count == 1:
                possible_dead_ends.append((x, y))
    return possible_dead_ends


def stage_two(grid: list, width: int,
              height: int) -> list[tuple[tuple[int, int], str]]:

    """
    This function takes a grid of cells and returns a list of
    possible dead ends with their open directions (e.g. ((3,3), "E"))
    that don't leave the maze bounds. The function iterates through
    each cell in the grid, finds their open walls,
    and adds each cell and its open directions to the list."""

    all = stage_one(grid)
    stage_two_list = []
    for cell in all:
        cx, cy = cell
        if not cells.is_open(grid[cy][cx].walls, "E") and cx + 1 < width:
            stage_two_list.append((cell, "E"))
        if not cells.is_open(grid[cy][cx].walls, "S") and cy + 1 < height:
            stage_two_list.append((cell, "S"))
        if not cells.is_open(grid[cy][cx].walls, "W") and cx - 1 >= 0:
            stage_two_list.append((cell, "W"))
        if not cells.is_open(grid[cy][cx].walls, "N") and cy - 1 >= 0:
            stage_two_list.append((cell, "N"))
    return stage_two_list


def stage_three(grid: list, width: int, height: int,
                pattern_cells: set) -> list:

    """
    This function takes a grid of cells, the width, the height,
    and a set of the 42 pattern cells. It returns a list of possible
    dead ends with their open directions that their neighbors are NOT part
    of the pattern. The function iterates through each cell in the grid,
    finds their open walls, and adds each cell and its open directions
    to the list if their neighbors are not part of the pattern."""

    all = stage_two(grid, width, height)
    stage_three_list = []
    for cell, direction in all:
        n_cell = cell
        if direction == "E":
            n_cell = (n_cell[0] + 1, n_cell[1])
        elif direction == "S":
            n_cell = (n_cell[0], n_cell[1] + 1)
        elif direction == "W":
            n_cell = (n_cell[0] - 1, n_cell[1])
        elif direction == "N":
            n_cell = (n_cell[0], n_cell[1] - 1)
        if n_cell not in pattern_cells:
            stage_three_list.append((cell, direction))
    return stage_three_list


def stage_four(grid: list, width: int, height: int,
               pattern_cells: set) -> None:

    """
      This function takes the candidates from stage three and removes
      the walls between the dead ends and their neighbors to create
      the imperfect maze."""

    stage_four_list = stage_three(grid, width, height, pattern_cells)
    for cell, direction in stage_four_list:
        cx, cy = cell
        if direction == "E":
            grid[cy][cx].walls &= ~2
            grid[cy][cx + 1].walls &= ~8
        elif direction == "S":
            grid[cy][cx].walls &= ~4
            grid[cy + 1][cx].walls &= ~1
        elif direction == "W":
            grid[cy][cx].walls &= ~8
            grid[cy][cx - 1].walls &= ~2
        elif direction == "N":
            grid[cy][cx].walls &= ~1
            grid[cy - 1][cx].walls &= ~4


def pacman_mode(grid: list, width: int, height: int,
                pattern_cells: set) -> None:

    """
        This function takes a grid of cells, the width, the height,
        and a set of the 42 pattern cells. It uses the impeferct maze
        helper functions to create a board directly usable
        by a Pac-Man-like game
    """

    candidates = stage_three(grid, width, height, pattern_cells)
    for cell, direction in candidates:
        cx, cy = cell
        if direction == "E":
            grid[cy][cx].walls &= ~2
            grid[cy][cx + 1].walls &= ~8
        elif direction == "S":
            grid[cy][cx].walls &= ~4
            grid[cy + 1][cx].walls &= ~1
        elif direction == "W":
            grid[cy][cx].walls &= ~8
            grid[cy][cx - 1].walls &= ~2
        elif direction == "N":
            grid[cy][cx].walls &= ~1
            grid[cy - 1][cx].walls &= ~4
