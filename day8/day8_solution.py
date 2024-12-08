import numpy as np


def read_in_map_and_antenna(input_file: str) -> list[set[str], np.ndarray]:
    antenna = set()
    map_grid = []
    with open(input_file) as raw_map:
        for line in raw_map.readlines():
            line = [*line.strip()]
            map_grid.append(line)
            antenna.update(set(line))
    antenna -= {"."}
    return antenna, np.array(map_grid)


def antinode_is_in_grid(antinode: tuple[int], grid: np.ndarray) -> bool:
    row, column = antinode
    max_row, max_column = grid.shape
    if row < 0 or column < 0 or row > max_row - 1 or column > max_column - 1:
        return False
    return True


def get_row_col_diff(coord_1: tuple[int], coord_2: tuple[int]) -> tuple[int]:
    row_1, column_1 = coord_1
    row_2, column_2 = coord_2
    row_dif = row_2 - row_1
    column_dif = column_2 - column_1
    return row_dif, column_dif


def find_all_antinodes_p1(input_file: str) -> int:
    antennas, map_grid = read_in_map_and_antenna(input_file)
    all_antinodes = set()
    for antenna in antennas:
        all_row, all_column = np.where(map_grid == antenna)
        all_coords = list(zip(all_row, all_column))
        for coord_1 in all_coords:
            for coord_2 in all_coords:
                if coord_1 != coord_2:
                    row_dif, column_dif = get_row_col_diff(coord_1, coord_2)
                    antinode_1 = (coord_1[0] - row_dif, coord_1[1] - column_dif)
                    antinode_2 = (coord_2[0] + row_dif, coord_2[1] + column_dif)
                    if antinode_is_in_grid(antinode_1, map_grid):
                        all_antinodes.add(antinode_1)
                    if antinode_is_in_grid(antinode_2, map_grid):
                        all_antinodes.add(antinode_2)
    return len(all_antinodes)


def get_antinodes_for_antenna_p2(
    dif: tuple[int], start_coord: tuple[int], map_grid: np.ndarray, negative: bool
) -> set[tuple[int]]:
    antinodes = set()
    if negative:
        i = 0
        while True:
            antinode_1 = ((start_coord[0] - i * dif[0]), (start_coord[1] - i * dif[1]))
            if not antinode_is_in_grid(antinode_1, map_grid):
                break
            antinodes.add(antinode_1)
            i += 1
    else:
        j = 0
        while True:
            antinode_2 = ((start_coord[0] + j * dif[0]), (start_coord[1] + j * dif[1]))
            if not antinode_is_in_grid(antinode_2, map_grid):
                break
            antinodes.add(antinode_2)
            j += 1
    return antinodes


def find_all_antinodes_p2(input_file: str) -> int:
    antennas, map_grid = read_in_map_and_antenna(input_file)
    all_antinodes = set()
    for antenna in antennas:
        all_row, all_column = np.where(map_grid == antenna)
        all_coords = list(zip(all_row, all_column))
        for coord_1 in all_coords:
            for coord_2 in all_coords:
                if coord_1 != coord_2:
                    dif = get_row_col_diff(coord_1, coord_2)
                    antinodes_1 = get_antinodes_for_antenna_p2(
                        dif, coord_1, map_grid, True
                    )
                    antinodes_2 = get_antinodes_for_antenna_p2(
                        dif, coord_2, map_grid, False
                    )
                    all_antinodes.update(antinodes_1 | antinodes_2)
    return len(all_antinodes)


if __name__ == "__main__":
    print(find_all_antinodes_p1("day8/day8_final_input.txt"))
    print(find_all_antinodes_p2("day8/day8_final_input.txt"))
