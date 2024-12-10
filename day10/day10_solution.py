import numpy as np


def read_in_map(practise_input: str) -> np.ndarray:
    with open(practise_input) as raw_map:
        return np.array(
            [list(map(int, [*line.strip()])) for line in raw_map.readlines()]
        )


DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]


def is_pos_in_grid(pos: tuple[int], grid: np.ndarray) -> bool:
    row, column = pos
    max_row, max_column = grid.shape
    if row < 0 or column < 0 or row > max_row - 1 or column > max_column - 1:
        return False
    return True


def get_next_steps(
    current_pos: tuple[int],
    current_height: int,
    start_pos: tuple[int],
    map_grid: np.ndarray,
) -> list[tuple[int]]:
    next_steps = []
    for direction in DIRECTIONS:
        new_position = (current_pos[0] + direction[0], current_pos[1] + direction[1])
        if (
            is_pos_in_grid(new_position, map_grid)
            and (new_height := map_grid[new_position]) == current_height + 1
        ):
            next_steps.append((new_position, new_height, start_pos))
    return next_steps


def find_all_paths_p1_p2(input_file: str) -> int:
    map_grid = read_in_map(input_file)
    start_rows, start_columns = np.where(map_grid == 0)
    paths = [
        ((start_row, start_column), 0, (start_row, start_column))
        for start_row, start_column in zip(start_rows, start_columns)
    ]
    finished_paths = []
    while paths:
        current_pos, current_height, start_pos = paths.pop()
        if current_height == 9:
            finished_paths.append((current_pos, start_pos))
            continue
        paths.extend(get_next_steps(current_pos, current_height, start_pos, map_grid))
    return len(set(finished_paths)), len(finished_paths)


if __name__ == "__main__":
    print(find_all_paths_p1_p2("day10/day10_final_input.txt"))
