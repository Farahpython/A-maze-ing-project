import sys
from menu import run_menu
from output_file import output
from mazegen import MazeGenerator
from mazegen import get_pattern_cells


def main() -> None:
    try:
        with open(sys.argv[1], "r") as f:
            config = {}
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    print("Error: invalid config format")
                    sys.exit(1)
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()
                if key in config:
                    print("Error: duplicated key")
                    sys.exit(1)
                config[key] = value
        new_config = {}
        for key in config:
            new_config[key.lower()] = config[key].lower()
        config = new_config
        valid_keys = ["width", "height", "entry", "exit", "output_file",
                      "perfect", "seed", "algorithm", "display_mode"]
        for key in config:
            if key not in valid_keys:
                print("Error : invalid key")
                sys.exit(1)
        if "width" in config:
            try:
                width = int(config["width"])
            except ValueError:
                print("Error: width must be a number")
                sys.exit(1)
            if width <= 0:
                print("Error: width must be a positive number")
                sys.exit(1)
            if width > 40 or width < 3:
                print("Error: width value will exceed terminal size")
                print("valid width values for maze display: from 3 to 40")
                sys.exit(1)

        else:
            print("Error: width is missing from config")
            sys.exit(1)
        if "height" in config:
            try:
                height = int(config["height"])
            except ValueError:
                print("Error: height must be a number")
                sys.exit(1)
            if height <= 0:
                print("Error: height must be a positive number")
                sys.exit(1)
            if height > 40 or height < 3:
                print("Error: height value will exceed terminal size")
                print("valid height values for maze display: from 3 to 40")
                sys.exit(1)
        else:
            print("Error: height is missing from config")
            sys.exit(1)
        if "entry" in config:
            parts = config["entry"].split(",")
            if len(parts) != 2:
                print("Error: entry must have exactly two coordinates")
                sys.exit(1)
            try:
                x = int(parts[0])
                y = int(parts[1])
                entry = (x, y)
                if x < 0 or y < 0:
                    print("Error: entry values must be positive")
                    sys.exit(1)
                elif x >= width or y >= height:
                    print("Error: entry values must be within maze bounds")
                    sys.exit(1)
            except ValueError:
                print("Error: entry coordinates must be numbers")
                sys.exit(1)
        else:
            print("Error: entry is missing from config")
            sys.exit(1)
        if "exit" in config:
            parts2 = config["exit"].split(",")
            if len(parts2) != 2:
                print("Error: exit must have exactly two coordinates")
                sys.exit(1)
            try:
                x2 = int(parts2[0])
                y2 = int(parts2[1])
                entry2 = (x2, y2)
                if x2 < 0 or y2 < 0:
                    print("Error: exit values must be positive")
                    sys.exit(1)
                if x2 >= width or y2 >= height:
                    print("Error: exit values must be within maze bounds")
                    sys.exit(1)
            except ValueError:
                print("Error: exit coordinates must be numbers")
                sys.exit(1)
        else:
            print("Error: exit is missing from config")
            sys.exit(1)
        if entry == entry2:
            print("Error: entry and exit cannot be the same")
            sys.exit(1)
        if "output_file" in config:
            o_file = config["output_file"]
            if o_file == "":
                print("Error: output_file cannot be empty")
                sys.exit(1)
        else:
            print("Error: output_file is missing from config")
            sys.exit(1)
        if "perfect" in config:
            perfect_str = config["perfect"].lower()
            if perfect_str == "true":
                perfect = True
            elif perfect_str == "false":
                perfect = False
            else:
                print("Error: perfect key must be bool value")
                sys.exit(1)
        else:
            print("Error: perfect is missing from config")
            sys.exit(1)
        seed = None
        if "seed" in config:
            try:
                seed = int(config["seed"])
            except ValueError:
                print("Error: seed must be a number")
                sys.exit(1)
    except FileNotFoundError:
        print("Error: file not found")
        sys.exit(1)
    except IndexError:
        print("Error: config.txt not found... ")
        sys.exit(1)
    pattern_cells = get_pattern_cells(width, height)
    if entry in pattern_cells:
        print(f"Error: entry coordinates {entry} overlap with"
              f"the 42 pattern")
        sys.exit(1)
    if entry2 in pattern_cells:
        print(f"Error: exit coordinates {entry2} overlap"
              f"with the '42' pattern")
        sys.exit(1)
    maze = MazeGenerator(width, height, seed, pattern_cells)
    grid = maze.generate()
    grid, path = run_menu(width, height, entry, entry2,
                          pattern_cells, seed, perfect)
    output(height, width, o_file, grid, path, entry, entry2)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram Interrupted. Exiting..")
    except EOFError:
        print("\nProgram Interrupted. Exiting..")
