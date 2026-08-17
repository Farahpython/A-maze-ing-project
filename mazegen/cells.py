from mazegen.grid import Cell


class MazeUnsolvableError(Exception):
    pass


directions_bits = {"N": 1, "E": 2, "S": 4, "W": 8}
opposite = {"N": "S", "E": "W", "S": "N", "W": "E"}
offsets = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}


def is_open(walls: int, direction: str) -> bool:
    return (walls & directions_bits[direction] == 0)


def find_path(
    grid: list[list[Cell]],
    start: tuple[int, int],
    end: tuple[int, int],
    width: int, height: int
) -> str:
    visited_set = {start}
    exploring_queue = [(start, "")]
    while exploring_queue:
        current_coord, current_path = exploring_queue.pop(0)
        if current_coord == end:
            return current_path
        for direction in directions_bits:
            x, y = current_coord
            if is_open(grid[y][x].walls, direction):
                off_1, off_2 = offsets[direction]
                neighbor_coord = (x + off_1, y + off_2)
                nx, ny = neighbor_coord
                if 0 <= nx < width and 0 <= ny < height:
                    if neighbor_coord not in visited_set:
                        visited_set.add(neighbor_coord)
                        new_path = current_path + direction
                        exploring_queue.append((neighbor_coord, new_path))
    raise MazeUnsolvableError(f"No path found between {start} and {end}")


def path_to_coords(start: tuple[int, int], path: str) -> set[tuple[int, int]]:
    coords = {start}
    current_coord = start
    for direction in path:
        off_1, off_2 = offsets[direction]
        current_coord = (current_coord[0] + off_1, current_coord[1] + off_2)
        coords.add(current_coord)
    return coords
