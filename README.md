*This activity has been created as part of the 42 curriculum by jabu-alh, fadarwis*

# Maze Project (A-Maze-ing)

## Description
This project is a maze generation and solving application written in Python.
It reads a plain-text configuration file, generates a maze (perfect or "Pac-Man playable"),
computes the shortest path between an entry and an exit cell, and renders the result
directly in the terminal using ANSI escape sequences (colored entry, exit, "42" pattern,
and — optionally displayed — shortest path).

The core maze-generation logic lives in a standalone, reusable package (`mazegen`) so it
can be imported and reused in future projects, independently of the rendering code.


### Requirements
- Python 3.10+ (the code uses modern type hints such as `int | None`).
- No third-party dependencies to run the project: only the standard library
  (`random`, `sys`, `shutil`) is used. `flake8`/`mypy` are only needed for linting.

### Instructions: How to run the project
```bash
make install   # creates a venv and installs flake8 + mypy into it
make run       # runs: python3 a_maze_ing.py config.txt
make debug     # runs the main script under pdb
make lint      # flake8 + mypy checks
make clean     # removes __pycache__, .mypy_cache, build/dist artifacts and the venv
```
- `a_maze_ing.py` is the main program file.
- `config.txt` is the only argument: a plain text file describing the maze to generate.
  You can point it to any file with a different name.

The program validates the configuration file and reports a clear error message
(without crashing) for missing keys, invalid values, out-of-bounds coordinates, an
entry/exit colliding with the "42" pattern, or a terminal window too small to display
the maze.

### Interactive menu
Once the maze is generated and rendered, `run` shows a menu to:
1. Re-generate a new maze (new random seed).
2. Show/Hide the shortest path between entry and exit.
3. Rotate the wall color.
4. Quit — the final maze and its shortest path are then written to `OUTPUT_FILE`.

## Configuration file format
The complete format of config file : KEY=VALUE
for example:
```text
WIDTH=15                    # Maze width (number of cells)
HEIGHT=16                   # Maze height
ENTRY=0,0                   # Entry coordinates (x,y)
EXIT=9,11                   # Exit coordinates (x,y)
OUTPUT_FILE=maze.txt        # Output filename
PERFECT=False               # Is the maze perfect?
SEED=42                     # Optional: seed for reproducible generation
ALGORITHM=backtracker       # Optional: generation algorithm
```

A default `config.txt` is provided at the root of the repository.

## Output file
When the menu is closed (option 4), the final maze is written to `OUTPUT_FILE` (see
`output_file.py`): one hexadecimal digit per cell (bit 0=N, 1=E, 2=S, 3=W; `1` = closed
wall), one row per line, followed by an empty line, then the entry coordinates, the exit
coordinates, and the shortest path as `N`/`E`/`S`/`W` letters — matching the format checked
by the provided `maze_analyzer.py`.

## Maze generation

- **Algorithm — Recursive backtracker (DFS).** Starting from `(0,0)`, the generator pushes
  the current cell on a stack, picks a random unvisited neighbour, knocks down the wall
  between them, and keeps going until it has to backtrack. This produces long, winding,
  non-uniform corridors — a more interesting maze than algorithms that spread openings
  evenly.
- **Shortest path — BFS.** `mazegen.cells.find_path` explores the maze breadth-first from
  the entry cell, guaranteeing the first time it reaches the exit it has found the
  shortest possible route (returned as a string of `N`/`E`/`S`/`W` moves).
- **The "42" pattern.** `mazegen.grid.get_pattern_cells` computes a fixed set of coordinates
  (centered in the grid) shaping a "4" and a "2". Those cells are marked as already
  "visited" before generation starts, so the backtracker never carves a passage through
  them and they stay fully closed. If the maze is too small to fit the pattern, generation
  still proceeds but a message is printed and the pattern is skipped. Entry and exit points
  are rejected if they fall on a pattern cell.
- **Two generation modes**, controlled by `PERFECT`:
  - `PERFECT=True`: the raw DFS output is kept as-is — a perfect maze, i.e. exactly one
    path between any two cells (a spanning tree, no loops).
  - `PERFECT=False` (default): `impacman.pacman_mode` is run afterwards. It locates
    dead-end cells (exactly one open wall), collects candidate walls that could be removed
    without touching a neighbour of the "42" pattern, and knocks all of them down. This
    adds loops to the maze so it works as a playable Pac-Man-style board (no dead ends
    besides the "42" pattern, multiple routes between points) instead of a single-solution
    maze.

