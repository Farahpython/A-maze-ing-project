from mazegen.grid import Cell


def output(height: int, width: int, output_file: str,
           grid: list[list[Cell]], path: str,
           entry: tuple, entry2: tuple) -> None:
    with open(output_file, "w") as f:
        for y in range(height):
            for x in range(width):
                f.write(f"{grid[y][x].walls:X}")
            f.write("\n")
        f.write("\n")
        f.write(f"{entry[0]},{entry[1]}\n")
        f.write(f"{entry2[0]},{entry2[1]}\n")
        f.write(path + "\n")
