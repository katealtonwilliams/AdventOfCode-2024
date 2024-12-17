import numpy as np
import copy
from typing import Callable


def create_map_p2(raw_map: list[str]) -> np.ndarray:
    new_map = []
    for line in raw_map:
        line = (
            line.replace("#", "##")
            .replace("O", "[]")
            .replace(".", "..")
            .replace("@", "@.")
        )
        new_map.append([*line])
    return np.array(new_map)


def read_in_map_and_dirs(input_file: str) -> tuple[np.ndarray, list]:
    with open(input_file) as raw_map_and_dirs:
        map_and_dirs = raw_map_and_dirs.read().split("\n")
    split_point = map_and_dirs.index("")
    map_grid = [[*line] for line in map_and_dirs[:split_point]]
    directions = []
    for line in map_and_dirs[split_point + 1 :]:
        directions.extend([*line])
    return np.array(map_grid), directions, create_map_p2(map_and_dirs[:split_point])


DIR_MAP = {"<": (0, -1), "^": (-1, 0), ">": (0, 1), "v": (1, 0)}


def move_blocks_p1(
    current_position: tuple[int],
    direction: tuple[int],
    new_position: tuple[int],
    current_grid: np.ndarray,
    positions_to_map: dict[tuple[int] : str],
) -> dict[str : tuple[int]] | None:
    o_position = copy.deepcopy(new_position)
    while current_grid[o_position] == "O":
        o_position = (o_position[0] + direction[0], o_position[1] + direction[1])
    if current_grid[o_position] == "#":
        return None
    positions_to_map[o_position] = "O"
    return positions_to_map, new_position


def map_blocks_up_and_down_p2(
    current_position: tuple[int],
    direction: tuple[int],
    new_position: tuple[int],
    current_grid: np.ndarray,
    positions_to_map: dict[tuple[int] : str],
) -> tuple[dict[tuple[int] : str], tuple[int]]:
    blocks_to_check = {current_position}
    seen_blocks = set()
    non_shifted_points = {}
    while blocks_to_check:
        position_to_check = blocks_to_check.pop()
        if position_to_check not in seen_blocks:
            new_position_to_check = (
                position_to_check[0] + direction[0],
                position_to_check[1],
            )
            if current_grid[new_position_to_check] == "#":
                return None
            if current_grid[new_position_to_check] == "[":
                blocks_to_check.add(new_position_to_check)
                non_shifted_points[new_position_to_check] = "["
                if (
                    current_grid[
                        new_position_right := (
                            new_position_to_check[0],
                            new_position_to_check[1] + 1,
                        )
                    ]
                    == "#"
                ):
                    return None
                else:
                    blocks_to_check.add(new_position_right)
                    non_shifted_points[new_position_right] = "]"
            if current_grid[new_position_to_check] == "]":
                blocks_to_check.add(new_position_to_check)
                non_shifted_points[new_position_to_check] = "]"
                if (
                    current_grid[
                        new_position_left := (
                            new_position_to_check[0],
                            new_position_to_check[1] - 1,
                        )
                    ]
                    == "#"
                ):
                    return None
                else:
                    blocks_to_check.add(new_position_left)
                    non_shifted_points[new_position_left] = "["
        seen_blocks.add(position_to_check)
    shifted_points = {
        (position[0] + direction[0], position[1]): block
        for position, block in non_shifted_points.items()
    }
    for point in non_shifted_points.keys():
        if point not in shifted_points:
            shifted_points[point] = "."
    return shifted_points | positions_to_map, new_position


def move_blocks_p2(
    current_position: tuple[int],
    direction: tuple[int],
    new_position: tuple[int],
    current_grid: np.ndarray,
    positions_to_map: dict[tuple[int] : str],
) -> dict[str : tuple[int]] | None:
    block_position = copy.deepcopy(new_position)
    if direction == (0, 1) or direction == (0, -1):
        while (
            current_grid[block_position] == "[" or current_grid[block_position] == "]"
        ):
            prev_position = copy.deepcopy(block_position)
            block_position = (block_position[0], block_position[1] + direction[1])
            if current_grid[block_position] == "#":
                return None
            positions_to_map[block_position] = current_grid[prev_position]
        return positions_to_map, new_position
    return map_blocks_up_and_down_p2(
        current_position, direction, new_position, current_grid, positions_to_map
    )


def move_one_step(
    arrow: str,
    current_position: tuple[int],
    current_grid: np.ndarray,
    move_blocks_func: Callable,
) -> dict[str : tuple[int]] | None:
    direction = DIR_MAP[arrow]
    new_position = (
        current_position[0] + direction[0],
        current_position[1] + direction[1],
    )
    positions_to_map = {}
    positions_to_map[new_position] = "@"
    positions_to_map[current_position] = "."
    if current_grid[new_position] == "#":
        return None
    if current_grid[new_position] == ".":
        positions_to_map[current_position] = "."
        return positions_to_map, new_position
    return move_blocks_func(
        current_position, direction, new_position, current_grid, positions_to_map
    )


def get_total_gps(current_grid: np.ndarray, block_shape: str) -> int:
    block_rows, block_columns = np.where(current_grid == block_shape)
    gps_coords = 0
    for block_row, block_column in zip(block_rows, block_columns):
        gps_coords += (100 * block_row) + block_column
    return gps_coords


def simulate_movement(
    input_file: str, move_blocks_func: Callable, block_shape: str, part: int
) -> int:
    if part == 1:
        current_grid, directions, _ = read_in_map_and_dirs(input_file)
    else:
        _, directions, current_grid = read_in_map_and_dirs(input_file)
    current_position = (
        np.where(current_grid == "@")[0][0],
        np.where(current_grid == "@")[1][0],
    )
    for arrow in directions:
        if (
            points_to_edit := move_one_step(
                arrow, current_position, current_grid, move_blocks_func
            )
        ) is not None:
            positions_to_map, new_position = points_to_edit
            for point, new_value in positions_to_map.items():
                current_grid[point] = new_value
            current_position = new_position
    return get_total_gps(current_grid, block_shape)


if __name__ == "__main__":
    print(simulate_movement("day15/day15_final_input.txt", move_blocks_p1, "O", 1))
    print(simulate_movement("day15/day15_final_input.txt", move_blocks_p2, "[", 2))
