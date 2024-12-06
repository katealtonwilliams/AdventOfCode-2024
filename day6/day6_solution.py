import numpy as np
from copy import deepcopy


def read_in_map(input_file: str) -> np.ndarray:
    with open(input_file) as raw_map:
        map_grid = [[*line.strip()] for line in raw_map.readlines()]
    return np.array(map_grid)


def get_next_direction(current_direction: tuple[int]) -> tuple[int]:
    direction_loop = {
        (-1, 0): (0, 1),
        (0, 1): (1, 0),
        (1, 0): (0, -1),
        (0, -1): (-1, 0),
    }
    return direction_loop[current_direction]


def pos_is_in_grid(pos: tuple[int], grid: np.ndarray) -> int:
    row, column = pos
    max_row, max_column = grid.shape
    if row < 0 or column < 0 or row > max_row - 1 or column > max_column - 1:
        return False
    return True


def get_full_route(input_file: str) -> int:
    map_grid = read_in_map(input_file)
    current_pos = np.where(map_grid == "^")[0][0], np.where(map_grid == "^")[1][0]
    current_direction = (-1, 0)
    visited_pos = set()
    visited_pos.add(current_pos)
    while True:
        next_pos = (
            current_direction[0] + current_pos[0],
            current_direction[1] + current_pos[1],
        )
        if not pos_is_in_grid(next_pos, map_grid):
            break
        if map_grid[next_pos] == "#":
            current_direction = get_next_direction(current_direction)
            next_pos = (
                current_direction[0] + current_pos[0],
                current_direction[1] + current_pos[1],
            )
        current_pos = next_pos
        visited_pos.add(current_pos)
    return len(visited_pos)


def find_next_pivot_point(
    current_pivot_point: tuple[int], current_direction: tuple[int], map_grid: np.ndarray
) -> tuple[int, int]:
    current_row, current_column = current_pivot_point

    if current_direction[1] == 0:
        next_pivot_column = current_column
        search_column = map_grid.T[current_column]

        if current_direction[0] == 1:
            if len(next_index := np.where(search_column[current_row:] == "#")[0]) == 0:
                return None
            next_pivot_row = next_index[0] + current_row - 1

        if current_direction[0] == -1:
            if (
                len(next_index := np.where(search_column[:current_row][::-1] == "#")[0])
                == 0
            ):
                return None
            next_pivot_row = current_row - next_index[0]

    if current_direction[0] == 0:
        next_pivot_row = current_row
        search_row = map_grid[current_row]

        if current_direction[1] == 1:
            if len(next_index := np.where(search_row[current_column:] == "#")[0]) == 0:
                return None
            next_pivot_column = next_index[0] + current_column - 1

        if current_direction[1] == -1:
            if (
                len(next_index := np.where(search_row[:current_column][::-1] == "#")[0])
                == 0
            ):
                return None
            next_pivot_column = current_column - next_index[0]

    return next_pivot_row, next_pivot_column


def creates_infinite_loop(map_grid: np.ndarray, block_position: tuple[int]) -> int:
    updated_grid = deepcopy(map_grid)
    updated_grid[block_position] = "#"
    pivot_point = (
        np.where(updated_grid == "^")[0][0],
        np.where(updated_grid == "^")[1][0],
    )
    current_direction = (-1, 0)
    pivot_points = []
    while True:
        pivot_point = find_next_pivot_point(
            pivot_point, current_direction, updated_grid
        )

        current_direction = get_next_direction(current_direction)

        if pivot_point is None:
            return False
        if (pivot_point, current_direction) in pivot_points:
            return True
        pivot_points.append((pivot_point, current_direction))


def find_infinite_loops(input_file: str) -> int:
    map_grid = read_in_map(input_file)
    infinite_loops_count = 0
    for row_index, row in enumerate(map_grid):
        for col_index, item in enumerate(row):
            if item != "#" and item != "^":
                infinite_loops_count += creates_infinite_loop(
                    map_grid, (row_index, col_index)
                )
    return infinite_loops_count


if __name__ == "__main__":
    print(get_full_route("day6/day6_final_input.txt"))
    print(find_infinite_loops("day6/day6_final_input.txt"))