## Reusable package (`mazegen`)
The maze-generation core is a standalone package, importable independently of the
terminal renderer, and built around a single class: `MazeGenerator`.

**Basic usage:**
```python
from mazegen import MazeGenerator, get_pattern_cells, find_path

grid = MazeGenerator(width=15, height=16, seed=42,
                      pattern_cells=get_pattern_cells(15, 16)).generate()
path = find_path(grid, start=(0, 0), end=(9, 11), width=15, height=16)
```

- **Custom parameters:** `MazeGenerator(width, height, seed=None, pattern_cells=None)` —
  pass a `seed` for reproducible mazes, and `pattern_cells` (from `get_pattern_cells`) to
  keep the "42" shape closed. `.generate()` builds and returns the grid.
- **Accessing the structure:** `generate()` returns a `list[list[Cell]]` grid. Each `Cell`
  has a `walls` bitmask (bit 0=N, 1=E, 2=S, 3=W; `1` = closed); check a side with
  `is_open(cell.walls, "N")`.
- **Accessing a solution:** `find_path(grid, start, end, width, height)` returns the
  shortest path as a string of `N`/`E`/`S`/`W` moves (raises `MazeUnsolvableError` if none
  exists). `path_to_coords(start, path)` converts it to a set of `(x, y)` coordinates.

**Installing / rebuilding the package:** the pre-built `mazegen-1.0.0-py3-none-any.whl` sits
at the root of the repository (`pip install mazegen-1.0.0-py3-none-any.whl`). To rebuild it
from source: `pip install build` then `python -m build` (uses `pyproject.toml`), which
regenerates the `.whl`/`.tar.gz` in `dist/`. The package is released under the MIT license
(see `LICENSE.md`), which allows reuse and distribution in later projects.

## Team and Project Management

1. Roles of each team member:
* **jabu-alh**: `grid`, `__init__`, output, menu files
* **fadrwis**: `renderer`, `cells`, `impacman`
* **together**: `a_maze_ing`, config

2. Anticipated planning and how it evolved until the end:
**Initial Plan:** We originally planned to complete the entire project in approximately two
weeks, assuming the setup and error-handling would be straightforward.
**How it Evolved:** The project timeline extended to about a month, mainly because:
  * 1. We spent significant time studying how to properly build and package a reusable
    Python library (`.whl` and `.tar.gz`).
  * 2. We decided to build a robust system, which required anticipating and handling
    every possible user error or edge case in the configuration file and arguments.

### 3. Retrospective (What Worked vs. What Could Be Improved)
* **What Worked Well:**
  * **Exceptional Teamwork:** Communication stayed smooth throughout the month, which made
    resolving complex bugs (like keeping the "42" pattern and the imperfect-maze wall
    removal from colliding) much easier.
  * **Fair Task Distribution:** Tasks were divided based on each member's strengths.
* **What Could Be Improved:**
  * **UI/Visuals Trade-off:** We initially wanted a graphical display using **MiniLibX
    (MLX)**. Given the time constraints, ASCII rendering with ANSI colors turned out to be
    a much faster way to satisfy the visual requirements. A graphical interface would be a
    natural next step.

### 4. Tools Used
* **GitHub:** Our primary tool for collaboration — sharing files, tracking changes,
  reviewing each other's code, and working on different features concurrently.

## Resources
- https://www.kufunda.net/publicdocs/Mazes%20for%20Programmers%20Code%20Your%20Own%20Twisty%20Little%20Passages%20(Jamis%20Buck).pdf
- https://youtu.be/cS-198wtfj0?si=6HklbA1h44ScrI3m
- AI: used to learn maze-generation/pathfinding algorithms and ANSI terminal rendering
  techniques (`mazegen` and `renderer`). Every AI-suggested approach was reviewed and
  rewritten by hand before being used in the code.
- https://medium.com/@msgold/using-python-to-create-and-solve-mazes-672285723c96

